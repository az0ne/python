# -*- coding: utf-8 -*-
import xadmin
from xadmin.views.edit import UpdateAdminView
from models import *
from forms import StageForm, DiscountedForm, CareerCourseForm
#from custom_inline import *  # add by chenyu


class StageInline(object):
    model = Stage
    extra = 1
    style = 'accordion'

class CourseInline(object):
    model = Course.stages_m.through
    extra = 1
    style = 'accordion'

class LessonResourceInline(object):
    model = LessonResource
    extra = 1
    style = 'accordion'

class LessonInline(object):
    model = Lesson
    extra = 1
    style = 'accordion'
    inlines = [LessonResourceInline]

class CareerCourseAdmin(object):
    list_display = ('name', 'description','click_count','try_price','net_price','discounted','contract_price','institute_id','id')
    list_editable = ('institute_id')
    list_filter = ('institute_id',)
    search_fields = ['name','id']

    inlines = [StageInline]

    def save_models(self):
        obj = self.new_obj
        obj.save()
        self._update_discounted(obj)

    # #重写List界面上修改折扣
    # def post(self, request, object_id):
    #     result = super(CareerCourseAdmin, self).post(request, object_id)
    #     if isinstance(self, EditPatchView):
    #         self._update_discounted(CareerCourse.objects.get(id=object_id))
    #     return result
    def _update_discounted(self,obj):
        if obj.net_price:
            obj.contract_price = obj.net_price - obj.discounted_price
            obj.save()

    def get_model_form(self, **kwargs):
        self.form = CareerCourseForm
        return super(CareerCourseAdmin, self).get_model_form(**kwargs)


class StageAdmin(object):

    list_display = ('name', 'description','id', 'lps_version')
    search_fields = ['name','id']
    # custom_inlines = [CourseInline]

    # zhangyu xadmin lps3版本控制
    def queryset(self):
        return self.model._default_manager.xall()

    def get_model_form(self, **kwargs):
        self.form = StageForm
        return super(StageAdmin, self).get_model_form(**kwargs)

    def save_models(self):
        obj = self.new_obj
        if obj.lps_version == '':
            obj.lps_version = None
        obj.save()


class CourseAdmin(object):
    list_display = ('name','date_publish','need_days','teacher','click_count','score_ava','id')
    search_fields = ['name','id']
    style_fields = {'search_keywords': 'm2m_transfer'}
    inlines = [LessonInline]

class CourseResourceAdmin(object):
    list_display=('name','download_url','download_count','id')
    search_fields = ['name','id']

class LessonAdmin(object):
    inlines = [LessonResourceInline]
    list_display = ('name','video_length','play_count','id')
    search_fields = ['name','id']

class LessonResourceAdmin(object):
    list_display = ('name','download_url','download_count','id')

class DiscussAdmin(object):
    list_display = ('content','id')
    search_fields = ['content']

# zhangyu Course_Stages_m register xadmin
class Course_Stages_mAdmin(object):
    list_display = ('course', 'stage', 'is_required')
    search_fields = ['course__name', 'stage__name']

class CareerCatagoryAdmin(object):
    list_display = ('name',)
    search_fields = ['name']

class CourseCatagoryAdmin(object):
    list_display = ('name','career_catagory__name','is_hot_tag')
    list_editable = ['is_hot_tag']
    search_fields = ['career_catagory__name']

class InstituteAdmin(object):
    list_display = ('name', 'keywords', 'online_count', 'link_course')
    list_editable = ['keywords', 'online_count', 'link_course']
    search_fields = ['name']

# add_by_zhangyunrui 网站改版20160118
class StudentProjectImageAdmin(object):
    list_display = ('image_url', 'career_course',)
    list_editable = ['image_url', 'career_course',]

class ShowStageAdmin(object):
    list_display = ('name', 'description', 'task_knowledge_test', 'task_list', 'image_url',)
    list_editable = ['name', 'description', 'task_knowledge_test', 'task_list', 'image_url',]
    search_fields = ['name']

class DiscountedAdmin(object):
    list_display = ('type', 'content', 'name', 'id')
    search_fields = ['type']
    # readonly_fields = ('type', 'content', 'name')

    def get_model_form(self, **kwargs):
        self.form = DiscountedForm
        return super(DiscountedAdmin, self).get_model_form(**kwargs)

    #只有修改Model对象时,才不能编辑
    def get_readonly_fields(self):
        if isinstance(self, UpdateAdminView):
            self.readonly_fields = ('type', 'content')
        return super(DiscountedAdmin, self).get_readonly_fields()


class CourseDirectionAdmin(object):
    list_display = ('name',)
    search_fields = ['name']
    style_fields = {'career_course': 'm2m_transfer'}


xadmin.site.register(CareerCatagory, CareerCatagoryAdmin)
xadmin.site.register(CourseCatagory, CourseCatagoryAdmin)
xadmin.site.register(CareerCourse, CareerCourseAdmin)
xadmin.site.register(Discounted, DiscountedAdmin)
xadmin.site.register(Stage, StageAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(LessonResource, LessonResourceAdmin)
xadmin.site.register(Discuss, DiscussAdmin)
xadmin.site.register(Course_Stages_m, Course_Stages_mAdmin)
xadmin.site.register(Institute, InstituteAdmin)
xadmin.site.register(StudentProjectImage, StudentProjectImageAdmin)
xadmin.site.register(ShowStage, ShowStageAdmin)
xadmin.site.register(CourseDirection, CourseDirectionAdmin)
