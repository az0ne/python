# -*- coding: utf-8 -*-
__author__ = 'guotao'
import datetime,json
from django.shortcuts import render
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import functions
from mz_lps.models import Class, ClassStudents
from mz_lps3.models import ClassMeeting, ClassMeetingRelation
from mz_common.decorators import teacher_required
from mz_common.views import sys_send_message
from celery_tasks import app


@csrf_exempt
@teacher_required
def create_classmeeting(request):
    """
    创建班会
    :param request:
    :return:
    """
    try:
        if request.method == 'POST':
            valid_msg = None
            user = request.user
            content = request.POST.get('subject', '').strip()
            data = request.POST.get('date', '')
            time = request.POST.get('time', '')
            join_class = request.POST.get('joinClass', '')
            if content == '':
                valid_msg = '班会主题不能为空!'
            if data == '' or time == '':
                valid_msg = '班会开始时间不能为空!'
            if join_class == '':
                valid_msg = '班会关联的班级不能为空!'
            if valid_msg:
                return HttpResponse(json.dumps({'status': 'failure','msg':valid_msg}), content_type="application/json")
            result=functions.create_classmeeting(user,content,data,time,join_class)
            if result:
                # 班会消息
                join_class_lst = join_class.split(',')
                class_meeting_message.delay(join_class_lst, data, time, 18)
                # class_meeting_message(join_class_lst, data, time, 18)  # 传的班级code
                return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': 'failure','msg':'创建班会失败，可能选择的班级已经不存在！'}), content_type="application/json")
    except Exception as e:
        # print e
        return HttpResponse(json.dumps({'status': 'failure','msg':'创建班会失败，请检查输入后重试！'}), content_type="application/json")

@csrf_exempt
@teacher_required
def get_classmeeting(request,classmeeting_id):
    try:
        classmeeting=ClassMeeting.objects.get(id=classmeeting_id)
    except:
        raise Http404
    setattr(classmeeting,'d_date',classmeeting.startline.strftime('%Y/%m/%d'))
    setattr(classmeeting,'d_time',classmeeting.startline.strftime('%H:%M'))
    class_coding_lst=[]
    classmeetingrelation_lst=classmeeting.classmeetingrelation_set.all()
    for classmeetingrelation_obj in classmeetingrelation_lst:
        try:
            class_obj = Class.objects.xall().get(id=classmeetingrelation_obj.class_id,lps_version='3.0')
            class_coding_lst.append(class_obj.coding)
        except:
            pass
    setattr(classmeeting,'class_coding_lst',class_coding_lst)
    #写入数据库
    return render(request,'mz_lps3/teacher/div_alter_class_meeting.html',locals())

@csrf_exempt
@teacher_required
def alter_classmeeting(request,classmeeting_id):
    try:
        if request.method == 'POST':
            classmeeting_id = int(classmeeting_id)
            valid_msg = None
            # user = request.user
            content = request.POST.get('subject', '')
            data = request.POST.get('date', '')
            time = request.POST.get('time', '')
            # if content == '':
            #     valid_msg = '班会主题不能为空!'
            if data == '' or time == '':
                valid_msg = '班会开始时间不能为空!'
            if valid_msg:
                return HttpResponse(json.dumps({'status': 'failure','msg':valid_msg}), content_type="application/json")
            result=functions.alter_classmeeting(classmeeting_id,data,time,content)
            if result:
                meeting_relation_list = ClassMeetingRelation.objects.filter(class_meeting_id=classmeeting_id)
                join_class_lst = [meeting_relation.class_id for meeting_relation in meeting_relation_list]
                class_meeting_message.delay(join_class_lst, data, time, 19)
                # class_meeting_message(join_class_lst, data, time, 19)
                return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': 'failure','msg':'没有找的班会ID，可能已经删除！'}), content_type="application/json")
    except Exception as e:
        # print e
        return HttpResponse(json.dumps({'status': 'failure','msg':'修改班会失败，请检查输入后重试！'}), content_type="application/json")


@app.task(name='views_teacher.class_meeting_message')
def class_meeting_message(join_class_lst, date, time, message_type):
    date_time = date + ' ' + time
    if message_type == 18:
        content = '你的老师创建了新的班会计划，时间是%s，记得准时参加哦' % date_time
        class_students_lst = ClassStudents.objects.filter(student_class__coding__in=join_class_lst, is_pause=False,
                                                          status=ClassStudents.STATUS_NORMAL)
    else:
        content = '你的老师更改了班会时间，时间是%s，记得准时参加哦' % date_time
        class_students_lst = ClassStudents.objects.filter(student_class_id__in=join_class_lst, is_pause=False,
                                                          status=ClassStudents.STATUS_NORMAL)
    for class_student in class_students_lst:
        if not class_student.is_active:
            continue
        sys_send_message(0, class_student.user.id, message_type, content)
    return True
