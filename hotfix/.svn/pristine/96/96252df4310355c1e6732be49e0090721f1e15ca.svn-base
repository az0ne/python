import xadmin
from models import *


class UserTaskAdmin(object):
    list_display = ('id', 'user', 'status', 'create_datetime')
    search_fields = ['user', 'id']

class CourseUserTaskAdmin(object):
    list_display = ('id', 'user', 'user_class', 'week', 'plan_study_time', 'real_study_time', \
                    'real_study_time_ext', 'plan_gradute_time')

class UserQualityModelItemsAdmin(object):
    list_display = ('id', 'quality_type', 'score', 'ava_score', 'week')

class ClassMeetingTaskAdmin(object):
    list_display = ('id', 'user_class', 'startline', 'status', 'is_check_before_classmeeting',\
                    'is_check_get_risk_in_week')

class ReadMeUserTaskAdmin(object):
    list_display = ('id', 'user', 'status', 'create_datetime')

class TeacherProfileUserTaskAdmin(object):
    list_display = ('id', 'user', 'status', 'create_datetime')

class StuStatusUserTaskAdmin(object):
    search_fields = ['student_id','id']
    list_display = ('id', 'user', 'stu_status', 'student_id')

class CourseTaskDoneAdmin(object):
    list_display = ('id', 'course_user_task', 'course', 'relate_id', 'relate_type')

class JoinClassUserTaskAdmin(object):
    list_display = ('id', 'user', 'status')

class ViewContractUserTaskAdmin(object):
    list_display = ('id', 'user', 'user_class', 'status')

class FullProfileUserTaskAdmin(object):
    list_display = ('id', 'user', 'status')


class AsyncMethodAdmin(object):
    list_display = ('id', 'calc_type', 'methods', 'is_calc', 'submit_datetime', 'calc_datetime')

class TraceTypeDictAdmin(object):
    list_display = ('id', 'name', 'index',)

class CheckContractUserTaskAdmin(object):
    list_display = ('id', 'user_class__id', 'finish_date', 'status')

class GiveScoreStudentsUserTaskAdmin(object):
    list_display = ('timeliness', 'professional_level','explain_level','harvest','finish_date', 'status',
                    'user__id','week__startline','week__id','id')

class GiveScoreStudentsResultAdmin(object):
    list_display = ('timeliness', 'professional_level','explain_level','harvest','ava_total','week__user_class__id','week__id','id')

class ClassMeetingTaskVideoAdmin(object):
    list_display = ('live_room', 'play_id', 'play_subject','record_id','number','create_time')

class ClassMeetingTaskVideo510Admin(object):
    list_display = ('live_room', 'play_id', 'name','size','record_start_time','record_end_time')

# Register your models here.
xadmin.site.register(ClassMeetingTask, ClassMeetingTaskAdmin)
xadmin.site.register(UserTask, UserTaskAdmin)
xadmin.site.register(CourseUserTask, CourseUserTaskAdmin)
xadmin.site.register(CourseTaskDone, CourseTaskDoneAdmin)
xadmin.site.register(UserQualityModelItems, UserQualityModelItemsAdmin)
xadmin.site.register(ReadMeUserTask, ReadMeUserTaskAdmin)
xadmin.site.register(TeacherProfileUserTask, TeacherProfileUserTaskAdmin)
xadmin.site.register(StuStatusUserTask, StuStatusUserTaskAdmin)
xadmin.site.register(ViewContractUserTask, ViewContractUserTaskAdmin)
xadmin.site.register(FullProfileUserTask, FullProfileUserTaskAdmin)
xadmin.site.register(AsyncMethod, AsyncMethodAdmin)
xadmin.site.register(JoinClassUserTask, JoinClassUserTaskAdmin)
xadmin.site.register(TraceTypeDict, TraceTypeDictAdmin)
xadmin.site.register(CheckContractUserTask, CheckContractUserTaskAdmin)
xadmin.site.register(GiveScoreStudentsUserTask, GiveScoreStudentsUserTaskAdmin)
xadmin.site.register(GiveScoreStudentsResult, GiveScoreStudentsResultAdmin)
xadmin.site.register(ClassMeetingTaskVideo, ClassMeetingTaskVideoAdmin)
xadmin.site.register(ClassMeetingTaskVideo510, ClassMeetingTaskVideo510Admin)
