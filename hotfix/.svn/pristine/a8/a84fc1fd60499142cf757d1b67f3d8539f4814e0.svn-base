# -*- coding: utf-8 -*-

"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/3/29 15:23
@note:  ??
"""
import datetime
import requests
import json

from utils.logger import logger as log
from core.common.http.response import success_json, failed_json
from mz_course.models import CareerCourse, Course, Course_User_Score, Stage, CourseDirection, Lesson
from mz_lps.models import ClassStudents, Class
from mz_lps4.class_dict import NORMAL_CLASS_DICT, LPS4_DICT
from mz_user.models import MyFavorite, UserProfile, UserLearningLesson
from mz_lps3.models import StageTaskRelation
from django.conf import settings
from django.db.models import Q
from .interface import strip_tags, emoji_to_app, is_ios_check
from website.api.user.interface import get_user_type
from website.api.learning.interface import video_detail
from website.api.user.decorators import app_user_required
from mz_common.models import RecommendKeywords, CareerObjRelation
from mz_common.forms import DiscussForm, GetDiscussForm
from mz_pay.views import goto_pay
import db.api.common.app
import db.api.course.career_course_pay
import db.api.course.course_task


# 获取方向
def app_get_direction_list(request):
    result = [dict(
                direction_id=direction.id,
                direction_name=direction.name
                )
              for direction in CourseDirection.objects.all()]
    return success_json({'list': result})


def app_get_direction_list_new(request):
    if is_ios_check(request):
        result = db.api.common.app.app_direction_career_course_ios_check()
    else:
        result = db.api.common.app.app_direction_career_course(_enable_cache=True)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    directions = result.result()
    data = []
    temp = {}
    temp_career = []
    for direction in directions:
        is_classed = False
        is_payed = False
        if request.user.is_authenticated():
            result = db.api.common.app.app_user_class_type(
                    user_id=request.user.id, career_id=direction['career_id'])
            if not result.is_error():
                is_payed = result.result()['is_normal_class']
                is_app_free = result.result()['is_app_free']
                if is_payed or is_app_free:
                    is_classed = True
        if int(temp.get('direction_id', 0)) == int(direction['direction_id']):
            temp.update(dict(
                direction_name=direction['direction_name'],
                direction_id=direction['direction_id'],
                direction_img=settings.SITE_URL + settings.MEDIA_URL + str(direction['direction_image']),
                career_list=[]
            ))
            temp_career.append(dict(
                career_id=direction['career_id'],
                career_name=direction['career_name'],
                is_classed=is_classed,       # 是否报班 无论付费班还是app体验班
                is_can_pay=direction['is_class'],       # 该课程是否能够报名
                is_payed=is_payed,  # 用户是否付费该课程
                img_url=settings.SITE_URL + settings.MEDIA_URL + str(direction['app_career_image']),
                career_url=settings.SITE_URL + '/course/%s-px' % direction['short_name']
            ))
        else:
            if int(temp.get('direction_id', 0)) != int(direction['direction_id']) and temp and temp_career:
                temp['career_list'] = temp_career
                data.append(temp)
                temp = {}
                temp_career = []
            temp.update(dict(
                direction_name=direction['direction_name'],
                direction_id=direction['direction_id'],
                direction_img=settings.SITE_URL + settings.MEDIA_URL + str(direction['direction_image']),
                career_list=[]
            ))
            temp_career.append(dict(
                career_id=direction['career_id'],
                career_name=direction['career_name'],
                is_classed=is_classed,       # 是否报班 无论付费班还是app体验班
                is_can_pay=direction['is_class'],       # 该课程是否能够报名
                is_payed=is_payed,  # 用户是否付费该课程
                img_url=settings.SITE_URL + settings.MEDIA_URL + str(direction['app_career_image']),
                career_url=settings.SITE_URL + '/course/%s-px' % direction['short_name']
            ))
    temp['career_list'] = temp_career
    data.append(temp)
    return success_json({'list': data})


# 获取方向职业课程
def app_direction(request):
    result = []
    direction = request.POST.get('direction', None)
    if direction:
        if is_ios_check(request):
            career_courses = CourseDirection.objects.get(id=direction).career_course.all().exclude(
                short_name__icontains='Android'
            ).order_by('index')
        else:
            career_courses = CourseDirection.objects.get(id=direction).career_course.all().order_by('index')
    else:
        if is_ios_check(request):
            career_courses = CareerCourse.objects.all().exclude(
                short_name__icontains='Android'
            ).exclude(coursedirection__name=None).order_by('index')
        else:
            career_courses = CareerCourse.objects.all().exclude(coursedirection__name=None).order_by('index')
    for career_course in career_courses:
        result.append(dict(
            career_id=career_course.id,
            career_name=career_course.name,
            student_count=career_course.student_count,
            img_url=settings.SITE_URL + settings.MEDIA_URL + str(career_course.app_career_image),
            career_url=settings.SITE_URL + '/course/%s-px' % career_course.short_name
        ))
    return success_json({'list': result})


# 收藏课程
@app_user_required
def app_collect_course(request):
    course_id = request.POST.get('course_id', None)
    lesson_id = request.POST.get('lesson_id', None)
    user = request.user
    favorite = MyFavorite()
    if not course_id:
        try:
            course = Lesson.objects.get(id=lesson_id).course
        except Lesson.DoesNotExist:
            return failed_json(u'找不到相关课程')
    else:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return failed_json(u'找不到相关课程')
    if MyFavorite.objects.filter(user=user, course=course).exists():
        return failed_json(u'该课程已经收藏')
    favorite.user = user
    favorite.course = course
    favorite.save()
    # 收藏数+1
    course.favorite_count += 1
    course.save()
    return success_json({})


# 为课程打分
@app_user_required
def app_grade_course(request):
    course_id = request.POST.get('course_id', None)
    score = request.POST.get('score', None)
    user = request.user
    if not score:
        return failed_json(u'评分不能为空')
    if score not in ['0', '1', '2', '3', '4', '5']:
        return failed_json(u'评分格式错误')
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return failed_json(u'该课程不存在')
    try:
        Course_User_Score.objects.get(course=course, user=user)
        return failed_json(u'已经打过分')
    except Course_User_Score.DoesNotExist:
        new_record = Course_User_Score()
        new_record.score = float(score)
        new_record.course = course
        new_record.user = user
        new_record.save()
        return success_json({})


# 获取课程视频列表
@app_user_required
def app_lesson_list(request):
    course_id = request.POST.get('course_id', None)
    user = request.user
    try:
        course = Course.objects.get(id=course_id)
        course.click_count += 1
        course.save()
    except Course.DoesNotExist:
        return failed_json(u'该课程不存在')
    if course.need_pay:
        user_classes = ClassStudents.objects.filter(user_id=user.id, status=1, student_class__class_type=0)
        user_career = []
        for user_class in user_classes:
            user_career.append(int(user_class.student_class.career_course_id))
        career_ids = []
        career_objs = CareerObjRelation.objects.filter(obj_id=course_id, obj_type='COURSE')
        for career_obj in career_objs:
            career_ids.append(int(career_obj.career_id))
        tmp = [v for v in user_career if v in career_ids]
        if not tmp:
            return failed_json(u'当前课程只有付费学员才能观看')
    teacher = course.teacher
    teacher_info = {
        'teacher_id': teacher.id,
        'teacher_name': teacher.nick_name,
        'teacher_avatar': settings.SITE_URL + settings.MEDIA_URL + str(teacher.avatar_url),
        'teacher_description': teacher.description,
    }

    data = {
        'is_favorite': 1 if user.myfavorite.filter(id=course.id).exists() else 0,
        'course_name': course.name,
        'study_number': course.student_count,
        'teacher_info': teacher_info,
        "img_url": settings.SITE_URL + settings.MEDIA_URL+str(course.image),
        'video_list': []
    }

    lessons = course.lesson_set.all()
    learnings = UserLearningLesson.objects.filter(lesson__in=lessons, is_complete=True, user_id=user.id)
    learning_ids = [learning.lesson_id for learning in learnings]
    for lesson in lessons:
        is_watch = False
        if lesson.id in learning_ids:
            is_watch = True

        data['video_list'].append({
            'video_id': lesson.id,
            'video_name': lesson.name,
            'video_url': lesson.video_url,
            'is_watch': is_watch
        })
    return success_json(data)


# 课程库
def app_course_list(request):
    # 推荐
    recommend_data = recommend_course(request, 1, 10)
    # 最新课程
    if is_ios_check(request):
        result = db.api.common.app.app_course_by_click_or_new_for_ios_check(
                order='date_publish', page_index=1, page_size=10
            )
    else:
        result = db.api.common.app.app_course_by_click_or_new('date_publish', 1, 10)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    course_data = [dict(
            course_id=course['id'],
            course_name=course['name'],
            img_url=settings.SITE_URL + settings.MEDIA_URL + str(course['image']),
            student_count=course['click_count']
            ) for course in result.result()]
    # 企业直通班列表
    if is_ios_check(request):
        result = db.api.common.app.app_direction_career_course_ios_check()
    else:
        result = db.api.common.app.app_direction_career_course(_enable_cache=True)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    career_list = result.result()
    career_data = [dict(
            career_id=career['career_id'],
            career_name=career['career_name'],
            img_url=settings.SITE_URL + settings.MEDIA_URL + str(career['career_image']),
            student_count=career['student_count']
        ) for career in career_list if career['short_name'] != 'business']
    return success_json({'recommend': recommend_data, 'new_course': course_data, 'career_list': career_data})


# 获取更多课程
def app_get_more_course_list(request):
    course_type = request.POST.get('type')
    page = int(request.POST.get('page', 1))
    pagesize = int(request.POST.get('pageSize', 15))
    if course_type == '1':
        data = recommend_course(request, page, pagesize)
        return success_json({'list': data})
    elif course_type == '2':
        if is_ios_check(request):
            result = db.api.common.app.app_course_by_click_or_new_for_ios_check(
                    order='date_publish', page_index=page, page_size=pagesize
                )
        else:
            result = db.api.common.app.app_course_by_click_or_new('date_publish', page, pagesize)
        if result.is_error():
            return failed_json(u'服务器开小差了,稍后再试吧')
        data = [dict(
                course_id=course['id'],
                course_name=course['name'],
                img_url=settings.SITE_URL + settings.MEDIA_URL + str(course['image']),
                student_count=course['click_count']
                ) for course in result.result()]
        return success_json({'list': data})
    else:
        return failed_json(u'课程类型错误')


def filter_career_course(career_course_list_temp):
    career_list = []
    for career_course in career_course_list_temp:

        is_class = False
        classes = Class.objects.xall().filter(career_course_id=career_course.id, lps_version='3.0')
        for cls in classes:
            if (cls.is_active is True) and (cls.is_closed is False) and (cls.status == 1):
                is_class = True
                break
        if not is_class:
            continue
        stages = career_course.stage_set.order_by("index")
        total_courses = 0
        for stage in stages:
            total_courses += Course.objects.filter(stages_m=stage, is_active=True).count()
        if total_courses == 0:
            continue
        if StageTaskRelation.objects.filter(stage__career_course_id=career_course.id).exists():
            career_list.append(career_course)
    return career_list


def app_recommend_course(request):

    recommend_data = recommend_course(request, 1, 10)

    return success_json({'list': recommend_data})


# 推荐课程
def recommend_course(request, page, pagesize):
    career_course_id = None
    if request.user.is_authenticated():
        result = db.api.common.app.app_last_career_course(user_id=request.user.id)
        if not result.is_error():
            user_career = result.result()
            career_course_id = user_career if user_career else None
    if career_course_id:
        result = db.api.common.app.app_course_by_career_id(career_course_id['career_course_id'], page, pagesize)
        if result.is_error():
            return failed_json(u'服务器开小差了,稍后再试吧')
        if not result.result():
            result = db.api.common.app.app_course_by_click_or_new('click_count', page, pagesize)
            if result.is_error():
                return failed_json(u'服务器开小差了,稍后再试吧')
    else:
        if is_ios_check(request):
            result = db.api.common.app.app_course_by_click_or_new_for_ios_check(
                order='click_count', page_index=page, page_size=pagesize
            )
        else:
            result = db.api.common.app.app_course_by_click_or_new('click_count', page, pagesize)
        if result.is_error():
            return failed_json(u'服务器开小差了,稍后再试吧')
    data = [dict(
            course_id=course['id'],
            course_name=course['name'],
            img_url=settings.SITE_URL + settings.MEDIA_URL + str(course['image']),
            student_count=course['click_count']
            ) for course in result.result()]
    return data


# 直通班课程
def app_courses(request):
    career_id = request.POST.get('career_id', None)
    if not career_id:
        return failed_json(u'职业课程ID不能为空')
    data = []
    try:
        career_course = CareerCourse.objects.get(id=career_id)
        stage_list = Stage.objects.filter(career_course=career_course).order_by('index')
        for stage in stage_list:
            course_list = Course.objects.filter(stages_m=stage).order_by('date_publish')
            for course in course_list:
                data.append(dict(
                    course_id=course.id,
                    course_name=course.name,
                    img_url=settings.SITE_URL + settings.MEDIA_URL + str(course.image),
                    student_count=course.student_count
                ))
        return success_json({'list': data})
    except CareerCourse.DoesNotExist:
        return failed_json(u'该职业课程不存在')


# 课程搜索
def app_course_search(request):
    page = int(request.POST.get('page', 1))
    pagesize = int(request.POST.get('pageSize', 15))
    keyword = request.POST.get('keyword', None)
    if keyword is not None and keyword != '':
        if is_ios_check(request):
            courses = Course.objects.filter(Q(name__icontains=keyword) | Q(search_keywords__name__icontains=keyword),
                                            Q(is_click=True)).distinct().exclude(
                                            Q(search_keywords__name__icontains='Android') |
                                            Q(search_keywords__name__icontains='WindowsPhone') |
                                            Q(search_keywords__name__icontains='Windows Phone') |
                                            Q(name__icontains='Android') |
                                            Q(name__icontains='Windows Phone') |
                                            Q(name__icontains='WindowsPhone'))
        else:
            courses = Course.objects.filter(Q(name__icontains=keyword) | Q(search_keywords__name__icontains=keyword),
                                            Q(is_click=True)).distinct()
        totalnum = courses.count()
        courses = courses[(page-1)*pagesize if (page-1)*pagesize < totalnum else totalnum:page*pagesize
                          if page*pagesize < totalnum else totalnum]
        courses_data = [{"course_id": course.id,
                         "course_name": course.name,
                         "img_url": settings.SITE_URL + settings.MEDIA_URL + str(course.image),
                         "student_count": course.student_count} for course in courses]
        career_ourses_data = []
        if page == 1:
            if is_ios_check(request):
                career_courses = CareerCourse.objects.filter(Q(name__icontains=keyword) |
                                                             Q(search_keywords__name__icontains=keyword),
                                                             Q(course_scope=None)).distinct().exclude(
                                                             short_name__icontains='Android')
            else:
                career_courses = CareerCourse.objects.filter(Q(name__icontains=keyword) |
                                                             Q(search_keywords__name__icontains=keyword),
                                                             Q(course_scope=None)).distinct()
            career_courses_list = filter_career_course(career_courses)
            career_ourses_data = [{"career_id": course.id,
                                   "career_name": course.name,
                                   "img_url": settings.SITE_URL + settings.MEDIA_URL + str(course.image),
                                   "student_count": course.student_count} for course in career_courses_list]
        data = {
            "career_course": career_ourses_data,
            "course": courses_data
        }
        return success_json(data)
    else:
        return failed_json(u'关键词不能为空')


# 课程评论
@app_user_required
def app_get_comment_list(request):
    lesson_id = request.POST.get('lessonId')
    # page = request.POST.get('page', 1)
    # page_size = request.POST.get('pageSize', 15)
    form = GetDiscussForm(dict(object_id=lesson_id, object_type='LESSON'))
    if form.is_valid():
        discuss_list = form.get_discuss()
    else:
        return failed_json(form.errors)

    child_discuss_list = []
    parent_discuss_list = []
    data = []
    for discuss in discuss_list:
        if discuss['parent_id']:
            child_discuss_list.append(discuss)
        else:
            parent_discuss_list.append(discuss)
    count = len(parent_discuss_list)
    for discuss in parent_discuss_list:
        child_list = []
        for child_discuss in child_discuss_list:
            if child_discuss['parent_id'] == discuss['id']:
                child_list.append(dict(
                    comment_id=child_discuss['id'],
                    user_id=child_discuss['user_id'],
                    user_name=child_discuss['nick_name'],
                    avatar=settings.SITE_URL + settings.MEDIA_URL + child_discuss['head'],
                    desc=strip_tags(emoji_to_app(child_discuss['comment'])),
                    type=get_user_type(UserProfile.objects.get(pk=child_discuss['user_id'])),
                    date=str(child_discuss['create_date']),
                ))
        data.append(dict(
            comment_id=discuss['id'],
            user_id=discuss['user_id'],
            user_name=discuss['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + discuss['head'],
            desc=strip_tags(emoji_to_app(discuss['comment'])),
            type=get_user_type(UserProfile.objects.get(pk=discuss['user_id'])),
            date=str(discuss['create_date']),
            child_list=child_list
        ))

    return success_json({'list': data, 'comment_count': count})


# 提交课程评论
@app_user_required
def app_submit_comment(request):
    user = request.user
    lesson_id = request.POST.get('lessonId')
    parent_id = request.POST.get('commentId', 0)
    desc = request.POST.get('desc', None)
    if desc is None:
        return failed_json(u'评论内容为空')
    post_data = dict(
        user_id=user.id, nick_name=user.nick_name,
        head=user.avatar_middle_thumbnall, create_date=datetime.datetime.now(),
        parent_id=parent_id, object_id=lesson_id, object_type='LESSON', comment=desc)

    form = DiscussForm(post_data)
    if form.is_valid():
        result = form.save()
        if not result:
            return failed_json(u'保存失败')
        return success_json({})
    return failed_json(form.errors)


# 老师课程
@app_user_required
def app_teacher_course(request):
    teacher_id = request.POST.get('target_id', None)
    if not teacher_id:
        return failed_json(u'ID不能为空')
    try:
        teacher = UserProfile.objects.get(id=teacher_id)
        if not teacher.is_teacher():
            return failed_json(u'目标用户不是老师')
        course_list = Course.objects.filter(teacher=teacher)
        return success_json({'list': [dict(
                                          course_id=course.id,
                                          name=course.name,
                                          img_url=settings.SITE_URL + settings.MEDIA_URL + str(course.image),
                            ) for course in course_list]})
    except UserProfile.DoesNotExist:
        return failed_json(u'老师用户不存在')


# 他的课程
@app_user_required
def app_user_course(request):
    student_id = request.POST.get('target_id', None)
    if not student_id:
        return failed_json(u'目标ID为空')
    class_students = ClassStudents.objects.filter(user_id=student_id)
    career_course_list = []
    for class_student in class_students:
        career = class_student.student_class.career_course
        career_course_list.append({
                "career_id": str(career.id),
                "name": str(career.name),
                "img_url": settings.SITE_URL + settings.MEDIA_URL+str(career.app_career_image),
            })
    return success_json({'list': career_course_list})


# 视频播放
@app_user_required
def app_course_video(request):
    lesson_id = request.POST.get('lesson_id', None)
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return failed_json(u'找不到该章节')
    data = video_detail(request.user, lesson)
    return success_json(data)


# 热门关键字
def app_hot_search(request):
    if is_ios_check(request):
        keywords = RecommendKeywords.objects.using('default').all().exclude(name__icontains='Android')[:10]
    else:
        keywords = RecommendKeywords.objects.using('default').all()[:10]
    keywords = [{"name": keyword.name} for keyword in keywords]
    return success_json({'list': keywords})


# 职业课程详情
def app_career_detail(request):
    career_id = request.POST.get('career_id', None)
    if not career_id:
        return failed_json(u'职业课程不能为空')
    try:
        career_course = CareerCourse.objects.get(id=career_id)
    except CareerCourse.DoesNotExist:
        return failed_json(u'找不到相关职业课程')

    stages = career_course.stage_set.all().order_by("index", "id")
    data = {}
    if stages:
        data = dict(
            career_name=career_course.name,
            desc=career_course.description,
            stage=[dict(
                stage_id=stage.id,
                stage_name=stage.name,
                stage_desc=stage.description,
                list=[dict(
                    course_id=course.id,
                    name=course.name,
                    img_url=settings.SITE_URL + settings.MEDIA_URL + str(course.image),
                    updating=0 if course.is_click else 1
                ) for course in Course.objects.filter(stages_m=stage).order_by("index", "id")]
            ) for stage in stages]
        )
        career_course.click_count += 1
        career_course.save(update_fields=['click_count'])
    return success_json(data)


# 提交支付
@app_user_required
def app_submit_pay(request):
    career_id = request.POST.get('careercourse_id', None)
    pay_type = request.POST.get('pay_type', None)
    class_coding = request.POST.get('class_coding', None)
    service_provider = request.POST.get('service_provider', None)
    if not career_id:
        return failed_json(u'职业课程不能为空')
    if (not pay_type) and (int(pay_type) not in [0, 6]):
        return failed_json(u'支付类型不正确')
    if not class_coding:
        return failed_json(u'班级不能为空')
    if (not service_provider) and (int(service_provider) not in [2, 3]):
        return failed_json(u'支付方式不正确')
    result = db.api.common.app.app_user_class_type(user_id=request.user.id, career_id=career_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    class_type = result.result()
    if class_type['is_normal_class']:
        if class_type['is_full_paid']:
            return failed_json(u'已经报名该课程！')
        else:
            return failed_json(u'您已报名试学,APP不支持余款支付,请到官网进行余款支付')
    return goto_pay(request, career_id, pay_type, class_coding, service_provider, 0)


# app支付
@app_user_required
def app_pay(request):
    user = request.user
    career_id = request.POST.get('ccourse_id', None)
    if not career_id:
        return failed_json(u'职业课程不能为空')
    result = db.api.course.career_course_pay.get_career_course_detail(career_id)
    if result.is_error():
        return failed_json(u'找不到相关职业课程')
    career_course = result.result()
    result = db.api.common.app.app_user_class_type(user_id=user.id, career_id=career_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    class_type = result.result()
    if class_type['is_normal_class']:
        if class_type['is_full_paid']:
            return failed_json(u'已经报名该课程！')
        else:
            return failed_json(u'您已报名试学,APP不支持余款支付,请到官网进行余款支付')
    class_id = NORMAL_CLASS_DICT[int(career_id)]
    try:
        class_obj = Class.objects.xall().get(id=class_id)
    except Class.DoesNotExist:
        return failed_json(u'找不到对应班级')
    result = db.api.course.course_task.get_career_course_knowledge_task_count(career_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    total_num = result.result()
    data = dict(
        course_name=career_course['name'],
        class_name=class_obj.coding,
        total_knowledge=total_num['knowledge_item_count'],
        total_lessons=total_num['knowledge_lesson_count'],
        total_meetings='30+',
        total_practices=total_num['project_count'],
        payment_kinds=[
            {
                "name": "无需保就业",
                "money": career_course['jobless_price'],
                "type": "6"
            },
            {
                "name": "保就业",
                "money": career_course['net_price'],
                "type": "0"
            }
        ],
        payment_types=[{
            "name": "支付宝",
            "type": "2",
            "valid": True
        }, {
            "name": "微信支付",
            "type": "3",
            "valid": False if is_ios_check(request) else True
        }]
    )

    return success_json(data)

    
@app_user_required
def app_snap_project_upload(request):
    res = {
        "msg": ""
    }
    # 更新lps_version值
    try:
        data = json.loads(request.body)
        snap_val = json.loads(data['snap_val'])
        try:
            class_id = int(snap_val['class_id'])
        except KeyError:
            data = request.body
        else:
            if class_id in LPS4_DICT.keys():
                lps_version = 4
            else:
                lps_version = 3
            snap_val.update(dict(lps_version=lps_version))
            snap_val = json.dumps(snap_val)
            data['snap_val'] = snap_val
            data = json.dumps(data)
    except Exception as e:
        log.warn("request snap_service failed. details:%s" % e)
        return failed_json(u'服务器开小差了，请稍后再试')

    try:
        res = requests.post("%s/add/" % settings.SNAP_SERVICE_ADDR, data=data, timeout=2).json()
    except Exception as e:
        log.warn("request snap_service failed. details:%s" % e)
        return failed_json(unicode(res["msg"]))

    log.warn("request snap_service succeed.")
    
    return success_json(res)
