#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper


class User(SqlResultWrapper):
    """
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDERS = {GENDER_MALE:u'男', GENDER_FEMALE:u'女'}
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

    uuid                    = UUIDField(auto=True)
    username                = models.CharField("用户名", max_length=30, unique=True)
    first_name              = models.CharField("名字", max_length=30, blank=True)
    last_name               = models.CharField("姓氏", max_length=30, blank=True)
    email                   = models.EmailField("邮件地址", unique=True, null=True, blank=True)
    is_staff                = models.BooleanField("职员状态", default=False, help_text="是否能够登录管理后台")
    is_active               = models.BooleanField("是否激活", default=True, help_text="用户是否被激活，未激活则不能使用")
    is_disabled             = models.BooleanField("是否禁用", default=False, help_text="用户是否被禁用，被禁用则不能使用")
    date_joined             = models.DateTimeField("创建日期", default=datetime.now())
    nick_name               = models.CharField(max_length=50, verbose_name=u"昵称", unique=True, null=True, blank=True)
    avatar_url              = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_big.png", max_length=200, blank=True, null=True, verbose_name=u"头像220x220")
    avatar_middle_thumbnall = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_middle.png", max_length=200, blank=True, null=True, verbose_name=u"头像104x104")
    avatar_small_thumbnall  = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_small.png", max_length=200, blank=True, null=True, verbose_name=u"头像70x70")
    avatar_alt              = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"头像ALT说明")
    qq                      = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"QQ号码")
    mobile                  = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name=u"手机号码")
    valid_email             = models.SmallIntegerField(default=0, choices=((0, u"否"),(1, u"是"),), verbose_name=u"是否验证邮箱")
    valid_mobile            = models.SmallIntegerField(default=0, choices=((0, u"否"),(1, u"是"),), verbose_name=u"是否验证手机")
    company_name            = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"公司名")
    position                = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"职位名")
    teach_feature           = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"教学特点")
    description             = models.TextField(blank=True, null=True, verbose_name=u"个人介绍")
    uid                     = models.IntegerField(blank=True, null=True, unique=True, verbose_name=u"对应ucenter用户ID")
    register_way            = models.ForeignKey(RegisterWay, null=True, blank=True, verbose_name=u"注册途径")
    city                    = models.ForeignKey(CityDict, null=True, blank=True, verbose_name=u"城市")
    index                   = models.IntegerField("排列顺序(从小到大)",default=999)
    badge                   = models.ManyToManyField(BadgeDict, null=True, blank=True, verbose_name=u"徽章")
    certificate             = models.ManyToManyField(Certificate, null=True, blank=True, verbose_name=u"证书")
    mylesson                = models.ManyToManyField(Lesson, null=True, blank=True, verbose_name=u"我的学习章节", through=u"UserLearningLesson")
    mystage                 = models.ManyToManyField(Stage, null=True, blank=True, verbose_name=u"我的解锁阶段", through=u"UserUnlockStage")
    myfavorite              = models.ManyToManyField(Course, null=True, blank=True, verbose_name=u"我的收藏", through=u"MyFavorite")
    token                   = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"设备Token")
    study_goal_opt          = models.ForeignKey(StudyGoal, blank=True, null=True, verbose_name=u"学习目标选项")
    study_goal              = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"学习目标")
    study_base_opt          = models.ForeignKey(StudyBase, null=True, blank=True, verbose_name=u"学习基础选项")
    study_base              = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"学习基础")

    # 高校专区
    academics               = models.ManyToManyField(AcademicOrg, null=True, blank=True, verbose_name=u"高校专区")

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

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    """
    pass
