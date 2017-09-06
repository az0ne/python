# coding: utf-8
import re
import json
import datetime
from core.common.http.response import success_json, failed_json
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.db.models import Q

import db.api.lps.teacher_warning
import db.api.common.app
import db.api.coach.coach
from mz_common.function_discuss import answer_post_api
from mz_common.models import AndroidVersion
from mz_lps.models import Project, ProjectMaterial, ProjectImage
from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord
from mz_lps4.interface_teacher_warning import update_teacher_backlog_is_done
from mz_user.models import UserProfile
from utils.logger import logger as log
from website.api.user.decorators import app_teacher_required
from website.api.warning_teacher.interface import get_app_teacher_info, app_get_my_student_by_teacher_id_interface, \
    get_teacher_warning_backlog_by_teacher_id_interface, get_question_detail_interface, \
    get_backlog_detail_by_id_interface, get_project_detail_interface, get_meeting_list_interface, \
    get_meeting_detail_interface,app_backlog_history_by_teacher_id_interface
from utils.constants import CoachCommentUserType
from mz_lps4.interface_coach import post_coach_comment
from utils.constants import CoachUserType
from mz_lps4.interface_coach import create_coach_info_teacher

@app_teacher_required
def one_to_one_service(request):
    """
    1v1服务列表
    :param request:
    :return:
    """
    teacher_id = request.user.id
    result = get_teacher_warning_backlog_by_teacher_id_interface(teacher_id)
    if not result.get('success', False):
        return failed_json(u"请求失败，请稍后再试")
    else:
        return success_json(result.get('data', {}))


@app_teacher_required
def get_meeting_list(request):
    """
    获取班会列表
    :param request:
    :return:
    """
    teacher_id = request.user.id

    result = get_meeting_list_interface(teacher_id)
    if not result.get('success', False):
        return failed_json(result.get('msg', u'服务器开小差了,稍后再试吧'))

    return success_json(result.get('data', []))


@app_teacher_required
def get_question_detail(request):
    """
    问题详情
    :param request:
    :return:
    """
    user_id = request.user.id

    # get priority and deadline in data
    backlog_id = request.POST.get('backlog_id', None)
    if not backlog_id:
        return failed_json(u"backlog_id不能为空")
    result = get_backlog_detail_by_id_interface(backlog_id)
    if not result.get('success', False):
        log.warn('get_backlog_detail_by_id_interface, backlog_id %s' % backlog_id)
        return failed_json(result.get('msg', u'服务器开小差了,稍后再试吧'))
    else:
        data = result.get('data', {})
    if not data:
        log.warn('priority and deadline data is null, backlog_id %s' % backlog_id)
        return failed_json(u'服务器开小差了,稍后再试吧')

    # update question_detail
    problem_id = data.get('obj_id', None)
    if not problem_id:
        log.warn('data has no obj_id, backlog_id %s' % backlog_id)
        return failed_json(u'服务器开小差了,稍后再试吧')
    del data['obj_id']
    result = get_question_detail_interface(problem_id, user_id)
    if not result.get('success', False):
        log.warn('get_question_detail_interface, backlog_id %s' % backlog_id)
        return failed_json(result.get('msg', u'服务器开小差了,稍后再试吧'))
    question_detail = result.get('data', {})

    data.update(question_detail)

    # update is_new in backlog
    result = db.api.lps.teacher_warning.update_backlog_status_by_obj_id('is_new', problem_id, 4)
    # 4 is question & answer
    if result.is_error():
        log.warn('update_backlog_status_by_obj_id error, obj_id %s', problem_id)
    return success_json(data)


@app_teacher_required
def answer_question(request):
    """
    回复问题
    :param request:
    :return:
    """
    user = request.user
    _post = request.POST

    comment = _post.get('comment', None)
    parent_id = _post.get('parent_id', None)
    problem_id = _post.get('problem_id', None)
    answer_user_id = _post.get('user_id', None)
    answer_nick_name = _post.get('nick_name', None)

    if not (comment and problem_id and parent_id and answer_user_id and answer_nick_name):
        return failed_json(u'参数不全')
    is_succeed, fail_msg, result = answer_post_api(user, comment, parent_id, problem_id, answer_user_id,
                                                   answer_nick_name)

    if is_succeed:
        return success_json()
    else:
        return failed_json(fail_msg)


@app_teacher_required
def get_project_detail(request):
    """
    获取项目详情
    :param request:
    :return:
    """
    backlog_id = request.POST.get('backlog_id', None)
    if not backlog_id:
        return failed_json(u"backlog_id不能为空")

    result = get_project_detail_interface(backlog_id)
    if not result.get('success', False):
        return failed_json(result.get('msg', u'服务器开小差了,稍后再试吧'))

    data = result.get('data', {})

    # update priority and deadline in data
    result = get_backlog_detail_by_id_interface(backlog_id)
    if not result.get('success', False):
        return failed_json(u'服务器开小差了,稍后再试吧')
    else:
        data.update(result.get('data', {}))

    # update is_new in backlog
    result = db.api.lps.teacher_warning.update_backlog_status_by_obj_id('is_new', data.get('obj_id', 0), 3)
    # 3 is project
    if result.is_error():
        log.warn('update_backlog_status_by_obj_id error, backlog_id %s', backlog_id)

    return success_json(data)


@app_teacher_required
def get_meeting_detail(request):
    """
    获取班会详情
    :param request:
    :return:
    """
    backlog_id = request.POST.get('backlog_id', None)
    if not backlog_id:
        return failed_json(u"backlog_id不能为空")

    data_result = get_meeting_detail_interface(backlog_id)
    if not data_result.get('success', False):
        return failed_json(data_result.get('msg', u'服务器开小差了,稍后再试吧'))

    # update is_new in backlog
    result = db.api.lps.teacher_warning.update_backlog_new_status_by_id(backlog_id)
    if result.is_error():
        log.warn('db update_backlog_new_status_by_id error, backlog_id %s' % backlog_id)

    return success_json(data_result.get('data', {}))


def app_teacher_login(request):
    """
    老师端登陆
    :param request:
    :return:
    """
    user_account = request.POST.get('account', None)
    user_password = request.POST.get('password', None)
    if not user_account:
        return failed_json(u"账号不能为空")
    if not user_password:
        return failed_json(u"密码不能为空")
    p = re.compile(settings.REGEX_EMAIL + "|" + settings.REGEX_MOBILE)
    if not p.match(user_account):
        return failed_json(u"账号格式不对")
    try:
        user = UserProfile.objects.get(Q(email=user_account) | Q(mobile=user_account))
        if user.is_disabled:
            return failed_json(u"账号被禁用")
        if not user.is_teacher():
            return failed_json(u"只有老师才能登陆")
    except UserProfile.DoesNotExist:
        return failed_json(u"账号不存在")
    user = authenticate(username=user_account, password=user_password)
    if user:
        if user.is_active:
            login(request, user)
            return success_json(get_app_teacher_info(user, is_self=request.session.session_key))
        return failed_json(u"账号未激活")
    return failed_json(u"账号或密码错误")


@app_teacher_required
def fetch_all_students(request):
    """
    获取我的学生by老师
    :param request:
    :return:
    """
    teacher_id = request.user.id
    data = app_get_my_student_by_teacher_id_interface(teacher_id)
    return success_json(dict(list=data))


# 检查更新
def teacher_check_update(request):
    current_version = request.POST.get('currVno', None)  # 安卓版本号
    client = request.POST.get('client')
    ios_version = request.POST.get('vno')               # ios版本号
    # 是否有新版本
    has_new_version = False

    if client == 'ios':

        result = db.api.common.app.ios_version(_enable_cache=True, app_type=2)
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
    version_list = AndroidVersion.objects.using('default').filter(type=AndroidVersion.TYPE_TEACHER).order_by("-id")
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


# 更新设备token
@app_teacher_required
def app_update_push_token(request):
    push_token = request.POST.get('pushToken', None)
    client = request.POST.get('client')
    user_id = request.user.id
    if client == 'ios':
        app = 2
    elif client == 'android':
        app = 1
    else:
        return failed_json(u'wrong type')
    result = db.api.common.app.app_update_user_token(user_id=user_id, token=push_token, app=app)
    if result.is_error():
        log.error('update_user_token_failed')
        return failed_json(u'服务器开小差了,稍后再试吧')
    return success_json({})

# app 1.1-------------------------------------------------------------------------------------


@app_teacher_required
def service_history(request):
    """
    获取代办历史记录
    :param request:
    :return:
    """
    teacher_id = request.user.id
    page = request.POST.get('page', '1')
    order = request.POST.get('order', '1')
    types = request.POST.get('types', None)
    if not page:
        return failed_json(u"page不能为空")
    if not order:
        return failed_json(u"order不能为空")
    if not types:
       types = []
    else:
        try:
            types = map(lambda x: int(x), types.split(','))
        except:
            return failed_json(u"types格式不正确")
    try:
        page = int(page)
    except:
        return failed_json(u"page格式不正确")

    if order not in ['0', '1']:
        return failed_json(u"order格式不正确")

    data = app_backlog_history_by_teacher_id_interface(teacher_id, page, order, types)
    return success_json(dict(list=data))


@app_teacher_required
def app_get_history_detail(request):
    """
    学习辅导详情
    :param request:
    :return:
    """
    coach_id = request.POST.get('coach_id')
    page = int(request.POST.get('page', 1))
    page_size = int(request.POST.get('pageSize', 15))

    user = request.user

    coach_result = db.api.coach.coach.get_coach(coach_id, user.id, user.is_student())

    if coach_result.is_error():
        log.warn('get_coach failed. coach_id: {0}, '
                 'user_id: {1}.'.format(coach_id, user.id))
    coach = coach_result.result()
    if not coach:
        return failed_json(u'服务器开小差了,稍后再试吧')

    comments_result = db.api.lps.teacher_warning.get_coach_history_comments(coach_id, (page-1)*page_size, page_size)
    if comments_result.is_error():
        log.warn('get_coach_comments failed. '
                 'coach_id: {}'.format(coach_id))
        comments = []
    else:
        comments = comments_result.result()

    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    data = [dict(
            comment_id=comment['coach_id'],
            name=comment['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
            user_type=1 if comment['user_type'] == CoachCommentUserType.STUDENT else 2,
            time=comment['create_date'].strftime('%Y/%m/%d %H:%M:%S'),
            content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
            p.sub(pic_url, '<p>%s</p>' % comment['comment']),
            priority=comment['done_status']
            ) for comment in comments]
    final_data = {'list': data}
    if page == 1:
        final_data['list'][0].update({'source': coach['source']})
    return success_json(final_data)


@app_teacher_required
def app_get_coach_list(request):
    """
    辅导列表
    :param request:
    :return:
    """
    teacher_id = request.user.id
    result = get_teacher_warning_backlog_by_teacher_id_interface(teacher_id)
    if not result.get('success', False):
        return failed_json(u"请求失败，请稍后再试")
    else:
        return success_json(result.get('data', {}))


@app_teacher_required
def app_create_coach_info(request):
    """
    创建辅导详情
    :param request:
    :return:
    """
    teacher = request.user
    career_id = request.POST.get('career_id')
    student_id = request.POST.get('student_id')
    stage_task_id = int(request.POST.get('stage_task_id', 0))
    comment = request.POST.get('comment')
    if not student_id:
        return failed_json(u"student_id不能为空")
    source = None
    if stage_task_id:
        from mz_lps3.models import StageTaskRelation
        try:
            stage_task_relation = StageTaskRelation.objects.get(id=stage_task_id)
            source = '%s %s' % (stage_task_relation.stage.name, stage_task_relation.task.name)
        except StageTaskRelation.DoesNotExist:
            source = None
    try:
        return create_coach_info_teacher(teacher, career_id, student_id, source, None, comment, CoachUserType.TEACHER)
    except Exception, e:
        log.warn('create_coach_info_student is except:%s' % str(e))
        return failed_json(u'服务器错误')


@app_teacher_required
def app_reply_coach_info(request):
    """
    回复辅导
    :param request:
    :return:
    """
    user = request.user
    coach_id = request.POST.get('coach_id')
    comment = request.POST.get('comment', '')

    if not coach_id:
        return failed_json(u"coach_id不能为空")
    if not comment:
        return failed_json(u"comment不能为空")
    try:
        result = post_coach_comment(coach_id, user, comment)
    except Exception, e:
        log.warn('post_coach_comment is except:%s coach_id:%s' % (str(e), coach_id))
        result = failed_json(u'服务器开小差了，请稍后再试。')

    return result


@app_teacher_required
def app_get_coach_detail(request):
    """
    学习辅导详情
    :param request:
    :return:
    """
    coach_id = request.POST.get('coach_id')
    page = int(request.POST.get('page', 1))
    page_size = int(request.POST.get('page_size', 15))

    user = request.user

    coach_result = db.api.coach.coach.get_coach(coach_id, user.id, user.is_student())

    if coach_result.is_error():
        log.warn('get_coach failed. coach_id: {0}, '
                 'user_id: {1}.'.format(coach_id, user.id))
    coach = coach_result.result()
    if not coach:
        return failed_json(u'服务器开小差了,稍后再试吧')

    comments_result = db.api.coach.coach.get_coach_comments(coach_id, start_index=(page-1)*page_size,
                                                            end_index=page_size)
    if comments_result.is_error():
        log.warn('get_coach_comments failed. '
                 'coach_id: {}'.format(coach_id))
        comments = []
    else:
        comments = comments_result.result()

    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    data = [dict(
            service_id=comment['id'],
            name=comment['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
            user_type=1 if comment['user_type'] == CoachCommentUserType.STUDENT else 2,
            time=comment['create_date'].strftime('%Y/%m/%d %H:%M:%S'),
            content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
            p.sub(pic_url, '<p>%s</p>' % comment['comment']),
            ) for comment in comments]
    final_data = {'list': data}
    if page == 1:
        final_data['list'][0].update({'source': coach['source']})
        # update priority and deadline in data
        backlog_id = request.POST.get('backlog_id')
        result = get_backlog_detail_by_id_interface(backlog_id)
        if not result.get('success', False):
            log.warn('get_backlog_detail_by_id_interface error, backlog_id %s' % backlog_id)
            return failed_json(u'服务器开小差了,稍后再试吧')
        final_data.update(result.get('data', {}))
        # update is_new in backlog
        result = db.api.lps.teacher_warning.update_backlog_new_status_by_id(backlog_id)
        if result.is_error():
            log.warn('db update_backlog_new_status_by_id error, backlog_id %s' % backlog_id)
    return success_json(final_data)


@app_teacher_required
def app_teacher_project_coach(request):
    # 老师项目辅导详情
    coach_id = request.POST.get('coach_id')
    backlog_id = request.POST.get('backlog_id')
    teacher = request.user
    result = db.api.coach.coach.get_coach(coach_id, teacher.id, False)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    if not result.result():
        return failed_json(u'找不到相关数据')
    coach = result.result()
    if coach['teacher_id'] != teacher.id:
        return failed_json(u'权限不符')
    source_location = coach['source_location']
    source_location = json.loads(source_location)
    source_location = source_location['project']
    try:
        user_task_record = UserTaskRecord.objects.get(
            class_id=source_location['class_id'], student_id=source_location['student_id'],
            stage_task_id=source_location['stage_task_id'])
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到相关数据')

    is_task = False if source_location['item_id'] else True
    if is_task:
        project_id = user_task_record.stage_task.task.project_id
        project = Project.objects.get(id=project_id)
    else:
        try:
            item_record = UserKnowledgeItemRecord.objects.get(student_id=source_location['student_id'],
                                                              class_id=source_location['class_id'],
                                                              knowledge_item_id=source_location['item_id'],
                                                              user_task_record=user_task_record)
        except UserKnowledgeItemRecord.DoesNotExist:
            return failed_json(u'找不到相关数据')
        project_id = item_record.knowledge_item.obj_id
        project = Project.objects.get(id=project_id)
    # 获取项目素材，项目图片示例,项目描述,项目示例视频
    project_material = ProjectMaterial.objects.filter(project=project)
    project_image = ProjectImage.objects.filter(project=project)
    result = db.api.coach.coach.get_project_coach_comment(coach['id'])
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    comment_list = result.result()
    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    tmp = {}
    comments = []
    project_is_commented = False
    for comment in comment_list:
        if comment['user_id'] == teacher.id:
            project_is_commented = True
        if tmp.get('comment_id') == comment['id']:
            tmp['sub_material'].append(comment['file_name'])
        else:
            if tmp:
                comments.append(tmp)
            tmp = dict(
                comment_id=comment['id'],
                content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
                p.sub(pic_url, '<p>%s</p>' % comment['comment']),
                user_type=comment['user_type'],
                user_id=comment['user_id'],
                name=comment['nick_name'],
                avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
                time=comment['create_date'].strftime("%Y/%m/%d %H:%M:%S"),
                sub_material=[]
            )
            if comment['mz_coach_project.id']:
                tmp['sub_material'].append(comment['file_name'])
    comments.append(tmp)
    teacher_name = '小麦'
    teacher_header = settings.SITE_URL + '/static/images/wapwike/weixin_share_logo.jpg'
    if user_task_record.status == 'DONE':
        project_status = 1
    elif user_task_record.status == 'DOING':
        project_status = 0
    else:
        project_status = 2
    data = dict(
        project_info=dict(
            show_score=is_task,
            teacher_name=teacher_name,
            teacher_header=teacher_header,
            project_id=project.id,
            project_is_commented=project_is_commented,
            project_name=project.title,
            project_desc=project.description,
            project_score=user_task_record.score,
            project_status=project_status,
            project_material=[material.name for material in project_material],
            img_list=[settings.SITE_URL+settings.MEDIA_URL+str(img.image) for img in project_image]
        ),
        reply_list=comments,
    )
    result = get_backlog_detail_by_id_interface(backlog_id)
    if not result.get('success', False):
        log.warn('get_backlog_detail_by_id_interface error, backlog_id %s' % backlog_id)
        return failed_json(u'服务器开小差了,稍后再试吧')
    data.update(result.get('data', {}))
    # update is_new in backlog
    result = db.api.lps.teacher_warning.update_backlog_new_status_by_id(backlog_id)
    if result.is_error():
        log.warn('db update_backlog_new_status_by_id error, backlog_id %s' % backlog_id)
    return success_json(data)


@app_teacher_required
def app_teacher_score_project(request):
    # 老师
    score = request.POST.get('score')
    coach_id = request.POST.get('coach_id')
    teacher = request.user
    result = db.api.coach.coach.get_coach_data(coach_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    if not result.result():
        return failed_json(u'找不到相关数据')
    coach = result.result()
    if coach['teacher_id'] != teacher.id:
        return failed_json(u'权限不符')

    if score not in ['S', 'A', 'B', 'C', 'D']:
        return failed_json(u'分数不正确')
    source_location = coach['source_location']
    source_location = json.loads(source_location)
    source_location = source_location['project']
    try:
        user_task_record = UserTaskRecord.objects.get(class_id=source_location['class_id'],
                                                      student_id=source_location['student_id'],
                                                      stage_task_id=source_location['stage_task_id'])
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到相关数据')

    coach = result.result()
    user_task_record.score = score
    if score == 'D':
        user_task_record.status = 'FAIL'
    else:
        user_task_record.status = 'PASS'
    user_task_record.correct_time = datetime.datetime.now()
    user_task_record.save()
    update_teacher_backlog_is_done(coach['id'], None, request.user.id, coach['student_id'], 14)
    return success_json()
