# -*- coding: utf-8 -*-

"""
@version: 2016/5/18
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/5/18 11:31
@note:  ??
"""
import datetime
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db.models import Q

from core.common.cache.decorators import cache_data
from mz_user.models import UserProfile, ProvinceDict, CityDict, ThirdPartyUser, ProfessionalSkill
from mz_common.models import EmailVerifyRecord, MobileVerifyRecord
from core.common.utils import validators
from mz_user.views import do_send_email_async
from utils.sms_manager import tpl_send_sms


class SendingDenied(Exception):
    pass


class UserBaseInterface(object):
    def __init__(self, user_id=None, user_object=None):
        self._user_id = user_id
        self._user_object = user_object

    @cached_property
    def user_id(self):
        return self._user_id or self.user.id

    @cached_property
    def user(self):
        self._user_object = self._user_object or get_object_or_404(UserProfile, id=self.user_id)
        self.user_id = self._user_object.id
        return self._user_object

    @classmethod
    def check_email_exists(cls, email):
        return UserProfile.objects.filter(email=email).exists()

    @classmethod
    def check_mobile_exists(cls, mobile):
        return UserProfile.objects.filter(mobile=mobile).exists()

    @classmethod
    def can_send_email(cls, email, ip):
        try:
            # 邮箱格式校验
            validators.v_email(email)
        except validators.VerifyError as e:
            return False, e.message
        # 邮箱发送限制校验
        start = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        one_min_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        send_count = EmailVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=start)).count()
        if EmailVerifyRecord.objects.filter(Q(email=email), Q(created__gt=one_min_ago)).exists():
            return False, u"当前邮箱距离上一次发送邮件未超过60s"
        if send_count > settings.EMAIL_COUNT:
            return False, u"当前ip超过发送次数"
        return True, ''

    @classmethod
    def can_send_sms(cls, mobile, ip):
        """
        电话号码校验
        :param mobile:
        :param ip:
        :return: True or False
        """
        try:
            # 手机格式校验
            validators.v_mobile(mobile)
        except validators.VerifyError as e:
            return False, e.message
        # 手机发送限制校验
        start = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        if MobileVerifyRecord.objects.filter(created__gt=start, mobile=mobile).count() >= settings.SMS_MAX_COUNT_MOBILE:
            return False, u"该手机号超过当日短信发送限制数量"

        if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=start)).count() >= settings.SMS_COUNT:
            return False, u"该IP超过当日短信发送限制数量"

        one_min_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=one_min_ago)).exists():
            return False, u"当前ip距离上一次发送验证码未超过60s"
        if MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(created__gt=one_min_ago)).exists():
            return False, u"当前手机号距离上一次发送验证码未超过60s"
        return True, ''

    def update_profile(self, **kwargs):
        """
        更新用户信息
        :param kwargs:
        :return:
        """
        user = self.user
        try:
            if not kwargs.get('nick_name'):
                raise Exception(u'请填写昵称')
            if user.is_student():
                validators.v_nick(kwargs.get('nick_name'), min_len=1, max_len=11)
            if UserProfile.objects.filter(nick_name=kwargs.get('nick_name')).exclude(id=user.id).exists():
                raise Exception(u'昵称已存在')
            if not kwargs.get('real_name'):
                raise Exception(u'请填写真实姓名')
            validators.v_len(kwargs.get('real_name'), min_l=2, max_l=5, name=u'真实姓名')
            if not kwargs.get('qq'):
                raise Exception(u'请填写qq')
            if not kwargs.get('wechat'):
                raise Exception(u'请填写微信号')
            if user.is_teacher():
                if not kwargs.get('teach_feature'):
                    raise Exception(u'请填写教学特点')
                if not kwargs.get('description'):
                    raise Exception(u'请填写个人简介')
            elif user.is_student():
                if not kwargs.get('birthday'):
                    raise Exception(u'请填写生日')
                if not kwargs.get('address'):
                    raise Exception(u'请填写地址')
        except Exception, e:
            return False, e.message
        for k, v in kwargs.iteritems():
            if v is None:
                continue
            setattr(user, k, v)
        user.save()
        return True, ''

    def update_avatar(self, **kwargs):
        """
        更新用户头像
        :param kwargs:
        :return:
        """
        user = self.user

        user.avatar_url = kwargs.pop('big')
        user.avatar_middle_thumbnall = kwargs.pop('middle')
        user.avatar_small_thumbnall = kwargs.pop('small')

        user.save(update_fields=['avatar_url', 'avatar_middle_thumbnall', 'avatar_small_thumbnall'])

    def reset_password(self, old, new):
        """
        重设密码
        :param old:
        :param new:
        :return:
        """
        user = self.user
        if not user.check_password(old):
            return False, u'原密码错误'
        try:
            validators.v_len(new, 8, 50, name=u'密码')
            validators.v_password(new)
        except validators.VerifyError as e:
            return False, e.message
        user.set_password(new)
        user.save(update_fields=["password"])
        return True, u'密码修改成功'

    def bind_email(self, email):
        """
        绑定邮箱
        :param email:
        """
        user = self.user
        assert isinstance(user, UserProfile)
        user.email = email
        user.username = email
        user.valid_email = 0
        user.save(update_fields=['email', 'username', 'valid_email'])

    def bind_mobile(self, mobile):
        """
        绑定手机
        :param mobile:
        :return:
        """
        user = self.user
        assert isinstance(user, UserProfile)
        user.mobile = mobile
        user.username = mobile
        user.valid_mobile = 1
        user.save(update_fields=['mobile', 'username', 'valid_mobile'])

    def get_osite_accounts(self):
        """获取第三方绑定的账号"""
        user = self.user
        data = {'qq': {}, 'wechat': {}}
        for third in ThirdPartyUser.objects.filter(user=user):
            third_dict = dict(
                openid=third.openid,
                nick_name=third.nickname,
                user_id=third.user_id,
                token=third.token,
                id=third.id
            )
            if third.partner == 'qq':
                data['qq'] = third_dict
            if third.partner == 'wechat':
                data['wechat'] = third_dict
        return data

    def unbind_osite_account(self, site):
        ThirdPartyUser.objects.filter(partner=site, user_id=self.user_id).delete()

    @staticmethod
    def send_check_email(email, ip, email_type):
        """
        发送邮件
        :param email:
        :param ip:
        :param email_type: 0，注册   1，忘记密码
        :return: True
        """
        random_str = get_random_string(length=10)
        # 邮件发送记录写入数据库
        email_record = EmailVerifyRecord()
        email_record.code = random_str
        email_record.email = email
        email_record.type = email_type
        email_record.ip = ip
        email_record.save()

        # 发送验证邮件
        do_send_email_async.delay(email, random_str, email_type)

    @staticmethod
    def send_check_mobile(mobile, ip, mobile_type):
        """
        发送验证码短信
        :param mobile:
        :param ip:
        :param mobile_type: 0，注册   1，忘记密码
        :return: True or False
        """
        # 生成激活码
        random_str = get_random_string(length=6, allowed_chars='0123456789')
        # 邮件发送记录写入数据库
        mobile_record = MobileVerifyRecord()
        mobile_record.code = random_str
        mobile_record.mobile = mobile
        mobile_record.type = mobile_type
        mobile_record.ip = ip
        mobile_record.source = 1
        mobile_record.save()
        # 发送短信
        tpl_send_sms.delay(
            settings.SMS_APIKEY, settings.SMS_TPL_ID, random_str, mobile)


class CommonDataInterface:
    @staticmethod
    @cache_data(60 * 60)
    def get_provinces():
        return [[province.id, province.name] for province in ProvinceDict.objects.all()]

    @staticmethod
    @cache_data(60 * 60)
    def get_cities_by_province_id(province_id, cache_pk=None):
        cities = CityDict.objects.filter(province=province_id)
        city_list = [{'city_id': city.id, 'city_name': city.name} for city in cities]
        return city_list

    @staticmethod
    @cache_data(60 * 60)
    def get_pro_skills():
        ret = dict()
        objs = ProfessionalSkill.objects.all()
        for obj in objs:
            ret.setdefault(obj.domain, [])
            ret[obj.domain].append(dict(id=obj.id, skill=obj.skill))
        return ret

    @classmethod
    def get_pro_skills_by_domain(cls, domain):
        return cls.get_pro_skills().get(domain, [])
