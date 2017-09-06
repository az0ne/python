# -*- coding: utf-8 -*-

"""
WAP端的注册,登陆相关的view.
绝大部分的函数同mz_user.views内的函数相似.
建立一套独立代码(而不不是修改之前的代码)的主要原因是节省回归测试时间
正确的做法应该是采用面向对象的"修改关闭扩展开放"的原则进行代码编写

Note: 该文件依赖mz_user.views的两个函数: common_register, do_send_sms_signup. 要注意避免相互依赖

"""

import json

import urlparse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from mz_common.views import *
from models import *
from aca_course.models import *
from mz_common.captcha_functions import verify_captcha_code
from mz_user.views import common_register, do_send_sms_signup

from utils.logger import logger as log

NO_JUMP_URL_NAMES = ['find_password', 'signup']

def get_refer_url(request):
    """
    @brief 确定登陆之前的url. 该url将用于登陆之后的跳转
    :param request:
    :return:
    """
    # 将url的reverse放到全局, 会出问题.
    no_jump_urls = (reverse(item) for item in NO_JUMP_URL_NAMES)
    no_jump_urls = ('%s%s' % (settings.MOBILE_SITE.lower(), item.lower()) for item in no_jump_urls)
    refer_url = request.META.get('HTTP_REFERER')
    if not refer_url or refer_url.lower() in no_jump_urls:  # 如果在不跳转列表内, 或者无前跳引用URL, 则跳转到首页
        return settings.MOBILE_SITE
    return refer_url

@require_POST
def user_login(request):
    """
    @brief wap端登陆
    :param request:
    :return:
    """
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        #获取表单信息
        account = login_form.cleaned_data["account_l"]
        password = login_form.cleaned_data["password_l"]
        source_url = get_refer_url(request)
        #登录验证
        user = authenticate(username=account, password=password)
        if user is not None:  # 登录
            if user.is_active:  # 根据产品的逻辑, 凡是绑定手机号的账号, 应该都是激活的账号, 此处编码仅仅是为了逻辑完备.
                login(request, user)
                if user.is_student():
                    url_parse = urlparse.urlparse(source_url)
                    if not url_parse[2] or url_parse[2] == '/':
                        source_url = '/home/base/'
                return HttpResponse(json.dumps(dict(status='success', url=source_url)), content_type="application/json")
            else:
                return HttpResponse(json.dumps(dict(status='failure', msg='账号未激活')), content_type="application/json")
        return HttpResponse(json.dumps(dict(status='failure', msg='账号或者密码错误，请重新输入')), content_type="application/json")
    return HttpResponse(json.dumps(login_form.errors), content_type="application/json")

@require_POST
def verify_random_code(request):
    """
    @brief 验证注册的随机验证码和手机号
    :param request:
    :return:
    @note 该函数用于手机注册的第一步: 验证用户手机号和随机验证码.
          如果手机号合法,并且随机验证码正确, 则设置session.
    """

    register_form = WapMobileRegisterForm(request.POST)

    if register_form.is_valid():  # 手机号合法, 验证随机验证码

        hash_key = request.POST.get('hash_key')
        code = request.POST.get('code')

        if hash_key and code:
            try:
                result = verify_captcha_code(request, hash_key, code)
            except Exception as e:
                log.warn('verify_random_code fail: %s, more info hash_key: %s, code: %s' % (str(e), hash_key, code))
                return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")

            if result:  # 验证成功, 设置session
                request.session['captcha_status'] = '1'
                return HttpResponse(json.dumps(dict(status='success')), content_type="application/json")

        else:  # 参数不够
            return HttpResponse(json.dumps(dict(captcha='验证码参数不足')), content_type="application/json")

        return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")

    return HttpResponse(json.dumps(register_form.errors), content_type="application/json")

@require_POST
def wap_mobile_register(request):
    """
    @brief 手机注册账号表单
    :param request:
    :return:
    """
    register_form = WapMobileRegisterForm(request.POST)

    if register_form.is_valid():

        # 验证码验证
        if not request.session.get('captcha_status'):  # 前置步骤正确的情况下, 这里的代码应该不会到达
            hash_key = request.POST.get('hash_key')
            code = request.POST.get('code')
            if hash_key and code:
                try:
                    result = verify_captcha_code(request, hash_key, code)
                except Exception as e:
                    log.warn('wap_mobile_register fail: %s, more info hash_key: %s, code: %s' % (str(e), hash_key, code))
                    return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")
                if not result:
                    return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")
            else:  # 参数不够
                return HttpResponse(json.dumps(dict(captcha='验证码参数不足')), content_type="application/json")

        #获取表单信息
        password = register_form.cleaned_data.get('password_m')
        mobile = register_form.cleaned_data.get('mobile')
        source = '新网站'
        source_url = get_refer_url(request)  # 此处需要处理引用URL.考虑一种变态的场景:用户从找回密码页面点开登陆框,然后点击注册

        try:
            common_register(request, mobile, password, source)
        except Exception as e:
            log.warn('wap_mobile_register fail %s, more info: mobile: %s, password %s' % (str(e), mobile, password))
            return HttpResponse(json.dumps(dict(status='failure', msg='注册失败')), content_type="application/json")

        # 同步登录
        user = authenticate(username=mobile, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps(dict(status='success', source_url=source_url)), content_type="application/json")
    return HttpResponse(json.dumps(register_form.errors), content_type="application/json")

@require_POST
def password_send_sms_code(request):
    """
    @brief 找回密码时, 验证随机验证码是否正确, 如果正确, 则发送验证码
    :param request:
    :return:
    """

    find_password_form = WapFindPasswordForm(request.POST)

    if find_password_form.is_valid():

        hash_key = request.POST.get('hash_key')
        code = request.POST.get('code')

        if hash_key and code:
            try:
                result = verify_captcha_code(request, hash_key, code)
            except Exception as e:
                log.warn('password_send_sms_code fail: %s, more info hash_key: %s, code: %s' % (str(e), hash_key, code))
                return HttpResponse('{"captcha": "请输入正确的验证码"}', content_type="application/json")
            if not result:
                return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")
        else:  # 参数不够
            return HttpResponse(json.dumps(dict(captcha='验证码参数不足')), content_type="application/json")

        request.session['captcha_status'] = '1'

        #获取表单信息
        account = find_password_form.cleaned_data.get("account")

        #手机则发送短信并进入短信验证界面
        try:
            result = do_send_sms_signup(account, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], 1)
        except Exception as e:
            log.warn('verify_random_code: do_send_sms_signup: fail: %s, more info hash_key: %s, code: %s' %
                     (str(e), hash_key, code))
            return HttpResponse(json.dumps(dict(status='failure', account='发送手机验证码失败, 请稍后再试')),
                                content_type="application/json")
        return HttpResponse(result, content_type="application/json")

    return HttpResponse(json.dumps(find_password_form.errors), content_type="application/json")

@require_POST
def reset_password(request):
    """
    @brief 重设密码
    :param request:
    :return:
    @note: 步骤:
                 1. 验证手机号是否合法
                 2. 验证随机验证码是否合法, 此处再次验证是否有必要?
                 3. 验证手机号+手机验证码组合是否合法
                 4. 验证新密码是否合法
                 5. 修改密码
    """
    # 验证手机号是否合法
    find_password_form = WapFindPasswordForm(request.POST)
    if not find_password_form.is_valid():
        return HttpResponse(json.dumps(find_password_form.errors), content_type="application/json")

    # 验证随机验证码是否合法
    if not request.session.get('captcha_status'):

        hash_key = request.POST.get('hash_key')
        code = request.POST.get('code')

        if hash_key and code:
            try:
                result = verify_captcha_code(request, hash_key, code)
            except Exception as e:
                log.warn('reset_password fail: %s, more info hash_key: %s, code: %s' % (str(e), hash_key, code))
                return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")
            if not result:
                return HttpResponse(json.dumps(dict(captcha='请输入正确的验证码')), content_type="application/json")
        else:  # 参数不够
            return HttpResponse(json.dumps(dict(captcha='验证码参数不足')), content_type="application/json")

    # 验证手机号码+手机验证码是否合法
    find_password_mobile_form = WapFindPasswordMobileForm(request.POST)
    if not find_password_mobile_form.is_valid():
        return HttpResponse(json.dumps(find_password_mobile_form.errors), content_type="application/json")

    # 验证密码是否合法
    password = request.POST.get('password_m')
    if len(password.replace(' ', '')) < 8 or len(password.replace(' ', '')) > 20:
        return HttpResponse(json.dumps(dict(password_m='请输入正确的密码')), content_type="application/json")

    # 重置密码
    password = make_password(password)
    account = find_password_mobile_form.cleaned_data.get("mobile_f")
    try:
        user = UserProfile.objects.get(Q(mobile=account))
        user.password = password
        user.save()
        return HttpResponse('{"status":"success"}', content_type="application/json")
    except UserProfile.DoesNotExist:
        log.warn('reset_password: reset password: Fail. More info mobile %s' % account)
        return HttpResponse('{"status":"failure"}', content_type="application/json")
