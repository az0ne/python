# -*- coding: utf-8 -*-
# version 2.0
# modify record
# -------------
# version 2.4
# modify record
# 增加字段 restore_datetime 在classstudents
# -------------
# version 2.7
# modify record
# 增加字段 result 在homeworkrecord
# -------------
import datetime
from django.db import models
from django.conf import settings
from django.forms.forms import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from mz_course.models import Lesson, Course, CareerCourse


# Create your models here.

class ClassManager(models.Manager):
    def get_queryset(self):
        # 调用父类的方法，在原来返回的QuerySet的基础上返回新的QuerySet
        return super(ClassManager, self).get_queryset().exclude(lps_version='3.0')

    def xall(self):
        return super(ClassManager, self).get_queryset()


# 班级
class Class(models.Model):
    CLASS_TYPE_NORMAL = 0
    CLASS_TYPE_EXPERIENCE = 1
    CLASS_TYPE_FREE = 2
    CLASS_TYPE_FREE_488 = 3
    CLASS_TYPE_EXPERIENCE_3_1 = 4
    CLASS_TYPE = {CLASS_TYPE_EXPERIENCE: u'体验班', CLASS_TYPE_NORMAL: u'正常付费班级',
                  CLASS_TYPE_FREE: u'app免费班级', CLASS_TYPE_FREE_488: u'488免费试学班',
                  CLASS_TYPE_EXPERIENCE_3_1: u'3.1体验班'}
    STATUS_ONGOING = 1
    STATUS_OVER = 2
    STATUS = {STATUS_ONGOING: u"进行中", STATUS_OVER: u"已结束"}
    name = models.CharField("班级名称", max_length=50, default=None, null=True)
    coding = models.CharField(u"班级编号", unique=True, max_length=30)
    date_publish = models.DateTimeField(u"创建日期", auto_now_add=True)
    date_open = models.DateTimeField(u"开课日期")
    student_limit = models.IntegerField(u"学生上限", default=35)
    current_student_count = models.IntegerField(u"当前报名数", default=0)
    is_active = models.BooleanField(u"有效性", default=True)
    status = models.SmallIntegerField(u"班级状态", default=1, choices=STATUS.items())
    qq = models.CharField(u"班级QQ群", max_length=13)
    qq_key = models.CharField("班级QQ群key", max_length=100, null=True, blank=True)
    qq_qrcode = models.ImageField("班级QQ群二维码(300*300)", upload_to='class_qq/qr_code')
    # teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"teacher", verbose_name=u"班级老师", null=True,
    #                             blank=True)
    edu_admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"edu_admin", verbose_name=u"教务老师",
                                  null=True, blank=True)
    monitor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"monitor", verbose_name=u"班长", null=True,
                                blank=True)  # 2016/4/11添加 by yf
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name=u"students",
                                      verbose_name=u"班级学生", through=u"ClassStudents")
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name=u"teachers",
                                      verbose_name=u"班级老师", through=u"ClassTeachers")
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程")

    is_closed = models.BooleanField(default=False, verbose_name=u"是否显示报名")
    lps_version = models.CharField(u"lps版本", max_length=16, blank=True, null=True)
    meeting_enabled = models.BooleanField(u"班会开启", default=False)
    meeting_start = models.DateTimeField(u"班会开始时间", blank=True, null=True)
    meeting_duration = models.SmallIntegerField(u"班会持续天数", blank=True, null=True)
    class_type = models.IntegerField(u"班级类型", choices=CLASS_TYPE.items(), default=CLASS_TYPE_NORMAL, db_index=True)

    objects = ClassManager()

    class Meta:
        verbose_name = u"班级"
        verbose_name_plural = verbose_name

    @property
    def teacher_name(self):
        return ','.join(teacher.staff_name for teacher in self.teachers.all())

    @property
    def teacher(self):
        """获取一个老师对象（解决多老师改版可能存在的BUG）"""
        return self.teachers.all()[0] if self.teachers.all() else None

    @property
    def eduadmin_name(self):
        return self.edu_admin.staff_name

    @property
    def course_name(self):
        return self.career_course.name

    @property
    def class_end_time(self):
        """班级毕业时间(为meeting_start加meeting_duration)"""
        now = datetime.datetime.now()
        # meeting_enabled为True,代表班级已开始
        if self.meeting_enabled:
            # meeting_start没有值时,取现在的时间
            # meeting_duration为班级持续时间,默认值为90
            end_time = (self.meeting_start or now) + datetime.timedelta(days=self.meeting_duration or 90)

            return end_time

    @property
    def class_left_days(self):
        """班级剩余天数"""
        now = datetime.datetime.now()
        # class_end_time有值,代表班级已开始
        if self.class_end_time:
            class_left_days = (self.class_end_time - now).days + 1

            return class_left_days

    def is_experience(self):
        """判断是否为体验班"""
        return self.class_type == self.CLASS_TYPE_EXPERIENCE

    def is_normal(self):
        """正常班级"""
        return self.class_type == self.CLASS_TYPE_NORMAL

    def is_free(self):
        """app免费班级"""
        return self.class_type == self.CLASS_TYPE_FREE

    def is_free488_class(self):
        """488免费试学班"""
        return self.class_type == self.CLASS_TYPE_FREE_488

    def __unicode__(self):
        return str(self.coding)

    @property
    def display_name(self):
        return self.name if self.name else self.coding


# 班级和学生产生的关联对象
class ClassStudents(models.Model):
    STATUS_NORMAL = 1
    STATUS_QUIT = 2
    STATUS = {STATUS_NORMAL: u'正常', STATUS_QUIT: u'退学'}
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"学生")
    student_class = models.ForeignKey(Class, verbose_name=u"班级")
    study_point = models.IntegerField("学生在该班级下的学力", default=0)
    is_view_contract = models.BooleanField(u"是否查看入学协议", default=False)  # add for lps2.0
    is_send_sms = models.BooleanField(u"是否已经发送短信（老师和教务）", default=False)  # add for 入学流程优化
    is_qq_hints = models.BooleanField(u"是否QQ加群提示提示", default=False)  # add for 入学流程优化
    is_employment_contract = models.NullBooleanField(u'是否需要就业', null=True, blank=True, default=None)  # add for 入学流程优化
    is_view_employment_contract = models.BooleanField(u'是否查看就业协议', default=False)  # add for lps3.0
    is_view_not_employment_contract = models.BooleanField(u'是否查看非就业的服务', default=False)  # add for lps3.0
    salary = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"就业承诺薪资")
    employment_contract_time = models.DateTimeField(u"就业协议填写时间", null=True, blank=True, default=None)
    student_degree = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"学生学历")
    student_intention_city = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"学生意向就业城市")
    is_pause = models.BooleanField(u"是否暂停", default=False)  # add for lps2.0
    # add for lps2.0，为None表示全部款项已付清
    deadline = models.DateTimeField("截止时间", null=True, blank=True, default=None)
    pause_reason = models.CharField("暂停原因", null=True, blank=True, max_length=200)
    pause_datetime = models.DateTimeField(u"暂停时间", null=True, blank=True, default=None)
    restore_datetime = models.DateTimeField(u"恢复时间", null=True, blank=True, default=None)
    # add for APP v3，提供学生最后学习时间
    latest_study_datetime = models.DateTimeField(u"最后学习时间", null=True, blank=True, default=None)
    created = models.DateTimeField(u"加入班级时间", null=True, auto_now_add=True)
    status = models.IntegerField(u"状态", choices=STATUS.items(), default=STATUS_NORMAL, db_index=True)
    quit_datetime = models.DateTimeField(u"退学时间", null=True, blank=True)
    start_work_time = models.IntegerField(u"开始工作时间", default=0)
    is_view_resume_intro = models.IntegerField(u"是否查看填写简历引导", default=0)

    class Meta:
        verbose_name = u"班级学生"
        verbose_name_plural = verbose_name
        unique_together = (("user", "student_class"),)
        ordering = ['-study_point']

    def can_study(self):
        """可以学习"""
        self.status in (self.STATUS_NORMAL,)

    @property
    def is_full_payment_user(self):
        """全款用户"""
        return not self.deadline

    @property
    def is_trial_user(self):
        """试学用户"""
        return bool(self.deadline)

    @property
    def pay_deadline(self):
        """支付截止时间"""
        return self.deadline + datetime.timedelta(days=5)

    @property
    def is_overdue(self):
        """超期(试学用户)"""
        return self.student_class.meeting_enabled and datetime.datetime.now() > self.pay_deadline

    @property
    def is_active(self):
        """当前活跃用户"""
        return self.status == self.STATUS_NORMAL and \
               ((self.is_full_payment_user and not self.is_pause)
                or (self.is_trial_user and not self.need_pay() and not self.is_overdue)
                )

    @property
    def deadline_str(self):
        """试学截止时间"""
        if self.deadline:
            return self.deadline.strftime('%Y-%m-%d %H:%M')
        else:
            return ''

    @property
    def pay_deadline_str(self):
        if self.deadline:
            return self.pay_deadline.strftime('%Y-%m-%d %H:%M')
        return ''

    @property
    def deadline_str_ch(self):
        """试学截止时间'年月日'"""
        if self.deadline:
            return self.deadline.strftime('%Y年%m月%d日')
        else:
            return ''

    @property
    def pay_deadline_str_ch(self):
        """缴费截止时间'年月日'"""
        if self.deadline:
            return self.pay_deadline.strftime('%Y年%m月%d日')
        return ''

    # @property
    # def deadline_seconds(self):
    #     """试学倒计时(秒)"""
    #     if self.deadline:
    #         _timedelta = self.deadline - datetime.datetime.now()
    #         if _timedelta:
    #             return _timedelta.total_seconds()
    #
    # @property
    # def pay_deadline_seconds(self):
    #     """付款倒计时(秒)"""
    #     if self.deadline:
    #         _timedelta = self.pay_deadline - datetime.datetime.now()
    #         if _timedelta:
    #             return _timedelta.total_seconds()

    def need_pay(self):
        """判断是否需要支付余款"""
        if not self.deadline:
            return False
        if not self.student_class.meeting_enabled:
            return False
        now = datetime.datetime.now()
        if self.deadline < now < self.pay_deadline:
            return True
        return False

# 班级老师关系表
class ClassTeachers(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"老师")
    teacher_class = models.ForeignKey(Class, verbose_name=u"班级")
    is_active = models.BooleanField(u'有效性', default=True)

    class Meta:
        verbose_name = u"班级老师"
        verbose_name_plural = verbose_name
        unique_together = (("teacher", "teacher_class"),)


# 课程学分对象
class CourseScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"cs_user", verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    lesson_score = models.IntegerField("随堂测验得分", null=True, blank=True, default=None)
    course_score = models.IntegerField("课堂总测验得分", null=True, blank=True, default=None)
    project_score = models.IntegerField("项目制作得分", null=True, blank=True, default=None)
    is_complete = models.BooleanField("是否完成课程", default=False)
    complete_date = models.DateTimeField("课程完成时的时间", null=True, blank=True, default=None)
    rebuild_count = models.SmallIntegerField("第几次重修", default=0)
    date_publish = models.DateTimeField("建立时间", auto_now_add=True)

    class Meta:
        verbose_name = u"课程学分"
        verbose_name_plural = verbose_name
        ordering = ['-rebuild_count']

    def __unicode__(self):
        return str(self.id)


# 学习计划
class Planning(models.Model):
    date_publish = models.DateTimeField("建立时间", auto_now_add=True)
    is_active = models.BooleanField("有效性", default=True)
    version = models.IntegerField("版本号", default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户")
    career_course = models.ForeignKey(CareerCourse, verbose_name="职业课程")

    class Meta:
        verbose_name = "学习计划"
        verbose_name_plural = verbose_name
        ordering = ['-version', '-id']
        unique_together = (("user", "career_course", "version"),)

    def __unicode__(self):
        return str(self.id)


# 学习计划项
class PlanningItem(models.Model):
    need_days = models.IntegerField("所需天数")
    course = models.ForeignKey(Course, verbose_name="课程")
    rebuild_count = models.SmallIntegerField("重修版本号", default=0)
    planning = models.ForeignKey(Planning, verbose_name="学习计划")

    class Meta:
        verbose_name = "学习计划项"
        verbose_name_plural = verbose_name
        ordering = ['id']
        unique_together = (("planning", "course", "rebuild_count"),)

    def __unicode__(self):
        return str(self.id)


# 计划暂停记录
class PlanningPause(models.Model):
    pause_date = models.DateTimeField("暂停时间")
    restore_date = models.DateTimeField("恢复时间", null=True, blank=True)
    reason = models.CharField("暂停原因", max_length=200)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pp_teacher", verbose_name="老师")
    planning = models.ForeignKey(Planning, verbose_name="学习计划")

    class Meta:
        verbose_name = "计划暂停记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 考核
class Examine(models.Model):
    EXAMINE_TYPE = (
        (1, "课后作业"),
        (2, "试卷"),
        (3, "在线练习"),
        (4, "人工任务"),
        (5, "项目制作"),
        (6, "限时答题"),  # lps 3.0
    )
    RELATION_TYPE = {
        (0, "知识点"),  # lps 3.0
        (1, "章节"),
        (2, "课程"),
        (3, "阶段"),
    }
    title = models.CharField("名称", max_length=200, default='')  # lps 3.0 增加名称
    description = models.TextField("考核描述")
    examine_type = models.IntegerField("考核类别", choices=EXAMINE_TYPE)
    relation_type = models.IntegerField("关联类型", choices=RELATION_TYPE)
    relation_id = models.IntegerField("关联ID", blank=True, null=True)
    is_active = models.BooleanField("有效性", default=True)
    date_publish = models.DateTimeField("建立时间", auto_now_add=True)
    score = models.IntegerField("分值", blank=True, null=True)
    study_point = models.IntegerField("学力", blank=True, null=True)

    class Meta:
        verbose_name = "考核管理"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    def validate_unique(self, exclude=None):
        # these next 5 lines are directly from the Model.validate_unique source code
        unique_checks, date_checks = self._get_unique_checks(exclude=exclude)
        errors = self._perform_unique_checks(unique_checks)
        date_errors = self._perform_date_checks(date_checks)
        for k, v in date_errors.items():
            errors.setdefault(k, []).extend(v)

        # here I get a list of all pairs of parent_org, alias from the database (returned
        # as a list of tuples) & check for a match, in which case you add a non-field
        # error to the error list
        # 如果不是Mission（人工考核任务），则需要在添加和修改时检查'examine_type', 'relation_type', 'relation_id'的唯一性
        if type(self) is not Mission and self.relation_type != 0:
            pairs = Examine.objects.exclude(pk=self.pk).values_list('examine_type', 'relation_type', 'relation_id')
            if (self.examine_type, self.relation_type, self.relation_id) in pairs:
                errors.setdefault(NON_FIELD_ERRORS, []).append('examine_type and relation_type and relation_id'
                                                               ' must be unique')

        # finally you raise the ValidationError that includes all validation errors,
        # including your new unique constraint
        if errors:
            raise ValidationError(errors)


# 项目制作考核
class Project(Examine):
    video_guide = models.URLField(u'视频讲解', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "项目制作考核"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 项目素材
class ProjectMaterial(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'项目制作', blank=True, null=True)
    name = models.CharField("项目素材名称", max_length=50)
    material = models.FileField(u'素材', upload_to="Project/Material/%Y/%m")

    class Meta:
        verbose_name = "项目素材"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 项目截图
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'项目制作', blank=True, null=True)
    image = models.ImageField(u'截图', upload_to='Project/ProjectImage/%Y/%m')

    class Meta:
        verbose_name = "项目截图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 课后作业
class Homework(Examine):
    class Meta:
        verbose_name = "课后作业"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 试卷
class Paper(Examine):
    class Meta:
        verbose_name = "试卷"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 试卷题目单选题，与试卷多对一的关系
class Quiz(models.Model):
    DEFAULT_ITEM_LIST = "[['A','选项'], ['B','选项'], ['C','选项'], ['D','选项']]"  # add for lps 3.0
    question = models.TextField("题目描述")
    item_list = models.TextField("题目选项", default=DEFAULT_ITEM_LIST)
    result = models.CharField("答案", max_length=1)
    index = models.IntegerField("试题顺序(从小到大)", default=999)
    paper = models.ForeignKey(Paper, verbose_name="试卷")

    class Meta:
        verbose_name = "试卷题目"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.question


# 在线代码练习
class CodeExercise(Examine):
    LANG_TYPE = {
        (1, "python"),
        (2, "php"),
        (3, "c"),
    }

    lang_type = models.IntegerField("语言类型", choices=LANG_TYPE)
    result = models.TextField("参考答案")

    class Meta:
        verbose_name = "代码练习"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"代码练习"


# 人工考核
class Mission(Examine):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="老师")
    name = models.CharField("任务名称", max_length=30)

    class Meta:
        verbose_name = "人工考核"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 考核记录
class ExamineRecord(models.Model):
    is_active = models.BooleanField("有效性", default=True)
    score = models.IntegerField("获得分数", default=None, blank=True, null=True)
    study_point = models.IntegerField("获得学力", default=None, blank=True, null=True)
    date_publish = models.DateTimeField("建立时间", auto_now_add=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="er_student", verbose_name="学生")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="er_teacher", verbose_name="评分老师", blank=True,
                                null=True)
    rebuild_count = models.SmallIntegerField("第几次重修", default=0)
    examine = models.ForeignKey(Examine, verbose_name="对应考核")

    class Meta:
        verbose_name = "考核记录"
        verbose_name_plural = verbose_name
        unique_together = (("student", "examine", "rebuild_count"),)

    def __unicode__(self):
        return str(self.id)


# 项目制作考核记录
class ProjectRecord(ExamineRecord):
    project = models.ForeignKey(Project, verbose_name="对应项目制作考核")
    desc = models.TextField("项目描述", null=True, blank=True)
    remark = models.TextField("项目考核评语", null=True, blank=True)
    upload_file = models.FileField("上传项目作品", upload_to="project/%Y/%m")

    class Meta:
        verbose_name = "考核记录_项目制作"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 项目制作考核记录截图
class ProjectRecordImage(models.Model):
    project_record = models.ForeignKey(ProjectRecord, verbose_name=u'项目制作考核记录', blank=True, null=True)
    image = models.ImageField(u'截图', upload_to='Project/ProjectRecordImage/%Y/%m')

    class Meta:
        verbose_name = "考核记录_项目制作截图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 课后作业记录
class HomeworkRecord(ExamineRecord):
    homework = models.ForeignKey(Homework, verbose_name="对应课后作业")
    upload_file = models.FileField("上传作品", upload_to="homework/%Y/%m")
    result = models.TextField("编码结果", null=True, blank=True)

    class Meta:
        verbose_name = "考核记录_课后作业"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 试卷记录
class PaperRecord(ExamineRecord):
    paper = models.ForeignKey(Paper, verbose_name="对应试卷")
    accuracy = models.DecimalField("正确率", null=True, blank=True, default=None, max_digits=3, decimal_places=2)

    class Meta:
        verbose_name = "考核记录_试卷考核"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 做题记录
class QuizRecord(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="对应试题")
    result = models.CharField("试题项结果", max_length=200)
    paper_record = models.ForeignKey(PaperRecord)

    class Meta:
        verbose_name = "考核记录_做题记录"
        verbose_name_plural = verbose_name
        unique_together = (("quiz", "paper_record"),)

    def __unicode__(self):
        return str(self.id)


# 在线练习结果
class CodeExerciseRecord(ExamineRecord):
    result = models.TextField("编码结果")
    code_exercise = models.ForeignKey(CodeExercise, verbose_name="对应代码练习")

    class Meta:
        verbose_name = "考核记录_代码练习"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"考核记录_代码练习"


class MissionRecord(ExamineRecord):
    mission = models.ForeignKey(Mission, verbose_name="对应人工考核")

    class Meta:
        verbose_name = "考核记录_人工考核"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 直播室Model
class LiveRoom(models.Model):
    live_id = models.CharField(u"直播室ID", null=True, blank=True, max_length=15)
    live_code = models.CharField(u"课堂编号", null=True, blank=True, max_length=15)
    live_is_open = models.SmallIntegerField(u"是否开启直播", default=0, null=True, blank=True,
                                            choices=((0, u"未开启"), (1, u"开启"),))
    assistant_token = models.CharField(u"助教口令", null=True, blank=True, max_length=10)
    student_token = models.CharField(u"Web端学生口令", null=True, blank=True, max_length=10)
    teacher_token = models.CharField(u"老师口令", null=True, blank=True, max_length=10)
    student_client_token = models.CharField(u"学生客户端口令", null=True, blank=True, max_length=10)
    student_join_url = models.CharField(u"学生加入直播室地址", null=True, blank=True, max_length=100)
    teacher_join_url = models.CharField(u"老师加入直播室地址", null=True, blank=True, max_length=100)
    date_publish = models.DateTimeField(u"建立时间", auto_now_add=True)
    live_class = models.OneToOneField(Class, verbose_name=u"直播室关联班级", unique=True)

    class Meta:
        verbose_name = "直播室"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
