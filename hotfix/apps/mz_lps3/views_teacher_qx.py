# -*- coding: utf-8 -*-
import logging

from django.core.urlresolvers import reverse
from django.http.response import Http404
import requests
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from mz_lps3.models import UserKnowledgeItemRecord, UserTaskRecord, UserGiftRecord, StudyHistory
from mz_lps.models import ProjectRecord, ProjectRecordImage, Project, Class
from mz_common.decorators import teacher_required
from mz_common.views import sys_send_message
from utils.sms_manager import send_sms, get_templates_id
from mz_user.models import ClassStudentDynamic, UserProfile
from mz_lps3.functions_scf import ClassDyMsgQueue
from mz_lps4.interface import is_lps_class
from utils.logger import logger as log
logger = logging.getLogger('mz_lps3.views')


def student_task_div(request, class_id, student_id, stage_task_id):
    """
    学生任务详情|给学生任务打分 弹出层
    :param class_id:班级id
    :param student_id: 学生id
    :param stage_task_id: 阶段任务唯一 id
    """
    user_task_record = UserTaskRecord.objects.get(
        class_id=class_id, student_id=student_id,
        stage_task_id=stage_task_id)

    # 是否打过分
    is_marking = True
    if user_task_record.status == 'DONE':
        is_marking = False
    project_id = user_task_record.stage_task.task.project_id
    project = Project.objects.get(id=project_id)
    project_record = ProjectRecord.objects.get(project=project, student_id=student_id,
                                               examine_id=project.examine_ptr_id)
    project_image = ProjectRecordImage.objects.filter(project_record=project_record)

    try:
        class_id = int(class_id)
    except:
        logger.warn('class_id is not a int')
        raise Http404
    if Class.objects.xall().filter(id=class_id, class_type=Class.CLASS_TYPE_FREE_488, lps_version='3.0').exists():
        return render(request, "mz_lps3_free/teacher/div_student_task.html", locals())

    return render(request, "mz_lps3/teacher/div_student_task.html", locals())


def student_item_project_div(request, class_id, student_id, stage_task_id, item_id):
    """
    学生的 item--project详情
    """
    user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=student_id,
                                                  stage_task_id=stage_task_id)
    item_record = UserKnowledgeItemRecord.objects.get(student_id=student_id, class_id=class_id,
                                                      knowledge_item_id=item_id, user_task_record=user_task_record)
    project_id = item_record.knowledge_item.obj_id
    project = Project.objects.get(id=project_id)
    project_record = ProjectRecord.objects.get(project=project, student_id=student_id,
                                               examine_id=project.examine_ptr_id)
    project_image = ProjectRecordImage.objects.filter(project_record=project_record)
    return render(request, "mz_lps3/teacher/div_student_item_project.html", locals())


@csrf_exempt
@teacher_required
def set_course_project_score(request, class_id, student_id, stage_task_id):
    """
    给项目制作打分
    """
    score = request.POST.get('score', None)
    comment = request.POST.get('desc', '').strip()
    try:
        if not comment:
            return JsonResponse({'status': 'fail', 'message': '评语不能为空'})
        user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=student_id,
                                                      stage_task_id=stage_task_id)
        project = Project.objects.get(id=user_task_record.stage_task.task.project_id)
        project_record = ProjectRecord.objects.get(project=project, student_id=student_id,
                                                   examine_id=project.examine_ptr_id)

        user_task_record.score = score
        if score == 'D':
            user_task_record.status = 'FAIL'
        else:
            user_task_record.status = 'PASS'
        user_task_record.save()
        log.info("updated user_task_record "
                "class_id:%s student_id:%s stage_task_id:%s score：%s update_time:%s" % (
                    class_id,
                    student_id,
                    stage_task_id,
                    score,
                    datetime.datetime.now()))
        project_record.remark = comment
        project_record.save()

        # 更新老师已经完成项目制作打分的提醒
        is_lps4 = is_lps_class(class_id)

        project_mark_number = UserTaskRecord.objects.filter(class_id=class_id, student_id=student_id, status='DONE').\
            count()

        task = user_task_record.stage_task.task
        from functions_nj import calc_done_type
        done_type = calc_done_type(
            user_task_record.created, user_task_record.done_time,
            task.expect_time, task.excellent_time, user_task_record.paused_seconds)
        if done_type == 'quickly' and task.gift and user_task_record.score == 'A':  # 提前完成
            try:
                gift_record = UserGiftRecord()
                gift_record.student_id = student_id
                gift_record.class_id = class_id
                gift_record.gift = task.gift
                gift_record.save()
            except:
                pass   # 防止获取重复礼物
        if done_type == 'quickly' and user_task_record.status == 'PASS':
            try:
                requests.put(url=settings.FPS_HOST + 'service/ticket/', data={
                    'user_id': student_id, 'op_type': 'task_finish_on_time'}, timeout=2)
            except Exception as e:
                logger.error(e)
        # 给学员推送消息,加入学员动态：老师给项目制作打分
        student = UserProfile.objects.get(id=student_id)
        try:
            task_name = user_task_record.stage_task.task.name
            if is_lps4:
                href = reverse('lps4_index', kwargs={"career_id": is_lps4})
            else:
                href = 'http://www.maiziedu.com/lps3/student/class/%s' % class_id
            alert_msg = "老师已给你" + str(task_name) + "的项目制作打了分，<a href='%s'>赶快去看看吧！</a>" % href
            sys_send_message(A_id=0, B_id=student_id, action_type=11, content=alert_msg, action_id=user_task_record.id)

            if user_task_record.score != 'D':
                if student.mobile and student.valid_mobile == 1:
                    try:
                        send_sms.delay(settings.SMS_APIKEY,
                                 get_templates_id('studying_score_abc'),
                                 int(student.mobile),
                                 user_task_record.score.encode('utf-8'),
                                 task_name.encode('utf-8'),
                                 user_task_record.score.encode('utf-8')
                                 )
                    except Exception, e:
                        logger.error(e)
                try:
                    study_history = StudyHistory()
                    study_history.student_id = student_id
                    study_history.class_id = class_id
                    study_history.content = '我提交了%s的作业，得到评分%s' % (task_name, user_task_record.score)
                    study_history.save()
                except:
                    pass
            else:
                if student.mobile and student.valid_mobile == 1:
                    try:
                        send_sms.delay(settings.SMS_APIKEY,
                                 get_templates_id('studying_score_d'),
                                 int(student.mobile),
                                 user_task_record.score.encode('utf-8'),
                                 task_name.encode('utf-8'))
                    except Exception, e:
                        logger.error(e)
            # params = dict(user=UserProfile.objects.get(id=student_id), type=3)
            # ClassStudentDynamic.objects.get_or_create(**params)
        except Exception as e:
            logger.error(e)
        # 记录班级动态消息
        message = dict(user_id=student.id,
                       nick_name=student.real_name if student.real_name else student.nick_name,
                       avatar_url=student.avatar_url.url,
                       message='在任务%s获得了%s评分' % (user_task_record.stage_task.task.name, score),
                       time=datetime.datetime.now())
        ClassDyMsgQueue.push(class_id, ClassDyMsgQueue.format_message(message))
        return JsonResponse({'status': 'success', 'number': project_mark_number})
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'fail', 'message': str(e)})
