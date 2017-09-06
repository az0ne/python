# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from xadmin.views.base import filter_hook
from models import *
from mz_user.models import *
from django.contrib.auth.models import *
from django import forms
from mz_pay.models import UserPurchase
from mz_course.models import *
from mz_lps.models import *
from aca_course.models import *
from mz_eduadmin.stats.models import *
from PIL import Image
from utils.ImageProcess import MyGaussianBlur

class BaseSetting(object):
    enable_themes = False
    use_bootswatch = True

class GlobalSetting(object):
    site_title = '麦子学院管理后台'
    site_footer = 'Maiziedu.Com'
    global_search_models = [UserProfile,]
    menu_style = 'accordion'

    def get_site_menu(self):
        return (
            {'title': '用户模块', 'menus':(
                {'title':'用户','url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '组',  'url': self.get_model_url(Group, 'changelist')},
                {'title':'权限','url': self.get_model_url(Permission, 'changelist')},
            )},
            {'title': '支付模块', 'menus':(
                {'title':'订单','url': self.get_model_url(UserPurchase, 'changelist')},
                {'title':'职业课程优惠','url': self.get_model_url(Discounted, 'changelist')},
            )},
            {'title': '课程模块', 'menus':(
                {'title': '学院分类','url': self.get_model_url(Institute, 'changelist')},
                {'title': '职业课程','url': self.get_model_url(CareerCourse, 'changelist')},
                {'title': '课程阶段','url': self.get_model_url(Stage, 'changelist')},
                {'title': '课程','url': self.get_model_url(Course, 'changelist')},
                {'title': '课程源码及其他文件附件','url': self.get_model_url(CourseResource, 'changelist')},
                {'title': '章节','url': self.get_model_url(Lesson, 'changelist')},
                {'title': '章节源码及其他文件附件','url': self.get_model_url(LessonResource, 'changelist')},
                {'title': '课程讨论','url': self.get_model_url(Discuss, 'changelist')},
                {'title': 'APP课程方向','url': self.get_model_url(CourseDirection, 'changelist')},
            )},
            {'title': '学习管理', 'menus':(
                {'title': '班级','url': self.get_model_url(Class, 'changelist')},
                {'title': '学习计划','url': self.get_model_url(Planning, 'changelist')},
                {'title': '学习计划项','url': self.get_model_url(PlanningItem, 'changelist')},
                {'title': '计划暂停记录','url': self.get_model_url(PlanningPause, 'changelist')},
                {'title': '课后作业','url': self.get_model_url(Homework, 'changelist')},
                {'title': '项目制作','url': self.get_model_url(Project, 'changelist')},
                {'title': '项目素材','url': self.get_model_url(ProjectMaterial, 'changelist')},
                {'title': '项目截图','url': self.get_model_url(ProjectImage, 'changelist')},
                {'title': '试卷','url': self.get_model_url(Paper, 'changelist')},
                {'title': '试卷题目','url': self.get_model_url(Quiz, 'changelist')},
                {'title': '代码练习','url': self.get_model_url(CodeExercise, 'changelist')},
                {'title': '考核管理','url': self.get_model_url(Examine, 'changelist')},
                {'title': '人工考核','url': self.get_model_url(Mission, 'changelist')},
                {'title': '考核记录','url': self.get_model_url(ExamineRecord, 'changelist')},
                {'title': '考核记录_课后作业','url': self.get_model_url(HomeworkRecord, 'changelist')},
                {'title': '考核记录_项目制作','url': self.get_model_url(ProjectRecord, 'changelist')},
                {'title': '考核记录_试卷考核','url': self.get_model_url(PaperRecord, 'changelist')},
                {'title': '考核记录_做题记录','url': self.get_model_url(QuizRecord, 'changelist')},
                {'title': '考核记录_代码练习','url': self.get_model_url(CodeExerciseRecord, 'changelist')},
                {'title': '考核记录_人工考核','url': self.get_model_url(MissionRecord, 'changelist')},
                {'title': '课程学分','url': self.get_model_url(CourseScore, 'changelist')},
            )},
            {'title': '公共模块', 'menus':(
                {'title':'消息','url': self.get_model_url(MyMessage, 'changelist')},
                {'title':'广告位管理','url': self.get_model_url(Ad, 'changelist')},
                {'title':'App广告位管理','url': self.get_model_url(AppAd, 'changelist')},
                {'title':'友情链接','url': self.get_model_url(Links, 'changelist')},
                {'title':'关键词','url': self.get_model_url(Keywords, 'changelist')},
                {'title':'推荐搜索关键词','url': self.get_model_url(RecommendKeywords, 'changelist')},
                {'title':'单页SEO设置','url': self.get_model_url(PageSeoSet, 'changelist')},
                {'title':'APP留言反馈','url': self.get_model_url(Feedback, 'changelist')},
                {'title':'Android版本管理','url': self.get_model_url(AndroidVersion, 'changelist')},
                {'title':'手机活动页咨询统计','url': self.get_model_url(AppConsultInfo, 'changelist')},
                {'title':'招聘位部门管理','url': self.get_model_url(MaiziDeparment, 'changelist')},
                {'title':'招聘位职位详细信息','url': self.get_model_url(RecruitPosition, 'changelist')},
                {'title':'FAQ','url': self.get_model_url(FAQ, 'changelist')},
            )},
            {'title': '字典管理', 'menus':(
                {'title': '国家字典',  'url': self.get_model_url(CountryDict, 'changelist')},
                {'title':'省份字典','url': self.get_model_url(ProvinceDict, 'changelist')},
                {'title':'城市字典','url': self.get_model_url(CityDict, 'changelist')},
                {'title':'徽章字典','url': self.get_model_url(BadgeDict, 'changelist')},
                {'title':'证书字典','url': self.get_model_url(Certificate, 'changelist')},
                {'title':'注册途径','url': self.get_model_url(RegisterWay, 'changelist')},
            )},
            {'title': '高校专区', 'menus':(
                {'title':'省份城市','url': self.get_model_url(ProvinceCity, 'changelist')},
                {'title':'组织机构','url': self.get_model_url(AcademicOrg, 'changelist')},
                {'title':'课程类型','url': self.get_model_url(CourseType, 'changelist')},
                {'title':'专业课程','url': self.get_model_url(AcademicCourse, 'changelist')},
                {'title':'课程阶段','url': self.get_model_url(AcademicStage, 'changelist')},
                {'title':'阶段课程','url': self.get_model_url(Course, 'changelist')},
                {'title':'课程章节','url': self.get_model_url(Lesson, 'changelist')},
                {'title':'专业班级','url': self.get_model_url(AcademicClass, 'changelist')},
                {'title':'院校通知','url': self.get_model_url(Notification, 'changelist')},
                {'title':'高校用户','url': self.get_model_url(AcademicUser, 'changelist')},
            )},
            {'title': '教务系统', 'menus': (
                {'title': '学生完成度记录', 'url': self.get_model_url(StudentCompletion, 'changelist')},
                {'title': '满意度调查问卷版块', 'url': self.get_model_url(QuestionnaireTopic, 'changelist')},
                {'title': '满意度调查问卷题目', 'url': self.get_model_url(QuestionnaireItem, 'changelist')},
                {'title': '学生问卷', 'url': self.get_model_url(StudentQuestionnaire, 'changelist')},
                {'title': '学生问卷题目记录', 'url': self.get_model_url(StudentQuestionnaireItemScore, 'changelist')},
                {'title': '老师问卷记录', 'url': self.get_model_url(TeacherQuestionnaireRecord, 'changelist')},
            )},
            {'title':'系统功能','menus':(
                {'title':'视频长度更新','url':'#'},
                {'title':'学生加入班级','url':'#'},
                {'title':'学生退出班级','url':'#'},
                {'title':'学生转换班级','url':'#'},
                {'title':'订单添加与导出','url':'#'},
                {'title':'优惠码管理','url':'#'},
                {'title':'同步头像','url':'#'},
                {'title':'管理推荐阅读','url':'#'},
                {'title':'直播室列表','url':'#'},
                {'title':'消息列表','url':'#'},
                {'title':'高校用户列表','url':'#'},
                {'title':'清除首页缓存','url':'#'},
                {'title':'清除企业直通班缓存','url':'#'},
                {'title':'lps2支付信息升级','url':'#'},
            )},
        )
    @filter_hook
    def get_media(self):
        media = forms.Media()
        media.add_js(('/static/js/backend_xadmin.js',))
        return media

# Register your models here.
class MyMessageAdmin(object):
    list_display = ('userA','userB','action_content','date_action','id')
    list_filter = ('action_type',)

class AppAdAdmin(object):
    list_display = ('title','description','id')
    search_fields = ('title','description')

class AdAdmin(object):
    list_display = ('title','description','id')
    search_fields = ('title','description')

    def save_models(self):
        obj = self.new_obj
        if obj.type == 0:
            obj.save()
            in_filename = obj.image_url.file.name
            file_name = in_filename.split("/")[-1].split('.')[-2]
            back_file = file_name+"_backimage"
            out_filename = in_filename.replace(file_name,back_file)
            image = Image.open(in_filename)
            image = image.filter(MyGaussianBlur(radius=200))
            image.save(out_filename)

            obj.back_image = obj.image_url.name.replace(file_name,back_file)
            obj.save()
        else:
            obj.save()

class LinksAdmin(object):
    list_display = ('title','description','id')
    search_fields = ('title','description')

class KeywordsAdmin(object):
    list_display = ('name','id')
    search_fields = ['name']

class RecommendKeywordsAdmin(object):
    list_display = ('name','id')
    search_fields = ['name']

class PageSeoSetAdmin(object):
    list_display = ('page_name','seo_title','seo_keyword')
    search_fields = ['page_name']

class FeedbackAdmin(object):
    list_display = ('content','date_publish','id')
    search_fields = ['content']

class AndroidVersionAdmin(object):
    list_display = ('vno','size','is_force','type')
    search_fields = ['vno']

class AppConsultInfoAdmin(object):
    list_display = ('name', 'phone', 'qq', 'interest', 'source', 'date_publish','market_from')
    search_fields = ('name', 'phone', 'qq', 'source','market_from')
    list_filter = ('market_from',)

class MaiziDeparmentAdmin(object):
    list_display = ('name', 'index')
    search_fields = ['name']

class RecruitPositionAdmin(object):
    list_display = ('department', 'title', 'desc', 'index')
    search_fields = ['title']

class FAQAdmin(object):
    list_display = ('title', 'content', 'type', 'index')
    search_fields = ['title']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(MyMessage, MyMessageAdmin)
xadmin.site.register(Ad, AdAdmin)
xadmin.site.register(AppAd, AppAdAdmin)
xadmin.site.register(Links, LinksAdmin)
xadmin.site.register(Keywords, KeywordsAdmin)
xadmin.site.register(RecommendKeywords, RecommendKeywordsAdmin)
xadmin.site.register(PageSeoSet, PageSeoSetAdmin)
xadmin.site.register(Feedback, FeedbackAdmin)
xadmin.site.register(AndroidVersion, AndroidVersionAdmin)
xadmin.site.register(AppConsultInfo, AppConsultInfoAdmin)
xadmin.site.register(MaiziDeparment, MaiziDeparmentAdmin)
xadmin.site.register(RecruitPosition, RecruitPositionAdmin)
xadmin.site.register(FAQ, FAQAdmin)
