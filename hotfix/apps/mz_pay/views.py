# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from fps_interface.interface import pay_attention_to_classmates
import qrcode
from cStringIO import StringIO
from django.conf import settings
from django.core.mail import send_mail

from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord
from mz_lps4.class_dict import NORMAL_CLASS_DICT, LPS4_DICT
from utils.alipay import create_direct_pay_by_user, notify_verify, notify_verify_rsa, params_filter, build_mysign, \
    app_create_direct_pay_by_user, wap_create_direct_pay_by_user
from utils.message_queue import mq_service
from utils.tool import generation_order_no, generate_random
from mz_course.views import get_careercourse_class, \
    get_careercourse_trystage_list, get_careercourse_balance_payment, get_careercourse_buybtn_status, \
    get_careercourse_lockstage_list, get_careercourse_allstage_list, is_unlock_in_stagelist, sys_send_message, \
    app_send_message
from mz_course.models import CareerCourse, Stage
from mz_lps.models import Class, ClassStudents
from mz_pay.models import UserPurchase
from mz_user.models import UserUnlockStage, MyCourse
from mz_course.views import get_real_amount
from mz_common.views import *
import logging, threading
from django.conf import settings
import hashlib
from django.shortcuts import get_object_or_404
import xml.etree.ElementTree as ET
import traceback
import requests
import hmac
import os
from utils.sms_manager import send_sms, get_templates_id, send_sms_new
from mz_user.functions_introduce import if_user_is_invited, if_first_register_course, update_invitation_course_info, \
    send_message
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
from core.common.http.response import success_json, failed_json
from urllib import quote_plus
from django.db.models import F
from db.api.course.course_task import get_career_course_knowledge_task_count
import db.api.lps.student
import db.api.onevone.meeting
import db.api.onevone.study_service
from utils.logger import logger as log

logger = logging.getLogger('mz_pay.views')
mutex = threading.Lock()


@login_required(login_url="/")
def goto_pay(request, careercourse_id, pay_type, class_coding, service_provider=1, other=None, has_discount=None):
    """
    服务端验证客户端支付数据，无误后跳转支付宝即时到账接口
    :param request:
    :return:
    """
    try:
        # 获取应该支付的金额
        if request.user.is_authenticated():
            # 获取优惠码
            code_sno = request.session.get('code_sno', None)
            money = request.session.get('money', None)
            # 得到当前职业课程对象
            cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
            # 判断当前班级是否已经达到人数上限student_limit、current_student_count
            try:
                cur_class = Class.objects.xall().get(coding=class_coding)
            except Class.DoesNotExist:
                return render(request, 'mz_common/failure.html', {'reason': '无此班级编号'})
            if pay_type in ("0", "1", "3", "6", "7"):
                # 判断该班级中是否已经有该学生
                cur_class = Class.objects.xall().get(coding=class_coding)
                if cur_class.students.filter(id=request.user.id).count() == 0:
                    if cur_class.current_student_count >= cur_class.student_limit:
                        return render(request, 'mz_common/failure.html', {'reason': '当前班级人数已经达到人数上限'})
                # 判断用户是否已经在职业课程所属的其他某个班级, 添加排除加入体验班
                if ClassStudents.objects.filter(
                        Q(user=request.user),
                        Q(student_class__career_course=cur_class.career_course),
                        Q(student_class__class_type=Class.CLASS_TYPE_NORMAL),
                        ~Q(student_class=cur_class)).exists():
                    class_students = ClassStudents.objects.get(
                        Q(user=request.user),
                        Q(student_class__career_course=cur_class.career_course),
                        Q(student_class__class_type=Class.CLASS_TYPE_NORMAL),
                        ~Q(student_class=cur_class))
                    return render(request, 'mz_common/failure.html',
                                  {'reason': '你已经加入该职业课程下的其他班级(' + class_students.student_class.coding + ')，不能重复加班'})

            # 需提交支付宝的参数
            order_no = generation_order_no()
            pay_amount = 0  # 支付金额
            pay_title = "职业课程：《" + cur_careercourse.name + "》"  # 支付名称
            pay_description = ""  # 支付描述
            # 需要解锁的阶段
            target_stage_list = []
            # 课程购买按钮的状态，0全款或首付款，1余款，2已经购买
            # pay_type 0 全额，1 试学首付款，2 尾款， 3 阶段款,6 无就业全款
            # 不以阶段方式购买
            if pay_type != "3":
                setattr(cur_careercourse, "buybtn_status",
                        get_careercourse_buybtn_status(request.user, cur_careercourse,
                                                       class_lps_version=cur_class.lps_version))
                if cur_careercourse.buybtn_status == 0:
                    if pay_type == "0":
                        # 职业课程所有阶段ID列表
                        target_stage_list = get_careercourse_allstage_list(cur_careercourse,
                                                                           class_lps_version=cur_class.lps_version)
                        # 全额
                        # setattr(cur_careercourse, "total_price",
                        #         get_careercourse_total_price(cur_careercourse, class_lps_version=cur_class.lps_version))
                        pay_description = "你现在正在支付《" + cur_careercourse.name + "》职业课程的全款,班级号：" + class_coding
                        pay_amount = cur_careercourse.net_price or 0
                        # 老带新立减
                        if if_user_is_invited(request.user.id) and if_first_register_course(request.user.id):
                            pay_amount -= 200
                    elif pay_type in ["1", "7"]:
                        # 职业课程试学阶段ID列表
                        target_stage_list = get_careercourse_trystage_list(cur_careercourse,
                                                                           class_lps_version=cur_class.lps_version)
                        # 试学首付
                        # setattr(cur_careercourse, "first_payment", get_careercourse_first_payment(cur_careercourse,
                        #                                                                           class_lps_version=cur_class.lps_version))
                        pay_description = "你现在正在支付《" + cur_careercourse.name + "》职业课程的首付款,班级号：" + class_coding
                        pay_amount = cur_careercourse.try_price
                    elif pay_type == "6":
                        # 职业课程所有阶段ID列表
                        target_stage_list = get_careercourse_allstage_list(cur_careercourse,
                                                                           class_lps_version=cur_class.lps_version)
                        # 无就业全额
                        pay_description = "你现在正在支付《" + cur_careercourse.name + "》职业课程的无就业全款,班级号：" + class_coding
                        if cur_careercourse.enable_free_488:
                            pay_amount = cur_careercourse.jobless_price
                        else:
                            pay_type = '0'
                            pay_amount = cur_careercourse.net_price

                        if pay_amount == None:
                            pay_amount = 0
                        # 老带新立减
                        if if_user_is_invited(request.user.id) and if_first_register_course(request.user.id):
                            pay_amount -= 200
                elif cur_careercourse.buybtn_status == 1:
                    if pay_type == "2":
                        # 职业课程未支付还处于解锁的所有阶段ID列表
                        target_stage_list = get_careercourse_lockstage_list(request.user, cur_careercourse,
                                                                            class_lps_version=cur_class.lps_version)
                        # 计算尾款应支付金额
                        # setattr(cur_careercourse, "balance_payment",
                        #         get_careercourse_balance_payment(request.user, cur_careercourse,
                        #                                          class_lps_version=cur_class.lps_version))
                        # 用户当前所属该职业课程下的某个班级
                        # setattr(cur_careercourse, "careercourse_class",
                        #         get_careercourse_class(request.user, cur_careercourse))
                        class_coding = get_careercourse_class(request.user, cur_careercourse)
                        cur_class = Class.objects.xall().get(coding=class_coding)
                        pay_description = "你现在正在支付《" + cur_careercourse.name + "》职业课程的余款,班级号：" + class_coding
                        pay_amount = get_careercourse_balance_payment(request.user, cur_careercourse,
                                                                      class_lps_version=cur_class.lps_version)
                        # 如果使用了优惠码，则减去对应的优惠金额
                        if code_sno is not None and money is not None:
                            pay_amount = int(pay_amount) - int(money)
                elif cur_careercourse.buybtn_status == 2:
                    return render(request, 'mz_common/failure.html', {'reason': '该职业课程已经完全解锁，不需再买'})
                else:
                    return render(request, 'mz_common/failure.html', {'reason': '未知的购买方式'})
            # lps2.0新增
            else:
                return render(request, 'mz_common/failure.html', {'reason': '未知的购买方式'})

            # lps2.0取消的代码
            # else:
            #     # 以阶段方式购买
            #     buy_status = get_careercourse_buybtn_status(request.user, cur_careercourse)
            #     if buy_status == 1 :
            #         class_coding = get_careercourse_class(request.user, cur_careercourse)
            #     stage = Stage.objects.get(pk=stage_id)
            #     target_stage_list.append(stage.id)
            #     pay_description="你现在正在支付《"+cur_careercourse.name+"》职业课程的《"+stage.name+"》阶段,班级号："+class_coding
            #     pay_amount = stage.price
            #
            # #检查要支付的目标阶段是否已经解锁，如已解锁则提醒错误
            # if is_unlock_in_stagelist(request.user, target_stage_list) :
            #     return render(request, 'mz_common/failure.html',{'reason':'待购买的课程阶段中包含已经解锁的阶段，请联系管理员'})

            # 生成订单并存入到数据库
            purchase = UserPurchase()
            purchase.user = request.user
            purchase.pay_price = pay_amount
            purchase.order_no = order_no
            purchase.pay_type = pay_type
            purchase.pay_way = int(service_provider)
            purchase.pay_status = 0
            purchase.pay_careercourse = cur_careercourse
            purchase.pay_class = cur_class
            # 订单管理需要存入支付时的价格
            purchase.net_price = cur_careercourse.net_price
            if pay_type == "0" and has_discount == '1':
                # 优惠金额
                purchase.pay_price = pay_amount - cur_careercourse.discounted_price
                purchase.discounted_price = cur_careercourse.discounted_price
                pay_amount = pay_amount - cur_careercourse.discounted_price
            elif has_discount == '2':
                discount = 1000 if int(careercourse_id) == 133 else 1500
                purchase.pay_price = pay_amount - discount
                purchase.discounted_price = discount
                pay_amount = pay_amount - discount
            elif has_discount == '3':
                if datetime.now() > datetime(2017, 1, 11):
                    discount = pay_amount-2999
                    pay_amount = 2999
                else:
                    discount = pay_amount-2799
                    pay_amount = 2799
                purchase.pay_price = pay_amount
                purchase.discounted_price = discount
            else:
                purchase.pay_price = pay_amount
                purchase.discounted_price = 0
            purchase.contract_price = cur_careercourse.contract_price
            if cur_careercourse.buybtn_status == 0 and pay_type in ["1", "7"]:
                if pay_type == "1":
                    purchase.final_payment_price = cur_careercourse.net_price - cur_careercourse.try_price - cur_careercourse.discounted_price
                else:
                    purchase.final_payment_price = cur_careercourse.jobless_price - cur_careercourse.try_price - cur_careercourse.discounted_price
            purchase.save()
            purchase.pay_stage = Stage.objects.xall().filter(id__in=target_stage_list)

            if code_sno is not None:
                purchase.coupon_code = code_sno
                request.session['code_sno'] = None
                request.session['money'] = None
            purchase.save()
            if int(service_provider) == 1:
                # 支付宝
                payurl = create_direct_pay_by_user(order_no, pay_title, pay_description, pay_amount, '')
                return render(request, 'mz_pay/tips.html', {'payurl': payurl, 'service_provider': '支付宝'})
            elif int(service_provider) == 2:
                # 移动支付宝
                paystr = app_create_direct_pay_by_user(order_no, pay_title, pay_description, pay_amount)
                data = dict(
                    paystr=paystr
                )
                return success_json(data)
            elif int(service_provider) == 3:
                # 移动微信
                result = app_wechat_pay(request, order_no)
                if result[0]:
                    data = dict(
                        weixinPay=result[1]
                    )
                    return success_json(data)
                return failed_json(u'服务器出问题了,请稍后再试')

            elif int(service_provider) == 5:
                # 么分期
                if not other:
                    return render(request, 'mz_common/failure.html', {'reason': '电话号码为空'})
                payurl = mi_me_pay(order_no, other)
                return render(request, 'mz_pay/mime_tips.html', {'payurl': payurl})
            elif int(service_provider) == 7:
                payurl = fen_qi_le_pay(request, order_no)
                return render(request, 'mz_pay/tips.html', {'payurl': payurl, 'service_provider': '分期乐'})
            elif int(service_provider) == 8:
                data = yee_pay(order_no, other)
                return render(request, 'mz_pay/yee_tips.html', {'data': data})
            elif int(service_provider) == 9:
                remain_student = cur_class.student_limit - cur_class.current_student_count
                data = uubee_pay(order_no, request.user, pay_type, class_coding, remain_student)
                return render(request, 'mz_pay/uubee_tips.html', {'data': data})
            elif int(service_provider) == 10:  # WAP端支付宝
                # WAP has different url from PC
                return_url = '%s%s' % (settings.MOBILE_SITE,
                                       reverse('pay:wap_alipay_return',
                                               kwargs=dict(career_course_short_name=cur_careercourse.short_name)))
                payurl = wap_create_direct_pay_by_user(order_no, pay_title, pay_description, pay_amount, return_url)
                return render(request, 'mz_pay/tips.html', {'payurl': payurl, 'service_provider': '支付宝'})
            else:
                # 微信
                return render(request, 'mz_pay/paydemo.html', {'course': cur_careercourse.name,
                                                               'fees': pay_amount,
                                                               'trade_no': order_no
                                                               })

        else:
            return render(request, 'mz_common/failure.html', {'reason': '请先登录再进行支付'})
    except Exception as e:
        logger.error(e)
        import traceback

        err = traceback.format_exc()
        logger.error(err)
        return render(request, 'mz_common/failure.html', {'reason': '服务器繁忙，请稍后再试'})


@require_GET
def wap_alipay_return(request, career_course_short_name):
    """
    WAP端支付宝支付成功后同步处理跳转告知用户
    :param request:
    :return:
    @todo 处理支付失败的情况
    """
    order_no = request.GET.get('out_trade_no')
    course_url = reverse('career_course_detail', kwargs=dict(course_id=career_course_short_name))

    try:
        verify_result = notify_verify(request.GET)  # 解码并验证数据是否有效
        if verify_result:
            trade_no = request.GET.get('trade_no')
            trade_status = request.GET.get('trade_status')
            total_fee = request.GET.get('total_fee')
            result = order_handle(trade_status, order_no, trade_no, total_fee)
            if result[0] == "success":
                order_handler_sucess_sendsms(order_no)
                return HttpResponseRedirect(course_url)
        else:
            return render(request, 'mz_pay/wap_pay_fail.html', {'url': course_url, 'order_no': order_no})
    except Exception as e:
        logger.error(e)

    return render(request, 'mz_pay/wap_pay_fail.html', {'url': course_url, 'order_no': order_no})

@csrf_exempt
def alipay_notify(request):
    '''
    支付成功后异步通知处理
    :param request:
    :return:
    '''
    try:
        if request.method == 'POST':
            verify_result = notify_verify(request.POST)  # 解码并验证数据是否有效
            if verify_result:
                order_no = request.POST.get('out_trade_no')
                trade_no = request.POST.get('trade_no')
                trade_status = request.POST.get('trade_status')
                total_fee = request.POST.get('total_fee')
                result = order_handle(trade_status, order_no, trade_no, total_fee)
                if result[0] == 'success':
                    return HttpResponse('success')  # 有效数据需要返回 'success' 给 alipay
    except Exception as e:
        logger.error(e)
    return HttpResponse('fail')


def alipay_app_notify(request):
    try:
        if request.method == 'POST':
            verify_result = notify_verify_rsa(request.POST)  # 解码并验证数据是否有效
            if verify_result:
                order_no = request.POST.get('out_trade_no')
                trade_no = request.POST.get('trade_no')
                trade_status = request.POST.get('trade_status')
                total_fee = request.POST.get('total_fee')
                result = order_handle(trade_status, order_no, trade_no, total_fee)
                if result[0] == 'success':
                    return HttpResponse('success')  # 有效数据需要返回 'success' 给 alipay
    except Exception as e:
        logger.error(e)
    return HttpResponse('fail')


def alipay_return(request):
    '''
    支付成功后同步处理跳转告知用户
    :param request:
    :return:
    '''
    try:
        if request.method == 'GET':
            verify_result = notify_verify(request.GET)  # 解码并验证数据是否有效
            if verify_result:
                order_no = request.GET.get('out_trade_no')
                trade_no = request.GET.get('trade_no')
                trade_status = request.GET.get('trade_status')
                total_fee = request.GET.get('total_fee')
                result = order_handle(trade_status, order_no, trade_no, total_fee)
                if result[0] == "success":
                    order_handler_sucess_sendsms(order_no)
                    return render(request, 'mz_pay/success.html',
                                  {'careercourse_name': result[3], 'url': '/lps2/learning/plan/' + str(result[2]) + '/',
                                   'total_fee': total_fee})
            else:
                order_no = request.GET.get('out_trade_no', '')
                url, _, _, _ = get_error_url(order_no)
                return render(request, 'mz_pay/error.html', {'url': url})
    except Exception as e:
        logger.error(e)

    order_no = request.GET.get('out_trade_no', '')
    url, _, _, _ = get_error_url(order_no)

    return render(request, 'mz_pay/error.html', {'url': url})


def get_error_url(order_no):
    try:
        purchase = UserPurchase.objects.get(order_no=order_no)
        career_course_id = purchase.pay_careercourse.id
        career_course_name = purchase.pay_careercourse.name
        pay_money = purchase.pay_money
        return '/pay/view/?career_id=' + str(career_course_id), career_course_id, career_course_name, pay_money
    except UserPurchase.DoesNotExist:
        return '/course/', '', '', '', ''


# 根据支付宝返回结果处理解锁和订单结果
@transaction.commit_manually
def order_handle(trade_status, order_no, trade_no, total_fee):
    mutex.acquire()
    try:
        # 根据商户订单号查询到对应订单信息
        purchase = UserPurchase.objects.get(order_no=order_no)
        # 更新优惠码信息
        if purchase.coupon_code:
            coupon = Coupon_Details.objects.get(code_sno=purchase.coupon_code)
            coupon_obj = Coupon.objects.get(id=coupon.coupon_id)
            coupon.user = purchase.user
            coupon.is_use = True
            coupon.use_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            coupon.save()
            coupon_obj.surplus -= 1
            coupon_obj.save()
        # 如果已经报名体验班级，先退出体验班级
        enjoin_class = Class.objects.xall().filter(
            students=purchase.user,
            career_course=purchase.pay_class.career_course, class_type=Class.CLASS_TYPE_EXPERIENCE)
        if enjoin_class:
            enjoin_class[0].current_student_count -= 1
            enjoin_class[0].save()
            ClassStudents.objects.filter(student_class=enjoin_class[0],
                                         user=purchase.user).delete()

        # 如果是lps3.1试学班，删除任务记录
        experience_3_1_class = Class.objects.xall().filter(
            students=purchase.user, career_course=purchase.pay_class.career_course,
            class_type=Class.CLASS_TYPE_EXPERIENCE_3_1)
        if experience_3_1_class:
            # 删除学生3.1体验班级记录
            experience_3_1_class = experience_3_1_class[0]
            experience_3_1_class.current_student_count -= 1
            experience_3_1_class.save()
            ClassStudents.objects.filter(student_class=experience_3_1_class, user=purchase.user).delete()
            # 删除用户学习记录
            UserKnowledgeItemRecord.objects.filter(
                student_id=purchase.user.id, class_id=experience_3_1_class.id).delete()
            UserTaskRecord.objects.filter(student_id=purchase.user.id, class_id=experience_3_1_class.id).delete()

        # 订单对应班级
        cur_class = Class.objects.xall().get(coding=purchase.pay_class.coding)
        return_qq = cur_class.qq
        return_qq_key = cur_class.qq_key if cur_class.qq_key else ''
        return_career_id = cur_class.career_course.id
        return_career_name = cur_class.career_course.name
        if purchase.pay_status == 1:
            transaction.rollback()
            mutex.release()
            return ("success", return_qq, return_career_id, return_career_name, return_qq_key)
        if trade_status in ('TRADE_FINISHED', 'TRADE_SUCCESS'):
            # 获取lps3.1老师信息
            career_id = purchase.pay_class.career_course.id
            teacher = db.api.onevone.study_service.get_service_teacher(career_id)
            if teacher.is_error():
                log.warn('get_service_teacher is error. career_id: %s' % career_id)
                teacher = ()
            else:
                teacher = teacher.result()

            # 解锁相应的阶段
            # 获取该订单对应的阶段
            for stage in purchase.pay_stage.xall().filter(userpurchase=purchase):
                try:
                    unlock_stage, created = UserUnlockStage.objects.get_or_create(user=purchase.user, stage=stage)
                except Exception as e:
                    logger.error(str(e))

            # 修改班级目前报名人数和更新学员到对应班级
            if cur_class.students.filter(pk=purchase.user.id).count() == 0:
                cur_class.current_student_count += 1
                cur_class.save()
                class_students = ClassStudents()
                class_students.student_class = cur_class
                class_students.user = purchase.user
                if purchase.pay_careercourse.enable_free_488 and purchase.pay_type in [6, 7]:  # 无就业全款 无就业首付款
                    class_students.is_employment_contract = False
                if purchase.pay_careercourse.enable_free_488 and purchase.pay_type in [0, 1]:  # 就业全款   就业首付款
                    class_students.is_employment_contract = True
                # 获取当前学力
                if not cur_class.lps_version == '3.0':
                    class_students.study_point = get_study_point(purchase.user, cur_class.career_course)

                try:
                    class_students.save()
                except Exception as e:
                    logger.error(str(e))

            # 根据付款方式（首付、全额、余款）来更新班级权限使用的截止时间
            class_students = ClassStudents.objects.get(student_class=cur_class, user=purchase.user)
            if purchase.pay_type in [1, 7]:
                # 首付计算截止时间(90天)

                class_students.deadline = datetime.now() + timedelta(days=90)

            elif purchase.pay_type == 0 or purchase.pay_type == 2:
                # 截止时间为None表示全额或余款支付，没有截止时间限制
                class_students.deadline = None

            class_students.save()

            # 添加到lps4的班
            if purchase.pay_class.id in NORMAL_CLASS_DICT.values():
                user_id = purchase.user.id
                lps4_student_type = 0 if purchase.pay_type == 6 else 1

                if teacher:
                    teacher_id = teacher[0]['teacher_id']
                else:
                    teacher_id = 4  # 王海宁的id

                if purchase.pay_price in [2799, 2999]:
                    #　大学生优惠
                    time_graduate = datetime.now() + timedelta(days=60)
                else:
                    time_graduate = datetime.now() + timedelta(days=180)

                db.api.lps.student.insert_user_to_normal_class(
                    user_id, lps4_student_type, career_id, teacher_id, datetime.now(), time_graduate)
                # 更新直播次数
                db.api.onevone.meeting.get_onevone_meeting_user_count(user_id, career_id)

            # 添加职业课程到我的课程
            if MyCourse.objects.filter(user=purchase.user, course=purchase.pay_careercourse.id,
                                       course_type=2).count() == 0:
                my_course = MyCourse()
                my_course.user = purchase.user
                my_course.course = purchase.pay_careercourse.id
                my_course.course_type = 2
                my_course.index = 1
                my_course.save()

            # 改变该订单的状态
            purchase.trade_no = trade_no
            purchase.date_pay = datetime.now()
            purchase.pay_status = 1
            purchase.pay_money = int(float(total_fee))
            purchase.save()
            transaction.commit()
            mutex.release()

            # ### 给学生发送通知消息 开始 ####
            is_lps4 = LPS4_DICT.get(int(cur_class.id))
            # 发送到运营消息队列服务
            if is_lps4:
                try:
                    institute = Institute.objects.get(id=purchase.pay_careercourse.institute_id)
                except Institute.DoesNotExist:
                    institute = None
                if institute:
                    result = db.api.onevone.study_service.get_teacher_info_by_lps4(career_id=is_lps4,
                                                                                   student_id=int(purchase.user.id))
                    if not result.is_error():
                        if result.result():
                            teacher = result.result()
                            r = mq_service.publish({
                                "event": "user_pay_info_sync",
                                "data": {
                                    "user_id": purchase.user.id,
                                    "nick_name": purchase.user.nick_name,
                                    "career_id": purchase.pay_careercourse.id,
                                    "career_name": purchase.pay_careercourse.name,
                                    "teacher_id": teacher['id'],
                                    "teacher_name": teacher['real_name'] or teacher['nick_name'],
                                    "teacher_mobile": teacher['mobile'],
                                    "domain": institute.name,
                                }
                            })
                            log.info('mq_user_pay_info_sync: %s' % str(r))
                    else:
                        log.warn('order handle db.api.onevone.study_service.get_teacher_by_lps4')

            # 发送站内信
            if is_lps4:
                href = reverse('lps4_index', kwargs={"career_id": is_lps4})
            else:
                href = 'http://www.maiziedu.com/lps3/student/class/%s' % cur_class.id
            alert_msg = "您已成功报名课程#" + return_career_name + "#。快和小麦一起，开启精彩学习之旅吧~"
            sys_send_message(0, purchase.user.id, 50,
                             alert_msg + "<a href='%s'>进入学习面板>></a>" % href)

            # 给报名的学生发短信
            student_mobile = class_students.user.mobile
            if student_mobile:
                send_sms_new(student_mobile, 'pay_success_4_0', [purchase.pay_class.career_course.name,
                                                                 str(purchase.pay_price)])
            # 给学生发邮件
            student_email = class_students.user.email
            if student_email:
                student_email_msg = """
亲爱的同学，恭喜你支付成功！正式入学麦子学院“%s专业”，接下来请你务必完善入学信息，以便老师与你进行第一次的入学沟通和开启你全新的麦子学习生涯。

新同学，点击%s立即开始学习！

您付款金额为：%s，如有疑请致电4008628862【麦子学院】

                """ % (purchase.pay_careercourse.name, settings.SITE_URL + href, str(purchase.pay_price))
                try:
                    send_mail(settings.EMAIL_SUBJECT_PREFIX + "入学欢迎邮件", student_email_msg,
                              settings.EMAIL_FROM, [student_email])
                except Exception as e:
                    logger.error(e)

            # 给销售发送邮件
            email = 'xiaoshoudingdan@maiziedu.com'
            email_msg = '麦子账号:' + purchase.user.username + ';'
            email_msg += '订单号:' + order_no + ';'
            email_msg += '班级编号:' + cur_class.coding + ';'
            email_msg += '金额:' + str(purchase.pay_price) + ';'
            email_msg += '交易号:' + trade_no + ';'
            email_msg += '支付成功时间:' + datetime.now().strftime("%Y-%m-%d %H:%M") + ';'
            email_msg += '支付方式:' + purchase.PAY_WAYS.get(purchase.pay_way) + ';'

            # 麦子账号，订单号，报名课程编号（例如：WEB20160331），金额，交易号（微信支付是1开头的一串数字，支付宝支付是2开头的一串数字），支付成功时间，支付方式
            try:
                send_mail(settings.EMAIL_SUBJECT_PREFIX + "订单支付成功信息", email_msg, settings.EMAIL_FROM, [email])
            except Exception as e:
                logger.error(e)
            return ("success", return_qq, return_career_id, return_career_name, return_qq_key)
        elif trade_status == "WAIT_BUYER_PAY":
            transaction.rollback()
            mutex.release()
            return ("fail", "lose")
        else:
            purchase.pay_status = 2
            purchase.save()
            transaction.commit()
            mutex.release()
            return ("fail", "lose")
    except Exception as e:
        logger.error(traceback.format_exc())
        transaction.rollback()
        mutex.release()
    return ("fail", "lose")


# 支付界面
def pay_view(request):
    career_ids = request.GET.get('career_ids', None)
    # 屏蔽老支付接口
    if career_ids is None:
        return render(request, 'mz_common/failure.html', {'reason': '职业课程ID不能为空'})
    career_ids = career_ids.split(',')
    return HttpResponseRedirect('/pay/view/?career_id=' + str(career_ids[0]))

    career_course_list = []
    passresponse_data = []
    try:
        if career_ids is None:
            return render(request, 'mz_common/failure.html', {'reason': '职业课程ID不能为空'})
        if not request.user.is_authenticated():
            return render(request, 'mz_common/failure.html', {'reason': '请登录后再进行支付'})

        # 分解职业ID参数
        career_ids = career_ids.split(',')
        # 获取职业课程、价格还有对应的班级信息
        career_course_list = CareerCourse.objects.filter(pk__in=career_ids).order_by("id")
        career_course_list_count = len(career_course_list)

        for career_course in career_course_list:
            lps_version = None
            class_coding = get_careercourse_class(request.user, career_course)
            if class_coding:
                lps_version = Class.objects.xall().get(coding=class_coding).lps_version
            # 根据不同情况获取不同的支付金额
            career_course = get_real_amount(request.user, career_course, lps_version=lps_version)
            if career_course.buybtn_status == 1:
                careercourse_class = Class.objects.xall().get(coding=career_course.careercourse_class)
                passresponse_data = [{
                    "buybtn_status": str(career_course.buybtn_status),
                    "first_pay": str(career_course.first_payment),
                    "balance_pay": str(career_course.balance_payment),
                    "teacher": careercourse_class.teacher,
                    "all_pay": str(career_course.total_price),
                    "class_list": [{"id": str(careercourse_class.id),
                                    "coding": str(careercourse_class.coding),
                                    "name": str(careercourse_class.display_name),
                                    "student_limit": str(careercourse_class.student_limit),
                                    "current_student_count": str(careercourse_class.current_student_count)}
                                   ]
                }]
            else:
                # 该职业课程下所有开放的班级
                teacher_list = career_course.class_set.xall().filter(career_course=career_course).filter(is_active=True,
                                                                                                         status=1,
                                                                                                         is_closed=False).values(
                    'teachers').distinct()
                for teacher in teacher_list:
                    teacher = UserProfile.objects.get(id=teacher['teachers'])
                    career_course_class_list = Class.objects.xall().filter(teachers=teacher, status=1, is_closed=False,
                                                                           career_course=career_course)

                    passresponse_data_meta = {
                        "buybtn_status": str(career_course.buybtn_status),
                        "first_pay": str(career_course.first_payment),
                        "balance_pay": str(career_course.balance_payment) if career_course.buybtn_status == 1 else "-1",
                        "all_pay": str(career_course.total_price),
                        "teacher": teacher,
                        "class_list": [{"id": str(_class.id),
                                        "coding": str(_class.coding),
                                        "name": str(_class.display_name),
                                        "student_limit": str(_class.student_limit),
                                        "current_student_count": str(_class.current_student_count),
                                        "teacher": str(_class.teacher.nick_name)}
                                       for _class in career_course_class_list]
                    }
                    passresponse_data.append(passresponse_data_meta)
    except Exception as e:
        logger.error(e)
    is_memedai_preferential = False
    if (datetime.now() < datetime(2016, 2, 7, 23, 59, 59)) and (datetime.now() > datetime(2016, 1, 25)):
        if career_ids[0] in ['13', '6', '2']:
            is_memedai_preferential = True
    return render(request, 'mz_pay/pay.html',
                  {'career_course_list': career_course_list, "passresponse_data": passresponse_data,
                   'career_course_list_count': career_course_list_count,
                   'is_memedai_preferential': is_memedai_preferential})


# 支付界面
def pay_view2(request):
    career_id = request.GET.get('career_id', None)
    # 是否是分期
    loan = request.GET.get('loan', '0')
    fql = request.GET.get('fql')
    # 老带新转介绍判断
    old_invit_new_status = False
    try:
        if career_id is None:
            return render(request, 'mz_common/failure.html', {'reason': '职业课程ID不能为空'})
        if not request.user.is_authenticated():
            return render(request, 'mz_common/failure.html', {'reason': '请登录后再进行支付'})

        # 获取职业课程、价格还有对应的班级信息
        career_course_list = CareerCourse.objects.select_related().filter(pk=career_id).order_by("id")
        if not career_course_list:
            return render(request, 'mz_common/failure.html', {'reason': '职业课程ID错误'})
        career_course = career_course_list[0]

        lps_version = None
        class_coding = get_careercourse_class(request.user, career_course)
        if class_coding:
            lps_version = Class.objects.xall().get(coding=class_coding).lps_version
        # 根据不同情况获取不同的支付金额
        career_course = get_real_amount(request.user, career_course, lps_version=lps_version)
        if career_course.buybtn_status == 1:
            careercourse_class = Class.objects.xall().get(coding=career_course.careercourse_class)

            # lps_version = careercourse_class.lps_version
            # career_course = get_real_amount(request.user, career_course, lps_version=lps_version)
            # 加入了班级但是已经退学的情况
            class_quit = False
            if ClassStudents.objects.filter(student_class=careercourse_class, user=request.user, status=2).count() > 0:
                class_quit = True
            # 查询首付款订单中的优惠金额
            discounted_price = 0
            user_purs = UserPurchase.objects.select_related().filter(user=request.user, pay_careercourse=career_course,
                                                                     pay_status=1, pay_type__in=[1, 7]).order_by("-id")
            if user_purs.count() > 0:
                discounted_price = user_purs[0].discounted_price
            passresponse_data_meta = {
                "buybtn_status": str(career_course.buybtn_status),
                "first_pay": str(career_course.first_payment),
                "discounted_price": discounted_price,
                "all_balance_pay": discounted_price + career_course.balance_payment,
                "balance_pay": career_course.balance_payment if not class_quit else 0,
                "teacher": careercourse_class.teacher,
                "all_pay": str(career_course.total_price),
                "career_id": career_course.id,
                "lps_version": lps_version,
                "class": {"id": str(careercourse_class.id),
                          "coding": str(careercourse_class.coding),
                          "name": str(careercourse_class.name if careercourse_class.name else ''),
                          "student_limit": str(careercourse_class.student_limit),
                          "current_student_count": str(careercourse_class.current_student_count)}
            }
        else:
            if ClassStudents.objects.filter(
                    student_class__career_course=career_course, user=request.user,
                    student_class__class_type=Class.CLASS_TYPE_NORMAL
            ).exists():
                return render(request, 'mz_common/failure.html', {'reason': '已经报名该课程！'})
            # 是否已经报名试学班,如果报名试学班则删除
            # ClassStudents.objects.filter(student_class__career_course=career_course, student_class__type=1, user=request.user).delete()
            # 该职业课程下所有开放的班级
            careercourse_class_list = Class.objects.xall() \
                .filter(career_course=career_course, status=1, is_closed=False, is_active=True) \
                .filter(class_type=Class.CLASS_TYPE_NORMAL) \
                .filter(current_student_count__lt=F('student_limit')).order_by('id')
            if not careercourse_class_list:
                return render(request, 'mz_common/failure.html', {'reason': '该职业课程没有开班，请联系客服'})
            careercourse_class = careercourse_class_list[0]

            lps_version = careercourse_class.lps_version
            career_course = get_real_amount(request.user, career_course, lps_version=lps_version)

            teacher = careercourse_class.teacher

            passresponse_data_meta = {"buybtn_status": str(career_course.buybtn_status),
                                      "first_pay": str(career_course.first_payment),
                                      "balance_pay": str(
                                          career_course.balance_payment) if career_course.buybtn_status == 1 else "-1",
                                      "all_pay": str(career_course.total_price),
                                      "jobless_price": str(career_course.jobless_price),
                                      "jobless_discounted_price": str(
                                          career_course.total_price - (career_course.jobless_price or 0)),
                                      "teacher": teacher,
                                      "career_id": career_course.id,
                                      "lps_version": lps_version,
                                      "class": {"id": str(careercourse_class.id),
                                                "coding": str(careercourse_class.coding),
                                                "name": str(careercourse_class.name if careercourse_class.name else ''),
                                                "student_limit": str(careercourse_class.student_limit),
                                                "current_student_count": str(careercourse_class.current_student_count),
                                                "teacher": str(careercourse_class.teacher.nick_name)}
                                      }

            if if_user_is_invited(request.user.id) and if_first_register_course(request.user.id):
                old_invit_new_status = True
                passresponse_data_meta['old_pay'] = passresponse_data_meta['all_pay']
                passresponse_data_meta['all_pay'] = str(int(passresponse_data_meta['all_pay']) - 200)
                passresponse_data_meta['old_jobless_price'] = passresponse_data_meta['jobless_price']
                passresponse_data_meta['jobless_price'] = str(int(passresponse_data_meta['jobless_price']) - 200)

    except Exception as e:
        logger.error(e)
    # 么么贷限时优惠（已经到期）
    # is_memedai_preferential = False
    # if (datetime.now() < datetime(2016, 2, 7, 23, 59, 59)) and (datetime.now() > datetime(2016, 1, 25)):
    #     if career_id in ['13', '6', '2']:
    #         is_memedai_preferential = True
    # 分期乐首付款
    if fql:
        if career_course.buybtn_status == 0:
            return render(request, 'mz_pay/pay_step_fql.html',
                      {'career_course': career_course, "passresponse_data": passresponse_data_meta,
                       'old_invit_new_status': old_invit_new_status})
    return render(request, 'mz_pay/pay_step.html',
                  {'career_course': career_course, "passresponse_data": passresponse_data_meta, "loan": loan,
                   'old_invit_new_status': old_invit_new_status})


def pay_view3(request):
    career_id = request.GET.get('career_id', None)
    index = request.GET.get('index', None)
    fql = request.GET.get('fql')
    off = request.GET.get('off', None)
    new_year = request.GET.get('year-end-special', None)
    college_student = request.GET.get('college-student', None)
    if not request.user.is_authenticated():
        return render(request, 'mz_common/failure.html', {'reason': '请登录后再进行支付'})
    if fql:
        return pay_view2(request)
    if career_id is None:
        return render(request, 'mz_common/failure.html', {'reason': '职业课程ID不能为空'})

    # 获取职业课程
    try:
        career_course = CareerCourse.objects.get(pk=career_id)

    except CareerCourse.DoesNotExist:
        return render(request, 'mz_common/failure.html', {'reason': '职业课程ID错误'})
    lps_version = None
    class_coding = get_careercourse_class(request.user, career_course)
    if class_coding:
        lps_version = Class.objects.xall().get(coding=class_coding).lps_version
    # 根据不同情况获取不同的支付金额
    career_course = get_real_amount(request.user, career_course, lps_version=lps_version)
    if career_course.buybtn_status == 1:
        careercourse_class = Class.objects.xall().get(coding=career_course.careercourse_class)
        if ClassStudents.objects.filter(student_class=careercourse_class, user=request.user, status=2).exists():
            return render(request, 'mz_common/failure.html', {'reason': '你已退学当前课程'})
    else:
        if ClassStudents.objects.filter(
                    student_class__career_course=career_course, user=request.user,
                    student_class__class_type=Class.CLASS_TYPE_NORMAL).exists():
            return render(request, 'mz_common/failure.html', {'reason': '已经报名该课程！'})
        # lps3.1改成直接从NORMAL_CLASS_DICT里面取那个唯一的班
        try:
            class_id = NORMAL_CLASS_DICT[int(career_id)]
        except KeyError:
            # 该职业课程下所有开放的班级
            careercourse_class_list = Class.objects.xall() \
                .filter(career_course=career_course, status=1, is_closed=False, is_active=True) \
                .filter(class_type=Class.CLASS_TYPE_NORMAL) \
                .filter(current_student_count__lt=F('student_limit')).order_by('id')
            if not careercourse_class_list:
                return render(request, 'mz_common/failure.html', {'reason': '该职业课程没有开班，请联系客服'})
            careercourse_class = careercourse_class_list[0]
        else:
            try:
                careercourse_class = Class.objects.xall().get(id=class_id)
            except Class.DoesNotExist:
                return render(request, 'mz_common/failure.html', {'reason': '该职业课程没有开班，请联系客服'})

        lps_version = careercourse_class.lps_version
        career_course = get_real_amount(request.user, career_course, lps_version=lps_version)

        # lps3.1修改，为了让支付成功跳转可以区分开
        if NORMAL_CLASS_DICT.has_key(careercourse_class.id):
            lps_version = '3.1'
    has_discount = 0
    if off:
        # 折扣优惠
        has_discount = 1
        career_course.net_price = career_course.net_price - career_course.discounted_price
    elif new_year:
        # 年终优惠
        has_discount = 2
        if int(career_id) == 133:
            # 互联网商学院
            career_course.net_price = career_course.net_price - 1000
            career_course.jobless_price = career_course.jobless_price - 1000
        else:
            career_course.net_price = career_course.net_price - 1500
            career_course.jobless_price = career_course.jobless_price - 1500
    elif college_student:
        if datetime.now() > datetime(2017, 1, 11):
            career_course.jobless_price = 2999
        else:
            career_course.jobless_price = 2799
        index = '1'
        has_discount = 3
    return render(request, 'mz_pay/new_pay.html', {'index': index,
                                                   'career_id':career_id,
                                                   'lps_version': lps_version,
                                                   'short_name': career_course.short_name,
                                                   'career_course': career_course,
                                                   'has_discount': has_discount,
                                                   "careercourse_class": careercourse_class,
                                                   'lps_count': get_career_course_knowledge_task_count(career_id).result()})


# 支付界面 - 根据职业课程ID获取班级信息
@csrf_exempt
def get_class_list_by_career_id(request):
    career_id = request.GET.get('career_id', None)
    # zhangyu
    lps_version = None
    class_id = request.GET.get('class_id', None)
    if class_id:
        course_class = Class.objects.xall().filter(id=class_id)
        if course_class:
            lps_version = course_class[0].lps_version
    try:
        try:
            career_course = CareerCourse.objects.get(pk=career_id)
        except CareerCourse.DoesNotExist:
            return HttpResponse('{"status": "failure", "data": "没有该职业课程"}', content_type="application/json")

        # 该职业课程下所有开放的班级
        career_course_class_list = career_course.class_set.xall().filter(career_course=career_course).filter(
            is_active=True, status=1, is_closed=False)

        # 根据不同情况获取不同的支付金额
        if lps_version:
            career_course = get_real_amount(request.user, career_course, lps_version)
        else:
            career_course = get_real_amount(request.user, career_course)
        if career_course.buybtn_status == 1:
            careercourse_class = Class.objects.xall().get(coding=career_course.careercourse_class)
            career_course_class_list = career_course.class_set.xall().filter(career_course=career_course).filter(
                is_active=True, status=1)

        # 0显示全款支付和试学首付,1显示尾款支付按钮，2显示已经购买
        response_data = {
            "buybtn_status": str(career_course.buybtn_status),
            "first_pay": str(career_course.first_payment),
            "balance_pay": str(career_course.balance_payment) if career_course.buybtn_status == 1 else "-1",
            "all_pay": str(career_course.total_price),
            "class_list": [{"id": str(careercourse_class.id),
                            "coding": str(careercourse_class.coding),
                            "student_limit": str(careercourse_class.student_limit),
                            "current_student_count": str(careercourse_class.current_student_count),
                            "teacher": str(careercourse_class.teacher.nick_name)}]
            if career_course.buybtn_status == 1 else
            [{"id": str(_class.id),
              "coding": str(_class.coding),
              "student_limit": str(_class.student_limit),
              "current_student_count": str(_class.current_student_count),
              "teacher": str(_class.teacher.nick_name)}
             for _class in career_course_class_list]
        }

    except Exception as e:
        logger.error(e)
        return HttpResponse('{"status": "failure", "data": "服务器出错了，请联系客服: 400-862-8862"}',
                            content_type="application/json")

    return HttpResponse('{"status": "success", "data": ' + json.dumps(response_data) + '}',
                        content_type="application/json")


@csrf_exempt
def wechat_pay(request):
    '''
    支付成功后异步通知处理
    :param request:
    :return:
    '''
    try:
        if request.method == 'POST':
            root = ET.fromstring(request.body)
            out_trade_no = ''
            nonce_str = ''
            transaction_id = ''
            total_fee = ''
            result_code = ''
            for child in root._children:
                if child.tag == 'out_trade_no':
                    out_trade_no = child.text
                elif child.tag == 'nonce_str':
                    nonce_str = child.text
                elif child.tag == 'transaction_id':
                    transaction_id = child.text
                elif child.tag == 'total_fee':
                    total_fee = child.text
                elif child.tag == 'result_code':
                    result_code = child.text
            if total_fee:
                total_fee = float(total_fee) / 100
            logger.info("wechat_pay:" + out_trade_no + ":" + nonce_str)
            order = get_object_or_404(UserPurchase, order_no=out_trade_no)
            if order:
                if result_code == 'SUCCESS':
                    result = order_handle('TRADE_SUCCESS', out_trade_no, transaction_id, total_fee)
                    if result[0] == 'success':
                        order_handler_sucess_sendsms(out_trade_no)
                        return_xml = """
                                        <xml>
                                            <return_code><![CDATA[SUCCESS]]></return_code>
                                            <return_msg><![CDATA[OK]]></return_msg>
                                        </xml>
                                     """
                        return HttpResponse(return_xml, content_type="application/xml")
    except Exception as e:
        logger.error(e)
    return_xml = """
                    <xml>
                        <return_code><![CDATA[FAIL]]></return_code>
                        <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                 """
    return HttpResponse(return_xml, content_type="application/xml")


def query_trade_status(request, order_no):
    # 微信支付二维码页面js动态查询订单状态
    query_result = {
        "status": "success",
        "pay_status": "",
        "msg": ""}

    user_purchases = UserPurchase.objects.filter(order_no=order_no, user=request.user)
    if user_purchases:
        user_purchase = user_purchases[0]
        pay_status = user_purchase.pay_status
        query_result["pay_status"] = pay_status
    else:
        query_result["status"] = "fail"
        query_result["msg"] = "订单不存在"
    return HttpResponse(json.dumps(query_result), content_type="application/json")


def render_success_view(request, order_no):
    # 微信支付成功后页面跳转
    url, career_course_id, career_course_name, total_fee = get_error_url(order_no)
    if url != '/course/':
        return render(request, 'mz_pay/success.html',
                      {'careercourse_name': career_course_name,
                       'url': '/lps2/learning/plan/' + str(career_course_id) + '/',
                       'total_fee': total_fee})
    return render(request, 'mz_pay/error.html', {'url': url})


def go_wechat_pay(request, order_no, app_id, mch_id, wechat_type, key):
    # 获取用户ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        _temp_ip_list = request.META.get('HTTP_X_FORWARDED_FOR').split(',')
        if len(_temp_ip_list) > 0:
            ip = _temp_ip_list[0]
        else:
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')
    else:
        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')

    user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    body_name = '职业课程：《%s》' % user_purchase.pay_careercourse.name
    nonce_str = generate_random(20, 1)
    user_purchase.nonce_str = nonce_str
    user_purchase.save()
    out_trade_no = order_no
    total_fee = user_purchase.pay_price * 100
    # total_fee = 1
    sign_url = "appid=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&" \
               "out_trade_no=%s&spbill_create_ip=%s&total_fee=%s&trade_type=%s" % (
                   app_id, body_name, mch_id, nonce_str,
                   settings.WEIXIN_NOTIFY_URL, out_trade_no, ip,
                   total_fee, wechat_type
               )
    sign_url = sign_url + '&key=' + key
    md5_signer = hashlib.md5()
    md5_signer.update(sign_url)
    sign = md5_signer.hexdigest().upper()
    xml_string = """
                    <xml>
                        <appid>%s</appid>
                        <body>%s</body>
                        <mch_id>%s</mch_id>
                        <nonce_str>%s</nonce_str>
                        <notify_url>%s</notify_url>
                        <out_trade_no>%s</out_trade_no>
                        <spbill_create_ip>%s</spbill_create_ip>
                        <total_fee>%s</total_fee>
                        <trade_type>%s</trade_type>
                        <sign>%s</sign>
                    </xml>
                """ % (
        app_id, body_name, mch_id, nonce_str, settings.WEIXIN_NOTIFY_URL,
        out_trade_no, ip, total_fee,
        wechat_type, sign)

    xml_string = xml_string.encode('utf-8')
    req = urllib2.Request(url=settings.WEIXIN_PAY_URL,
                          data=xml_string,
                          headers={'Content-Type': 'application/xml'})
    response = urllib2.urlopen(req)
    json_read = response.read()
    logger.info("weixinpay" + json_read)
    root = ET.fromstring(json_read)
    return root, nonce_str


def generate_qrcode(request, order_no):
    # 微信生成支付二维码

    root, nonce_str = go_wechat_pay(request, order_no, settings.WEIXIN_PAY_APPID, settings.WEIXIN_PAY_MCH_ID,
                         settings.WEIXIN_PAY_TRADE_TYPE, settings.WEIXIN_PAY_KEY)
    code_url = ''
    for child in root._children:
        if child.tag == 'code_url':
            code_url = child.text

    img = qrcode.make(code_url)
    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()

    response = HttpResponse(image_stream, content_type="image/png")
    response['Last-Modified'] = 'Mon, 27 Apr 2015 02:05:03 GMT'
    response['Cache-Control'] = 'max-age=31536000'
    return response


def app_wechat_pay(request, order_no):
    # app 微信支付
    root, nonce_str = go_wechat_pay(request, order_no, settings.WEIXIN_APP_PAY_APPID, settings.WEIXIN_APP_PAY_MCH_ID,
                         settings.WEIXIN_APP_PAY_TRADE_TYPE, settings.WEIXIN_APP_PAY_KEY)
    data = {}
    for child in root._children:
        if child.tag == 'prepay_id':
            data['prepayid'] = child.text
    if not data.get('prepayid', None):
        return False, ''
    data['timestamp'] = int(time.time())
    data['appid'] = settings.WEIXIN_APP_PAY_APPID
    data['partnerid'] = settings.WEIXIN_APP_PAY_MCH_ID
    data['package'] = 'Sign=WXPay'
    data['noncestr'] = nonce_str
    _tmp = sorted(data.iteritems(), key=lambda dict_x: dict_x[0])
    sign_string = "&".join(["=".join(map(str, x)) for x in _tmp]) + '&key=' + settings.WEIXIN_APP_PAY_KEY
    md5_signer = hashlib.md5()
    md5_signer.update(sign_string)
    sign = md5_signer.hexdigest().upper()
    data['sign'] = sign
    return True, data


def wechat_query(request, order_no):
    # 微信支付订单查询
    nonce_str = generate_random(20, 1)
    sign_url = "appid=%s&mch_id=%s&nonce_str=%s&out_trade_no=%s&key=%s" % (
        settings.WEIXIN_PAY_APPID, settings.WEIXIN_PAY_MCH_ID, nonce_str, order_no, settings.WEIXIN_PAY_KEY)
    md5_signer = hashlib.md5()
    md5_signer.update(sign_url)
    sign = md5_signer.hexdigest().upper()
    xml_string = """
                    <xml>
                        <appid>%s</appid>
                        <mch_id>%s</mch_id>
                        <nonce_str>%s</nonce_str>
                        <out_trade_no>%s</out_trade_no>
                        <sign>%s</sign>
                    </xml>
                """ % (settings.WEIXIN_PAY_APPID, settings.WEIXIN_PAY_MCH_ID, nonce_str, order_no, sign)
    xml_string = xml_string.encode('utf-8')
    wechat_query_url = 'https://api.mch.weixin.qq.com/pay/orderquery'
    req = urllib2.Request(url=wechat_query_url,
                          data=xml_string,
                          headers={'Content-Type': 'application/xml'})
    is_success = False
    state = False
    transaction_id = ''
    try:
        response = urllib2.urlopen(req)
        json_read = response.read()
        root = ET.fromstring(json_read)
        trade_state = ''
        for child in root._children:
            if child.tag == 'trade_state':
                trade_state = child.text
            elif child.tag == 'transaction_id':
                transaction_id = child.text

        if trade_state == 'SUCCESS':
            state = True
        is_success = True
        return is_success, state, transaction_id
    except:
        return is_success, state, transaction_id


def mi_me_pay(order_no, mobile_number):
    # 么分期生成二维码跳转链接
    user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    user_purchase.mobile = mobile_number
    user_purchase.save()

    app_id = settings.MIME_PAY_APPID  # 渠道id
    apply_amt = user_purchase.pay_price * 100  # 借款金额（单位分）
    course_name = user_purchase.pay_careercourse.name  # 课程名
    course_name = course_name.replace(' ', '')
    contract_amt = user_purchase.pay_price * 100  # 合约金额（单位分）
    contact_url = 'http://www.maiziedu.com/pay/mime/contract/'  # PDF合约(url)
    mobile = mobile_number  # 手机号码
    order_date = str(datetime.now().strftime("%Y%m%d%H%M%S"))  # 订单时间
    class_no = user_purchase.pay_class.coding  # 课程编号
    project_no = order_no  # 订单号
    if (datetime.now() < datetime(2016, 2, 7, 23, 59, 59)) and (datetime.now() > datetime(2016, 1, 25)):
        if user_purchase.pay_careercourse.id in [13, 6, 2]:
            apply_amt -= 20000
            contract_amt -= 20000
    data = dict(
        appId=app_id,
        applyAmt=apply_amt,
        commodityName=course_name.encode('utf-8') + '-' + class_no.encode('utf-8'),
        contactUrl=contact_url,
        contractAmt=contract_amt,
        mobile=mobile.encode('utf-8'),
        orderDate=order_date,
        projectNo=project_no,
    )
    _tmp = sorted(data.iteritems(), key=lambda x: x[0].upper())
    sign_string = "".join(["".join(map(str, x)) for x in _tmp]) + settings.MIME_PAY_KEY
    md5_signer = hashlib.md5()
    md5_signer.update(sign_string)
    sign = md5_signer.hexdigest()
    data['signvalue'] = sign

    str_json = json.dumps(data)
    r = requests.post(url=settings.MIME_PAY_URL, data=str_json, headers={'Content-Type': 'application/json'})
    if r.status_code == 200:
        ret = json.loads(r.text)
        mime_url = ret['content']
        return mime_url
    else:
        raise Exception('调用接口出错')


@csrf_exempt
def mimepay_notify(request):
    """
    支付成功后异步通知处理
    """
    if request.method == 'POST':
        json_obj = json.loads(request.body)
        order_no = json_obj['out_trade_no']
        trade_no = json_obj['trade_no']
        trade_status = json_obj['trade_status']
        total_fee = json_obj['total_fee']
        if total_fee:
            total_fee = float(total_fee) / 100
        user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
        result = order_handle(trade_status, order_no, trade_no, total_fee)
        if result[0] == 'success':
            order_handler_sucess_sendsms(order_no)
            return HttpResponse('success')
    return HttpResponse('fail')


def union_pay(order_no):
    """
    银联支付
    :param order_no
    """
    # user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    # date_time = datetime.now()
    # data = dict(
    #     version='5.0.0',  # 版本号
    #     encoding='UTF-8',  # 编码方式
    #     signMethod='01',  # 签名方法
    #     txnType='01',  # 交易类型
    #     txnSubType='01',  # 交易子类
    #     bizType='000201',  # 产品类型
    #     channelType='07',  # 渠道类型
    #     accessType='0',  # 接入类型
    #     currencyCode='156',  # 交易币种
    #     certId='',  # 证书序列号
    #     merId=settings.UNION_PAY_MER_ID,  # 商户代码
    #     orderId=order_no,  # 商户订单号
    #     txnTime=date_time.strftime("%Y%m%d%H%M%S"),  # 订单发送时间
    #     txnAmt=user_purchase.pay_price * 100,  # 交易金额,单位为分
    #     frontUrl=settings.UNION_PAY_RETURN,  # 前台通知地址
    #     backUrl=settings.UNION_PAY_NOTIFY,  # 后台通知地址
    #     # orderTimeout='10000',                                                         # 订单接收超时时间,单位为毫秒
    #     # payTimeout=(date_time + timedelta(minutes=15)).strftime("%Y%m%d%H%M%S"),      # 订单支付超时时间YYYYMMDDhhmmss
    # )
    # cer_file = open('/home/strii/Downloads/abc/银联支付/生产/123456/123456.pem').read()
    # key = load_certificate(FILETYPE_PEM, cer_file)
    # cert_id = X509.get_serial_number(key)
    # data['certId'] = cert_id
    # _tmp = sorted(data.iteritems(), key=lambda dict_x: dict_x[0])
    # sign_string = "&".join(["=".join(map(str, x)) for x in _tmp])
    # sha1_signer = hashlib.sha1()
    # sha1_signer.update(sign_string.encode('gbk'))
    # sign_str = sha1_signer.hexdigest().lower()
    # passphrase = "000000"
    # key = load_privatekey(FILETYPE_PEM, cer_file, passphrase.encode('gbk'))
    # signature = base64.b64encode(sign(key, sign_str.encode('utf-8'), 'sha1'))
    # data['signature'] = signature
    # return data
    pass


def union_return(request):
    """
    支付成功后同步处理跳转告知用户
    :param request:
    :return:
    """
    try:
        if request.method == 'POST':
            verify_result = union_notify_verify(request.POST)  # 验证签名
            if verify_result:
                order_no = request.POST.get('orderId')
                trade_no = request.POST.get('queryId')
                respcode = request.POST.get('respCode')
                respmsg = request.POST.get('respMsg')
                total_fee = request.POST.get('txnAmt')
                if total_fee:
                    total_fee = float(total_fee) / 100
                if respcode == '00' and respmsg == 'success':
                    result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                    if result[0] == "success":
                        order_handler_sucess_sendsms(order_no)
                        return render(request, 'mz_pay/success.html',
                                      {'careercourse_name': result[3],
                                       'url': '/lps2/learning/plan/' + str(result[2]) + '/',
                                       'total_fee': total_fee})
            else:
                return render(request, 'mz_common/failure.html', {'reason': '支付来源验证错误，请联系管理员'})
    except Exception as e:
        logger.error(e)

    order_no = request.GET.get('orderId', '')
    url, _, _, _ = get_error_url(order_no)
    return render(request, 'mz_pay/error.html', {'url': url})


def union_notify(request):
    """
    银联支付成功后异步通知处理
    :param request:
    :return:
    """
    try:
        if request.method == 'POST':
            verify_result = union_notify_verify(request.POST)  # 验证签名
            if verify_result:
                order_no = request.POST.get('orderId')
                trade_no = request.POST.get('queryId')
                respcode = request.POST.get('respCode')
                respmsg = request.POST.get('respMsg')
                total_fee = request.POST.get('txnAmt')
                if total_fee:
                    total_fee = float(total_fee) / 100
                if respcode == '00' and respmsg == 'Success!':
                    result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                    if result[0] == 'success':
                        return HttpResponse('success')
    except Exception as e:
        logger.error(e)
    return HttpResponse('fail')


def union_notify_verify(params):
    """
    验证银联签名
    :param params:
    :return:
    """
    # from utils.alipay import smart_str
    # ks = params.keys()
    # ks.sort()
    # newparams = {}
    # prestr = ''
    # for k in ks:
    #     v = params[k]
    #     k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
    #     if k != 'signature' and v != '':
    #         newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
    #         prestr += '%s=%s&' % (k, newparams[k])
    # prestr = prestr[:-1]
    # sha1_signer = hashlib.sha1()
    # sha1_signer.update(prestr.encode('gbk'))
    # sign_str = sha1_signer.hexdigest().lower()
    # cer_file = open('/home/strii/Downloads/abc/银联支付/生产/acp.pem').read()
    # key = load_certificate(FILETYPE_PEM, cer_file)
    # try:
    #     result = verify(key, base64.decodestring(params['signature']), sign_str, 'sha1')
    #     if result is None:
    #         return True
    # except:
    #     return False
    # return False
    pass


def fen_qi_le_pay(request, order_no):
    """
    分期乐支付跳转
    :param request
    :param order_no: 订单号
    :return:
    """
    user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    # 获取用户ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        _temp_ip_list = request.META.get('HTTP_X_FORWARDED_FOR').split(',')
        if len(_temp_ip_list) > 0:
            ip = _temp_ip_list[0]
        else:
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')
    else:
        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')
    date_time = datetime.now()
    data = dict(
        amount=user_purchase.pay_price*100,     # 支付金额,单位为分
        out_trade_no=quote_plus(user_purchase.order_no.encode('utf-8')),    # 商户订单号
        partner_id=quote_plus(settings.FQL_PAY_MER_ID),      # 商户号
        notify_url=quote_plus(settings.FQL_PAY_NOTIFY),      # 后台回调地址
        subject=quote_plus(user_purchase.pay_careercourse.name.encode('utf-8')),         # 商品描述
        client_ip=quote_plus(ip),       # ip
        c_merch_id=quote_plus('1'),      # 提交该订单商户的所属子商户编号
        payment_type=1,    # 支付类型
        time_start=quote_plus(date_time.strftime('%Y-%m-%d %H:%M:%S')),      # 交易开始时间 YYYY-mm-dd HH:mm:ss
        time_expire=quote_plus((date_time + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')),     # 交易失效时间
        # return_url=quote_plus(settings.FQL_PAY_RETURN),      # 前台回调地址，分期乐暂时没有返回数据，所以注释掉
        body=quote_plus('报名班级：%s' % user_purchase.pay_class.coding.encode('utf-8')),            # 商品细节信息
    )
    _tmp = sorted(data.iteritems(), key=lambda dict_x: dict_x[0])
    sign_string = "&".join(["=".join(map(str, x)) for x in _tmp]) + '&key=%s' % settings.FQL_PAY_KEY
    md5_signer = hashlib.md5()
    md5_signer.update(sign_string)
    sign = md5_signer.hexdigest().lower()
    data['sign'] = sign

    str_json = json.dumps(data)
    r = requests.post(url='http://mapi.fenqile.com/merchpay/pay', data=str_json,
                      headers={'Content-Type': 'application/json'})
    if r.status_code == 200:
        ret = json.loads(r.text)
        fql_url = ret['url']
        return fql_url
    else:
        raise Exception('调用接口出错')


def fen_qi_le_return(request):
    """
    分期乐同步回调
    :param request:
    :return:
    """
    if request.method == 'GET':
        _, prestr = params_filter(request.GET)
        mysign = build_mysign(prestr, settings.FQL_PAY_KEY, settings.ALIPAY_SIGN_TYPE)
        if mysign == request.GET.get('sign'):
            if request.GET.get('result') == '0' and request.GET.get('trans_status') == '200':
                order_no = request.GET.get('out_trade_no')
                trade_no = request.GET.get('trans_id')
                total_fee = request.GET.get('amount')
                result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                if result[0] == "success":
                    order_handler_sucess_sendsms(order_no)
                    return render(request, 'mz_pay/success.html',
                                  {'careercourse_name': result[3], 'url': '/lps2/learning/plan/' + str(result[2]) + '/',
                                   'total_fee': total_fee})

    order_no = request.GET.get('out_trade_no', '')
    url, _, _, _ = get_error_url(order_no)
    return render(request, 'mz_pay/error.html', {'url': url})


def fen_qi_le_notify(request):
    data = request.body
    if data:
        data = json.loads(data)
        _, prestr = params_filter(data)
        md5_signer = hashlib.md5()
        md5_signer.update(prestr + '&key=%s' % settings.FQL_PAY_KEY)
        sign = md5_signer.hexdigest().lower()
        if sign == data.get('sign'):
            if data.get('result') == 0 and data.get('trans_status') == '200':
                order_no = data.get('out_trade_no')
                trade_no = data.get('trans_id')
                total_fee = data.get('amount')
                result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                if result[0] == "success":
                    order_handler_sucess_sendsms(order_no)
                    return JsonResponse({"result": 0})
    return JsonResponse({"status": "false"})

def uubee_pay(order_no, user, pay_type, class_coding, remain_student):
    # 有贝分期跳转
    user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    career_course_name = user_purchase.pay_careercourse.name.encode('utf-8')
    institute_id = user_purchase.pay_careercourse.institute_id
    risk_item = dict(
        ub_user_dt_reg=user.date_joined.strftime('%Y%m%d%H%M%S'),
        account_login=user.mobile,
        account_name=user.nick_name,
        ub_transaction_history='是' if ClassStudents.objects.filter(user=user, student_class__class_type=0).exists()
                               else '否',
        ub_historical_experience='是' if ClassStudents.objects.filter(user=user, student_class__class_type__in=[1, 2, 3])
                                 .exists() else '否',
        ub_order_amt=user_purchase.pay_price,
        pay_amount=user_purchase.pay_price,
        ub_order_code=user_purchase.order_no,
        ub_course_name=career_course_name,
        ub_course_information=user_purchase.pay_careercourse.description.encode('utf=8'),
        ub_teacher_id=1,
        ub_teacher_name=u'麦子老师',
        ub_trade_type=institute_id,
        ub_learning_goals=1 if pay_type == '0' else 2,
        ub_vocational_class=class_coding,
        ub_trade_serveice_number=remain_student
    )
    data = dict(
        transcode='8001',
        version='1.0',
        oid_partner=settings.UUBEE_PAY_MER_ID,   # 商户编号
        mob_user=user.mobile,            # 用户手机号
        user_id=user.id,             # 用户ID
        busi_partner='109001',
        pro_code='100103',
        no_order=user_purchase.order_no,   # 商户唯一订单号
        dt_order=user_purchase.date_add.strftime('%Y%m%d%H%M%S'),
        money_order=user_purchase.pay_price,
        # money_order=1,
        name_goods=career_course_name,
        back_url=settings.UUBEE_PAY_RETURN,
        notify_url=settings.UUBEE_PAY_NOTIFY,
        risk_item=risk_item,
    )
    data_str = json.dumps(data)

    # 签名
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/rsa_private_maizi_uubee.pem'
    with open(path, 'rb') as private_file:
        key = private_file.read()
    rsa_key = RSA.importKey(key)
    signer = Signature_pkcs1_v1_5.new(rsa_key)
    h = SHA.new(data_str)
    sign = signer.sign(h)
    signature = base64.b64encode(sign)
    # 加密
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/uubee_pub_key.pem'
    with open(path, 'rb') as private_file:
        key = private_file.read()
    rsa_key = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    content = encrypt_spilt(data_str, cipher)
    content = base64.b64encode(content)
    return {'content': content, 'sign': signature}


def encrypt_spilt(message, cipher):
    # 分段加密所以下面的117为key.size/8-11得出
    key_length = 117
    count = len(message)
    if count > key_length:
        encryption = ""
        index = 0
        while index < count:
            i = key_length if count-index > key_length else count-index
            submsg = message[index:index+i]
            index += i
            j = cipher.encrypt(submsg)
            encryption += j
        return encryption
    else:
        encryption = cipher.encrypt(message)
        return encryption


def decrypt_spilt(message):
    # 分段解密
    # 下面的128为key.size/8得出
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/rsa_private_maizi_uubee.pem'
    with open(path, 'rb') as private_file:
        key = private_file.read()
    rsa_key = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    message = base64.b64decode(message)
    key_length = 128
    count = len(message)
    dsize = SHA.digest_size
    sentinel = Random.new().read(64+dsize)
    if count > key_length:
        decryption = ""
        index = 0
        while index < count:
            i = key_length if count-index > key_length else count-index
            submsg = message[index:index+i]
            index += i
            j = cipher.decrypt(submsg, sentinel)
            decryption += j
        return decryption
    else:
        decryption = cipher.decrypt(message, sentinel)
        return decryption


def verify_rsa_signature(content, signature):
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/uubee_pub_key.pem'
    with open(path, 'rb') as public_file:
        key = public_file.read()
    rsa_key = RSA.importKey(key)
    h = SHA.new(content)
    verifier = Signature_pkcs1_v1_5.new(rsa_key)
    if not verifier.verify(h, base64.b64decode(signature)):
        return False
    return True


def uubee_pay_return(request):

    data = {}
    content = request.POST.get('content')
    signature = request.POST.get('sign')
    if content:
        content = decrypt_spilt(content)
        sign_result = verify_rsa_signature(content, signature)
        if sign_result:
            data = json.loads(content)
            result_pay = data.get('result_pay')
            order_no = data.get('no_order')
            trade_no = data.get('oid_paybill')
            total_fee = data.get('money_order')
            if result_pay == 'SUCCESS':
                result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                if result[0] == "success":
                    order_handler_sucess_sendsms(order_no)
                    return render(request, 'mz_pay/success.html',
                                  {'careercourse_name': result[3], 'url': '/lps2/learning/plan/' + str(result[2]) + '/',
                                   'total_fee': total_fee})

    order_no = data.get('out_trade_no', '')
    url, _, _, _ = get_error_url(order_no)
    return render(request, 'mz_pay/error.html', {'url': url})


def uubee_pay_notify(request):
    content = request.POST.get('content')
    signature = request.POST.get('sign')
    if content:
        content = decrypt_spilt(content)
        sign_result = verify_rsa_signature(content, signature)
        if sign_result:
            data = json.loads(content)
            result_pay = data.get('result_pay')
            order_no = data.get('no_order')
            trade_no = data.get('oid_paybill')
            total_fee = data.get('money_order')
            if result_pay == 'SUCCESS':
                result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
                if result[0] == "success":
                    return JsonResponse({'ret_code': '0000', 'ret_msg': '交易成功'})
    return JsonResponse({'ret_code': 'fail'})


def yee_pay(order_no, other):
    """
    易宝支付跳转
    :param order_no:
    :param other: 银行通道编码
    :return:
    """
    bank = {"ICBC": "ICBC-NET-B2C",
            "ABC": "ABC-NET-B2C",
            "CCB": "CCB-NET-B2C",
            "BOC": "BOC-NET-B2C",
            "CMBCHINA": "CMBCHINA-NET-B2C",
            "BOCO": "BOCO-NET-B2C",
            "CEB": "CEB-NET-B2C",
            "CIB": "CIB-NET-B2C",
            "POST": "POST-NET-B2C",
            "PINGANBANK": "PINGANBANK-NET-B2C",
            "ECITIC": "ECITIC-NET-B2C",
            "HXB": "HXB-NET-B2C"}
    user_purchase = get_object_or_404(UserPurchase, order_no=order_no)
    name = user_purchase.pay_careercourse.name
    data = dict(
        p0_Cmd='Buy',        # 业务类型
        p1_MerId=str(settings.YEE_PAY_MER_ID),         # 商户编号
        p2_Order=str(user_purchase.order_no),        # 商户订单号
        p3_Amt=str(user_purchase.pay_price),          # 支付金额
        # p3_Amt='0.01',
        p4_Cur='CNY',        # 交易币种
        p5_Pid=name.encode("utf-8"),          # 商品名称
        p8_Url=str(settings.YEE_PAY_RETURN),          # 同步回调地址
        pd_FrpId=bank[other],                # 支付通道编码
        pm_Period='1',                            # 订单有效期
        pr_NeedResponse='1'                       # 应答机制
    )
    _tmp = sorted(data.iteritems(), key=lambda dict_x: dict_x[0])
    sign_string = ''.join([(x[1]) for x in _tmp])
    hmac_signer = hmac.new(settings.YEE_PAY_MER_KEY)
    hmac_signer.update(sign_string)
    sign_value = hmac_signer.hexdigest()
    data['hmac'] = sign_value
    return data


def yee_pay_return(request):
    data = request.POST
    keys = ['p1_MerId', 'r0_Cmd', 'r1_Code', 'r2_TrxId', 'r3_Amt', 'r4_Cur',
            'r5_Pid', 'r6_Order', 'r7_Uid', 'r8_MP', 'r9_BType']
    sign_string = ''.join([data[k] if k != 'r5_Pid' else
                           ''.join(chr(ord(x)) for x in data[k]).decode('GBK').encode('utf-8') for k in keys])
    hmac_signer = hmac.new(settings.YEE_PAY_MER_KEY)
    hmac_signer.update(sign_string)
    sign_value = hmac_signer.hexdigest()
    if data['hmac'] == sign_value:
        if data['r1_Code'] == '1':
            order_no = data.get('r6_Order')
            trade_no = data.get('r2_TrxId')
            total_fee = data.get('r3_Amt')
            result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
            if result[0] == "success":
                order_handler_sucess_sendsms(order_no)
                return render(request, 'mz_pay/success.html',
                              {'careercourse_name': result[3], 'url': '/lps2/learning/plan/' + str(result[2]) + '/',
                               'total_fee': total_fee})

    order_no = data.get('out_trade_no', '')
    url, _, _, _ = get_error_url(order_no)
    return render(request, 'mz_pay/error.html', {'url': url})


def yee_pay_notify(request):
    data = request.GET
    keys = ['p1_MerId', 'r0_Cmd', 'r1_Code', 'r2_TrxId', 'r3_Amt', 'r4_Cur',
            'r5_Pid', 'r6_Order', 'r7_Uid', 'r8_MP', 'r9_BType']
    sign_string = ''.join([data[k] for k in keys])
    hmac_signer = hmac.new(settings.YEE_PAY_MER_KEY)
    hmac_signer.update(sign_string)
    sign_value = hmac_signer.hexdigest()
    if data['hmac'] == sign_value:
        if data['r1_Code'] == '1':
            order_no = data.get('r6_Order')
            trade_no = data.get('r2_TrxId')
            total_fee = data.get('r3_Amt')
            result = order_handle('TRADE_SUCCESS', order_no, trade_no, total_fee)
            if result[0] == "success":
                return HttpResponse('success')
    return HttpResponse('fail')


@login_required(login_url="/")
def goto_onepay(request):
    # 更新一键支付状态 zhangyu
    if request.method == 'GET':
        user = request.user
        try:
            userppaybind = UserPayBind.objects.filter(user_id=user.id)
            if userppaybind:
                url = '/pay/view/?career_id=' + userppaybind[0].careercourse_id
                userppaybind.update(status=1)
                # 删除session中的一键支付标记
                if request.session.get('is_onepay'):
                    del request.session['is_onepay']
                return HttpResponse("{'status':'sucess', 'url': '" + url + "'}", content_type="application/json")
        except UserPayBind.DoesNotExist:
            pass
    return HttpResponse("{'status':'failure'}", content_type="application/json")


def order_handler_sucess_sendsms(order_no):
    try:
        purchase = UserPurchase.objects.get(order_no=order_no)
        # 老带新完成支付后处理操作
        if purchase.pay_type == 0 and purchase.pay_status == 1:
            if if_user_is_invited(purchase.user.id) and if_first_register_course(purchase.user.id):
                update_invitation_course_info(purchase.user.id, purchase.pay_careercourse.id)  # course_id为用户报名课程的id
                send_message(purchase.user.id, purchase.pay_careercourse.name)  # course_name为用户报名课程的名字
    except Exception as e:
        logger.error('order_handler_sucess_sendsms: ' + str(e))


def send_sms_join_class_success(careercourse_name, user_mobile, teacher_qq, teacher_name):
    from utils.sms_manager import send_sms, get_templates_id
    now_time = datetime.now()

    try:
        apikey = settings.SMS_APIKEY
        if user_mobile:
            send_sms(apikey,
                     get_templates_id('join_class_notify_3_1'),
                     user_mobile,
                     careercourse_name.encode('utf-8'),
                     now_time.year,
                     now_time.month,
                     now_time.day,
                     teacher_name,
                     teacher_qq
                     )
    except Exception as e:
        logger.exception('send_sms_join_class_success: ' + str(e))
