#!/usr/bin/env python
# -*- coding: utf8 -*-


from mz_platform.objects.sql_result_wrapper import SqlResultWrapper
from mz_platform.apis.user_sys_api import UserSysApi


class Course(SqlResultWrapper):
    """
    @brief  class Course

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
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="老师")
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
    """

    def __init__(self, orm_obj=None):
        super(Course, self).__init__(orm_obj)

    def is_all_field_safe(self, fields):
        """
        @brief test all **fields** in **course_obj** is True

        @param course_obj : ``Course`` object
        @param fields : [String], if None return True
        @retval CareerCourse: return val
        """
        if not fields:
            return True

        return all(self.values(*fields))

    @property
    def teacher(self):
        """
        @brief 得到课程相关的teacher对象, 如果失败返回None

        根据teacher id
        """
        if not self._teacher:
            api = UserSysApi.default_instance()
            r = api.get_one_teacher(pk=self.teacher_id)
            if not r:
                return None
            self._teacher = r.obj
        return self._teacher

    @property
    def teacher_id(self):
        return self['teacher_id']
