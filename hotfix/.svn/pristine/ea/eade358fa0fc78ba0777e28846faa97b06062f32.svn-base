# -*- coding: utf-8 -*-
import xadmin
from models import *
from xadmin.plugins.auth import UserAdmin
from forms import UserCreationForm, UserChangeForm
from xadmin.layout import Fieldset, Main, Side, Row

class CountryDictAdmin(object):
    pass

class ProvinceDictAdmin(object):
    pass

class CityDictAdmin(object):
    pass

class BadgeDictAdmin(object):
    pass

class CertificateAdmin(object):
    pass

class RegisterWayAdmin(object):
    pass

# class MyCourseInline(object):
#     model = MyCourse
#     extra = 1
#     style = 'accordion'

# class UserLearningLessonInline(object):
#     model = UserLearningLesson
#     extra = 1
#     style = 'accordion'

# class MyFavoriteInline(object):
#     model = MyFavorite
#     extra = 1
#     style = 'accordion'

# class UserUnlockStageInline(object):
#     model = UserUnlockStage
#     extra = 1
#     style = 'accordion'

#继承xadmin的UserAdmin以定制User的Admin界面
class UserProfileAdmin(UserAdmin):

    list_display = ('nick_name', 'email', 'mobile', 'first_name', 'last_name', 'is_staff', 'register_way', 'uuid', 'id')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email', 'mobile', 'nick_name','register_way__name')
    ordering = ('date_joined',)
    # inlines = [MyCourseInline, MyFavoriteInline, UserUnlockStageInline, UserLearningLessonInline]

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserAdmin, self).get_model_form(**kwargs)

    def save_models(self):
        if self.new_obj.email == '':
            self.new_obj.email = None
        if self.new_obj.invitation_code == '':
            self.new_obj.invitation_code = None
        if self.new_obj.mobile == '':
            self.new_obj.mobile = None
        self.new_obj.save()

    def valid_forms(self, *args, **kwargs):
        try:
            res = self.form_obj.is_valid()
            if self.form_obj.errors.get('email', ''):
                if self.form_obj.errors['email'][0] == u'具有 邮件地址 的 用户 已存在。':
                    self.form_obj.errors.pop('email')
            if self.form_obj.errors.get('invitation_code', ''):
                if self.form_obj.errors['invitation_code'][0] == u'具有 邀请码 的 用户 已存在。':
                    self.form_obj.errors.pop('invitation_code')
            if self.form_obj.errors.get('mobile', ''):
                if self.form_obj.errors['mobile'][0] == u'具有 手机号码 的 用户 已存在。':
                    self.form_obj.errors.pop('mobile')
            if not self.form_obj.errors:
                res = True
        except Exception:
            pass
        return res

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('登录信息',
                             Row('email', 'mobile'),
                             'password',
                             #css_class='unsort no_title'
                    ),
                    Fieldset('个人信息',
                             Row('avatar_url', 'avatar_middle_thumbnall', 'avatar_small_thumbnall'),
                             Row('first_name', 'last_name'),
                             Row('nick_name', 'qq'),
                             Row('valid_email', 'valid_mobile'),
                    ),
                    Fieldset('VIP信息',
                             'is_vip', 'date_limit'
                    ),
                    Fieldset('权限信息',
                             'groups', 'user_permissions'
                    ),
                    Fieldset('日期信息',
                             'last_login', 'date_joined'
                    ),
                    ),
                Side(
                    Fieldset('Status',
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                    )
            )
        return super(UserAdmin, self).get_form_layout()

class MyCourseAdmin(object):
    list_display = ('user', 'course', 'course_type', 'id')

class StudyGoalAdmin(object):
    list_display = ('name', 'index', 'id')

class StudyBaseAdmin(object):
    list_display = ('name', 'index', 'id')

class AcademicOrgAdmin(object):
    list_display = ('name', 'index', 'id')

class StarStoryAdmin(object):
    list_display = ('id', 'user', 'name', 'index', 'date_add')

class InvitationRecordAdmin(object):
    list_display = ('id', 'userB', 'if_attend_course', 'attend_course', 'register_time',
                    'first_attend_time', 'userA', 'userA_info', 'if_payed')
    list_filter = ('if_attend_course', 'if_payed')
    ordering = ('register_time', 'first_attend_time')
    readonly_fields = ('userA', 'userB', 'register_time', 'if_attend_course', 'attend_course',  'first_attend_time',
                       'channel')
class ProfessionalSkillAdmin(object):
    list_display = ('skill', 'domain')

class UserProfessionalSkillAdmin(object):
    list_display = ('user', 'skill', 'level')

class UserJobInfoAdmin(object):
    list_display = ('user', 'career_course_id', 'intention_job_city', 'graduate_institution', 'position', 'industry')

xadmin.site.register(CountryDict, CountryDictAdmin)
xadmin.site.register(ProvinceDict, ProvinceDictAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(BadgeDict, BadgeDictAdmin)
xadmin.site.register(Certificate, CertificateAdmin)
xadmin.site.register(RegisterWay, RegisterWayAdmin)
#注册UserProfile需先取消UserProfile的注册，因为系统自动已按get_user_model注册了User对象
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(MyCourse, MyCourseAdmin)
xadmin.site.register(StudyGoal, StudyGoalAdmin)
xadmin.site.register(StudyBase, StudyBaseAdmin)
xadmin.site.register(AcademicOrg, AcademicOrgAdmin)
xadmin.site.register(StarStory, StarStoryAdmin)
xadmin.site.register(InvitationRecord, InvitationRecordAdmin)
xadmin.site.register(ProfessionalSkill, ProfessionalSkillAdmin)
xadmin.site.register(UserProfessionalSkill, UserProfessionalSkillAdmin)
xadmin.site.register(UserJobInfo, UserJobInfoAdmin)
