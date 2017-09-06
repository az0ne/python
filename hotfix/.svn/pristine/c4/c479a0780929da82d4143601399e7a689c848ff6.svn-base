#!/usr/bin/python
# -*- coding:utf-8 -*-

# version 2.0
# version 2.1
# modify record
#  AppConsultInfo增加了 uniquetogether
# -------------
# version 2.3
# modify record
#  MyMessage的action_types 增加了 4 教师督促学生
# -------------
from django.db import models
# from datetime import datetime
from django.conf import settings
from datetime import datetime, timedelta


# Create your models here.
class MyMessage(models.Model):
    action_types = (
        ('1', '系统消息'),
        ('2', '课程讨论回复'),
        ('3', '论坛讨论回复'),
        ('4', '教师督促学生'),
        ('5', '粉丝'),
        ('6', '赞'),
        ('7', '@我'),
        ('8', '系统推送消息'),
        ('9', '开始新课程学习'),
        ('10', '班级排名变化'),
        ('11', '项目制作成绩'),
        ('12', '班会开始'),
        ('13', '班会缺勤'),
        ('14', '超时提醒'),
        ('15', '完成任务'),
        ('16', '续费通知'),
        ('17', 'APP体验课程'),
        ('18', '新的班会通知'),
        ('19', '班会时间更改'),
        ('20', '转介绍'),
        ('21', '问答：提问被回复'),
        ('22', '问答：回复被回复'),
        ('23', '问答：有新的提问'),
        ('50', '报名成功'),
        ('51', '项目提交')
    )

    class Meta:
        verbose_name = u'我的消息'
        verbose_name_plural = verbose_name

    userA = models.IntegerField(u"用户A")  # 发送方，为0表示系统用户
    userB = models.IntegerField(u"用户B")  # 接收方，为0就给所有用户发送消息
    action_type = models.CharField(u'类型', choices=action_types, max_length=2)
    action_id = models.IntegerField(u'动作id', blank=True, null=True)
    action_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u"添加日期", auto_now_add=True)
    is_new = models.BooleanField(u'是否为最新', default=True)

    def __unicode__(self):
        return str(self.id)


class Log(models.Model):
    log_types = (
        ('1', '班级管理'),
    )

    class Meta:
        verbose_name = u'日志'
        verbose_name_plural = verbose_name

    userA = models.IntegerField(u"用户A")
    userB = models.IntegerField(u"用户B", blank=True, null=True)
    log_type = models.CharField(u'类型', choices=log_types, max_length=1)
    log_id = models.IntegerField(u'动作id', blank=True, null=True)
    log_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u'添加日期', auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class Ad(models.Model):
    class Meta:
        verbose_name = u'网站广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(u'广告描述', max_length=200)
    image_url = models.ImageField(u'图片路径(课程列表页与老师列表页广告图片上传大小为500*40）)', upload_to='ad/%Y/%m')
    back_image = models.CharField("图片背景虚化图", null=True, blank=True, max_length=100)
    callback_url = models.URLField(u'回调url', null=True, blank=True)
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    type = models.SmallIntegerField(default=0, choices=((0, "首页"), (1, "课程列表页"), (2, "老师列表页"),), verbose_name="广告类型")

    def __unicode__(self):
        return self.title


class AppAd(models.Model):
    ad_types = (
        ('0', '课程'),
        ('1', '企业直通班'),
        ('2', '问答'),
        ('3', '文章'),
        ('4', '活动'),
        ('5', '外链'),
    )

    class Meta:
        verbose_name = u'App广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(u'广告描述', max_length=200, blank=True, null=True)
    image_url = models.ImageField(u'图片路径', upload_to='ad/%Y/%m')
    ad_type = models.CharField(u'广告类型', choices=ad_types, max_length=1)
    target_id = models.IntegerField(u'跳转目标ID')
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    callback_url = models.URLField(u'回调url', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Links(models.Model):
    title = models.CharField(u'标题', max_length=50)
    description = models.CharField(u'友情链接描述', max_length=200)
    image_url = models.ImageField(u'图片路径', upload_to='links/%Y/%m', null=True, blank=True)
    callback_url = models.URLField(u'回调url')
    is_pic = models.BooleanField(u'是否为图片', default=False)

    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Keywords(models.Model):
    name = models.CharField(u'关键词', max_length=50)

    class Meta:
        verbose_name = u'关键词'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class RecommendKeywords(models.Model):
    name = models.CharField(u'推荐搜索关键词', max_length=50)

    class Meta:
        verbose_name = u'推荐搜索关键词'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class PageSeoSet(models.Model):
    page_name_types = (
        ('1', '首页'),
        ('2', '移动app'),
        ('3', '职业课程'),
        ('4', '课程列表页'),
        ('5', '教师列表页'),
        ('6', '企业直通班页')
    )
    page_name = models.CharField("单页名称", choices=page_name_types, max_length=3, null=True, blank=True)
    seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)

    class Meta:
        verbose_name = u'单页SEO设置'
        verbose_name_plural = verbose_name
        unique_together = (("page_name",),)

    def __unicode__(self):
        return self.page_name


class MobileVerifyRecord(models.Model):
    '''
    手机验证码记录表
    '''

    code = models.CharField(max_length=6, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    type = models.SmallIntegerField(default=0, choices=((0, "注册"), (1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    source = models.IntegerField(default=3, choices=((1, "pc"), (2, "手机"), (3, "未知")), verbose_name="来源")

    class Meta:
        verbose_name = "手机验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code


class EmailVerifyRecord(models.Model):
    '''
    邮箱验证记录表（包括注册和忘记密码使用到的验证链接）
    '''

    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.CharField(max_length=50, verbose_name="邮箱")
    type = models.SmallIntegerField(default=0, choices=((0, "注册"), (1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "邮箱验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code


class Coupon(models.Model):
    # endtime = datetime.now() + timedelta(days=90)
    surplus = models.IntegerField(verbose_name=u"剩余张数")
    coupon_price = models.CharField(max_length=20, verbose_name=u"优惠金额")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    endtime = models.DateTimeField(auto_now_add=True, verbose_name=u"结束时间")

    class Meta:
        verbose_name = u"优惠码"
        verbose_name_plural = verbose_name


class Coupon_Details(models.Model):
    code_sno = models.CharField(max_length=20, unique=True, verbose_name=u"优惠码")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=u"用户")
    use_time = models.CharField(max_length=50, default=None, verbose_name=u"使用时间")
    is_use = models.BooleanField(default=False, verbose_name=u"是否使用")
    is_lock = models.BooleanField(default=False, verbose_name=u"是否锁定")
    coupon = models.ForeignKey(Coupon, verbose_name="id")
    careercourse_id = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"职业课程id")

    class Meta:
        verbose_name = u"优惠码详情"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code_sno


class RecommendedReading(models.Model):
    ACTIVITY = 'AV'
    NEWS = 'NW'
    DISCUSS = 'DC'

    READING_TYPES = (
        (ACTIVITY, '官方活动'),
        (NEWS, '开发者资讯'),
        (DISCUSS, '技术交流'),
    )

    reading_type = models.CharField(max_length=2,
                                    choices=READING_TYPES,
                                    default=ACTIVITY
                                    )

    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "首页推荐文章"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


# 消息推送Model
class MsgBox(models.Model):
    sendtarget=models.SmallIntegerField(u"发送对象",default="-1", null=True, blank=True, choices=((-1,u"全部"),(0, u"学生"), (1,u"老师"),))
    content=models.TextField(u'消息内容')
    date_send = models.DateTimeField(u"发送时间", auto_now_add=True)
    is_sendmsg = models.BooleanField(u"是否发送站内信", default=False)
    is_sendemail = models.BooleanField(u"是否发送邮件", default=False)
    is_sendappmsg = models.BooleanField(u"是否推送App消息", default=False)

    class Meta:
        verbose_name = "消息推送记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# （app）留言反馈model
class Feedback(models.Model):
    feed_types = (
        (0, '默认'),
        (1, '课程是硬伤'),
        (2, '32个赞'),
        (3, '天呐！有bug'),
        (4, '差评！'),
        (5, '我有idea'),
    )
    feed_type = models.SmallIntegerField(u'反馈类型', default=0, choices=feed_types)
    user_id = models.IntegerField(u"用户ID", default=None, null=True)
    content = models.TextField(u'反馈内容')
    date_publish = models.DateTimeField(u"发布时间", auto_now_add=True)

    class Meta:
        verbose_name = "留言反馈"
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)


# （app）版本管理
class AndroidVersion(models.Model):
    TYPE_STUDENT = 1
    TYPE_TEACHER = 2
    APP_TYPE = {TYPE_STUDENT: u'学生版', TYPE_TEACHER: u'老师版'}
    vno = models.CharField(max_length=10, verbose_name="版本号")
    size = models.CharField(max_length=10, verbose_name="文件大小", null=True, blank=True)
    desc = models.TextField(null=True, blank=True, verbose_name="功能简介")
    is_force = models.BooleanField(default=False, verbose_name="是否强制更新")
    down_url = models.CharField(max_length=100, verbose_name="下载地址")
    type = models.IntegerField(u'app版本', default=TYPE_STUDENT)

    class Meta:
        verbose_name = "版本管理"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return str(self.id)


# Add by Steven YU
# 组织结构基类
class Org(models.Model):
    name = models.CharField("名称", unique=True, max_length=30)
    index = models.IntegerField("顺序(从小到大)", default=999)
    image = models.ImageField("小图标", upload_to="org/%Y/%m", null=True, blank=True)
    big_image = models.ImageField("大图标", upload_to="org/%Y/%m", null=True, blank=True)
    app_image = models.ImageField("app端小图标", upload_to="org/%Y/%m", null=True, blank=True)
    description = models.TextField("介绍", null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父级机构")
    level = models.IntegerField("级别", default=1)

    class Meta:
        verbose_name = "组织机构"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 手机活动页面咨询统计信息
class AppConsultInfo(models.Model):
    market_types = (
        ('sem', 'SEM'),
        ('10086', '中国移动'),
        ('operate', '运营'),
        ('trad', '传统培训'),
    )

    name = models.CharField("姓名", max_length=30, null=True, blank=True)
    phone = models.CharField("电话", max_length=30, null=True, blank=True)
    qq = models.CharField("QQ", max_length=30, null=True, blank=True)
    interest = models.CharField("兴趣方向", max_length=50, null=True, blank=True)
    source = models.CharField("来源", max_length=50, null=True, blank=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)

    market_from = models.CharField("市场推广来源", default='sem', max_length=20, null=True, blank=True, choices=market_types)

    class Meta:
        verbose_name = "手机活动页咨询统计"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = (("name", "phone", "qq", "interest"),)

    def __unicode__(self):
        return self.name


class MaiziDeparment(models.Model):
    name = models.CharField("部门", max_length=30)
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "麦子学院部门"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class RecruitPosition(models.Model):
    department = models.ForeignKey(MaiziDeparment, verbose_name="部门")
    title = models.CharField("职位", max_length=30)
    desc = models.TextField("描述", max_length=1000)
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "招聘职位"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


# 新手问答与课程页常见问答
class FAQ(models.Model):
    title = models.CharField("标题", max_length=200)
    content = models.TextField("内容", max_length=1000)
    type = models.SmallIntegerField(default=0, choices=((0, "新手问答页"), (1, "课程页"),), verbose_name="问答类型")
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class ObjTagRelation(models.Model):
    '''对象标签关系'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    tag_id = models.IntegerField(u'标签ID', db_index=True)
    careercatagory_id = models.IntegerField(u'专业方向ID', db_index=True)

    class Meta:
        verbose_name = u'对象标签关系'
        verbose_name_plural = verbose_name


class ObjTagIndex(models.Model):
    '''对象标签索引'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    keywords = models.CharField(u'关键字', max_length=500, db_index=True)

    class Meta:
        verbose_name = u'对象标签索引'
        verbose_name_plural = verbose_name


class ObjSEO(models.Model):
    '''对象SEO'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
        ('CAREERCOURSELINE',u'职业课程路线'),
        ('LESSON', '视频'),
        ('ARTICLETYPE', '文章'),  # 文章分类页面SEO
    )
    obj_type = models.CharField(u'对象类型', max_length=20, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    seo_title = models.CharField(u'SEO title', max_length=500)
    seo_keywords = models.CharField(u'SEO keywords', max_length=500)
    seo_description = models.CharField(u'SEO description', max_length=500)

    class Meta:
        verbose_name = u'对象SEO'
        verbose_name_plural = verbose_name


################李希临时添加到此处############################

class CareerObjRelation(models.Model):
    '''职业与对象关系'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
        ('LESSON', '视频'),
    )
    career_id = models.IntegerField(u'职业课程ID', db_index=True)
    obj_id = models.IntegerField(u'对象ID', db_index=True)
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'职业与对象关系'
        verbose_name_plural = verbose_name


class CareerAd(models.Model):
    '''职业对应广告'''
    '''评论列表'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章详情'),
        ('COURSE', '课程'),
    )
    career_id = models.IntegerField(u'职业课程ID', db_index=True)
    img_url = models.CharField(u'对象类型', max_length=500)
    img_title = models.CharField(u'图片title', max_length=500)
    type = models.CharField(u'对象类型', choices=TYPE_CHOICES, default='COURSE', max_length=20)
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'职业对应广告'
        verbose_name_plural = verbose_name

class UserCenterAd(models.Model):
    '''个人中心对应广告'''
    img_url = models.CharField(u'对象类型', max_length=500)
    img_title = models.CharField(u'图片title', max_length=500)
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'个人中心对应广告'
        verbose_name_plural = verbose_name


class NewArticle(models.Model):
    '''文章'''
    title = models.CharField(u'文章标题', max_length=200)
    content = models.TextField(u'内容')
    abstract = models.CharField(u'摘要', max_length=200)
    title_image = models.CharField(u'文章配图', max_length=200)
    is_top = models.BooleanField(u'是否置顶', default=False)
    user_id = models.IntegerField(u'发表用户ID')
    nick_name = models.CharField(u'昵称', max_length=50)
    user_head = models.CharField(u'用户头像', max_length=200)
    replay_count = models.IntegerField(u'回复数量')
    praise_count = models.IntegerField(u'点赞数量')
    publish_date = models.DateTimeField(u'发布日期')
    article_type_id = models.IntegerField(u'类型', db_index=True)
    is_top= models.BooleanField(u'是否置顶', default=False)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

class UserPraise(models.Model):
    '''用户文章点赞'''
    user_id = models.IntegerField(u'点赞用户ID')
    article_id = models.IntegerField(u'点赞文章ID')

    class Meta:
        verbose_name = u'文章用户点赞记录'
        unique_together = ('user_id', 'article_id')

class ArticleType(models.Model):
    '''文章类型'''
    name = models.CharField(u'文章类型', max_length=50)
    short_name = models.CharField(u'文章类型', max_length=50)
    is_homepage = models.BooleanField(u'是否首页显示', default=False)

    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name


class NewDiscuss(models.Model):
    '''评论列表'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('LESSON', '视频'),
    )
    object_id = models.IntegerField(u'对象ID', default=0, db_index=True)
    object_type = models.CharField(u'对象类型', choices=TYPE_CHOICES, default='ARTICLE', max_length=20)
    comment = models.TextField(u'评论', blank=True, null=True)
    user_id = models.IntegerField(u'用户ID', db_index=True)
    nick_name = models.CharField(u'昵称', max_length=50, blank=True, null=True)
    head = models.CharField(u'头像', max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    parent_id = models.IntegerField(u'父级评论_id', default=0, db_index=True)

    class Meta:
        verbose_name = u'评论列表'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    image_title = models.CharField(u'图片标题', max_length=200)
    image_url = models.ImageField(u'图片', upload_to='banner/%Y/%m')
    url = models.URLField(u'链接', null=True, blank=True)
    index = models.IntegerField(u'序号', default=0, db_index=True)
    bgcolor = models.CharField(u'背景颜色', max_length=50, default=0)
    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class HotTeacherResume(models.Model):
    teacher_id = models.IntegerField(u'教师id', default=0, db_index=True)
    start_time = models.CharField(u'开始时间', max_length=10)
    end_time = models.CharField(u'结束时间', max_length=10)
    company = models.CharField(u'公司名称', max_length=50)
    title = models.CharField(u'职位', max_length=50)
    project1 = models.CharField(u'项目1', max_length=100)
    project2 = models.CharField(u'项目2', max_length=100)
    project3 = models.CharField(u'项目3', max_length=100)
    project4 = models.CharField(u'项目4', max_length=100)
    project5 = models.CharField(u'项目5', max_length=100)

    class Meta:
        verbose_name = u'教师简历'
        verbose_name_plural = verbose_name


class HotTeacherStudentWorks(models.Model):
    teacher_id = models.IntegerField(u'教师id', default=0, db_index=True)
    type = models.CharField(u'所属人', max_length=10)
    image_url = models.ImageField(u'作品url', upload_to='HotTeacherStudentWorks/%Y/%m')
    image_title = models.CharField(u'作品描述', max_length=500)
    url = models.URLField(u'链接地址', null=True, blank=True)

    class Meta:
        verbose_name = u'教师学生作品'
        verbose_name_plural = verbose_name


class HotTeacher(models.Model):
    name = models.CharField(u'教师姓名', max_length=50)
    info = models.CharField(u'教师简介', max_length=500)
    wishes = models.CharField(u'寄语', max_length=500)
    class_count = models.IntegerField(u'带班数')
    student_count = models.IntegerField(u'毕业人数')
    employment_rate = models.IntegerField(u'就业率')
    is_homepage = models.BooleanField(u'是否在首页显示', default=False)

    class Meta:
        verbose_name = u'首页教师'
        verbose_name_plural = verbose_name


class NewAd(models.Model):
    TYPE_CHOICES = (
        ('ARTICLE', '文章列表'),
        ('COURSELIST', '课程库'),
        ('UC', '个人中心'),
    )
    type = models.CharField(choices=TYPE_CHOICES, default='ARTICLE', max_length=10)
    img_url = models.ImageField(u'图片地址',max_length=500)
    img_title = models.CharField(u'图片标题', max_length=500)
    url = models.URLField(u'链接地址',null=True, blank=True)
    is_actived = models.BooleanField(u'是否被激活',default=False)

    class Meta:
        verbose_name = u'首页教师'
        verbose_name_plural = verbose_name