# -*- coding: utf-8 -*-
import xadmin
from models import *
from mz_pay.views import order_handle
from mz_user.models import UserUnlockStage
from mz_lps.models import ClassStudents
from mz_common.views import get_study_point, sys_send_message, app_send_message
from django.core.mail import send_mail
from mz_user.models import MyCourse

class UserPurchaseAdmin(object):
    list_display = ('user', 'pay_price', 'order_no', 'pay_type', 'date_add', 'pay_status', 'id')
    list_filter = ('pay_type', 'pay_way', 'pay_status')
    search_fields = ['order_no', 'trade_no', 'user__mobile', 'user__email']

    def save_models(self):
        obj = self.new_obj
        if obj.pay_status == 1:
            purchase = UserPurchase.objects.get(pk=obj.pk)
            if purchase.pay_status == 0:
                try:
                    # 根据商户订单号查询到对应订单信息
                    trade_status = "TRADE_SUCCESS"
                    purchase = UserPurchase.objects.get(order_no=obj.order_no)
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
                    # 订单对应班级
                    cur_class = Class.objects.xall().get(coding=purchase.pay_class.coding)
                    return_qq = cur_class.qq
                    return_career_id = cur_class.career_course.id
                    if purchase.pay_status == 1:
                        return ("success", return_qq, return_career_id)
                    if trade_status in ('TRADE_FINISHED', 'TRADE_SUCCESS'):
                        # 解锁相应的阶段
                        # 获取该订单对应的阶段
                        for stage in purchase.pay_stage.xall().filter(userpurchase=purchase):
                            unlock_stage, created = UserUnlockStage.objects.get_or_create(user=purchase.user, stage=stage)

                        #修改班级目前报名人数和更新学员到对应班级
                        if cur_class.students.filter(pk=purchase.user.id).count() == 0:
                            cur_class.current_student_count += 1
                            cur_class.save()
                            class_students = ClassStudents()
                            class_students.student_class = cur_class
                            class_students.user = purchase.user
                            # 获取当前学力
                            class_students.study_point = get_study_point(purchase.user, cur_class.career_course)
                            class_students.save()

                            #### 给学生发送通知消息 开始 ####

                            # 发送站内信
                            alert_msg = "恭喜你报名成功，请加入"+str(cur_class.coding)+"班QQ群"+str(cur_class.qq)+"开始和同学一起学习吧！"
                            sys_send_message(0, purchase.user.id, 1, alert_msg + "<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(cur_class.career_course.id)+"'>进入课程LPS</a>")

                            # 发送邮件
                            if purchase.user.email is not None:
                                try:
                                    send_mail(settings.EMAIL_SUBJECT_PREFIX + "班级报名成功邮件", alert_msg, settings.EMAIL_FROM, [purchase.user.email])
                                except Exception as e:
                                    pass

                            # app推送
                            app_send_message("系统消息", alert_msg, [purchase.user.token])

                            #### 给学生发送通知消息 结束 ####

                            #### 给对应带班老师发送通知消息 开始 ####
                            # alert_msg = "有新生报名了你的班级"+str(cur_class.coding)+"，<a href='http://www.maiziedu.com/lps2/teach/plan/"+str(cur_class.id)+"/"+str(purchase.user.id)+"/'>快去看看吧！</a>"
                            # sys_send_message(0, cur_class.teacher.id, 1, alert_msg)

                            # alert_msg = "有新生报名了你的班级"+str(cur_class.coding)+"，快去看看吧！</a>"
                            #
                            # app_send_message("系统消息", alert_msg, [cur_class.teacher.token])
                            #### 给对应带班老师发送通知消息 结束 ####

                        # 根据付款方式（首付、全额、余款）来更新班级权限使用的截止时间
                        class_students = ClassStudents.objects.get(student_class=cur_class, user=purchase.user)
                        if purchase.pay_type == 1:
                            # 首付计算截止时间(30天)
                            class_students.deadline = datetime.now() + timedelta(days=15)

                        elif purchase.pay_type == 0 or purchase.pay_type == 2:
                            # 截止时间为None表示全额或余款支付，没有截止时间限制
                            class_students.deadline = None
                        class_students.save()

                        #添加职业课程到我的课程
                        if MyCourse.objects.filter(user=purchase.user, course=purchase.pay_careercourse.id, course_type=2).count() == 0 :
                            my_course = MyCourse()
                            my_course.user = purchase.user
                            my_course.course = purchase.pay_careercourse.id
                            my_course.course_type = 2
                            my_course.index = 1
                            my_course.save()

                        # 改变该订单的状态
                        purchase.trade_no = ""
                        purchase.date_pay = datetime.now()
                        purchase.pay_status = 1
                        purchase.save()

                        return ("success", return_qq, return_career_id)
                    elif trade_status != "WAIT_BUYER_PAY":
                        purchase.pay_status = 2
                        purchase.save()
                except Exception as e:
                    pass
                return ("fail","lose")
            obj.save()
        else:
            obj.save()


class UserPayBindAdmin(object):
    list_display = ('user_id', 'careercourse_id', 'status')
    search_fields = ['user_id', 'careercourse_id']


xadmin.site.register(UserPurchase, UserPurchaseAdmin)
xadmin.site.register(UserPayBind, UserPayBindAdmin)

