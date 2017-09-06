# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from mz_course.models import Stage, CareerCourse, Lesson
from mz_lps.models import Project, Class, Examine
from mz_user.models import UserProfile
# StageTaskRelation 定制stage外键manager
from foreignkey_manager import CustomManagerForeignKey


class StudentInfo(models.Model):
    '''
    完善学生信息(弃用)
    '''
    student_id = models.IntegerField(u'学生ID', unique=True, db_index=True)
    real_name = models.CharField(u'真实姓名', max_length=30)
    email = models.EmailField(u'邮件地址', max_length=30)
    mobile = models.CharField(u'手机号码', max_length=11)
    address = models.CharField(u'地址', max_length=200)

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class Gift(models.Model):
    name = models.CharField(u'名称', max_length=50)
    desc = models.CharField(u'描述', max_length=200, null=True, blank=True)
    image = models.ImageField(u'图片', upload_to="lps3/gift/%Y/%m", null=True, blank=True)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '礼品'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


# class GiftItem(models.Model):
#     name = models.CharField(u'名称', max_length=50)
#     desc = models.CharField(u'描述', max_length=200)
#     created = models.DateTimeField(u'创建时间', auto_now_add=True)
#
#     parent = models.ForeignKey(Gift, verbose_name=u'所属礼品')
#
#     class Meta:
#         verbose_name = '礼品项'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return str(self.name)


class UserGiftRecord(models.Model):
    student_id = models.IntegerField(u'学生ID', db_index=True)
    class_id = models.IntegerField(u'班级ID', db_index=True)
    task_id = models.IntegerField(u'课程任务ID', db_index=True)
    gift = models.ForeignKey(Gift, verbose_name=u'礼品', db_index=True)
    provided = models.BooleanField(u'已发放', default=False)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '礼品领取记录'
        verbose_name_plural = verbose_name
        unique_together = (('student_id', 'class_id', 'task_id'),)

    def __unicode__(self):
        return str(self.id)


class Knowledge(models.Model):
    name = models.CharField(u'名称', max_length=50)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '知识点'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class Task(models.Model):
    TASK_TYPE_NORMAL = 0
    TASK_TYPE_FREE_488 = 1
    TASK_TYPE = {TASK_TYPE_NORMAL: u'正常', TASK_TYPE_FREE_488: u'488免费试学任务'}
    name = models.CharField(u'名称', max_length=20)
    desc = models.TextField(u'描述', max_length=100, null=True, blank=True)
    video_guide = models.URLField(u'视频讲解', max_length=200, null=True, blank=True)
    expect_time = models.SmallIntegerField(u'预期时长：天')
    excellent_time = models.SmallIntegerField(u'最短时长：天')
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    project_id = models.IntegerField(verbose_name=u'任务项目')
    gift = models.ForeignKey(Gift, verbose_name=u'礼品', null=True, blank=True)
    knowledges = models.ManyToManyField(Knowledge, verbose_name=u'任务知识点关系', through='TaskKnowledgeRelation')

    type = models.IntegerField(u'任务类型', choices=TASK_TYPE.items(), default=TASK_TYPE_NORMAL)

    class Meta:
        verbose_name = '课程任务'
        verbose_name_plural = verbose_name

    @property
    def project(self):
        objs = Project.objects.filter(id=self.project_id)
        return objs[0] if objs else None

    def is_free488_task(self):
        return self.type == self.TASK_TYPE_FREE_488

    def __unicode__(self):
        return str(self.name)


class StageTaskRelation(models.Model):
    STAGE_TASK_TYPE_NORMAL = 0
    STAGE_TASK_TYPE_FREE_3_1 = 1
    TASK_TYPE = {STAGE_TASK_TYPE_NORMAL: u'正常', STAGE_TASK_TYPE_FREE_3_1: u'lps3.1免费任务'}

    name = models.CharField(u'名称', max_length=50, blank=True, null=True)
    index = models.SmallIntegerField(u'排列顺序(从小到大)', default=999)

    # stage = models.ForeignKey(Stage, verbose_name=u'阶段')
    stage = CustomManagerForeignKey(Stage, verbose_name=u'阶段', manager=Stage.objects.xall)
    task = models.ForeignKey(Task, verbose_name=u'任务')
    type = models.IntegerField(u'阶段任务类型', choices=TASK_TYPE.items(), default=STAGE_TASK_TYPE_NORMAL)

    class Meta:
        verbose_name = '阶段任务关系表'
        verbose_name_plural = verbose_name
        unique_together = (('stage', 'task'),)

    def __unicode__(self):
        return str(self.name)


class UserTaskRecordManager(models.Manager):
    def get_queryset(self):
        # 调用父类的方法，在原来返回的QuerySet的基础上返回新的QuerySet
        return super(UserTaskRecordManager, self).get_queryset().exclude(is_in_sequence=0)

    def not_in_sequence_all(self):
        return super(UserTaskRecordManager, self).get_queryset()


class UserTaskRecord(models.Model):
    SCORE_CHOICES = (
        ('S', 'S'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    STATUS_CHOICES = (
        ('DOING', '已开始'),
        ('DONE', '已完成'),
        ('PASS', '已通过'),
        ('FAIL', '未通过'),
        ('REDOING', '重修中'),
    )
    status = models.CharField(u'状态', max_length=10, choices=STATUS_CHOICES, default='DOING', db_index=True)
    score = models.CharField(u'成绩', max_length=3, choices=SCORE_CHOICES, blank=True, null=True)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    is_pause = models.BooleanField(u'是否暂停', default=False)
    pause_datetime = models.DateTimeField(u'暂停时间', null=True, blank=True, default=None)
    paused_seconds = models.IntegerField(u'暂停秒数', default=0)
    done_time = models.DateTimeField(u'完成时间', null=True, blank=True)
    correct_time = models.DateTimeField(u'作业批改时间', null=True, blank=True)

    stage_task = models.ForeignKey(StageTaskRelation, verbose_name=u'阶段任务关系')
    student_id = models.IntegerField(u'学生ID', db_index=True)
    class_id = models.IntegerField(u'班级ID', db_index=True)

    learning_item_id = models.IntegerField(u'当前学习中的item_id', null=True)
    is_in_sequence = models.BooleanField(u'是否是按序解锁任务', default=True)

    objects = UserTaskRecordManager()

    class Meta:
        verbose_name = '学生任务记录'
        verbose_name_plural = verbose_name
        unique_together = (('stage_task', 'student_id', 'class_id'),)

    def __unicode__(self):
        return str(self.id)

    def has_done(self):
        """已做过,包括 完成未打分,通过,未通过"""
        return self.status in ("DONE", "PASS", "FAIL")

    def is_going(self):
        """进行中"""
        return self.status in ("DOING", "REDOING")

    @property
    def student(self):
        students = UserProfile.objects.filter(pk=self.student_id)
        return students[0] if students else None


class TaskKnowledgeRelation(models.Model):
    name = models.CharField(u'名称', max_length=50, blank=True, null=True)
    index = models.SmallIntegerField(u'排列顺序(从小到大)', default=999)

    task = models.ForeignKey(Task, verbose_name=u'任务')
    knowledge = models.ForeignKey(Knowledge, verbose_name=u'知识点')

    class Meta:
        verbose_name = '任务知识点关系表'
        verbose_name_plural = verbose_name
        unique_together = (('task', 'knowledge'),)

    def __unicode__(self):
        return str(self.name)


# class UserKnowledgeRecord(models.Model):
#     created = models.DateTimeField(u'创建时间', auto_now_add=True)
#     done_time = models.DateTimeField(u'完成时间', null=True, blank=True)
#
#     task_knowledge = models.ForeignKey(TaskKnowledgeRelation, verbose_name=u'任务知识点关系')
#     student_id = models.IntegerField(u'学生ID', db_index=True)
#     class_id = models.IntegerField(u'班级ID', db_index=True)
#
#     user_task_record = models.ForeignKey(UserTaskRecord, verbose_name=u"用户任务记录")
#
#     class Meta:
#         verbose_name = '学生知识点记录'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return str(self.id)
#
#     @property
#     def student(self):
#         students = UserProfile.objects.filter(pk=self.student_id)
#         return students[0] if students else None


class KnowledgeItem(models.Model):
    TYPE_CHOICES = (
        ('LESSON', '课程视频'),
        ('PROJECT', '项目制作'),
        ('TEST', '限时答题'),
        ('CODE', '在线编程'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='LESSON')
    obj_id = models.IntegerField(u'对象ID')
    expect_time = models.SmallIntegerField(u'预期时长：分钟(限时答题)', null=True, blank=True)
    index = models.SmallIntegerField(u'排列顺序(从小到大)', default=999)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    parent = models.ForeignKey(Knowledge, verbose_name=u'所属知识点')

    class Meta:
        verbose_name = '知识点项'
        verbose_name_plural = verbose_name
        unique_together = (('obj_type', "obj_id", "parent"),)

    def __unicode__(self):
        return str(self.id)

    __obj = None

    @property
    def name(self):
        if self.obj:
            if self.obj_type in ("TEST", "PROJECT"):
                return self.obj.title
            else:  #
                return self.obj.name
        else:
            return u""

    @property
    def obj(self):
        if self.obj_type == 'LESSON':
            objs = Lesson.objects.filter(id=self.obj_id)
            return objs[0] if objs else None
        elif self.obj_type == 'PROJECT':
            objs = Project.objects.filter(id=self.obj_id)
            return objs[0] if objs else None
        elif self.obj_type == 'TEST':
            objs = Examine.objects.filter(id=self.obj_id)
            return objs[0] if objs else None
        return None


class UserKnowledgeItemRecord(models.Model):
    STATUS_CHOICES = (
        ('DOING', '已开始'),
        ('DONE', '已完成'),
        # ('PASS', '已通过'),
        # ('FAIL', '未通过'),
    )
    status = models.CharField(u'状态', max_length=10, choices=STATUS_CHOICES, default='DOING')
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    done_time = models.DateTimeField(u'完成时间', null=True, blank=True)

    knowledge_item = models.ForeignKey(KnowledgeItem, verbose_name=u'任务知识点项')
    student_id = models.IntegerField(u'学生ID', db_index=True)
    class_id = models.IntegerField(u'班级ID', db_index=True)

    user_task_record = models.ForeignKey(UserTaskRecord, verbose_name=u"用户任务记录")
    # user_knowledge_record = models.ForeignKey(UserKnowledgeRecord, verbose_name=u"用户知识点记录")

    class Meta:
        verbose_name = '学生知识点项记录'
        verbose_name_plural = verbose_name
        unique_together = (('knowledge_item', 'student_id', 'class_id', 'user_task_record'),)

    def __unicode__(self):
        return str(self.id)

    @property
    def student(self):
        students = UserProfile.objects.filter(pk=self.student_id)
        return students[0] if students else None


class StudyHistory(models.Model):
    student_id = models.IntegerField(u'学生ID', db_index=True)
    class_id = models.IntegerField(u'班级ID', db_index=True)
    content = models.CharField(u'内容', max_length=100)  # log
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '学习历程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    @property
    def student(self):
        students = UserProfile.objects.filter(pk=self.student_id)
        return students[0] if students else None


class ClassRank(models.Model):
    # guotao
    class_id = models.IntegerField(u'班级ID', db_index=True)
    classmeeting_id = models.IntegerField(u'周直播班会ID', db_index=True)
    student_id = models.IntegerField(u"学生id", db_index=True)
    rank = models.IntegerField(u"班级排名", default=None, null=True)
    total_score = models.IntegerField(u"班级总成绩", default=None, null=True)
    rank_change = models.IntegerField(u'排名变化', default=None, null=True)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '班级排名表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    @property
    def student(self):
        students = UserProfile.objects.filter(pk=self.student_id)
        return students[0] if students else None


class ClassMeeting(models.Model):
    student_id = models.IntegerField(u"学生id", default=None, null=True, db_index=True)
    create_datetime = models.DateTimeField(u"创建时间", auto_now_add=True)
    startline = models.DateTimeField(u"班会时间", null=True, blank=True)
    status = models.SmallIntegerField(u"状态", default=1, choices=((0, "未开始"), (1, "已结束"), (2, "进行中")))
    finish_date = models.DateTimeField(u"实际完成时间", null=True, blank=True)
    content = models.CharField(u"内容", null=True, blank=True, max_length=100)
    is_temp = models.BooleanField(u'是否临时创建', default=False)
    create_id = models.IntegerField(u"用户id", default=None, null=True, db_index=True)

    class Meta:
        verbose_name = "班会"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class ClassMeetingRelation(models.Model):
    """ClassTmpMetting"""
    class_meeting = models.ForeignKey(ClassMeeting)
    class_id = models.IntegerField(verbose_name=u"班级id", db_index=True)

    class Meta:
        verbose_name = "班级ID和班会关系表"
        verbose_name_plural = verbose_name
        unique_together = (("class_meeting", "class_id"),)

    def __unicode__(self):
        return str(self.id)


# 直播室Model
class LiveRoom(models.Model):
    live_id = models.CharField(u"直播室ID", null=True, blank=True, max_length=15)
    live_code = models.CharField(u"课堂编号", null=True, blank=True, max_length=15)
    assistant_token = models.CharField(u"助教口令", null=True, blank=True, max_length=10)
    student_token = models.CharField(u"Web端学生口令", null=True, blank=True, max_length=10)
    teacher_token = models.CharField(u"老师口令", null=True, blank=True, max_length=10)
    student_client_token = models.CharField(u"学生客户端口令", null=True, blank=True, max_length=10)
    student_join_url = models.CharField(u"学生加入直播室地址", null=True, blank=True, max_length=100)
    teacher_join_url = models.CharField(u"老师和助教加入直播室地址", null=True, blank=True, max_length=100)
    date_publish = models.DateTimeField(u"建立时间", auto_now_add=True)
    class_meeting = models.OneToOneField(ClassMeeting, verbose_name=u"直播室关联临时班会", unique=True)

    class Meta:
        verbose_name = "直播室"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

class ClassMeetingMobileRecord(models.Model):
    """
    班会是否用手机发送过记录
    """
    class_meeting = models.OneToOneField(ClassMeeting, verbose_name=u"手机发送记录关联班会", unique=True)
    start_3hour_ago = models.BooleanField(u'班会开启3小时前', default=False)

    def __unicode__(self):
        return str(self.id)

class ClassMeetingVideo(models.Model):
    # guotao
    class_id = models.IntegerField(verbose_name=u"班级id", db_index=True)
    live_id = models.CharField(u"直播室id", max_length=200, default='')
    play_id = models.CharField(u"播放id", max_length=200, default='')
    play_subject = models.CharField(u"视频主题", null=True, blank=True, max_length=200, default='')
    create_time = models.DateTimeField(u"创建时间", null=True, blank=True)
    token = models.CharField(u"token", null=True, blank=True, max_length=50, default='')
    creator = models.IntegerField(default=0, verbose_name=u"视频上传者")
    url = models.CharField(u"播放url", max_length=200, default='', blank=True)
    description = models.CharField(u"描述", max_length=200, default='', blank=True)
    number = models.CharField(u"number", max_length=200, default='', blank=True)

    class Meta:
        verbose_name = "直播班会的视频信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.play_id)


class ClassMeetingAttendance(models.Model):
    # 考勤
    STATUS_CHOICES = {
        'punctual': u'正常出席',
        'late': u'迟到',
        'absent': u'缺席',
    }
    status = models.CharField(u'状态', max_length=10, choices=STATUS_CHOICES.items(), default='punctual')
    class_meeting_id = models.IntegerField(u"班会id", db_index=True)
    student_id = models.IntegerField(verbose_name=u"学生id")
    liveroom_in_time = models.DateTimeField(u"进入直播课时间", null=True, blank=True)
    liveroom_out_time = models.DateTimeField(u"离开直播课时间", null=True, blank=True)

    class Meta:
        verbose_name = "班会考勤表"
        verbose_name_plural = verbose_name

    @property
    def status_text(self):
        return self.STATUS_CHOICES.get(self.status)

    @property
    def class_meeting(self):
        class_meeting = ClassMeeting.objects.filter(pk=self.class_meeting_id)
        return class_meeting[0] if class_meeting else None

    def __unicode__(self):
        return str(self.id)


class ClassRankRecord(models.Model):
    """
    班级排名，支持按照不同的标准和时间间隔进行排名
    """
    TYPE_CHOICES = {
        '1': u'班级成绩每天排名',
        '2': u'班级进度每天排名',
    }
    rank_type = models.CharField(u'排名类型', max_length=10, choices=TYPE_CHOICES.items(), default='1')
    class_id = models.IntegerField(u'班级ID', db_index=True)
    rank_detail = models.TextField(u'排名详情', default='', null=True)
    rank_date = models.DateTimeField(u'统计时间', auto_now_add=True)

    class Meta:
        db_table = "mz_lps3_classrankrecord"
        verbose_name = '班级排名记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
