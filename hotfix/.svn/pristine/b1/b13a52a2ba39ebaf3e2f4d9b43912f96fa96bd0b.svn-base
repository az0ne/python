# -*- coding: utf-8 -*-
__author__ = 'guotao'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()
import logging, datetime, urllib, urllib2, json
from django.conf import settings
from collections import OrderedDict
from django.shortcuts import get_object_or_404, Http404
from utils.tool import generate_random
from mz_user.models import UserProfile
from mz_lps.models import Class, ClassStudents
from django.db.models import Q
from mz_lps3.models import ClassMeeting, ClassMeetingVideo, LiveRoom, ClassMeetingAttendance, ClassMeetingRelation, \
    StudyHistory
from functions_nj import get_class_students_full_payment
from mz_course.views import sys_send_message
from mz_pay.models import UserPurchase

logger = logging.getLogger('mz_lps3.functions')
# ---学生端--------------------------------------------------------------------------------------------------------------
def get_weekday(weekday_int):
    week_dict = {0: '星期一',
                 1: '星期二',
                 2: '星期三',
                 3: '星期四',
                 4: '星期五',
                 5: '星期六',
                 6: '星期天', }

    return week_dict.get(weekday_int, '')


def get_classmeetings_by_class_id(class_id):
    """
    学生端获取班会历史
    :param class_id 班级ID
    :return dict  eg:{year:{month:[video1,video2]}}
    """
    class_videos = ClassMeetingVideo.objects.filter(class_id=class_id).order_by('-create_time')
    video_dict = OrderedDict()
    for video in class_videos:
        year = video.create_time.year
        month = video.create_time.month
        setattr(video, 'd_week', get_weekday(video.create_time.weekday()))
        setattr(video, 'd_date', video.create_time.strftime("%m-%d"))
        setattr(video, 'd_time', video.create_time.strftime("%H:%M"))
        try:
            video.play_subject = LiveRoom.objects.get(live_id=video.live_id).class_meeting.content
        except LiveRoom.DoesNotExist:
            pass
        if video_dict.has_key(year):
            if video_dict[year].has_key(month):
                video_dict[year][month].append(video)
            else:
                video_dict[year][month] = [video]
        else:
            video_dict[year] = OrderedDict({month: [video]})

    return video_dict


def get_class_video_by_play_id(class_id, play_id):
    """
    根据ID播放班会视频
    :param play_id 播放ID
    :return
    """
    class_video = get_object_or_404(ClassMeetingVideo, play_id=play_id, class_id=class_id)
    try:
        _class = Class.objects.xall().get(id=class_video.class_id)
    except Class.DoesNotExist:
        raise Http404
    career_course_name = _class.career_course.name
    setattr(class_video, 'career_course_name', career_course_name)
    return class_video


def get_classmeeting_list(class_id, user_id, **kwargs):
    """
    根据班会以及状态，返还班会数据列表
    :param class_id:
    :param kwargs:
    :return: [{id:'',content:'',d_week:'',d_date:'',d_time:'',status:'',datetime:'',join_url:'',token:'',nick_name,''},]
    """
    user = get_object_or_404(UserProfile, id=user_id)
    if kwargs.has_key('status') and kwargs.get('status') == 0:  # 返还最近未开始的班会
        class_meeting_lst = ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id).exclude(status=1). \
                                order_by('startline')[:2]
    else:  # 构建未结束的班会数据
        class_meeting_lst = ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id).exclude(status=1). \
                                order_by('startline')[:5]
    classmeeting_lst = []
    for class_meeting in class_meeting_lst:
        classmeeting_lst.append(_serialize_classmeeting(class_meeting, user))
    return classmeeting_lst


def _serialize_classmeeting(data_obj, user):
    """
    序列化班会数据
    :param data_obj:
    :return:
    """
    data_dict = {}
    try:
        startline = data_obj.startline
        data_dict['id'] = data_obj.id
        data_dict['content'] = data_obj.content
        data_dict['datetime'] = startline
        data_dict['d_week'] = get_weekday(startline.weekday())
        data_dict['d_date'] = startline.strftime("%m-%d")
        data_dict['d_time'] = startline.strftime("%H:%M")
        data_dict['status'] = data_obj.status
        live_room_lst = LiveRoom.objects.filter(class_meeting=data_obj)
        data_dict['nick_name'] = user.real_name if user.real_name else user.nick_name
        data_dict['join_url'] = ''
        data_dict['room_number'] = ''
        if live_room_lst:
            if user.is_teacher():
                values = {'nickname': data_dict['nick_name'], 'token': live_room_lst[0].teacher_token}
                data_dict['join_url'] = live_room_lst[0].teacher_join_url + '?' + urllib.urlencode(values)
                data_dict['token'] = live_room_lst[0].teacher_token
            else:  # 大班课学生端以助教身份进入
                values = {'nickname': data_dict['nick_name'], 'token': live_room_lst[0].assistant_token}
                data_dict['join_url'] = live_room_lst[0].teacher_join_url + '?' + urllib.urlencode(values)
                data_dict['token'] = live_room_lst[0].assistant_token
            data_dict['room_number'] = live_room_lst[0].live_code

    except Exception, e:
        # print(e)
        logger.error(e)
    return data_dict


# ---老师端-------------------------------------------------------------------------------------------------------------

def get_teacher_classmeetings_by_class_id(class_id):
    """
    老师获取班会历史记录
    :param class_id 班级ID
    :return dict  eg:{year:{month:[video1,video2]}}
    """
    class_meeting_lst = ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id, status=1).order_by(
        '-startline')
    class_meeting_dict = OrderedDict()
    for class_meeting in class_meeting_lst:
        year = class_meeting.startline.year
        month = class_meeting.startline.month
        setattr(class_meeting, 'd_week', get_weekday(class_meeting.startline.weekday()))
        setattr(class_meeting, 'd_date', class_meeting.startline.strftime("%m-%d"))
        setattr(class_meeting, 'd_time', class_meeting.startline.strftime("%H:%M"))
        # 通过live_id,查询出是否有视频
        setattr(class_meeting, 'video', None)
        # 如果是临时班会，每次班会对应一个直播室，，所以通过Live_ID可以找到最多一个视频记录
        live_room = LiveRoom.objects.filter(class_meeting=class_meeting)
        if live_room.count() > 0:
            class_meeting_video_lst = ClassMeetingVideo.objects.filter(class_id=class_id, live_id=live_room[0].live_id)
            if class_meeting_video_lst.count() > 0:
                setattr(class_meeting, 'video', class_meeting_video_lst[0])
        # 组织结构
        if class_meeting_dict.has_key(year):
            if class_meeting_dict[year].has_key(month):
                class_meeting_dict[year][month].append(class_meeting)
            else:
                class_meeting_dict[year][month] = [class_meeting]
        else:
            class_meeting_dict[year] = OrderedDict({month: [class_meeting]})

    return class_meeting_dict


def get_attendance_info(class_meeting, class_id=None, is_update=True):
    """
    获取考勤信息
    :param class_id: 制定班级ID（不制定表示即:是所有班会缺勤人数）
    :param classmeeting_id:
    :return:
    """
    # #获取当前班会包含的班级
    if class_id == None:
        class_id_lst = ClassMeetingRelation.objects.filter(class_meeting=class_meeting).values_list("class_id",
                                                                                                    flat=True)
    else:
        class_id_lst = [class_id]
    # if ClassMeetingAttendance.objects.filter(class_meeting_id=class_meeting.id).count()==0:
    #     #更新当前班会的考勤数据
    if is_update:
        update_attendance_info(class_meeting)
    # 准时的
    punctual_user_lst = []
    punctual_lst = ClassMeetingAttendance.objects.filter(class_meeting_id=class_meeting.id, status='punctual')
    for punctual in punctual_lst:
        user = UserProfile.objects.filter(id=punctual.student_id)
        if user:
            punctual_user_lst.append(user[0])
    # 迟到的
    late_user_lst = []
    late_lst = ClassMeetingAttendance.objects.filter(class_meeting_id=class_meeting.id, status='late')
    for late in late_lst:
        user = UserProfile.objects.filter(id=late.student_id)
        if user:
            late_user_lst.append(user[0])
    # 缺勤的
    absent_user_lst = []
    # 缺勤的class_students
    class_student_lst = ClassStudents.objects.filter(student_class_id__in=class_id_lst, is_pause=False,
                                                     status=ClassStudents.STATUS_NORMAL).exclude(
        user__in=punctual_user_lst).exclude(user__in=late_user_lst)
    for class_student in class_student_lst:
        absent_user_lst.append(class_student.user)

    return punctual_user_lst, late_user_lst, absent_user_lst, class_student_lst


def get_classcoding_lst(class_id):
    """
    获取3.0下所以班的班级coding
    :return:
    """
    class_lst = []
    class_set = Class.objects.xall().filter(status=1, is_active=True, lps_version='3.0').exclude(id=class_id)
    for class_obj in class_set:
        class_lst.append(class_obj.coding)
    return class_lst


def create_classmeeting(user, content, date, time, join_class):
    """
    根据信息创建班会
    :param user:
    :param content:
    :param date:
    :param time:
    :param join_class:
    :return:
    """
    startline = datetime.datetime.strptime(date + ' ' + time, '%Y/%m/%d %H:%M')
    # 检查班级ID
    class_lst = []
    join_class_lst = join_class.split(',')
    for join_class_coding in join_class_lst:
        try:
            class_obj = Class.objects.xall().get(coding=join_class_coding, lps_version='3.0')
            class_lst.append(class_obj)
        except:
            pass
    # 写入数据库
    if class_lst != []:
        class_meeting = ClassMeeting.objects.create(startline=startline, status=0, content=content, is_temp=True,
                                                    create_id=user.id)
        class_meeting_relation_lst = []
        for class_obj in class_lst:
            class_meeting_relation_lst.append(
                ClassMeetingRelation.objects.create(class_meeting=class_meeting, class_id=class_obj.id))
        result, log = create_liveroom(user, class_meeting, class_lst)
        if result is False:  # 如果创建直播室失败，则删除临时班会记录
            logger.error('create_liveroom' + log)
            for class_meeting_relation in class_meeting_relation_lst:
                class_meeting_relation.delete()
            class_meeting.delete()
        return result
    else:
        return False


def alter_classmeeting(classmeeting_id, data, time, content):
    """
    根据信息修改班会
    :param classmeeting_id:
    :param content:
    :param data:
    :param time:
    :return:
    """
    startline = datetime.datetime.strptime(data + ' ' + time, '%Y/%m/%d %H:%M')
    # 检查班级ID
    try:
        class_meeting = ClassMeeting.objects.get(id=classmeeting_id)
    except:
        return False
    class_meeting.startline = startline
    class_meeting.content = content
    class_meeting.save()
    return True


# ---公共方法-------------------------------------------------------------------------------------------------------------

def create_liveroom(teacher, class_meeting, class_lst):
    """
    创建直播室接口处理地址
    :param teacher:
    :param class_meeting:
    :param class_lst:
    :return:
    """
    url = settings.LIVE_ROOM_CREATE_API
    values = {
        'loginName': settings.LIVE_ROOM_USERNAME,
        'password': settings.LIVE_ROOM_PASSWORD,
        'sec': 'true',
        'subject': '%s_%s(%s)' % (class_meeting.content, str(class_meeting.id), datetime.datetime.now().ctime()),
        'startDate': datetime.datetime.now(),
        'scene': 0,
        'speakerInfo': teacher.staff_name + ',' + teacher.description,
        'scheduleInfo': class_lst[0].career_course.description if class_lst else '',
        'studentToken': generate_random(6, 0),
        'description': '这里是' + ','.join([class_obj.coding for class_obj in class_lst]) + '班的直播课堂，欢迎加入课堂',
        'realtime': True,
    }
    data = urllib.urlencode(values)  # 解析成key=value?key=value
    req = urllib2.Request(url, data)  # 发送的地址和数据
    response = urllib2.urlopen(req)  # 发送请求
    result = json.loads(response.read())  # 取出数据
    # 保存直播室相关数据
    if result['code'] == '0':
        live_room = LiveRoom()
        live_room.live_id = result['id']
        live_room.live_code = result['number']
        live_room.assistant_token = result['assistantToken']
        live_room.student_token = result['studentToken']
        live_room.teacher_token = result['teacherToken']
        live_room.student_client_token = result['studentClientToken']
        live_room.student_join_url = result['studentJoinUrl']
        live_room.teacher_join_url = result['teacherJoinUrl']
        live_room.class_meeting = class_meeting
        live_room.save()
        return True, result['code']
    else:
        return False, result['code']


def update_attendance_info(class_meeting):
    """
    更新值得班会的考勤数据
    :param classmeeting:
    :return:
    """
    # 获取当前班会包含的班级
    class_id_lst = ClassMeetingRelation.objects.filter(class_meeting=class_meeting).values_list("class_id", flat=True)
    live_room_lst = LiveRoom.objects.filter(class_meeting=class_meeting)
    if live_room_lst.count() > 0:
        startline = class_meeting.startline
        finish_date = class_meeting.finish_date
        start_datetime = (startline - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        finish_datetime = (startline + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        url = settings.LIVE_ROOM_JOININFO_API
        values = {
            'loginName': settings.LIVE_ROOM_USERNAME,
            'password': settings.LIVE_ROOM_PASSWORD,
            'sec': 'true',
            'roomId': live_room_lst[0].live_id,
            'startTime': start_datetime,
            "endTime": finish_datetime,
        }
        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.loads(response.read().replace('\t', ''))
        except Exception, e:
            logger.error(e)
            # print(e)
            return
        inittime = datetime.datetime(1970, 1, 1)
        cmdelta30 = startline + datetime.timedelta(minutes=30) - inittime
        cmdelta_finish = (finish_date if finish_date else startline + datetime.timedelta(minutes=60 * 3)) - inittime
        cmdelta = startline - inittime
        if result['code'] == '0':
            user_list = result['list']
            for user_info in user_list:
                try:
                    delta_join = datetime.timedelta(
                        microseconds=long(user_info['joinTime'] * 1000)) + datetime.timedelta(hours=8)
                    delta_leave = datetime.timedelta(
                        microseconds=long(user_info['leaveTime'] * 1000)) + datetime.timedelta(hours=8)
                    # 为了避免同名的学生
                    student_lst = UserProfile.objects.filter(
                        Q(real_name=user_info['nickname']) | Q(nick_name=user_info['nickname']))
                    for student in student_lst:
                        class_students = ClassStudents.objects.filter(student_class_id__in=class_id_lst,
                                                                      user=student,
                                                                      is_pause=False,
                                                                      status=ClassStudents.STATUS_NORMAL)
                        if student.is_student() and class_students.exists():
                            status = None
                            # 准时参加
                            if delta_join < cmdelta30 and delta_leave > cmdelta:
                                status = 'punctual'
                            # 迟到
                            if cmdelta30 < delta_join < cmdelta_finish:
                                status = 'late'
                            # 缺勤:
                            if cmdelta_finish < delta_join:
                                status = 'absent'
                            attendance_leve = {'punctual': 1, 'late': 2, 'absent': 3}
                            if status:
                                class_meeting_atts = ClassMeetingAttendance.objects.filter(
                                    class_meeting_id=class_meeting.id, student_id=student.id)
                                if class_meeting_atts.count() > 0:
                                    class_meeting_att = class_meeting_atts[0]
                                    # 解决用户多次进入会议（有多条考勤记录试）按照优先级觉得是否重写考勤数据
                                    if attendance_leve[class_meeting_att.status] <= attendance_leve[status]:
                                        break
                                    class_meeting_att.status = status
                                    class_meeting_att.class_meeting_id = class_meeting.id
                                    class_meeting_att.student_id = student.id
                                    class_meeting_att.liveroom_in_time = delta_join + inittime
                                    class_meeting_att.liveroom_out_time = delta_leave + inittime
                                    class_meeting_att.save()
                                else:
                                    ClassMeetingAttendance.objects.create(status=status,
                                                                          class_meeting_id=class_meeting.id,
                                                                          student_id=student.id,
                                                                          liveroom_in_time=delta_join + inittime,
                                                                          liveroom_out_time=delta_leave + inittime)

                                    content = '我参加了第一次班会，了解了专业和老师，正式开始了学习'
                                    for class_student in class_students:
                                        if StudyHistory.objects.filter(student_id=student.id,
                                                                       class_id=class_student.student_class_id,
                                                                       content=content).count() == 0:
                                            StudyHistory.objects.create(student_id=student.id,
                                                                        class_id=class_student.student_class_id,
                                                                        content=content, created=delta_join + inittime)
                            break
                except Exception, e:
                    logger.error(e)


# ---郭涛，入学时长 2016.4.11----------------------------------------------------------------------------------------------
def is_employment_contract(class_student):
    """
    是否提示选择就业
    :param class_student: 班级学生对象
    """
    class_id = class_student.student_class.id
    user_id = class_student.user.id
    result = get_class_students_full_payment(class_id, user_id)
    pay_type = result[user_id]
    # 全款，并且班会开始2周
    if class_student.is_employment_contract == None and pay_type == True and \
                    ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id, status=1,
                                                is_temp=False).count() >= 2 and \
            not class_student.is_view_employment_contract:
        return True
    else:
        return False

def is_choose_employment_contract(class_student):
    """
    是否选择就业
    :param class_student: 班级学生对象
    """
    class_id = class_student.student_class.id
    user_id = class_student.user.id
    result = get_class_students_full_payment(class_id, user_id)
    pay_type = result[user_id]
    # 全款，并且班会开始2周
    if class_student.is_employment_contract and pay_type == True and \
                    ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id, status=1,
                                                is_temp=False).count() >= 2 and \
            not class_student.is_view_employment_contract:
        return True
    else:
        return False

# 完善学习信息后，流程内容
def send_joinclass_sms_t_e(class_student):
    """
    完善学籍信息后提醒教务,和老师
    """
    # 发送站内信
    sclass = class_student.student_class
    teachers = sclass.teachers.all()
    edu_admin = sclass.edu_admin
    user = class_student.user
    real_name = user.real_name if user.real_name else user.nick_name
    course_name = sclass.career_course.name
    coding = sclass.coding
    result = get_class_students_full_payment(sclass.id, user.id)
    pay_type = '全款' if result[user.id] else '试学'
    join_date = class_student.created.strftime("%Y-%m-%d")

    alert_msg = '新学员入班： %s【%s/%s/%s】；入班时间%s。' % (real_name, course_name, coding, pay_type, join_date)
    alert_msg += "<a href='" + str(
        settings.SITE_URL) + "/lps3/teacher/class/" + str(sclass.id) + "/student_info/" + str(
        user.id) + "/'>查看完整信息>></a>"
    for teacher in teachers:
        sys_send_message(0, teacher.id, 1, alert_msg)
    sys_send_message(0, edu_admin.id, 1, alert_msg)

    # 教务短信提醒
    from utils.sms_manager import send_sms, get_templates_id

    try:
        apikey = settings.SMS_APIKEY
        if edu_admin.mobile:
            send_sms(apikey,
                     get_templates_id('join_class_edu_admin'),
                     int(edu_admin.mobile),
                     real_name.encode('utf-8'),
                     course_name.encode('utf-8'),
                     coding.encode('utf-8'),
                     pay_type,
                     join_date)
    except Exception as e:
        logger.exception('send_sms_join_class_edu_admin: ' + str(e))

    # # 老师短信
    # try:
    #     apikey = settings.SMS_APIKEY
    #     for teacher in teachers:
    #         if teacher.mobile:
    #             send_sms(apikey,
    #                      get_templates_id('join_class_edu_admin'),
    #                      int(teacher.mobile),
    #                      real_name.encode('utf-8'),
    #                      course_name.encode('utf-8'),
    #                      coding.encode('utf-8'),
    #                      pay_type,
    #                      join_date)
    # except Exception as e:
    #     logger.exception('send_sms_join_class_teacher: ' + str(e))


if __name__ == '__main__':
    print get_classmeeting_list(114, 42114)
