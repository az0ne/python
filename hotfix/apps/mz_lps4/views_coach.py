# -*- coding: utf-8 -*-
import os
import datetime
import json
import uuid

from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseServerError
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings

from mz_common.views import sys_send_message
from mz_lps.models import Project, Class, ProjectMaterial, ProjectImage
from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord
from mz_lps4.class_dict import LPS4_DICT, TRY_CLASS_DICT
from mz_lps4.interface_lps import get_free_task_id_by_class_id
from utils.constants import CoachUserType
from utils.logger import logger as log
from mz_lps4.context import get_lps4_context
from mz_lps4.interface_coach import get_coach_detail, post_coach_comment
from utils.sensitive_word import sensitive_word
from core.common.http.response import failed_json, success_json
from mz_lps4.interface_coach import create_coach_info_student, create_coach_info_teacher
from mz_lps3.functions_nj import TaskKnowledgeInterface
from mz_lps4.interface_teacher_warning import add_project_coach_teacher_backlog, update_teacher_backlog_is_done
from utils.send_sms_and_message import SendSmsAndMessage
from mz_common.decorators import teacher_required, student_required
from mz_common.functions import paginater
import db.api.onevone.study_service
import db.api.lps.lps_index
import db.api.coach.coach
from utils.tool import upload_generation_dir


@require_http_methods(['GET', 'POST'])
@login_required
def coach_detail(request, coach_id):
    """
    老师学生辅导详情
    :param request:
    :param coach_id:
    :return:
    """
    user = request.user

    if request.method == 'GET':
        data = get_coach_detail(coach_id, user)
        career_id = data['coach'].get('career_id', 0)

        if user.is_student():
            template = 'mz_lps4/stu_ques_ans_detail.html'
            if data['coach']['source_type'] == CoachUserType.PROJECT:
                slp = data['coach']['source_location_project']
                return redirect(reverse(
                    'lps4:student_coach_project',
                    kwargs={
                        'class_id': slp['class_id'],
                        'stage_task_id': slp['stage_task_id'],
                        'item_id': slp['item_id']
                    })
                )
        else:
            template = 'mz_usercenter/teacher/tutor_detail.html'
            if data['coach']['source_type'] == CoachUserType.PROJECT:
                return redirect(reverse(
                    'lps4:teacher_coach_project',
                    kwargs={'coach_id': data['coach']['id']})
                )

        return render(
            request, template, data,
            context_instance=get_lps4_context(request, career_id))

    else:
        content = request.POST.get('content')
        return post_coach_comment(coach_id, user, content)


@teacher_required
def teacher_coach_list(request, career_id, student_id):
    """
    老师端 辅导列表
    :param request:
    :param career_id: 职业课程id
    :param student_id: 学生id
    :return:
    """
    page = request.GET.get('page', 1)
    page_size = 10
    page_aroud = 2
    try:
        page = int(page)
    except ValueError:
        page = 1
    order_by = request.GET.get('order_by', 'all')
    if order_by not in ['done', 'todo', 'all']:
        order_by = 'all'
    teacher_id = request.user.id
    result = db.api.onevone.study_service.check_into_service(career_id=career_id, teacher_id=teacher_id,
                                                             student_id=student_id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404
    result = db.api.coach.coach.teacher_coach_count(career_id=int(career_id), student_id=int(student_id),
                                                    teacher_id=int(teacher_id), order_by=order_by)
    if result.is_error():
        raise Http404
    if not result.result():
        total_count = 0
    else:
        total_count = result.result()['total_count']
    page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count,
                                                                    page_aroud)
    coach_result = db.api.coach.coach.teacher_coach_list(career_id=int(career_id),
                                                         student_id=int(student_id),
                                                         teacher_id=int(teacher_id),
                                                         start_index=start_index, end_index=page_size,
                                                         order_by=order_by)
    if coach_result.is_error():
        raise Http404
    data = coach_result.result()
    for coach in data:
        if coach['source_type'] == CoachUserType.STUDENT_VIDEO:
            # 视频播放
            source_location = json.loads(coach['source_location'])
            if source_location.get('lps'):
                param_list = source_location.get('lps')
                if len(param_list) == 5:
                    coach['url'] = reverse('course:lesson_video_view', kwargs={'course_id': param_list[3],
                                                                               'lesson_id': param_list[4]})
                    coach['url'] = '%s?t=%s' % (coach['url'], coach['source'].split(' ')[-1])
    # 清除新服务数目
    result = db.api.coach.coach.clean_new_coach_count(
            career_id=career_id, user_id=student_id, teacher_id=teacher_id)
    if result.is_error():
        raise Http404
    return render(request, 'mz_usercenter/teacher/tutor_list.html', {'career_id': career_id,
                                                                     'teacher_id': teacher_id,
                                                                     'student_id': student_id,
                                                                     'page_count_list': page_count_list,
                                                                     'page_index': page_index,
                                                                     'data': data,
                                                                     'order_by': order_by})


@student_required
def student_coach_list(request, career_id):
    """
    学生 学习建议列表
    :param request:
    :param career_id:
    :return:
    """
    user = request.user
    teacher = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=request.user.id)
    if teacher.is_error():
        raise Http404
    if not teacher.result():
        raise Http404

    if request.method == 'GET':
        # 顶部职业课程信息
        result = db.api.onevone.study_service.get_lps4_student_career(user_id=user.id)
        if result.is_error():
            raise Http404
        if not result.result():
            raise Http404
        careers = []
        for career in result.result():
            result = db.api.lps.lps_index.get_lps_3_1_career_info(career['career_id'])
            if result.is_error():
                raise Http404
            careers.append(result.result()[0])

        page = request.GET.get('page', 1)
        page_size = 10
        page_aroud = 2
        try:
            page = int(page)
        except ValueError:
            page = 1
        result = db.api.coach.coach.student_coach_count(career_id=int(career_id), student_id=int(user.id))
        if result.is_error():
            raise Http404
        if not result.result():
            total_count = 0
        else:
            total_count = result.result()['total_count']
        page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count, page_aroud)
        data = db.api.coach.coach.student_coach_list(career_id=int(career_id),
                                                     student_id=int(user.id),
                                                     start_index=start_index, end_index=page_size)
        if data.is_error():
            raise Http404
        data = data.result()
        for coach in data:
            if coach['source_type'] == CoachUserType.STUDENT_VIDEO:
                # 视频播放
                source_location = json.loads(coach['source_location'])
                if source_location.get('lps'):
                    param_list = source_location.get('lps')
                    if len(param_list) == 5:
                        coach['url'] = reverse('lps3:student_item_lesson', kwargs={'class_id': param_list[0],
                                                                                   'stagetask_id': param_list[1],
                                                                                   'item_id': param_list[2]})
                        coach['url'] = '%s?t=%s' % (coach['url'], coach['source'].split(' ')[-1])
        # 清除学生未读服务数
        result = db.api.coach.coach.clean_new_coach_count(career_id=career_id,
                                                          user_id=request.user.id,
                                                          teacher_id=None)
        if result.is_error():
            raise Http404
        return render(request, 'mz_lps4/stu_ques_ans.html', {'data': data,
                                                             'career_id': int(career_id),
                                                             'page_count_list': page_count_list,
                                                             'page_index': page_index,
                                                             'careers': careers,
                                                             }, context_instance=get_lps4_context(request, career_id))

    if request.method == 'POST':

        comment = request.POST.get('content')
        source = request.POST.get('source')
        source_location = request.POST.get('source_location')
        source_type = request.POST.get('source_type', CoachUserType.STUDENT)

        try:
            return create_coach_info_student(user, career_id, source, source_location, comment, source_type)
        except Exception, e:
            log.warn('create_coach_info_student is except:%s' % str(e))
            return failed_json(u'服务器错误')


def teacher_create_coach(request, career_id, student_id):
    """
    老师新建学习辅导
    :param request:
    :param career_id:
    :param student_id:
    :return:
    """
    teacher = request.user
    result = db.api.onevone.study_service.check_into_service(
            career_id=career_id, teacher_id=teacher.id, student_id=student_id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404

    if request.method == 'GET':
        # result = db.api.onevone.study_service.get_user_name(
        #         user_id=student_id)
        # if result.is_error():
        #     raise Http404
        # teacher_id = teacher.id
        # student_name = result.result()['real_name'] or result.result()['nick_name']
        return render(request, 'mz_usercenter/teacher/tutor_add.html', locals())

    if request.method == 'POST':
        # 保存学习建议
        comment = request.POST.get('content')
        try:
            return create_coach_info_teacher(teacher, career_id, student_id, None, None, comment, CoachUserType.TEACHER)
        except Exception, e:
            log.warn('create_coach_info_student is except:%s' % str(e))
            return failed_json(u'服务器错误')


def student_coach_project(request, class_id, stage_task_id, item_id):
    """
    学生 项目辅导详情
    :param request:
    :param class_id:
    :param stage_task_id:
    :param item_id:
    :return:
    """
    try:
        class_id = int(class_id)
        stage_task_id = int(stage_task_id)
    except ValueError:
        raise Http404
    if class_id <= 0 or stage_task_id <= 0:
        raise Http404
    try:
        klass = Class.objects.xall().get(id=class_id)
    except Class.DoesNotExist:
        raise Http404
    user = request.user
    user_task_record = get_object_or_404(
        UserTaskRecord, class_id=class_id, student_id=user.id, stage_task_id=stage_task_id)
    career_id = LPS4_DICT.get(class_id)
    # 获取对应老师
    result = db.api.onevone.study_service.get_teacher_info_by_lps4(int(career_id), int(user.id))
    if result.is_error():
        raise Http404
    teacher = result.result()
    is_task = False
    # 当前任务球是否全部完成
    if int(item_id) == 0:
        if user_task_record.status == 'DOING':
            iface = TaskKnowledgeInterface(class_id, stage_task_id, class_type=klass.class_type)
            iface.load_student_data(user.id)
            if not iface.all_items_have_done(user.id):
                raise Http404
            guide_task_id = klass.career_course.lps3_guide_task_id
            # lps3.1 试学班的免费任务自动修改
            # 如果class_id在lps3.1免费班字典里
            if class_id in TRY_CLASS_DICT.values():
                free_task_ids = get_free_task_id_by_class_id(class_id)
                if user_task_record.stage_task.task_id in [guide_task_id, settings.GUIDE_TASK_ID] + free_task_ids:
                    user_task_record.status = 'PASS'
                    user_task_record.score = 'A'
                    user_task_record.done_time = datetime.datetime.now()
                    user_task_record.save()

    source_location = json.dumps(dict(
        project=dict(
            class_id=int(class_id),
            stage_task_id=int(stage_task_id),
            item_id=int(item_id),
            student_id=int(user.id)
        )
    ))
    if int(item_id) == 0:
        is_task = True
        project_id = user_task_record.stage_task.task.project_id
        project = Project.objects.get(id=project_id)
    else:
        item_record = get_object_or_404(UserKnowledgeItemRecord, student_id=user.id, class_id=class_id,
                                        knowledge_item_id=item_id, user_task_record=user_task_record)
        if item_record.status == 'DOING':
            if class_id in TRY_CLASS_DICT.values():
                item_record.status = 'DONE'
                item_record.done_time = datetime.datetime.now()
                item_record.save()
        project_id = item_record.knowledge_item.obj_id
        project = Project.objects.get(id=project_id)

    if request.method == 'GET':
        # 获取项目素材，项目图片示例,项目描述,项目示例视频
        project_material = ProjectMaterial.objects.filter(project=project)
        project_image = ProjectImage.objects.filter(project=project)
        project_desc = project.description
        video = project.video_guide

        # 辅导列表
        comments = []
        can_submit = False
        if_reply = False
        if teacher:
            can_submit = True
            result = db.api.coach.coach.get_project_coach(career_id, user.id, teacher['id'], source_location, True)
            if result.is_error():
                raise Http404
            if result.result():
                coach = result.result()
                result = db.api.coach.coach.get_project_coach_comment(coach['id'])
                if result.is_error():
                    return HttpResponseServerError()
                comment_list = result.result()
                tmp = {}
                for comment in comment_list:
                    if comment['user_id'] == user.id:
                        if_reply = True
                    if tmp.get('comment_id') == comment['id']:
                        name = '%s-%s-%s-%s' % (user_task_record.stage_task.task.name, project.title,
                                                comment['nick_name'], comment['create_date'].strftime("%Y%m%d%H%M%S"))
                        tmp['project'].append(dict(
                            file_name=comment['file_name'],
                            file_type=comment['file_type'],
                            file_url='%s?name=%s&url=%s' % (settings.PROJECT_DOWN_DOMAIN, name,
                                                            comment['file_url'])
                        ))
                    else:
                        if tmp:
                            comments.append(tmp)
                        tmp = dict(
                            coach_id=comment['coach_id'],
                            comment_id=comment['id'],
                            content=comment['comment'],
                            user_type=comment['user_type'],
                            user_id=comment['user_id'],
                            nick_name=comment['nick_name'],
                            head=comment['head'],
                            create_date=comment['create_date'].strftime("%Y年%m月%d日 %H:%M:%S"),
                            project=[]
                        )
                        if comment['mz_coach_project.id']:
                            name = '%s-%s-%s-%s' % (user_task_record.stage_task.task.name, project.title,
                                                    comment['nick_name'],
                                                    comment['create_date'].strftime("%Y%m%d%H%M%S"))
                            tmp['project'].append(dict(
                                file_name=comment['file_name'],
                                file_type=comment['file_type'],
                                file_url='%s?name=%s&url=%s' % (settings.PROJECT_DOWN_DOMAIN, name,
                                                                comment['file_url'])
                            ))
                comments.append(tmp)
        if user_task_record.status == 'DOING':
            div_class = 'pulling'
            div_content = '提交项目后将获得项目评分'
        elif user_task_record.status == 'DONE':
            div_class = 'waiting'
            div_content = '老师将为你的项目评分，<br/>请耐心等待...'
        else:
            if user_task_record.score == 'S':
                div_class = 'super'
                div_content = '超出预期的完成了作业'
            elif user_task_record.score == 'A':
                div_class = 'amazing'
                div_content = '出色的完成了作业'
            elif user_task_record.score == 'B':
                div_class = 'beautiful'
                div_content = '完成了作业主要考核点，<br/>但仍有些许瑕疵'
            elif user_task_record.score == 'C':
                div_class = 'change'
                div_content = '完成了作业但并无出彩之处'
            else:
                div_class = 'danger'
                div_content = '学生的作业没有达到要求'
        return render(request, 'mz_lps4/project_production.html', {'is_task': is_task,
                                                                   'if_reply': if_reply,
                                                                   'user': user,
                                                                   'career_id': career_id,
                                                                   'project_title': project.title,
                                                                   'project_material': project_material,
                                                                   'project_image': project_image,
                                                                   'project_desc': project_desc,
                                                                   'video': video,
                                                                   'comment_list': comments,
                                                                   'div_class': div_class,
                                                                   'div_content': div_content,
                                                                   'teacher': teacher,
                                                                   'class_id': class_id,
                                                                   'stage_task_id': stage_task_id,
                                                                   'item_id': item_id,
                                                                   'can_submit': can_submit})
    if request.method == 'POST' and teacher:
        comment = request.POST.get('content')
        files_list = request.POST.get('fileList')
        if not comment:
            return failed_json(u'内容不能为空')
        abstract = strip_tags(comment)
        abstract = abstract.replace('&nbsp;', '')
        if abstract:
            # 敏感词判断
            result = sensitive_word.filter(abstract)
            if result == sensitive_word.SERVER_ERROR:
                return failed_json(u'服务器错误')
            if result == sensitive_word.FAIL:
                return failed_json(u'含有不正当词汇')
        username = user.real_name or user.nick_name
        result = db.api.coach.coach.get_project_coach(career_id, user.id, teacher['id'], source_location, True, False)
        if result.is_error():
            return failed_json(u'服务器开小差了，请稍后再试')
        if files_list:
            files_list = json.loads(files_list).values()
        now = datetime.datetime.now()
        if result.result():
            coach = result.result()
            result = db.api.coach.coach.add_coach_comment(
                coach['id'], comment, 10, user.id, username,
                str(user.avatar_url), coach['career_id'], files_list)
            if result.is_error():
                return failed_json(u'服务器开小差了，请稍后再试', code=500)
            comment_id = result.result()
            add_project_coach_teacher_backlog(user, teacher['id'], career_id, abstract, coach['id'], comment_id,
                                              send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)
        else:
            # 新建
            source = '【项目制作】 %s %s' % (user_task_record.stage_task.task.name, project.title)
            data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher['id'], 'nick_name': username,
                    'head': str(user.avatar_url), 'source_type': 30, 'abstract': abstract, 'source': source, 'now': now,
                    'source_location': source_location, 'comment': comment, 'user_id': user.id,
                    'is_student': True, 'files_list': files_list}
            result = db.api.coach.coach.create_new_coach(**data)
            if result.is_error():
                return failed_json(u'服务器错误')
            if int(item_id) == 0:
                user_task_record.status = 'DONE'
                user_task_record.done_time = datetime.datetime.now()
                user_task_record.save()
            else:
                item_record = UserKnowledgeItemRecord.objects.get(
                        class_id=class_id, student_id=request.user.id,
                        knowledge_item_id=item_id, user_task_record=user_task_record)
                if item_record.status == 'DOING':
                    item_record.status = 'DONE'
                    item_record.done_time = datetime.datetime.now()
                    item_record.save()
            coach_id = result.result()
            add_project_coach_teacher_backlog(user, teacher['id'], career_id, abstract, coach_id, None,
                                              send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)
        if user_task_record.status == 'FAIL':
            user_task_record.status = 'REDOING'
            user_task_record.save()
        files_div = ''
        if files_list:
            tmp = '''
            <dt class="%s">%s</dt>
            <dd><a href="/uploads/%s">下载</a></dd>
            '''

            files_div = ''.join([tmp % (f['file_type'], f['file_name'], f['file_url']) for f in files_list])

            files_div = '<dl class="source-lists color66 marginB40">%s</dl>' % files_div

        return success_json({'user_id': user.id, 'head': settings.MEDIA_URL + str(user.avatar_url),
                             'nick_name': username, 'create_date': now.strftime("%Y年%m月%d日 %H:%M:%S"),
                             'user_type': 'vip', 'comment': comment, 'files_div': files_div})


def coach_project_upload(request):
    """
    项目辅导文件上传
    :param request:
    :return:
    """
    files = request.FILES.get('file')
    if not files:
        return failed_json(u'文件不能为空')
    if files.size / 1024 > (30 * 1024):
        return failed_json(u'文件大小超过30MB')
    file_limit = ['zip', 'rar', 'ppt', 'doc', 'xls', 'docx', 'xlsx', 'pptx', 'pdf', 'txt']
    file_type = files.name.split(".")[-1].lower()
    if file_type not in file_limit:
        return failed_json(u'文件格式不支持')
    path = os.path.join(settings.MEDIA_ROOT, upload_generation_dir('project'))
    # 如果目录不存在创建目录
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + str(files.name.split(".")[-1])
    path_file = os.path.join(path, file_name)
    db_file_url = path_file.split("..")[-1].replace('/uploads', '').replace('\\', '/')[1:]
    try:
        with open(path_file, 'wb') as f:
            f.write(files.file.read())
    except Exception as e:
        log.warn('coach_project_upload error: %s' % str(e))
        return failed_json(u'服务器错误')
    return success_json({'url': db_file_url, 'name': files.name, 'type': file_type})


def teacher_coach_project(request, coach_id):
    """
    老师 项目辅导详情
    :param request:
    :param coach_id:
    :return:
    """
    teacher = request.user
    result = db.api.coach.coach.get_coach(coach_id, teacher.id, False)
    if result.is_error():
        return HttpResponseServerError()
    if not result.result():
        raise Http404
    coach = result.result()
    if coach['teacher_id'] != teacher.id:
        raise Http404
    if request.method == 'GET':
        source_location = coach['source_location']
        source_location = json.loads(source_location)
        source_location = source_location['project']
        user_task_record = UserTaskRecord.objects.get(
            class_id=source_location['class_id'], student_id=source_location['student_id'],
            stage_task_id=source_location['stage_task_id'])
        is_task = False if source_location['item_id'] else True
        score = 'waiting'
        if is_task:
            if user_task_record.score == 'S':
                score = 'super'
            elif user_task_record.score == 'A':
                score = 'amazing'
            elif user_task_record.score == 'B':
                score = 'beautiful'
            elif user_task_record.score == 'C':
                score = 'change'
            elif user_task_record.score == 'D':
                score = 'danger'
            else:
                score = 'waiting'
            project_id = user_task_record.stage_task.task.project_id
            project = Project.objects.get(id=project_id)
        else:
            item_record = get_object_or_404(UserKnowledgeItemRecord, student_id=source_location['student_id'],
                                            class_id=source_location['class_id'],
                                            knowledge_item_id=source_location['item_id'],
                                            user_task_record=user_task_record)
            project_id = item_record.knowledge_item.obj_id
            project = Project.objects.get(id=project_id)
        # 获取项目素材，项目图片示例,项目描述,项目示例视频
        project_material = ProjectMaterial.objects.filter(project=project)
        project_image = ProjectImage.objects.filter(project=project)
        project_desc = project.description
        video = project.video_guide
        result = db.api.coach.coach.get_project_coach_comment(coach['id'])
        if result.is_error():
            return HttpResponseServerError()
        comment_list = result.result()
        tmp = {}
        comments = []
        if_reply = False
        for comment in comment_list:
            if comment['user_id'] == teacher.id:
                if_reply = True
            if tmp.get('comment_id') == comment['id']:
                name = '%s-%s-%s-%s' % (user_task_record.stage_task.task.name, project.title,
                                        comment['nick_name'],
                                        comment['create_date'].strftime("%Y%m%d%H%M%S"))
                tmp['project'].append(dict(
                    file_name=comment['file_name'],
                    file_type=comment['file_type'],
                    file_url='%s?name=%s&url=%s' % (settings.PROJECT_DOWN_DOMAIN, name, comment['file_url'])
                ))
            else:
                if tmp:
                    comments.append(tmp)
                tmp = dict(
                    coach_id=comment['coach_id'],
                    comment_id=comment['id'],
                    content=comment['comment'],
                    user_type=comment['user_type'],
                    user_id=comment['user_id'],
                    nick_name=comment['nick_name'],
                    head=comment['head'],
                    create_date=comment['create_date'].strftime("%Y年%m月%d日 %H:%M:%S"),
                    project=[]
                )
                if comment['mz_coach_project.id']:
                    name = '%s-%s-%s-%s' % (user_task_record.stage_task.task.name, project.title,
                                            comment['nick_name'],
                                            comment['create_date'].strftime("%Y%m%d%H%M%S"))
                    tmp['project'].append(dict(
                        file_name=comment['file_name'],
                        file_type=comment['file_type'],
                        file_url='%s?name=%s&url=%s' % (settings.PROJECT_DOWN_DOMAIN, name, comment['file_url'])
                    ))
        comments.append(tmp)
        return render(request, 'mz_usercenter/teacher/project_making.html',
                      {'is_task': is_task, 'comment_list': comments, 'coach_id': coach['id'], 'if_reply': if_reply,
                       'project_material': project_material, 'project_image': project_image,
                       'project_desc': project_desc, 'video': video, 'can_submit': True, 'score': score,
                       'class_id': source_location['class_id'], 'stage_task_id': source_location['stage_task_id'],
                       'student_id': source_location['student_id']})

    if request.method == 'POST':
        comment = request.POST.get('content')
        files_list = request.POST.get('fileList')
        if files_list:
            files_list = json.loads(files_list).values()
        if not comment:
            return failed_json(u'内容不能为空')
        abstract = strip_tags(comment)
        abstract = abstract.replace('&nbsp;', '')
        # 敏感词判断
        if abstract:
            result = sensitive_word.filter(abstract)
            if result == sensitive_word.SERVER_ERROR:
                return failed_json(u'服务器错误')
            if result == sensitive_word.FAIL:
                return failed_json(u'含有不正当词汇')
        username = teacher.real_name or teacher.nick_name
        result = db.api.coach.coach.add_coach_comment(
                coach['id'], comment, 20, teacher.id, username,
                str(teacher.avatar_url), coach['career_id'], files_list)
        if result.is_error():
            return failed_json(u'服务器开小差了，请稍后再试', code=500)
        comment_id = result.result()
        update_teacher_backlog_is_done(coach_id, comment_id, teacher.id, coach['student_id'], 14)
        now = datetime.datetime.now()
        files_div = ''
        if files_list:
            tmp = '''
            <dt class="%s">%s</dt>
            <dd><a href="%s">下载</a></dd>
            '''
            files_div = ''.join([tmp % (f['file_type'], f['file_name'], f['file_url']) for f in files_list])
            files_div = '<dl class="source-lists color66 marginB40">%s</dl>' % files_div

        return success_json({'user_id': teacher.id, 'head': settings.MEDIA_URL + str(teacher.avatar_url),
                             'nick_name': username, 'create_date': now.strftime("%Y年%m月%d日 %H:%M:%S"),
                             'user_type': 'teacher', 'comment': comment, 'files_div': files_div})


def grade_coach_project(request):
    """
    项目辅导打分
    :param request:
    :return:
    """
    score = request.POST.get('score', None)
    class_id = request.POST.get('class_id', None)
    student_id = request.POST.get('student_id', None)
    stage_task_id = request.POST.get('stage_task_id', None)
    if score not in ['S', 'A', 'B', 'C', 'D']:
        return failed_json(u'分数不正确')
    try:
        user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=student_id,
                                                      stage_task_id=stage_task_id)
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到相关数据')
    source_location = json.dumps(dict(
        project=dict(
            class_id=int(class_id),
            stage_task_id=int(stage_task_id),
            item_id=0,
            student_id=int(student_id)
        )
    ))
    career_id = LPS4_DICT.get(int(class_id))
    if not career_id:
        return failed_json(u'找不到相关数据')
    result = db.api.coach.coach.get_project_coach(career_id, student_id, request.user.id, source_location, False)
    if result.is_error():
        return failed_json(u'服务器错误')
    if not result.result():
        return failed_json(u'找不到相关数据')
    coach = result.result()
    user_task_record.score = score
    if score == 'D':
        user_task_record.status = 'FAIL'
    else:
        user_task_record.status = 'PASS'
    user_task_record.correct_time = datetime.datetime.now()
    user_task_record.save()
    update_teacher_backlog_is_done(coach['id'], None, request.user.id, student_id, 14)
    task_name = user_task_record.stage_task.task.name
    href = reverse('lps4:student_coach_project', kwargs={'class_id': class_id,
                                                         'stage_task_id': stage_task_id,
                                                         'item_id': 0})
    alert_msg = "老师已给你" + str(task_name) + "的项目制作打了分，<a href='%s'>赶快去看看吧！</a>" % href
    sys_send_message(A_id=0, B_id=student_id, action_type=11, content=alert_msg, action_id=user_task_record.id)

    return success_json()
