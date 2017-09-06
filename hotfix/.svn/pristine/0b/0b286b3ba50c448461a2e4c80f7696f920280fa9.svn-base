# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from PIL import Image, ImageFile
from mz_user import functions
from mz_user.functions import get_user_id_from_invitation_code, save_job_info
from mz_user.functions_introduce import add_invitation_record
from django.shortcuts import get_object_or_404
from utils.tool import second_to_time
from utils.sms_manager import *
from mz_common.decorators import student_required, teacher_required
from mz_common.views import *
from django.contrib.auth.decorators import login_required
from models import *
from mz_course.models import *
from mz_course.views import get_recent_learned_lesson
from django.db.models import Count
from aca_course.models import *
from mz_pay.models import UserPayBind
import urlparse
from django.conf import settings
import random
from celery import shared_task
import base64, json, re, urllib, urllib2, os, uuid, logging
import mz_user.functions
from geetest.views import validate
from django.shortcuts import render

import db
from mz_oauth import WeiXinAuth2

logger = logging.getLogger('mz_user.views')

@csrf_exempt
def user_login(request):
    '''
    前台登录
    :param request:
    :return:
    '''
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        #获取表单信息
        account = login_form.cleaned_data["account_l"]
        password = login_form.cleaned_data["password_l"]
        source_url = request.POST.get("source_url",None)
        if source_url is None:
            source_url = request.META.get('HTTP_REFERER')
        url_parse = urlparse.urlparse(source_url)
        if not url_parse[2] or url_parse[2] == '/':
            source_url = '/home/?source=login'
        elif not url_parse[2] or url_parse[2].startswith('/user/signup'):
            source_url = '/home/?source=login'
        #登录验证
        user = authenticate(username=account, password=password)
        if user is not None:
            # 登录
            if user.is_active:
                login(request, user)
                # 记录登录日志
                db.api.user.user.insert_user_log(user.id, "login")
                # 如果是第三方绑定
                partner = request.POST.get('partner')
                openid = request.POST.get('openid')
                if partner and openid:
                    source_url = mz_user.functions.url_remove_params(source_url, 'partner', 'openid', 'qq_nickname')
                    try:
                        thirdpartyuser = ThirdPartyUser.objects.get(partner=partner, openid=openid)
                        if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user=user)):
                            thirdpartyuser.user = user
                            thirdpartyuser.save()
                    except Exception, e:
                        logger.error('第三方登录绑定：%s' % e)

                # zhangyu 是否弹出一键支付
                status = False
                careercourse_id = ''
                try:
                    userpaybind = UserPayBind.objects.filter(user_id=user.id, status=0).order_by('id')
                    if userpaybind:
                        status = True
                        careercourse_id = userpaybind[0].careercourse_id
                        # session中放置一键支付标记
                        request.session['is_onepay'] = '1'
                except UserPayBind.DoesNotExist:
                    status = False

                return HttpResponse('{"status":"success", "url":"'+source_url+'", "onepay_status":"'+
                                    str(status)+'", "careercourse_id": "'+careercourse_id+'"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"failure","msg":"no_active"}', content_type="application/json")

        else:
            # 如果主站未查询到对应的账号信息，则尝试从老网站验证用户登录信息，如果验证通过，则在新网站里面插入对应账号信息
            try:
                # 如果已有对应账号，则不需再去老网站验证
                UserProfile.objects.get(Q(email=account) | Q(mobile=account))
            except UserProfile.DoesNotExist:
                pass
            except Exception, e:
                logger.error(e)
            return HttpResponse('{"status":"failure"}', content_type="application/json")
    return HttpResponse(json.dumps(login_form.errors), content_type="application/json")


def user_logout(request):
    '''
    前台注销
    :param request:
    :return:
    '''
    try:
        logout(request)
        # 同步从论坛登出
    except Exception as e:
        logger.error(e)
    return HttpResponseRedirect(reverse('index_front'))


# 判断该进哪个用户中心
def user_center(request):
    if request.user.is_authenticated():
        source = request.GET.get('source', None)
        if request.user.is_student():
            if settings.FPS_SWITCH:
                center_api = settings.FPS_CENTER
                if source:
                    center_api = settings.FPS_CENTER+"?source="+source
            else:
                center_api = "/user/student"
            response = HttpResponseRedirect(center_api)
            response.set_cookie("is_jump",1)
            response.set_cookie("f_number",False)
        else:
            if settings.FPS_SWITCH:
                center_api = settings.FPS_CENTER
                if source:
                    center_api = settings.FPS_CENTER+"?source="+source
            else:
                center_api = "/user/teacher"

            response = HttpResponseRedirect(center_api)
            response.set_cookie("is_jump",1)
            response.set_cookie("f_number",False)
        return response
    else:
        return render(request, 'mz_common/failure.html',{'reason':'请先登录再进入个人中心。'})


def email_register(request):
    '''
    邮件注册账号表单
    :param request:
    :return:
    '''
    register_form = EmailRegisterForm(request.POST)
    if register_form.is_valid():
        # 验证码验证
        try:
            result = validate(request)
        except KeyError:
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        request.session['captcha_status'] = '1'
        #获取表单信息
        password = register_form.cleaned_data["password"]
        email = register_form.cleaned_data["email"]

        #发送注册激活邮件
        result = do_send_mail_reg(email, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 0)
        ret = result.next()
        if ret != 1:
            return HttpResponse(ret, content_type="application/json")

        user = common_register(request, email, password, "新网站")
        result.next()
        # 如果是第三方邮件注册
        partner = request.POST.get('partner')
        openid = request.POST.get('openid')

        # 记录邀请码注册用户
        invitation_code = request.POST.get('invitation_code')
        if invitation_code:
            usera = get_user_id_from_invitation_code(invitation_code)
            add_invitation_record(usera, user.id)

        if partner and openid:
            try:
                thirdpartyuser = ThirdPartyUser.objects.get(partner=partner, openid=openid)
                if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user=user)):
                    thirdpartyuser.user = user
                    thirdpartyuser.save()
            except Exception, e:
                logger.error('第三方邮件注册：%s' % e)

    return HttpResponse(json.dumps(register_form.errors), content_type="application/json")


def mobile_register_step_one(request):
    '''
    手机验证第一步
    :param request:
    :return:
    '''
    register_form = MobileRegisterForm(request.POST)

    if register_form.is_valid():
        # 验证码验证
        try:
            result = validate(request)
        except KeyError:
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        request.session['captcha_status'] = '1'
        return HttpResponse('{"status": "success"}', content_type="application/json")
    return HttpResponse(json.dumps(register_form.errors), content_type="application/json")


def mobile_register(request):
    '''
    手机注册账号表单
    :param request:
    :return:
    '''

    register_form = MobileRegisterForm(request.POST)
    if register_form.is_valid():
        # 验证码验证
        if not request.session.get('captcha_status', None):
            # 验证码验证 , 为了兼容老的弹出登录框
            try:
                result = validate(request)
            except KeyError:
                return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
            status = json.loads(result.content)
            if status['status'] == 'fail':
                return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
            request.session['captcha_status'] = '1'
        #获取表单信息
        password = register_form.cleaned_data["password_m"]
        mobile = register_form.cleaned_data["mobile"]
        source='新网站'
        httppath=request.META.get('HTTP_REFERER')
        if httppath.find('pages/ad')>-1:
            source='推广页'+httppath[httppath.find('pages/ad'):]
        user = common_register(request, mobile, password, source)
        # 如果是第三方手机注册
        partner = request.POST.get('partner')
        openid = request.POST.get('openid')

        # 记录邀请码注册用户
        invitation_code = request.POST.get('invitation_code')
        if invitation_code:
            usera = get_user_id_from_invitation_code(invitation_code)
            add_invitation_record(usera, user.id)

        if partner and openid:
            try:
                thirdpartyuser = ThirdPartyUser.objects.get(partner=partner, openid=openid)
                if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user=user)):
                    thirdpartyuser.user = user
                    thirdpartyuser.save()
            except Exception, e:
                logger.error('第三方手机注册：%s' % e)
        else:
            # 同步登录
            user = authenticate(username=mobile, password=password)
            if user is not None:
                login(request, user)
    return HttpResponse(json.dumps(register_form.errors), content_type="application/json")


def random_avatar():
    url_big_s = 'avatar/%d_big.jpg'
    url_middle_s = 'avatar/%d_middle.jpg'
    url_small_s = 'avatar/%d_samll.jpg'
    i = random.randint(1,30)
    url_big = url_big_s % i
    url_middle = url_middle_s % i
    url_small = url_small_s % i

    return url_big,url_middle,url_small


def common_register(request, account, password, source):
    #将注册信息写入数据库
    user = UserProfile()
    url_big,url_middle,url_small = random_avatar()
    user.avatar_url = url_big
    user.avatar_middle_thumbnall = url_middle
    user.avatar_small_thumbnall = url_small
    try:
        user.username = account
        user.password = make_password(password)
        if re.compile(settings.REGEX_EMAIL).match(account):
            user.email = account
            user.is_active = False
            # 查询nick_name是否已经存在
            nick_name = account.split("@")[0]
            nick_name_count = UserProfile.objects.filter(nick_name__icontains=nick_name).count()
            if nick_name_count > 0:
                nick_name = str(nick_name) + "_" + str(nick_name_count)
            user.nick_name = nick_name
        elif re.compile(settings.REGEX_MOBILE).match(account):
            user.mobile = account
            user.nick_name = account
            user.valid_mobile = 1
        try:
            user.register_way = RegisterWay.objects.get(name=source)
        except RegisterWay.DoesNotExist:
            user.register_way = RegisterWay.objects.create(name=source)
        user.save()
        #  记录注册日志
        db.api.user.user.insert_user_log(user.id, "register")
        # 设置用户默认学生分组
        group = Group.objects.get(name="学生")
        group.user_set.add(user)
    except Exception as e:
        print e
        logger.error(e)

    return user


def find_password(request):
    findpassword_form = FindPasswordForm(request.POST)
    if findpassword_form.is_valid():
        # 验证码验证
        try:
            result = validate(request)
        except KeyError:
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        request.session['captcha_status'] = '1'
        #获取表单信息
        account = findpassword_form.cleaned_data["account"]
        #判断账号是邮箱还是手机号
        if re.compile(settings.REGEX_MOBILE).match(account):
            #手机则发送短信并进入短信验证界面
            result = do_send_sms_signup(account, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 1)
            return HttpResponse(result, content_type="application/json")
        elif re.compile(settings.REGEX_EMAIL).match(account):
            #发送找回密码邮件
            result = do_send_mail(account, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 1)
            return HttpResponse(result, content_type="application/json")

    return HttpResponse(json.dumps(findpassword_form.errors), content_type="application/json")


def find_password_mobile_code(request):
    '''
    手机注册账号表单
    :param request:
    :return:
    '''
    find_password_mobile_form = FindPasswordMobileForm(request.POST)
    if find_password_mobile_form.is_valid():
        if not request.session.get('captcha_status', None):
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        #获取表单信息
        return HttpResponse('{"status":"success"}', content_type="application/json")
    return HttpResponse(json.dumps(find_password_mobile_form.errors), content_type="application/json")


def reset_password(request, account, code):

    '''
    重置密码
    :param request:
    :param email: 邮箱或手机账号
    :param code: 随机码
    :return:
    '''
    if re.compile(settings.REGEX_MOBILE).match(account):
        #手机则发送短信并进入短信验证界面
        record = MobileVerifyRecord.objects.filter(Q(mobile=account), Q(code=code), Q(type=1)).order_by("-created")
        if record:
            if datetime.now()-timedelta(minutes=30) > record[0].created:
                return render(request, 'mz_common/failure.html',{'reason':'手机验证码已经过期，请到重新发送手机验证码'})
        else:
            return render(request, 'mz_common/failure.html',{'reason':'找回密码信息错误，无法找回'})
    else:
        account = base64.b64decode(account)
        if re.compile(settings.REGEX_EMAIL).match(account):
            #发送找回密码邮件
            record = EmailVerifyRecord.objects.filter(Q(email=account), Q(code=code), Q(type=1)).order_by("-created")
            if record:
                if datetime.now()-timedelta(days=1) > record[0].created:
                    return render(request, 'mz_common/failure.html',{'reason':'找回密码链接已经过期，请到重新发送找回密码邮件'})
            else:
                return render(request, 'mz_common/failure.html',{'reason':'找回密码信息错误，无法找回'})

    #设置session临时保存通过验证的account信息
    request.session['reset_account'] = account
    #跳转到密码重置界面
    return HttpResponseRedirect(reverse('user:update_reset_password_view'))


#密码重置界面
def update_reset_password_view(request):
    update_password_form = UpdatePasswordForm()
    return render(request, 'mz_user/reset_password.html',locals())


# 密码重置Ajax处理
def update_reset_password(request):
    update_password_form = UpdatePasswordForm(request.POST)
    if update_password_form.is_valid():
        password = make_password(update_password_form.cleaned_data['password'])
        #从服务端获取对应的账号
        account = request.session['reset_account']
        try:
            user = UserProfile.objects.get(Q(email=account) | Q(mobile=account))
            user.password = password
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        except UserProfile.DoesNotExist:
            return HttpResponse('{"status":"failure"}', content_type="application/json")
    return HttpResponse(json.dumps(update_password_form.errors), content_type="application/json")


# def send_sms_code(request):
#     '''
#     发送手机验证码ajax请求方法
#     :param request:
#     :return:
#     '''
#     mobile = request.POST["mobile"]
#     error_message=""
#     #检验手机号码格式
#     if mobile == "":
#         error_message = '{ "mobile":"请输入手机号" }'
#     else:
#         p=re.compile(settings.REGEX_MOBILE)
#         if not p.match(mobile):
#             error_message = '{ "mobile":"注册账号需为手机格式" }'
#         elif UserProfile.objects.filter(mobile=mobile).count() > 0:
#             #检验该手机号是否注册
#             error_message = '{ "mobile":"该账号已被注册" }'
#
#     if error_message != "":
#         return HttpResponse(error_message, content_type="application/json")
#         #发送短信
#     result = do_send_sms(mobile, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 0)
#     return HttpResponse(result, content_type="application/json")


def send_sms_code_signup(request):
    '''
    发送手机验证码ajax请求方法
    :param request:
    :return:
    '''

    mobile = request.POST.get("mobile", '')
    way = request.POST.get("way", '')

    # 验证码验证
    if not request.session.get('captcha_status', None):
        return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")

    send_type = 1 if way else 0
    error_message=""
    #检验手机号码格式
    if mobile == "":
        error_message = '{ "mobile":"请输入手机号" }'
    else:
        p=re.compile(settings.REGEX_MOBILE)
        if not p.match(mobile):
            error_message = '{ "mobile":"注册账号需为手机格式" }'
        elif UserProfile.objects.filter(mobile=mobile).count() > 0 and not way:
            #检验该手机号是否注册
            error_message = '{ "mobile":"该账号已被注册" }'

    if error_message != "":
        return HttpResponse(error_message, content_type="application/json")

    #发送短信
    result = do_send_sms_signup(mobile, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], send_type)
    return HttpResponse(result, content_type="application/json")


# def do_send_sms(mobile, ip, type=0):
#     '''
#     生成短信发送记录并发送手机验证码
#     :param request:
#     :param mobile:
#     :return:
#     '''
#
#     #查询同IP是否超出最大短信数量发送限制
#     start = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)
#
#     if MobileVerifyRecord.objects.filter(created__gt=start, mobile=mobile).count() >= settings.SMS_MAX_COUNT_MOBILE:
#         return '{"status":"failure","mobile": "该手机号超过当日短信发送限制数量"}'
#
#     if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=start)).count() >= settings.SMS_COUNT:
#         return '{"status":"failure","mobile": "该IP超过当日短信发送限制数量"}'
#
#     one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
#     if MobileVerifyRecord.objects.filter(Q(ip=ip),Q(created__gt = one_min_ago)).exists():
#         return '{"status":"failure","mobile": "当前ip距离上一次发送验证码未超过60s"}'
#     if MobileVerifyRecord.objects.filter(Q(mobile=mobile),Q(created__gt = one_min_ago)).exists():
#         return '{"status":"failure","mobile": "当前手机号距离上一次发送验证码未超过60s"}'
#
#     #生成激活码
#     random_str = generate_random(6, 0)
#     #邮件发送记录写入数据库
#     mobile_record = MobileVerifyRecord()
#     mobile_record.code = random_str
#     mobile_record.mobile = mobile
#     mobile_record.type = type
#     mobile_record.ip = ip
#     mobile_record.source = 1
#     mobile_len = len(mobile)
#     mobile_record.save()
#
#     #发送短信
#     apikey = settings.SMS_APIKEY
#     tpl_id = settings.SMS_TPL_ID  #短信模板ID
#     tpl_value = random_str
#
#     try:
#         tpl_send_sms.delay(apikey, tpl_id, tpl_value, mobile)
#
#         result='{"status":"success"}'
#         return result
#     except Exception,e:
#         logger.error(e)


def do_send_sms_signup(mobile, ip, type=0):
    '''
    生成短信发送记录并发送手机验证码
    :param request:
    :param mobile:
    :return:
    '''
    #查询同IP是否超出最大短信数量发送限制
    start = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)

    if MobileVerifyRecord.objects.filter(created__gt=start, mobile=mobile).count() >= settings.SMS_MAX_COUNT_MOBILE:
        return '{"status":"failure","mobile": "该手机号超过当日短信发送限制数量"}'

    if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=start)).count() >= settings.SMS_COUNT:
        return '{"status":"failure","mobile": "该IP超过当日短信发送限制数量"}'

    one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    if MobileVerifyRecord.objects.filter(Q(ip=ip),Q(created__gt = one_min_ago)).exists():
        return '{"status":"failure","mobile": "当前IP距离上一次发送验证码未超过60s"}'
    if MobileVerifyRecord.objects.filter(Q(mobile=mobile),Q(created__gt = one_min_ago)).exists():
        return '{"status":"failure","mobile": "当前手机号距离上一次发送验证码未超过60s"}'


    #生成激活码
    random_str = generate_random(6, 0)
    #邮件发送记录写入数据库
    mobile_record = MobileVerifyRecord()
    mobile_record.code = random_str
    mobile_record.mobile = mobile
    mobile_record.type = type
    mobile_record.ip = ip
    mobile_record.source = 1
    mobile_record.save()

    #发送短信
    apikey = settings.SMS_APIKEY
    tpl_id = settings.SMS_TPL_ID  #短信模板ID
    tpl_value = random_str
    try:
        tpl_send_sms.delay(apikey, tpl_id, tpl_value, mobile)
        result = '{"status":"success", "info": "验证码已经发送至您的手机，请注意查收"}'
        return result
    except Exception, e:
        return '{"status":"failure","mobile": "请稍后再试"}'


def do_send_mail(email, ip, type=0):

    '''
    生成邮件发送记录并发送注册激活邮件
    :param request:
    :param email:目标邮箱地址
    :param type:邮件类型（0：注册激活邮件；1：找回密码邮件）
    :return:
    '''

    #查询同IP是否超出最大发送邮件限制
    start = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)
    one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    send_count=EmailVerifyRecord.objects.filter(Q(ip=ip),Q(created__gt = start)).count()
    if EmailVerifyRecord.objects.filter(Q(email=email),Q(created__gt = one_min_ago)).exists():
        return '{"status":"failure","email_ue": "当前邮箱距离上一次发送邮件未超过60s"}'
    if send_count > settings.EMAIL_COUNT:
        return '{"status":"failure","email_ue": "当前ip超过发送次数"}'
        #生成激活码
    random_str = generate_random(10, 1)
    #邮件发送记录写入数据库
    email_record = EmailVerifyRecord()
    email_record.code = random_str
    email_record.email = email
    email_record.type = type
    email_record.ip = ip
    email_record.save()

    #发送验证邮件
    do_send_email_async.delay(email, random_str, type)
    return 1


def do_send_mail_reg(email, ip, type=0):

    '''
    生成邮件发送记录并发送注册激活邮件
    :param request:
    :param email:目标邮箱地址
    :param type:邮件类型（0：注册激活邮件；1：找回密码邮件）
    :return:
    '''

    #查询同IP是否超出最大发送邮件限制
    start = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)
    one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    send_count=EmailVerifyRecord.objects.filter(Q(ip=ip),Q(created__gt = start)).count()
    if EmailVerifyRecord.objects.filter(Q(email=email),Q(created__gt = one_min_ago)).exists():
        yield '{"status":"failure","email_ue": "当前邮箱距离上一次发送邮件未超过60s"}'
    if send_count > settings.EMAIL_COUNT:
        yield '{"status":"failure","email_ue": "当前ip超过发送次数"}'
        #生成激活码
    random_str = generate_random(10, 1)
    #邮件发送记录写入数据库
    email_record = EmailVerifyRecord()
    email_record.code = random_str
    email_record.email = email
    email_record.type = type
    email_record.ip = ip
    email_record.save()

    yield 1
    #发送验证邮件
    do_send_email_async.delay(email, random_str, type)
    yield 0


@shared_task(name='mz_user.do_send_email_async')
def do_send_email_async(email, random_str, type):
    email_title=email_body=""
    if type == 0:
        email_title = settings.EMAIL_SUBJECT_PREFIX + "注册账号激活邮件"
        email_body = """欢迎使用麦子学院账号激活功能 \r\n
请点击链接激活账号：\r
%(site_url)s/user/active/%(email)s/%(random_str)s \r\n
(该链接在24小时内有效)  \r
如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问。 \r
        """ % {'site_url': settings.SITE_URL, 'email': base64.b64encode(email), 'random_str': random_str}
    elif type == 1:
        email_title = settings.EMAIL_SUBJECT_PREFIX + "找回密码邮件"
        email_body = """欢迎使用麦子学院找回密码功能 \r\n
请点击链接重置密码：\r
%(site_url)s/user/password/reset/%(email)s/%(random_str)s \r\n
(该链接在24小时内有效)  \r
如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问。 \r
        """ % {'site_url': settings.SITE_URL, 'email': base64.b64encode(email), 'random_str': random_str}

    try:
        return send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    except Exception,e:
        logger.error(e)
        return 0


def do_active(request, email, code):
    '''
    邮箱激活
    :param request:
    :param code:激活码
    :return:
    '''
    #验证激活码是否正确或过期
    email = base64.b64decode(email)
    try:
        user = UserProfile.objects.get(email__iexact=email)
        if user.valid_email == 0:
            record = EmailVerifyRecord.objects.filter(email__iexact=email, code__exact=code, type=0).order_by("-created")
            if record:
                if datetime.now()-timedelta(days=1) > record[0].created:
                    return render(request, 'mz_common/failure.html',{'reason':'激活链接已经过期，请再次发送激活邮件'})
                # 改变账号状态
                user.valid_email = 1
                user.is_active = True
                user.save()
            else:
                return render(request, 'mz_common/failure.html',{'reason':'激活信息错误，无法激活'})
        else:
            return render(request, 'mz_common/failure.html',{'reason':'该邮箱已经被激活'})
        return render(request, 'mz_common/success.html',{'reason':'邮箱激活成功'})
    except UserProfile.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'无此用户'})


# 学生用户中心公用变量
@student_required
def student_common(request):
    # 获取章节学习总时间
    mylesson_time=request.user.mylesson.extra(select={'sum': 'sum(video_length)'}).values('sum')[0]['sum']
    if mylesson_time != None:
        mylesson_time = second_to_time(mylesson_time)
    else:
        mylesson_time = "0小时"
        # 获取课程总数
    mycourse_count = MyCourse.objects.filter(user = request.user).extra(select={'count': 'count(course)'}).values('count')[0]['count']

    locals={"mylesson_time":mylesson_time,"mycourse_count":mycourse_count}

    return locals


# 我的课程
@student_required
def student_mycourse_view(request):
    common_val = student_common(request)
    user = request.user

    #获取高校课程列表
    academic_courses = AcademicUser.objects.filter(user= request.user).order_by("-id")
    academic_course_list=[]
    course_list=[]
    for course in academic_courses:
        try:
            academic_course = AcademicCourse.objects.get(pk=course.academic_course)
            cur_careercourse = CareerCourse.objects.get(pk=course.academic_course.id)
            clazz = Class.objects.filter(students=user, career_course=cur_careercourse)
            course_lists = CourseUserTask.objects.filter(user = user,user_class = clazz,status = 2).order_by("-id")

        except AcademicCourse.DoesNotExist:
            continue
            #根据职业课程找到对应的班级,计算班级排名未完成
        curren_stu_ranking = current_user_ranking(academic_course, request.user)
        # if curren_stu_ranking != "NotSignUp":
        if len(course_lists) > 0:
            all_stu = all_stu_ranking(academic_course,request.user)
            if course_lists[0].rank_in_class:

                setattr(academic_course, "cur_ranking", course_lists[0].rank_in_class)
                setattr(academic_course, "stu_count", len(all_stu))
            else:
                setattr(academic_course, "cur_ranking", '--')
                setattr(academic_course, "stu_count", len(all_stu))
        elif curren_stu_ranking != "NotSignUp":
            setattr(academic_course, "cur_ranking", '--')
            setattr(academic_course, "stu_count", '--')
        else:
            setattr(academic_course, "cur_ranking","NotSignUp")
        academic_course_list.append(academic_course)


    # 获取职业课程列表
    mycourses = MyCourse.objects.filter(user = request.user).order_by("index","-id")
    career_course_list=[]
    course_list=[]
    class_sort_stu = 0
    for course in mycourses:
        if course.course_type == 2 :
            try:
                career_course = CareerCourse.objects.get(pk=course.course)
                #Add by Steven YU,已经添加到高校专区的，就不在这里显示
                if career_course.course_scope is not None:
                    continue

                clazz = Class.objects.filter(students=user, career_course=career_course)
                course_lists = CourseUserTask.objects.filter(user = user,user_class = clazz,status = 2).order_by("-id")
                # if len(course_list) > 0:
                #     class_sort_stu = course_list[0].rank_in_class

            except CareerCourse.DoesNotExist:
                continue
            #根据职业课程找到对应的班级,计算班级排名未完成
            curren_stu_ranking = current_user_ranking(career_course,request.user)
            # if curren_stu_ranking !="NotSignUp":
            if len(course_lists) > 0:
                all_stu = all_stu_ranking(career_course,request.user)
                if course_lists[0].rank_in_class:

                    setattr(career_course, "cur_ranking", course_lists[0].rank_in_class)
                    setattr(career_course, "stu_count", len(all_stu))
                else:
                    setattr(career_course, "cur_ranking", '--')
                    setattr(career_course, "stu_count", len(all_stu))
            elif curren_stu_ranking != "NotSignUp":
                setattr(career_course, "cur_ranking", '--')
                setattr(career_course, "stu_count", '--')
            else:
                setattr(career_course, "cur_ranking","NotSignUp")
            career_course_list.append(career_course)
        elif course.course_type == 1:
            try:
                course = Course.objects.get(pk=course.course)
            except Course.DoesNotExist:
                continue
            # 最近观看的章节
            setattr(course, "recent_learned_lesson", "还未观看过该课程")
            recent_learned_lesson = get_recent_learned_lesson(request.user, course)
            if recent_learned_lesson != None:
                course.recent_learned_lesson = "最近观看《"+str(recent_learned_lesson.lesson.name)+"》"
            course_list.append(course)
    return render(request, 'mz_user/student_mycourse_view.html',locals())


# 我的收藏
@student_required
def student_myfavorite_view(request):
    common_val = student_common(request)
    favorited_courses = MyFavorite.objects.filter(user=request.user).order_by("-date_favorite")
    current_page = int(request.GET.get('page', '1'))
    pn,pt,pl,pp,np,ppn,npn,cp,pr = instance_pager(favorited_courses,current_page,settings.COURSE_LIST_PAGESIZE)
    course_list=[]
    for favorite in pl:
        # 最近观看的章节
        setattr(favorite.course, "recent_learned_lesson", "还未观看过该课程")
        recent_learned_lesson = get_recent_learned_lesson(request.user, favorite.course)
        if recent_learned_lesson != None:
            favorite.course.recent_learned_lesson = "最近观看《"+str(recent_learned_lesson.lesson.name)+"》"
        course_list.append(favorite.course)
    return render(request, 'mz_user/student_myfavorite_view.html',locals())


# 我的证书
@student_required
def student_mycertificate_view(request):
    common_val = student_common(request)
    certificate_list = request.user.certificate.all()
    current_page = int(request.GET.get('page', '1'))
    pn,pt,pl,pp,np,ppn,npn,cp,pr = instance_pager(certificate_list,current_page,settings.COURSE_LIST_PAGESIZE)
    return render(request, 'mz_user/student_mycertificate_view.html',locals())


# 证书下载
@student_required
def student_mycertificate_download(request,certificate_id):
    # 根据证书ID获取证书图片路径
    certificate = Certificate.objects.get(pk=certificate_id)
    filename = settings.SITE_URL+settings.MEDIA_URL+str(certificate.image_url)
    f = urllib2.urlopen(filename, timeout=3)
    data = f.read()
    f.close()

    # 以证书名称作为下载名称
    filename = "certificate_"+str(certificate.id)+"."+str(certificate.image_url).split(".")[-1]
    response = HttpResponse(data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


# 用户的消息
@login_required(login_url="/")
def user_mymessage_view(request):
    common_val = student_common(request)
    message_list_tmp = MyMessage.objects.filter(Q(userB = request.user.id) | Q(userB = 0,action_type = 1)).order_by("-date_action")
    current_page = int(request.GET.get('page', '1'))
    pn,pt,pl,pp,np,ppn,npn,cp,pr = instance_pager(message_list_tmp,current_page,settings.MYMESSAGE_PAGESIZE)
    message_list = []
    for message in pl :
        #将消息设置为已读
        message.is_new = False
        message.date_action = message.date_action
        message.save()
        #根据需要取出对应信息
        if message.userA != 0 and message.userA != None:
            userA = UserProfile.objects.filter(pk=message.userA)[:1]
            message.userA = userA[0] if userA else ''
        if message.action_type == "2" :
            #课程
            action_id = Lesson.objects.filter(pk=message.action_id)[:1]
            message.action_id = action_id[0] if action_id else ''
        if message.action_type == "3" :
            #替换内容中的链接地址
            hyperlink_pat = re.compile(r'<\s*[Aa]{1}\s+[^>]*?[Hh][Rr][Ee][Ff]\s*=\s*[\"\']?([^>\"\']+)[\"\']?.*?>')
            comment_pat = re.compile(r'<!--(.*?)-->')
            html_source = comment_pat.sub('', message.action_content)
            match_links = hyperlink_pat.findall(html_source)
            for links in match_links:
                links_new = links.replace(links,settings.BBS_SITE_URL+"/"+links)
                message.action_content = message.action_content.replace(links,links_new)
        # 教师督促学生
        if message.action_type == "4":
            # 获取班级编号
            position = message.action_content.find("*")
            class_number = message.action_content[:position]
            message.action_content = message.action_content[position + 1:]
            class_id = Class.objects.filter(coding=class_number)[0].career_course_id
        message_list.append(message)
    return render(request, 'mz_user/user_mymessage_view.html',locals())


# 老师班级中心
@teacher_required
def teacher_myclass_view(request):
    # 获取老师课程列表
    try:
        user= request.user
        if user.is_academic_teacher():
            ac_user = AcademicUser.objects.get(user = user)
            school = ac_user.owner_college
            acourse = AcademicCourse.objects.filter(owner=school)
            for course in acourse:
                classobj = AcademicClass.objects.get(career_course_id=course.id)
                setattr(course, "class_id",classobj.id)
            return render(request, 'mz_user/school_teacher_view.html', locals())
        else:
            classing = Class.objects.filter(teachers = request.user,status = 1,is_active = True).annotate(num_students=Count('students'))
            classfinish = Class.objects.filter(teachers = request.user,status = 2,is_active = True).annotate(num_students=Count('students'))
            return render(request, 'mz_user/teacher_myclass_view.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    return HttpResponse("failure", content_type="text/plain")


# 个人资料 - 头像裁切
@login_required(login_url="/")
def avatar_crop(request):

    marginTop=0
    marginLeft=0
    width=0
    height=0
    picheight=0
    picwidth=0

    if request.GET.get('marginTop'):
        marginTop=int(request.GET.get('marginTop'))
    if request.GET.get('marginLeft'):
        marginLeft=int(request.GET.get('marginLeft'))
    if request.GET.get('width'):
        width=int(request.GET.get('width'))
    if request.GET.get('height'):
        height=int(request.GET.get('height'))
    if request.GET.get('picheight'):
        picheight=int(request.GET.get('picheight'))
    if request.GET.get('picwidth'):
        picwidth=int(request.GET.get('picwidth'))

    #裁切
    avatar_up_small = "" #upload Thumbnail
    avatar_target_path = ""
    avatar_middle_target_path = ""
    avatar_small_target_path = ""
    try:
        # 获取头像临时图片名称
        avatar_tmp = request.session.get("avatar_tmp",None)
        source_path = os.path.join(settings.MEDIA_ROOT,'temp',avatar_tmp)
        avatar_up_small = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_thumbnail.jpg"
        avatar_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_big.jpg"
        avatar_middle_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_middle.jpg"
        avatar_small_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_small.jpg"
        f = Image.open(source_path)
        f.resize((picwidth,picheight),Image.ANTIALIAS).save(avatar_up_small, 'jpeg', quality=100)
        ft = Image.open(avatar_up_small)
        box=(marginTop,marginLeft,marginTop+width,marginLeft+height)
        # box(0,0,100,100)
        ft.crop(box).resize((220,220), Image.ANTIALIAS).save(avatar_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((104,104), Image.ANTIALIAS).save(avatar_middle_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((70,70), Image.ANTIALIAS).save(avatar_small_target_path, 'jpeg', quality=100)

        # 读取原来的头像信息并删除(默认图片不能删除，by guotao 2015.9.23)
        if str(request.user.avatar_url).count('/')>1 and avatar_tmp != str(request.user.avatar_url).split("/")[-1] :
            avatar_url_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_url)
            avatar_middle_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_middle_thumbnall)
            avatar_small_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_small_thumbnall)
            if os.path.exists(avatar_url_path) :
                os.remove(avatar_url_path)
            if os.path.exists(avatar_middle_thumbnall_path) :
                os.remove(avatar_middle_thumbnall_path)
            if os.path.exists(avatar_small_thumbnall_path) :
                os.remove(avatar_small_thumbnall_path)
    except Exception,e:
        logger.error(e)

    # 将裁切后的图片路径信息更新图片字段
    request.user.avatar_url = avatar_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.avatar_middle_thumbnall = avatar_middle_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.avatar_small_thumbnall = avatar_small_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.save()

    if request.user.uid:
        sync_avatar(request.user.uid, avatar_target_path)

    return HttpResponse('{"status":"success"}', content_type="application/json")


def sync_avatar(forum_uid, big):
    import shutil

    root_path = settings.PROJECT_ROOT
    filename, extension = os.path.splitext(big)
    filename = filename.split("../")[-1]
    pure_name = '_'.join(filename.split('_')[:-1])

    forum_uid = "%09d" % forum_uid
    dir1 = forum_uid[0:3]
    dir2 = forum_uid[3:5]
    dir3 = forum_uid[5:7]
    prefix = forum_uid[-2:]

    for size in ('big', 'middle', 'small'):
        main_avatar_path = root_path + "/" + pure_name + '_' + size + extension

        forum_avatar_dir_path = root_path + '/forum/uc_server/data/avatar/' + dir1 + '/' + dir2 + '/' + dir3

        if not os.path.exists(forum_avatar_dir_path):
            os.makedirs(forum_avatar_dir_path)

        avatar_name = prefix + '_avatar_' + size + extension
        forum_avatar_path = forum_avatar_dir_path + '/' + avatar_name
        if os.path.exists(forum_avatar_path):
            os.remove(forum_avatar_path)

        shutil.copyfile(main_avatar_path, forum_avatar_path)


# 个人资料 - 头像上传
@csrf_exempt
@login_required(login_url="/")
def avatar_upload(request):
    ret="0"
    file = request.FILES.get("Filedata",None)
    if file:
        result =_upload(file)
        if result:
            if result[0] == True:
                ret='{"status":"success","filename":"'+str(result[1])+'","width":'+str(result[2])+',"height":'+str(result[3])+'}'
            else:
                ret='{"status":"failure","message":"'+str(result[1])+'"}'
                #头像上传成功，则暂时保存头像名称的session
            request.session['avatar_tmp'] = result[1]
    return HttpResponse(ret, content_type="text/plain")


#头像图片上传
def _upload(file):
    '''''图片上传函数'''
    if file:
        if file.size / 1024 > settings.AVATAR_SIZE_LIMIT :
            return (False,"头像大小超过"+str(settings.AVATAR_SIZE_LIMIT)+"KB限制")
            # 判断图片格式
        if settings.AVATAR_SUFFIX_LIMIT.find(file.name.split(".")[-1]) == -1 :
            return (False,"头像必须为GIF/JPG/PNG/BMP格式")
        path=os.path.join(settings.MEDIA_ROOT,"temp")
        if not os.path.exists(path): #如果目录不存在创建目录
            os.makedirs(path)

        file_name=str(uuid.uuid1())+".jpg"
        path_file=os.path.join(path,file_name)
        parser = ImageFile.Parser()
        for chunk in file.chunks():
            parser.feed(chunk)
        img = parser.close()
        try:
            if img.mode != "RGB":
                img = img.convert("RGB")
            width, height = img.size
            img.save(path_file, 'jpeg', quality=100)
        except Exception,e:
            logger.error(e)
            return (False,"头像上传失败")
        return (True,file_name, width, height)
    return (False,"头像上传失败")


# 用户的个人资料
@login_required(login_url="/")
def user_myinfo_view(request):
    common_val = student_common(request)
    changeform = ChangePassword(request.POST)
    user = request.user
    update_mobile_form = UpdateMobileForm({'mobile_um':user.mobile,'uid_um':user.id})
    update_email_form = UpdateEmailForm({'email_ue':user.email,'uid_ue':user.id})
    mobile_code_update_mobile_form = FindPasswordMobileForm()
    userform = UserInfoSave({'nick_name':user.nick_name,'position':user.position,'description':user.description,'qq':user.qq,'mobile':user.mobile,
                             'email':user.email,'studygoal':user.study_goal_opt.index if user.study_goal_opt else 0,
                             'studybase':user.study_base_opt.index if user.study_base_opt else 0})

    return render(request, 'mz_user/user_myinfo_view.html', locals())


# 根据省份查城市
@login_required(login_url="/")
def city_list(request):
    provid = request.GET['provid']
    city_list = {}
    citys = CityDict.objects.filter(province = provid)
    for city in citys:
        city_list.setdefault("cityid", []).append([city.id,city.name])
    return HttpResponse(json.dumps(city_list), content_type="application/json")


#用户信息保存
@login_required(login_url="/")
def user_info_save(request):
    try:
        # logger.error('mz_user:user_info_save:')
        # logger.error('mz_user:user_info_save:' + str(request.POST))
        userinfosave = UserInfoSave(request.POST)
        goal_text = request.POST.get('goal_text', None)
        base_text = request.POST.get('base_text', None)

        if userinfosave.is_valid():
            nick_name = userinfosave.cleaned_data["nick_name"]
            real_name = userinfosave.cleaned_data["real_name"]
            gender = None
            if userinfosave.cleaned_data["gender"] in (u'1', u'2'):
                gender = userinfosave.cleaned_data["gender"]
            degree = userinfosave.cleaned_data["degree"]
            address = userinfosave.cleaned_data["address"]
            position = userinfosave.cleaned_data["position"]
            description = userinfosave.cleaned_data["description"]
            qq = userinfosave.cleaned_data["qq"]
            cityid = userinfosave.cleaned_data["city"]
            try:
                birthday_year = request.POST["birthday_year"]
                birthday_month = request.POST["birthday_month"]
                birthday_day = request.POST["birthday_day"]
                birthday = "".join([birthday_year, '-', birthday_month, '-', birthday_day])
            except Exception, e:
                logger.error(e)
                birthday = '1990-01-01'
            user = request.user

            if userinfosave.cleaned_data["studygoal"]:
                study_goal = userinfosave.cleaned_data["studygoal"]
                studygoal = StudyGoal.objects.get(index=study_goal).name
                if str(studygoal) == "其他":
                    if goal_text is None or goal_text == "":
                        valid_msg = {'goal_text': '学习目标不能为空'}
                    if len(goal_text) > 20:
                        valid_msg = {'goal_text': '学习目标长度不能超过20个字符'}
                    user.study_goal = goal_text
                    user.study_goal_opt = StudyGoal.objects.get(index=study_goal)
                else:
                    user.study_goal = StudyGoal.objects.get(index=study_goal).name
                    user.study_goal_opt = StudyGoal.objects.get(index=study_goal)

            if userinfosave.cleaned_data["studybase"]:
                study_base = userinfosave.cleaned_data["studybase"]
                studybase = StudyBase.objects.get(index=study_base).name
                if str(studybase) == "其他":
                    if base_text is None or goal_text == "":
                        valid_msg = {'base_text': '学习基础不能为空'}
                    if len(base_text) > 20:
                        valid_msg = {'base_text': '学习基础长度不能超过20个字符'}
                    user.study_base = base_text
                    user.study_base_opt = StudyBase.objects.get(index=study_base)
                else:
                    user.study_base = StudyBase.objects.get(index=study_base).name
                    user.study_base_opt = StudyBase.objects.get(index=study_base)

            user.nick_name = nick_name
            user.real_name = real_name
            user.gender = gender
            user.birthday = birthday
            user.degree = degree
            user.address = address
            user.position = position
            user.city_id = cityid
            user.description = description
            user.qq = qq
            user.save()
            all_info_registed = user.is_all_info_registed()

            need_regist_all = 'lps=3' in request.META['HTTP_REFERER']
            if need_regist_all:
                if all_info_registed:#所有信息完善
                    return HttpResponse('{"status":"个人信息已经完善,您可以去进行学习啦!"}', content_type="application/json")
                else:#未完善所有信息
                    # 注释内容: 指定未完成字段
                    # uncompleted_field = user.uncompleted_field()
                    # return HttpResponse('{"status":"信息已保存,但是个人信息还不够完善,暂时还不能进行学习哦!", "reason": ' + uncompleted_field + '}', content_type="application/json")
                    return HttpResponse('{"status":"信息已保存,但是个人信息还不够完善,暂时还不能进行学习哦!"}', content_type="application/json")
            else:#正常保存流程
                return HttpResponse(json.dumps(''), content_type="application/json")
            #uc_user_edit(request, user.uid, user.nick_name, user.password, '', user.email)
    except IntegrityError:
        return HttpResponse('{"status":"昵称（姓名）不能重复"}', content_type="application/json")
    except Exception as e:
       logger.error(e)
       return HttpResponse('{"status":"操作失败，请稍后再试"}', content_type="application/json")
    return HttpResponse(json.dumps(userinfosave.errors), content_type="application/json")


# 个人资料保存 - 发送激活邮件
@login_required(login_url="/")
def user_info_email(request):
    email = request.POST["email"]
    error_message=""
    #检验手机号码格式
    if email == "":
        error_message = '{ "email":"请输入邮箱账号" }'
    else:
        p=re.compile(settings.REGEX_EMAIL)
        if not p.match(email):
            error_message = '{ "email":"邮箱账号格式不正确" }'
    if error_message != "":
        return HttpResponse(error_message, content_type="application/json")
    #发送激活邮件
    result = do_send_mail(email, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 0)
    return HttpResponse(result, content_type="application/json")

# 个人资料 - 密码修改
@login_required(login_url="/")
def change_password(request):
    changeform = ChangePassword(request.POST)
    if changeform.is_valid():
        account = request.user.username
        original_pass = changeform.cleaned_data["original_pass"]
        pass1 = changeform.cleaned_data["newpass1"]
        user = authenticate(username=account, password=original_pass)
        if user is not None:
            request.user.password = make_password(pass1)
            request.user.save()
            # uc_user_edit(request, user.uid, user.nick_name, user.password, pass1, user.email)
        else:
            error_message = '{ "error":"原密码不正确" }'
            return HttpResponse(error_message, content_type="application/json")
    return HttpResponse(json.dumps(changeform.errors), content_type="application/json")

# 个人资料 - 手机修改验证 - 短信发送
@login_required(login_url="/")
def user_update_mobile_sendsms(request):
    update_mobile_form = UpdateMobileForm(request.POST)
    if update_mobile_form.is_valid():
        # 验证码验证
        try:
            result = validate(request)
        except KeyError:
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        request.session['captcha_status'] = '1'
        #验证通过返回成功，发送短信并继续下一步
        mobile_um = update_mobile_form.cleaned_data["mobile_um"]
        request.session["new_update_mobile"] = mobile_um
        result = do_send_sms_signup(mobile_um, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 1)
        return HttpResponse(result, content_type="application/json")
    return HttpResponse(json.dumps(update_mobile_form.errors), content_type="application/json")

# 个人资料 - 手机修改验证 - 保存数据
@login_required(login_url="/")
def user_update_mobile(request):
    update_mobile_form = FindPasswordMobileForm(request.POST)
    if update_mobile_form.is_valid():
        try:
            request.user.mobile = request.session["new_update_mobile"]
            request.user.username = request.session["new_update_mobile"]
            request.user.valid_mobile = 1
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        except Exception,e:
            logger.error(e)
            return HttpResponse('{"status":"failure"}', content_type="application/json")
    return HttpResponse(json.dumps(update_mobile_form.errors), content_type="application/json")

# 个人资料 - 邮箱修改验证
@login_required(login_url="/")
def user_update_email(request):
    update_email_form = UpdateEmailForm(request.POST)
    if update_email_form.is_valid():
        # 验证码验证
        try:
            result = validate(request)
        except KeyError:
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return HttpResponse('{"captcha": "验证码错误"}', content_type="application/json")
        request.session['captcha_status'] = '1'
        email = update_email_form.cleaned_data["email_ue"]
        request.user.email = email
        request.user.username = email
        request.user.valid_email = 0
        request.user.save()
        result = do_send_mail(email, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 0)
        if result == 1 :
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(result, content_type="application/json")
    return HttpResponse(json.dumps(update_email_form.errors), content_type="application/json")

# 个人资料 - 实时取回邮箱
@login_required(login_url="/")
def user_fetch_email(request):
    email = get_object_or_404(UserProfile, id=request.user.id).email
    email_json = {'email': email}
    return HttpResponse(json.dumps(email_json), content_type="application/json")

# 个人资料 - 实时取回电话
@login_required(login_url="/")
def user_fetch_mobile(request):
    mobile = get_object_or_404(UserProfile, id=request.user.id).mobile
    mobile_json = {'mobile': mobile}
    return HttpResponse(json.dumps(mobile_json), content_type="application/json")

#获取职业课程
@teacher_required
def get_careercourse(request):
    allcourse = CareerCourse.objects.filter(course_scope=None)
    json_str = [{"id":c.id,"name":c.name.strip(),"short":c.short_name.upper()} for c in allcourse ]
    return HttpResponse(json.dumps(json_str),content_type="application/json")


def create_class_save(request):
    classno =""
    qun = ""
    classno = request.POST['classno']
    qun = request.POST['qun']
    selectclass = request.POST['selectclass']
    se_year = request.POST['se_year']
    se_month = request.POST['se_month']
    se_day = request.POST['se_day']
    meeting_duration = request.POST.get('meeting_duration')
    if qun =="":
        message = '{"message":"QQ群不能为空"}'
        return HttpResponse(message,content_type="application/json")
    is_true = Class.objects.xall().filter(coding=classno)
    if is_true:
        message = '{"message":"创建的班级号已经存在"}'
        return HttpResponse(message,content_type="application/json")

    if classno != "" : #判断班级号是否存在
        createclass = Class()
        createclass.student_limit=30
        timedate = se_year+"-"+se_month+"-"+se_day
        createclass.coding = str(classno)
        createclass.qq = qun
        createclass.date_open = timedate

        createclass.career_course_id = selectclass
        # add by yiming for lps 3.0
        if meeting_duration and int(meeting_duration) > 0:
            createclass.lps_version = '3.0'
            createclass.meeting_duration = meeting_duration
        createclass.save()
        ClassTeachers.objects.create(teacher=request.user, teacher_class=createclass)
        message = '{"message":"success"}'
    else:
        message = '{"message":"error"}'
    return HttpResponse(message,content_type="application/json")

###################### 移动端登录注册 开始 #######################################
def mobile_login_view(request):
    if request.user.is_authenticated():
        return render(request, 'mz_common/failure.html',{'reason':'已经登录，无须重复登录。<a href="javascript:history.go(-1)">返回</a>'})
    login_form = LoginForm()
    # 上一个页面请求地址
    source_url = request.META.get('HTTP_REFERER', '')
    return render(request, 'mz_user/mobile_login.html',locals())
def mobile_register_view(request):
    if request.user.is_authenticated():
        return render(request, 'mz_common/failure.html',{'reason':'已经登录，不能注册。<a href="javascript:history.go(-1)">返回</a>'})
    login_form = LoginForm()
    email_register_form = EmailRegisterForm()
    mobile_register_form = MobileRegisterForm()
    # 上一个页面请求地址
    source_url = request.GET.get("source_url", None)
    if source_url == None: source_url = settings.SITE_URL
    return render(request, 'mz_user/mobile_register.html',locals())
###################### 移动端登录注册 结束 #######################################


#获取学习目标下拉列表的值
@csrf_exempt
def get_study_goal(request):
    try:
        study_goals = StudyGoal.objects.all()
    except Exception as e:
        logger.error(e)

    list = [{
                "id": obj.id,
                "name": obj.name,
                "index": obj.index
            } for obj in study_goals]
    return HttpResponse(json.dumps(list), content_type="application/json")

#获取专业基础下拉列表的值
@csrf_exempt
def get_study_base(request):
    try:
        study_base = StudyBase.objects.all()
    except Exception as e:
        logger.error(e)

    list = [{
                "id": obj.id,
                "name": obj.name,
                "index": obj.index
            } for obj in study_base]
    return HttpResponse(json.dumps(list), content_type="application/json")


# 获取老用户头像以及真实姓名，教师的个人介绍以及学生的学习目标和学习基础
@csrf_exempt
def get_photo_and_nickname(request):
    user_id = request.user.id
    try:
        user_info = UserProfile.objects.get(id=user_id)
    except Exception as e:
        logger.error(e)
    user_name = ""
    photo_path = ""

    if user_info.nick_name:
        user_name = user_info.nick_name
    if user_info.avatar_middle_thumbnall:
        photo_path = user_info.avatar_middle_thumbnall.url

    result = {
        "nick_name": user_name,
        "avatar_middle_thumbnall": photo_path,
        "people": ""
    }
    # 获取教师的描述信息
    if request.user.is_teacher():
        result["people"] = "教师"
        user_description = ""
        if user_info.description:
            user_description = user_info.description
        result["description"] = user_description
    # 登陆账号为学生账号
    if request.user.is_student():
        result["people"] = "学生"
    return HttpResponse(json.dumps(result), content_type="application/json")

def send_again_mail(request):
    if request.GET:
        email = request.GET['username']
        if do_send_mail(email,request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 0) == 1:
            return HttpResponse(json.dumps({'status':1}),content_type='application/json')
        return HttpResponse(json.dumps({'status':0}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status':0}),content_type='application/json')

def connect(request):
    partner = request.GET.get('partner')
    referer = request.META.get('HTTP_REFERER') or settings.SITE_URL
    redirect_uri = '%s/user/connect/success/?partner=%s&referer=%s' % \
                   (settings.SITE_URL, partner, urllib.quote(referer))
    if partner == 'qq':
        from mz_oauth import QQAuth2
        auth_url = QQAuth2.get_qq_token(settings.QQ_AUTH_URL,
                                        settings.QQ_ID, redirect_uri)
        return HttpResponseRedirect(auth_url)
    elif partner == 'wechat':
        from mz_oauth import WeiXinAuth2
        auth_url = WeiXinAuth2.get_weixin_code(settings.WEIXIN_AUTH_URL,
                    settings.WEIXIN_ID, redirect_uri)
        return HttpResponseRedirect(auth_url)
    raise Http404

def get_weixin_auth_token(request):
    """
    @brief 获得微信用户的token, openid等信息
    :param request:
    :return:

    @note: 用户登陆暂未实现. 关于用户登陆的几点说明:
           用户登陆之后, 可以避免用户重复授权. 实现用户登陆, 有两种方案:
            1. 为第三方用户建立userprofile记录;
            2. 重新实现Django的session管理机制
           目前两种方案都很重, 所以暂不实现.
    @todo 随着产品的演进, 实现用户登陆
    """
    code = request.GET.get('code')
    if not code:
        raise Http404
    redirect_url = request.GET.get('referer', settings.SITE_URL)
    success, access_token, openid = WeiXinAuth2.get_weixin_page_token(code)
    if success and access_token and openid:
        user_data = dict(partner='wechat', openid=openid, token=access_token)
        result, nick_name, head_image = WeiXinAuth2.get_weixin_page_user_info(access_token, openid)
        nick_name = nick_name.encode("utf8")
        if result and nick_name:
            user_data['nickname'] = nick_name
        try:  # 建立第三方用户档案, 如果失败, 不能影响用户参与课程
            db.api.user.user.create_or_update_third_party_user(**user_data)
        except Exception as e:
            logger.error(str(e))
        # 用户登陆, 暂未实现
        redirect_url = mz_user.functions.url_add_params(redirect_url, login=True, openid=openid,
                                                        nick_name=nick_name if nick_name else None,
                                                        head_image=head_image)
        redirect_url = '%s#2' % redirect_url  # 定位tab
        return HttpResponseRedirect(redirect_url)
    raise Http404

def connect_success(request):
    partner = request.GET.get('partner')
    code = request.GET.get('code', '')
    third_login_url = request.GET.get('referer', settings.SITE_URL)
    success, openid, token, nickname_check, nickname = False, None, None, False, None
    if partner == 'qq':
        from mz_oauth import QQAuth2
        success, openid, token = QQAuth2.get_openid(settings.QQ_TOKEN_URL,
                                                  settings.QQ_OPENID_URL,
                                                  settings.QQ_ID, settings.QQ_KEY,
                                                  code, settings.SITE_URL)
        nickname_check, nickname = QQAuth2.get_nicknameforqq(settings.QQ_USERINFO_URL, token, openid, settings.QQ_ID)
    elif partner == 'wechat':
        from mz_oauth import WeiXinAuth2
        success, openid, token = WeiXinAuth2.get_openid(settings.WEIXIN_TOKEN_URL,
                                                      settings.WEIXIN_AUTH_TOKEN_URL,
                                                      settings.WEIXIN_ID, settings.WEIXIN_KEY, code)
        nickname_check, nickname = WeiXinAuth2.get_nicknameforweixin(settings.WEIXIN_USERINFO_URL, token, openid)
    if success and openid and token:
        params = dict(partner=partner, openid=openid)
        third_party_user, created = ThirdPartyUser.objects.get_or_create(**params)
        third_party_user.token = token
        if nickname_check and nickname:
            third_party_user.nickname = nickname
        third_party_user.save()
        if third_party_user.user:
            if third_party_user.user.is_active:
                third_party_user.user.backend = 'mz_user.auth.CustomBackend'
                login(request, third_party_user.user)
                return HttpResponseRedirect(third_login_url)
            else:
                third_login_url = mz_user.functions.url_add_params(third_login_url, verify_email=third_party_user.user.email)
                return HttpResponseRedirect(third_login_url)
        else:
            if partner == 'qq':
                third_login_url = mz_user.functions.url_add_params(third_login_url, partner=third_party_user.partner,
                                                                   openid=third_party_user.openid,
                                                                   qq_nickname=third_party_user.nickname if partner == 'qq' else None)
            else:
                third_login_url = mz_user.functions.url_add_params(third_login_url, partner=third_party_user.partner,
                                                                   openid=third_party_user.openid)
            return HttpResponseRedirect(third_login_url)
    raise Http404


# 个人中心第三方绑定
def user_center_third(partner, openid, user_id):
    try:
        thirdpartyuser, created = ThirdPartyUser.objects.get_or_create(partner=partner, openid=openid)
        if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user_id=int(user_id))):
            thirdpartyuser.user_id = int(user_id)
            thirdpartyuser.save()
            return True
    except Exception, e:
        logger.error('第三方接口绑定POST：%s' % e)
        return False


@csrf_exempt
def connect_from_fps_settings(request):
    if request.method == 'GET' and request.GET.get('get_info'):
        user_id = request.GET.get('user_id')
        try:
            users = ThirdPartyUser.objects.filter(user_id=int(user_id))
            users = [dict(partner=user.partner, openid=user.openid, nickname=user.nickname,
                          user_id=user.user_id, token=user.token, id=user.id
                          ) for user in users]
            return HttpResponse(json.dumps(users), content_type="application/json")
        except Exception, e:
            logger.error('第三方接口绑定GET：%s' % e)
    if request.method == 'GET' and request.GET.get('openid'):
        partner = request.GET.get('partner')
        openid = request.GET.get('openid')
        user_id = request.GET.get('user_id')
        try:
            thirdpartyuser, created = ThirdPartyUser.objects.get_or_create(partner=partner, openid=openid)
            if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user_id=int(user_id))):
                thirdpartyuser.user_id = int(user_id)
                thirdpartyuser.save()
                return HttpResponse('ok')
        except Exception, e:
            logger.error('第三方接口绑定POST：%s' % e)
    if request.method == 'GET' and request.GET.get('id'):
        id = request.GET.get('id')
        try:
            user = ThirdPartyUser.objects.get(id=int(id))
            user.delete()
            return HttpResponse('ok')
        except Exception, e:
            logger.error('第三方接口绑定DELETE：%s' % e)
    raise Http404

@login_required()
def get_invitation_code(request):
    if request.method == 'GET':
        invitation_code = functions.get_invitation_code(request.user.id)  # 获取分享链接
        qrcode = functions.get_qrcode_file_path(invitation_code)  # 获取 qrcode
        payload = dict(invitation_link='%s/?ic=%s' % (settings.SITE_URL+'/user/invitation/share', invitation_code), qrcode=qrcode)
        return JsonResponse(payload)
    raise Http404

# @csrf_exempt
# def get_qr_code(request):
#     if request.method == 'POST':
#         qrcode = generate_qrcode(request.user.id)
#         print qrcode
#         qrcode = '<img src="data:image/png;' + qrcode + '"/>'
#         print qrcode
#         # return HttpResponse(qrcode, content_type="image/png")
#         return HttpResponse(qrcode)
#     raise Http404

def get_invitation_link_page(request, invitation_code):
    return render(request, 'mz_user/user_share_introduce.html',
                  {'invitation_link': '%s/?ic=%s' % (settings.SITE_URL, invitation_code)})

def judge_nick_name_is_exist(request):
    nick_name = request.GET.get('nick_name', '')
    jsonp = request.GET.get('jsonp', '')

    if request.user.is_authenticated():
        if request.user.nick_name == nick_name:
            return HttpResponse('%s(%s)' % (jsonp, json.dumps({'status':0, 'is_exist': '0'})),content_type='application/json')

    if UserProfile.objects.filter(nick_name=nick_name).count():
        return HttpResponse('%s(%s)' % (jsonp, json.dumps({'status':0, 'is_exist': '1'})),content_type='application/json')
    return HttpResponse('%s(%s)' % (jsonp, json.dumps({'status':0, 'is_exist': '0'})),content_type='application/json')


# 登陆页
def sign_up(request):
    invitation_code = request.GET.get('ic', '')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render(request, 'mz_common/sign_up.html', locals())


# 登陆成功页面dd
@login_required(login_url="/")
def sign_success(request):
    return render(request, 'mz_common/sign_success.html')


@login_required(login_url="/")
def save_job_intention_info(request):
    save_job_info(request.user.id, request.POST.dict())
    class_id = int(request.POST['class_id'])
    return HttpResponseRedirect(reverse("lps3:student_class",
                                        kwargs=dict(class_id=class_id)))


@login_required(login_url="/")
def save_job_intention_info_lps_3_1(request):
    save_job_info(request.user.id, request.POST.dict())
    career_id = int(request.POST['career_id'])
    return HttpResponseRedirect(reverse("lps4_index", kwargs=dict(career_id=career_id)))


# 转介绍链接页
def invitation_link(request):
    link_display = False
    if request.user.is_authenticated():
        if request.user.is_student():
            if ClassStudents.objects.filter(user=request.user, student_class__class_type=Class.CLASS_TYPE_NORMAL).exists():
                link_display = True
    return render(request, 'mz_user/user_add_invite.html', locals())


# 转介绍跳往注册页
def invitation_share(request):
    invitation_code = request.GET.get('ic', None)
    return render(request, 'mz_user/user_add_invitation.html', locals())
