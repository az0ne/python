# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from mz_common.lps_version import get_user_study_version
from mz_course.models import CareerCourse
from mz_lps3.decorators import check_student_status
from mz_lps4.class_dict import TRY_CLASS_DICT, LPS4_DICT
from mz_lps4.interface_lps import get_free_task_id_by_class_id

__author__ = 'strii'
import os
import time
import datetime
import logging
from hashlib import md5

from django.http import Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mz_lps3.models import UserKnowledgeItemRecord, UserTaskRecord, KnowledgeItem, Task
from mz_lps.models import ProjectRecord, ProjectRecordImage, Project, Class, ProjectMaterial, ProjectImage
from mz_common.views import file_upload, sys_send_message
from mz_lps3.functions_scf import ClassDyMsgQueue
from mz_lps4.interface import is_lps_class
logger = logging.getLogger('mz_lps3.functions')


@csrf_exempt
@check_student_status
def project_upload_task(request, class_id, stage_task_id, task_id):
    """最终项目提交"""
    return project_upload(request, class_id, stage_task_id, task_id=task_id)


@csrf_exempt
@check_student_status
def project_upload_item(request, class_id, stage_task_id, item_id):
    """知识点项目提交"""
    return project_upload(request, class_id, stage_task_id, item_id=item_id)


# 项目提交
def project_upload(request, class_id, stage_task_id, task_id=None, item_id=None):
    _class = Class.objects.xall().get(id=class_id)
    files = request.FILES.get("project-reset-file", None)
    desc = request.POST.get('desc', '')
    f = request.FILES.get('uploadPreview', None)
    img_urls = request.POST.get('img_urls', None)
    img_record_path = request.POST.get('img_url', None)
    file_path = request.POST.get('file_path', None)
    exist_project_record = False
    try:
        if item_id:
            project_id = KnowledgeItem.objects.get(id=item_id).obj_id
        else:
            task = Task.objects.get(id=task_id)
            project_id = task.project_id
        project = Project.objects.get(id=project_id)

    except Exception as e:
        logger.error(e)
        return JsonResponse({"status": "fail", "message": str(e)})
    try:
        # 重做删除已上传图片
        if img_record_path:
            try:
                image_record_path = os.path.join(settings.MEDIA_ROOT) + "/" + img_record_path
                if os.path.exists(image_record_path):
                    os.remove(image_record_path)
                return JsonResponse({"status": "success"})
            except Exception as e:
                logger.error(e)
                return JsonResponse({"status": "fail", "message": str(e)})
        # 上传图片
        if f:
            # 判断图片格式,大小
            if "*.jpg; *.jpeg; *.png;".find(f.name.split(".")[-1]) == -1:
                return JsonResponse({"status": "fail", "message": "头像必须为JPG/PNG/JPEG格式"})
            if f.size / 1024 > 500:
                return JsonResponse({"status": "fail", "message": "图片大小超过" + "500" + "KB限制"})
            ext = f.name.split('.')[-1]
            image_md5 = md5()
            image_md5.update(str(f) + str(time.time()))
            file_relative_path = '/'.join((create_or_find_dir(), image_md5.hexdigest()))
            file_path = '/'.join((settings.MEDIA_ROOT, file_relative_path))
            image_file = open(file_path + '.' + ext, 'wb')
            image = f.read()
            image_file.write(image)
            image_file.close()
            img_url = file_relative_path + '.' + ext

            return JsonResponse({"status": "success", "img_url": img_url})
        # 上传项目制作
        if files:
            # 上传文件
            result = file_upload(files, 'project')
            if result[0]:
                return JsonResponse({"status": "success", "file_path": result[2]})
            return JsonResponse({"status": "fail", "message": str(result[1])})
        # 上传项目描述
        if desc and img_urls and file_path:
            desc = desc.strip()
            if not file_path:
                return JsonResponse({'status': 'fail', 'message': '文件不能为空'})
            elif not img_urls:
                return JsonResponse({'status': 'fail', 'message': '图片不能为空'})
            elif not desc:
                return JsonResponse({'status': 'fail', 'message': '描述不能为空'})

            try:
                project_record = ProjectRecord.objects.get(project=project, student=request.user,
                                                           examine_id=project.examine_ptr_id)
                exist_project_record = True
            except ProjectRecord.DoesNotExist:
                project_record = ProjectRecord()
                project_record.student = request.user
                project_record.examine_id = project.examine_ptr_id
                project_record.project = project
                project_record.save()
            # 如果已经上传，先删除对应的文件后再执行更新操作
            if exist_project_record:
                if project_record.upload_file:
                    project_record_path = os.path.join(settings.MEDIA_ROOT) + "/" + str(project_record.upload_file)
                    if os.path.exists(project_record_path):
                        os.remove(project_record_path)

            project_record.desc = desc
            project_record.upload_file = file_path
            project_record.save()
            if exist_project_record:
                ProjectRecordImage.objects.filter(project_record=project_record).delete()
            img_list = img_urls.split(',')
            for img in img_list:
                if img:
                    img_record = ProjectRecordImage()
                    img_record.project_record = project_record
                    img_record.image = img
                    img_record.save()
            is_lps4_project = False  # 是否是4.0项目制作
            # 更改项目制作为完成状态
            user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=request.user.id,
                                                          stage_task_id=stage_task_id)
            if item_id:
                item_record = UserKnowledgeItemRecord.objects.get(
                    class_id=class_id, student_id=request.user.id,
                    knowledge_item_id=item_id, user_task_record=user_task_record)
                item_record.status = 'DONE'
                item_record.done_time = datetime.datetime.now()
                item_record.save()
            else:
                guide_task_id = _class.career_course.lps3_guide_task_id
                # lps3.1 试学班的免费任务自动修改
                free_task_ids = []
                # 如果class_id在lps3.1免费班字典里
                if int(class_id) in TRY_CLASS_DICT.values():
                    free_task_ids = get_free_task_id_by_class_id(class_id)

                if user_task_record.stage_task.task.id in [guide_task_id, settings.GUIDE_TASK_ID] + free_task_ids:
                    user_task_record.status = 'PASS'
                    user_task_record.score = 'A'
                    project_record.remark = ''
                    project_record.save()
                else:
                    user_task_record.status = 'DONE'
                    is_lps4_project = True
                user_task_record.done_time = datetime.datetime.now()
                user_task_record.save()
            is_lps4 = is_lps_class(class_id)
            # 4.0的班级提交需要评分的项目制作
            try:
                # app推送消息
                if not item_id:
                    if _class.class_type == Class.CLASS_TYPE_NORMAL:
                        msg_count = '恭喜你已经完成了任务%s，请等待老师为你打分' % task.name
                        sys_send_message(0, request.user.id, 15, msg_count, user_task_record.id)
                # 给对应带班老师推送消息
                if is_lps4:
                    href = reverse('home:teacher:onevone_service')
                else:
                    href = 'http://www.maiziedu.com/lps3/teacher/class/%s/' % str(class_id)
                project_name = project.title

                avatar_html = '<img class="avatar" src="{}">'.format(
                    settings.MEDIA_URL+str(request.user.avatar_small_thumbnall))

                alert_msg = str(request.user.nick_name) + "已上传了" + \
                    str(project_name) + "的项目制作，<a href='%s'>赶快去看看吧</a>！" % href
                alert_msg = avatar_html + '<p>{}</p>'.format(alert_msg)

                for teacher in _class.teachers.all():
                    sys_send_message(0, teacher.id, 51, alert_msg)
                # 记录班级动态消息
                message = dict(user_id=request.user.id,
                               nick_name=request.user.real_name if request.user.real_name else request.user.nick_name,
                               avatar_url=request.user.avatar_url.url,
                               message='提交了项目%s' % str(project_name),
                               time=datetime.datetime.now())
                ClassDyMsgQueue.push(class_id, ClassDyMsgQueue.format_message(message))
            except Exception as e:
                # print e
                pass
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail", "message": "上传失败请重新上传"})
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status": "fail", "message": str(e)})


def create_or_find_dir():
    cur_time = datetime.datetime.now()
    try:
        file_path = '/'.join((settings.MEDIA_ROOT, 'Project/ProjectRecordImage', cur_time.strftime('%Y'),
                              cur_time.strftime('%m')))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return '/'.join(('Project/ProjectRecordImage', cur_time.strftime('%Y'), cur_time.strftime('%m')))
    except Exception as e:
        logger.error(e)
        return False


@check_student_status
def get_project_task(request, class_id, stage_task_id):
    """task项目制作页面"""
    try:
        class_id = int(class_id)
        stage_task_id = int(stage_task_id)
    except ValueError:
        raise Http404
    if class_id <= 0 or stage_task_id <= 0:
        raise Http404

    is_task = 1
    usertask = get_object_or_404(
        UserTaskRecord, class_id=class_id, student_id=request.user.id, stage_task_id=stage_task_id)
    task_id = usertask.stage_task.task.id
    project_id = usertask.stage_task.task.project_id
    project = Project.objects.get(id=project_id)
    has_upload = False
    if ProjectRecord.objects.filter(project=project, student=request.user, examine_id=project.examine_ptr_id).exists():
        if ProjectRecord.objects.get(project=project, student=request.user, examine_id=project.examine_ptr_id).desc:
            has_upload = True
            if usertask.status == 'DOING':
                _class = Class.objects.xall().get(id=class_id)
                guide_task_id = _class.career_course.lps3_guide_task_id
                # lps3.1 试学班的免费任务自动修改
                free_task_ids = []
                # 如果class_id在lps3.1免费班字典里
                if class_id in TRY_CLASS_DICT.values():
                    free_task_ids = get_free_task_id_by_class_id(class_id)
                if usertask.stage_task.task_id in [guide_task_id, settings.GUIDE_TASK_ID] + free_task_ids:
                    usertask.status = 'PASS'
                    usertask.score = 'A'
                else:
                    usertask.status = 'DONE'
                usertask.done_time = datetime.datetime.now()
                usertask.save()

    if LPS4_DICT.get(int(class_id)) and not has_upload:
        return redirect(reverse('lps4:student_coach_project', kwargs={'class_id': class_id,
                                                                      'stage_task_id': stage_task_id,
                                                                      'item_id': 0}))
    if not has_upload:
        from mz_lps3.functions_nj import TaskKnowledgeInterface
        cclass = request.cclass
        iface = TaskKnowledgeInterface(class_id, stage_task_id, class_type=cclass.class_type)
        iface.load_student_data(request.user.id)

        if not iface.all_items_have_done(request.user.id):
            raise Http404
    # 获取项目素材，项目图片示例,项目描述,项目示例视频
    project_material = ProjectMaterial.objects.filter(project=project)
    project_image = ProjectImage.objects.filter(project=project)
    project_desc = project.description
    video = project.video_guide

    is_score = True if usertask.status in ("PASS", "FAIL") else False
    # is_refresher = True if usertask.status == 'REDOING' else False
    from mz_lps3.views_student import render_study_right_item_list_div
    html_usertask_item_list = render_study_right_item_list_div(
        request, class_id, request.user.id, stage_task_id)

    _type = get_user_study_version(request.user.id)
    task = get_object_or_404(Task, stagetaskrelation__id=stage_task_id)
    career = get_object_or_404(CareerCourse, class__id=class_id)
    return render(
        request, "mz_lps3/student/study_project.html",
        {'materials': project_material, 'images': project_image, 'project_desc': project_desc,
         'video': video, 'is_score': is_score, 'is_task': is_task, 'class_id': int(class_id),
         'obj_id': task_id, 'project_title': project.title, 'stage_task_id': stage_task_id,
         'html_usertask_item_list': html_usertask_item_list, 'has_upload': has_upload,
         'student_class': request.cclass,
         'is_lps4': is_lps_class(class_id),
         'trace_pay_type': _type['pay_type'],
         'trace_user_type': _type['user_type'],
         'trace_taskball_name': task.name,
         'trace_career_name': career.name,
         'trace_project_name': project.title,
         }
    )


@check_student_status
def get_project_item(request, class_id, stage_task_id, item_id):
    """item项目制作页面"""
    user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=request.user.id,
                                                  stage_task_id=stage_task_id)
    item_record = get_object_or_404(UserKnowledgeItemRecord, student_id=request.user.id, class_id=class_id,
                                    knowledge_item_id=item_id, user_task_record=user_task_record)
    is_score = False
    # is_refresher = False
    is_task = 0
    project_id = item_record.knowledge_item.obj_id
    project = Project.objects.get(id=project_id)
    has_upload = False
    if ProjectRecord.objects.filter(project=project, student=request.user, examine_id=project.examine_ptr_id).exists():
        if ProjectRecord.objects.get(project=project, student=request.user, examine_id=project.examine_ptr_id).desc:
            has_upload = True
            if item_record.status == 'DOING':
                item_record.status = 'DONE'
                item_record.done_time = datetime.datetime.now()
                item_record.save()
    if LPS4_DICT.get(int(class_id)) and not has_upload:
        return redirect(reverse('lps4:student_coach_project', kwargs={'class_id': class_id,
                                                                      'stage_task_id': stage_task_id,
                                                                      'item_id': item_id}))
    # 获取项目素材，项目图片示例,项目描述,项目示例视频
    project_material = ProjectMaterial.objects.filter(project=project)
    project_image = ProjectImage.objects.filter(project=project)
    project_desc = project.description
    video = project.video_guide
    from mz_lps3.views_student import render_study_right_item_list_div
    html_usertask_item_list = render_study_right_item_list_div(
        request, class_id, request.user.id, stage_task_id, item_id)

    _type = get_user_study_version(request.user.id)
    task = get_object_or_404(Task, stagetaskrelation__id=stage_task_id)
    career = get_object_or_404(CareerCourse, class__id=class_id)
    return render(
        request, "mz_lps3/student/study_project.html",
        {'materials': project_material, 'images': project_image, 'project_desc': project_desc,
         'video': video, 'is_score': is_score, 'is_task': is_task, 'class_id': int(class_id),
         'obj_id': item_id, 'project_title': project.title, 'stage_task_id': stage_task_id,
         'html_usertask_item_list': html_usertask_item_list, 'has_upload': has_upload,
         'student_class': request.cclass,
         'is_lps4': is_lps_class(class_id),
         'trace_pay_type': _type['pay_type'],
         'trace_user_type': _type['user_type'],
         'trace_taskball_name': task.name,
         'trace_career_name': career.name,
         'trace_project_name': project.title,
         }
    )


# 查看评分
def task_project_score(request, class_id, task_id):
    result = {}
    try:
        # is_refresher = False
        user_task_record = UserTaskRecord.objects.get(
            class_id=class_id, student_id=request.user.id,
            stage_task__task_id=task_id)

        score = user_task_record.score if user_task_record.score else ''
        # 是否重修
        # if user_task_record.status == 'REDOING':
        #     is_refresher = True
        project_id = Task.objects.get(id=task_id).project_id
        project = Project.objects.get(id=project_id)
        project_record = ProjectRecord.objects.get(project=project, student=request.user,
                                                   examine_id=project.examine_ptr_id)
        project_image = ProjectRecordImage.objects.filter(project_record=project_record)
        img_list = []
        for img in project_image:
            img_list.append(str(img.image))

        result['data'] = {}
        result['status'] = 'success'
        result['data']['score'] = score
        # result['data']['is_refresher'] = is_refresher
        result['data']['image'] = img_list
        result['data']['desc'] = project_record.desc
        result['data']['comment'] = project_record.remark if project_record.remark else ''
        result['data']['file'] = project_record.upload_file.url
        return JsonResponse(result)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status": "fail", "message": str(e)})


# item已上传详情
def item_project_detail(request, class_id, stage_task_id, item_id):
    result = {}
    try:
        # is_refresher = False

        user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=request.user.id,
                                                      stage_task_id=stage_task_id)
        item_record = UserKnowledgeItemRecord.objects.get(student_id=request.user.id, class_id=class_id,
                                                          knowledge_item_id=item_id, user_task_record=user_task_record)

        project_id = item_record.knowledge_item.obj_id
        project = Project.objects.get(id=project_id)
        project_record = ProjectRecord.objects.get(project=project, student=request.user,
                                                   examine_id=project.examine_ptr_id)
        project_image = ProjectRecordImage.objects.filter(project_record=project_record)
        img_list = []
        for img in project_image:
            img_list.append(str(img.image))

        result['data'] = {}
        result['status'] = 'success'
        result['data']['score'] = ''
        # result['data']['is_refresher'] = is_refresher
        result['data']['image'] = img_list
        result['data']['desc'] = project_record.desc
        result['data']['comment'] = ''
        result['data']['file'] = project_record.upload_file.url
        return JsonResponse(result)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status": "fail", "message": str(e)})
