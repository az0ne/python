# -*- coding: utf-8 -*-

"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/3/29 15:23
@note:  ??
"""
import re
import logging
from datetime import datetime, timedelta
from interface import avatar_crop, send_sms, get_user_type
from core.common.http.response import success_json, failed_json
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.db.models import Q
from mz_course.models import Course, Lesson
from mz_user.views import _upload, common_register
from mz_user.models import UserProfile, ThirdPartyUser, MyFavorite, StudyGoal, StudyBase, AppSendMessageNum
from mz_common.models import MobileVerifyRecord, Feedback, AndroidVersion, MyMessage
from django.contrib.auth.hashers import make_password
from .decorators import app_user_required
from website.api.course.interface import strip_tags, filter_emoji
import db.api.common.app
from mz_usercenter.base.views_settings import bind_mobile_sendsms, bind_mobile


logger = logging.getLogger('mz_user.views')


# 登陆
def app_user_login(request):
    user_account = request.POST.get('account', None)
    user_password = request.POST.get('password', None)
    if not user_account:
        return failed_json(u"账号不能为空")
    if not user_password:
        return failed_json(u"密码不能为空")
    p = re.compile(settings.REGEX_EMAIL+"|"+settings.REGEX_MOBILE)
    if not p.match(user_account):
        return failed_json(u"账号格式不对")
    try:
        user = UserProfile.objects.get(Q(email=user_account) | Q(mobile=user_account))
        if user.is_disabled:
            return failed_json(u"账号被禁用")
    except UserProfile.DoesNotExist:
        return failed_json(u"账号不存在")
    user = authenticate(username=user_account, password=user_password)
    if user:
        if user.is_active:
            login(request, user)
            partner = request.POST.get('partner')
            openid = request.POST.get('openid')
            if partner and openid:    # 第三方绑定
                bool_result, result = third_bind(user, partner, openid)
                if not bool_result:
                    return failed_json(result)
            return success_json(get_user_info(user, is_self=request.session.session_key))
        return failed_json(u"账号未激活")
    return failed_json(u"账号或密码错误")


# 登出
def app_user_logout(request):
    logout(request)
    return success_json({})


# 是否绑定第三方
def third_check(request):
    partner = request.POST.get('partner')
    openid = request.POST.get('openid')
    token = request.POST.get('token')
    nickname = request.POST.get('nickname')
    if partner and openid and token:
        params = dict(partner=partner, openid=openid)
        third_party_user, created = ThirdPartyUser.objects.get_or_create(**params)
        third_party_user.token = token
        third_party_user.nickname = nickname
        third_party_user.save()
        if third_party_user.user:
            if third_party_user.user.is_active:
                third_party_user.user.backend = 'mz_user.auth.CustomBackend'
                login(request, third_party_user.user)
                user_data = get_user_info(third_party_user.user, is_self=request.session.session_key)
                return success_json({'isBind': 1, 'accountInfo': user_data})
        return success_json({'isBind': 0, 'accountInfo': {}})
    return failed_json(u'校验失败')


# 第三方绑定
def third_bind(user, partner, openid):
    try:
        thirdpartyuser = ThirdPartyUser.objects.get(partner=partner, openid=openid)
        if (not thirdpartyuser.user) and (not ThirdPartyUser.objects.filter(partner=partner, user=user)):
            thirdpartyuser.user = user
            thirdpartyuser.save()
            return True, ''
        return False, u'当前麦子账号已绑定第三方账号'
    except ThirdPartyUser.DoesNotExist:
        return True, ''


# 获取用户信息
def get_user_info(user, is_self=None):
    user_dict = dict(
            user_id=user.id,
            nick_name=user.nick_name,
            school=user.graduate_institution,
            gender=UserProfile.GENDERS[user.gender] if user.gender else None,
            degree=UserProfile.DEGREES[user.degree] if user.degree else None,
            birthday=user.birthday,
            type=get_user_type(user),
            avatar=settings.SITE_URL + settings.MEDIA_URL + str(user.avatar_small_thumbnall),
            real_name=user.real_name,
    )
    if is_self:
        result = db.api.common.app.app_last_career_course(user_id=user.id)
        if result.is_error():
            career_course_id = None
        else:
            user_career = result.result()
            career_course_id = user_career if user_career else None
        mobile = user.mobile if user.valid_mobile == 1 and user.mobile else ''
        user_self_dict = dict(
            token=is_self,
            qq=user.qq,
            in_service='在职' if user.in_service == 1 else '不在职',
            work_city=user.intention_job_city,
            service_year=UserProfile.SERVICE_YEAR_CHOICES[user.service_year] if user.service_year else None,
            study_goal=user.study_goal,
            study_base=user.study_base,
            current_ccourse_id=career_course_id['career_course_id'] if career_course_id else None,
            mobile=mobile,
            account=user.username
        )
        user_dict.update(user_self_dict)
    for k, v in user_dict.iteritems():
        if v is None:
            user_dict[k] = ''
    return user_dict


# app手机号校验发送短信
def app_mobile_register_sms(request):
    mobile = request.POST.get('account', None)
    send_type = int(request.POST.get('type', 0))  # 0注册 1找回密码
    if send_type not in [0, 1]:
        return failed_json(u"type类型错误")
    if not mobile:
        return failed_json(u"账号为空")
    p = re.compile(settings.REGEX_MOBILE)
    if not p.match(mobile):
        return failed_json(u"手机格式不正确")

    if UserProfile.objects.filter(mobile=mobile).exists():
        if send_type == 0:
            # 检验该手机号是否注册
            return failed_json(u"该账号已被注册")
    else:
        if send_type == 1:
            return failed_json(u'该账号未注册')
    result = send_sms(mobile, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'], send_type=send_type)
    if result[0]:
        return success_json({})
    else:
        return failed_json(result[1])


# app手机号注册
def app_mobile_register(request):
    account = request.POST.get('account', None)
    password = request.POST.get('password', None)
    code = request.POST.get('mobile_code', None)
    if not account:
        return failed_json(u"账号不能为空")
    p = re.compile(settings.REGEX_MOBILE)
    if not p.match(account):
        return failed_json(u"手机格式不正确")
    if UserProfile.objects.filter(mobile=account).exists():
        return failed_json(u"该账号已被注册")
    if not password:
        return failed_json(u"密码不能为空")
    if len(password.replace(' ', '')) < 8:
        return failed_json(u"密码小于八位")
    if len(password.replace(' ', '')) > 50:
        return failed_json(u"密码长度需小于50位")
    if not code:
        return failed_json(u"验证码不能为空")
    record = MobileVerifyRecord.objects.filter(Q(mobile=account), Q(code=code), Q(type=0)).order_by("-created")
    if record:
        if datetime.now()-timedelta(minutes=30) > record[0].created:
            return failed_json(u"验证码已过期，请重新获取")
    else:
        return failed_json(u"验证码不匹配")
    user = common_register(request, account, password, 'APP')
    # 如果是第三方手机注册
    partner = request.POST.get('partner')
    openid = request.POST.get('openid')
    if partner and openid:  # 第三方绑定
        third_bind(user, partner, openid)
    user = authenticate(username=account, password=password)
    if user:
        login(request, user)
        return success_json(get_user_info(user, is_self=request.session.session_key))


# app找回密码
def app_find_password(request):
    account = request.POST.get('account', None)
    password = request.POST.get('password', None)
    code = request.POST.get('mobile_code', None)
    if not account:
        return failed_json(u"账号不能为空")
    p = re.compile(settings.REGEX_MOBILE)
    if not p.match(account):
        return failed_json(u"手机格式不正确")
    if not password:
        return failed_json(u"密码不能为空")
    if len(password.replace(' ', '')) < 8:
        return failed_json(u"密码小于八位")
    if len(password.replace(' ', '')) > 50:
        return failed_json(u"密码长度需小于50位")
    if not code:
        return failed_json(u"验证码不能为空")
    record = MobileVerifyRecord.objects.filter(Q(mobile=account), Q(code=code), Q(type=1)).order_by("-created")
    if record:
        if datetime.now()-timedelta(minutes=30) > record[0].created:
            return failed_json(u"验证码已过期，请重新获取")
    else:
        return failed_json(u"验证码不匹配")
    try:
        user = UserProfile.objects.get(mobile=account)
    except UserProfile.DoesNotExist:
        raise failed_json(u"该账号不存在，请重试")
    user.password = make_password(password)
    user.save()
    return success_json({})


# 用户信息选项
def app_user_info_choices(request):
    # 性别
    genders_choices = [dict(id=x[0], name=x[1]) for x in UserProfile.GENDERS.iteritems()]
    # 学历
    degree_choices = [dict(id=x[0], name=x[1]) for x in UserProfile.DEGREES.iteritems()]
    # 工作年限
    service_year = [dict(id=x[0], name=x[1]) for x in UserProfile.SERVICE_YEAR_CHOICES.iteritems()]
    # 是否在职
    is_work = [dict(id=x[0], name=x[1]) for x in UserProfile.IS_SERVICE_CHOICES.iteritems()]
    # 个人目标
    studygoals_choices = [dict(id=study.id, name=study.name) for study in StudyGoal.objects.all() if study.name != '其他']
    # 个人基础
    studybase_choices = [dict(id=study.id, name=study.name) for study in StudyBase.objects.all() if study.name != '其他']
    return success_json({'gender': genders_choices, 'degree': degree_choices, 'service_year': service_year,
                         'is_work': is_work, 'studygoals': studygoals_choices, 'studybases': studybase_choices})


# 提交用户信息
@app_user_required
def app_submit_user_info(request):
    # 基本信息
    nick_name = request.POST.get('nick_name', None)
    school = request.POST.get('school', None)
    gender = request.POST.get('gender', None)
    degree = request.POST.get('degree', None)
    birthday = request.POST.get('birthday', None)
    # 详细信息
    real_name = request.POST.get('real_name', None)
    qq = request.POST.get('qq', None)
    in_service = request.POST.get('in_service', None)
    intention_job_city = request.POST.get('work_city', None)
    service_year = request.POST.get('service_year', None)
    study_goal = request.POST.get('study_goal', None)
    study_base = request.POST.get('study_base', None)

    user = request.user
    if nick_name:
        if UserProfile.objects.filter(nick_name=nick_name).exists():
            return failed_json(u'昵称已存在')
        user.nick_name = nick_name
    if school:
        user.graduate_institution = school
    if gender:
        user.gender = gender
    if degree:
        user.degree = degree
    if birthday:
        user.birthday = birthday
    if real_name:
        user.real_name = real_name
    if qq:
        user.qq = qq
    if in_service:
        user.in_service = in_service
    if intention_job_city:
        user.intention_job_city = intention_job_city
    if service_year:
        user.service_year = service_year
    if study_goal:
        user.study_goal = StudyGoal.objects.get(index=study_goal).name
        user.study_goal_opt = StudyGoal.objects.get(index=study_goal)
    if study_base:
        user.study_base = StudyBase.objects.get(index=study_base).name
        user.study_base_opt = StudyBase.objects.get(index=study_base)
    try:
        user.save()
        return success_json({})
    except Exception as e:
        logger.error(e)
        return failed_json(u'修改失败')


# 上传头像
@app_user_required
def app_upload_avatar(request):
    img_file = request.FILES.get('avatar', None)
    result = _upload(img_file)
    if not result[0]:
        return failed_json(result[1])
    avatar_crop_result = avatar_crop(request, result[1], result[2], result[3])
    if not avatar_crop_result[0]:
        return failed_json(u'头像上传失败')
    return success_json({'avatar': avatar_crop_result[1]})


# 是否关注
# @app_user_required
# def app_is_follow(request):
#     user = request.user
#     target_id = request.POST.get('target_id', None)
#     if not target_id:
#         return failed_json(u'目标ID不能为空')
#     data = 0
#     if UserNetwork.objects.using('fps').filter(userA=user.id, userB=int(target_id)).exists():
#         data = 1
#     return success_json({'is_follow': data})


# 关注
# @app_user_required
# def app_follow(request):
#     user = request.user
#     target_id = request.POST.get('target_id', None)
#     if not target_id:
#         return failed_json(u'目标ID不能为空')
#     if UserNetwork.objects.using('fps').filter(userA=user.id, userB=int(target_id)).exists():
#         return failed_json(u'已关注')
#     UserNetwork.objects.using('fps').create(userA=user.id, userB=int(target_id))
#     return success_json({})


# 获取用户信息
@app_user_required
def app_get_user_info(request):
    target_id = request.POST.get('target_id', None)
    if not target_id:
        return failed_json(u'目标ID不能为空')
    try:
        target_user = UserProfile.objects.get(id=int(target_id))
    except UserProfile.DoesNotExist:
        return failed_json(u'用户不存在')
    data = get_user_info(target_user, is_self=None)
    return success_json(data)


# 获取反馈类型
def app_feedback_types(request):
    data_list = []
    for key, name in Feedback.feed_types:
        if key != 0:
            data_list.append(dict(
                feedback_id=key,
                feedback_name=name
            ))
    return success_json({'list': data_list})


# 意见反馈
@app_user_required
def app_submit_feedback(request):
    fb_type = request.POST.get('feedback_type', None)
    content = request.POST.get('content', None)
    if not content:
        return failed_json(u'反馈内容不能为空')
    feed_back = Feedback()
    if fb_type:
        feed_back.feed_type = fb_type
    feed_back.user_id = request.user.id
    feed_back.content = filter_emoji(content)
    feed_back.save()
    return success_json({})


# 联系人列表
# @app_user_required
# def app_get_contact(request):
#     user = request.user
#
#     def get_user_avatar_name(user_id):
#         try:
#             target_user = UserProfile.objects.get(id=user_id)
#             return dict(
#                 user_id=target_user.id,
#                 nick_name=target_user.nick_name,
#                 avatar=settings.SITE_URL + settings.MEDIA_URL + str(target_user.avatar_small_thumbnall)
#             )
#         except UserProfile.DoesNotExist:
#             pass
#
#     friend_list = []
#     usernets = UserNetwork.objects.using('fps').filter(userA=user.id).order_by('-join_datatime')
#     for usernet in usernets:
#         if UserNetwork.objects.using('fps').filter(userA=usernet.userB, userB=user.id):
#             friend_list.append(get_user_avatar_name(usernet.userB))
#
#     # 关注
#     follows = UserNetwork.objects.using('fps').filter(userA=user.id).order_by('-join_datatime')
#     follow_list = [get_user_avatar_name(follow.userB) for follow in follows]
#
#     # 粉丝
#     fans = UserNetwork.objects.using('fps').filter(userB=user.id).order_by('-join_datatime')
#     fans_list = [get_user_avatar_name(fan.userA) for fan in fans]
#
#     return success_json({'friend_list': friend_list, 'follow_list': follow_list, 'fans_list': fans_list})


# 我的收藏
@app_user_required
def app_my_collection(request):
    user = request.user
    return success_json(
        {"list": [
            {
                "course_id": str(favorite.course.id),
                "name": str(favorite.course.name),
                "img_url": settings.SITE_URL + settings.MEDIA_URL + str(favorite.course.image)
            } for favorite in MyFavorite.objects.filter(user=user).order_by("-date_favorite")]}
    )


# 删除收藏
@app_user_required
def app_del_collection(request):
    user = request.user
    course_ids = request.POST.get('courseIds', None)
    lesson_id = request.POST.get('lesson_id', None)
    if not course_ids:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            course_ids = [lesson.course_id]
        except Lesson.DoesNotExist:
            return failed_json(u'找不到相关课程')
    else:
        course_ids = course_ids.split(',')
    for course_id in course_ids:
        try:
            course = Course.objects.get(pk=course_id)
            favorite = MyFavorite.objects.get(user=user, course=course_id)
            favorite.delete()
            course.favorite_count -= 1
            course.save()
        except Course.DoesNotExist:
            return failed_json(u'找不到相关课程')
        except MyFavorite.DoesNotExist:
            pass
    return success_json({})


# 检查更新
def check_update(request):
    current_version = request.POST.get('currVno', None)  # 安卓版本号
    client = request.POST.get('client')
    ios_version = request.POST.get('vno')               # ios版本号
    # 是否有新版本
    has_new_version = False

    if client == 'ios':
        import db.api.common.app
        result = db.api.common.app.ios_version(_enable_cache=True)
        if result.is_error():
            return failed_json(u'已经是最新版本')
        version_list = result.result()
        if version_list:
            if not version_list[0]['is_check']:
                if int(ios_version) < int(version_list[0]['vno']):
                    return success_json({'new_version': {
                        "vno": version_list[0]['vno'],
                        "desc": version_list[0]['desc'],
                        "is_force": version_list[0]['is_force'],
                        }})
            if len(version_list) == 2:
                if int(ios_version) < int(version_list[1]['vno']):
                    return success_json({'new_version': {
                        "vno": version_list[1]['vno'],
                        "desc": version_list[1]['desc'],
                        "is_force": version_list[1]['is_force'],
                        }})
        return failed_json(u'已经是最新版本')

    # 安卓版本校验开始
    if current_version is None:
        return failed_json(u'当前版本号不能为空')
    # 最新版本号
    version_list = AndroidVersion.objects.using('default').filter(type=AndroidVersion.TYPE_STUDENT).order_by("-id")
    if version_list[0]:
        if current_version != version_list[0].vno:
            current_version_list = current_version.split(".")  # 当前版本号列表
            if len(current_version_list) != 3:
                return failed_json(u'当前版本号格式不正确')
            new_version_list = version_list[0].vno.split(".")
            for i in range(3):
                if current_version_list[i] == new_version_list[i]:
                    continue
                elif current_version_list[i] < new_version_list[i]:
                    has_new_version = True
                    break
                else:
                    break

        if has_new_version:
            return success_json({'new_version': {
                    "vno": version_list[0].vno,
                    "size": version_list[0].size,
                    "desc": version_list[0].desc,
                    "is_force": version_list[0].is_force,
                    "down_url": version_list[0].down_url
                }}
            )
    return failed_json(u'已经是最新版本')


# 消息数量和系统消息
@app_user_required
def app_message_count(request):
    is_total = request.POST.get('total', None)
    page = int(request.POST.get('page', '1'))
    pagesize = int(request.POST.get('pageSize', '15'))

    # 评论
    # comment_num = DynamicMsg.objects.using('fps').filter(action_type='2', userB=request.user.id, is_new=True).count()

    # 学习提醒: 完成任务，项目打分
    study_num = MyMessage.objects.using('default').filter(action_type__in=['11', '15'],
                                                          is_new=True, userB=request.user.id).count()
    # 班级动态: 成绩排名变化 体验成功
    class_num = MyMessage.objects.using('default').filter(action_type__in=['10', '17'],
                                                          is_new=True, userB=request.user.id).count()
    # 系统消息: 续费通知 报名成功 新的班会通知 班会就快开始
    system_num = MyMessage.objects.using('default').filter(
            action_type__in=['16', '18', '19', '50'], is_new=True, userB=request.user.id).count()
    if is_total:
        return success_json({'count': study_num+class_num+system_num})

    # 系统消息详情
    # todo 安卓更新后删除
    messages = MyMessage.objects.using('default').filter(
                                                action_type__in=['16', '18', '19', '50'], userB=request.user.id)
    totalnum = messages.count()
    messages = messages.order_by('-date_action')[(page-1)*pagesize if (page-1)*pagesize < totalnum else totalnum:
                                                 page*pagesize if page*pagesize < totalnum else totalnum]
    message_data = []
    for message in messages:
        if message.is_new:
            message.is_new = False
            message.save(using='default')
        message_data.append(dict(
            id=message.id,
            date=message.date_action.strftime('%Y/%m/%d %H:%M:%S'),
            content=strip_tags(message.action_content),
            ))

    data = dict(
        study_num=study_num,
        class_num=class_num,
        system_num=system_num,
        list=message_data
    )
    return success_json(data)


# 消息详情
@app_user_required
def app_message_detail(request):
    message_type = request.POST.get('type', None)
    page = int(request.POST.get('page', '1'))
    pagesize = int(request.POST.get('pageSize', '15'))
    if not message_type:
        return failed_json(u'消息类型不能为空')
    if message_type == '1':
        # 系统消息详情
        messages = MyMessage.objects.using('default').filter(
                                                action_type__in=['16', '18', '19', '50'], userB=request.user.id)
    elif message_type == '2':
        messages = MyMessage.objects.using('default').filter(action_type__in=['11', '15'], userB=request.user.id)
    elif message_type == '3':
        messages = MyMessage.objects.using('default').filter(action_type__in=['10', '17'], userB=request.user.id)
    else:
        return failed_json(u'消息类型不正确')
    totalnum = messages.count()
    messages = messages.order_by('-date_action')[(page-1)*pagesize if (page-1)*pagesize < totalnum else totalnum:
                                                 page*pagesize if page*pagesize < totalnum else totalnum]
    # 清除IOS消息数量
    try:
        mes_num = AppSendMessageNum.objects.get(user=request.user.id)
        mes_num.message_count = 0
        mes_num.save()
    except AppSendMessageNum.DoesNotExist:
        pass

    data = []
    for message in messages:
        content = strip_tags(message.action_content) if message.action_content else ''
        if message.is_new:
            message.is_new = False
            message.save(using='default')

        data.append(dict(
            id=message.id,
            type=message_type,
            date=message.date_action.strftime('%Y/%m/%d %H:%M:%S'),
            content=content,
        ))

    return success_json({'list': data})


# 更新设备token
@app_user_required
def app_update_push_token(request):
    push_token = request.POST.get('pushToken', None)
    user = request.user
    user.token = push_token
    user.save()
    return success_json({})


# 校验密码
@app_user_required
def app_check_password(request):
    password = request.POST.get('password')
    if not password:
        return failed_json(u'密码不能为空')

    check = request.user.check_password(password)
    if check:
        return success_json({})
    return failed_json(u'密码错误')


# 修改密码
@app_user_required
def app_change_password(request):
    new_password = request.POST.get('new_password')
    old_password = request.POST.get('old_password')
    if (not new_password) or (not old_password):
        return failed_json(u'密码不能为空')
    check = request.user.check_password(old_password)
    if check:
        user = request.user
        user.password = make_password(new_password)
        user.save()
        return success_json({})
    return failed_json(u'密码错误')


# 绑定手机验证
@app_user_required
def app_check_mobile(request):
    # 设置retry跳过geetest验证
    request.POST['retry'] = 1
    return bind_mobile_sendsms(request)


# 绑定手机
@app_user_required
def app_bind_mobile(request):
    return bind_mobile(request)


# 域名判断
def app_domain(request):
    client = request.POST.get('client')
    ios_version = request.POST.get('vno')               # ios版本号
    client_type = request.POST.get('type')
    dev_student_check = 17
    dev_teacher_check = 2
    domain = 'http://www.maiziedu.com/v4/'
    if client_type not in ['1', '2']:
        return failed_json(u'客户端类型错误')
    if client == 'ios':
        result = db.api.common.app.ios_version(client_type)
        if result.is_error():
            return failed_json(u'服务器错误')
        version_list = result.result()
        if version_list[0]['is_check']:
            if int(client_type) == 1:
                if int(ios_version) == dev_student_check and int(version_list[0]['vno'] == dev_student_check):
                    domain = 'http://dev.microoh.com:99/v4/'
            else:
                if int(ios_version) == dev_teacher_check and int(version_list[0]['vno'] == dev_teacher_check):
                    domain = 'http://dev.microoh.com:99/v4/'
        return success_json({'mainURL': domain})
    else:
        return failed_json(u'客户端类型错误')
