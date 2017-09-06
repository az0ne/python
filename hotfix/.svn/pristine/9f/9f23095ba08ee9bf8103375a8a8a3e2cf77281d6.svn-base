# -*- coding: utf-8 -*-

import base64, urllib, urllib2, re
import subprocess
import time
import logging
import json, random
import cgi
import operator
import db.api

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.db.models import F
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.http import require_GET

from models import *
from mz_common.function_discuss import get_questons, get_all_questions
from mz_course.functions import get_all_career_courses_info, \
    calc_course_video_length
from mz_pay.models import *
from mz_user.models import *
from mz_lps.models import *
from mz_common.models import *
from mz_common.views import *
from django.db.models.signals import post_save
from django.conf import settings
from django.views.generic.base import View
from mz_user.serializers import UserSerializer
from django.http import Http404
from django.db.models import QuerySet

from aca_course.models import *
from urlparse import urlparse, parse_qs
from django.db.models import Count

from mz_common.functions import checkMobile
from mz_platform.apis import course_sys_api
from mz_platform.apis import common_sys_api
from mz_platform.utils.view_shortcuts import ensure_apiresult_obj
from mz_platform.utils.view_shortcuts import ensure_obj
from mz_platform.utils.view_shortcuts import opt_apiresult_obj

from mz_usercenter.student.interface_record import first_signup_recommend
from utils.logger import logger as log
import db.api.common.new_discuss_post
import db.api.common.seo
import db.api.course.course
import db.api.course.lesson
import db.api.course.career_course
import db.api.common.links
import db.api.article.article
import db.api.wiki.wiki

logger = logging.getLogger('mz_course.views')


#   职业课程（课程）列表视图
def course_list_view(request):
    try:
        current_page = request.GET.get('page', '1')
        template_vars = cache.get('course_list_view_' + current_page)
        if not template_vars:
            career_course_list = CareerCourse.objects.filter(course_scope=None).order_by("index", "-id")
            pn, pt, pl, pp, np, ppn, npn, cp, pr = instance_pager(career_course_list, int(current_page),
                                                                  settings.COURSE_LIST_PAGESIZE)
            # 首页SEO信息读取
            seo = PageSeoSet()
            try:
                seo = PageSeoSet.objects.get(page_name='3')
            except PageSeoSet.DoesNotExist:
                pass

            template_vars = {'seo': seo, 'pl': pl, 'pn': pn, 'pr': pr, 'ppn': ppn, 'npn': npn, 'cp': cp}

            cache.set('course_list_view', template_vars, settings.CACHE_TIME)
    except Exception as e:
        return render(request, 'mz_common/failure.html', {'reason': '该页没有数据'})
    return render(request, 'mz_course/course_list.html', template_vars)


def course_list_view_ajax(request):
    json_str = []
    
    try:
        career_courses_apiresult = db.api.get_career_courses()
        
        if career_courses_apiresult.is_error():
            return HttpResponse(
                json.dumps({'result':'None'}),
                content_type="application/json")
            
        career_course_list = career_courses_apiresult.result()["result"]
        career_course_list = sorted(
            career_course_list, key=lambda x:(x["index"]))
        
        current_page = int(request.GET.get('page', '1'))
        pn,pt,pl,pp,np,ppn,npn,cp,pr = instance_pager(
            career_course_list,current_page,
            settings.COURSE_LIST_PAGESIZE)
    except Exception, e:
        return HttpResponse(json.dumps({'result': 'None'}), content_type="application/json")

    json_str = [{"course_color": p["course_color"], "id": p["id"], "image": str(p["image"]), "name": p["name"].strip(),
                 "student_count": p["student_count"]} for p in pl]

    return HttpResponse(json.dumps(json_str),content_type="application/json")
    
# def course_list_view_ajax(request):
#     json_str = []
#     try:
#         career_course_list = CareerCourse.objects.all().order_by("index", "-id")
#         current_page = int(request.GET.get('page', '1'))
#         pn,pt,pl,pp,np,ppn,npn,cp,pr = instance_pager(career_course_list,current_page, settings.COURSE_LIST_PAGESIZE)
#     except Exception, e:
#         return HttpResponse(json.dumps({'result':'None'}),content_type="application/json")
#     json_str = [{"course_color":p.course_color,"id":p.id,"image":str(p.image),"name":p.name.strip(),"student_count":p.student_count} for p in pl ]
#     return HttpResponse(json.dumps(json_str),content_type="application/json")

#处理老的url
def oldcourse_view(request, course_id, university_id = 0):
    try:
        cur_careercourse = CareerCourse.objects.get(pk=int(course_id))
    except CareerCourse.DoesNotExist:
        raise Http404()
    careercourse_name = cur_careercourse.short_name.lower()
    return HttpResponsePermanentRedirect(reverse('course:course_detail', kwargs={"course_id": careercourse_name}))

#   职业课程详细视图
def course_view(request, course_id, university_id = 0):
    #这段代码 以后要去掉和404页面函数的代码
    android = [4155 ,4121 ,3995 ,3875 ,3221 ,3391 ,3469 ,3300 ,3244 ,318 ,2703 ,1067 ,1056 ,297 ,1010 ,1009 ,1476 ,1417 ,258 ,919 ,876 ,471 ,220 ,833 ,756 ,450 ,175 ,1237 ,1216 ,421 ,1162 ,723 ,1132 ,2539 ,138 ,658 ,627 ,755 ,516 ,494 ,153 ,164 ,108 ,590 ,1097 ,1075 ,628 ,451 ,350]
    ios = [4005,3838,176]
    wp = [3978,3929,3887,3795,470,317,626,296,457,918,256,207,430,724,417,340,106]
    co2d = [2438,2429,2324,2334,722,2388,2406,2473,2450,548,257,2212,2175]
    other = [4009,2494,1293,1695,1629,1542,1541,1540,1868,1866,1830,1696,1364,2558,2607,4105,4089,4071,4009,3856,3617,3816,3491,3225,3420,2663]
    path_url =  request.path
    arr_path =  path_url.split('/')
    list_2 =[i for i in arr_path if i!='' ]
    arr_len =  len(list_2)
    if arr_len == 2:
        CourseType = list_2[0]
        CourseNum = list_2[1]
        cur_careercourse = get_object_or_404(CareerCourse, short_name__iexact=CourseNum)
        # cur_careercourse = CareerCourse.objects.get(short_name__iexact=CourseNum)
        CourseNum = cur_careercourse.id
        if CourseType=="course":
            if int(CourseNum) in android:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/2/")
            elif int(CourseNum) in ios:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/3/")
            elif int(CourseNum) in wp:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/8/")
            elif int(CourseNum) in co2d:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/7/")
            elif int(CourseNum) in other:
                return HttpResponsePermanentRedirect("http://www.maiziedu.com/course/")

    cur_university = None
    course_scope = 0
    cur_careercourse = None
    cur_careercourse_class_list = []
    total_courses = 0
    template_vars = cache.get('course_view_'+str(course_id)+'_'+str(university_id)+'_'+str(request.user.is_authenticated()))
    if not template_vars:
        try:
            if university_id:
                cur_university=AcademicOrg.objects.get(pk=university_id)
                course_scope=1
        except Exception as e:
            logger.error(e)

        # 根据职业课程ID查询对应阶段和课程的详细列表
        try:
            cur_careercourse = CareerCourse.objects.get(short_name__iexact=course_id)
            stages = cur_careercourse.stage_set.order_by("index")

            for stage in stages:
                setattr(stage, "course_list", [])
                stage.name = stage.name.replace(" ","")
                stage.course_list = Course.objects.filter(stages_m = stage, is_active = True).order_by("index", "id")
                total_courses += stage.course_list.count()
                # stage.course_list = stage.course_set.filter(is_active=True).order_by("index", "id")
                for course in stage.course_list:
                    #如果没有播放章节的记录，直接获取该课程下第一个章节进行播放
                    lesson_list = Lesson.objects.filter(course=course.id).order_by("index")
                    lesson_list_len = len(lesson_list)
                    setattr(course, "updated_course",lesson_list_len)
                    if not request.user.is_authenticated():
                        setattr(course, "url", "")
                        if lesson_list_len > 0:
                            lesson_url = "/course/%s/%d-%d"%(stage.career_course.short_name.lower(),course.id,lesson_list[0].id)
                            course.url = lesson_url
                        else:
                            course.url = "/course/"+str(course.id)+"/recent/play/"

            # 获取完成职业课程学习所需天数
            setattr(cur_careercourse, "need_days", 0)
            for stage in stages:
                sum_days = Course.objects.filter(stages_m = stage).extra(select={'sum': 'sum(need_days)'}).values('sum')[0]['sum']
                # sum_days = stage.course_set.extra(select={'sum': 'sum(need_days)'}).values('sum')[0]['sum']
                if sum_days is not None:
                    cur_careercourse.need_days += sum_days
        except Exception as e:
            logger.error(e)

        template_vars = {'course_scope': course_scope, 'cur_university': cur_university, 'cur_careercourse': cur_careercourse,
                         'stages': stages, 'cur_careercourse_class_list': [],'total_courses':total_courses}
        cache.set('course_view_'+str(course_id)+'_'+str(university_id)+'_'+str(request.user.is_authenticated()), template_vars, settings.CACHE_TIME)


    if cur_careercourse is None:
        cur_careercourse = template_vars['cur_careercourse']

    # 根据不同情况获取不同的支付金额
    # zhangyu
    lps_version = None
    if request.user.is_authenticated():
        course_class = Class.objects.xall().filter(career_course=cur_careercourse, students=request.user)
        if course_class.count():
            lps_version = course_class[0].lps_version
    if lps_version:
        cur_careercourse = get_real_amount(request.user, cur_careercourse, lps_version)
    else:
        cur_careercourse = get_real_amount(request.user, cur_careercourse)
    # 获取该职业课程下所有开放的班级
    # cur_careercourse_class_list = cur_careercourse.class_set.xall()\
    #     .filter(career_course__short_name=course_id, is_active=True, status=1, class_type=Class.CLASS_TYPE_NORMAL, is_closed=False)\
    #     .exclude(current_student_count=F('student_limit'))


    # 更新职业课程的点击次数
    cur_careercourse.click_count += 1
    cur_careercourse.save(update_fields=['click_count'])

    template_vars['cur_careercourse'] = cur_careercourse
    template_vars['cur_careercourse_class_list'] = cur_careercourse_class_list
    # 改变base.html样式
    template_vars['is_display'] = True

    # 增加相关文章和友情链接
    # 热门文章
    articles = db.api.article.article.get_career_course_article(cur_careercourse.id)
    if articles.is_error():
        article_data_list = []
    else:
        article_data_list = articles.result()

    # wiki
    wiki = db.api.wiki.wiki.get_home_page_wiki_by_career_id(cur_careercourse.id)
    if wiki.is_error():
        wiki = []
    else:
        wiki = wiki.result()

    if wiki:
        article_data_list.insert(2, wiki)

    template_vars['article_data_list'] = article_data_list[:3]

    template_vars['friend_links'] = db.api.common.links.get_career_course_links(cur_careercourse.id, 'FRIEND').result()
    template_vars['relate_links'] = db.api.common.links.get_career_course_links(cur_careercourse.id, 'RELATION').result()
    return render(request, 'mz_course/course_detail.html', template_vars)

# 根据课程ID查询当前应该播放的章节
def course_recent_play(request, course_id):
    # 更新课程的点击次数
    try:
        course = Course.objects.get(pk=course_id)
        course.click_count += 1
        course.save()
    except Exception, e:
        logger.error(e)

    stage_id = request.GET.get('stageid','')
    #查询当前应该播放的章节(获取最近一次播放的章节)
    if request.user.is_authenticated():
        recent_learned_lesson = get_recent_learned_lesson(request.user, course_id)
        if recent_learned_lesson is not None:
            #跳转到最近播放的章节播放
            return HttpResponsePermanentRedirect(reverse('lesson:lesson_view', kwargs={"lesson_id": recent_learned_lesson.lesson.id})+"?stageid="+str(stage_id))
    #如果没有播放章节的记录，直接获取该课程下第一个章节进行播放
    lesson_list = Lesson.objects.filter(course=course_id).order_by("index")
    if len(lesson_list) == 0:
        return render(request, 'mz_common/failure.html',{'reason':'该课程下还没有章节'})
    return HttpResponsePermanentRedirect(reverse('lesson:lesson_view', kwargs={"lesson_id": lesson_list[0].id})+"?stageid="+str(stage_id))

#处理老的/lesson/33 链接
def oldlesson_view(request,lesson_id):
    cur_lesson = Lesson.objects.get(pk=lesson_id)
    course_id = cur_lesson.course.id
    stage_set = cur_lesson.course.stages_m.all()
    stage_id = request.GET.get('stageid','')

    try:
        if stage_id != '':
            careercourse = Stage.objects.get(id=int(stage_id)).career_course.short_name.lower()
        else:
            careercourse = stage_set[0].career_course.short_name.lower()
    except:
        careercourse = 'others'
    return HttpResponsePermanentRedirect(reverse('course:lesson_view', kwargs={"careercourse":careercourse,"course_id": course_id,"lesson_id":lesson_id}))

#   章节视图
def lesson_view(request, lesson_id, course_id=0, careercourse=''):

    return redirect(reverse('course:lesson_video_view', kwargs={"course_id": course_id, "lesson_id": lesson_id}))
    # cur_lesson = None
    # cur_course = None
    # cur_careercourse = None
    # uncomplete_quiz_list = []  # 获取测验题列表
    # stage_id = request.GET.get('stageid','')
    # cur_careercourse_class_list = [] #该职业课程的班级列表
    # career_ids = [] #获取该章节的职业课程列表
    #
    # try:
    #     cur_lesson = Lesson.objects.get(pk=lesson_id)
    # except Lesson.DoesNotExist:
    #     raise Http404('No Lesson( mz_course.lesson_view ) matches the given query.')
    #     # return render(request, 'mz_common/failure.html', {'reason': '没有该章节'})
    #
    # # 更新播放次数
    # cur_lesson.play_count += 1
    # cur_lesson.save()
    #
    # cur_course = cur_lesson.course
    # # 更新点击次数
    # cur_course.click_count += 1
    # cur_course.save()
    # # if cur_lesson.course.stages is not None:
    # try:
    #     cur_careercourse = CareerCourse.objects.get(short_name__iexact=careercourse)
    #     if stage_id == '':
    #         stage_list = cur_careercourse.stage_set.all()
    #         for stage in cur_course.stages_m.all():
    #             if stage in stage_list:
    #                 stage_id = stage.id
    #                 break
    #
    #     if cur_careercourse.short_name.lower() == 'yuanhua':
    #         has_payed = False
    #         if cur_course.need_pay:
    #             class_students = ClassStudents.objects.filter(user=request.user,student_class__career_course__short_name__icontains='yuanhua')
    #             for class_student in class_students:
    #                 if class_student.deadline is None:
    #                     setattr(cur_careercourse,'has_pay','yes')
    #                     break
    #                 elif class_student.deadline > datetime.now():
    #                     setattr(cur_careercourse,'has_pay','yes')
    #                     break
    #
    # except Exception as e:
    #     pass
    # # 获取章节作业描述需求
    # setattr(cur_lesson, "homework", {"description": "", "upload_file": "", "code_exercise_type": 0})
    # if cur_lesson.have_homework:
    #     try:
    #         homework = Homework.objects.get(relation_id=lesson_id,relation_type = 1,examine_type = 1)
    #         cur_lesson.homework["description"] = homework.description
    #         if request.user.is_authenticated():
    #             homework_record = HomeworkRecord.objects.filter(examine = homework,student= request.user)
    #             #if cur_lesson.code_exercise_type and cur_lesson.code_exercise_type == 1:
    #             if len(homework_record) > 0:
    #                 cur_lesson.homework["upload_file"] = homework_record[0].upload_file
    #             else:
    #                 cur_lesson.homework["upload_file"] = ""
    #         cur_lesson.homework["code_exercise_type"] = cur_lesson.code_exercise_type
    #
    #     except Homework.DoesNotExist:
    #         homework = Homework()
    #         homework.examine_type = 1
    #         homework.relation_type = 1
    #         homework.relation_id = lesson_id
    #         homework.description = settings.DEFAULT_HOMEWORK
    #         homework.save()
    #         cur_lesson.homework["description"] = settings.DEFAULT_HOMEWORK
    #
    # template_vars = cache.get('lesson_view_'+str(lesson_id))
    # if not template_vars:
    #
    #     # 获取career_ids
    #     stage_m_list = cur_lesson.course.stages_m.all()
    #     for stage in stage_m_list:
    #         career_ids.append(str(stage.career_course.id))
    #     career_ids = ','.join(career_ids)
    #
    #     lesson_list = cur_course.lesson_set.order_by("index", "id")
    #
    #     # 去掉当前章节视频URL地址的空格
    #     cur_lesson.video_url = cur_lesson.video_url.strip()
    #
    #     # 课件下载
    #     #课程课件
    #     course_resource_list=list(cur_course.courseresource_set.all())
    #     #章节课件
    #     lesson_resource_list=list(cur_lesson.lessonresource_set.all())
    #
    #     # 视频完成多少提示考试
    #     VIDEO_EXAM_COMPLETE = settings.VIDEO_EXAM_COMPLETE
    #
    #     search_keywords = cur_course.search_keywords.all()
    #     search_keywords_plain = []
    #     for keyword in search_keywords:
    #         search_keywords_plain.append(keyword.name)
    #     search_keywords_string = ','.join(search_keywords_plain)
    #
    #     # bbs_url = settings.BBS_SITE_URL
    #
    #     #拉勾网接口(相关招聘信息读取)
    #     lagou = []
    #     web_url = ""
    #     try:
    #         # 职业课程是否包含相关关键词
    #         if cur_careercourse.name.upper().find("产品".upper()) > -1:
    #             web_url = settings.LAGOU_PRODUCT_MANAGER_API
    #         elif cur_careercourse.name.upper().find("ios".upper()) > -1:
    #             web_url = settings.LAGOU_IOS_API
    #         elif cur_careercourse.name.upper().find("android".upper()) > -1:
    #             web_url = settings.LAGOU_ANDROID_API
    #         elif cur_careercourse.name.upper().find("物联".upper()) > -1:
    #             web_url = settings.LAGOU_JOINT_PAI
    #         elif cur_careercourse.name.upper().find("嵌入式".upper()) > -1:
    #             web_url = settings.LAGOU_EMBEDDED_PAI
    #         elif cur_careercourse.name.upper().find("windowsphone".upper()) > -1:
    #             web_url = settings.LAGOU_WINPHONE_API
    #         elif cur_careercourse.name.upper().find("cocos2d".upper()) > -1:
    #             web_url = settings.LAGOU_COCOS2D_API
    #         elif cur_careercourse.name.upper().find("web".upper()) > -1:
    #             web_url = settings.LAGOU_WEB_API
    #         response = urllib2.urlopen(web_url, timeout=3)
    #         json_read = response.read()
    #         matchObj = re.match('success_jsonpCallback\(([\s\S]+)\)$',json_read)
    #         if matchObj:
    #             lagou_json = matchObj.group(1)
    #             lagou = json.loads(lagou_json)
    #     except Exception as e:
    #         pass
    #
    #     template_vars = {'cur_lesson': cur_lesson, 'cur_course': cur_course, 'cur_careercourse': cur_careercourse,
    #                      'lesson_list':lesson_list, 'search_keywords_string': search_keywords_string, 'lagou': lagou,
    #                      'lesson_resource_list':lesson_resource_list, 'course_resource_list': course_resource_list,
    #                      'VIDEO_EXAM_COMPLETE':VIDEO_EXAM_COMPLETE,
    #                      'cur_careercourse_class_list': [], 'uncomplete_quiz_list': [],
    #                      'stage_id': stage_id, 'career_ids': career_ids,'careercourse':careercourse}
    #
    #     cache.set('lesson_view_'+str(lesson_id), template_vars, settings.CACHE_TIME)
    #
    # template_vars['careercourse'] = careercourse
    # if cur_careercourse is not None:
    #     # 根据不同情况获取不同的支付金额
    #     cur_careercourse = get_real_amount(request.user, cur_careercourse)
    #     # 获取该职业课程下所有开放的班级
    #     cur_careercourse_class_list = cur_careercourse.class_set.filter(is_active=True, status=1)
    #
    # #给course增加收藏信息
    # setattr(cur_course, "is_favorite", False)
    # #检查该用户是否购买了该课程对应的职业课程所属的阶段
    # if request.user.is_authenticated():
    #     user = request.user
    #
    #     # 播放时课程是否加入到用户的课程列表
    #     add_into_mycourse(user, cur_course, cur_careercourse)
    #     # 播放时检查coursescore是否有用户和课程对应的记录
    #     check_course_score(user, cur_course)
    #     # 根据lessonid找到对应的paper
    #     paper = Paper.objects.filter(examine_type=2, relation_type=1, relation_id=lesson_id)
    #     if len(paper) > 0:
    #         # 获取重修次数
    #         rebuild_count = get_rebuild_count(user, cur_course)
    #         uncomplete_quiz_list = get_uncomplete_quiz(user, paper[0], rebuild_count)
    #     #判断用户是否已经解锁过该章节对应的阶段，已经解锁则不需要弹出支付提示框
    #     unlock_count = 0
    #     if cur_careercourse is not None:
    #         stage_id = stage_id if stage_id else '0'
    #         unlock_count = UserUnlockStage.objects.filter(Q(user=user), Q(stage_id = stage_id)).count()
    #         # unlock_count = UserUnlockStage.objects.filter(Q(user=user), Q(stage=cur_course.stages)).count()
    #     if unlock_count > 0:
    #         cur_lesson.is_popup = False
    #
    #     #查询是否收藏该课程
    #     if user.myfavorite.filter(id=cur_course.id).count() > 0:
    #         cur_course.is_favorite = True
    #
    #     # 更新当前观看章节（如果已经有记录只更新观看时间）
    #     user_learning_lesson = UserLearningLesson()
    #     try:
    #         user_learning_lesson = UserLearningLesson.objects.get(user=user, lesson=lesson_id)
    #     except UserLearningLesson.DoesNotExist :
    #         user_learning_lesson.lesson = cur_lesson
    #         user_learning_lesson.user = user
    #     user_learning_lesson.save()
    #
    # # 将一些更新后的参数存入到template_vars
    # template_vars['cur_careercourse'] = cur_careercourse
    # template_vars['cur_course'] = cur_course
    # template_vars['cur_lesson'] = cur_lesson
    # template_vars['uncomplete_quiz_list'] = uncomplete_quiz_list
    # template_vars['cur_careercourse_class_list'] = cur_careercourse_class_list
    # #add by ym
    # if cur_lesson.code_exercise_type:
    #     template_vars['online_code_url'] = settings.ONLINE_CODE_URL[cur_lesson.code_exercise_type]
    #
    # template_vars['stageid'] = stage_id
    # #YS
    #
    # template_vars['score'] = round(cur_course.score_ava,1)
    #
    # my_scores = Course_User_Score.objects.filter(user_id=request.user.id, course_id=cur_course.id)
    # template_vars['my_score'] = my_scores[0].score if my_scores else None
    #
    # #获取当前章节的评论总页数
    # discuzz_provider = getattr(settings, 'DISCUZZ_PROVIDER', 'FPS') #默认使用FPS评论
    # template_vars['discuzz_provider'] = discuzz_provider
    # if discuzz_provider == 'LPS':
    #     discuss_list = cur_lesson.discuss_set.filter(parent_id__isnull=True) #获取到所有父级评论
    #     pageNum=discuss_list.count()
    #     if pageNum%settings.COMMENT_PAGESIZE==0:
    #         com_pn=pageNum/settings.COMMENT_PAGESIZE
    #     else:
    #         com_pn=pageNum/settings.COMMENT_PAGESIZE+1
    #     template_vars["com_pn"]=com_pn
    # template_vars["rec_lesson_list"]=_random_lesson()
    #
    # # 改变base.html样式
    # template_vars['is_display'] = True
    #
    # # 添加乐视、保利威视的播放器支持
    # template = 'mz_course/lesson_view.html'
    # if 'yuntv.letv.com' in cur_lesson.video_url:
    #     video_url = cur_lesson.video_url
    #     url_parser = parse_qs(urlparse(video_url).query)
    #     setattr(cur_lesson,"platform_user_id","")
    #     setattr(cur_lesson,"platform_video_id","")
    #     if "uu" in url_parser:
    #         setattr(cur_lesson,"platform_user_id",url_parser['uu'][0])
    #     if "vu" in url_parser:
    #         setattr(cur_lesson,"platform_video_id",url_parser['vu'][0])
    #     template_vars['cur_lesson'] = cur_lesson
    #     template = 'mz_course/lesson_view_letv.html'
    # elif 'player.polyv.net' in cur_lesson.video_url:
    #     template = 'mz_course/lesson_view_polyv.html'
    # #相关文章
    # # relate_article_lst = cache.get('relate_article_'+str(course_id))
    # # if not relate_article_lst:
    # #     relate_article_lst=[]
    #     # try:
    #     #     import requests
    #     #     r = requests.get(url=settings.FPS_HOST+'service/article/relate_article/', data={'course_id': course_id}, timeout=5)
    #     #     if r.status_code == 200:
    #     #         ret = json.loads(r.text)
    #     #         if ret['status'] == True:
    #     #             relate_article_lst=ret['data']
    #     # except Exception,e:
    #     #     logger.error(e)
    #     # cache.set('relate_article_'+str(course_id), relate_article_lst, 3600*24)
    #
    # template_vars['relate_article_url'] = settings.FPS_HOST+'service/article/relate_article/?course_id=%s'%course_id
    #
    # if checkMobile(request):
    #     return render(request, 'mz_course/lesson_view_iphone.html', template_vars)
    # else:
    #     return render(request, template, template_vars)

def _random_lesson():
    rec_lesson_list=[]
    lesson_id_list=Lesson.objects.values_list("id",flat=True)
    id_list=random.sample(lesson_id_list,10)
    for id in id_list:
        try:
            lesson=Lesson.objects.get(pk=id)
            course=lesson.course
            course_id=course.id
            careercourse = course.stages_m.all()[0].career_course.short_name.lower()
            url=reverse('course:lesson_view', kwargs={"careercourse":careercourse,"course_id": course_id,"lesson_id":id})
            course_image=course.image
            course_name=course.name
            lesson_name=lesson.name
            rec_lesson_list.append({'url':url,'image':course_image,'course_name':course_name,'lesson_name':lesson_name})
        except Exception as e:
            logger.info('%s:Course:%s' % (e, lesson.course))
        if len(rec_lesson_list)>=3:
            break
    return rec_lesson_list

# 在线编程(yuan)
class Response:
    message = "数据加载失败"
    success = False
    data = {}

    @staticmethod
    def dumps():
        return json.dumps({
            "message": Response.message,
            "success": Response.success,
            "data": Response.data
        })

def response_init(func):
    def _init(request):
        Response.message = "数据加载失败"
        Response.success = False
        Response.data = {}
        return func(request)
    return _init

@csrf_exempt
@response_init
def save_code_result(request):
    if request.method == 'POST':
        try:
            cmdContext = request.POST['code']
            cmdOutput = request.POST['output']
            lesson_id = request.POST['lesson_id']
            course_id = request.POST['course_id']

            cur_lesson = Lesson.objects.get(pk=lesson_id)
            if cur_lesson.have_homework:
                #if request.user.is_authenticated():
                try:
                    homework = Homework.objects.get(relation_id=lesson_id,relation_type=1, examine_type=1)
                    homework_records = HomeworkRecord.objects.filter(examine=homework, student=request.user)
                    if len(homework_records)>0:
                        homework_record = homework_records[0]
                    else:
                        homework_record = HomeworkRecord()
                        homework_record.student = request.user
                        homework_record.examine_id = homework.id
                        homework_record.homework = homework
                        homework_record.save()

                except Exception as e:
                    logger.error(e)
                homework_record.result = cmdContext + '\n' + cmdOutput
                try:
                    homework_record.save()
                except Exception as e:
                    logger.error(e)

            Response.data = {
                "cmdOutput": cmdOutput
            }
            Response.message = "ok"
            Response.success = True
        except Exception as e:
            logger.error(e)
        return HttpResponse(Response.dumps(), content_type="application/json")


#需要禁止执行的代码
Illegal_input = ['.system(', '.pipe(', 'popen', 'win32api', '.spawn', 'commands.', 'subprocess', 'open(', 'file(']

@csrf_exempt
@response_init
def get_code_result(request):
    if request.method == 'GET':
        try:
            cmdContext = request.GET['code']
            lesson_id = request.GET['lesson_id']
            course_id = request.GET['course_id']
            user_id= request.GET['user_id']
            # cmdContext = request.POST['code']
            # lesson_id = request.POST['lesson_id']
            # course_id = request.POST['course_id']
            if [cmd for cmd in Illegal_input if cmd in cmdContext]:
                cmdOutput = 'Illegal Input'
            else:
                filehandle = open('uploads/cmd_source/command.py', 'w')
                filehandle.write(cmdContext)
                filehandle.close()
                p = subprocess.Popen(['python', "uploads/cmd_source/command.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
                time.sleep(1)
                p.kill()
                cmdOutput = p.communicate()[0]
            #判断是否成功运行
                if ('Traceback' in cmdOutput) and ('Error' in cmdOutput):
                    try:
                        Response.data = {
                            "cmdOutput": cmdOutput
                        }
                        Response.message = "wrong"
                        Response.success = True
                    except Exception as e:
                        logger.error(e)
                    return HttpResponse(Response.dumps(), content_type="application/json")
                #保存结果
                else:
                    cur_lesson = Lesson.objects.get(pk=lesson_id)
                    if cur_lesson.have_homework:
                        #if request.user.is_authenticated():
                        try:
                            homework = Homework.objects.get(relation_id=lesson_id,relation_type=1, examine_type=1)
                            homework_records = HomeworkRecord.objects.filter(examine=homework, student=user_id) #request.user)
                            if len(homework_records)>0:
                                homework_record = homework_records[0]
                            else:
                                homework_record = HomeworkRecord()
                                homework_record.student = UserProfile.objects.get(pk=user_id) # request.user
                                homework_record.examine_id = homework.id
                                homework_record.homework = homework
                                homework_record.save()

                        except Exception as e:
                            logger.error(e)
                        homework_record.result = cmdContext + '\n' + cmdOutput
                        try:
                            homework_record.save()
                        except Exception as e:
                            logger.error(e)
        except Exception as e:
            logger.error(e)
        try:
            Response.data = {
                "cmdOutput": cmdOutput
            }
            Response.message = "ok"
            Response.success = True
        except Exception as e:
            logger.error(e)
        return HttpResponse(Response.dumps(), content_type="application/json")


def update_favorite(request, course_id):
    if request.user.is_authenticated():
        favorite = MyFavorite()
        course = Course()
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            result = '{"status":"failure","message":"不存在该课程"}'
        try:
            favorite = MyFavorite.objects.get(user=request.user, course=course_id)
            favorite.delete()
            # 收藏数减1
            course.favorite_count -= 1
            course.save()
            result = '{"status":"success","message":"取消收藏成功"}'
        except MyFavorite.DoesNotExist :
            favorite.user = request.user
            favorite.course_id = course_id
            favorite.save()
            # 收藏数加1
            course.favorite_count += 1
            course.save()
            result = '{"status":"success","message":"收藏成功"}'
        except Exception as e:
            logger.error(e)
    else:
        result = '{"status":"failure","message":"请登录之后再收藏"}'
    return HttpResponse(result, content_type="application/json")


#评论函数
@csrf_exempt
def add_comment(request):
    if request.POST['comment']=="":
        message = '{"message":"评论不能为空"}'
        return HttpResponse(message,content_type="application/json")
    comment = request.POST['comment']
    parent_id = request.POST['parent_id'] or None
    lesson_id = request.POST['lesson_id']
    child_uid = request.POST['child_uid'] or None
    # stage_id = request.POST['stage_id'] or None

    user = request.user
    dis = Discuss()
    dis.content = comment
    dis.parent_id = parent_id
    dis.lesson_id = lesson_id
    dis.user = user.id
    pid = dis.save()
    new_id = Discuss.objects.order_by('-id')[0]
    if child_uid is not None and int(user.id) != int(child_uid):
        sys_send_message(user.id,child_uid,2,comment,lesson_id) #添加消息函数

        # app推送
        try:
            child_user = UserProfile.objects.get(pk=child_uid)
            lesson = Lesson.objects.get(pk=lesson_id)
            #app_send_message("系统消息", str(user.nick_name) + "在课程" + str(lesson.name) + "中回复了你", [child_user.username])
            # app_send_message_token("系统消息", str(user.nick_name) + "在课程" + str(lesson.name) + "中回复了你", [child_user.token])
        except Exception as e:
            logger.error(e)

    # 如果子回复为None则表示给录课老师的留言
    if child_uid is None:
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
            # 录课老师对象
            teacher = lesson.course.teacher
            sys_send_message(user.id,teacher.id,2,comment,lesson_id) #添加消息函数
            app_send_message("系统消息", str(user.nick_name) + "在课程" + str(lesson.name) + "中回复了你", [teacher.token])
            # 带课老师对象
            ts = []
            for stage in lesson.course.stages_m.all():
                # ts = ts + Class.objects.filter(career_course=stage.career_course).values("teacher")
                ts = ts + [teacher_values['teachers'] for teacher_values in Class.objects.filter(career_course=stage.career_course).values("teachers")]

            teachers = UserProfile.objects.filter(
                id__in = list(set(ts)))
                #id__in=ts.distinct())
                # id__in=Class.objects.filter(career_course=lesson.course.stages.career_course).values("teacher").distinct())
            for class_teacher in teachers:
                if teacher.id != class_teacher.id:
                    sys_send_message(user.id,class_teacher.id,2,comment,lesson_id) #添加消息函数
                    app_send_message("系统消息", str(user.nick_name) + "在课程" + str(lesson.name) + "中回复了你", [class_teacher.token])
        except Exception as e:
            logger.error(e)
    # zhangyu
    comment = str(cgi.escape(comment)).replace('\"', '\'')
    comment = comment.replace('\n', ' ')
    #获取当前章节的评论总页数 guotao
    pageNum = Discuss.objects.filter(parent_id__isnull=True,lesson_id=lesson_id).count() #获取到所有父级评论
    if pageNum%settings.COMMENT_PAGESIZE==0:
        com_pn=pageNum/settings.COMMENT_PAGESIZE
    else:
        com_pn=pageNum/settings.COMMENT_PAGESIZE+1
    message = '{"message":"success","parent_id":"'+str(new_id.id)+'","comment":"'+comment+'","com_pn":"'+str(com_pn)+'"}'
    return HttpResponse(message,content_type="application/json")

#作业提交
@csrf_exempt
def job_upload(request):
    ret="0"
    files = request.FILES.get("Filedata",None)
    lesson_id = request.POST['lesson_id']
    if files:
        result =file_upload(files, 'homework')
        if result[0] == True:
            ret='{"status":"success","message":"'+str(result[1])+'"}'
            try:
                examine = Homework.objects.get(Q(relation_type=1), Q(relation_id=lesson_id),Q(examine_type = 1))
                workobj = HomeworkRecord.objects.filter(examine_id = examine.id,student_id= request.user.id)
                if workobj:
                    project_record_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(workobj[0].upload_file)
                    if os.path.exists(project_record_path) : #如果存在就移除
                        os.remove(project_record_path)
                    # 如果已经上传，就执行更新操作
                    HomeworkRecord.objects.filter(examine_id=examine.id,student_id=request.user.id).update(upload_file=result[2])
                else:
                    work = HomeworkRecord()
                    work.upload_file = result[2]
                    work.student = request.user
                    work.examine_id = examine.id
                    work.homework = examine
                    work.save()
                    # 首次上传时加上1学力
                    update_study_point_score(request.user, 1, examine=examine, examine_record=work, rebuild_count=0, update_type=2)
            except Homework.DoesNotExist:
                ret='{"status":"failure","message":"保存失败"}'
                return HttpResponse(ret, content_type="text/plain")
            except Exception as e:
                logger.error(e)
        else:
            ret='{"status":"failure","message":"'+str(result[1])+'"}'
    return HttpResponse(ret, content_type="text/plain")

# #判断是否上传
# def is_up(exaid,user_id):
#     workobj = HomeworkRecord.objects.filter(examine_id = exaid,student_id= user_id)
#     if workobj.exists():
#         return True
#     else:
#         return False

# #模板判断是否上传,传值到模板
# def template_is_up(request,lesson_id):
#     bools = 0
#     try:
#         examine = Homework.objects.get(Q(relation_type=1), Q(relation_id=lesson_id))
#         if is_up(examine.id):
#             bools = 1
#         else:
#             bools = 0
#     except:
#         return HttpResponse(bools)
#     return HttpResponse(bools)

# 课程（隐藏）额外购买渠道
# def course_pay_other(request, careercourse_id):
#
#     if not request.user.is_authenticated():
#         return render(request, 'mz_common/failure.html',{'reason': '请先回首页登录后再访问该页面'})
#
#     cur_careercourse = None    # 职业课程
#     cur_careercourse_stage_list = []    # 职业课程下所属阶段
#     user_careercourse_unlockstage_list = []    # 用户职业课程中已经解锁的阶段
#
#     # 获取职业课程下所有的阶段
#     try:
#         cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
#     except CareerCourse.DoesNotExist:
#         return render(request, 'mz_common/failure.html',{'reason':'没有该职业课程'})
#     cur_careercourse_stage_list_temp = cur_careercourse.stage_set.all().order_by("index", "id")
#     user_careercourse_unlockstage_list = UserUnlockStage.objects.filter(user=request.user, stage__career_course=careercourse_id)
#     for stage in cur_careercourse_stage_list_temp:
#         # 给stage增加一个标记，标记该阶段是否已经解锁
#         setattr(stage, "is_unlock", False)
#         for unlockstage in user_careercourse_unlockstage_list:
#             if stage.id == unlockstage.stage.id:
#                 stage.is_unlock = True
#                 break
#         cur_careercourse_stage_list.append(stage)
#
#     # 如果已经购买过该职业课程的阶段，则获取之前购买选择的班级
#     cur_careercourse_class_list=[]
#     setattr(cur_careercourse, "careercourse_class", None)
#     if len(user_careercourse_unlockstage_list) != 0:
#         cur_careercourse.careercourse_class = get_careercourse_class(request.user, cur_careercourse)
#     else:
#         # 获取该职业课程下所有开放的班级
#         cur_careercourse_class_list = cur_careercourse.class_set.filter(is_active=True, status=1)
#
#     return render(request, 'mz_course/careercourse_pay_other.html', locals())

# 更新章节完成状态
def update_learning_lesson(request, lesson_id):
    try:
        if request.user.is_authenticated() and request.user.is_unlockstage():
            learning_lesson = UserLearningLesson.objects.get(user=request.user, lesson=lesson_id)
            if not learning_lesson.is_complete:
                learning_lesson.is_complete = True
                learning_lesson.save()

                # 更新学力
                update_study_point_score(student=request.user, study_point=1, course=learning_lesson.lesson.course, rebuild_count=0, lesson_id = lesson_id, update_type=1)
    except Exception, e:
        logger.error(e)
        return HttpResponse({"status": "failure"}, content_type="application/json")
    return HttpResponse({"status": "success"}, content_type="application/json")


# 获取职业课程价格
# def get_careercourse_total_price(careercourse, class_lps_version=None):
#     price = 0
#     stages = careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version)
#     if stages.count() > 0:
#         price = stages.extra(select={'sum': 'sum(price)'}).values('sum')[0]['sum'] * careercourse.discount
#         if price is None:price = 0
#     return int(price)

# 获取职业课程列表所有阶段ID列表
def get_careercourse_allstage_list(careercourse, class_lps_version=None):
    return careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version).order_by("index", "id").values_list("id")

# 获取职业课程首付金额
# def get_careercourse_first_payment(careercourse, class_lps_version=None):
#     price = careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version).filter(is_try=True).extra(select={'sum': 'sum(price)'}).values('sum')[0]['sum']
#     if price == None:price =0
#     return int(price)

# 获取试学阶段ID列表
def get_careercourse_trystage_list(careercourse, class_lps_version=None):
    return careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version).filter(is_try=True).order_by("index","id").values_list("id")

# 获取还未支付阶段的余款 by 订单管理 郭涛
def get_careercourse_balance_payment(user, careercourse, class_lps_version=None):
    price = None
    #查询首付款订单中的应付款（余款）
    user_purs=UserPurchase.objects.filter(user=user, pay_careercourse=careercourse, pay_status=1, pay_type__in=[1, 7]).order_by("-id")
    if user_purs.count() > 0:
        price = user_purs[0].final_payment_price
    #如果没有首付款则不能支付余款
    if price == None:price = 0
    discount_price = get_final_payment_discount(user, careercourse)
    if discount_price[0]:
        price = discount_price[1]
    return int(price)


# 获取之前打折过后的余款价格
def get_final_payment_discount(user, careercourse):
    class_code = get_careercourse_class(user, careercourse)
    if not class_code:
        return False, ''
    try:
        kalss = ClassStudents.objects.get(user=user, student_class__coding=class_code)
        join_time = kalss.created
        if join_time:
            if join_time > datetime(2016, 4, 1):
                return False, ''
    except ClassStudents.DoesNotExist:
        return False, ''

    if user.email == '18530975@qq.com':
        if careercourse.short_name == 'php':
            return True, 5942
        if careercourse.short_name == 'ios':
            return True, 6792
    from discount_students import student_dict

    discount_price = student_dict.get(user.mobile) or student_dict.get(user.email)
    if discount_price:
        return True, int(discount_price)
    return False, ''


# 获取还未支付加锁的阶段ID列表
def get_careercourse_lockstage_list(user, careercourse, class_lps_version=None):
    user_careercourse_unlockstage_list = UserUnlockStage.objects.filter(user=user, stage__career_course=careercourse, stage__lps_version=class_lps_version).values_list("stage")
    return careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version).filter(~Q(id__in=user_careercourse_unlockstage_list)).values_list("id")

# 根据阶段解锁状态来判断课程购买按钮的状态(0显示全款支付和试学首付,1显示尾款支付按钮，2显示已经购买)
def get_careercourse_buybtn_status(user, careercourse, class_lps_version=None):
    careercourse_stage_count = careercourse.stage_set.xall().filter(career_course=careercourse, lps_version=class_lps_version).extra(select={'count': 'count(name)'}).values('count')[0]['count']
    user_careercourse_unlockstage_count = UserUnlockStage.objects.filter(user=user, stage__career_course=careercourse, stage__lps_version=class_lps_version).count()

    # 判断是否加入体验班
    if Class.objects.filter(students=user, career_course=careercourse, class_type=Class.CLASS_TYPE_EXPERIENCE).exists():
        user_careercourse_unlockstage_count = 0

    if user_careercourse_unlockstage_count == 0:
        return 0
    elif careercourse_stage_count > user_careercourse_unlockstage_count:
        return 1
    else:
        return 2

# 根据用户和职业课程找到用户在职业课程中所属班级编号，
def get_careercourse_class(user, careercourse):
    try:
        userclass = Class.objects.xall().get(students=user, career_course=careercourse, class_type=Class.CLASS_TYPE_NORMAL)
        return userclass.coding
    except Class.DoesNotExist :
        return None

# 根据用户、职业课程来判断目标支付阶段列表中是否有已经解锁的阶段
def is_unlock_in_stagelist(user, target_stage_list) :
    if UserUnlockStage.objects.filter(user=user, stage__in=target_stage_list).count() > 0 :
        return True
    return False

# 判断不同情况下支付的实际金额 by 订单管理 郭涛
def get_real_amount(user, careercourse, lps_version=None):
    # 根据课程阶段价格计算课程总价
    setattr(careercourse, "total_price", careercourse.net_price)
    # 获取首付款价格
    setattr(careercourse, "first_payment", careercourse.try_price)
    # 获取首付试学的阶段列表
    # setattr(careercourse, "trystage_list", get_careercourse_trystage_list(careercourse, lps_version))
    if user.is_authenticated():
        # 课程购买按钮的状态
        setattr(careercourse, "buybtn_status", get_careercourse_buybtn_status(user, careercourse, lps_version))
        if careercourse.buybtn_status == 1:
            #计算尾款应支付金额
            setattr(careercourse, "balance_payment", get_careercourse_balance_payment(user, careercourse, lps_version))
            #用户当前所属该职业课程下的某个班级
            setattr(careercourse, "careercourse_class", get_careercourse_class(user, careercourse))
    return careercourse

# 播放时课程是否加入到用户的课程列表
def add_into_mycourse(user, cur_course, cur_careercourse):
    # 判断该课程是否属于某个职业课程
    if user.is_student():
        # if cur_course.stages == None:  #不属于某个职业课程
        #     # 判断该课程是否已经在该用户的课程列表
        #     if MyCourse.objects.filter(user=user, course=cur_course.id, course_type=1).count() == 0 :
        #         my_course = MyCourse()
        #         my_course.user = user
        #         my_course.course = cur_course.id
        #         my_course.course_type = 1
        #         my_course.save()
        #         #更新相应小课程的学习人数
        #         cur_course.student_count += 1
        #         cur_course.save()
        # else:  #属于某个职业课程
        if cur_careercourse is not None:
            if MyCourse.objects.filter(user=user, course=cur_careercourse.id, course_type=2).count() == 0 :
                my_course = MyCourse()
                my_course.user = user
                my_course.course = cur_careercourse.id
                my_course.course_type = 2
                my_course.save()
                #更新职业课程的学习人数
                cur_careercourse.student_count += 1
                cur_careercourse.save()
                #更新相应小课程的学习人数
        if cur_course is not None:
            if not MyCourse.objects.filter(user=user, course=cur_course.id, course_type=1).exists():
                my_course = MyCourse()
                my_course.user = user
                my_course.course = cur_course.id
                my_course.course_type = 1
                my_course.save()
                cur_course.student_count += 1
                cur_course.save()


# 得到用户最近观看的章节
def get_recent_learned_lesson(user, course):
    recent_learned_lesson = UserLearningLesson.objects.filter(user=user,lesson__course=course).order_by("-date_learning")
    if recent_learned_lesson:
        return recent_learned_lesson[0]
    return None

# ajax分页评论函数
def lesson_comment(request):
    lesson_id = request.GET.get('lessonid')
    page = request.GET.get('page','1')
    child_comment=[]
    cur_lesson = None
    try:
        cur_lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该章节'})
    # if cur_lesson.course.stages != None:
    discuss_list = cur_lesson.discuss_set.filter(parent_id__isnull=True).order_by("-date_publish") #获取到所有父级评论
    try:
        com_pn,com_pt,discuss_list,com_pp,com_np,com_ppn,com_npn,com_cp,pr = instance_pager(discuss_list,int(page),settings.COMMENT_PAGESIZE)
        for c in discuss_list:
            child = cur_lesson.discuss_set.filter(parent_id = c.id)
            child_comment.append(child)
        fefe=checkMobile(request)
        if fefe:
            return render(request,'mz_course/lesson_view_comm_iphone.html', locals())
        else:
            return render(request,'mz_course/lesson_view_comm_foreach.html', locals())
    except Exception,e:
        ret = ""
        return HttpResponse(ret)


#老师（他的课程）
def has_course(request,has_id):
    page = request.GET.get('page', '1')
    template_vars = cache.get('has_course_'+str(has_id)+'_'+str(page))
    if not template_vars:
        hascourese = Course.objects.filter(teacher_id = has_id)
        pn,pt,courses,pp,np,ppn,npn,cp,pr = instance_pager(hascourese,int(page),settings.GLOBAL_PAGESIZE)
        try:
            has = UserProfile.objects.get(pk =has_id )
        except Exception as e:
            pass

        template_vars = {'has': has, 'courses': courses, 'pn': pn, 'pr': pr, 'ppn': ppn, 'npn': npn, 'cp': cp}

        cache.set('has_course_'+str(has_id)+'_'+str(page), template_vars, settings.CACHE_TIME)

    return render(request, 'mz_course/user_has_course.html', template_vars)

#评分成功后重新计算分数
def _recalculate_score(**kwargs):
    posted_score = kwargs['instance'].score#传过来的分数
    target_course = kwargs['instance'].course#目标课程
    original_score = Course.objects.get(id=target_course.id).score_ava#当前平均分
    curscore_num = Course_User_Score.objects.filter(course_id=target_course.id).count()-1#当前评价人数
    new_score = ((curscore_num * original_score) + posted_score) / (curscore_num + 1)
    target_course.score_ava = new_score
    target_course.save()

post_save.connect(_recalculate_score,sender=Course_User_Score)

#YS:课程评分,POST请求
@ensure_csrf_cookie
def score(request):
    score = float(request.POST.get(u'score'))
    course_id = int(request.POST.get(u'course_id'))
    user_id = int(request.POST.get(u'user_id'))
    #构造新的分数记录
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponse('{"is_succeed":0}',content_type="application/json")

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return HttpResponse('{"is_succeed":0}',content_type="application/json")

    try:
        new_record = Course_User_Score.objects.get(course__id=course_id,user__id=user_id)
    except Course_User_Score.DoesNotExist:
        new_record = Course_User_Score()

    new_record.score = score
    new_record.course = course
    new_record.user = user
    new_record.save()

    return HttpResponse('{"is_succeed":1,"score":%s}' %round(float(new_record.course.score_ava),1), content_type="application/json")


# 职业课程列表页
class CareerCourseListView(View):
    template = "mz_course/career_course_list_new.html"

    def get(self, request):
        # 手机浏览老的职业课程列表
        if checkMobile(request):
            self.template = "mz_course/career_course_list.html"
            template_vars = cache.get('career_course_list')
            if not template_vars:
                seo = PageSeoSet()
                try:
                    seo = PageSeoSet.objects.get(page_name='3')
                except PageSeoSet.DoesNotExist:
                    pass

                career_courses = CareerCourse.objects.filter(course_scope=None).order_by("-status")
                for career_course in career_courses:
                    stages = career_course.stage_set.order_by("index")
                    total_days = 0
                    total_courses = 0
                    for stage in stages:
                        total_courses += Course.objects.filter(stages_m = stage,is_active=True).count()
                        sum_days = Course.objects.filter(stages_m = stage).extra(select={'sum': 'sum(need_days)'}).values('sum')[0]['sum']
                        if sum_days is not None:
                            total_days += sum_days
                    total_days = int(total_days)
                    setattr(career_course, 'total_days', total_days)
                    setattr(career_course, 'total_courses', total_courses)

                template_vars = {'career_courses':career_courses,'seo':seo, 'is_display': True}

                cache.set('career_course_list', template_vars, settings.CACHE_TIME)

            return render(request, self.template, template_vars)
        # 新企业直通班列表页
        else:
            # if request.user.is_anonymous():
            #     html = cache.get('career_course_list_new_html')
            #     if html:
            #         return HttpResponse(html)

            # is_consult = True
            recommend_careers = None
            if request.user.is_authenticated():
                # 新注册用户推荐课程弹窗
                recommend_careers = first_signup_recommend(request.user)

                # if request.user.is_teacher():
                #     is_consult = False
                # elif ClassStudents.objects.filter(user=request.user).exists():
                #     is_consult = False

            # student_star_list = self._get_student_star()
            # big_career_course_list, small_career_course_list, career_course_list = self._get_career_course()
            # faqs = FAQ.objects.filter(type=1).order_by('index')[:4]
            # display_xinchun = not (request.user and request.user.is_authenticated()\
            #                            and request.user.is_teacher()) and datetime.now()<datetime(2016,3,1)
            #
            # software_development, intelligent_hardware, design, product_operation = get_all_career_courses_info()

            seo = PageSeoSet()
            try:
                seo = PageSeoSet.objects.get(page_name='6')
            except PageSeoSet.DoesNotExist:
                pass

            # career_course_list_temp = career_course_list
            # career_course_list = []
            # for career_course in career_course_list_temp:
            #     classes = Class.objects.xall().filter(career_course_id=career_course.id)
            #     for cls in classes:
            #         if ((cls.current_student_count < cls.student_limit) and \
            #             (cls.is_active == True) and \
            #             (cls.is_closed == False) and \
            #             (cls.status == 1)):
            #             career_course_list.append(career_course)
            #             break

            # template_vars = {
                             # 'student_star_list': student_star_list, 'big_career_course_list': big_career_course_list,
                             # 'small_career_course_list': small_career_course_list, 'faqs': faqs,
                             # 'is_display': True, 'display_xinchun': display_xinchun, 'is_consult': is_consult,
                             # 'career_course_list': career_course_list,
                             # 'software_development': software_development,
                             # 'intelligent_hardware': intelligent_hardware,
                             # 'design': design,
                             # 'product_operation': product_operation,
                             # 'seo': seo, 'recommend_careers': recommend_careers}

            # c = RequestContext(request, template_vars)
            # t = get_template('mz_course/career_course_list_new.html')
            # html = t.render(c)
            # # 游客保存缓存
            # if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
            #     cache.set('career_course_list_new_html', html, 60*60)

            return render(request, 'mz_course/career_course_list_new.html', {'seo': seo,
                                                                             'recommend_careers': recommend_careers})

    def _set_coursecount_coursestudyday(self, career_course):
        '''
        get carreer course stage count
        '''
        stages = career_course.stage_set.order_by("index")
        total_days = 0
        total_courses = 0
        for stage in stages:
            total_courses += Course.objects.filter(stages_m = stage,is_active=True).count()
            sum_days = Course.objects.filter(stages_m=stage).extra(select={'sum': 'sum(need_days)'}).values('sum')[0]['sum']
            if sum_days is not None:
                total_days += sum_days
        total_days = int(total_days)
        setattr(career_course, 'total_days', total_days)
        setattr(career_course, 'total_courses', total_courses)

    def _get_student_star(self):
        '''
        qxoo
        获取明星学员
        '''
        try:
            student_star_list = StarStory.objects.all().order_by('-date_add')[:4]
        except Exception as e:
            logger.error('%s _get_student_star' % e)
            return []
        return student_star_list

    def _get_career_course(self):
        '''
        qxoo
        获取职业课程
        '''
        big_career_course_list = []
        small_career_course_list = []
        career_course_list = []
        try:
            # 开班数量倒序获取热门直通班
            big_career_course_list = CareerCourse.objects.filter(is_hot=True, course_scope=None).annotate(
                class_count=Count('class')).order_by('-class_count')
            # 开班数量倒序获取直通班
            small_career_course_list = CareerCourse.objects.filter(is_hot=False, course_scope=None).annotate(
                class_count=Count('class')).order_by('-class_count')

            career_course_list = CareerCourse.objects.filter(course_scope=None).annotate(
                class_count=Count('class')).exclude(class_count=0).order_by('-class_count')

            # 获取职业课程教师，最多获取六个教师
            for career_course in big_career_course_list:
                teacher_list = list(set(career_course.class_set.filter(status=1, is_closed=False).order_by('id').values_list('teachers__id', flat=True)))
                teacher_list = UserProfile.objects.filter(id__in=teacher_list).values('id', 'avatar_small_thumbnall')
                if teacher_list:
                    teacher_list = teacher_list[0:5 if len(teacher_list) > 5 else len(teacher_list)]
                setattr(career_course, 'teacher_list', teacher_list)
                self._set_coursecount_coursestudyday(career_course)
            #
            for career_course in small_career_course_list:
                self._set_coursecount_coursestudyday(career_course)

            for career_course in career_course_list:
                self._set_coursecount_coursestudyday(career_course)

        except Exception as e:
            logger.error('%s _get_career_course' % e)
            
        return big_career_course_list, small_career_course_list, career_course_list


def get_student_dynamic(request):
    dynamics = ClassStudentDynamic.objects.all().order_by('-date_add')[:50]
    dynamics = [dynamic for dynamic in dynamics if dynamic.obj]
    for dynamic in dynamics:
        obj = dynamic.obj
        if dynamic.type == 1:
            href = "/course/%s-px/" % obj.career_course.short_name
            content = '报名了直通班课程：<a class="color5e" href="%s" target="_blank">%s</a> 班级：%s' % (href, obj.career_course.name, obj.coding)
            setattr(dynamic, 'content', content)

        elif dynamic.type == 2:
            content = '本周学习任务已经完成了100%啦！'
            setattr(dynamic, 'content', content)

        elif dynamic.type in [3, 5, 6]:
            stage_set = obj.stages_m.all()
            try:
                careercourse = stage_set[0].career_course.short_name.lower()
            except:
                careercourse = 'others'
            try:
                lesson_id = Lesson.objects.filter(course=obj.id).order_by("index", "id")[0].id
            except:
                lesson_id = ''
            href = "/course/%s/%d-%d" % (careercourse, obj.id, lesson_id)
            if dynamic.type == 3:
                content = '的课程作业：<a class="color5e" href="%s" target="_blank">《%s》</a> 被老师批改啦！' % (href,obj.name)
            elif dynamic.type == 5:
                content = '提交了课程：<a class="color5e" href="%s" target="_blank">《%s》</a> 的项目实战作业！' % (href,obj.name)
            else:
                content = '在课程 <a class="color5e" href="%s" target="_blank">《%s》</a> 下的提问被同班同学回复啦！' % (href,obj.name)
            setattr(dynamic, 'content', content)

        elif dynamic.type == 4:
            href = settings.FPS_HOST+'article/%d' % obj.id
            content = '发表的文章：<a class="color5e" href="%s" target="_blank">《%s》</a> 被同班同学回复啦！' % (href,obj.title)
            setattr(dynamic, 'content', content)

        elif dynamic.type == 7:
            href = settings.FPS_HOST+'article/%d' % obj.id
            content = '发表了文章<a class="color5e" href="%s" target="_blank">《%s》</a>' % (href,obj.title)
            setattr(dynamic, 'content', content)
    return render_to_response("mz_course/class_student_dynamic.html", {"dynamics": dynamics})


# 老师列表页
class TeacherListView(View):
    template = "mz_course/teacher_list.html"

    def get(self, request):
        if request.method == 'GET':
            seo = PageSeoSet()
            try:
                seo = PageSeoSet.objects.get(page_name='5')
            except Exception,e:
                logger.error(e)
            # 广告位
            try:
                ad = Ad.objects.filter(type=2)[0]
            except:
                ad = []
            try:
                page = int(request.GET.get('page', 1))
                if page < 1:
                    page = 1
            except:
                page = 1
            group = Group.objects.get(name='老师')   # 所有老师
            te_list = Course.objects.distinct().values_list('teacher')
            teachers = group.user_set.filter(id__in=te_list).order_by("-id")
            caree_num = teachers.count()
            if caree_num == 0:
                return render(request, self.template)
            num_pages = int((caree_num + 8 - 1) / 8)  # 总页数
            if page >= num_pages:
                page = num_pages

            if page == 1:  # 分页
                cur_page = teachers[:8]
            else:
                cur_page = teachers[8 * page - 8:8 * page if page != num_pages else None]

            pages, banner = self.get_page_info(page, num_pages)

            template_vars = {'pages': pages,
                             'page': page,
                             'seo': seo,
                             'last_page': num_pages,
                             'banner': banner,
                             'lists': cur_page,
                             'ad': ad,
                             }
            # cache.set('teacher_list', template_vars, settings.CACHE_TIME)
            return render(request, self.template, template_vars)

    # 分页
    def get_page_info(self, page, page_num, pages=None):
        if not pages:
            pages = range(1, page_num+1)
        if page_num >= 2:
                pages = pages[1:-1]
        banner = False
        if page_num <= 6:
            pass
        else:
            if page+4 <= page_num:
                banner = True
            if page < 4:
                pages = pages[:4]
            elif page >= page_num-2:
                pages = pages[-4:]
            else:
                pages = pages[page-4:page+1]
        return pages, banner


# 课程列表页
class CourseListView(View):
    template = "mz_course/stage_course_list.html"

    def get(self, request):

        try:
            page = int(request.GET.get('page', 1))
            if page < 1:
                page = 1
        except:
            page = 1

        title = '公开课 - 麦子学院'
        career_catagory = request.GET.get(u'career', 'all')
        career_catagory = "all" if career_catagory == '' else career_catagory
        course_catagory = request.GET.get(u'catagory', 'all')
        course_catagory = "all" if course_catagory == '' else course_catagory
        sort_by = request.GET.get(u'sort_by', '')

        # 游客读取页面缓存
        if request.user.is_anonymous():
            if career_catagory+course_catagory+sort_by+str(page) == 'allall1':
                html = cache.get('allall1')
                if html:
                    return HttpResponse(html)
        try:
            ad = Ad.objects.filter(type=1)[0]
        except:
            ad = []

        seo = PageSeoSet()
        try:
            seo = PageSeoSet.objects.get(page_name='4')
        except Exception,e:
            logger.error(e)

        if course_catagory != 'all':
            title = course_catagory + ' - ' + title
        if career_catagory != 'all':
            title = career_catagory + ' - ' + title

        career_catagorys_list = CareerCatagory.objects.all().order_by('id')  # 课程方向
        course_catagorys_list = []
        if career_catagory != 'all':
            course_catagorys = CourseCatagory.objects.filter(career_catagory__name=career_catagory)
            course_catagory_list = [course_cata.name for course_cata in course_catagorys]
            course_catagorys_list.extend(course_catagory_list)
        else:
            for career_catag in career_catagorys_list:           # 课程分类
                course_catagorys = CourseCatagory.objects.filter(career_catagory=career_catag)
                course_catagory_list = [course_cata.name for course_cata in course_catagorys]
                course_catagorys_list.extend(course_catagory_list)

        courses = []
        total_nums = 0
        # 按课程方向筛选
        if course_catagory != 'all' and career_catagory == 'all':
            query = Course.objects.filter(Q(name__icontains=course_catagory) |
                                          Q(search_keywords__name__icontains=course_catagory),
                                          is_click=True, is_active=True).query
            query.group_by = ['name']
            courses = QuerySet(query=query, model=Course)
            total_nums = len(courses)
        # 按课程分类下的课程方向筛选
        elif course_catagory != 'all' and career_catagory != 'all':
            query = Course.objects.filter(Q(name__icontains=course_catagory) |
                                          Q(search_keywords__name__icontains=course_catagory),
                                          is_click=True, is_active=True).query
            query.group_by = ['name']
            courses = QuerySet(query=query, model=Course)
            total_nums = len(courses)
        # 按课程分类排序
        elif course_catagory == 'all' and career_catagory != 'all':
            tmp_course_catagorys = CourseCatagory.objects.filter(career_catagory__name=career_catagory)
            course_catagory_list = [tmp_course_catagory.name for tmp_course_catagory in tmp_course_catagorys]
            query_list = []
            for item in course_catagory_list:
                query_list.append(Q(name__icontains=item))
                query_list.append(Q(search_keywords__name__icontains=item))
            filter_query = reduce(operator.or_, tuple(query_list))
            query = Course.objects.filter(filter_query, is_click=True, is_active=True).query
            query.group_by = ['name']
            courses = QuerySet(query=query, model=Course).order_by('-date_publish')
            total_nums = Course.objects.filter(filter_query, is_click=True, is_active=True).values('name').distinct().count()
        # 全部课程
        elif course_catagory == 'all' and career_catagory == 'all':
            query = Course.objects.filter(is_active=True, is_click=True).query
            query.group_by = ['name']
            courses = QuerySet(query=query, model=Course).order_by('-date_publish')
            total_nums = Course.objects.filter(is_active=True, is_click=True).values('name').distinct().count()
        # 按热门排序
        if sort_by == 'hot':
            courses = courses.order_by("-favorite_count")
        # 按最新排序
        elif sort_by == "new":
            courses = courses.order_by("-date_publish")
        # 按播放次数排序
        elif sort_by == "mostplay":
            course_list = [course for course in courses]
            lesson_group = Lesson.objects.filter(course__in=course_list).values('course').annotate(s_amount=Sum('play_count')).order_by('-s_amount')
            courses = []
            for le in lesson_group:
                try:
                    cours = Course.objects.get(id=le['course'], is_click=True)
                    courses.append(cours)
                except:
                    pass
            total_nums = len(courses)

        num_pages = int((total_nums + 16 - 1) / 16)  # 总页数
        if num_pages != 0:
            if page >= num_pages:
                page = num_pages

            if page == 1:  # 分页
                cur_page = courses[:16]
            else:
                cur_page = courses[16 * page - 16:16 * page if page != num_pages else None]
        else:
            cur_page = []
        pages, banner = self.get_page_info(page, num_pages)

        for course in cur_page:
            stage_set = course.stages_m.all()

            try:
                careercourse = stage_set[0].career_course.short_name.lower()
            except:
                careercourse = 'others'
            lesson_list = Lesson.objects.filter(course_id=course.id).order_by("index")
            callback_url = "/course/%s/%d-%d" % (careercourse, course.id, lesson_list[0].id) if lesson_list else ""
            setattr(course, 'callback_url', callback_url)

        t = get_template(self.template)
        html = t.render(RequestContext(request, {'banner': banner,
                                               'page': page,
                                               'pages': pages,
                                               'seo': seo,
                                               'last_page': num_pages,
                                               'lists': cur_page,
                                               'career_catagorys_list': career_catagorys_list,
                                               'course_catagorys_list': course_catagorys_list,
                                               'direction': career_catagory,
                                               'classified': course_catagory,
                                               'sort': sort_by,
                                               'title': title,
                                               'ad': ad
                                               }))
        # 游客保存首页缓存
        if request.user.is_anonymous():
            if career_catagory+course_catagory+sort_by+str(page) == 'allall1':
                cache.set('allall1', html, 60*60)
        return HttpResponse(html)

    # 分页
    def get_page_info(self, page, page_num, pages=None):
        if not pages:
            pages = range(1, page_num+1)
        if page_num >= 2:
                pages = pages[1:-1]
        banner = False
        if page_num <= 6:
            pass
        else:
            if page+4 <= page_num:
                banner = True
            if page < 4:
                pages = pages[:4]
            elif page >= page_num-2:
                pages = pages[-4:]
            else:
                pages = pages[page-4:page+1]
        return pages, banner


# 课程介绍页
class CourseIntroductionView(View):
    template = ""

    def get(self, request, course_id):
        self.template = "mz_course/introduction/%s.html" % course_id
        career_course = CareerCourse.objects.get(short_name__iexact=course_id)
        # 手机端过来全部跳转大纲页
        if checkMobile(request):
            return HttpResponseRedirect("/course/%s" % course_id)
        # 该职业课程是否有介绍页
        if career_course.guide_line_page:
            # 是否是登陆用户并且报过该职业课程的学员
            if request.user.is_authenticated() and Class.objects.filter(career_course=career_course, students=request.user).exists():
                # 是否是从大纲页跳转到介绍页
                if request.GET.get('force'):
                    return render(request, self.template, {'couse_short_name': course_id,
                                                           'cur_careercourse': career_course,
                                                           'is_display': True
                                                           })
                else:
                    return HttpResponseRedirect("/course/%s" % course_id)
            else:
                return render(request, self.template, {'couse_short_name': course_id,
                                                       'cur_careercourse': career_course,
                                                       'is_display': True
                                                       })
        else:
            if request.GET.get('force'):
                return render(request, self.template, {'couse_short_name': course_id,
                                                       'cur_careercourse': career_course,
                                                       'is_display': True
                                                       })
            else:
                return HttpResponseRedirect("/course/%s" % course_id)


# 价格列表页
def career_course_price_list(request):
    career_course_list = CareerCourse.objects.all()
    data = []
    data_3 = []
    for career_course in career_course_list:
        result = {}
        result_3 = {}
        full_price = 0
        beta_price = 0
        full_price_3 = 0
        beta_price_3 = 0
        stages = Stage.objects.xall().filter(career_course=career_course)
        for stage in stages:
            if stage.lps_version == '3.0':
                full_price_3 += stage.price
                if stage.is_try:
                    beta_price_3 += stage.price
            else:
                full_price += stage.price
                if stage.is_try:
                    beta_price += stage.price
        if beta_price != 0 or full_price != 0:
            result['name'] = career_course.name
            result['version'] = '2.0'
            result['beta_price'] = beta_price
            result['full_price'] = full_price
            data.append(result)
        if beta_price_3 != 0 or full_price_3 != 0:
            result_3['name'] = career_course.name
            result_3['version'] = '3.0'
            result_3['beta_price'] = beta_price_3
            result_3['full_price'] = full_price_3
            data_3.append(result_3)
    return render(request, 'mz_course/career_course_price.html', {'career_courses': data, 'career_courses_3': data_3})


# 课程详情页
@require_GET
def course_detail_view(request, course_id):
    api = course_sys_api.CourseSysApi.default_instance()
    common_api = common_sys_api.CommonSysApi.default_instance()

    # 记录课程点击次数
    result = db.api.course.course.update_course_click_count(course_id)
    if result.is_error():
        log.info('update_course_click_count fail. More info: course_id: %s' % course_id)

    course = ensure_apiresult_obj(api.get_one_course, id=course_id)
    course.tags = opt_apiresult_obj([], common_api.get_course_tags, course_id)
    teacher = ensure_obj(course.teacher)
    lessons = api.get_all_lesson(course_id=course_id).obj

    career_courses = api.get_careercourse_by_course(course_id=course_id, is_active=True).obj
    if career_courses:
        career_courses = career_courses[0]
        # 需要排除当前展示的课程id，所以，获取11个相关课程，并过滤，
        course_list = api.get_course_by_careercourse(
            career_courses.id, limit=11).obj
        cl = list(item for item in course_list if item.id != int(course_id))
        course_list = cl[:10]
        ad = api.get_ad_by_careercourse(career_courses.id).obj
        ad = ad[0] if ad else None
    else:
        course_list = []
        ad = {}

    articles = db.api.article.article.get_article_with_course(course_id=course_id).result()
    for article in articles:  # 将分组聚合的tag信息拆分
        if article['tag']:
            article['tag'] = dict(list(item.split('_') for item in article['tag'].split(','))[:3])
    courseware = api.get_all_courseresource_by_course(course_id=course_id).obj
    seo = common_api.get_course_seo(course_id).obj

    wiki_item_list = db.api.wiki.wiki.get_wiki_by_lps_course_id(course_id)
    if wiki_item_list.is_error():
        log.info('get_wiki_by_lps_course_id fail. More info: course_id: %s' % course_id)
        wiki_item_list = []
    else:
        wiki_item_list = wiki_item_list.result()

    data = dict(
        course=course, teacher=teacher, lessons=lessons, articles=articles,
        career_courses=career_courses, course_list=course_list, ad=ad,
        courseware=courseware, course_video_length=calc_course_video_length(lessons),
        seo=seo, wiki_item_list=wiki_item_list)
    return render(request, 'mz_course/lesson_video_lists.html', data)


# 章节播放页
@require_GET
def lesson_video_view(request, course_id, lesson_id):
    """

    :param request:
    :param course_id:
    :param lesson_id:
    :return:
    course: id, need_pay
    lessen_list: [[id, name, video_length], ...]
    lesson: [id, name, video_length, video_url]

    seo
    discuss_list
    course_ware(课件下载)
    """
    # 记录课程播放次数
    result = db.api.course.lesson.update_lesson_play_count(lesson_id)
    if result.is_error():
        log.info('update_lesson_play_count fail. More info: course_id: %s lesson_id: %s' % (course_id, lesson_id))

    user_id = request.user.id
    now = datetime.now()

    data = {}
    # 获取课程相关属性
    course = db.api.course.course.get_id_course(course_id)
    if course.is_error():
        log.warn('get_id_course is error. user_id: %s' % user_id)
        course = {}
    else:
        course = course.result()
        if course:
            course = course[0]
        else:
            raise Http404  # 没有取到course,返回404错误

    lesson = db.api.course.lesson.get_lesson_by_id(lesson_id)
    if lesson.is_error():
        log.warn('get_lesson_by_id is error. user_id: %s' % user_id)
        lesson = {}
    else:
        lesson = lesson.result()

    lesson_list = db.api.course.lesson.get_lesson_list_by_course_id(course_id)
    if lesson_list.is_error():
        log.warn('get_lesson_list_by_course_id is error. user_id: %s' % user_id)
        lesson_list = []
    else:
        lesson_list = lesson_list.result()

    data['course'] = course
    data['lesson'] = lesson
    data['lesson_list'] = lesson_list

    # 获取小课程相关职业课程
    career_courses = db.api.course.career_course.get_career_course_by_course_id_through_careerobjrelation(course_id)
    if career_courses.is_error():
        log.warn('get_career_course_by_course_id_through_careerobjrelation is error. user_id: %s' % user_id)
        career_courses = []
    else:
        career_courses = career_courses.result()

    # 设置广告
    career_courses_id = []
    career_course = {}
    ad_career_course = {}
    # 若无相关职业课程,职业课程的基础为所有职业课程
    if not career_courses:
        all_career_courses = db.api.course.career_course.get_career_courses()
        if all_career_courses.is_error():
            log.warn('get_career_courses is error. user_id: %s' % user_id)
        else:
            all_career_courses = all_career_courses.result()
            # 如果有职业课程,广告职业课程为在职业课基础里随机取一个职业课程
            if all_career_courses:
                all_career_courses = all_career_courses['result']
                ad_career_course = all_career_courses[random.randrange(0, len(all_career_courses), 1)]
    # 否则选出career_courses_id,随机取出真正相关的职业课程,广告职业课程为此职业课程
    else:
        map(lambda x: career_courses_id.append(x['id']), career_courses)
        career_course = career_courses[random.randrange(0, len(career_courses), 1)]
        ad_career_course = career_course

    data['career_course'] = career_course
    data['ad_career_course'] = ad_career_course

    # 获取课程资源
    course_resource = db.api.course.course.get_course_resource_by_course_id(course_id)
    if course_resource.is_error():
        log.warn('get_course_resource_by_course_id is error. user_id: %s' % user_id)
        course_resource = []
    else:
        course_resource = course_resource.result()
    data['course_resource'] = course_resource

    group_name_teacher = db.api.common.new_discuss_post.is_teacher(user_id)
    if group_name_teacher.is_error():
        log.warn('is_enterprise_student_or_teacher is error. user_id: %s' % user_id)

    group_name = 'teacher' if group_name_teacher.result() else ''
    data['group_name'] = group_name

    # 判断用户对此课程相关职业课是否付费
    if not career_courses_id:
        is_paid = False
    else:
        is_paid = db.api.course.career_course.is_career_student_of_these_career_courses(user_id, now, career_courses_id)
        if is_paid.is_error():
            log.warn('is_career_student_of_these_career_courses is error. user_id: %s' % user_id)
            is_paid = False
        else:
            is_paid = is_paid.result()
            is_paid = bool(is_paid)
        # 如果是老师,也算作已付费
        if group_name == 'teacher':
            is_paid = True
    data['is_paid'] = is_paid

    # 获取seo
    seo = db.api.common.seo.get_seo_by_obj_id(course_id, 'COURSE')
    if seo.is_error():
        log.warn('get_seo_by_obj_id is error. user_id: %s' % user_id)
        seo = {}
    else:
        seo = seo.result()
    data['seo'] = seo

    # 获取问答列表
    all_questions, my_questions = get_questons(lesson_id, user_id)
    data['all_questions'] = all_questions
    data['my_questions'] = my_questions
    data['lesson_id'] = lesson_id
    data['discuss_location'] = '%s_%s' % (course_id, lesson_id)  # 回复讨论的位置

    # 获取lesson相关老师
    teachers = {}
    if career_courses_id:
        teachers = db.api.common.new_discuss_post.get_lesson_teachers(career_courses_id)
        if teachers.is_error():
            log.warn('get_lesson_teachers is error. user_id: %s' % user_id)
            teachers = ''
        else:
            teachers = teachers.result()
            if teachers:
                teachers = teachers[random.randrange(0, len(teachers), 1)]
    data['teachers'] = teachers

    return render(request, 'mz_course/lessonVideo.html', data)


# 章节播放页
@require_GET
def lps4_lesson_video_view(request, course_id, lesson_id):
    """

    :param request:
    :param course_id:
    :param lesson_id:
    :return:
    course: id, need_pay
    lessen_list: [[id, name, video_length], ...]
    lesson: [id, name, video_length, video_url]

    seo
    discuss_list
    course_ware(课件下载)
    """
    # 记录课程播放次数
    result = db.api.course.lesson.update_lesson_play_count(lesson_id)
    if result.is_error():
        log.info('update_lesson_play_count fail. More info: course_id: %s lesson_id: %s' % (course_id, lesson_id))

    user_id = request.user.id
    now = datetime.now()

    data = {}
    # 获取课程相关属性
    course = db.api.course.course.get_id_course(course_id)
    if course.is_error():
        log.warn('get_id_course is error. user_id: %s' % user_id)
        course = {}
    else:
        course = course.result()
        if course:
            course = course[0]
        else:
            raise Http404  # 没有取到course,返回404错误

    lesson = db.api.course.lesson.get_lesson_by_id(lesson_id)
    if lesson.is_error():
        log.warn('get_lesson_by_id is error. user_id: %s' % user_id)
        lesson = {}
    else:
        lesson = lesson.result()

    lesson_list = db.api.course.lesson.get_lesson_list_by_course_id(course_id)
    if lesson_list.is_error():
        log.warn('get_lesson_list_by_course_id is error. user_id: %s' % user_id)
        lesson_list = []
    else:
        lesson_list = lesson_list.result()

    data['course'] = course
    data['lesson'] = lesson
    data['lesson_list'] = lesson_list
    # 章节编号
    try:
        data['lesson_num'] = [l['id'] for l in lesson_list].index(lesson['id']) + 1
    except Exception:
        raise Http404

    # 获取小课程相关职业课程
    career_courses = db.api.course.career_course.get_career_course_by_course_id_through_careerobjrelation(course_id)
    if career_courses.is_error():
        log.warn('get_career_course_by_course_id_through_careerobjrelation is error. user_id: %s' % user_id)
        career_courses = []
    else:
        career_courses = career_courses.result()

    # 设置广告
    career_courses_id = []
    career_course = {}
    ad_career_course = {}
    # 若无相关职业课程,职业课程的基础为所有职业课程
    if not career_courses:
        all_career_courses = db.api.course.career_course.get_career_courses()
        if all_career_courses.is_error():
            log.warn('get_career_courses is error. user_id: %s' % user_id)
        else:
            all_career_courses = all_career_courses.result()
            # 如果有职业课程,广告职业课程为在职业课基础里随机取一个职业课程
            if all_career_courses:
                all_career_courses = all_career_courses['result']
                ad_career_course = all_career_courses[random.randrange(0, len(all_career_courses), 1)]
    # 否则选出career_courses_id,随机取出真正相关的职业课程,广告职业课程为此职业课程
    else:
        map(lambda x: career_courses_id.append(x['id']), career_courses)
        career_course = career_courses[random.randrange(0, len(career_courses), 1)]
        ad_career_course = career_course

    data['career_course'] = career_course
    data['ad_career_course'] = ad_career_course

    # 获取课程资源
    course_resource = db.api.course.course.get_course_resource_by_course_id(course_id)
    if course_resource.is_error():
        log.warn('get_course_resource_by_course_id is error. user_id: %s' % user_id)
        course_resource = []
    else:
        course_resource = course_resource.result()
    data['course_resource'] = course_resource

    group_name_teacher = db.api.common.new_discuss_post.is_teacher(user_id)
    if group_name_teacher.is_error():
        log.warn('is_enterprise_student_or_teacher is error. user_id: %s' % user_id)

    group_name = 'teacher' if group_name_teacher.result() else ''
    data['group_name'] = group_name

    # 判断用户对此课程相关职业课是否付费
    if not career_courses_id:
        is_paid = False
    else:
        is_paid = db.api.course.career_course.is_career_student_of_these_career_courses(user_id, now, career_courses_id)
        if is_paid.is_error():
            log.warn('is_career_student_of_these_career_courses is error. user_id: %s' % user_id)
            is_paid = False
        else:
            is_paid = is_paid.result()
            is_paid = bool(is_paid)
        # 如果是老师,也算作已付费
        if group_name == 'teacher':
            is_paid = True
    data['is_paid'] = is_paid

    # 获取seo
    seo = db.api.common.seo.get_seo_by_obj_id(course_id, 'COURSE')
    if seo.is_error():
        log.warn('get_seo_by_obj_id is error. user_id: %s' % user_id)
        seo = {}
    else:
        seo = seo.result()
    data['seo'] = seo

    # 获取问答列表
    all_questions = get_all_questions(lesson_id, user_id, 20)
    data['questions'] = all_questions
    data['lesson_id'] = lesson_id
    data['discuss_location'] = '%s_%s' % (course_id, lesson_id)  # 回复讨论的位置

    # 获取lesson相关老师
    teachers = {}
    if career_courses_id:
        teachers = db.api.common.new_discuss_post.get_lesson_teachers(career_courses_id)
        if teachers.is_error():
            log.warn('get_lesson_teachers is error. user_id: %s' % user_id)
            teachers = ''
        else:
            teachers = teachers.result()
            if teachers:
                teachers = teachers[random.randrange(0, len(teachers), 1)]
    data['teachers'] = teachers

    # wiki
    wiki_item_list = db.api.wiki.wiki.get_wiki_by_lps_course_id(course_id)
    if wiki_item_list.is_error():
        log.info('get_wiki_by_lps_course_id fail. More info: course_id: %s' % course_id)
        wiki_item_list = []
    else:
        wiki_item_list = wiki_item_list.result()
    data['wiki_item_list'] = wiki_item_list

    # 技能提升
    api = course_sys_api.CourseSysApi.default_instance()
    # 需要排除当前展示的课程id，所以，获取5个相关课程，并过滤，
    course_list = api.get_course_by_careercourse(
        ad_career_course['id'], limit=5).obj
    cl = list(item for item in course_list if item.id != int(course_id))
    course_list = cl[:4]
    data['course_list'] = course_list

    return render(request, 'mz_course/video_play/small_course.html', data)


class CourseListViewNew(View):
    """
    @brief 基于新架构和库表设计的课程库view
    """

    template = "mz_course/stage_course_list.html"

    # todo 为快速开发，直接从service调用sql执行．基于最新架构进行改造
    from mz_platform.services.functions.mz_service import MZService
    mz_service = MZService()

    def get(self, request):

        page = self.__init_page(request)

        self.career_category = int(request.GET.get(u'career', 0))
        self.course_category = int(request.GET.get(u'catagory', 0))
        self.sort_by = request.GET.get(u'sort_by', '')

        # 游客读取页面缓存
        # todo
        # 1. 采用最新的cache系统
        # 2. 目前的cache策略是，仅缓存用户未登录， 且career_category == 0, course_category == 0, sort_by == '', page == 1 的页面
        #    该策略需要更多讨论。暂时采用目前策略
        need_cache = request.user.is_anonymous() and self.career_category == 0 and self.course_category == 0 and \
                     self.sort_by == '' and page == 1
        if need_cache:
            html = cache.get('course_list_all_all_1')
            if html:
                return HttpResponse(html)

        # todo  采用最新表结构的广告，等待李希确认
        try:
            ad = Ad.objects.filter(type=1)[0]
        except:
            ad = []

        # 方向和分类列表
        # todo 为快速开发，并未按照新的架构方式实现，按最新的架构改造
        career_category_list = self.__get_career_category_list()
        course_category_list = self.__get_course_category_list()

        # 获取方向和分类的名字
        name = list(item['name'] for item in career_category_list if item['id'] == self.career_category)
        self.career_category_name = name[0] if name else ''
        name = list(item['name'] for item in course_category_list if item['id'] == self.course_category)
        self.course_category_name = name[0] if name else ''

        # seo
        seo = self.__generate_seo()

        # 获取符合查询条件的sql
        # todo 为快速开发，并未按照新的架构方式实现，按最新的架构改造
        sql = self.__generate_sql()

        # 处理分页
        from mz_platform.services.functions.mz_service import Pager
        pager = Pager(sql, 16)
        num_pages = pager.page_total()
        page = pager.page_safe(page)
        cur_page = pager.page_data(page)
        pages, banner = pager.get_page_info(page, num_pages)

        t = get_template(self.template)
        html = t.render(RequestContext(request, dict(banner=banner, page=page, pages=pages, seo=seo,
                                                     last_page=num_pages, lists=cur_page,
                                                     career_catagorys_list=career_category_list,
                                                     course_catagorys_list=course_category_list,
                                                     direction=self.career_category,
                                                     classified=self.course_category, sort=self.sort_by, ad=ad)))

        # 游客保存首页缓存
        if need_cache:
            cache.set('course_list_all_all_1', html, 60*60)

        return HttpResponse(html)

    def __get_career_category_list(self):
        """
        @brief 获取全部课程方向列表
        @return:

        @todo 基于新的架构方式实现
        """
        sql = '''
            select id, name from mz_course_careercatagory
            '''
        return self.mz_service.db.select(sql)

    def __get_course_category_list(self):
        """
        @brief 获取全部课程分类列表
        @return:

        @todo 基于新的架构方式实现
        """
        if self.career_category:
            sql = '''
                select distinct t.id, t.name from mz_course_tag as t
                inner join mz_common_objtagrelation as otr on t.id = otr.tag_id
                where otr.obj_type = "COURSE" and otr.careercatagory_id = %s
                ''' % self.career_category
        else:
            sql = '''
                select id, name from mz_course_tag
                '''
        return self.mz_service.db.select(sql)

    def __generate_seo(self):
        """
        @brief 生成页面需要的TDK

        @return:

        @note  方向，分类和热度的组合条件，严格依照文档。其它组合的情况未做考虑和实现。
        """
        title_pref = [u'课程库', u'麦子学院']
        sort_content = dict(new=u'最新', hot=u'最热', mostplay=u'最多播放')
        seo_description = u'IT职业在线学习，视频教程免费观看，为软件开发人员提供包括Android开发教程、iOS开发教程、' \
              u'手游开发教程、python基础教程、嵌入式开发教程、产品经理教程、C语言教程、html5教程、php教程' \
              u'等多门编程语言在内的IT职业课程的学习。'
        seo_title = u'课程库 - IT培训视频教程-麦子学院'
        seo_keyword = u'IT教程，IT在线教育，IT培训课程，IT职业课程，IT在线学习，IT在线视频教程'

        if self.career_category == 0 and self.course_category == 0:  # 课程方向，分类都没有选择，
            seo_title = seo_title
            seo_keyword = seo_keyword

        if self.career_category != 0 and self.course_category == 0:  # 只选择了课程方向
            tmp = title_pref[:]
            tmp.insert(0, self.career_category_name)
            seo_title = '-'.join(tmp)
            seo_keyword = ', '.join(['%s' % self.career_category_name,
                                     '%s学习' % self.career_category_name, '%s教程' % self.career_category_name])

        if self.career_category != 0 and self.course_category != 0 and not self.sort_by:  # 同时选择方向，分类，但未选择热度
            tmp = title_pref[:]
            tmp.insert(0, self.career_category_name)
            tmp.insert(0, '%s教程' % self.course_category_name)
            seo_title = '-'.join(tmp)
            seo_keyword = ', '.join(['%s' % self.course_category_name,
                                     '%s学习' % self.course_category_name, '%s教程' % self.course_category_name])

        if self.career_category != 0 and self.course_category != 0 and self.sort_by:  # 同时选择了方向, 分类和热度
            tmp = title_pref[:]
            tmp.insert(0, self.career_category_name)
            tmp.insert(0, '%s%s' % (sort_content[self.sort_by], self.course_category_name))
            seo_title = '-'.join(tmp)
            seo_keyword = ', '.join(['%s' % self.course_category_name,
                                     '%s学习' % self.course_category_name,
                                     '%s%s教程' % (sort_content[self.sort_by], self.course_category_name)])
        return dict(seo_description=seo_description, seo_keyword=seo_keyword, seo_title=seo_title)

    @staticmethod
    def __init_page(request):
        try:
            page = int(request.GET.get('page', 1))
            page = 1 if page < 1 else page
        except (ValueError, TypeError):
            page = 1
        return page

    def __generate_sql(self):
        """
        @brief 生成需要sql语句
        @return:
        """
        sql = '''select distinct c.* from mz_course_course as c inner join mz_common_objtagrelation as o
                 on c.id = o.obj_id where o.obj_type = "COURSE" and'''
        sql_prifix = '''and c.is_active = 1 and c.is_click = 1'''

        # 处理筛选标签
        if self.course_category != 0:  # 如果课程分类有定义，则按照课程分类筛选
            sql = '%s %s %s' % (sql, 'o.tag_id = %s' % self.course_category, sql_prifix)
        elif self.career_category != 0:  # 如果课程方向有定义，但课程分类未定义，则按照课程方向筛选
            sql = '%s %s %s' % (sql, 'o.careercatagory_id = %s' % self.career_category, sql_prifix)
        elif self.course_category == 0 and self.career_category == 0:  # 课程方向和分类均未筛选，则返回全部课程
            sql = '''select distinct * from mz_course_course where is_active=1 and is_click=1'''

        # 处理排序
        sql_sort_by = dict(hot='order by -favorite_count', new='order by -date_publish')
        if self.sort_by in ['hot', 'new']:  # 按照最新,最热排序
            sql = '%s %s' % (sql, sql_sort_by[self.sort_by])
        if self.sort_by == 'mostplay':  # 按照播放次数排序的时候，需要额外写sql, 因为需要统计每个lesson的播放次数之和
            sql = '''select distinct c.*, sum(l.play_count) as play_total from mz_course_course as c
                     inner join mz_common_objtagrelation as o on c.id = o.obj_id
                     left outer join mz_course_lesson as l on c.id = l.course_id
                     where o.obj_type = "COURSE" and c.is_active = 1 and c.is_click = 1'''
            sql_prifix = '''group by c.id order by play_total desc'''
            if self.course_category != 0:
                sql = '%s %s' % (sql, ' and o.tag_id = %s' % self.course_category)
            elif self.career_category != 0:
                sql = '%s %s' % (sql, ' and o.careercatagory_id = %s' % self.career_category)
            sql = '%s %s' % (sql, sql_prifix)

        return sql
