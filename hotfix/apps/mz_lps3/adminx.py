# -*- coding: utf-8 -*-
import xadmin
from mz_lps3 import models
from mz_course.models import Stage


class StageTaskRelationAdmin(object):

    list_display = ('id', 'name', 'index', 'stage', 'task')

    # zhangyu xadmin lps3版本控制
    def get_model_form(self, **kwargs):
        form = super(StageTaskRelationAdmin, self).get_model_form(**kwargs)
        form.base_fields['stage']._queryset = Stage.objects.xall().filter(lps_version='3.0')
        return form

class TaskAdmin(object):
    list_display = ('id', 'name', 'created')

class UserTaskRecordAdmin(object):
    list_display = ('id', 'student_id', 'stage_task', 'class_id', 'status', 'score', 'created')

class KnowledgeAdmin(object):
    list_display = ('id', 'name', 'created')

class TaskKnowledgeRelationAdmin(object):
    list_display = ('id', 'name', 'index', 'task', 'knowledge')

class UserKnowledgeRecordAdmin(object):
    list_display = ('id', 'task_knowledge', 'student_id', 'class_id', 'created')

class KnowledgeItemAdmin(object):
    list_display = ('id', 'parent', 'obj_type', 'obj_id', 'index', 'created')

class UserKnowledgeItemRecordAdmin(object):
    list_display = ('id', 'student_id', 'knowledge_item', 'class_id', 'status', 'score', 'created')

class GiftAdmin(object):
    list_display = ('id', 'name', 'created')



class StudyHistoryAdmin(object):
    list_display = ('id', 'student_id', 'class_id', 'content', 'created')


class ClassMeetingRelationInline(object):
    model = models.ClassMeetingRelation
    extra = 1
    style = 'accordion'

# class LiveRoomInline(object):
#     model = models.LiveRoom
#     extra = 1
#     style = 'accordion'

class ClassMeetingAdmin(object):
    list_display = ('id', 'content', 'startline', 'status', 'is_temp')
    search_fields = ['content','id']
    inlines = [ClassMeetingRelationInline]


class LiveRoomAdmin(object):
    list_display = ('id','live_id', 'live_code', 'student_client_token', 'student_join_url','teacher_token','teacher_join_url')
    search_fields = ['live_id','live_code']

class ClassMeetingAttendanceAdmin(object):
    list_display = ('id','class_meeting_id', 'student_id', 'status','liveroom_in_time')
    search_fields = ['live_id','live_code']

class ClassMeetingVideoAdmin(object):
    list_display = ('id','class_id', 'live_id', 'play_subject','create_time','token','url')
    search_fields = ['class_id','live_id']

# Register your models here.
xadmin.site.register(models.StageTaskRelation, StageTaskRelationAdmin)
xadmin.site.register(models.Task, TaskAdmin)
xadmin.site.register(models.UserTaskRecord, UserTaskRecordAdmin)

xadmin.site.register(models.Knowledge, KnowledgeAdmin)
xadmin.site.register(models.TaskKnowledgeRelation, TaskKnowledgeRelationAdmin)

xadmin.site.register(models.KnowledgeItem, KnowledgeItemAdmin)
xadmin.site.register(models.UserKnowledgeItemRecord, UserKnowledgeItemRecordAdmin)

xadmin.site.register(models.Gift, GiftAdmin)
xadmin.site.register(models.StudyHistory, StudyHistoryAdmin)

xadmin.site.register(models.ClassMeeting, ClassMeetingAdmin)
xadmin.site.register(models.LiveRoom, LiveRoomAdmin)
xadmin.site.register(models.ClassMeetingAttendance, ClassMeetingAttendanceAdmin)
xadmin.site.register(models.ClassMeetingVideo, ClassMeetingVideoAdmin)
