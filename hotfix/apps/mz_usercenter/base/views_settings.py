# -*- coding: utf-8 -*-

"""
@version: 2016/5/19
@author: Jackie
@contact: jackie@maiziedu.com
@file: views_settings.py
@time: 2016/5/19 10:26
@note:  ??
"""
import json
import datetime
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from core.common.http.response import success_json, failed_json
from mz_common.models import MobileVerifyRecord
from mz_user.models import ThirdPartyUser
from mz_user.interface import UserBaseInterface
from mz_user.views import random_avatar
from geetest.views import validate
from mz_user.avatar import avatar_upload as _avatar_upload
from mz_user.avatar import avatar_crop


@login_required(login_url="/")
def avatar_random(request):
    """
    随机头像
    :param request:
    :return:
    """
    url_big, url_middle, url_small = random_avatar()
    result = dict(
        big=url_big,
        middle=url_middle,
        small=url_small
    )
    UserBaseInterface(user_object=request.user).update_avatar(**result)
    return success_json({'avatar': settings.MEDIA_URL + url_big})


def avatar_upload(request):
    """
    上传头像
    :param request:
    :return:
    """
    imgfile = request.FILES.get('image')
    try:
        flag, result = _avatar_upload(imgfile)
        if flag:
            return success_json(result)
        else:
            return failed_json(result)
    except:
        return failed_json(u'上传失败,请稍后再试')


def avatar_save(request):
    """
    头像剪切保存
    :param request:
    :return:
    """
    pic_dict = dict(
        picwidth=int(request.POST.get('picwidth')),
        picheight=int(request.POST.get('picheight')),
        width=int(request.POST.get('width')),
        height=int(request.POST.get('height')),
        left=int(request.POST.get('left')),
        top=int(request.POST.get('top')),
    )
    img_url = request.POST.get('img_url')
    result = avatar_crop(img_url, **pic_dict)
    UserBaseInterface(user_object=request.user).update_avatar(**result)
    return success_json()


@login_required(login_url="/")
def bind_mobile_sendsms(request):
    """
    修改手机发送短信
    :param request:
    :return:
    """
    # 手机校验
    mobile = request.POST.get('mobile')
    if not mobile:
        return failed_json(u'请输入手机号')
    if UserBaseInterface.check_mobile_exists(mobile):
        return failed_json(u'该手机号已被注册')
    ip = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
    result = UserBaseInterface.can_send_sms(mobile, ip)
    if not result[0]:
        return failed_json(result[1])
    # 校验验证码
    if not request.POST.get('retry'):
        try:
            result = validate(request)
        except KeyError:
            return failed_json(u'验证码错误')
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return failed_json(u'验证码错误')
    # 发送短信
    UserBaseInterface.send_check_mobile(mobile, ip, mobile_type=1)
    return success_json({})


@login_required(login_url="/")
def bind_mobile(request):
    """
    修改手机号
    :param request:
    :return:
    """
    mobile = request.POST.get('mobile')
    mobile_code = request.POST.get('mobile_code')
    if not mobile_code:
        return failed_json(u'请输入验证码')
    record = MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(code=mobile_code), Q(type=1)).order_by("-created")
    if record:
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > record[0].created:
            return failed_json(u'验证码已过期')
    else:
        return failed_json(u'验证码不正确')
    UserBaseInterface(user_object=request.user).bind_mobile(mobile)
    return success_json({})


@login_required(login_url="/")
def bind_email_sendemail(request):
    """
    修改邮箱发送邮件
    :param request:
    :return:
    """
    # 邮箱校验
    email = request.POST.get('email')
    if not email:
        return failed_json(u'请输入邮箱')
    if UserBaseInterface.check_email_exists(email):
        return failed_json(u'该邮箱已被注册')
    ip = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
    result = UserBaseInterface.can_send_email(email, ip)
    if not result[0]:
        return failed_json(result[1])
    # 校验验证码
    try:
        result = validate(request)
    except KeyError:
        return failed_json(u'验证码错误')
    status = json.loads(result.content)
    if status['status'] == 'fail':
        return failed_json(u'验证码错误')
    # 发送邮件
    request.user.email = email
    request.user.username = email
    request.user.valid_email = 0
    request.user.save()
    UserBaseInterface.send_check_email(email, ip, email_type=0)
    return success_json({})


@login_required(login_url="/")
def send_email_again(request):
    """
    再次发送邮件
    :param request:
    :return:
    """
    user = request.user
    email = user.email
    if not email:
        return failed_json(u'请先绑定邮箱')
    if user.valid_email == 1:
        return failed_json(u'邮箱已验证成功')
    ip = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
    result = UserBaseInterface.can_send_email(email, ip)
    if not result[0]:
        return failed_json(result[1])
    # 发送邮件
    UserBaseInterface.send_check_email(email, ip, email_type=0)
    return success_json({})


@login_required(login_url="/")
def password_change(request):
    """
    修改密码
    :param request:
    :return:
    """
    old_password = request.POST.get('old_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')
    if not old_password:
        return failed_json(u'原密码不能为空')
    if not (new_password1 and new_password2):
        return failed_json(u'新密码不能为空')
    if new_password1 != new_password2:
        return failed_json(u'两次密码不一致')

    result = UserBaseInterface(user_object=request.user).reset_password(old_password, new_password1)
    if not result[0]:
        return failed_json(result[1])
    logout(request)
    return success_json({})


@login_required(login_url="/")
def unbind_other_site(request):
    other_site = request.GET.get('site')
    if other_site not in ('qq', 'wechat'):
        raise Http404
    # 第三方取消绑定
    UserBaseInterface(user_object=request.user).unbind_osite_account(site=other_site)
    return HttpResponseRedirect(reverse('home:settings:index'))


def bind_other_site(request):
    """no use"""
    pass
