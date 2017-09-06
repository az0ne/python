# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
import xadmin
from models import *
from forms import QuizForm

# Register your models here.
class ClassStudentsInline(object):
    model = ClassStudents
    extra = 1
    style = 'accordion'

class ClassTeachersInline(object):
    model = ClassTeachers
    extra = 1
    style = 'accordion'

class ClassAdmin(object):

    list_display = ('coding', 'name','date_open','teachers','id', 'lps_version')
    search_fields = ['coding','name','teachers']
    inlines = [ClassStudentsInline,ClassTeachersInline]

    # zhangyu xadmin lps3版本控制
    def queryset(self):
        return self.model._default_manager.xall()

    def save_models(self):
        obj = self.new_obj
        if (not obj.lps_version=='3.0') and obj.class_type==Class.CLASS_TYPE_EXPERIENCE:
            raise Exception(u"只有lps_version=3.0的版本才支持体验班")

        if obj.id is None and obj.class_type == Class.CLASS_TYPE_EXPERIENCE:#新增
            if Class.objects.xall().filter(
                    class_type=Class.CLASS_TYPE_EXPERIENCE,
                    career_course_id=obj.career_course_id).exists():
                raise Exception(u"本职业课程已存在体验班,不要再新建了")
        if obj.id:
            if Class.objects.xall().get(id=obj.id).class_type != obj.class_type:
                raise Exception(u"班级类型不允许修改")


        if obj.lps_version == '':
            obj.lps_version = None
        obj.save()

class PlanningAdmin(object):
    list_display = ('user', 'career_course','date_publish','id')
    search_fields = ['relation_id','description']

class PlanningItemAdmin(object):
    list_display = ('planning', 'course','need_days','id')
    search_fields = ['course','planning']

class PlanningPauseAdmin(object):
    list_display = ('planning', 'pause_date','restore_date','reason','id')

class ExamineAdmin(object):
    list_display = ('examine_type', 'relation_type','relation_id','id')
    search_fields = ['relation_id','description']

class HomeworkAdmin(object):
    list_display = ('id', 'relation_type','relation_id','description')
    search_fields = ['relation_id', 'description']

class ProjectAdmin(object):
    list_display = ('id', 'relation_type','relation_id','description')
    search_fields = ['relation_id','description']

class PaperAdmin(object):
    list_display = ('id', 'relation_type','relation_id','description')
    search_fields = ['relation_id','description']

class QuizAdmin(object):
    list_display = ('question', 'paper','index','id')
    search_fields = ['question','item_list']

    def get_model_form(self, **kwargs):
        self.form = QuizForm
        return super(QuizAdmin, self).get_model_form(**kwargs)


class CodeExerciseAdmin(object):
    list_display = ('id', 'relation_type','relation_id','description')
    search_fields = ['relation_id','description']

class MissionAdmin(object):
    list_display = ('id', 'relation_type','relation_id','description')
    search_fields = ['relation_id','description']

class ExamineRecordAdmin(object):
    list_display = ('id', 'examine', 'score', 'study_point', 'rebuild_count', 'date_publish')

class HomeworkRecordAdmin(object):
    list_display = ('id', 'homework', 'score', 'study_point', 'rebuild_count', 'date_publish')


class ProjectRecordAdmin(object):
    list_display = ('id', 'project', 'score', 'study_point', 'rebuild_count', 'date_publish')


class ProjectMaterialAdmin(object):
    list_display = ('id', 'project', 'material')


class ProjectImageAdmin(object):
    list_display = ('id', 'project', 'image')

class PaperRecordAdmin(object):
    list_display = ('id', 'paper', 'score', 'study_point', 'rebuild_count', 'date_publish')


class QuizRecordAdmin(object):
    list_display = ('id', 'paper_record', 'result')

class CodeExerciseRecordAdmin(object):
    list_display = ('id', 'code_exercise', 'score', 'study_point', 'rebuild_count', 'date_publish')


class MissionRecordAdmin(object):
    list_display = ('id', 'mission', 'score', 'study_point', 'rebuild_count', 'date_publish')


class CourseScoreAdmin(object):
    list_display = ('id', 'user', 'course', 'is_complete', 'rebuild_count', 'date_publish')
    search_fields = ['user', 'course', 'rebuild_count']

class LiveRoomAdmin(object):
    list_display = ('id', 'live_class', 'date_publish', 'live_is_open')

xadmin.site.register(Class, ClassAdmin)
xadmin.site.register(Planning, PlanningAdmin)
xadmin.site.register(PlanningItem, PlanningItemAdmin)
xadmin.site.register(PlanningPause, PlanningPauseAdmin)
xadmin.site.register(Examine, ExamineAdmin)
xadmin.site.register(Homework, HomeworkAdmin)
xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(Paper, PaperAdmin)
xadmin.site.register(Quiz, QuizAdmin)
xadmin.site.register(CodeExercise, CodeExerciseAdmin)
xadmin.site.register(Mission, MissionAdmin)
xadmin.site.register(ExamineRecord, ExamineRecordAdmin)
xadmin.site.register(HomeworkRecord, HomeworkRecordAdmin)
xadmin.site.register(ProjectRecord, ProjectRecordAdmin)
xadmin.site.register(PaperRecord, PaperRecordAdmin)
xadmin.site.register(QuizRecord, QuizRecordAdmin)
xadmin.site.register(CodeExerciseRecord, CodeExerciseRecordAdmin)
xadmin.site.register(MissionRecord, MissionRecordAdmin)
xadmin.site.register(CourseScore, CourseScoreAdmin)
xadmin.site.register(LiveRoom, LiveRoomAdmin)
xadmin.site.register(ProjectMaterial, ProjectMaterialAdmin)
xadmin.site.register(ProjectImage, ProjectImageAdmin)


