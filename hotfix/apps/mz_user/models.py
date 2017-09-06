
# -*- coding: utf-8 -*-

# version 2.0
# modify record
# 增加UserSocialProfile
# -------------
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, date
from django.core.mail import send_mail
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils.functional import cached_property
from mz_course.models import CareerCourse, Course, Lesson, Stage
from uuidfield import UUIDField
from django.core import signing

from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from fps_interface.interface import FpsInterface
from django.db import transaction
from fps_interface.models import Article, Discuss, CourseAsk
from mz_lps.models import Class, ClassStudents


# 学习目标
class StudyGoal(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"学习目标")
    index = models.IntegerField("学习目标顺序(从小到大)", default=999)

    class Meta:
        verbose_name = u"学习目标"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 学习基础
class StudyBase(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"学习基础")
    index = models.IntegerField("学习基础顺序(从小到大)", default=999)

    class Meta:
        verbose_name = u"学习基础"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CountryDict(models.Model):
    """
    国家字典
    """

    name = models.CharField(max_length=50, verbose_name=u"国家")
    index = models.IntegerField("国家顺序(从小到大)", default=999)

    class Meta:
        verbose_name = u"国家字典"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class ProvinceDict(models.Model):
    """
    省份字典
    """

    name = models.CharField(max_length=50, verbose_name=u"省份")
    index = models.IntegerField("省份顺序(从小到大)", default=999)
    country = models.ForeignKey(CountryDict, verbose_name=u"国家")

    class Meta:
        verbose_name = u"省份字典"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CityDict(models.Model):
    """
    城市字典
    """

    name = models.CharField(max_length=50, verbose_name=u"城市")
    index = models.IntegerField("城市顺序(从小到大)", default=999)
    province = models.ForeignKey(ProvinceDict, verbose_name=u"省份")

    class Meta:
        verbose_name = u"城市字典"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class BadgeDict(models.Model):
    """
    徽章字典
    """

    name = models.CharField(max_length=50, verbose_name=u"徽章名称")
    badge_type = models.SmallIntegerField(choices=((0, u"VIP徽章"), (1, u"职业课程徽章"),), verbose_name=u"徽章类型")
    badge_url = models.ImageField(upload_to='badge/%Y/%m', max_length=200, null=True, blank=True, verbose_name=u"徽章路径")
    career_course = models.OneToOneField(CareerCourse, null=True, blank=True, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"徽章字典"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Certificate(models.Model):
    """
    证书
    """

    name = models.CharField(max_length=50, verbose_name=u"证书名称")
    image_url = models.ImageField(upload_to='certificate/%Y/%m', max_length=200, null=True, blank=True,
                                  verbose_name=u"证书地址")
    career_course = models.OneToOneField(CareerCourse, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"证书字典"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class RegisterWay(models.Model):
    '''
    注册途径
    '''

    name = models.CharField(max_length=100, verbose_name=u"途径名称")

    class Meta:
        verbose_name = u"注册途径"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AcademicOrg(models.Model):
    '''
    高校专区
    '''
    name = models.CharField("名称", unique=True, max_length=30)
    index = models.IntegerField("顺序(从小到大)", default=999)
    image = models.ImageField("小图标", upload_to="org/%Y/%m", null=True, blank=True)
    big_image = models.ImageField("大图标", upload_to="org/%Y/%m", null=True, blank=True)
    app_image = models.ImageField("app端小图标", upload_to="org/%Y/%m", null=True, blank=True)
    description = models.TextField("介绍", null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父级机构")
    level = models.IntegerField("级别", default=1)
    token_key = models.CharField(u"验证码", max_length=30)
    url = models.CharField(u"链接", max_length=30)

    class Meta:
        verbose_name = u"高校专区"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    # 获取用户的高校专区登录token
    def get_user_token(self, uuid):
        if not uuid:
            return None
        data = dict(uuid=str(uuid))
        return signing.dumps(data, key=self.token_key)

    def __unicode__(self):
        return self.name


class UserProfileManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        根据用户名和密码创建一个用户
        """
        now = datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, email, password, True, True,
                                 **extra_fields)


# 专业技能
class ProfessionalSkill(models.Model):
    skill = models.CharField(max_length=50, verbose_name=u'专业技能')
    domain = models.CharField(max_length=20, verbose_name=u'专业领域', db_index=True)

    class Meta:
        verbose_name = "专业技能"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    继承AbstractUser，扩展用户信息
    """
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDERS = {GENDER_MALE: u'男', GENDER_FEMALE: u'女'}
    DEGREE_GZ = 1
    DEGREE_DZ = 2
    DEGREE_BK = 3
    DEGREE_SS = 4
    DEGREE_BS = 5
    DEGREES = {DEGREE_GZ: u'高中及以下',
               DEGREE_DZ: u'大专',
               DEGREE_BK: u'大学本科',
               DEGREE_SS: u'硕士',
               DEGREE_BS: u'博士'}
    IS_SERVICE_TRUE = 1
    IS_SERVICE_FALSE = 2
    IS_SERVICE_CHOICES = {IS_SERVICE_TRUE: u'在职', IS_SERVICE_FALSE: u'不在职'}
    SERVICE_YEAR_0 = 1
    SERVICE_YEAR_0_1 = 2
    SERVICE_YEAR_1_3 = 3
    SERVICE_YEAR_3_5 = 4
    SERVICE_YEAR_5_10 = 5
    SERVICE_YEAR_10 = 6
    SERVICE_YEAR_CHOICES = {SERVICE_YEAR_0: u'应届毕业生',
                            SERVICE_YEAR_0_1: u'1年以下',
                            SERVICE_YEAR_1_3: u'1-3年',
                            SERVICE_YEAR_3_5: u'3-5年',
                            SERVICE_YEAR_5_10: u'5-10年',
                            SERVICE_YEAR_10: u'10年以上'}

    uuid = UUIDField(auto=True)
    username = models.CharField("用户名", max_length=30, unique=True)
    first_name = models.CharField("名字", max_length=30, blank=True)
    last_name = models.CharField("姓氏", max_length=30, blank=True)
    email = models.EmailField("邮件地址", unique=True, null=True, blank=True)
    is_staff = models.BooleanField("职员状态", default=False, help_text="是否能够登录管理后台")
    is_active = models.BooleanField("是否激活", default=True, help_text="用户是否被激活，未激活则不能使用")
    is_disabled = models.BooleanField("是否禁用", default=False, help_text="用户是否被禁用，被禁用则不能使用")
    date_joined = models.DateTimeField("创建日期", auto_now_add=True)
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", unique=True, null=True, blank=True)
    avatar_url = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_big.png", max_length=200,
                                   blank=True, null=True, verbose_name=u"头像220x220")
    avatar_middle_thumbnall = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_middle.png",
                                                max_length=200, blank=True, null=True, verbose_name=u"头像104x104")
    avatar_small_thumbnall = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_small.png",
                                               max_length=200, blank=True, null=True, verbose_name=u"头像70x70")
    avatar_alt = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"头像ALT说明")
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"QQ号码")
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name=u"手机号码")
    wechat = models.CharField(max_length=75, blank=True, null=True, unique=True, verbose_name=u"微信号码")
    valid_email = models.SmallIntegerField(default=0, choices=((0, u"否"), (1, u"是"),), verbose_name=u"是否验证邮箱")
    valid_mobile = models.SmallIntegerField(default=0, choices=((0, u"否"), (1, u"是"),), verbose_name=u"是否验证手机")
    company_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"公司名")
    position = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"职位名")
    teach_feature = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"教学特点")
    description = models.TextField(blank=True, null=True, verbose_name=u"个人介绍")
    uid = models.IntegerField(blank=True, null=True, unique=True, verbose_name=u"对应ucenter用户ID")
    register_way = models.ForeignKey(RegisterWay, null=True, blank=True, verbose_name=u"注册途径")
    city = models.ForeignKey(CityDict, null=True, blank=True, verbose_name=u"城市")
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    badge = models.ManyToManyField(BadgeDict, null=True, blank=True, verbose_name=u"徽章")
    certificate = models.ManyToManyField(Certificate, null=True, blank=True, verbose_name=u"证书")
    mylesson = models.ManyToManyField(Lesson, null=True, blank=True, verbose_name=u"我的学习章节",
                                      through=u"UserLearningLesson")
    mystage = models.ManyToManyField(Stage, null=True, blank=True, verbose_name=u"我的解锁阶段", through=u"UserUnlockStage")
    myfavorite = models.ManyToManyField(Course, null=True, blank=True, verbose_name=u"我的收藏", through=u"MyFavorite")
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"设备Token")
    study_goal_opt = models.ForeignKey(StudyGoal, blank=True, null=True, verbose_name=u"学习目标选项")
    study_goal = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"学习目标")
    study_base_opt = models.ForeignKey(StudyBase, null=True, blank=True, verbose_name=u"学习基础选项")
    study_base = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"学习基础")

    # 高校专区
    academics = models.ManyToManyField(AcademicOrg, null=True, blank=True, verbose_name=u"高校专区")

    # add_by_zhangyunrui 网站改版20160118
    teacher_photo = models.ImageField(u"老师照片1920x650", upload_to="teacher_photo/%Y/%m", max_length=200, blank=True,
                                      null=True)
    teacher_video = models.URLField(u"老师视频", max_length=200, blank=True, null=True)

    # 转介绍
    invitation_code = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name=u'邀请码')

    real_name = models.CharField(u'真实姓名', max_length=30, blank=True, null=True)
    gender = models.IntegerField(u'性别', choices=GENDERS.items(), null=True)
    address = models.CharField(u'联系地址', max_length=200, blank=True, null=True)
    birthday = models.DateField(u'出生日期', null=True, default='1990-01-01')
    degree = models.IntegerField(u'学历', choices=DEGREES.items(), null=True)

    # 20160310周迭代
    intention_job_city = models.CharField(u'意向就业城市', max_length=10, blank=True, null=True)
    graduate_institution = models.CharField(u'毕业院校', max_length=30, blank=True, null=True)
    in_service = models.IntegerField(u'是否在职', choices=IS_SERVICE_CHOICES.items(), null=True)
    service_year = models.IntegerField(u'工作年限', choices=SERVICE_YEAR_CHOICES.items(), null=True)
    id_number = models.CharField(u'身份证号', max_length=18, blank=True, null=True)

    industry = models.CharField(u'所在行业', max_length=20, blank=True, null=True)
    to_industry = models.CharField(u'想从事的行业', max_length=20, blank=True, null=True)
    is_recommend = models.BooleanField(u"是否推荐课程", default=True)

    # 20160922
    is_already_guided = models.BooleanField(u"是否已经经历过lps3.1新手引导", default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    if settings.SESSION_COOKIE_NAME != 'maiziedu':
        def check_password(self, raw_password):
            """
            Returns a boolean of whether the raw_password was correct. Handles
            hashing formats behind the scenes.
            """
            def setter(raw_password):
                pass
                # self.set_password(raw_password)
                # self.save(update_fields=["password"])
            return check_password(raw_password, self.password, setter)

    @property
    def staff_name(self):
        """定义内部人员姓名,例如老师,教务"""
        return self.real_name or self.nick_name

    @property
    def show_position(self):
        """职位显示"""
        if self.is_edu_admin():
            return self.position or u'教务老师'
        elif self.is_teacher():
            return self.position or u'金牌讲师'
        return ''

    @property
    def gender_text(self):
        return self.GENDERS.get(self.gender, '')

    # @property
    # def degree_text(self):
    #     return self.DEGREES.get(self.degree, '')

    @property
    def age(self):
        today = date.today()

        def _calc_age(birthday, today):
            """计算年龄"""
            age = today.year - birthday.year
            if today.isoformat()[-5:] < birthday.isoformat()[-5:]:
                age -= 1
            return age

        if self.birthday:
            return _calc_age(self.birthday, today)
        else:
            return None

    def get_teacher_major(self):
        objs = Class.objects.xall().filter(
            teachers=self,
            lps_version='3.0',
        ).values(
            'career_course__short_name'
        ).order_by('career_course_id')
        if objs:
            return objs[0]['career_course__short_name']
        else:
            return ''

    def get_user_age(self):
        if not self.birthday:
            return 0
        return int((date.today() - self.birthday).days / 365)

    def is_all_info_registed(self):
        """判断是否已经完善学籍信息"""
        return self.nick_name and self.real_name and self.mobile and self.gender and self.address and \
               self.birthday and self.degree and self.study_goal_opt and self.study_base_opt and self.city and self.qq

    def uncompleted_field(self):
        """返回未完成的那一项"""
        for field in ('nick_name', 'real_name', 'mobile', 'gender', 'address', 'birthday', 'degree',
                      'study_goal_opt', 'study_base_opt', 'city', 'qq'):
            if not eval('self.' + field):
                return self._meta._name_map[field][0]._verbose_name

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @cached_property
    def user_groups(self):
        return [g.name for g in self.groups.all()] + [u'学生']

    # 是否是老师
    def is_teacher(self):
        return u'老师' in self.user_groups

    # 是否为教务老师
    def is_edu_admin(self):
        return u'教务' in self.user_groups

    # 是否是学生
    def is_student(self):
        """
        关于多权限问题,,无教务,老师等权限,才判定为学生
        :return:
        """
        return (u'学生' in self.user_groups) and not self.is_teacher() and not self.is_edu_admin()

    # 是否是高校老师
    def is_academic_teacher(self):
        if self.is_teacher() and self.academicuser_set.all().count() > 0:
            return True
        return False

    # 是否是高校学生
    def is_academic_student(self):
        if self.is_student() and self.academicuser_set.all().count() > 0:
            return True
        return False

    def is_paying_subscriber(self):
        """是否为付费用户"""
        return self.is_unlockstage()

    # 验证学生是否是企业直通班的学生
    def is_unlockstage(self):
        if not hasattr(self, '_is_unlockstage'):
            setattr(self, '_is_unlockstage', self.userunlockstage_set.all().exists())
        return self._is_unlockstage

    def is_lps2_user(self):
        """
        判断是否为LPS2用户
        """
        return ClassStudents.objects.filter(user_id=self.id).exclude(student_class__lps_version='3.0').exists()

    def has_job_intention_info(self):
        """
        是否需要展示就业信息
        :param user_id:用户ID
        :return:True or False
        """
        from mz_lps.models import ClassStudents

        result = ClassStudents.objects.filter(
            user__id=self.id, status=ClassStudents.STATUS_NORMAL,
            student_class__class_type=Class.CLASS_TYPE_NORMAL,
            is_view_employment_contract=True).exists()
        return result

    def __unicode__(self):
        return str(self.username)


class ThirdPartyUser(models.Model):
    user = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name=u'用户')
    partner = models.CharField(u'第三方', max_length=10)
    openid = models.CharField(u'openid', max_length=50)
    nickname = models.CharField(u'openid', max_length=50)
    token = models.CharField(u'令牌', max_length=200)
    date_add = models.DateTimeField(u'添加时间', auto_now_add=True)

    class Meta:
        verbose_name = u'第三方用户'
        verbose_name_plural = verbose_name
        unique_together = (('partner', 'openid'),)

    def __unicode__(self):
        return str(self.id)


class UserSocialProfile(models.Model):
    user = models.ForeignKey(UserProfile, null=False, blank=False, verbose_name=u"用户")
    study_days = models.IntegerField(u"学习天数", blank=True, null=True, default=0)
    study_point = models.IntegerField(u"学力值", blank=True, null=True, default=0)
    rank = models.IntegerField(u"排名", blank=True, null=True, default=0)


class MyCourse(models.Model):
    user = models.ForeignKey(UserProfile, related_name=u"mc_user", verbose_name=u"用户")
    course = models.CharField(max_length=10, verbose_name=u"课程ID")
    course_type = models.SmallIntegerField(choices=((1, u"课程"), (2, u"职业课程"),), verbose_name=u"课程类型")
    index = models.IntegerField(default=999, verbose_name=u"课程显示顺序(从小到大)")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"我的课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class MyFavorite(models.Model):
    user = models.ForeignKey(UserProfile, related_name=u"mf_user", verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    date_favorite = models.DateTimeField(auto_now_add=True, verbose_name=u"收藏时间")

    class Meta:
        verbose_name = u"我的收藏"
        verbose_name_plural = verbose_name
        unique_together = (("user", "course"),)

    def __unicode__(self):
        return str(self.id)


# 用户学习章节记录(我的章节)
class UserLearningLesson(models.Model):
    date_learning = models.DateTimeField("最近学习时间", auto_now=True)
    is_complete = models.BooleanField("是否完成观看", default=False)
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    user = models.ForeignKey(UserProfile, verbose_name="用户")

    class Meta:
        verbose_name = "我的章节"
        verbose_name_plural = verbose_name
        unique_together = (("user", "lesson"),)

    def __unicode__(self):
        return str(self.id)


# 用户解锁的具体阶段
class UserUnlockStage(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    stage = models.ForeignKey(Stage, null=True, blank=True, verbose_name=u"解锁的阶段")
    date_unlock = models.DateTimeField(auto_now_add=True, verbose_name=u"解锁时间")

    class Meta:
        verbose_name = "我的解锁阶段"
        verbose_name_plural = verbose_name
        unique_together = (("user", "stage"),)

    def __unicode__(self):
        return str(self.id)


class StarStory(models.Model):
    '''就业明星'''
    user = models.ForeignKey(UserProfile, verbose_name='学员')
    name = models.CharField('姓名', null=True, blank=True, max_length=30)
    image = models.ImageField(upload_to='starstory/%Y/%m', verbose_name='学员头像',
                              null=True, blank=True, max_length=50)
    position = models.CharField('岗位', null=True, blank=True, max_length=16)
    salary = models.IntegerField('薪资', null=True, blank=True)
    story_title = models.CharField('文章标题', null=True, blank=True,
                                   max_length=12)
    story_speech = models.CharField('感言', null=True, blank=True,
                                    max_length=50)
    story_url = models.URLField('文章链接', null=True, blank=True, max_length=50)
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    date_add = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '就业明星'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return str(self.id)


class ClassStudentDynamic(models.Model):
    '''直通班学员动态'''
    types = (
        (1, 'xxx加入了xxxx职业课程（还需展示班级号）：职业课程点击跳转到对应的课程页'),
        (2, 'xxx本周学习任务已经完成了100%啦！：所有本周学习任务大于等于100%的学员，都这样显示'),
        (3, 'xxx的课程作业《xxxx》被老师批改啦！：课程点击跳转到对应的课程播放页'),
        (4, 'xxx发表的文章：xxxx被同班同学回复啦！：文章点击跳转到对应文章详情页'),
        (5, 'xxx提交了课程：《xxxx》的项目实战作业！：课程点击跳转到对应的课程播放页'),
        (6, 'xxx在课程《xxxx》下的提问被同班同学回复啦！：课程点击跳转到对应的课程播放页'),
        (7, 'xxx发表了文章《xxxx》：文章点击跳转到对应文章详情页'),
    )
    user = models.ForeignKey(UserProfile, verbose_name='学员')
    type = models.IntegerField('动态类型', choices=types)
    obj_id = models.IntegerField('对象ID', null=True, blank=True)
    date_add = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '直通班学员动态'
        verbose_name_plural = verbose_name
        ordering = ['-date_add', '-id']

    @property
    def obj(self):
        '''动态对象'''
        if self.type in [1] and self.obj_id:
            clazz = Class.objects.filter(id=self.obj_id)
            if clazz:
                return clazz[0]
        if self.type in [2]:
            return 'complete'
        if self.type in [3, 5] and self.obj_id:
            courses = Course.objects.filter(id=self.obj_id)
            if courses:
                return courses[0]
        if self.type in [4, 6] and self.obj_id:
            discusses = Discuss.objects.using('fps').filter(id=self.obj_id)
            if discusses:
                if self.type == 4:
                    entity = Article.objects.using('fps').filter(id=discusses[0].relate_id)
                    return entity[0]
                elif self.type == 6:
                    ask = CourseAsk.objects.using('fps').filter(id=discusses[0].relate_id)
                    if ask:
                        lessons = Lesson.objects.filter(id=ask[0].relate_id)
                        if lessons:
                            return lessons[0].course
        if self.type in [7] and self.obj_id:
            articles = Article.objects.using('fps').filter(id=self.obj_id)
            if articles:
                return articles[0]
        return None

    def __unicode__(self):
        return str(self.id)


# 用户APP推送消息未读记录
class AppSendMessageNum(models.Model):
    user = models.IntegerField("用户", blank=False, null=False)
    message_count = models.IntegerField("消息数", blank=False, null=False, default=0)
    dynamic_count = models.IntegerField("动态数", blank=False, null=False, default=0)

    class Meta:
        verbose_name = "APP推送消息未读记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 转介绍邀请记录
class InvitationRecord(models.Model):
    channel = {
        0: '微信',
        1: 'qq',
        2: '微博'
    }
    # userA = models.IntegerField(db_index=True, verbose_name=u'邀请人')
    # userB = models.IntegerField(unique=True, verbose_name=u'被邀请人')
    userA = models.IntegerField(verbose_name=u'邀请人')
    userB = models.IntegerField(unique=True, verbose_name=u'被邀请人')
    if_attend_course = models.BooleanField(default=False, verbose_name=u'是否报名课程')
    attend_course = models.ForeignKey(CareerCourse, blank=True, null=True, verbose_name=u'报名课程')
    register_time = models.DateTimeField(auto_now_add=True, verbose_name=u'注册时间')
    first_attend_time = models.DateTimeField(blank=True, null=True, verbose_name=u'第一次报名课程时间')
    channel = models.IntegerField(choices=channel.items(), blank=True, null=True, verbose_name=u'分享渠道')
    if_payed = models.BooleanField(default=False, verbose_name=u'是否支付红包')

    class Meta:
        verbose_name = u'邀请记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    def userA_info(self):
        return UserProfile.objects.values_list('mobile').get(id=self.userA)[0]

    userA_info.short_description = '邀请人手机号'


# 用户专业技能
class UserProfessionalSkill(models.Model):
    LEVEL_CHOICES = {
        0: u'不知道',
        1: u'了解',
        2: u'熟练',
        3: u'精通'
    }

    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    skill = models.ForeignKey(ProfessionalSkill, verbose_name=u"专业技能")
    level = models.IntegerField(choices=LEVEL_CHOICES.items(), verbose_name=u"掌握程度", default=0)

    class Meta:
        verbose_name = "用户专业技能"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 用户学习目标
class UserStudyGoal(models.Model):
    '''
    已经弃用和就业信息合并
    20161128 update: 启用，用于入学流程改版
    ALTER TABLE `mz_user_userstudygoal`
    CHANGE COLUMN `career_course_id` `domain_name` VARCHAR(20) NOT NULL ;
    ALTER TABLE `mz_user_userstudygoal`
    CHANGE COLUMN `goal` `goal_id` INT(11) NOT NULL ;

    '''
    GOAL_CHOICES = {
        0: u'技能提升',
        1: u'就业'
    }
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    # career_course_id = models.IntegerField(verbose_name=u'职业课程ID')
    domain_name = models.CharField(u'课程分类', max_length=20)
    goal = models.ForeignKey(StudyGoal, verbose_name=u"目标")

    class Meta:
        verbose_name = "用户学习目标"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class UserJobInfo(models.Model):
    """就业信息（用户在每个职业课程就业信息都不同）"""
    # GOAL_CHOICES = {
    #     0: u'技能提升',
    #     1: u'就业'
    # }

    DEGREE_GZ = 1
    DEGREE_DZ = 2
    DEGREE_BK = 3
    DEGREE_SS = 4
    DEGREE_BS = 5
    DEGREES = {DEGREE_GZ: u'高中及以下',
               DEGREE_DZ: u'大专',
               DEGREE_BK: u'大学本科',
               DEGREE_SS: u'硕士',
               DEGREE_BS: u'博士'}

    SERVICE_YEAR_0 = 1
    SERVICE_YEAR_0_1 = 2
    SERVICE_YEAR_1_3 = 3
    SERVICE_YEAR_3_5 = 4
    SERVICE_YEAR_5_10 = 5
    SERVICE_YEAR_10 = 6
    SERVICE_YEAR_CHOICES = {SERVICE_YEAR_0: u'应届毕业生',
                            SERVICE_YEAR_0_1: u'1年以下',
                            SERVICE_YEAR_1_3: u'1-3年',
                            SERVICE_YEAR_3_5: u'3-5年',
                            SERVICE_YEAR_5_10: u'5-10年',
                            SERVICE_YEAR_10: u'10年以上'}

    IS_SERVICE_TRUE = 1
    IS_SERVICE_FALSE = 2
    IS_SERVICE_CHOICES = {IS_SERVICE_TRUE: u'在职', IS_SERVICE_FALSE: u'不在职'}

    user = models.ForeignKey(UserProfile, verbose_name=u"用户", db_index=True)
    career_course_id = models.IntegerField(verbose_name=u'职业课程ID', db_index=True)
    # goal = models.IntegerField(choices=GOAL_CHOICES.items(), verbose_name=u"学习目标", default=0)
    intention_job_city = models.CharField(u'意向就业城市', max_length=10, blank=True, null=True)
    to_industry = models.CharField(u'想从事的行业', max_length=20, blank=True, null=True)
    degree = models.IntegerField(u'学历', choices=DEGREES.items(), null=True)
    service_year = models.IntegerField(u'工作年限', choices=SERVICE_YEAR_CHOICES.items(), null=True)
    in_service = models.IntegerField(u'是否在职', choices=IS_SERVICE_CHOICES.items(), null=True)
    graduate_institution = models.CharField(u'毕业院校', max_length=50, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"职位")
    industry = models.CharField(u'所在行业', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "就业信息"
        verbose_name_plural = verbose_name
        # 此行代码用runserver跑会报错,经和郭老师确认,删除此行代码对业务无影响,遂注销
        # unique_together = ('user_id', 'career_course_id')

    def __unicode__(self):
        return str(self.id)
