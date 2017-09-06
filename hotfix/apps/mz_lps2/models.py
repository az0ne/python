# -*- coding: utf-8 -*-
# version 2.0
# version 2.1
# modify record
# stuStatusUserTask 增加了 trace_type and trace_desc
# 增加了Model TraceTypeDict
# -------------
# version 2.6
# 增加了Model CheckContractUserTask
# 增加了Model GiveScoreUserTask
# -------------
from django.shortcuts import render
from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect
from django.db import models
from django.conf import settings
from aca_course.models import *
from mz_pay.models import *
from mz_user.models import *

from mz_lps.models import *
from mz_course.models import CareerCourse
#from mz_lps.models import Class,ClassStudents
from mz_user.models import UserProfile
from mz_pay.models import UserPurchase
from mz_user.models import ClassStudentDynamic


from django.dispatch import Signal
from django.db.models.signals import post_save
import time
from utils.tool import generate_random

from datetime import timedelta, datetime
# Create your models here.
import logging, os, json, re,urllib,urllib2
from django.db.models.signals import *
from django.shortcuts import render_to_response

# 每周班会
class ClassMeetingTask(models.Model):
    # user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"user", verbose_name=u"用户")
    user_class=models.ForeignKey(Class, verbose_name=u"班级")
    create_datetime=models.DateTimeField(u"创建时间",auto_now_add=True)
    startline=models.DateTimeField(u"班会时间",null=True, blank=True) #开始日期-截至日期 是每周任务必须的,除了评测模块，其他任务的时间为00：00：
    real_start_date=models.DateTimeField(u"实际开始时间", null=True, blank=True)
    status=models.SmallIntegerField(u"状态",default=1, choices=((0,"未开始"),(1,"已结束"),(2,"进行中")))
    finish_date=models.DateTimeField(u"实际完成时间", null=True, blank=True)
    content=models.CharField(u"内容", null=True,blank=True, max_length=100)
    is_check_before_classmeeting=models.BooleanField(u'是否完成班会前统计任务', default=False)
    is_check_get_risk_in_week=models.BooleanField(u'是否完成风险统计任务', default=False)
    is_temp = models.BooleanField(u'是否临时创建', default=False)


    class Meta:
        verbose_name = "直播班会用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class ClassMeetingTaskVideo510(models.Model):
    live_room = models.ForeignKey(LiveRoom,verbose_name=u"直播室",null=True,blank=True)
    play_id = models.CharField(u"视频id",max_length=200,default='')
    name = models.CharField(u"名称",max_length=200,default='')
    record_start_time = models.DateTimeField(u"录制开始时间")
    record_end_time = models.DateTimeField(u"录制结束时间")
    create_time = models.DateTimeField(u"创建时间", null=True, blank=True)
    size = models.IntegerField(default=0,verbose_name=u"视频大小")
    creator = models.IntegerField(default=0,verbose_name=u"视频上传者")

    class Meta:
        verbose_name = "视频信息(基础数据)"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.play_id)

class ClassMeetingTaskVideo(models.Model):
    live_room = models.ForeignKey(LiveRoom,verbose_name=u"直播室",null=True,blank=True)
    play_id = models.CharField(u"视频id",max_length=200,default='')
    play_subject = models.CharField(u"视频主题", null=True,blank=True, max_length=200,default='')
    record_id = models.IntegerField(default=0,verbose_name=u"记录id")
    create_time = models.DateTimeField(u"创建时间", null=True, blank=True)
    token = models.CharField(u"token", null=True,blank=True, max_length=50,default='')
    creator = models.IntegerField(default=0,verbose_name=u"视频上传者")
    url = models.CharField(u"播放url", max_length=200,default='')
    description = models.CharField(u"描述", max_length=200,default='')
    number = models.CharField(u"number", max_length=200,default='')
    class Meta:
        verbose_name = "直播室视频信息"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.play_id)

    #用户任务
class UserTask(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    create_datetime=models.DateTimeField(u"创建时间",auto_now_add=True)
    startline=models.DateTimeField(u"开始日期",null=True, blank=True) #开始日期-截至日期 是每周任务必须的,除了评测模块，其他任务的时间为00：00：00
    deadline=models.DateTimeField(u"截至日期", null=True, blank=True) #WeekUserTask截至日期为空，去班会时间为截至日期
    status=models.SmallIntegerField(u"状态",default=1, choices=((0,"未完成"),(1,"已完成"),(2,"进行中")))


    class Meta:
        verbose_name = "用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class JoinClassUserTask(UserTask):
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程", null=True, blank=True)
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "加入班级用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class ViewContractUserTask(UserTask):
    user_class=models.ForeignKey(Class, verbose_name=u"班级")
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "查看协议用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

#　查看入学协议并确定
class CheckContractUserTask(UserTask):
    user_class=models.ForeignKey(Class, verbose_name=u"班级")
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "入学协议用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class FullProfileUserTask(UserTask):
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "完善资料用户任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class CourseUserTask(UserTask):
    user_class=models.ForeignKey(Class, verbose_name=u"班级")
    #complete_degree= models.IntegerField(u"完成度", default=0) # 0~100
    rank_in_class=models.IntegerField(u"班级排名", default=0)
    plan_study_time=models.IntegerField(u"计划学时",default=15)
    real_study_time=models.IntegerField(u"计划内实际学时",default=0)
    real_study_time_ext=models.IntegerField(u"额外学时",default=0)
    total_study_time=models.IntegerField(u"总学时",default=0)
    ava_score=models.IntegerField(u"平均评测分",default=0)
    plan_gradute_time=models.DateField(u"预计毕业时间",null=True,blank=True)
    study_point=models.IntegerField(u"累计学力",null=True,blank=True)
    relate_content=models.CharField(u"相关内容",null=True,blank=True,max_length=10000)
    finish_content = models.CharField(u"实际完成情况",null=True,blank=True,max_length=10000)
    comment_count= models.IntegerField(u"评论次数",default=-1)
    liveroom_comment_count= models.IntegerField(u"直播课评论次数",default=-1)
    liveroom_in_time= models.DateTimeField(u"进入直播课时间", null=True, blank=True)
    liveroom_out_time= models.DateTimeField(u"离开直播课时间",null=True, blank=True)
    week=models.ForeignKey(ClassMeetingTask,null=True,blank=True)
    calc_log = models.CharField(u"增加日志",null=True, blank= True,max_length=1000)
    #Add by Steven YU
    is_first = models.BooleanField(u"第一周",null=False, blank=False, default=False)


    class Meta:
        verbose_name = "课程模块用户任务"
        verbose_name_plural = verbose_name
        # unique_together = (("user", "week"),)
    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(CourseUserTask, self).save(*args, **kwargs)
        # 加入学员动态：如果kpi>=100%，发动态
        if self.plan_study_time <= self.real_study_time and self.week:
            params = dict(user=self.user, type=2, obj_id=self.week.id)
            ClassStudentDynamic.objects.get_or_create(**params)

class CourseTaskDone(models.Model):
    course_user_task = models.ForeignKey(CourseUserTask, verbose_name=u"用户课程学习任务")
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    relate_id = models.IntegerField(u"相关ID",null=False,blank=False)
    relate_type = models.SmallIntegerField(u"相关类型", choices=((1,"完成视频"),(2,"提交作业"),(3,"项目制作")))
    finish_datetime = models.DateTimeField(u"完成时间", auto_now_add=True)
    #week=models.ForeignKey(ClassMeetingTask,null=False,blank=False)

    class Meta:
        verbose_name = "用户完成课程任务"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

class ReadMeUserTask(UserTask):
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "阅读须知老师任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

# 打分任务
class GiveScoreUserTask(UserTask):
    week=models.ForeignKey(ClassMeetingTask,null=True,blank=True)
    # user_class=models.ForeignKey(Class, verbose_name=u"班级")
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "打分任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class TeacherProfileUserTask(UserTask):
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    class Meta:
        verbose_name = "完善资料老师任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

class TraceTypeDict(models.Model):
    name        = models.CharField(max_length=50, verbose_name=u"督促类型")
    index       = models.IntegerField("督促类型(从小到大)", default=999)
    class Meta:
        verbose_name        = u"督促类型"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class StuStatusUserTask(UserTask):
    STATUS_TYPE = {
        (1,"完成项目制作"),
        (2,"进度落后太多"),
        (3,"通过课程"),
        (4,"未通过课程"),
        }
    stu_status=models.SmallIntegerField(u"提醒类型",choices=STATUS_TYPE)
    student_id=models.IntegerField(u"学生ID",null=False,blank=False)
    relate_id=models.IntegerField(u"相关ID",null=True,blank=True)
    trace_type = models.ForeignKey(TraceTypeDict, verbose_name=u"督促类型", null=True, blank=True)
    trace_desc = models.CharField(u"督促文本", null=True, blank=True, max_length=1000)
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)

    class Meta:
        verbose_name = "学生状态老师任务"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)

#给带班老师评分
class GiveScoreStudentsUserTask(UserTask):
    week=models.ForeignKey(ClassMeetingTask,null=True,blank=True)
    finish_date=models.DateField(u"实际完成日期", null=True, blank=True)
    timeliness=models.IntegerField(u"回答问题的即时性评分", null=True, blank=True)
    professional_level=models.IntegerField(u"专业水平评分", null=True, blank=True)
    explain_level=models.IntegerField(u"讲解水平评分", null=True, blank=True)
    harvest=models.IntegerField(u"收获的自评", null=True, blank=True)
    suggestion=models.TextField(u"对老师的意见或建议", null=True, blank=True)

    class Meta:
        verbose_name = "给带班老师评分任务"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

#给带班老师评分结果表
class GiveScoreStudentsResult(models.Model):
    week=models.ForeignKey(ClassMeetingTask,null=True,blank=True)
    timeliness=models.FloatField(u"即时性评分的平均值", null=True, blank=True)
    professional_level=models.FloatField(u"专业水平评分的平均值", null=True, blank=True)
    explain_level=models.FloatField(u"讲解水平评分的平均值", null=True, blank=True)
    harvest=models.FloatField(u"收获的自评平均值", null=True, blank=True)
    ava_total=models.FloatField(u"总分平均值", null=True, blank=True)

    class Meta:
        verbose_name = "老师评分汇总表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

# 用户素质项得分
class UserQualityModelItems(models.Model):
    QUALITY_TYPE = {
        (1,"执行力"),
        (2,"沟通力"),
        (3,"主动性"),
        }
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    quality_type=models.SmallIntegerField(u"素质类型",choices=QUALITY_TYPE)
    subject_score=models.IntegerField(u"老师打分", default=-1)
    score= models.IntegerField(u"素质项分数", default = -1)
    ava_score = models.IntegerField(u"平均分", default = -1)
    week=models.ForeignKey(ClassMeetingTask,null=True,blank=True)
    calc_datetime=models.DateTimeField(u"计算时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户模型项"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return str(self.id)


# 队列，用来做后台计算的排队
class AsyncMethod(models.Model):
    CALC_TYPES = (
        ('1','计算学力'),
        ('2','完成评测模块'),
    )
    name = models.CharField(u"名称",null = True,blank= True, max_length=10)
    methods= models.CharField(u"方法体", null=True, blank=True, max_length=300)
    calc_type= models.SmallIntegerField(u"计算类型",choices=CALC_TYPES)
    calc_datetime=models.DateTimeField(u"计算时间",null=True,blank=True)
    submit_datetime=models.DateTimeField(u"提交时间",auto_now_add=True)
    priority=models.SmallIntegerField(u"优先级",default=3) #1,2,3:1最高
    is_calc=models.BooleanField(u"已计算",default=False) #当已计蒜=False，但是计蒜时间有值，表示预期执行的时间
    error_reason = models.CharField(u"错误原因", null=True, blank=True, max_length=300)

    class Meta:
        verbose_name = u'异步方法'
        verbose_name_plural = verbose_name
        ordering = ['-priority', 'submit_datetime', 'id']
    def __unicode__(self):
        return str(self.id)

# ISOTIMEFORMAT='%Y-%m-%d'
#
# def _create_class(**kwargs):
#     obj=kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#     ret=True
#     if created and (obj is AcademicCourse):
#         inst=kwargs['instance']
#         if not len(AcademicClass.objects.filter(career_course=inst)):
#             cl = AcademicClass();
#             cl.coding = inst.short_name+'001'
#
#             cl.date_open = time.strftime(ISOTIMEFORMAT)
#             cl.student_limit = 100000
#             cl.qq="###"
#             cl.career_course=inst
#             cl.save()
#     else:
#         ret=False
#     return ret
#
#
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
#
#
# # function:推送加入班级任务
# # param: **kwargs
# # ret : Task_id
# # pass
# def _need_join_class(**kwargs):
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         if created and (obj is UserProfile):
#             instance = kwargs['instance']
#             try:
#                 task_lsit = JoinClassUserTask.objects.filter(user = instance)
#                 if len(task_lsit) < 1:   #是否推送过加入班级任务
#                     now = datetime.now()
#                     aDay = timedelta(days=3)
#                     now = now + aDay
#                     JoinClassUserTask.objects.create(
#                         user = instance,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2)
#                     return 1
#             except Exception as msg:
#                 print "join_class_exception--->",msg
#     return 0
#
#
#
#
# #function:当支付成功时,触发更新加入班级事件,且时间不超过三天,将其状态置为1.完成
# #param : **kwargs
# #ret : task_id 返回被更新任务的id
# #如果正确产生UserTask，ret=UserTask实例的ID
# def _update_join_class(**kwargs):
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         try:
#             if created and (obj is ClassStudents):
#                 #更新状态前必须检查状态id必须为2.进行中
#                 #所需条件  1.用户id
#                 instance = kwargs['instance']
#                 user = instance.user
#                 task_list = JoinClassUserTask.objects.filter(user = user,status = 2)
#                 if len(task_list) == 1:  #确定在数据库里面只有一条记录
#                     task = task_list[0]
#                     task.status = 1
#                     task.save()
#                     return 1
#         except Exception as msg:
#             print "update_join_class--->",msg
#     return 0
#
#
# #查看学习协议
# #如果正确产生UserTask，ret=UserTask实例的ID
# def _need_view_contract(**kwargs):
#     #需要的数据,用户id,通过UserPurchase外键关系获得用户id
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         if created and (obj is ClassStudents): #付款后添加查看学习协议任务
#             instance = kwargs['instance']
#             try:
#                     #加入班级
#                 contract = ViewContractUserTask.objects.filter(user = instance.user,user_class = instance.student_class)
#                 if len(contract) < 1:
#                     user = instance.user
#                     now = datetime.now()
#                     aDay = timedelta(days=3)
#                     now = now + aDay
#                     #获取班级
#                     classs = instance.student_class
#                     ViewContractUserTask.objects.create(
#                         user = user,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2,user_class = classs)
#                     return 1
#             except Exception as msg:
#                 print "view_contract----->",msg
#     return 0
# #更新学习协议
# def _update_view_contract(**kwargs):
#     ret=0
#     #如果正确产生UserTask，ret=UserTask实例的ID
#     return ret
#
# #支付成功，创建提醒完善资料任务
# #资料全部字段完善后，更改状态为完善
#
# def _need_full_profile(**kwargs):
#     '''
#     # function:向用户推送完善资料任务
#     '''
#     obj=kwargs['sender']
#     save = False
#     if kwargs.has_key('created'):
#         save = kwargs['created']
#         try:
#             if save and (obj is ClassStudents):#如果支付成功会触发监听，随后创建一条提醒完善资料任务
#                 inst=kwargs['instance']
#                 list = FullProfileUserTask.objects.filter(user = inst.user)
#                 if len(list) < 1:#如果FullProfileUserTask，列表为空说明还没有写入，为空就写入
#                     now = datetime.now()
#                     aDay = timedelta(days=3)
#                     now = now + aDay
#                     FullProfileUserTask.objects.create(user = inst.user,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2)
#                     return 1
#         except Exception as e:
#               print "full_userProfile",e
#     else:
#         return 0
#
#
# def _update_full_profile(**kwargs):
#     '''
#     # 当用户完善资料的时候需要更新完善资料任务,created:False
#     '''
#     obj=kwargs['sender']
#     save = False
#     try:
#         if kwargs.has_key('created'):
#             save = kwargs['created']
#             if (not save) and (obj is UserProfile):#如果资料被保存，触发监听，随后修改资料完善状态为已完成
#                 inst = kwargs['instance']
#                 #是否存在完善资料任务
#                 list = FullProfileUserTask.objects.filter(user = inst,status = 2)
#                 if len(list) == 1:
#                     if list[0].deadline > datetime.now():  #是否在指定时间内完成任务
#                         list[0].status = 1
#                     else:
#                         list[0].status = 0
#                     list[0].save()
#                     return 1
#     except Exception as msg:
#         print "udpate_full_userProfile---->",msg
#     return 0
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
#                 print "update_live_room--------->",msg
#     return 0
#
# def _created_live_room(**kwargs):
#     '''
#     # function:创建班级的时候创建直播室
#     '''
#     obj = kwargs['sender']
#     created = False
#     if kwargs.has_key('created'):
#         created = kwargs['created']
#         if created and (obj is Class):
#             instance = kwargs['instance']
#             try:
#                 if instance:
#                     if LiveRoom.objects.filter(live_class=instance).count() > 0:
#                         return 0
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
#
#             except Exception as msg:
#                 print "create_live_room-------->",msg
#
# def Post_Save_Handle(**kwargs):
#
#     try:
#         if _create_class(**kwargs):
#             pass
#         if _need_join_class(**kwargs):
#             pass
#         if _update_join_class(**kwargs):
#             pass
#         if _need_view_contract(**kwargs):
#             pass
#         if _update_view_contract(**kwargs):
#             pass
#         if _need_full_profile(**kwargs):
#             pass
#         if _update_full_profile(**kwargs):
#             pass
#         if _need_create_plan(**kwargs):
#             pass
#         if _update_create_plan(**kwargs):
#             pass
#         if _need_finish_course(**kwargs):
#             pass
#         if _update_finish_course(**kwargs):
#             pass
#         if _need_query_profile(**kwargs):           #向老师推送查看教师须知和完善个人资料的任务
#             pass
#         if _update_teacher_profile(**kwargs):       #更新老师完善资料的任务状态为已完成
#             pass
#         if _update_live_room(**kwargs):         #更新班会直播
#             pass
#         if _created_live_room(**kwargs):
#             pass
#     except Exception as e:
#         print "post_save------->",e
#         logging.error(e)
#
# from django.db.models.signals import m2m_changed
#
# def toppings_changed(**kwargs):
#     # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02BC1A90>, 'instance': <UserProfile: puddingshine@foxmail.com>, 'pk_set': set([2L]), 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'pre_add', 'sender': <class 'mz_user.models.UserProfile_groups'>}
#     # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02BC1A90>, 'instance': <UserProfile: puddingshine@foxmail.com>, 'pk_set': set([2L]), 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'post_add', 'sender': <class 'mz_user.models.UserProfile_groups'>}
# # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02AC1A70>, 'instance': <UserProfile: 183683266@qq.com>, 'pk_set': None, 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'pre_clear'}
# # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02AC1A70>, 'instance': <UserProfile: 183683266@qq.com>, 'pk_set': None, 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'post_clear'}
# # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02AC1A70>, 'instance': <UserProfile: 183683266@qq.com>, 'pk_set': set([2L]), 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'pre_add'}
# # {'reverse': False, 'signal': <django.db.models.signals.ModelSignal object at 0x02AC1A70>, 'instance': <UserProfile: 183683266@qq.com>, 'pk_set': set([2L]), 'using': 'default', 'model': <class 'django.contrib.auth.models.Group'>, 'action': u'post_add'}
#
#     print kwargs
#     action = kwargs['action']
#     pk_set = str(kwargs['pk_set'])
#     if action == "post_add" and "2" == pk_set[5:6]:
#         print "执行的pk_set",pk_set
#         instance = kwargs["instance"]
#         task_lsit_tea = ReadMeUserTask.objects.filter(user = instance).count()
#         if task_lsit_tea < 1:
#             now = datetime.now()
#             aDay = timedelta(days=3)
#             now = now + aDay
#             read_me_tea_task_id = ReadMeUserTask.objects.create(
#                 user = instance,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2
#             )
#
#         task_lsit_tea1 = TeacherProfileUserTask.objects.filter(user = instance).count()
#         if task_lsit_tea1 < 1:
#             now = datetime.now()
#             aDay = timedelta(days=3)
#             now = now + aDay
#
#             profile_task_id = TeacherProfileUserTask.objects.create(
#                 user = instance,create_datetime = datetime.now(),startline = datetime.now(),deadline = now,status = 2
#             )
#         need_join_class_list = JoinClassUserTask.objects.filter(user = instance)
#         if len(need_join_class_list) > 0:
#             need_join_class_list[0].delete()
#         return 1
# Signal.connect(post_save,Post_Save_Handle)
#
# post_save.connect(xxx,AcademicCourse.through)
# from django.db.models.signals import m2m_changed
# m2m_changed.connect(toppings_changed, sender=UserProfile.groups.through)



