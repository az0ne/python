# -*- coding: utf-8 -*-

# version 2.0
# version 2.1
# modify record
# 设置CareerCourse的short_name为unique
# -------------
# version 2.2
# modify record
# 增加了Model CourseResource
# -------------
# version 2.7
# modify record
# 增加了Lesson code_exercise_type
# -------------
from django.db import models
from django.conf import settings
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from datetime import datetime

from django.utils.functional import cached_property

from mz_common.models import Keywords


# Create your models here.
# 学院分类
class Institute(models.Model):
    name = models.CharField("学院名称", max_length=50)
    order = models.IntegerField("排序", max_length=50, default=0)
    keywords = models.CharField(u"关键字", max_length=100, null=True, blank=True)
    online_count = models.IntegerField(u"在线学习人数", default=0)
    link_course = models.CharField(u"关键字链接课程的英文缩写", max_length=50)

    class Meta:
        verbose_name = "学院分类"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name


# 折扣
class Discounted(models.Model):
    DISCOUNTED_TYPE = {
        '1': '折扣',
        '2': '现金',
    }
    type = models.CharField(u"折扣类型", max_length=10, choices=DISCOUNTED_TYPE.items(), default='1')
    content = models.PositiveIntegerField(u"折扣内容", default=None, null=True)
    name = models.CharField(u"活动说明", default=None, null=True, blank=True, max_length=20)

    class Meta:
        verbose_name = "优惠活动"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # 计算优惠金额
    def calc_discounted_price(self, price):
        if self.type == '1':
            return price * self.content / 100
        else:
            return self.content

    def __unicode__(self):
        return self.DISCOUNTED_TYPE[self.type] + '_' + str(self.content)


# 职业课程 models
class CareerCourse(models.Model):
    name = models.CharField("职业课程名称", max_length=50)
    short_name = models.CharField("职业课程英文名称简写", max_length=10, unique=True)
    image = models.ImageField("课程图标(160*160)", upload_to="course/%Y/%m")
    app_image = models.ImageField("课程小图标(24*24)", upload_to="course/%Y/%m", null=True, blank=True)
    app_career_image = models.ImageField("app图标", upload_to="course/%Y/%m", null=True, blank=True)
    description = models.TextField("文字介绍")
    student_count = models.IntegerField("学习人数", default=0)
    market_page_url = models.URLField("营销页面地址", blank=True, null=True)
    course_color = models.CharField("课程配色", max_length=50)
    discount = models.DecimalField("折扣", default=1, max_digits=3, decimal_places=2)
    click_count = models.IntegerField("点击次数", default=0)
    index = models.IntegerField("职业课程顺序(从小到大)", default=999)
    search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="搜索关键词")
    seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)
    # add by Steven YU
    course_scope = models.SmallIntegerField("课程类型", null=True, blank=True, choices=((0, "高校专区"), (1, "企业专区"),))
    product_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"产品ID")
    balance_product_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"产品尾款ID")

    status = models.IntegerField(default=0, choices=((0, "一般课程"), (1, "即将开班"), (2, "热门课程")), verbose_name="课程状态")
    guide_line_page = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"课程大纲页")
    qq = models.CharField("QQ群号", max_length=20, null=True, blank=True)
    qq_key = models.CharField("QQ群key", max_length=100, null=True, blank=True)
    is_hot = models.BooleanField(default=False, verbose_name=u"是否热门开班课程")
    institute_id = models.IntegerField("学院ID", default=0)  # guotao网站改版
    # add_by_zhangyunrui 网站改版20160118
    brief_intro = models.CharField(u"一句话介绍", max_length=150, null=True, blank=True)
    # add_by_zhangyunrui 网站改版20160216新增需求
    id_53kf = models.IntegerField(u"53客服id号", default=1, null=True, blank=True)
    course_color_px = models.CharField(u"介绍页课程配色", default="#3DBD9C", max_length=50, null=True, blank=True)
    image_px = models.ImageField(u"介绍页背景图片", default="course_image_px/aboutLessonbg.png",
                                 upload_to="course_image_px/%Y/%m", null=True, blank=True)
    image_px_2 = models.ImageField(u"介绍页第二屏背景图片", default="course_image_px_2/LessonImg001.png",
                                   upload_to="course_image_px_2/%Y/%m", null=True, blank=True)
    # add_by_zhangyunrui 网站改版20160216课程介绍页单独的介绍与tdk
    description_px = models.TextField(u"介绍页文字介绍", null=True, blank=True)
    seo_title_px = models.CharField(u"介绍页SEO标题", max_length=200, null=True, blank=True)
    seo_keyword_px = models.CharField(u"介绍页SEO关键词", max_length=200, null=True, blank=True)
    seo_description_px = models.TextField(u"介绍页SEO描述", null=True, blank=True)

    lps3_guide_task_id = models.IntegerField(u"lps3新手引导任务id", null=True, blank=True, db_index=True)
    # 订单管理
    try_price = models.PositiveIntegerField(u"试学价格", default=None, null=True)
    net_price = models.PositiveIntegerField(u"官网价格", default=None, null=True)
    discounted = models.ForeignKey(Discounted, verbose_name=u"优惠活动", null=True, blank=True)
    contract_price = models.PositiveIntegerField(u"合同价格", default=None, null=True, blank=True)
    # 488免费试学
    jobless_price = models.PositiveIntegerField(u"无需就业全款价格", default=None, null=True)
    enable_free_488 = models.BooleanField(u'是否开启488免费试学', default=False, db_index=True)
    is_class = models.BooleanField(u'是否可以报名', default=False)
    app_offline_image = models.ImageField("app离线图标", upload_to="course/%Y/%m", null=True, blank=True)
    # 视频播放页改版
    ad = models.ImageField(u"广告图片", null=True, blank=True)

    class Meta:
        verbose_name = "职业课程"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name

    @property
    def guide_task_id(self):
        from django.conf import settings
        return self.lps3_guide_task_id or getattr(settings,'GUIDE_TASK_ID',None) or 2

    # 优惠金额
    @cached_property
    def discounted_price(self):
        if self.discounted:
            return self.discounted.calc_discounted_price(self.net_price)
        else:
            return 0


class StageManager(models.Manager):
    def get_queryset(self):
        # 调用父类的方法，在原来返回的QuerySet的基础上返回新的QuerySet
        return super(StageManager, self).get_queryset().exclude(lps_version='3.0')

    def xall(self):
        return super(StageManager, self).get_queryset()


# 阶段 models
class Stage(models.Model):
    name = models.CharField("阶段名称", max_length=50)
    description = models.TextField("阶段描述")
    price = models.IntegerField("阶段价格")
    index = models.IntegerField("阶段顺序(从小到大)", default=999)
    is_try = models.BooleanField(default=False, verbose_name=u"是否是试学阶段")
    career_course = models.ForeignKey(CareerCourse, verbose_name="职业课程")

    # 首付款有效天数
    valid_days = models.IntegerField(default=30, verbose_name=u"有效时间")
    lps_version = models.CharField(u"lps版本", max_length=16, blank=True, null=True)

    objects = StageManager()

    class Meta:
        verbose_name = "课程阶段"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return '%s: %s' % (self.career_course, self.name)

        # def getCourseSet(self):
        #     # if self.course_set.count():
        #     #     return self.course_set.all()
        #     # else:
        #     return Course.objects.filter(stages_m = self)


# 课程 models
class Course(models.Model):
    name = models.CharField("课程名称", max_length=50)
    image = models.ImageField("课程封面", upload_to="course/%Y/%m")
    description = models.TextField("课程描述")
    is_active = models.BooleanField("有效性", default=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)
    need_days = models.IntegerField("无基础学生完成天数", default=7)
    need_days_base = models.IntegerField("有基础学生完成天数", default=5)
    student_count = models.IntegerField("学习人数", default=0)
    favorite_count = models.IntegerField("收藏次数", default=0)
    click_count = models.IntegerField("点击次数", default=0)
    # has_project = models.BooleanField("是否有项目考核", default=False)
    # has_examine = models.BooleanField("是否有课程总测验", default=True)
    is_novice = models.BooleanField("是否是新手课程", default=False)
    is_click = models.BooleanField("是否点击能进入课程", default=False)
    index = models.IntegerField("课程顺序(从小到大)", default=999)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="老师")
    stages_m = models.ManyToManyField(Stage, related_name="stages_m", blank=True, null=True, verbose_name="多阶段",
                                      through="Course_Stages_m")

    # stages = models.ForeignKey(Stage, blank=True, null=True, verbose_name="阶段")

    search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="小课程搜索关键词")
    # Add by Steven YU
    is_homeshow = models.BooleanField(u"是否在首页显示", default=False)
    # is_required = models.BooleanField(u"是否必修", default=True) # add fo lps2
    course_status = models.SmallIntegerField(u"课程状态", choices=((0, "更新中"), (1, "已完结"),), default=0)
    # add by guotao
    score_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="score_user", blank=True, null=True,
                                        verbose_name="课程用户评分", through="Course_User_Score")
    score_ava = models.FloatField("课程平均评分", default=0.0)
    need_pay = models.BooleanField(u"是否需要付费才能观看", default=False)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # def getStages(self, stage_id):
    #     stage=self.stages
    #     if stage_id>0:
    #         stage=Stage.objects.get(pk=stage_id)
    #     return stage

    def __unicode__(self):
        return self.name


# 阶段和课程产生的关联对象
class Course_Stages_m(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    stage = models.ForeignKey(Stage, verbose_name=u"阶段")
    is_required = models.BooleanField(u"是否必修", default=True)

    class Meta:
        verbose_name = u"阶段课程"
        verbose_name_plural = verbose_name
        unique_together = (("course", "stage"),)


class Course_User_Score(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    score = models.FloatField(u"课程评分", default=0.0)

    class Meta:
        verbose_name = u"课程用户评分"
        verbose_name_plural = verbose_name
        unique_together = (("course", "user"),)

    def __unicode__(self):
        return self.score


# 章节 models
class Lesson(models.Model):
    name = models.CharField("章节名称", max_length=50)
    video_url = models.CharField("视频资源URL", max_length=1000)
    video_length = models.IntegerField("视频长度（秒）")
    play_count = models.IntegerField("播放次数", default=0)
    share_count = models.IntegerField("分享次数", default=0)
    index = models.IntegerField("章节顺序(从小到大)", default=999)
    is_popup = models.BooleanField("是否弹出提示框（支付、登录）", default=False)
    course = models.ForeignKey(Course, verbose_name="课程")
    seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)
    # add by yuxin
    have_homework = models.BooleanField("是否有作业", null=False, blank=False, default=True)
    code_exercise_type = models.SmallIntegerField("在线编码类型", choices=((0, "无在线编码"), (1, "python"), (2, "php"),),
                                                  default=0)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 章节资源 models
class LessonResource(models.Model):
    name = models.CharField("章节资源名称", max_length=50)
    download_url = models.FileField("下载地址", upload_to="lesson/%Y/%m")
    download_count = models.IntegerField("下载次数", default=0)
    lesson = models.ForeignKey(Lesson, verbose_name="章节")

    class Meta:
        verbose_name = "章节资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 课程资源 models
class CourseResource(models.Model):
    name = models.CharField("课程资源名称", max_length=50)
    download_url = models.FileField("下载地址", upload_to="course/%Y/%m")
    download_count = models.IntegerField("下载次数", default=0)
    course = models.ForeignKey(Course, verbose_name="课程")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


from mz_lps.models import Class
# 章节讨论 models
class Discuss(models.Model):
    content = models.TextField("讨论内容")
    parent_id = models.IntegerField("父讨论ID", blank=True, null=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)

    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户")
    user_class = models.ForeignKey(Class, verbose_name="班级", null=True, blank=True)

    class Meta:
        verbose_name = "课程讨论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class CareerCatagory(models.Model):
    '''专业方向'''
    name = models.CharField(u'专业方向', max_length=50)

    class Meta:
        verbose_name = u'专业方向'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class CourseCatagory(models.Model):
    career_catagory = models.ForeignKey(CareerCatagory, verbose_name=u"课程方向")
    name = models.CharField(u"课程分类", max_length=50)
    is_hot_tag = models.BooleanField(default=False, verbose_name=u"是否热门标签")

    class Meta:
        verbose_name = u"课程分类"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class Tag(models.Model):
    '''标签'''
    name = models.CharField(u'标签', max_length=50)
    is_hot_tag = models.BooleanField(u'是否热门标签', default=False)

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class CareerTagRelation(models.Model):
    '''专业方向标签关系'''
    tag_id = models.IntegerField(u'标签ID', db_index=True)
    careercatagory_id = models.IntegerField(u'专业方向ID', db_index=True)

    class Meta:
        verbose_name = u'专业方向标签关系'
        verbose_name_plural = verbose_name


####这个会被删除
class CareerCourseRelation(models.Model):
    '''职业与课程关系'''
    careercourse_id = models.IntegerField(u'职业课程ID', db_index=True)
    course_id = models.IntegerField(u'课程ID', db_index=True)
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'职业与课程关系'
        verbose_name_plural = verbose_name


# class HotTags(models.Model):
#     name = models.CharField(max_length=50,verbose_name = u"标签名")
#     clicks = models.IntegerField(default=0,verbose_name = u"点击数")
#     index = models.IntegerField(default=0,verbose_name = u"排序")
#
#     class Meta:
#         verbose_name = u"热门标签"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return str(self.name)

def Post_Save_Handle(**kwargs):
    obj = kwargs['sender']
    created = False
    if kwargs.has_key('created'):
        created = kwargs['created']

    # 如果是添加新的课程章节，更新章节对应课程Course对象的最新发布时间
    if created and (obj is Lesson):
        inst = kwargs['instance']
        inst.course.date_publish = datetime.now()
        inst.course.save()


Signal.connect(post_save, Post_Save_Handle)


# add_by_zhangyunrui 网站改版20160118
class StudentProjectImage(models.Model):
    image_url = models.ImageField(u"学生作品图片", upload_to="student_project_image/%Y/%m", max_length=200)
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"学生作品图片"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class ShowStage(models.Model):
    name = models.CharField(u"阶段名称", max_length=50)
    description = models.TextField(u"阶段描述")
    task_knowledge_test = models.CharField(u"任务数、知识点数、测试项数", max_length=50, default="8,32,64")
    task_list = models.CharField(u"任务列表", max_length=200, default="任务一,任务二,任务三,任务四,任务五,任务六,任务七,任务八")
    image_url = models.ImageField(u"阶段图片", upload_to="show_stage/%Y/%m", max_length=200)
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"展示阶段"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class CourseDirection(models.Model):
    name = models.CharField(u"方向名称", max_length=20)
    career_course = models.ManyToManyField(CareerCourse, null=True, blank=True, verbose_name="相关职业课程")
    image = models.ImageField(u"app方向图标", upload_to="course/%Y/%m", null=True, blank=True)

    class Meta:
        verbose_name = u"职业课程方向"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class NewCareerCatagory(models.Model):
    '''专业方向'''
    name = models.CharField(u'专业方向', max_length=50)

    class Meta:
        verbose_name = u'专业方向'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)
