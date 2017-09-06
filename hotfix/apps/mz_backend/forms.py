# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.db.models.query_utils import Q

from mz_lps.models import Class, ClassStudents
from mz_pay.models import UserPurchase
from mz_user.models import UserProfile
from utils.tool import generation_order_no


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "username"}), label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput(attrs={"class": "pwd"}))


class OrderForm(forms.Form):
    error_messages = {
        "student_error": u"未找到该用户，请检查麦子账号。",
        "cls_error": u"未找到该班级，请确保录入的是一个lps3.0的正常付费班级",
        "date_error": u"请检查时间格式",
        "trade_no": u"交易流水号在已有订单中有重复，请重新给定"
    }

    PAY_WAYS = {1: u"网页支付宝", 2: u"移动支付宝", 6: u"银联支付"}

    student = forms.CharField(label=u"麦子账号")
    cls = forms.CharField(label=u"班级编号或名称")
    pay_type = forms.IntegerField(label=u"支付类型")
    pay_way = forms.IntegerField(label=u"收款平台")
    payment_account = forms.CharField(label=u"收款账号", max_length=50)
    trade_no = forms.CharField(label=u"交易流水号", max_length=100)
    date_pay = forms.CharField(label=u"支付时间")

    def clean_student(self):
        student = self.cleaned_data["student"]
        try:
            student = UserProfile.objects.get(
                Q(email=student) | Q(mobile=student))
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['student_error'],
                code=u'麦子账号')
        return student

    def clean_trade_no(self):
        trade_no = self.cleaned_data["trade_no"]
        try:
            UserPurchase.objects.get(trade_no=trade_no)
            raise forms.ValidationError(
                self.error_messages['trade_no'],
                code=u'交易流水号')
        except UserPurchase.DoesNotExist:
            return trade_no

    def clean_cls(self):
        cls = self.cleaned_data["cls"]
        cls = Class.objects.xall().filter(
            Q(coding=cls) | Q(name=cls), lps_version='3.0',
            class_type=Class.CLASS_TYPE_NORMAL).first()
        if not cls:
            raise forms.ValidationError(
                self.error_messages['cls_error'],
                code=u"班级编号或名称")
        return cls

    @staticmethod
    def get_cls(coding_name):
        cls = Class.objects.xall().filter(
            Q(coding=coding_name) | Q(name=coding_name), lps_version='3.0',
            class_type=Class.CLASS_TYPE_NORMAL).first()
        return cls

    def clean_date_pay(self):
        date_pay = self.cleaned_data["date_pay"].replace('T', ' ')
        try:
            date_pay = datetime.strptime(date_pay, "%Y-%m-%d %H:%M")
        except ValueError:
            raise forms.ValidationError(
                    self.error_messages['date_error'],
                    code=u"支付时间")
        return date_pay

    def save(self, is_commit=True):
        c_course = self.cleaned_data["cls"].career_course
        order_no = generation_order_no()
        order = UserPurchase(
            **dict(user=self.cleaned_data["student"],
                   order_no=order_no,
                   pay_class=self.cleaned_data["cls"],
                   pay_type=self.cleaned_data["pay_type"],
                   pay_way=self.cleaned_data["pay_way"],
                   payment_account=self.cleaned_data["payment_account"],
                   trade_no=self.cleaned_data["trade_no"],
                   date_pay=self.cleaned_data["date_pay"],
                   pay_careercourse=c_course,
                   pay_status=1,
                   net_price=c_course.net_price,
                   discounted_price=c_course.discounted_price,
                   contract_price=c_course.contract_price,
                   is_online_pay=False)
        )
        self.check_logic()
        if order.pay_type == 0:     # 全款
            order.pay_price = c_course.net_price-c_course.discounted_price
            order.pay_money = order.pay_price
        elif order.pay_type == 6:   # 无就业全款
            order.pay_price = c_course.jobless_price
            order.pay_money = order.pay_price
        elif order.pay_type == 1:   # 试学
            order.pay_price = c_course.try_price
            order.pay_money = order.pay_price
            order.final_payment_price = order.contract_price-c_course.try_price
        else:   # 余款
            try_order = self.get_try_order()
            order.pay_price = try_order.final_payment_price
            order.pay_money = order.pay_price
        if is_commit:
            order.save()
            return order
        return order

    def _get_order(self, pay_type):
        order = UserPurchase.objects.filter(
            user=self.cleaned_data["student"],
            pay_class=self.cleaned_data["cls"],
            pay_type=pay_type, pay_status=1).first()
        return order

    def get_try_order(self):    # 获取试学订单
        try_order = self._get_order(pay_type=1)
        # assert try_order, 'not find try learning pay order'
        assert try_order, u'未找到试学记录，不允许录入余款订单'
        return try_order

    def is_try_order(self):     # 学员是否有试学订单
        try:
            self.get_try_order()
            return True
        except AssertionError:
            return False

    def is_quit_class(self):    # 学员是否已退学
        cs = ClassStudents.objects.filter(
            user=self.cleaned_data["student"],
            student_class=self.cleaned_data["cls"]).first()
        assert cs, u'该学员不在该班级内'
        return True if cs.status == ClassStudents.STATUS_QUIT else False

    def is_full_order(self):    # 学员是否有全款订单
        full_order = self._get_order(pay_type=0)
        return True if full_order else False

    def is_final_order(self):    # 学员是否有尾款订单
        full_order = self._get_order(pay_type=2)
        return True if full_order else False

    def check_logic(self):
        pay_type = self.cleaned_data["pay_type"]
        if self.is_try_order():
            if pay_type == 0:
                raise AssertionError(
                    u"学员在该班级已有试学订单，请录入余款而不是全款")
            elif pay_type == 1:
                raise AssertionError(
                    u"学员在该班级已有试学订单，不允许再次录入")
        if self.is_full_order():
            raise AssertionError(
                u"学员在该班级已有全款订单，不允许录入")
        if pay_type == 2:
            if self.is_quit_class():
                raise AssertionError(
                    u"学员在该班级已退学，不允许录入余款")
            if self.is_final_order():
                raise AssertionError(
                    u"学员在该班级已有尾款订单，不允许录入")
