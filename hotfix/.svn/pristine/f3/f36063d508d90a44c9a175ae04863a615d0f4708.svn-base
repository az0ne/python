# -*- coding: utf-8 -*-
import random

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.conf import settings
from django.core.paginator import Paginator
from django.template import RequestContext
from django.template.loader import get_template
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.http import require_GET, require_http_methods, \
    require_POST

from core.common.upload.ueditor.upload.uploader import Uploader
from mz_common.article_functions import set_tags4article_list
from mz_common.decorators import ajax_login_required
from mz_common.forms import DiscussForm, GetDiscussForm, LikeArticleForm
from mz_common.models import *
from mz_platform.apis.article_sys_api import ArticleSysApi
from mz_platform.apis.common_sys_api import CommonSysApi
from mz_platform.apis.course_sys_api import CourseSysApi
from mz_platform.services.functions.mz_service import Pager
from mz_user.forms import *
from mz_course.models import *
from mz_lps.models import *
from mz_user.functions import is_invitation_code_available
from utils.tool import upload_generation_dir, strip_tags, get_param_by_request
from utils import xinge
import json, logging, os, uuid, urllib2, urllib
from itertools import chain
from mz_lps2.models import *
from fps_interface.utils import *
from django.views.generic.base import View
from mz_common.functions import checkMobile, safe_int
from django.db.models import QuerySet
from mz_common.models import FAQ
from django.db import connections
import requests
# platform refer
from mz_platform.apis import article_sys_api
from mz_platform.apis import common_sys_api
from mz_platform.utils.view_shortcuts import ensure_apiresult_obj
from mz_platform.utils.view_shortcuts import opt_apiresult_obj
from mz_platform.utils.view_tool import datetime_convert
# end platform refer

# 新的架构需要的接口
import db.api
import db.api.common.feedback
from mz_common.functions import paginater
from django.core import urlresolvers
from mz_common.functions import reformat_datetime_from_cache
from django.http import Http404
from utils.logger import logger as log
from mz_platform.utils.view_tool import datetime_convert
import db.api.common.app

logger = logging.getLogger('mz_common.views')

# guotao 查询数据库
def exec_sql(sql, params=None, database="default"):
    cursor = connections[database].cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()


def get_recommended_readings():
    readings = RecommendedReading.objects.all()
    rearranged_readings = {RecommendedReading.ACTIVITY: [], RecommendedReading.NEWS: [], RecommendedReading.DISCUSS: []}
    for reading in readings:
        rearranged_readings[reading.reading_type].append(reading)

    return {'readings': rearranged_readings, 'reading_types': RecommendedReading.READING_TYPES}


def index_front(request):
    # if request.user.is_authenticated() and (request.user.is_student() or request.user.is_teacher()):
    #     is_jump = request.COOKIES.get('is_jump',None)
    #     f_number = request.COOKIES.get('f_number',True)
    #     if is_jump is None and f_number == True:
    #         response = HttpResponseRedirect("/user/center")
    #         response.set_cookie("f_number",1)
    #         return HttpResponseRedirect("/user/center")

    ic = request.GET.get('ic')
    is_invitation = is_invitation_code_available(ic)

    # 游客读取首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get(
            'verify_email') and not is_invitation:
        # if checkMobile(request):
        #     html = cache.get('index_front_html_mobile')
        #     if html:
        #         return HttpResponse(html)
        # else:
        html = cache.get('index_front_html')
        if html:
            return HttpResponse(html)
    # if checkMobile(request):
    #     template_vars = cache.get('index_front_mobile')
    # else:
    template_vars = cache.get('index_front')
    if not template_vars:
        #     ad = Ad.objects.filter(type=0)
        #     text_links = Links.objects.filter(is_pic = 0)
        #     pic_links = Links.objects.filter(is_pic = 1)
        #
        #
        #     # courses = Course.objects.filter(is_active=True, is_click=True).order_by('-date_publish').values_list('name').distinct()
        #     query = Course.objects.filter(is_active=True, is_click=True).query
        #     query.group_by = ['name']
        #     courses = QuerySet(query=query, model=Course).order_by('-date_publish')
        #     num = 4 if checkMobile(request) else 8
        #     courses = courses[:num]
        #     for course in courses:
        #         stage_set = course.stages_m.all()
        #
        #         try:
        #             careercourse = stage_set[0].career_course.short_name.lower()
        #         except:
        #             careercourse = 'others'
        #         lesson_list = Lesson.objects.filter(course=course.id).order_by("index", "id")
        #
        #         setattr(course,"url","/course/%s/%d-%d"%(careercourse,course.id,lesson_list[0].id) if lesson_list else "")
        #     # articles = FPSInfo.get_article()
        #     # activities = FPSInfo.get_activity()
        #     # ask = FPSInfo.get_ask()
        #
        #     hot_tags = CourseCatagory.objects.filter(is_hot_tag=True).order_by('-id')[:10]
        #
        #     group = Group.objects.get(name = '老师')   #所有老师
        #     te_list = Course.objects.distinct().values_list('teacher')
        #     if checkMobile(request):
        #         teachers = group.user_set.filter(id__in = te_list).order_by("index")[:2]
        #     else:
        #         teachers = group.user_set.filter(id__in = te_list).order_by("index")[:5]

        # text_links = Links.objects.filter(is_pic = 0)
        # 首页SEO信息读取
        seo = PageSeoSet()
        try:
            seo = PageSeoSet.objects.get(page_name='1')
        except Exception, e:
            logger.error(e)
        hot_tags = CourseCatagory.objects.filter(is_hot_tag=True).order_by('-id')[:7]

        template_vars = {'seo': seo, 'hot_tags': hot_tags}

        # 获取推荐关键词
        recommendkeywords_list = RecommendKeywords.objects.all()[0:3].values_list('name', flat=True)
        template_vars['recommendkeywords'] = recommendkeywords_list

        # 首页学生老师课程数量
        init_days = (datetime.now() - datetime(2016, 3, 1)).days
        template_vars['student_num'] = 820000 + (init_days * 5)
        template_vars['teacher_num'] = 200 + init_days / 30 * 10
        template_vars['course_num'] = 700 + init_days / 30 * 5

        # if checkMobile(request):
        #     cache.set('index_front_mobile', template_vars, settings.CACHE_TIME)
        # else:
        cache.set('index_front', template_vars, settings.CACHE_TIME)

    # if checkMobile(request):
    #     home_career_courses = cache.get('index_front_careers_mobile')
    # else:
    home_career_courses = cache.get('home_career_courses')
    if not home_career_courses:
        institute_career_courses = []
        institute_lst = Institute.objects.all().order_by("order")
        for institute in institute_lst:
            # 查询出指定学院ID下所有开班的职业课程
            sql = """
            SELECT DISTINCT
              mz_course_careercourse.id,
              mz_course_careercourse.name,
              mz_course_careercourse.short_name,
              mz_course_careercourse.student_count,
              mz_course_careercourse.app_image
            FROM
              mz_course_careercourse
            Left JOIN mz_lps_class ON mz_lps_class.career_course_id = mz_course_careercourse.id
            WHERE
              mz_course_careercourse.course_scope is Null
              AND mz_lps_class.class_type = 0
              AND mz_lps_class.is_closed = False
              AND mz_lps_class.is_active = TRUE
              AND mz_lps_class.status = 1
              AND mz_course_careercourse.institute_id=%s
            ORDER BY mz_course_careercourse.click_count DESC
            """ % institute.id
            career_course_lst = []  # （指定学院的）职业课程
            student_counts = 0  # （指定学院的）学习人数
            for id, name, short_name, student_count, app_image in exec_sql(sql):
                career_course_lst.append(dict(id=id, name=name, short_name=short_name, student_count=student_count,
                                              app_image=app_image))
                student_counts += student_count
            institute_career_courses.append({'name': institute.name, 'career_course_lst': career_course_lst,
                                             'student_counts': format(student_counts, ',')})
        template_vars['institute_career_courses'] = institute_career_courses
        # if checkMobile(request):
        #     cache.set('index_front_careers_mobile', career_courses, settings.CACHE_TIME*6*24)
        # else:
        cache.set('home_career_courses', institute_career_courses, settings.CACHE_TIME * 6 * 24)
    else:
        template_vars['institute_career_courses'] = home_career_courses

    # template_vars['articles'] = FPSInfo.get_article()
    # return render(request, 'base_index2.html', template_vars)
    t = get_template('base_index3.html')

    template_vars['invitation_code'] = ic
    template_vars['is_invitation'] = is_invitation

    if is_invitation:
        template_vars['display_xinchun'] = False
    else:
        template_vars['display_xinchun'] = not (request.user and request.user.is_authenticated() \
                                                and request.user.is_teacher()) and datetime.now() < datetime(2016, 3, 1)
    # 报名倒计时（运营）
    deadline = datetime(2016, 3, 1)
    now_time = datetime.now()
    template_vars['display_countdown'] = not (request.user and request.user.is_authenticated() \
                                              and request.user.is_teacher()) and now_time < deadline and not is_invitation
    c = RequestContext(request, template_vars)
    html = t.render(c)
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get(
            'verify_email') and not is_invitation:
        # if checkMobile(request):
        #     cache.set('index_front_html_mobile', html, 60)
        # else:
        cache.set('index_front_html', html, 60)
    return HttpResponse(html)


# 首页ajax切换课程
def index_course_ajax_page(request):
    types = request.GET['type']
    page = request.GET['page']
    template_vars = cache.get('index_course_ajax_page_' + str(types) + '_' + str(page))
    if not template_vars:
        json_str = '['
        if types == "new":
            courses = Course.objects.filter(Q(is_click=True)).order_by()
        if types == "most":
            lesson_group = Lesson.objects.values('course').annotate(s_amount=Sum('play_count')).order_by('-s_amount')
            courses = []
            for le in lesson_group:
                try:
                    cours = Course.objects.get(id=le['course'], is_click=True)
                    courses.append(cours)
                except:
                    pass
        if types == "hot":
            courses = Course.objects.filter(Q(is_click=True)).order_by('-favorite_count').all()

        pn, pt, pl, pp, np, ppn, npn, cp, pr = instance_pager(courses, int(page), settings.GLOBAL_PAGESIZE)
        # for li in pl:
        #   json_str+='{"name":"'+str(li.name)+'","image":"'+settings.MEDIA_URL+str(li.image)+'","student_count":"'+str(li.student_count)+'","course_id":'+str(li.id)+'},'
        # json_str=json_str[:-1]
        # json_str +=']'
        # return HttpResponse(json_str)
        p_json = [{"name": p.name,
                   "image": settings.MEDIA_URL + str(p.image),
                   "student_count": p.student_count,
                   "course_id": p.id} for p in pl]

        template_vars = p_json

        cache.set('index_course_ajax_page_' + str(types) + '_' + str(page), template_vars, settings.CACHE_TIME)

    return HttpResponse(json.dumps(template_vars), content_type="application/json")


def teacher_list():
    try:
        group = Group.objects.get(name='老师')  # 所有老师
        te_list = Course.objects.distinct().values_list('teacher')
        teachers = group.user_set.filter(id__in=te_list).order_by("-id")

    except Exception, e:
        logger.error(e)
        return None
    return teachers


# 404错误页面
def page_not_found(request):
    # 这段代码以后要去掉
    path_url = request.path
    arr_path = path_url.split('/')
    list_2 = [i for i in arr_path if i != '']
    arr_len = len(list_2)
    if arr_len == 2:
        CourseType = list_2[0]
        CourseNum = list_2[1]
        if CourseType == "career":
            if int(CourseNum) == 10:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/7/")
            elif int(CourseNum) == 11:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/3/")
            elif int(CourseNum) == 2521:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/3/")
            elif int(CourseNum) == 2526:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/")
            elif int(CourseNum) == 2670:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/3/")
            elif int(CourseNum) == 2672:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/8/")
        if CourseType == 'news':
            return HttpResponsePermanentRedirect("http://forum.maiziedu.com")
    if arr_len == 3 and list_2[1] == 'node':
        if list_2[0] == 'search':
            if list_2[2].lower() == 'Java'.lower():
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/java.html?osc=java")
            if list_2[2].lower() == 'PHP'.lower():
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/php.html?osc=php")
            if list_2[2].lower() == 'android'.lower() or list_2[2] == '安卓':
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/android.html?osc=android")
            if list_2[2].lower() == 'cocos2d-x'.lower() or list_2[2].lower() == 'cocos2d'.lower():
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/cocos2d.html?osc=cocos2d")
            if list_2[2] == '嵌入式':
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/embed.html?osc=qrs")
            if list_2[2].lower() == 'ios'.lower() or list_2[2].lower() == 'swift':
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/iOS.html?osc=ios")
            if list_2[2] == '产品经理':
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/pm.html?osc=pm")
            if list_2[2].lower() == 'python'.lower():
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/pages/ad04/python.html?osc=python")
        return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/")

    response = render_to_response('mz_common/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


# 500错误页面
def page_error(request):
    return render(request, 'mz_common/500.html')


# 维护模式页面
def page_maintenance(request):
    fileHandle = open('maintenance.txt')
    fileList = fileHandle.readlines()
    fileHandle.close()
    return render(request, 'mz_common/503.html', locals())


# 定义共用的上下文处理器
def common_context(request):
    email_register_form = EmailRegisterForm()
    mobile_register_form = MobileRegisterForm()
    find_password_form = FindPasswordForm()
    update_password_form = UpdatePasswordForm()
    find_password_mobile_form = FindPasswordMobileForm()
    login_form = LoginForm()
    # 最新消息条数
    new_message_count = 0
    if request.user.is_authenticated():
        if request.user.is_teacher():
            message_type = [51, 22, 23]
        else:
            message_type = [11, 50, 21, 22]
        new_message_count = MyMessage.objects.filter(userB=request.user.id, is_new=True,
                                                     action_type__in=message_type).count()
    # bbs_site_url = settings.BBS_SITE_URL

    # all_career_courses = cache.get('all_career_courses')
    # if not all_career_courses:
    #     all_career_courses = []
    #     # all_career_courses = CareerCourse.objects.filter(course_scope=None).order_by("-click_count")
    #     institute_lst = Institute.objects.all().order_by("order")
    #     for institute in institute_lst:
    #         career_course_lst = CareerCourse.objects.filter(course_scope=None, institute_id=institute.id, ).order_by(
    #             "-click_count")
    #         all_career_courses.append({'name': institute.name, 'career_course_lst': career_course_lst})
    #     cache.set('all_career_courses', all_career_courses, settings.CACHE_TIME * 6 * 24)

    text_links = cache.get('text_links')
    if not text_links:
        text_links = Links.objects.filter(is_pic=0)
        cache.set('text_links', text_links, settings.CACHE_TIME * 6 * 24)
    # 报名倒计时（运营）
    # deadline = datetime(2016,3,1)
    # now_time = datetime.now()
    # seconds_countdown= int((deadline-now_time).total_seconds())
    locals = {
        "email_register_form": email_register_form,
        "mobile_register_form": mobile_register_form,
        "find_password_form": find_password_form,
        "update_password_form": update_password_form,
        "find_password_mobile_form": find_password_mobile_form,
        "login_form": login_form,
        "new_message_count": new_message_count,
        # "bbs_site_url": bbs_site_url,
        # "all_career_courses": all_career_courses,
        "text_links": text_links,
        "FPS_HOST": settings.FPS_HOST,
        "FPS_CENTER": settings.FPS_CENTER,
        "SITE_URL": settings.SITE_URL,
        "head_user": request.user,
		"WAP_AD_URL": settings.WAP_AD_URL,

		'mobile_site': settings.MOBILE_SITE,
        'time_stamp': 201703281700,
    }
    return locals


# 论坛消息条数调用接口
@csrf_exempt
def get_new_message_count(request):
    # 最新消息条数
    new_message_count = 0
    if request.user.is_authenticated():
        new_message_count = MyMessage.objects.filter(Q(userB=request.user.id) | Q(userB=0, action_type=1),
                                                     Q(is_new=True)).count()
    return HttpResponse(new_message_count)


# APP下载终端扫描地址
def terminal(request):
    ANDROID_DOWN_URL = settings.ANDROID_DOWN_URL
    IOS_DOWN_URL = settings.IOS_DOWN_URL
    WINPHONE_DOWN_URL = settings.WINPHONE_DOWN_URL
    IPAD_DOWN_URL = settings.IPAD_DOWN_URL
    return render(request, 'mz_common/terminal.html', locals())


# 热门搜索关键词推荐
def recommend_keyword(request):
    template_vars = cache.get('recommend_keyword')
    if not template_vars:
        try:
            keywords = RecommendKeywords.objects.all()[:10]
            keywords = [{"name": keyword.name} for keyword in keywords]
        except Exception as e:
            keywords = []

        template_vars = keywords

        cache.set('recommend_keyword', template_vars, settings.CACHE_TIME)

    return HttpResponse(json.dumps(template_vars),
                        content_type="application/json")


# 课程搜索
def course_search(request):
    keyword = request.GET['keyword'] or ""

    try:

        if keyword == "":
            courses = []
            careerCourses = []
            raise Exception()

        courses = Course.objects.filter(Q(name__icontains=keyword) |
                                        Q(search_keywords__name__icontains=keyword), Q(is_click=True),
                                        Q(is_homeshow=True)
                                        ).distinct()
        careerCourses = CareerCourse.objects.filter(Q(name__icontains=keyword) |
                                                    Q(search_keywords__name__icontains=keyword), Q(course_scope=None)
                                                    ).distinct()
        # courseStage = Course_Stages_m.objects.filter(course_id=course.id).first().stage_id
        courses = [{"id": course.id,
                    "name": course.name,
                    "course_color": settings.DEFAULT_COLOR,
                    "image": str(course.image),
                    "stage_id": Course_Stages_m.objects.filter(
                        course_id=course.id).first().stage_id if Course_Stages_m.objects.filter(
                        course_id=course.id) else ''} for course in courses]
        careerCourses = [{"id": course.id,
                          "name": course.name,
                          "course_color": course.course_color,
                          "image": str(course.image)} for course in careerCourses]

    except Exception as e:
        courses = []
        careerCourses = []
        logger.error(e)

    finally:
        coursesResult = {"courses": courses, "career_courses": careerCourses}
        return HttpResponse(json.dumps(coursesResult), content_type="application/json")


############### lps 开始##############################
# 获取该用户是第几次重修某个课程
def get_rebuild_count(user, course):
    '''
    获取该用户是第几次重修某个课程
    :param user: 用户对象
    :param course: 课程对象
p    :return:
    '''
    course_score = CourseScore.objects.filter(user_id=user.id, course=course).order_by("-rebuild_count")
    if course_score.count() > 0:
        return course_score[0].rebuild_count
    return 0


# 获取某个试卷下学生还未完成的试题列表
def get_uncomplete_quiz(user, paper, rebuild_count):
    '''
    获取某个试卷下学生还未完成的试题列表
    :param user: 用户对象
    :param paper: 试卷对象
    :param rebuild_count: 第几次重修
    :return:
    '''
    # 已经做过的试题ID列表
    quiz_record_list = []
    # 获取做题记录
    paper_record_list = PaperRecord.objects.filter(paper=paper, student=user, rebuild_count=rebuild_count)
    if len(paper_record_list) > 0:
        quiz_record_list = QuizRecord.objects.filter(paper_record=paper_record_list[0]).values_list("quiz")
        # 已经做过的题目则不再显示
    return Quiz.objects.filter(Q(paper=paper), ~Q(id__in=quiz_record_list))


# 检查测验分所有考核项是否已经完成
def check_exam_is_complete(user, course):
    '''
    检查测验分所有考核项是否已经完成
    :param user: 用户对象
    :param course: 课程对象
    :return: 0 考核未完成，1 考核已完成，2 没有考核项
    '''
    course_score = CourseScore.objects.filter(user=user, course=course).order_by("-rebuild_count")
    exam_status = check_exam_item_status(course)

    if exam_status['has_count'] == 0:
        return 2
    if len(course_score) > 0:
        # 检查是否完成项目考核并评分
        # 检查是否完成项目测验
        if exam_status['course_has_project']:
            project_list = Project.objects.filter(examine_type=5, relation_type=2, relation_id=course.id)
            if len(project_list) > 0:
                if ProjectRecord.objects.filter(Q(project=project_list[0]), Q(student=user),
                                                Q(rebuild_count=course_score[0].rebuild_count),
                                                ~Q(score=None)).count() == 0:
                    return 0
        # 检查是否完成课程总测验
        if exam_status['course_has_exam']:
            # 获取所有章节对应的paper
            # if paper_list is None:
            paper_list = Paper.objects.filter(examine_type=2, relation_type=2, relation_id=course.id)
            # 检查试卷是否完成
            if not check_iscomplete_paper_exam(paper_list, user, course_score[0].rebuild_count):
                return 0
        # 检查是否完成所有随堂测验
        if exam_status['lesson_has_exam']:
            # 获取该课程下所有lesson的测验是否已经完成并评分
            # 有随堂测验考核项的所有章节ID列表
            lesson_has_exam_list = []
            # 获取该课程下所有章节ID列表
            lesson_list = course.lesson_set.all().values_list("id")
            for lesson in lesson_list:
                if lesson_has_exam(lesson[0]):
                    lesson_has_exam_list.append(lesson[0])
            # 获取所有章节对应的paper
            # if paper_list is None:
            paper_list = Paper.objects.filter(examine_type=2, relation_type=1, relation_id__in=lesson_has_exam_list)
            # 继续检查试卷试题是否有做完
            if not check_iscomplete_paper_exam(paper_list, user, course_score[0].rebuild_count):
                return 0
        return 1
    return 0


# 检查学生是否已经完成试卷
def check_iscomplete_paper_exam(paper_list, user, rebuild_count):
    for paper in paper_list:
        quiz_count = Quiz.objects.filter(paper=paper).count()  # 试卷拥有的题目数量
        paper_record = PaperRecord.objects.filter(Q(paper=paper), Q(student=user), Q(rebuild_count=rebuild_count),
                                                  ~Q(score=None))  # 试卷对应考核记录
        if len(paper_record) > 0:
            quizrecord_count = QuizRecord.objects.filter(paper_record=paper_record).count()  # 学生已做的试题数量
            if quiz_count > quizrecord_count:
                return False  # 还有题目未做完
        else:
            return False  # 还有试卷未完成
    return True


# 更新学力和测验分
# stage_id需要用关键字赋值
def update_study_point_score(student, study_point=None, score=None, examine=None, examine_record=None, teacher=None,
                             course=None, rebuild_count=None, lesson_id=0, update_type=0):
    '''
    更新学力和测验分
    :param student: 学生对象
    :param study_point: 学力加分（可选项）
    :param score: 测验分加分（可选项）
    :param examine: 考核对象（可选项）
    :param examine_record: 考核记录对象（可选项）
    :param teacher: 老师对象（可选项）
    :param course: 课程（可选项）,更新非考核产生的学力和学分时候需传入
    :param rebuild_count: 第几次重修（可选项）
    :return:
    '''

    am_dict = {}
    am_dict["student"] = -1 if student is None else student.id
    am_dict["study_point"] = study_point
    am_dict["score"] = score
    am_dict["examine"] = -1 if examine is None else examine.id
    am_dict["examine_record"] = -1 if examine_record is None else examine_record.id
    am_dict["teacher"] = -1 if teacher is None else teacher.id
    am_dict["course"] = -1 if course is None else course.id
    am_dict["rebuild_count"] = rebuild_count
    am_dict["lesson_id"] = lesson_id
    am_dict["update_type"] = update_type

    temp = json.dumps(am_dict)
    this_async_method_list = AsyncMethod.objects.filter(methods=temp)
    if len(this_async_method_list) > 0:
        return

    async_method = AsyncMethod()
    async_method.calc_type = 1
    async_method.priority = 3
    async_method.methods = temp  # json.dumps(am_dict) #JSONEncoder.encode(am_dict)
    async_method.save()

    # 更新学生最后学习时间
    if not course:
        return

    stages = course.stages_m.all()
    for stage in stages:
        classobjs = ClassStudents.objects.filter(user=student, student_class__career_course=stage.career_course)
        if classobjs:
            classobj = classobjs[0]
            classobj.latest_study_datetime = async_method.submit_datetime
            classobj.save()


# def update_study_point_score(student, study_point=None, score=None, examine=None, examine_record=None, teacher=None, course=None, rebuild_count=None):
#     '''
#     更新学力和测验分
#     :param student: 学生对象
#     :param study_point: 学力加分（可选项）
#     :param score: 测验分加分（可选项）
#     :param examine: 考核对象（可选项）
#     :param examine_record: 考核记录对象（可选项）
#     :param teacher: 老师对象（可选项）
#     :param course: 课程（可选项）,更新非考核产生的学力和学分时候需传入
#     :param rebuild_count: 第几次重修（可选项）
#     :return:
#     '''
#
#     if course is None:
#         cur_course = Course()
#     else:
#         cur_course = course
#         # 根据考核对象类型找到相应对象
#     # 章节
#     if examine is not None and examine_record is not None:
#         if examine.relation_type == 1:
#             cur_lesson = Lesson.objects.filter(pk=examine.relation_id)
#             if len(cur_lesson) > 0:
#                 cur_course = cur_lesson[0].course
#         #课程
#         elif examine.relation_type == 2:
#             cur_course = Course.objects.filter(pk=examine.relation_id)
#             if len(cur_course)  > 0:
#                 cur_course = cur_course[0]
#
#         if rebuild_count is None:
#             rebuild_count = get_rebuild_count(student, cur_course)
#
#         # 更新考核记录学力
#         if score is not None:
#             examine_record.score = score  # 计算该试卷测验得分
#             if teacher is not None:
#                 examine_record.teacher = teacher
#         if study_point is not None:
#             examine_record.study_point = study_point   # 学力
#         examine_record.save()
#
#         # 在coursescore中更新测验分
#         check_course_score(student, cur_course) # 检查是否有course_score记录,没有则创建
#         if examine.examine_type in(2,5) and score is not None:
#             course_score = CourseScore.objects.filter(user=student,course=cur_course,rebuild_count=rebuild_count)
#             if len(course_score):
#                 # 考试测验
#                 # 试卷类型测验分
#                 if examine.examine_type == 2:
#                     # 随堂测验
#                     if examine.relation_type == 1:
#                         # 获取所有章节id列表
#                         lesson_list = cur_course.lesson_set.all().values_list("id")
#                         lesson_total_score = 0
#                         # 获取所有章节对应的paper
#                         paper_list = Paper.objects.filter(examine_type=2, relation_type=1, relation_id__in=lesson_list).values_list("id")
#                         # 获取所有章节对应的paperrecord
#                         paper_record_list = PaperRecord.objects.filter(Q(student=student),Q(paper__in=paper_list),Q(rebuild_count=rebuild_count),~Q(score=None))
#                         # 计算随堂测验总分
#                         for paper_record in paper_record_list:
#                             lesson_total_score += (100 / len(paper_list)) * paper_record.accuracy
#                         course_score[0].lesson_score = int(round(lesson_total_score))
#                     # 课程总测验
#                     elif examine.relation_type == 2:
#                         course_score[0].course_score = score
#                 # 项目类型测验分
#                 elif examine.examine_type == 5:
#                     course_score[0].project_score = score
#                     # 检查测验分考核项是否已经完全考核
#                 if check_exam_is_complete(student, cur_course) == 1:
#                     course_score[0].is_complete = True  # 所有测验完成状态
#                     course_score[0].complete_date = datetime.now()  # 测验完成时间
#
#                     for stage in cur_course.stages_m.all():
#                         stage_id = stage.id
#                         career_course = Stage.objects.get(pk = stage_id).career_course
#                         # 如已完成所有考核项，则发送课程通过与否的站内消息
#                         total_score = get_course_score(course_score[0], cur_course)
#                         if total_score >= 60:
#                             sys_send_message(0, student.id, 1, "恭喜您已通过<a href='/lps2/learning/plan/"+str(career_course.id)+"/'>"+
#                                                                str(cur_course.name)+"</a>课程，总获得测验分"+str(total_score)+
#                                                                "分！<a href='/lps2/learning/plan/"+str(career_course.id)+"/'>继续学习下一课</a>")
#                         else:
#                             sys_send_message(0, student.id, 1, "您的课程<a href='/lps2/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_id)+"'>"+str(cur_course.name)+
#                                                                "</a>挂科啦。不要灰心，<a href='/lps2/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_id)+"'>去重修</a>")
#                             # 继续检查是否完成该阶段的所有考核项
#                         if check_stage_exam_is_complete(student, cur_course, stage):
#                             # 如果完成了所有考核项，则检查该课程对应职业课程的所有阶段和解锁信息
#                             stage_list = Stage.objects.filter(career_course=stage.career_course)
#                             cur_stage_count = 0
#                             for i,stage in enumerate(stage_list):
#                                 if stage.id == stage_id:
#                                     cur_stage_count = i
#                                     break
#                             if (cur_stage_count+1) < len(stage_list):
#                                 # 检查下一个阶段是否已经解锁
#                                 if UserUnlockStage.objects.filter(user=student, stage=stage_list[cur_stage_count+1]).count()>0:
#                                     # 已经解锁
#                                     msg = "恭喜您能努力坚持学完"+career_course.name+"的第"+str(cur_stage_count+1)+"阶段，赶快继续深造吧，你离梦想仅一步之遥了哦！<a href='/lps/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_list[cur_stage_count+1].id)+"'>立即学习下一阶段</a>"
#                                 else:
#                                     # 还未解锁
#                                     msg = "恭喜您能努力坚持学完"+career_course.name+"的第"+str(cur_stage_count+1)+"阶段，赶快续费继续深造吧，你离梦想仅一步之遥了哦！<a href='/lps/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_list[cur_stage_count+1].id)+"'>立即购买下一阶段</a>"
#                             else:
#                                 msg = "恭喜您能努力坚持学完"+career_course.name+"所有课程，你还可以继续深造哦！<a href='/course/'>去选课程</a>"
#                             sys_send_message(0, student.id, 1, msg)
#                 else:
#                     # 如果是未完成所有考核项，但是测验分已经超过了60分，则可以判定课程通过，提前更新课程测验完成状态
#                     if get_course_score(course_score[0], cur_course) >= 60:
#                         course_score[0].is_complete = True  # 所有测验完成状态
#                 course_score[0].save()
#
#     # 更新班级学力汇总信息
#     if study_point > 0 and rebuild_count == 0:
#         for stage in cur_course.stages_m:
#             stage_id = stage.id
#             class_students = ClassStudents.objects.filter(user=student,student_class__career_course=Stage.objects.get(pk = stage_id).career_course)
#             if len(class_students)>0:
#                 class_students[0].study_point += study_point
#                 class_students[0].save()

# 检查某个阶段的所有考核项是否都已经完成
def check_stage_exam_is_complete(student, cur_course, stage):
    # 根据当前课程找到对应阶段下所有课程


    course_list = Course.objects.filter(stages_m=stage)
    for course in course_list:
        if course == cur_course:
            continue
        # 检查课程是否完成
        if check_exam_is_complete(student, course) == 0:
            return False
        if check_exam_is_complete(student, course) == 2:
            continue
    return True


# 检查课程各个考核项的状态
def check_exam_item_status(course):
    has_count = 0  # 测验分考核项计数
    lesson_has_exam = False
    course_has_exam = False
    course_has_project = False
    try:
        # 判断课程拥有几项评测分项（随堂测验？总测验？项目制作？）
        # 是否有随堂测验
        # 根据找到对应的paper
        paper_list = Paper.objects.filter(examine_type=2, relation_type=1,
                                          relation_id__in=course.lesson_set.all().values_list("id"))
        if Quiz.objects.filter(paper__in=paper_list).count() > 0:
            lesson_has_exam = True
            has_count += 1

        # 是否有总测验
        paper = Paper.objects.filter(examine_type=2, relation_type=2, relation_id=course.id)
        if Quiz.objects.filter(paper__in=paper).count() > 0:
            course_has_exam = True
            has_count += 1

        # 是否有项目制作
        if Project.objects.filter(examine_type=5, relation_type=2, relation_id=course.id).count() > 0:
            course_has_project = True
            has_count += 1
    except Exception, e:
        logger.error(e)
    return {'has_count': has_count,
            'lesson_has_exam': lesson_has_exam,
            'course_has_exam': course_has_exam,
            'course_has_project': course_has_project}


# 获取用户某门课程实际得分
def get_course_score(course_score, course=None):
    score = 0
    try:
        if course == None:
            course = Course.objects.get(pk=course_score.course.id)

        # 获取课程的各个考核项状态
        exam_status = check_exam_item_status(course)

        # Modify By Steven YU
        if course_score.lesson_score is None:
            ls = 0
        else:
            ls = course_score.lesson_score

        if course_score.course_score is None:
            cs = 0
        else:
            cs = course_score.course_score

        if course_score.project_score is None:
            ps = 0
        else:
            ps = course_score.project_score
        # Modify end


        if exam_status['has_count'] == 3:
            score = int(
                ls * settings.LESSON_EXAM_RATE + cs * settings.COURSE_EXAM_RATE + ps * settings.PROJECT_EXAM_RATE)
        elif exam_status['has_count'] == 2:
            # 随堂测验+课堂总测验
            if exam_status['lesson_has_exam'] and exam_status['course_has_exam']:
                lesson_exam_rate = settings.LESSON_EXAM_RATE / (settings.LESSON_EXAM_RATE + settings.COURSE_EXAM_RATE)
                course_exam_rate = settings.COURSE_EXAM_RATE / (settings.LESSON_EXAM_RATE + settings.COURSE_EXAM_RATE)
                score = ls * lesson_exam_rate + cs * course_exam_rate
            # 课堂总测验+项目制作
            elif exam_status['course_has_exam'] and exam_status['course_has_project']:
                course_exam_rate = settings.COURSE_EXAM_RATE / (settings.COURSE_EXAM_RATE + settings.PROJECT_EXAM_RATE)
                project_exam_rate = settings.PROJECT_EXAM_RATE / (
                    settings.COURSE_EXAM_RATE + settings.PROJECT_EXAM_RATE)
                score = cs * course_exam_rate + ps * project_exam_rate
            # 随堂测验+项目制作
            elif exam_status['lesson_has_exam'] and exam_status['course_has_project']:
                lesson_exam_rate = settings.LESSON_EXAM_RATE / (settings.LESSON_EXAM_RATE + settings.PROJECT_EXAM_RATE)
                project_exam_rate = settings.PROJECT_EXAM_RATE / (
                    settings.LESSON_EXAM_RATE + settings.PROJECT_EXAM_RATE)
                score = ls * lesson_exam_rate + ps * project_exam_rate
        else:
            rate = 0
            if exam_status['has_count'] == 1:
                rate = settings.HAS_1_EXAM_RATE
            if exam_status['lesson_has_exam']:
                score += ls * rate
            elif exam_status['course_has_exam']:
                score += cs * rate
            elif exam_status['course_has_project']:
                score += ps * rate

    except Exception as e:
        logger.error(e)
    return int(score)


# 检查coursescore里面是否有对应记录,没有则增加一条rebuild_count为0的数据
def check_course_score(user, course):
    if CourseScore.objects.filter(user=user, course=course).count() == 0:
        course_score = CourseScore()
        course_score.user = user
        course_score.course = course
        course_score.save()


# 获取当前用户学力
def current_study_point(careercourse, user):
    ret = {}
    try:
        classobj = ClassStudents.objects.get(user=user, student_class__career_course=careercourse)
        mypoint = classobj.study_point
        ret['classobj'] = classobj
        ret['mypoint'] = mypoint
        return ret
    except ClassStudents.DoesNotExist:
        message = 'NotSignUp'  # 没有报名
        return message
    except Exception, e:
        logger.error(e)


# 当前班级用户的学力排行用户
def all_stu_ranking(careercourse, user):
    ret = current_study_point(careercourse, user)
    if ret == "NotSignUp":
        return "NotSignUp"
    else:
        current_user_class = ret['classobj'].student_class  # 当前用户所在的班级ID
        # current_user_class = Class.objects.get(id='11')
        curren_all_stu = ClassStudents.objects.filter(student_class__career_course=careercourse,
                                                      student_class=current_user_class).order_by('-study_point')
        return curren_all_stu


# 获取用户当前排名
def current_user_ranking(careercourse, user):
    curren_all_stu = all_stu_ranking(careercourse, user)
    i = 0
    if curren_all_stu == "NotSignUp":
        return "NotSignUp"
    else:
        for stu in curren_all_stu:
            i += 1
            if stu.user.id == user.id:
                break
    return i


# 作业和项目文件上传函数
def file_upload(files, dirname):
    if files.size / 1024 > settings.JOB_SIZE_LIMIT:
        return (False, "文件大小超过" + str(settings.JOB_SIZE_LIMIT) + "KB限制")
    if settings.JOB_SUFFIX_LIMIT.find(files.name.split(".")[-1].lower()) == -1:
        return (False, "文件必须为ZIP/RAR格式")
    path = os.path.join(settings.MEDIA_ROOT, upload_generation_dir(dirname))
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + str(files.name.split(".")[-1])
    path_file = os.path.join(path, file_name)
    db_file_url = path_file.split("..")[-1].replace('/uploads', '').replace('\\', '/')[1:]
    status = open(path_file, 'wb').write(files.file.read())
    return (True, "文件上传成功", db_file_url)


# 判断章节是否有测验题
def lesson_has_exam(lesson_id):
    if Paper.objects.filter(examine_type=2, relation_type=1, relation_id=lesson_id).count() == 0:
        return False
    return True


# 是否有课后作业
def lesson_has_homework(lesson_id):
    if Homework.objects.filter(examine_type=1, relation_type=1, relation_id=lesson_id).count() == 0:
        return False
    return True


############### lps 结束##############################

class paging():
    '''
    此为文章分页功能，需要往里传递三个参数，分别如下：
    res:结果集
    page:页码号，即第几页,这个一般从URL的GET中得到
    pagenum:每页显示多少条记录
    '''

    def __init__(self, res, page, pagenum):
        self.res = res
        self.page = int(page)
        self.pagenum = int(pagenum)
        # tn = self.tablename.objects.all().order_by('-id') #查询tablename表中所有记录数，并以降序的方式对id进行排列
        self.p = Paginator(res, self.pagenum)  # 对表数据进行分页，每页显示pagenum条

    def pt(self):
        '''共有多少条数据'''
        return self.p.count

    def pn(self):
        '''总页数'''
        return self.p.num_pages

    def pr(self):
        '''获取页码列表'''
        return self.p.page_range

    def pl(self):
        '''第page页的数据列表'''
        return self.p.page(self.page).object_list

    def pp(self):
        '''是否有上一页'''
        return self.p.page(self.page).has_previous()

    def np(self):
        '''是否有下一页'''
        return self.p.page(self.page).has_next()

    def ppn(self):
        '''上一页的页码号'''
        if self.page <= 1:  # 假如当前页在第一页，那就直接返回1
            return '1'
        else:
            return self.p.page(self.page).previous_page_number()

    def npn(self):
        '''下一页的页码号'''
        if self.p.page(self.page).has_next() == False:  # 如果当前页不存在下一页，则返回最后一个页码值
            return self.page
        else:
            return self.p.page(self.page).next_page_number()


def instance_pager(obj, curren_page, page_size=5):
    if not curren_page:
        curren_page = 1
    p = paging(obj, curren_page, page_size)  # 实例化分页类
    pn = p.pn()  # 总页数
    pt = p.pt()  # 共有多少条数据
    pl = p.pl()  # 第x页的数据列表
    pp = p.pp()  # 是否有前一页
    np = p.np()  # 是否有后一页
    ppn = p.ppn()  # 前一页页码
    npn = p.npn()  # 后一页页码
    cp = int(curren_page)  # 获取当前页，并转为型形，方便下面进行计算和比较，并且模板文件中也要用到比较
    if cp < 5:  # 这里进行判断，假如当前页小于5的时候，
        pr = p.pr()[0:5]  # pr为获取页码列表，即当前页小于5的时候，模板中将显示第1页至第5页，如 1 2 3 4 5
    elif int(pn) - cp < 5:  # 假如最后页减当前页小于5时
        pr = p.pr()[int(pn) - 5:int(pn)]  # 页码列表显示最后5页，如共有30页的话，那显示：26 27 28 29 30
    else:  # 其它情况
        pr = p.pr()[cp - 3:cp + 2]  # 其它情况显示当前页的前4条至后4条，如当前在第10页的话，那显示：6 7 8 9 10
    return pn, pt, pl, pp, np, ppn, npn, cp, pr


def sys_send_message(A_id, B_id, action_type, content, action_id=None, career_id=0):
    """
    添加我的消息(站内信)
    @A_id:发送方，为0表示系统用户
    @B_id:接收方，为0就给所有用户发送消息
    @action_type: ('1','系统消息'),('2','课程讨论回复'),('3','论坛讨论回复'),
    @content：消息内容
    """
    if A_id != B_id:
        try:
            if int(action_type) in [14, 15, 16, 17]:  # 防止重复发送
                try:
                    MyMessage.objects.get(userA=A_id, userB=B_id, action_type=action_type,
                                          action_id=action_id)
                    return True
                except MyMessage.DoesNotExist:
                    pass

            msg = MyMessage()
            msg.userA = A_id
            msg.userB = B_id
            msg.action_type = action_type
            if action_id is not None:
                msg.action_id = action_id
            msg.action_content = content
            msg.save()
            # app推送
            if int(action_type) in [10, 11, 12, 14, 15, 16, 18, 19, 50]:
                app_push_message(B_id, int(action_type), content, career_id)

        except Exception as e:
            logger.error(e)
            return False
    return True


# app推送
def app_push_message(user_id, message_type, content, career_id):
    user = UserProfile.objects.get(id=int(user_id))
    if not user.token:
        return True
    # 1 学习提醒 2 班级动态 3 系统通知 4 任务地图
    if message_type == 14:
        push_type = 4
    elif message_type == 12:
        content = '你有一个班会即将开始'
        push_type = 5
    elif message_type in [11, 15]:
        push_type = 1
    elif message_type in [10, 17]:
        push_type = 2
    else:
        # if message_type == 1:
        #     if content.find('您已成功报名课程') == -1:
        #         return True
        push_type = 3

    app_num, if_created = AppSendMessageNum.objects.get_or_create(user=int(user_id))
    app_num.message_count += 1
    app_num.save()
    app_send_message_token('麦子学院', strip_tags(content), user.token, app_num.message_count,
                           career_id, app_type=push_type)


# Add by Steven YU
def app_send_message_token(title, content, token, count, career_id, client="all", app_type=1):
    """
    给app客户端推送消息
    :param title: 消息标题
    :param content: 消息内容
    :param token: 发送对象
    :param count: 未读数量
    :param career_id: 班级课程id
    :param client: 发送客户端类型
    :param app_type: 发送类型
    :return: True 成功，False 失败
    """
    try:
        if not settings.IS_SEND_MESSAGE:
            return True
        # ios通知
        if client == "ios" or client == "all":
            xg = xinge.XingeApp('2200080799', '13a1053f8dd211307ccbcd9582364033')
            msg = xinge.MessageIOS()
            # alert字段可以是字符串或json对象，参见APNS文档
            msg.alert = content
            # 消息为离线设备保存的时间，单位为秒。默认为0，表示只推在线设备
            msg.expireTime = 259200
            msg.custom = {"message_type": app_type,
                          'career_id': career_id
                          }
            msg.badge = count
            xg.PushSingleDevice(token, msg, xinge.XingeApp.ENV_PROD)
            # ENV_PROD = 1  生产环境
            # ENV_DEV = 2   开发环境

        # android 通知
        if client == "android" or client == "all":
            xg = xinge.XingeApp(settings.XG_ACCESS_ID, settings.XG_SECRET_KEY)
            msg = xinge.Message()
            msg.type = xinge.Message.TYPE_NOTIFICATION
            msg.title = title
            msg.content = content
            # 消息为离线设备保存的时间，单位为秒。默认为0，表示只推在线设备
            msg.expireTime = 259200
            msg.custom = {"message_type": app_type,
                          'career_id': career_id
                          }
            msg.style = xinge.Style(3, 1, 0, 1, 0)
            action = xinge.ClickAction()
            action.actionType = xinge.ClickAction.TYPE_ACTIVITY
            action.activity = "com.maiziedu.app.PushReceiveActivity"
            msg.action = action
            xg.PushSingleDevice(token, msg, xinge.XingeApp.ENV_DEV)

    except Exception as e:
        logger.error(e)
        return False
    return True


def app_send_message(title, content, account_list, client="all"):
    '''
    给app客户端推送消息
    :param title: 消息标题
    :param content: 消息内容
    :param account_list: 发送对象，为[]则给所有设备（所有用户）推送
    :param client: 发送客户端类型
    :return: True 成功，False 失败
    '''
    # try:
    #
    #
    #     # ios通知
    #     if client == "ios" or client == "all":
    #         if settings.IS_IOS_SEND_MESSAGE:
    #             count = 1
    #             try:
    #                 for token in account_list:
    #                     user = UserProfile.objects.get(token=token)
    #                     obj = AppSendMessageNum.objects.get(user=user)
    #                     count = obj.message_count + obj.dynamic_count
    #             except:
    #                 pass
    #             xg = xinge.XingeApp('2200080799', '13a1053f8dd211307ccbcd9582364033')
    #             msg = xinge.MessageIOS()
    #             # alert字段可以是字符串或json对象，参见APNS文档
    #             msg.alert = content
    #             # 消息为离线设备保存的时间，单位为秒。默认为0，表示只推在线设备
    #             msg.expireTime = 259200
    #             msg.custom = {"type": 1}
    #             msg.badge = count
    #             if len(account_list) > 0:
    #                 for account in account_list:
    #                     xg.PushSingleDevice(account, msg, xinge.XingeApp.ENV_PROD)
    #             elif len(account_list) == 0:
    #                 xg.PushAllDevices(0, msg, xinge.XingeApp.ENV_PROD)
    #
    #     # android 通知
    #     if client == "android" or client == "all":
    #         xg = xinge.XingeApp(settings.XG_ACCESS_ID, settings.XG_SECRET_KEY)
    #         msg = xinge.Message()
    #         msg.type = xinge.Message.TYPE_NOTIFICATION
    #         msg.title = title
    #         msg.content = content
    #         # 消息为离线设备保存的时间，单位为秒。默认为0，表示只推在线设备
    #         msg.expireTime = 259200
    #         msg.style = xinge.Style(3, 1, 0, 1, 0)
    #         action = xinge.ClickAction()
    #         action.actionType = xinge.ClickAction.TYPE_ACTIVITY
    #         action.activity="com.maiziedu.app.PushReceiveActivity"
    #         msg.action = action
    #         if len(account_list) > 0:
    #             for account in account_list:
    #                 print xg.PushSingleDevice(account, msg, xinge.XingeApp.ENV_DEV)
    #         elif len(account_list) == 0:
    #             xg.PushAllDevices(0, msg)
    #
    # except Exception as e:
    #     logger.error(e)
    #     return False
    return True


# app页面
def apppage(request):
    template_vars = cache.get('apppage')
    if not template_vars:
        text_links = Links.objects.filter(is_pic=0)
        # 首页SEO信息读取
        seo = PageSeoSet()
        try:
            seo = PageSeoSet.objects.get(page_name='2')
        except Exception as e:
            logger.error(e)

        template_vars = {'text_links': text_links, 'seo': seo, 'ANDROID_DOWN_URL': '', 'IOS_DOWN_URL': '',
                         'WINPHONE_DOWN_URL': '', 'IPAD_DOWN_URL': ''}

        cache.set('apppage', template_vars, settings.CACHE_TIME)

    template_vars['ANDROID_DOWN_URL'] = settings.ANDROID_DOWN_URL
    template_vars['IOS_DOWN_URL'] = settings.IOS_DOWN_URL
    template_vars['WINPHONE_DOWN_URL'] = settings.WINPHONE_DOWN_URL
    template_vars['IPAD_DOWN_URL'] = settings.IPAD_DOWN_URL
    # 改变base.html 样式
    template_vars['apppage_display'] = True
    return render(request, 'mz_common/app.html', template_vars)


# 手机搜索页面
def mobile_search(request):
    user = request.user
    return render(request, 'mz_common/mobile_search.html', locals())


# 重定向到老网站的手机接口
@csrf_exempt
def old_redirect(request):
    # 如果判断是post提交过来的接口，进行单独处理
    return HttpResponseRedirect('/')


def faq(request):
    return render(request, 'mz_common/faq.html', locals())


def activitypage(request):
    return render(request, 'mz_common/activitypage.html', locals())


def def_1017(request):
    return render(request, 'mz_common/1017.html', locals())


def def_1018(request):
    return render(request, 'mz_common/1018.html', locals())


def ios(request):
    return render(request, 'mz_common/ios.html', locals())


def ios8(request):
    return render(request, 'mz_common/ios8.html', locals())


def osc(request):
    return render(request, 'mz_common/osc.html', locals())


def protocol(request):
    return render(request, 'mz_common/protocol.html', locals())


# 获取用户当前某个职业课程下的实际总学力数
def get_study_point(user, career_course):
    # 当前学力总数
    study_point_count = 0
    lesson_list = Lesson.objects.filter(course__stages_m__career_course=career_course).values_list("id")
    course_list = Course.objects.filter(stages_m__career_course=career_course).values_list("id")
    # course_list = Course.objects.filter(stages__career_course=career_course).values_list("id")
    # 观看视频获得学力数
    study_point_count += UserLearningLesson.objects.filter(user=user, lesson__in=lesson_list, is_complete=True).count()
    # 课后作业获得学力数
    homework_list = Homework.objects.filter(examine_type=1, relation_type=1, relation_id__in=lesson_list).values_list(
        "id")
    study_point_count += HomeworkRecord.objects.filter(student=user, homework__in=homework_list,
                                                       rebuild_count=0).count()
    # 随堂测验获得学力数
    paper_list = Paper.objects.filter(examine_type=2, relation_type=1, relation_id__in=lesson_list).values_list("id")
    study_point_count += PaperRecord.objects.filter(student=user, paper__in=paper_list, rebuild_count=0).count()
    # 课程总测验获得学力数
    paper_list = Paper.objects.filter(examine_type=2, relation_type=2, relation_id__in=course_list).values_list("id")
    study_point_count += PaperRecord.objects.filter(student=user, paper__in=paper_list, rebuild_count=0).count() * 10
    # 项目制作获得学力数
    project_list = Project.objects.filter(examine_type=5, relation_type=2, relation_id__in=course_list).values_list(
        "id")
    study_point_count += ProjectRecord.objects.filter(student=user, project__in=project_list,
                                                      rebuild_count=0).count() * 10
    return study_point_count


# 优惠码验证
def coupon_vlidate(request):
    # careercourse
    careercourse = request.REQUEST.get('careercourse', None)
    result = ""
    request.session['code_sno'] = None
    request.session['money'] = None
    CouponCode = request.REQUEST.get("CouponCode", "").strip()
    p = re.compile('^[A-Za-z0-9]+$')
    c = p.match(CouponCode)
    if CouponCode == "":
        result = '{"status":"failure","message":"优惠码不能为空!"}'
    elif len(CouponCode) < 16 or len(CouponCode) > 16 or not (c):
        result = '{"status":"failure","message":"优惠码格式不正确!"}'
    elif careercourse is None:
        result = '{"status":"failure","message":"请选择职业课程!"}'

    if result != "":
        return HttpResponse(result, content_type="application/json")

    coupon_details = Coupon_Details.objects.filter(Q(code_sno=CouponCode))
    if len(coupon_details) > 0:
        coupon = coupon_details[0]
    else:
        return HttpResponse('{"status":"failure","message":"优惠码不存在!"}', content_type="application/json")

    if coupon.is_use:
        result = '{"status":"failure","message":"优惠码已经被使用!"}'
    elif coupon.is_lock and coupon.user != request.user:
        result = '{"status":"failure","message":"优惠码已被其他用户占用!"}'
    elif not (coupon.careercourse_id is None) and careercourse != coupon.careercourse_id:
        try:
            Course = CareerCourse.objects.get(pk=coupon.careercourse_id)
            result = '{"status":"failure","message":"你已经绑定了' + Course.name + '职业课程!"}'
        except Exception as e:
            result = '{"status":"failure","message":"未知错误!"}'
    else:
        if not (coupon.is_lock) and careercourse is not None:
            coupon.is_lock = True
            coupon.user = request.user
            coupon.use_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            coupon.careercourse_id = careercourse
            coupon.save()
        money_obj = Coupon.objects.get(id=coupon.coupon_id)
        money = money_obj.coupon_price
        request.session['code_sno'] = coupon.code_sno
        request.session['money'] = money
        result = '{"status":"success","message":"优惠码可以使用！","money":"' + money + '"}'
    return HttpResponse(result, content_type="application/json")


# 首页企业直通班课程
def index_ajax_careercourse_list(request):
    current_page = request.GET.get('page', '1')
    template_vars = cache.get('index_ajax_careercourse_list_' + str(current_page))
    if not template_vars:
        career_course_list = CareerCourse.objects.filter(course_scope=None).order_by("index", "-id")
        print len(career_course_list)
        lists = {}
        try:
            pagers = paging(career_course_list, int(current_page), 13)
            page_data = pagers.pl()
            if len(page_data) < 13 and pagers.pn() != 1:
                num = 13 - len(page_data)
                pagers_temp = paging(career_course_list, 1, num)
                p_data = pagers_temp.pl()
                page_data = chain(page_data, p_data)  # 返回的为一个迭代器
            lists = {
                'data': [{'id': p.short_name.lower(), 'imgUrl': str(p.image), 'text': p.name, 'bgColor': p.course_color,
                          'count': p.student_count} for p in page_data],
                'PageNum': pagers.pn()
            }
        except EmptyPage:
            pass

        template_vars = lists

        cache.set('index_ajax_careercourse_list_' + str(current_page), template_vars, settings.CACHE_TIME)

    return HttpResponse(json.dumps(template_vars), content_type="application/json")


# app下载
def app_download(request):
    return HttpResponseRedirect("http://www.maiziedu.com/uploads/app/" + str(settings.NEWEST_ANDROID_APP))


# 手机活动页面咨询统计
@csrf_exempt
def app_consult_info_add(request):
    try:
        source = request.POST.get("source", "").strip()
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        qq = request.POST.get("qq", "").strip()
        interest = request.POST.get("interest", "").strip()
        web_from = request.POST.get("web_from", "").strip()
        market_from = 'sem'

        # if source != "":
        #     if source.find("ad10086") >= 0:
        #         market_from = '10086'
        #
        #     source = source.split("?")
        #     if len(source) < 2:
        #         source = ""
        #     else:
        #         source = source[1]
        if web_from != "":
            if web_from == "traditional":
                market_from = "trad"
            else:
                market_from = "operate"
                source = web_from
        _interest = re.findall('.*/(.*).html', interest)
        if _interest:
            interest = _interest[0]
        app_consult_info = AppConsultInfo(market_from=market_from)
        app_consult_info.source = source
        app_consult_info.name = name
        app_consult_info.phone = phone
        app_consult_info.qq = qq
        app_consult_info.interest = interest
        app_consult_info.save()
    except Exception:
        return HttpResponse('{"status":"failure"}', content_type="application/json")
    return HttpResponse('{"status":"success"}', content_type="application/json")


# 手机活动页面咨询统计,信息流来源,支持JSONP跨域请求
@csrf_exempt
def app_consult_info_add_stream(request):
    try:
        if request.method == "GET":
            request_method = request.GET
        else:
            request_method = request.POST
        source = get_param_by_request(request_method, "source", "", str)
        name = get_param_by_request(request_method, "name", "", str)
        phone = get_param_by_request(request_method, "phone", "", str)
        qq = get_param_by_request(request_method, "qq", "", str)
        interest = get_param_by_request(request_method, "interest", "", str)
        web_from = get_param_by_request(request_method, "web_from", "", str)
        callback = get_param_by_request(request_method, "callback", "", str)
        status = dict(status="success")
        market_from = 'sem'
        # if source != "":
        #     if source.find("ad10086") >= 0:
        #         market_from = '10086'
        #     source = source.split("?")
        #     if len(source) < 2:
        #         source = ""
        #     else:
        #         source = source[1]
        if web_from != "":
            if web_from == "traditional":
                market_from = "trad"
            else:
                market_from = "operate"
                source = web_from
        _interest = re.findall('.*/(.*).html', interest)
        if _interest:
            interest = _interest[0]

        info_dict = dict(name=name, phone=phone, qq=qq, interest=interest, market_from=market_from, source=source,
                         date_publish=datetime.now())
        APIResult = db.api.common.app.app_consult_info_stream_insert(info_dict)
        if APIResult.is_error():

            status.update(dict(status="failure"))
    except Exception as e:

        status.update(dict(status="failure"))
    if callback:
        return HttpResponse('%s(%s)' % (callback, json.dumps(status)))
    return HttpResponse(json.dumps(status), content_type="application/json")

# 关于我们的页面
def aboutus(request):
    return render(request, 'mz_common/about.html', locals())


# 联系我们
def contactus(request):
    return render(request, 'mz_common/contact.html', locals())


# 加入我们
class JoinUs(View):
    template = 'mz_common/join.html'

    def get(self, request):
        departments = MaiziDeparment.objects.all().order_by('id')
        for department in departments:
            depart_desc = RecruitPosition.objects.filter(department=department).order_by('index')
            setattr(department, 'description', depart_desc)
        return render(request, self.template, {'departments': departments})


# 高校专区介绍页
def aca_about(request):
    return render(request, 'mz_common/aca_about.html', locals())


# 新手问答
def novice(request):
    faq = FAQ.objects.all().order_by('index')
    return render(request, 'mz_common/novice.html', {'faq': faq})


# lps演示页面跳转
def lps_demo(request):
    url = '/'
    if request.META.has_key('HTTP_REFERER'):
        url = request.META['HTTP_REFERER']
    is_consult = True
    if request.user.is_authenticated():
        if request.user.is_teacher():
            is_consult = False
        elif ClassStudents.objects.filter(user=request.user).exists():
            is_consult = False
    return render(request, 'mz_common/lps_demo.html', locals())


# 微信分享
def wechat_share(request):
    import random
    import string
    import hashlib

    share_url = request.GET.get('share_url')
    r = requests.get(
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx6c7177b5e7305539&secret=6acbb964533bcf8684c64bcbb1a84db1')
    token = json.loads(r.text)['access_token']
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token
    r2 = requests.get(url=url)
    jsapi_ticket = json.loads(r2.text)['ticket']
    ret = {
        'nonceStr': ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15)),
        'jsapi_ticket': jsapi_ticket,
        'timestamp': int(time.time()),
        'url': share_url
    }
    string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
    signature = hashlib.sha1(string).hexdigest()
    return JsonResponse({'time': ret['timestamp'], "sign": signature, "nonceStr": ret['nonceStr']})


# 文章列表页
@require_GET
def article_list_view(request, article_type):
    """
    @brief 重构之后的文章列表页
    :param request:
    :param article_type:
    :return:
    """
    page_index = safe_int(request.GET.get('page_index', 1), 1)
    page_index = 1 if page_index <= 0 else page_index
    hot_tags = db.api.common.tag.get_tag(is_hot=True).result()
    article_type_list = db.api.article.article.get_all_article_types().result()
    if article_type.lower() not in list(item.get('short_name', 'tech').lower() for item in article_type_list):
        article_type = article_type_list[0].get('short_name', 'tech')  # 如果传入type不在已有的之内,则取第一个或者'tech'
    article_type_obj = db.api.article.article.get_all_article_type_with_short_name(article_type).result()
    article_type_obj = article_type_obj[0] if article_type_obj else None
    articles = db.api.article.article.get_article_with_type(article_type, _enable_cache=True).result()
    for article in articles:  # 将分组聚合的tag信息拆分
        if article['tag']:
            article['tag'] = dict(list(item.split('_') for item in article['tag'].split(','))[:3])
    career_courses = db.api.get_hot_career_course().result()
    ad = db.api.article.article.get_article_list_ad().result()
    ad = ad[0] if ad else ad

    page_size = 10
    rows_count = len(articles)
    page_aroud = 2  # 页数处于中间时,前后分别围绕的页数
    page_count_list, page_index, start_index, end_index = paginater(page_index, page_size, rows_count, page_aroud)
    articles = articles[start_index:end_index]
    for article in articles:  # 转换从cache中取得的日期字符串
        article['publish_date'] = reformat_datetime_from_cache(article['publish_date'])

    url = '%s%s' % (urlresolvers.reverse('article_list_view', kwargs=dict(article_type=article_type)), '?')
    article_data = dict(article_list=articles)
    data = dict(article_type_list=article_type_list, article_data=article_data, hot_tags=hot_tags,
                career_courses=career_courses, ad=ad, article_type_s_name=article_type_obj, url=url,
                page_count_list=page_count_list, page_index=page_index)
    return render(request, 'mz_common/article_list.html', data)


# 文章列表(标签作为筛选条件)
@require_GET
def artilcle_list_tag_view(request, tag_id):
    """

    :param request:
    :param tag_id:
    :return:
    """
    tag_id = safe_int(tag_id)
    page_index = safe_int(request.GET.get('page_index', 1), 1)
    page_index = 1 if page_index <= 0 else page_index
    hot_tags = db.api.common.tag.get_tag(is_hot=True).result()
    all_tags = db.api.common.tag.get_tag().result()
    if tag_id not in list(int(item.get('id', 1010001)) for item in all_tags):  # 如果传入的tag_id不存在,处理
        tag_id = hot_tags[0].get('id', 1010001) if hot_tags else 1010001
    tag = db.api.common.tag.get_tag_by_id(tag_id).result()
    tag = tag[0] if tag else None
    articles = db.api.article.article.get_article_with_tag(tag_id, _enable_cache=True).result()
    for article in articles:  # 将分组聚合的tag信息拆分
        article['tag'] = dict(list(item.split('_') for item in article['tag'].split(','))[:3])
    career_courses = db.api.get_hot_career_course().result()
    ad = db.api.article.article.get_article_list_ad().result()
    ad = ad[0] if ad else ad

    page_size = 10
    rows_count = len(articles)
    page_aroud = 2  # 页数处于中间时,前后分别围绕的页数
    page_count_list, page_index, start_index, end_index = paginater(page_index, page_size, rows_count, page_aroud)
    articles = articles[start_index:end_index]
    for article in articles:  # 转换从cache中取得的日期字符串
        article['publish_date'] = reformat_datetime_from_cache(article['publish_date'])

    article_data = dict(article_list=articles)
    url = '%s%s' % (urlresolvers.reverse('artilcle_list_tag_view', kwargs=dict(tag_id=tag_id)), '?')
    data = dict(hot_tags=hot_tags, article_data=article_data, career_courses=career_courses, ad=ad, url=url,
                page_count_list=page_count_list, page_index=page_index, tag=tag)
    if settings.IS_MOBILE:
        data.update({'page_count': len(page_count_list)})
        data.update({'tag_id': tag_id})
        return render(request, 'mz_wap/article_list.html', data)
    return render(request, 'mz_common/article_list.html', data)


# WAP文章列表(标签作为筛选条件)
def wap_article_tag_page(request):
    page_index = int(request.POST.get('page_index'))
    tag_id = request.POST.get('tag_id')
    html = """
        <li><a href="/article/%s/">
        <p class="img"><img class="ui-imglazyload" alt="%s" src="%s">
        </p>
            <div class="txt">
                <h3>%s</h3>
                <p>%s</p>
                <dl>
                    <dd class="time">%s</dd>
                    %s
                </dl>
            </div>
        </a>
        </li>
        """
    data = ""
    articles = db.api.article.article.get_article_with_tag(tag_id, _enable_cache=True).result()
    page_size = 10
    rows_count = len(articles)
    page_aroud = 2  # 页数处于中间时,前后分别围绕的页数
    page_count_list, page_index, start_index, end_index = paginater(page_index, page_size, rows_count, page_aroud)
    articles = articles[start_index:end_index]
    for article in articles:  # 转换从cache中取得的日期字符串
        article['publish_date'] = datetime_convert(reformat_datetime_from_cache(article['publish_date']))
        article['tag'] = dict(list(item.split('_') for item in article['tag'].split(','))[:2])
        tags = ''
        if article.get('tag'):
            for k, v in article.get('tag').items():
                tags += '<dd class="tag">' + v + '</dd>'
        data += html % (article['id'], article['title'], settings.MEDIA_URL+article['title_image'],
                            article['title'], article['abstract'], article['publish_date'], tags)
    is_next = False
    if len(page_count_list) > int(page_index):
        is_next = True
    return JsonResponse({'data': data, 'is_next': is_next, 'page_index': page_index})


# 文章详情页
@require_GET
def article_detail_view(request, article_id):
    api = article_sys_api.ArticleSysApi().default_instance()
    common_api = common_sys_api.CommonSysApi().default_instance()
    try:
        article = ensure_apiresult_obj(api.get_one_article, id=article_id)
    except AssertionError as e:
        raise Http404()
    article_tags = article.tags[:3] if article.tags else None
    article_type = article.article_type
    hot_tags = article.hot_tags
    career_course = opt_apiresult_obj(
        {}, api.get_related_careercourse, article.id)
    if career_course:
        ad = opt_apiresult_obj(
            {}, common_api.get_career_course_ad, career_course.id, 'ARTICLE')
        recommend_article = opt_apiresult_obj(
            [], api.get_related_articles, career_course.id)
    else:
        ad = {}
        recommend_article = []
    if ad:
        ad['url'] = reverse('course:course_detail',
                            kwargs={'course_id': career_course.short_name})
    try:
        recommend_article.remove(article)
    except ValueError:
        pass
    like_list = opt_apiresult_obj([], common_api.get_article_users_like, article.id)
    is_like = request.user.id in like_list if request.user else False
    # hot_tags = opt_apiresult_obj([], common_api.get_all_article_tags, is_hot=True)
    hot_tags = db.api.common.tag.get_tag(is_hot=True).result()
    # tag_id = article.tags[0].id if article.tags else None

    # 记录view_count
    db.api.article.article.add_count(article_id, 'view_count')
    data = dict(article_type=article_type, article=article,
                recommend_article=recommend_article, hot_tags=hot_tags,
                career_course=career_course, ad=ad,  # tag_id=tag_id,
                is_like=is_like, article_tags=article_tags)
    if settings.IS_MOBILE:
        return render(request, 'mz_wap/article_detail.html', data)
    return render(request, 'mz_common/articleDetail.html', data)


# 添加评论
@ajax_login_required
@require_POST
def add_discuss(request):
    post_data = request.POST.dict()
    user = request.user

    post_data.update(dict(
        user_id=user.id, nick_name=user.nick_name,
        head=user.avatar_middle_thumbnall, create_date=datetime.now()))

    form = DiscussForm(post_data)
    if form.is_valid():
        result = form.save()
        if not result:
            return JsonResponse(dict(success=False,
                                     errors={'sys_error': [u'保存失败']}))
        return JsonResponse(dict(success=True, id=result['id'],
                                 parent_id=result['parent_id']))
    return JsonResponse(dict(success=False, errors=form.errors))


@require_GET
def ajax_get_discuss(request):
    """
    @brief      ajax接口，获取相关文章评论， 相关章节评论

    @return 返回如下格式
        {success:true,
        discuss: [{“id”:”评论ID”,
        "content":"内容",
        "head":"用户头像",
        "date":"几天前",
        ”nick_name”:”用户昵称”,
        “parent_id”:”父评论ID”}]}
    """
    form = GetDiscussForm(request.GET)
    if form.is_valid():
        discuss = form.get_discuss()
    else:
        return JsonResponse(dict(success=False, errors=form.errors))
    discuss = map(lambda x: dict(
        id=x.id,
        user_id=x.user_id,
        content=x.comment,
        head=x.head,
        nick_name=x.nick_name,
        parent_id=x.parent_id,
        date=datetime_convert(x.create_date)),
                  discuss)
    return JsonResponse(dict(success=True, discuss=discuss,
                             discuss_total=len(discuss)))


# 文章点赞
@ajax_login_required
@require_POST
def like_article(request):
    post_data = request.POST.dict()
    post_data.update(dict(user_id=request.user.id))

    form = LikeArticleForm(post_data)
    if form.is_valid():
        result = form.do_like()
    else:
        return JsonResponse(dict(success=False, errors=form.errors))
    if not result:
        return JsonResponse(dict(success=False,
                                 errors={'sys_error': [u'系统错误']}))
    like_num = form.get_like_num()
    return JsonResponse(dict(success=True, like_num=like_num))


# 首页老师包装介绍页
@require_GET
def teacher_introduce(request, teacher_id):
    common_api = common_sys_api.CommonSysApi().default_instance()
    seo = opt_apiresult_obj({}, common_api.get_teacher_seo, int(teacher_id))
    page_map = {684: 'teacher/teacherIntroduceAndroid.html',
                3287: 'teacher/teacherIntroduceUi.html',
                3472: 'teacher/teacherIntroducePython.html',
                4130: 'teacher/teacherIntroduceIos.html',
                #40986: 'teacher/teacherIntroduceIos.html',
                48129: 'teacher/teacherIntroducePhp.html',
                4: 'teacher/teacherIntroduceLinux.html',
                136574: 'teacher/teacherIntroduceQrs.html',
                36413: 'teacher/teacherIntroduceTe.html',
                20365: 'teacher/teacherIntroduceAndroid2.html'}
    return render(request, page_map[int(teacher_id)], dict(seo=seo))


@csrf_exempt
def upload_controller(request):
    result = ""
    action = request.GET.get("action", "")
    # print "action:" + action

    if action == "config":
        result = Uploader.get_config()

    elif action == "uploadimage" \
            or action == "uploadfile" \
            or action == "uploadvideo":
        fil = request.FILES.get("upfile", None)
        upload_result = Uploader.upload(fil, action)
        result = upload_result.info

    return HttpResponse(result, content_type="application/json")


def teacher_recruit(request):
    return render(request, 'teacherRecruit/teacherRecruitList.html')


def teacher_recruit_form(request):
    return render(request, 'teacherRecruit/teacherRecruitForm.html')


def ajax_teacher_recruit_form(request):
    """
    提交老师招聘
    :param request:
    :return:
    """
    from db.api.teacher.employ_teacher import insert_employ_teacher
    from utils.tool import get_param_by_request
    from geetest.views import validate

    if request.method == 'POST':
        # 校验验证码
        try:
            result = validate(request)
        except KeyError:
            return JsonResponse(dict(status=False, msg=u'验证码错误'))
        status = json.loads(result.content)
        if status['status'] == 'fail':
            return JsonResponse(dict(status=False, msg=u'验证码错误'))
        # 获取数据
        teacher_type = get_param_by_request(request.POST, 'lecturerType', _type=int)
        teacher_catagory = get_param_by_request(request.POST, 'formation', _type=int)
        name = get_param_by_request(request.POST, 'teacherRecruitName', _type=str)
        career = get_param_by_request(request.POST, 'teacherRecruitSkill', _type=str)
        work_time = get_param_by_request(request.POST, 'workingLife', _type=int)
        resume = get_param_by_request(request.POST, 'teacherRecruitTextArea', _type=str)
        mobile = get_param_by_request(request.POST, 'teacherRecruitPhone', _type=str)
        qq = get_param_by_request(request.POST, 'teacherRecruitQQ', _type=str)
        valid_msg = ''
        if not teacher_type:
            valid_msg = u'请选择讲师类型'
        if not teacher_catagory:
            valid_msg = u'请选择兼职类型'
        if not name or (name and len(name) > 20):
            valid_msg = u'对不起，真实姓名超出字数限制，请保证在20个字符以内'
        if not career or (career and len(career) > 30):
            valid_msg = u'对不起，技术方向超出字数限制，请保证在30个字符以内'
        if not work_time:
            valid_msg = u'请选择工作年限'
        if not mobile or (mobile and len(mobile) > 11):
            valid_msg = u'对不起，手机超出字数限制，请保证在11个字符'
        if not qq or (qq and len(qq) > 12):
            valid_msg = u'对不起，QQ超出字数限制，请保证在12个字符以内'
        if not resume or (resume and len(resume) > 1000):
            valid_msg = u'对不起，个人简介超出字数限制，请保证在1000个字符以内'
        if valid_msg:
            return JsonResponse(dict(status=False, msg=valid_msg))
        data_dict = dict(teacher_type=teacher_type, teacher_catagory=teacher_catagory,
                         name=name, career=career, work_time=work_time, resume=resume,
                         mobile=mobile, qq=qq)
        try:
            api_result = insert_employ_teacher(data_dict)
        except Exception, e:
            JsonResponse(dict(status=False, msg=str(e)))
        if api_result.is_error():
            JsonResponse(dict(status=False, msg=u'服务器出现了未知错误'))
    return JsonResponse(dict(status=True))
    # return JsonResponse(dict(status=False, msg=u'服务器出现了未知错误'))


@require_POST
def feedback_save(request):
    """
    用户反馈信息保存，要求必须登录才能发布反馈信息
    :param request:
    :return:
    """
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(json.dumps({"status": 'fail', "msg": "未登录"}), content_type="application/json")
    user_id = user.id
    nick_name = user.nick_name
    feedback_type = get_param_by_request(request.POST, "feedback_type", "", _type=str)
    feedback_content = get_param_by_request(request.POST, "feedback_content", "", _type=str)
    contact = get_param_by_request(request.POST, "contact", "", _type=str)
    image_url = get_param_by_request(request.POST, "image_url", "", _type=str)
    current_url = get_param_by_request(request.POST, "current_url", "", _type=str)
    dict_info = dict(content=feedback_content, feed_type=feedback_type, contact=contact, image_url=image_url,
                     user_id=user_id, nick_name=nick_name,current_url=current_url)
    insert_result = db.api.common.feedback.insert_feedback_info(dict_info)
    if insert_result.is_error():
        log.warn("Failed to insert teacher apply info.""dict_info:{0}".format(dict_info))
        return JsonResponse({"status": 'fail'})

    return JsonResponse({"status": 'success'})


def feedback_image_upload(request):
    '''
    用户反馈图片上传接口
    :param request:
    :return:
    '''
    image = request.FILES.get("image")
    image_url = ""
    status = "fail"
    if image:  # 图片上传
        ext = os.path.splitext(image.name)[1]  # 图片格式名
        image_name = str(uuid.uuid1()) + ext
        path = upload_generation_dir("feedback")
        image_path = os.path.join(path, image_name).replace('\\', '/')
        try:
            upload_image = open(image_path, "wb+")
            for chunk in image.chunks():
                upload_image.write(chunk)
            upload_image.close()
        except Exception as e:
            log.warn("upload feedback image failed.execute exception:%s" % e)
        image_url = image_path.split(settings.MEDIA_URL, 1)[1]  # 存入到数据库的字段
        status = "success"
    return HttpResponse(json.dumps({"status": status, "image_url": image_url}), content_type="application/json")
