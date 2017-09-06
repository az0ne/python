# -*- coding: utf-8 -*-

from django.db import models



class CareerCatagory(models.Model):
    '''专业方向'''
    name = models.CharField(u'专业方向', max_length=50)
    class Meta:
        verbose_name = u'专业方向'
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

# 职业课程 models
class CareerCourse(models.Model):
    name = models.CharField("职业课程名称", max_length=50)
    # short_name = models.CharField("职业课程英文名称简写", max_length=10, unique=True)
    # image = models.ImageField("课程图标(160*160)", upload_to="course/%Y/%m")
    # app_image = models.ImageField("课程小图标(24*24)", upload_to="course/%Y/%m", null=True, blank=True)
    # app_career_image = models.ImageField("app图标", upload_to="course/%Y/%m", null=True, blank=True)
    # description = models.TextField("文字介绍")
    # student_count = models.IntegerField("学习人数", default=0)
    # market_page_url = models.URLField("营销页面地址", blank=True, null=True)
    # course_color = models.CharField("课程配色", max_length=50)
    # discount = models.DecimalField("折扣", default=1, max_digits=3, decimal_places=2)
    # click_count = models.IntegerField("点击次数",default=0)
    # index = models.IntegerField("职业课程顺序(从小到大)",default=999)
    # search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="搜索关键词")
    # seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    # seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    # seo_description = models.TextField("SEO描述", null=True, blank=True)
    # #add by Steven YU
    # course_scope = models.SmallIntegerField("课程类型",null=True, blank=True, choices=((0,"高校专区"),(1,"企业专区"),))
    # product_id              = models.CharField(max_length=50,null=True, blank=True,verbose_name=u"产品ID")
    # balance_product_id    = models.CharField(max_length=50,null=True, blank=True, verbose_name=u"产品尾款ID")
    #
    # status = models.IntegerField(default=0,choices= ((0,"一般课程"),(1,"即将开班"),(2,"热门课程")),verbose_name="课程状态")
    # guide_line_page = models.CharField(max_length=50,null=True, blank=True, verbose_name=u"课程大纲页")
    # qq = models.CharField("QQ群号", max_length=20, null=True, blank=True)
    # qq_key = models.CharField("QQ群key", max_length=100, null=True, blank=True)
    # is_hot = models.BooleanField(default=False, verbose_name=u"是否热门开班课程")
    # institute_id = models.IntegerField("学院ID", default=0) #guotao网站改版
    # # add_by_zhangyunrui 网站改版20160118
    # brief_intro = models.CharField(u"一句话介绍", max_length=150, null=True, blank=True)
    # # add_by_zhangyunrui 网站改版20160216新增需求
    # id_53kf = models.IntegerField(u"53客服id号", default=1, null=True, blank=True)
    # course_color_px = models.CharField(u"介绍页课程配色", default="#3DBD9C", max_length=50, null=True, blank=True)
    # image_px = models.ImageField(u"介绍页背景图片", default="course_image_px/aboutLessonbg.png", upload_to="course_image_px/%Y/%m", null=True, blank=True)
    # image_px_2 = models.ImageField(u"介绍页第二屏背景图片", default="course_image_px_2/LessonImg001.png", upload_to="course_image_px_2/%Y/%m", null=True, blank=True)
    # # add_by_zhangyunrui 网站改版20160216课程介绍页单独的介绍与tdk
    # description_px = models.TextField(u"介绍页文字介绍", null=True, blank=True)
    # seo_title_px = models.CharField(u"介绍页SEO标题", max_length=200, null=True, blank=True)
    # seo_keyword_px = models.CharField(u"介绍页SEO关键词", max_length=200, null=True, blank=True)
    # seo_description_px = models.TextField(u"介绍页SEO描述", null=True, blank=True)
    #
    # lps3_guide_task_id = models.IntegerField(u"lps3新手引导任务id", null=True, blank=True, db_index=True)
    # # 订单管理
    # try_price = models.PositiveIntegerField(u"试学价格", default=None, null=True)
    # net_price = models.PositiveIntegerField(u"官网价格", default=None, null=True)
    # discounted = models.ForeignKey(Discounted, verbose_name=u"优惠活动", null=True, blank=True)
    # contract_price = models.PositiveIntegerField(u"合同价格", default=None, null=True, blank=True)

    # class Meta:
    #     verbose_name = "职业课程"
    #     verbose_name_plural = verbose_name
    #     ordering = ['-id']

    def __unicode__(self):
        return self.name

    # 优惠金额
    # @cached_property
    # def discounted_price(self):
    #     if self.discounted:
    #         return self.discounted.calc_discounted_price(self.net_price)
    #     else:
    #         return 0

class CourseCatagory(models.Model):
    career_catagory = models.ForeignKey(CareerCatagory,verbose_name=u"课程方向")
    name = models.CharField(u"课程分类", max_length=50)
    is_hot_tag = models.BooleanField(default=False,verbose_name=u"是否热门标签")
    class Meta:
        verbose_name = u"课程分类"
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


# 课程 models
class Course(models.Model):
    name = models.CharField("课程名称",max_length=50)
    image = models.ImageField("课程封面", upload_to="course/%Y/%m")
    description = models.TextField("课程描述")
    is_active = models.BooleanField("有效性", default=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)
    need_days = models.IntegerField("无基础学生完成天数", default=7)
    need_days_base = models.IntegerField("有基础学生完成天数", default=5)
    student_count = models.IntegerField("学习人数", default=0)
    favorite_count = models.IntegerField("收藏次数", default=0)
    click_count = models.IntegerField("点击次数",default=0)
    # has_project = models.BooleanField("是否有项目考核", default=False)
    # has_examine = models.BooleanField("是否有课程总测验", default=True)
    is_novice = models.BooleanField("是否是新手课程", default=False)
    is_click = models.BooleanField("是否点击能进入课程", default=False)
    index = models.IntegerField("课程顺序(从小到大)",default=999)
    # teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="老师")
    # stages_m = models.ManyToManyField(Stage, related_name="stages_m", blank=True, null=True, verbose_name="多阶段", through="Course_Stages_m")

    # stages = models.ForeignKey(Stage, blank=True, null=True, verbose_name="阶段")

    # search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="小课程搜索关键词")
    #Add by Steven YU
    is_homeshow = models.BooleanField(u"是否在首页显示", default=False)
    # is_required = models.BooleanField(u"是否必修", default=True) # add fo lps2
    course_status = models.SmallIntegerField(u"课程状态", choices=((0,"更新中"),(1,"已完结"),), default = 0)
    #add by guotao
    # score_user=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="score_user", blank=True, null=True, verbose_name="课程用户评分", through="Course_User_Score")
    score_ava=models.FloatField("课程平均评分", default=0.0)
    need_pay = models.BooleanField(u"是否需要付费才能观看",default=False)

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
