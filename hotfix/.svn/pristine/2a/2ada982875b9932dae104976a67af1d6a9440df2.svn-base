# -*- coding: utf-8 -*-

# version 2.0
# modify record
# -------------
from django.db import models
from datetime import datetime
from django.conf import settings
from mz_course.models import *
from mz_lps.models import Class
from mz_lps3.foreignkey_manager import CustomManagerForeignKey


# 支付订单模型.
class UserPurchase(models.Model):
    PAY_TYPES = {0: u"全款", 1: u"试学首付款", 2: u"尾款", 3: u"阶段款", 5: u"宜分期", 6:u'无就业全款价格',
                 7: u'无就业首付款'}
    PAY_WAYS = {1: u"网页支付宝", 2: u"移动支付宝", 3: u"移动微信支付", 4: u"微信支付", 5: u"么分期", 6: u"银联支付", 7: u'分期乐',
                8: u"易宝", 9: u"有贝分期", 10: u"WAP支付宝"}
    PAY_STATUS = {0: u"未支付", 1: u"支付成功", 2: u"支付失败"}

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户", db_index=True)
    pay_price = models.IntegerField(verbose_name=u"订单金额")
    pay_money = models.IntegerField(verbose_name=u"支付金额", null=True, blank=True)
    order_no = models.CharField(max_length=100, unique=True, verbose_name=u"订单号", db_index=True)
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    pay_type = models.SmallIntegerField(choices=PAY_TYPES.items(), default=0, verbose_name=u"支付类型", db_index=True)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name=u"下单时间")
    date_pay = models.DateTimeField(null=True, blank=True, verbose_name=u"支付时间")
    pay_way = models.SmallIntegerField(choices=PAY_WAYS.items(), verbose_name=u"支付方式", db_index=True)
    pay_status = models.SmallIntegerField(null=True, blank=True, default=0,
                                          choices=PAY_STATUS.items(), verbose_name=u"支付状态", db_index=True)
    pay_careercourse = models.ForeignKey(CareerCourse, verbose_name=u"支付订单对应职业课程", db_index=True)
    pay_class = CustomManagerForeignKey(Class, verbose_name=u"支付订单对应班级号",db_index=True, manager=Class.objects.xall)
    pay_stage = models.ManyToManyField(Stage, null=True, blank=True, verbose_name=u"支付订单对应阶段")
    coupon_code = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"优惠码")
    creditease_status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"宜信审核状态")
    creditease_msg = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"宜信审核详情")
    periodamount = models.IntegerField(verbose_name=u"每期还款金额", null=True, blank=True)
    schedules = models.TextField(null=True, blank=True, verbose_name=u"还款计划")
    nonce_str = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"随机字符串")
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name=u"手机号码")
    # 订单管理
    payment_account = models.CharField(u"收款账号", max_length=50, default=None, null=True, blank=True)
    net_price = models.IntegerField(u"官网价格", default=None, null=True)
    discounted_price = models.IntegerField(u"优惠金额", default=None, null=True)
    contract_price = models.IntegerField(u"合同价格", default=None, null=True)
    final_payment_price = models.IntegerField(u"应收款", default=None, null=True, blank=True)
    is_online_pay = models.BooleanField(u"是否是在线支付", default=True, db_index=True)


    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    @property
    def pay_way_text(self):
        return self.PAY_WAYS.get(self.pay_way)

    @property
    def pay_type_text(self):
        return self.PAY_TYPES.get(self.pay_type)


class UserPayBind(models.Model):
    user_id = models.CharField(max_length=20, null=False, blank=False, verbose_name=u"用户id")
    careercourse_id = models.CharField(max_length=20, null=False, blank=False, verbose_name=u"职业课程id")
    status = models.SmallIntegerField(u"显示状态", default=0, choices=((0, "显示"), (1, '屏蔽'),))

    class Meta:
        verbose_name = '一键支付'
        verbose_name_plural = verbose_name
        unique_together = (('user_id', 'careercourse_id'),)

    def __unicode__(self):
        return str(self.id)
