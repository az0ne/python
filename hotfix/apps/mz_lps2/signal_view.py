# -*- coding: utf-8 -*-

# from maiziedu_website import settings
# from aca_course.models import *
# from mz_pay.models import *
# from mz_user.models import *
from utils.sms_manager import send_sms, get_templates_id
# from mz_lps.models import *
# from mz_lps.models import Class,ClassStudents,CourseScore
# from mz_user.models import UserProfile
from mz_common.models import AppConsultInfo
from mz_lps2.models import *
from mz_lps2.calc_view import get_next_pan_task
# from mz_pay.models import UserPurchase

from django.dispatch import Signal
from django.db.models.signals import post_save, m2m_changed
import time
from utils.tool import generate_random

from datetime import timedelta, datetime
# Create your models here.
import logging, os, json, re,urllib,urllib2
# from django.db import transaction
from mz_backend.views import add_studyhistory_for_class


logger = logging.getLogger('mz_lps2.signal_view')

ISOTIMEFORMAT='%Y-%m-%d'



def _create_class(**kwargs):
    ret=True
    try:
        obj = kwargs['sender']
        created = False
        if kwargs.has_key('created'):
            created = kwargs['created']

        if created and (obj is AcademicCourse):
            inst = kwargs['instance']
            if not len(AcademicClass.objects.filter(career_course=inst)):
                cl = AcademicClass()
                cl.coding = inst.short_name+'001'

                cl.date_open = time.strftime(ISOTIMEFORMAT)
                cl.student_limit = 100000
                cl.qq="###"
                cl.career_course=inst
                cl.save()
        else:
            ret=False
        return ret
    except Exception as e:
        print '_create_class', e
        logger.error(e)

post_save.connect(_create_class, sender=AcademicCourse) # UserProfile.groups.through)

# 直播班会完成的时候推送打分任务
def _update_classmeetingtask(**kwargs):
    try:
        obj = kwargs['sender']
        if kwargs.has_key('created'):
            created = kwargs['created']
        if not created and (obj is ClassMeetingTask):
            inst = kwargs['instance']
            # 判断是否是第一周班会
            if ClassMeetingTask.objects.filter(user_class=inst.user_class, is_temp=False).count() == 1:
                return
            cmt = ClassMeetingTask.objects.filter(user_class=inst.user_class, is_temp=False).order_by('-startline')
            if inst.id != cmt[0].id:
                return
            # 判断是否已经生成任务
            if GiveScoreUserTask.objects.filter(week=inst).count():
                return
            # 判断直播班会是否已结束
            if inst.status == 1:
                gsut = GiveScoreUserTask()
                gsut.user = inst.user_class.teacher
                gsut.week = inst
                gsut.startline = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                gsut.status = 2
                gsut.save()

    except Exception as e:
        print '_update_classmeetingtask', e
        logger.error(e)

post_save.connect(_update_classmeetingtask, sender=ClassMeetingTask)

# # function:教师注册时需推送的任务
# def _need_query_profile(**kwargs):
#     return 0
# # function:老师完善个人资料后将任务状态置为已完成
# def _update_teacher_profile(**kwargs):
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         if (not created) and (obj is UserProfile):
#             instance = kwargs['instance']
#             #判断是学生还是老师
#             if instance.is_teacher():        #如果是老师  更新老师操作任务的状态 阅读教师须知(ReadMeUserTask),完善个人资料(TeacherProfileUserTask)
#                 task_lsit_tea1 = TeacherProfileUserTask.objects.filter(user = instance)
#                 if len(task_lsit_tea1) == 1:             #如果这个用户的这条记录存在于数据库说明已经创建,这次是更新
#                     task_lsit_tea1[0].status = 1
#                     task_lsit_tea1[0].save()            #将状态更改为1   已完成
#                     return task_lsit_tea1[0].status
#     return 0


# function:推送加入班级任务
# param: **kwargs
# ret : Task_id
# pass
def _need_join_class(**kwargs):
    obj = kwargs['sender']
    created = False
    if kwargs.has_key('created'):
        created = kwargs['created']
        if created and (obj is MyCourse):
            instance = kwargs['instance']
            if instance.course_type == 2:
                try:
                    career_course = CareerCourse.objects.get(id=int(instance.course))
                    task_list = JoinClassUserTask.objects.filter(user=instance.user, career_course=career_course)
                    if not task_list:   #是否推送过加入班级任务
                        now = datetime.now()
                        JoinClassUserTask.objects.create(
                            user=instance.user, create_datetime=now, startline=now,\
                            deadline=now+timedelta(days=3), status=2, career_course=career_course)
                        return 1
                except Exception as msg:
                    print "join_class_exception--->",msg
                    logger.error(msg)
    return 0

post_save.connect(_need_join_class, sender= MyCourse)



def _update_join_class(**kwargs):
    try:
        obj = kwargs['sender']
        created = False
        if kwargs.has_key('created'):
            created = kwargs['created']
            if created and (obj is ClassStudents):
                instance = kwargs['instance']
                user = instance.user
                now = datetime.now()
                career_course = instance.student_class.career_course
                clazz = instance.student_class

                try:
                    # zhangyu 加入班级添加学习历程
                    add_studyhistory_for_class(user, clazz)
                except Exception as msg:
                    print "study history--->",msg
                    logger.error(msg)

                try:
                    task_list = JoinClassUserTask.objects.filter(user=user, status=2,\
                                            career_course=career_course)
                    if task_list:
                        task_list[0].status = 1
                        task_list[0].finish_date = now
                        task_list[0].save()
                    else:
                        JoinClassUserTask.objects.create(
                            user=user, create_datetime=now, startline=now, deadline=now+timedelta(days=3),\
                            status=1, career_course=career_course, finish_date=now)
                except Exception as msg:
                    print "update_join_class--->",msg
                    logger.error(msg)

                try:
                    #查看学习协议
                    #如果正确产生UserTask，ret=UserTask实例的ID
                    contract = ViewContractUserTask.objects.filter(user = instance.user,user_class = instance.student_class)
                    if len(contract) < 1:
                        now = datetime.now()
                        aDay = timedelta(days=3)
                        now = now + aDay
                        #获取班级
                        classs = instance.student_class
                        ViewContractUserTask.objects.create(
                            user = user,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2,user_class = classs)
                        # return 1
                except Exception as msg:
                    print "view_contract----->",msg
                    logger.error(msg)

                try:
                    '''
                    # function:向用户推送完善资料任务
                    '''
                    list = FullProfileUserTask.objects.filter(user = user)
                    if len(list) < 1:#如果FullProfileUserTask，列表为空说明还没有写入，为空就写入
                        now = datetime.now()
                        aDay = timedelta(days=3)
                        now = now + aDay
                        FullProfileUserTask.objects.create(user=user, create_datetime=datetime.now(), startline=datetime.now(), deadline=now, status=2)
                        # return 1
                except Exception as msg:
                    print "full_userProfile----->", msg
                    logger.error(msg)

                try:
                    # 为用户推送下周班级任务,调用calc中方法
                    if not clazz.lps_version == '3.0':
                        get_next_pan_task(user, clazz)

                except Exception as msg:
                    print "signal_plan_for_nextweek----->", msg
                    logger.error(msg)

                try:
                    #查看入学协议
                    ccut = CheckContractUserTask()
                    ccut.user = user
                    ccut.user_class = clazz
                    ccut.status = 2
                    ccut.save()
                except Exception as msg:
                    print "view_contract----->", msg
                    logger.error(msg)

                # try:
                #     '''
                #     # 当用户完善资料的时候需要更新完善资料任务,created:False
                #     '''
                #     #是否存在完善资料任务
                #     list = FullProfileUserTask.objects.filter(user=instance, status=2)
                #     if len(list) == 1:
                #         if list[0].deadline > datetime.now():  #是否在指定时间内完成任务
                #             list[0].status = 1
                #         else:
                #             list[0].status = 0
                #         list[0].save()
                #         # return 1
                #     return 1
                # except Exception as msg:
                #     print "udpate_full_userProfile---->", msg
                #     logger.error(msg)

        return 0
    except Exception as e:
        print "_update_join_class", e
        logger.error(e)

# 20160617注释掉此行代码.因为app加班操作会触发此信号,此信号原本为监听lps2加班操作,现lps2已经不存在加班操作,故注释
# post_save.connect(_update_join_class, sender=ClassStudents)

# def _update_live_room(**kwargs):        #更新直播班会任务
#     '''
#     # function:当直播结束后,需要更新直播班会
#     '''
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         if (not created) and (obj is LiveRoom):
#             instance = kwargs['instance']
#             try:
#                 if instance.live_is_open == 0:          #为0表示已关闭直播室
#                     #找到与直播室关联的班级,找到这个班级正在直播的班会
#                     live_class = instance.live_class
#                     class_meeting_task_list = ClassMeetingTask.objects.filter(user_class = live_class,status = 2).order_by("-id")
#                     for class_meeting_task in class_meeting_task_list:
#                         class_meeting_task.finish_date = datetime.now()
#                         class_meeting_task.status = 1   #1  已结束
#                         class_meeting_task.save()
#                 elif instance.live_is_open == 1:        #为1表示已开启直播室
#                     live_class = instance.live_class
#                     class_meeting_task_list = ClassMeetingTask.objects.filter(user_class = live_class,status = 0).order_by("-id")
#                     for class_meeting_task in class_meeting_task_list:
#                         class_meeting_task.status = 2   #2 进行中
#                         class_meeting_task.real_start_date = datetime.now()
#                         class_meeting_task.save()
#                     return 1
#             except Exception as msg:
#                 print "update_live_room--------->", msg
#     return 0
#
# post_save.connect(_update_live_room, sender= LiveRoom)

# def _created_live_room(**kwargs):
#     '''
#     # function:创建班级的时候创建直播室
#     '''
#     try:
#         obj = kwargs['sender']
#         created = False
#         if kwargs.has_key('created'):
#             created = kwargs['created']
#             if created and (obj is Class):
#                 instance = kwargs['instance']
#                 if instance:
#                     if LiveRoom.objects.filter(live_class=instance).count() > 0:
#                         return 0
#
#                     # 有时会出现创建了直播室，但是没有和班级关联起来，所以在创建之前先检查有没有对应的直播室
#                         # 创建直播室接口处理地址
#                     # url = settings.LIVE_ROOM_QUERY_API
#                     # values = {
#                     #     'loginName':settings.LIVE_ROOM_USERNAME,
#                     #     'password':settings.LIVE_ROOM_PASSWORD,
#                     #     'sec':'true',
#                     #     'subject':instance.coding,
#                     #     }
#                     # data = urllib.urlencode(values)     #解析成key=value?key=value
#                     # req = urllib2.Request(url, data)    #发送的地址和数据
#                     # response = urllib2.urlopen(req)     #发送请求
#                     # result = json.loads(response.read())    #取出数据
#                     # # 但没有对应的直播室的时候，再创建
#                     # if result['code'] != 0:
#
#                     # 创建直播室接口处理地址
#                     url = settings.LIVE_ROOM_CREATE_API
#                     values = {
#                         'loginName':settings.LIVE_ROOM_USERNAME,
#                         'password':settings.LIVE_ROOM_PASSWORD,
#                         'sec':'true',
#                         'subject':instance.coding,
#                         'startDate':datetime.now(),
#                         'scene':1,
#                         'speakerInfo':instance.teacher.nick_name+','+instance.teacher.description,
#                         'scheduleInfo':instance.career_course.description,
#                         'studentToken':generate_random(6,0),
#                         'description':'这里是'+instance.coding+'班的直播课堂，欢迎加入课堂',
#                         'realtime':True,
#                         }
#                     data = urllib.urlencode(values)     #解析成key=value?key=value
#                     req = urllib2.Request(url, data)    #发送的地址和数据
#                     response = urllib2.urlopen(req)     #发送请求
#                     result = json.loads(response.read())    #取出数据
#
#                     # 保存直播室相关数据
#                     if result['code'] == '0':
#                         live_room = LiveRoom()
#                         live_room.live_id = result['id']
#                         live_room.live_code = result['number']
#                         live_room.assistant_token = result['assistantToken']
#                         live_room.student_token = result['studentToken']
#                         live_room.teacher_token = result['teacherToken']
#                         live_room.student_client_token = result['studentClientToken']
#                         live_room.student_join_url = result['studentJoinUrl']
#                         live_room.teacher_join_url = result['teacherJoinUrl']
#                         live_room.live_class = instance
#                         live_room.save()
#                         return 1
#                     else:
#                         logging.error("create_live_room, geesee error")
#
#     except Exception as msg:
#         print "create_live_room-------->",msg
#         logger.error(msg)

# post_save.connect(_created_live_room, sender= Class)

# def _update_stustatususertask(**kwargs):
#     ret = True
#     print '_update_stustatususertask ：', kwargs
#     try:
#         obj = kwargs['sender']
#         created = False
#         if kwargs['instance'] and (obj is ProjectRecord):
#             inst=kwargs['instance']
#             if inst.score:
#                 stuusertask_list = StuStatusUserTask.objects.filter(student_id=inst.student.id, relate_id=inst.project.re)
#                 if len(stuusertask_list) > 0:
#                     stuusertask_list[0].finish_date = datetime.now().strftime(ISOTIMEFORMAT)
#                     stuusertask_list[0].status = 1
#                     stuusertask_list[0].save()
#         else:
#             ret=False
#         return ret
#     except Exception as e:
#         print '_update_stustatususertask',e
#         logger.error(e)

# post_save.connect(_update_stustatususertask, sender=ProjectRecord)

# #更新学习协议
# def _update_view_contract(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret
#
#
#
# def _need_create_plan(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret
# def _update_create_plan(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret
# def _need_finish_course(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret
# def _update_finish_course(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret

def toppings_changed(**kwargs):
    try:
        action = kwargs['action']
        pk_set = str(kwargs['pk_set'])
        if action == "post_add" and "2" == pk_set[5:6]:
            print "执行的pk_set",pk_set
            instance = kwargs["instance"]
            task_lsit_tea = ReadMeUserTask.objects.filter(user = instance).count()
            if task_lsit_tea < 1:
                now = datetime.now()
                aDay = timedelta(days=3)
                now = now + aDay
                read_me_tea_task_id = ReadMeUserTask.objects.create(
                    user = instance,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2
                )

            task_lsit_tea1 = TeacherProfileUserTask.objects.filter(user = instance).count()
            if task_lsit_tea1 < 1:
                now = datetime.now()
                aDay = timedelta(days=3)
                now = now + aDay

                profile_task_id = TeacherProfileUserTask.objects.create(
                    user = instance,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2
                )
            need_join_class_list = JoinClassUserTask.objects.filter(user = instance)
            if len(need_join_class_list) > 0:
                need_join_class_list[0].delete()
            return 1
    except Exception as e:
        print "post_add------->", e
        logger.error(e)

# Signal.connect(post_save,Post_Save_Handle)
m2m_changed.connect(toppings_changed, sender=UserProfile.groups.through)


# 给指定的渠道发送收集的用户信息
def _send_phonesms(**kwargs):
    try:
        obj = kwargs['sender']
        if kwargs.has_key('created'):
            created = kwargs['created']
            if created and (obj is AppConsultInfo):
                instance = kwargs['instance']
                # 发送短信
                mobile = 18683629262

                apikey = settings.SMS_APIKEY
                # '姓名:%(name)s;电话:%(telephone)s;课程来源:%(source)s;期望来电时间:%(qq)s'
                try:
                    send_sms.delay(apikey,
                                   get_templates_id('interest_student_info_2'),
                                   mobile,
                                   instance.name,
                                   instance.phone,
                                   instance.source,
                                   instance.qq)
                except Exception, e:
                    logger.error(e)
                # 给填写资料的同学发信息
                # '预约成功!您的麦子专属课程顾问将按照您约定的时间联系您,届时将以028开头的号码来电,请保持您的手机畅通!'
                try:
                    send_sms.delay(apikey, get_templates_id('tel_contact_2'), instance.phone)
                except Exception, e:
                    logger.error(e)

    except Exception as e:
        logger.error(e)


post_save.connect(_send_phonesms, sender=AppConsultInfo)

def Post_Save_Handle(**kwargs):
    obj=kwargs['sender']
    created = False
    if kwargs.has_key('created'):
        created = kwargs['created']

    #如果用户注册发送消息给fps
    inst=kwargs['instance']
    result = ''
    if created and (obj is UserProfile):
        result = FpsInterface.new_user({"user_id":inst.id})
    elif created and (obj is Class):
        result = FpsInterface.new_class({"class_id":inst.id})
    #elif (obj is ClassStudents):
    #    result = FpsInterface.student_join({"class_id":inst.student_class.id,"user_id":inst.user.id})
    elif created and (obj is Discuss):
        result = FpsInterface.new_discuss({"discuss_id":inst.id,"child_id":inst.parent_id})
        print result

Signal.connect(post_save, Post_Save_Handle)