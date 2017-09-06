# -*- coding: utf-8 -*-

__author__ = 'Steven'
from django.db import connection
# from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect
# from datetime import datetime
# from mz_common.models import *
# from mz_user.forms import *
# from mz_course.models import *
# from mz_lps.models import *
# from mz_lps2.models import *
# from mz_common.views import get_course_score
# import json, logging, os, uuid,urllib2,urllib
# from mz_user.models import *
from mz_common.views import *
# import time
# from mz_lps2.calc_view import get_weekdate_bybausertask
from datetime import date
from models import CourseUserTask
import random

logger = logging.getLogger('mz_lps2.chart_view')
#界面图表所需数据

#############################
# 所有私有方法
#############################

# 完成计划图表
def _find_all_week_task(user, clazz):
    '''
    # author:简超
    # function:为完成计划图表提供数据
    # param:user 当前登录的用户
    # return:
    '''
    course_user_task_list = [{"date":"","plan_study_time":0,"real_study_time":0}]
    try:
        if user and clazz:
            course_user_task = CourseUserTask.objects.filter(user = user,user_class = clazz).order_by("create_datetime")   #取出这个用户的所有course_user_task
            if len(course_user_task) > 0:
                course_user_task_list = [{
                    "date":course.create_datetime.strftime('%m/%d'),
                    "plan_study_time":100,
                    "real_study_time":_accomplish_percent(course.plan_study_time,course.real_study_time,course.real_study_time_ext)
                } for course in course_user_task]
        else:
            return HttpResponse("请登录", content_type="application/json")
    except Exception as e:
        logging.error(e)
    return json.dumps(course_user_task_list)

def _accomplish_percent(plan_study_time,real_study_time,real_study_time_ext):
    '''
    # function:计算比率
    # param:plan_study_time  计划学时
    # param:real_study_time  实际学时
    # real_study_time_ext 额外的学时
    '''

    if not real_study_time:
        return 0
    #如果实际完成学时小于计划学时
    if real_study_time < plan_study_time:
        real_extra_study_percent = int(float(real_study_time)/float(plan_study_time)*100)
    elif real_study_time >= plan_study_time:
        real_extra_study_percent = int(float(real_study_time+real_study_time_ext)/float(plan_study_time)*100)
    return real_extra_study_percent


# 截取名字
def _get_split_9(name):
    str1 = name

    try:
        if len(name.decode('utf-8')) > 9:
            str1 = name.decode('utf-8')[:9].encode('utf-8')+"..."
        else:
            str1 = '           ' + str(name.course.name)
    except UnicodeEncodeError:
        str1 = '           ' + name[:9]
    finally:
        return '           '+str1

    return str1


# 评测分数图表
def _find_all_course_score(user,careerscore):
    '''
    # function:评测分数
    # param:user
    # param:careerscore
    # ret :课程名  评测分数
    '''
    #取出职业课程下面的所有课程'

    course_list = _create_lesson_proj_list(careerscore)
    list = []
    try:
        for course_id in course_list:
            course=Course.objects.get(pk=course_id)
            course_score= CourseScore.objects.filter(user = user,course = course)

            if len(course_score) >= 1:
                stage_id = _get_stage_id(course_score[0])
                course_id = course_score[0].course.id
                name = "S"+str(stage_id)+"C"+str(course_id)
                str1 = _get_split_9(course_score[0].course.name)
                this_course_score=0
                if check_exam_is_complete(user, course) == 1:
                    this_course_score=get_course_score(course_score[0])
                    course_score_json = {
                        "course_name_1":name,
                        "course_name":str1,
                        "course_score":this_course_score
                    }
                    list.append(course_score_json)
            # else:
            #     course_score_json = {
            #         "course_name_1": '',
            #         "course_name": '',
            #         "course_score": 0
            #     }
            #     list.append(course_score_json)
    except Exception as e:
        logger.error(e)
    #
    # # for course_score in course_score_list:
    # #     stage_id = _get_stage_id(course_score)
    # #     course_id = course_score.course.id
    # #     name = "S"+str(stage_id)+"C"+str(course_id)
    # #     str1 = _get_split_9(course_score.course.name)
    # #
    # #     course_score_json = {
    # #         "course_name_1":name,
    # #         "course_name":str1,
    # #         "course_score":get_course_score(course_score)
    # #     }
    # #     list.append(course_score_json)
    return json.dumps(list)

def _create_lesson_proj_list(career_course):
    """
    分次创建LESSON_PROJ_LIST（分职业课程）
    {career_id:{stage_id:[course_id,],}}
    """
    local_lesson_proj_list = []
    stage_set = Stage.objects.filter(career_course=\
                                        career_course).order_by('index', 'id')
    for each_stage in stage_set:
        course_set = Course.objects.filter(stages_m=\
                                        each_stage).order_by('index', 'id')
        for each_course in course_set:
            local_lesson_proj_list.append(int(each_course.id))
    return local_lesson_proj_list

def _get_stage_id(course_score):

    if course_score:
        course_obj = course_score.course
        list = course_obj.stages_m.all()
        if len(list) > 0:
            return int(list[0].id)
    return 0

def _check_is_null(variable):
    if variable:
        return variable
    else:
        return 0

# 学力增长曲线图表
def _find_all_study_point(user,clazz):
    '''
    # function:学力增长
    # param: user
    # ret: [{"time":None,"point":None}]
    '''
    if user and clazz:
        course_score_json = [{"date":"", "study_point":0}]
        course_score_list = CourseUserTask.objects.filter(user = user, user_class = clazz).order_by("create_datetime")
        course_score_json = [{
            "date":_course_score_week_startline(get_weekdate_bybausertask(course_score)).strftime("%m/%d"),
            "study_point":int(_check_is_null(course_score.study_point))
        } for course_score in course_score_list]
        return course_score_json

def _course_score_week_startline(startline):
    if startline:
        return startline
    else:
        return datetime.now()

def _three_key_ch(user_quality_list, courseusertask):
    json_arr = {}
    try:
        if (user_quality_list[0].quality_type == 1 and user_quality_list[1].quality_type == 2 and
                    user_quality_list[2].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[0].score)
            json_arr["chart_capacity"] = str(user_quality_list[1].score)
            json_arr["initiative"] = str(user_quality_list[2].score)

        if (user_quality_list[0].quality_type == 1 and user_quality_list[2].quality_type == 2 and
                    user_quality_list[1].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[0].score)
            json_arr["chart_capacity"] = str(user_quality_list[2].score)
            json_arr["initiative"] = str(user_quality_list[1].score)
        if (user_quality_list[1].quality_type == 1 and user_quality_list[0].quality_type == 2 and
                    user_quality_list[2].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[1].score)
            json_arr["chart_capacity"] = str(user_quality_list[0].score)
            json_arr["initiative"] = str(user_quality_list[2].score)
        if (user_quality_list[1].quality_type == 1 and user_quality_list[2].quality_type == 2 and
                    user_quality_list[0].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[1].score)
            json_arr["chart_capacity"] = str(user_quality_list[2].score)
            json_arr["initiative"] = str(user_quality_list[0].score)
        if (user_quality_list[2].quality_type == 1 and user_quality_list[1].quality_type == 2 and
                    user_quality_list[0].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[2].score)
            json_arr["chart_capacity"] = str(user_quality_list[1].score)
            json_arr["initiative"] = str(user_quality_list[0].score)
        if (user_quality_list[2].quality_type == 1 and user_quality_list[0].quality_type == 2 and
                    user_quality_list[1].quality_type == 3):
            json_arr["exe_capacity"] = str(user_quality_list[2].score)
            json_arr["chart_capacity"] = str(user_quality_list[0].score)
            json_arr["initiative"] = str(user_quality_list[1].score)

        json_arr["date"] = courseusertask.create_datetime.strftime('%m/%d')
    except Exception as e:
        print e
        logger.error(e)
    return json_arr

def _calc_stu_radarchart(user,clazz):   #雷达图
    #定义
    user_quality_exe = 0
    user_quality_chat = 0
    user_quality_initiative = 0
    class_meeting_task = ClassMeetingTask.objects.filter(user_class=clazz)
    #执行力
    user_quality_list = UserQualityModelItems.objects.filter(quality_type = 1,user = user,week__in = class_meeting_task).order_by("-id")     #__in  在这个范围
    if user_quality_list:
        user_quality_exe = user_quality_list[0].ava_score
    #沟通力
    user_quality_list = UserQualityModelItems.objects.filter(quality_type = 2,user = user,week__in = class_meeting_task).order_by("-id")     #__in  在这个范围
    if user_quality_list:
        user_quality_chat = user_quality_list[0].ava_score
    #主动性
    user_quality_list = UserQualityModelItems.objects.filter(quality_type = 3,user = user,week__in = class_meeting_task).order_by("-id")     #__in  在这个范围
    if user_quality_list:
        user_quality_initiative = user_quality_list[0].ava_score

    if int(user_quality_exe) == -1:
        user_quality_exe = 0
    if int(user_quality_chat) == -1:
        user_quality_chat = 0
    if int(user_quality_initiative) == -1:
        user_quality_initiative = 0
    json_arr = {}
    json_arr['exe_capacity_alto'] = int(user_quality_exe)
    json_arr['chart_capacity_alto'] = int(user_quality_chat)
    json_arr['initiative_alto'] = int(user_quality_initiative)

    return json.dumps([{'exe_capacity_alto':80,'chart_capacity_alto':80,'initiative_alto':80},json_arr])



# author:简超
# function:取出所有班会的沟通力,执行力,主动性,三项指标汇总  为曲线图提供数据源
# param:
# ret:
def _calc_stu_quality_diff(user, clazz):   #曲线图
    json_list = [{"exe_capacity":0, "chart_capacity":0, "initiative":0}]
    class_meeting_task = ClassMeetingTask.objects.filter(user_class=clazz, is_temp=False).order_by("-id")      #获得这个班的班会集合
    try:
        for i in range(len(class_meeting_task)):
                class_meeting = class_meeting_task[i]
                user_quality_list = UserQualityModelItems.objects.filter(user = user,week = class_meeting)  #三项指标   1,2,3
                if len(user_quality_list) == 3  and i < (len(class_meeting_task)-1):
                     #求时间
                    #if len(CourseUserTask.objects.filter(week=class_meeting_task[i+1], user=user)) < 1:
                    #    continue
                    #获得指定班会之前最近用户课程任务
                    courseusertask = CourseUserTask.objects.filter(week__in=class_meeting_task[i+1:], user=user).order_by("-id")[0]
                    json_arr = _three_key_ch(user_quality_list, courseusertask)
                    json_list.append(json_arr)
    except Exception as e:
        print e
        logger.error(e)

    return sorted(json_list, key=lambda data: data['date'] if data.has_key('date') else 0)      #对字典按照时间进行排序

#获取用户名截取8个体字符
def _get_split_username(username):
    if len(username) > 8:
        return username[:8] + '...  '
    else:
        return username

def _get_key_performance_indicate(student, clazz,  vek_id):
    #如果没有开班会那么就表示用户任务不会关联班会
    if 0==vek_id:
        user_quality_list = CourseUserTask.objects.filter(user_id=student.id,user_class=clazz,week=None)
    else:
        user_quality_list = CourseUserTask.objects.filter(user_id=student.id,user_class=clazz,week_id=vek_id)
    if len(user_quality_list) > 0:
        course_user_task = user_quality_list[0]    #这个学生本周的CourseUserTask
        kpi = _accomplish_percent(course_user_task.plan_study_time,course_user_task.real_study_time,course_user_task.real_study_time_ext)
        if kpi:
            # if kpi > 100:
            #     kpi = 100
            return int(kpi)
        else:
            return 0
    else:
        return 0

#计算所有评测分数平均分
def _get_stu_all_ava_socre(clazz, student):
    course_user_task_list = CourseUserTask.objects.filter(user=student, user_class=clazz)
    if len(course_user_task_list) < 1:
        return 0
    sum = 0
    count = 0
    ava_score = 0
    for course_user_task in course_user_task_list:
        if course_user_task.ava_score == 0:
            count += 1
        sum += course_user_task.ava_score

    if count != 0:
        ava_score = sum / count
    return ava_score

def _get_stu_curweek_all_socre(student):
    ava_score = _get_stu_curweek_ava_score(student)
    study_point = _get_stu_curweek_study_point(student)
    all_score = random.randint(50,99)
    all_score = float(study_point) * 0.1 + float(ava_score) * 0.8
    return int(all_score)


def _get_stu_curweek_ava_score(student):
    cursor = connection.cursor()
    cursor.execute("""
    select max(week_id) from mz_lps2_courseusertask as courseusertask
    INNER JOIN mz_lps2_usertask as usertask on usertask.id =  courseusertask.usertask_ptr_id
    where usertask.user_id = %s
    """, [student.id])
    user_quality_list = None
    user_quality_list = cursor.fetchone()   #取出这个学生最大的周 id
    if user_quality_list[0]:
        #根据这个学生  这个周  取出平均评测分数
        course_user_task = CourseUserTask.objects.filter(user = student,week = int(user_quality_list[0]))
        if len(course_user_task) == 1:
            return int(course_user_task[0].ava_score)
        else:
            return 0
    else:
        return 0

def _get_stu_curweek_study_point(student):
    cursor = connection.cursor()
    cursor.execute("""
    select max(week_id) from mz_lps2_courseusertask as courseusertask
    INNER JOIN mz_lps2_usertask as usertask on usertask.id =  courseusertask.usertask_ptr_id
    where usertask.user_id = %s
    """, [student.id])
    user_quality_list = None
    user_quality_list = cursor.fetchone()
    if user_quality_list[0]:
         #根据这个学生  这个周  取出累计学力
        course_user_task = CourseUserTask.objects.filter(user = student,week = int(user_quality_list[0]))
        if len(course_user_task) >= 1:
            if course_user_task[0].study_point:
                return int(course_user_task[0].study_point)
            else:
                return 0
        else:
            return 0
    else:
        return 0

#############################
# 所有公用方法
#############################
#得到本人的图表数据
def find_self_student_chart(user,clazz,careercourse):
    try:
        if not (user and clazz):
            return HttpResponse("请传入用户和班级对象",content_type="application/json")
        cobweb_json = _calc_stu_radarchart(user,clazz)    #个人素质雷达图返回一个json数据
        different_list = _calc_stu_quality_diff(user,clazz)   #个人素质曲线图返回一个list
        accomplish_percenet_list = _find_all_week_task(user,clazz)        #完成计划曲线图返回一个list
        course_score_list = _find_all_course_score(user,careercourse)                            #评测分数返回一个List
        study_point_list = _find_all_study_point(user, clazz)                  #学力曲线图返回一个list

        #将所有数据全部放到一个字典里面
        total = {}
        total['cobweb_json'] = cobweb_json
        total['different_list'] = different_list
        total['accomplish_percenet_list'] = accomplish_percenet_list
        total['course_score_list'] = course_score_list
        total['study_point_list'] = study_point_list
        return total
    except Exception as e:
        logging.error(e)
        return {}

# 得到整个班级的kpi数据
def find_all_student_progress(clazz, vek_id=0, step=0, n_step=0):
    '''
    # function:本周key performance indicate完成情况
    # param:clazz班级id
    '''
    if not isinstance(clazz,Class):
        clazz = Class.objects.get(id=clazz)

    is_step = [0, 0]     # 是否分页，0为无分页，1有，list长度2
    vek_new_id = 0
    class_start_date = 0    #kpi开始计算时间
    class_end_date = 0
    student_list_json =[]

    try:
        #分页获取数据
        if vek_id != 0 or step != 0:
            class_meeting_list = ClassMeetingTask.objects.filter(user_class=clazz, is_temp=False).order_by('-startline')

            if n_step + 1 < len(class_meeting_list):
                is_step[0] = 1
                if class_meeting_list[n_step + 1].startline:
                    class_start_date = class_meeting_list[n_step + 1].startline.strftime("%Y-%m-%d")
                else:
                    class_start_date = date.today().strftime("%Y-%m-%d")
            else:
                class_start_date = clazz.date_publish.strftime("%Y-%m-%d")

            class_end_date = class_meeting_list[n_step].startline.strftime("%Y-%m-%d")

            if n_step > 0:
                is_step[1] = 1

            if n_step < len(class_meeting_list) - 1 and n_step > -1:
                vek_new_id = list(class_meeting_list)[n_step + 1].id
        else:
            class_meeting_list = ClassMeetingTask.objects.filter(user_class=clazz, is_temp=False).order_by('-startline')
            if len(class_meeting_list) > 1:
                is_step[0] = 1
                if class_meeting_list[1].startline:
                    class_start_date = class_meeting_list[1].startline.strftime("%Y-%m-%d")
                else:
                    class_start_date = date.today().strftime("%Y-%m-%d")
                class_end_date = class_meeting_list[0].startline.strftime("%Y-%m-%d")
                vek_new_id = class_meeting_list[1].id
            elif len(class_meeting_list) == 1:
                class_start_date = clazz.date_publish.strftime("%Y-%m-%d")
                class_end_date = class_meeting_list[0].startline.strftime("%Y-%m-%d")
                # vek_new_id = class_meeting_list[0].id
            else:
                class_start_date = clazz.date_publish.strftime("%Y-%m-%d")
                class_end_date = clazz.date_publish.strftime("%Y-%m-%d")

        if clazz:
            #整个班级学员
            student_list = clazz.students.all()
            student_list_json = [{
                                     "img": student.avatar_small_thumbnall.url,
                                     "name": _get_split_username(student.nick_name),
                                     "kpi": _get_key_performance_indicate(student ,clazz, vek_new_id),
                                     "url": "/lps2/teach/plan/" + str(clazz.id) + '/' + str(student.id) + '/',
                                     "pause": ClassStudents.objects.filter(user=student,student_class=clazz)[0].is_pause
                                 } for student in student_list]

    except Exception as e:
        logging.error(e)
    return student_list_json, is_step, class_start_date, class_end_date


# 获取学生个人学力总和的百分比
def _get_stu_curweek_study_point_all(student, clazz):
    c_u_t_list = CourseUserTask.objects.filter(user=student, user_class=clazz).order_by("-create_datetime")
    count = 0
    for c_u in c_u_t_list:
        count = int(_check_is_null(c_u.study_point))
        if int(_check_is_null(c_u.study_point)) != 0:
            break
    return count

# 得到整个班级排名
def find_all_student_rank(clazz):
    '''
    # function:班级排名
    # 计算公式  : 综合分数 = 学力值 * 10% + 平均评测分数 * 80%
    # 取出的数据:1,累计学力值 2,平均评测分 3,学生名字 4,综合分数
    '''
    student_list_sort = []
    try:
        if clazz:
            #整个班级学员
            student_list = clazz.students.all()
            study_point_count=_get_curweek_study_point_all(clazz)
            student_list_json = [{
                                     "ava_score": _get_stu_curweek_ava_score(student),
                                     "study_point": _get_stu_curweek_study_point_all(student,clazz),
                                     "all_score": _get_stu_curweek_all_socre(student),
                                     "name": _get_split_username(student.nick_name)
                                 } for student in student_list]
        student_list_sort = sorted(student_list_json, key=lambda stu: float(stu['study_point']) * 0.1 + float(stu['ava_score']) * 0.9, reverse=True)
    except Exception as e:
        logging.error(e)
    return student_list_sort,study_point_count

# 获取对应班级的学力总数
#guotao 2015.5.20
def _get_curweek_study_point_all(clazz):
    # 学力总数
    study_point_count = 0
    # class 中 career_course 下所有的 stages
    stages = Stage.objects.filter(career_course=clazz.career_course)
    # stages 下的所有 课程
    courses = Course.objects.filter(stages_m__in=stages.values("id")).order_by("index", "id")
    # 随堂测验学力数
    # 获取有随堂测验的节总数
    for course in courses:
        course_lesson = course.lesson_set.all()
        course_lesson_list = course_lesson.values_list("id")
        # 观看视频学力数
        study_point_count += len(course_lesson_list) * 1
        # 有课后作业学力数
        # study_point_count += len(course_lesson_list) * 1
        study_point_count += course_lesson.filter(have_homework=True).count()
        # 获取有随堂测验的章节总数
        pagers =  Paper.objects.filter(examine_type=2,
                                       relation_type=1,
                                       relation_id__in=course_lesson_list)
        study_point_count += Quiz.objects.filter(paper__in=pagers).count()

        #课程总测验学力数
        study_point_count += Paper.objects.filter(examine_type=2,
                                                        relation_type=2,
                                                        relation_id=course.id).count() * 10

        # 项目制作学力数
        study_point_count += Project.objects.filter(examine_type=5,
                                                        relation_type=2,
                                                        relation_id=course.id).count() * 10
        if study_point_count < 100:
            study_point_count = 100
    return study_point_count

def get_weekdate_bybausertask(usertask_obj):
    """
    根据用户任务对象，获取任务开始时间，即班会时间
    By add guotao 2015.6.18
    :param usertask_obj:
    :return:
    """
    if  usertask_obj.week:
        return usertask_obj.week.startline
    else:
        return  usertask_obj.user_class.date_open
