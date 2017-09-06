# -*- coding: utf-8 -*-

__author__ = 'changfu'

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.conf import settings
import logging
import datetime
import requests
from mz_common.models import MyMessage
from mz_user.models import UserProfile
from mz_lps.models import Class
from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord, ClassMeeting,LiveRoom,ClassMeetingVideo
from mz_lps3.functions_nj import get_student_doing_tasks_timeleft
from mz_lps3.functions_gt import get_classmeeting_list,_serialize_classmeeting
from mz_lps3.functions_scf import ClassDyMsgQueue

logger = logging.getLogger('mz_lps3.views')

# space holder for develop test.
# def get_student_doing_tasks_timeleft(user_id, class_id):
#     return [dict(task_id=2, task_name='task2', timeleft=-5),
#             dict(task_id=3, task_name='task3', timeleft=600),
#             dict(task_id=4, task_name='task4', timeleft=25*60*60)]

# space holder for develop test.
# def get_classmeeting_list(class_id, status):
#     return [{'content': 'test1', 'url': 'url-test1', 'startline': datetime.datetime.now()},
#             {'content': 'test2', 'url': 'url-test2', 'startline': datetime.datetime.now()}]

def welcome_message(user_id, class_id, template):
    """
    判断是否首次进入任务面板， 确定是否显示欢迎消息 1.7.1.a
    :param user_id:
    :param clas_id:
    :return:
    """
    try:
        user_name = UserProfile.objects.get(pk=user_id).nick_name
        class_obj = Class.objects.xall().get(pk=class_id)
        message_content = '%s同学你好，欢迎你开始%s课程的学习！学习过程中获得的积分和成就可以直接兑换奖品哟！' \
                          % (user_name, class_obj.career_course.name)
        obj, created = MyMessage.objects.get_or_create(userA=0, userB=user_id, action_type=9,
                                                       action_id=class_id, is_new=False)
        if created:  # message not exists, then, insert such a message and show it to user
            return render_to_string(template, {'message_content': message_content})
    except Exception as msg:
        logger.error(msg)

def class_rank_message(user_id, class_id, template):
    """
    判断是否需要展示班级排名变化， 1.7.1.c/d
    :param user_id:
    :param class_id:
    :param template:
    :return:
    """
    try:
        messages = MyMessage.objects.filter(userB=user_id, action_id=class_id, action_type=10).order_by('-date_action')
        if messages.exists():  # first check if such message exists.
            msg = messages[0]
            if msg.is_new:  # mes is un-read, then show it to user, and update message as read
                msg.is_new = False
                msg.save()
                return render_to_string(template, {'message_content': msg.action_content})
    except Exception as msg:
        logger.error(msg)

def task_schedule_message(user_id, class_id, template):
    """
    判断当前用户任务剩余时间是否小于24h, 如果是，则显示消息给用户。每次刷新任务面板都要显示
    :param user_id:
    :param class_id:
    :param template:
    :return:
    """
    try:
        results = get_student_doing_tasks_timeleft(class_id, user_id)
        if results:
            data = []
            for result in results:
                if 0 <= result['timeleft'] <= 24 * 60 * 60:  # task not expired and left time no more than 24h
                    data.append(render_to_string(template,
                                                 {'message_content': '哎呀，你还剩不到1天时间可完成当前任务%s啦，抓紧学习吧！'
                                                                     % result['task_name']}))
            if data:
                return data
    except Exception as msg:
        logger.error(msg)

@csrf_exempt
@login_required
def global_message(request):
    """
    进入任务面板，确定是否显示全局消息。全局消息按照 a->c/d->e 的顺序检查。
    :param request:
    :return:
    """
    template = 'mz_lps3/student/div_global_message.html'
    if request.method != 'POST':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    user_id = request.user.id
    class_id = request.POST.get('class_id')
    if user_id and class_id:
        data = []
        for sub_func in [welcome_message, class_rank_message]:  # handle welcome message and class rank message
            result = sub_func(user_id, class_id, template)
            data.append(result) if result else ''
        result = task_schedule_message(user_id, class_id, template)  # handle task schedule message
        data.extend(result) if result else ''
        result = True if data else False
        return JsonResponse({'status': result, 'data': data})
    return JsonResponse({'status': False, 'data': 'no enough parameters'})

@login_required
def task_score_message(request):
    """
    进入任务面板，确定是否显示任务分数消息。
    :param request:
    :return:
    """
    template = 'mz_lps3/student/div_task_score.html'
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    user_id = request.user.id
    if user_id:
        try:
            messages = MyMessage.objects.filter(userB=user_id, action_type=11, is_new=True).order_by('date_action')
            if not messages.exists():
                data = {'status': False, 'data': 'No message'}
            else:
                data = {'status': True, 'data': []}
                for each_message in messages:
                    try:
                        user_task = UserTaskRecord.objects.get(pk=each_message.action_id)
                        passed = True if user_task.score in ['S', 'A', 'B', 'C'] else False
                        time_consumption = (user_task.done_time - user_task.created).seconds - user_task.paused_seconds
                        time_excellent = True if time_consumption <= user_task.stage_task.task.excellent_time * 24 * 3600 \
                                              and user_task.score == 'A' else False
                        data['data'].append(render_to_string(template,
                                                              {'task_name': user_task.stage_task.task.name,
                                                               'class_id': user_task.class_id,
                                                               'stage_task_id': user_task.stage_task.pk,
                                                               'passed': passed, 'task_score': user_task.score,
                                                               'time_excellent': time_excellent,
                                                               'gift': user_task.stage_task.task.gift},
                                                              context_instance=RequestContext(request)))
                    except Exception as msg:
                        logger.error(msg)
                messages.update(is_new=False)  # update messages.
        except Exception as msg:
            logger.error(msg)
            data = {'status': False, 'data': str(msg)}
    else:
        data = {'status': False, 'data': 'No enough parameters'}
    return JsonResponse(data)

@login_required
def class_meeting_schedule(request):
    """
    用户在任务面板停留，当班会开始时间在15分钟之内，则弹出该消息
    :param request:
    :return:
    """
    template = 'mz_lps3/student/div_live-start.html'
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    class_id = request.GET.get('class_id')
    user_id = request.user.id
    if class_id and user_id:
        try:
            next_meetings = get_classmeeting_list(class_id, user_id, status=0)
            if not next_meetings:   # this should not happen
                data = {'status': False, 'data': 'No schedule meeting yet'}
            else:
                data = {'status': True, 'data': []}
                index = 0  # TODO: use emunate to use index.
                for next_meeting in next_meetings:
                    if (next_meeting['datetime'] - datetime.datetime.now()).days > 7:
                        # if the latest meeting will not start in one week, then, don't show the message.
                        continue
                    try:
                        left_time = int((next_meeting['datetime'] - datetime.datetime.now()).total_seconds())
                        # if the meeting will start in 15 minutes, then pop the the msg at once.
                        left_time = 0 if 0 < left_time <= 15 * 60 else left_time - 15 * 60 #郭涛 修改过期班会还要提醒的BUG
                        # construct class meeting join url
                        #
                        # meeting_url = '%s?nickname=%s&token=%s' % (next_meeting['join_url'], next_meeting['nick_name'],
                        #                                            next_meeting['token'])
                        html = render_to_string(template, {'class_name': Class.objects.xall().get(pk=class_id).coding,
                                                           'meeting_content': next_meeting['content'],
                                                           'meeting_url': next_meeting['join_url'], 'index': index},
                                                context_instance=RequestContext(request))
                        data['data'].append({'left_time': left_time, 'html': html})
                        index += 1
                    except Exception as msg:
                        logger.error(msg)
        except Exception as msg:
            logger.error(msg)
            data = {'status': False, 'data': str(msg)}
    else:
        data = {'status': False, 'data': 'No enough parameters'}
    return JsonResponse(data)


@login_required
def update_learning_lesson(request, user_knowledge_item_id):
    """
    used for LPS3.0
    :param user_knowledge_item_id:
    :return:
    """
    if request.method != 'GET':
        JsonResponse({'status': False, 'data': 'wrong method'})
    try:
        user_knowledge_item = UserKnowledgeItemRecord.objects.select_related().get(pk=user_knowledge_item_id)
        if user_knowledge_item.status == 'DOING':
            user_knowledge_item.status, user_knowledge_item.done_time = 'DONE', datetime.datetime.now()
            user_knowledge_item.save()
            # 记录班级动态消息
            message = dict(user_id=request.user.id,
                           nick_name=request.user.real_name if request.user.real_name else request.user.nick_name,
                           avatar_url=request.user.avatar_url.url,
                           message='已经学习了%s' % user_knowledge_item.knowledge_item.name,
                           time=datetime.datetime.now())
            ClassDyMsgQueue.push(user_knowledge_item.class_id, ClassDyMsgQueue.format_message(message))
    except Exception, e:
        # print e
        logger.error(e)
        return JsonResponse({"status": False, 'data': str(e)})
    return JsonResponse({"status": True})

def head_user_info(request, user_id):
    """
    user head info from FPS
    :param request:
    :param user_id:
    :return:
    """
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    template = 'mz_lps3/student/div_fps_header.html'
    try:
        user_info_data = requests.get(url='%scommon/ajax/header_userinfo/%s/' % (settings.FPS_HOST, user_id),
                                 timeout=2)
        user_info = user_info_data.json().get('data')
        if not user_info_data.json().get('status'):
            logger.error(user_info)  # record error if fail
        return JsonResponse({'status': True, 'data': render_to_string(template, {'userinfo': user_info},
                                                                      context_instance=RequestContext(request))})
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': False, 'data': str(e)})

@login_required
def class_meeting_open_message(request):
    """
    进入任务面板，确定是否显示班会开始提醒。
    :param request:
    :return:
    """
    template = 'mz_lps3/student/div_class_meeting_open.html'
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    user_id = request.user.id
    if user_id:
        try:
            messages = MyMessage.objects.filter(userB=user_id, action_type=12, is_new=True).order_by('date_action')
            if not messages.exists():
                data = {'status': False, 'data': 'No message'}
            else:
                data = {'status': True, 'data': []}
                for each_message in messages:
                    try:
                        class_meeting = ClassMeeting.objects.get(pk=each_message.action_id)
                        user=UserProfile.objects.get(pk=user_id)
                        if class_meeting.startline <= datetime.datetime.now() <= class_meeting.finish_date:
                            #序列化班会信息
                            classmeeting=_serialize_classmeeting(class_meeting,user)
                            data['data'].append(render_to_string(template,
                                                                  {'classmeeting': classmeeting},
                                                                  context_instance=RequestContext(request)))
                    except Exception as msg:
                        logger.error(msg)
                messages.update(is_new=False)  # update messages.
        except Exception as msg:
            logger.error(msg)
            data = {'status': False, 'data': str(msg)}
    else:
        data = {'status': False, 'data': 'No enough parameters'}
    return JsonResponse(data)

@login_required
def class_meeting_absence_message(request):
    """
    进入任务面板，确定是否显示班会缺勤提醒。
    :param request:
    :return:
    """
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    class_id = request.GET.get('class_id')
    user_id = request.user.id
    if user_id:
        try:
            messages = MyMessage.objects.filter(userB=user_id, action_type=13, is_new=True).order_by('date_action')
            if not messages.exists():
                data = {'status': False, 'data': 'No message'}
            else:
                data = {'status': True, 'data': []}
                for each_message in messages:
                    try:
                        class_meeting = ClassMeeting.objects.get(pk=each_message.action_id)
                        setattr(class_meeting,'video',None)
                        #有录制的视频记录
                        live_room=LiveRoom.objects.filter(class_meeting=class_meeting)
                        if live_room.count()>0:
                            class_meeting_video_lst=ClassMeetingVideo.objects.filter(class_id=class_id,live_id=live_room[0].live_id)
                            if class_meeting_video_lst.count()>0:
                                setattr(class_meeting,'video',class_meeting_video_lst[0])

                        if class_meeting.video:
                            template = 'mz_lps3/student/div_class_meeting_absence.html'
                        else:
                            template = 'mz_lps3/student/div_class_meeting_absence_1.html'

                        data['data'].append(render_to_string(template,
                                                              {'class_meeting': class_meeting,
                                                               'class_id':class_id},
                                                              context_instance=RequestContext(request)))
                    except Exception as msg:
                        logger.error(msg)
                messages.update(is_new=False)  # update messages.
        except Exception as msg:
            logger.error(msg)
            data = {'status': False, 'data': str(msg)}
    else:
        data = {'status': False, 'data': 'No enough parameters'}
    return JsonResponse(data)

@require_GET
@login_required
def finished_task_record(request, class_id, student_id):
    """
    已完成的任务列表
    :param request:
    :param class_id:
    :param student_id:
    :return:
    """
    template = 'mz_lps3/student/div_student_task_record.html'
    score_to_number_score = {
        'A': 3,
        'B': 2,
        'C': 1,
        'D': 0
    }
    nick_name, avatar_url = UserProfile.objects.values_list('nick_name', 'avatar_url').get(id=student_id)
    task_records = UserTaskRecord.objects.select_related().\
        filter(class_id=class_id, student_id=student_id, status__in=['PASS', 'FAIL']).order_by('done_time')
    format_records = [dict(task_name=record.stage_task.task.name,
                           score=record.score,
                           number_score=score_to_number_score[record.score]*10)
                      for record in task_records]

    def calc_level(score='A'):
        return len(filter(lambda x: True if x['score'] == score else False, format_records))

    total_a, total_b, total_c, total_d = calc_level('A'), calc_level('B'), calc_level('C'), calc_level('D')
    total_number_score = reduce(lambda x, y: x + y, [r['number_score'] for r in format_records] or [0])
    total_tasks = len(format_records)
    fps_center = settings.FPS_CENTER
    MEDIA_URL = settings.MEDIA_URL
    html = render_to_string(template, locals())
    return JsonResponse(dict(status=True, data=html))

# @require_GET
# @login_required
def class_dynamic_message(request):
    """

    :param request:
    :return:
    """
    class_id = request.GET.get('class_id')
    timestampe = request.GET.get('timestampe')
    if not class_id or not timestampe:
        return JsonResponse(dict(status=False, message='No enough parameters'))
    messages = ClassDyMsgQueue.get(class_id)
    if float(timestampe) != 0:  # 如果时戳不为0,则过滤
        messages = filter(lambda x: True if x['timestampe'] > float(timestampe) else False, messages)
    timestampe = messages[-1]['timestampe'] if messages else timestampe
    return JsonResponse(dict(status=True, data=messages, timestampe=timestampe))

