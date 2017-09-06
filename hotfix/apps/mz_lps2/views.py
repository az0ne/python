# -*- coding: utf-8 -*-
# import json
# from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect, JsonResponse
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt

from django.db.models import Avg
# from mz_common.models import *
from django.shortcuts import redirect
from mz_lps2.serializers import StudentSerializer
# from mz_user.forms import *
# from mz_course.models import *
# from mz_lps.models import *
# from mz_lps2.models import *
# import json, logging, os, uuid,urllib2,urllib
# from mz_user.models import *
# from mz_common.views import *
# from mz_course.views import get_real_amount
from mz_lps4.class_dict import NORMAL_CLASS_DICT
from mz_user.views import sync_avatar # add by humingxing
from django.db.utils import IntegrityError
# import time
# from mz_course.models import Stage
# from mz_course.models import CareerCourse
from chart_view import *
from models import CourseUserTask,ClassMeetingTask
from django.contrib.auth.decorators import login_required
# from mz_common.decorators import student_required, teacher_required, lps_student_teacher_required
from django.views.decorators.csrf import csrf_exempt
from PIL import Image # add by chenyu
import collections, cgi
from datetime import datetime, date # modify by chenyu
# from mz_lps2.signal_view import *
# from mz_lps2.calc_view import get_weekdate_bybausertask
# from django.core.serializers import serialize
#
logger = logging.getLogger('mz_lps2.views')
import traceback

# 老师，学生端都在使用
def is_specific_task( user_task, this_class):
    try:
        this_class.objects.get(pk = user_task.id)
        return True
    except Exception as e:
        return False

def add_attr_joinclass(user_task, career_course):

    join_class_user_task = JoinClassUserTask.objects.filter(id=user_task.id, career_course_id=career_course.id).first()
    if join_class_user_task:
        setattr(user_task, "href", "")  #
        setattr(user_task, "type", "joinclass")
        setattr(user_task, "finish_date",join_class_user_task.finish_date)
    return user_task

def add_attr_viewcontract(user_task, clazz):

    try:
         view_contract_user_task = ViewContractUserTask.objects.get(id = user_task.id)
    except Exception as e:
        print "add_attr",e
        return None
    #根据当前班级查找用户
    if view_contract_user_task.user_class in clazz:
        setattr(user_task, "finish_date", view_contract_user_task.finish_date)
        setattr(user_task, "href", "")
        setattr(user_task, "type", "viewcontract")
    else:
        return None
    return user_task

def add_attr_fullprofile(user_task):
    try:
        full_profile_user_task = FullProfileUserTask.objects.get(id = user_task.id)
    except Exception as e:
        print "add_sttr_full_profile",e
        return None
    setattr(user_task, "finish_date", full_profile_user_task.finish_date)
    setattr(user_task, "href", "")
    setattr(user_task, "type", "fullprofile")
    return user_task

def add_attr_checkcontractusertask(user_task, clazz):
    '''
    查看入学须知任务 zhangyu
    :param user_task:
    :return:
    '''
    try:
        gsut = CheckContractUserTask.objects.get(id=user_task.id)
    except Exception as e:
        print "add_attr_checkcontractusertask", e
        return None
    if gsut.user_class in clazz:
        times = user_task.create_datetime.strftime("%Y-%m-%d")
        setattr(user_task, "type", "checkcontractuser")
        setattr(user_task, "href", "")            #跳转的位置
        setattr(user_task, "title", "点击签署就业服务协议")           #title
        setattr(user_task, "time", times)         #start time
        setattr(user_task, "content", "")
        setattr(user_task, "status", gsut.status)
        return user_task
    return None

def add_attr_givescorestu(user_task,clazz):
    try:
        giveScore_stu = GiveScoreStudentsUserTask.objects.get(id = user_task.id)
    except Exception as e:
        print "add_attr_givescorestu",e
        return None
    if giveScore_stu.week.user_class in clazz:
        setattr(user_task, "create_datetime", giveScore_stu.create_datetime)
        setattr(user_task, "title", "给带班老师评分")
        setattr(user_task, "content", "请对带班老师进行评分，以便给您提供更好的学习指导")
        setattr(user_task, "type", "giveScore_stu")
        return user_task
    return  None

def _set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, is_ext):
    each_course_user_task = {}
    finish_date = this_week_course_list[3]
    each_course_user_task["finish_date"]= finish_date
    each_course_user_task["href"] = "{% url 'lps2.lps2_learning_detail' "+ str(course_user_task.user_class.career_course.id) + " %}"  #
    each_course_user_task["type"] = "course"
    each_course_user_task["title"]= this_week_course_list[2] # 安卓基础开发与环境搭建
    each_course_user_task["text1"]= text1 # 视频观看与随堂作业（1/15）
    each_course_user_task["text2"] =text2 # 项目制作（1/5）
    each_course_user_task["is_ext"] = is_ext # 是否额外任务
    each_course_user_task["create_datetime"]= course_user_task.create_datetime.strftime("%Y-%m-%d %H:%M:%S")
    each_course_user_task["status"] = this_week_course_list[4]
    return each_course_user_task

def save_attr_course(course_user_task):
    create_time = course_user_task.create_datetime
    # 获取职业课程Id
    utl = []
    # is_ext = 0
    # course_t = course_user_task
    # try:
    #     course_user_task_1 = CourseUserTask.objects.get(id = user_task.id)
    #     course_t = course_user_task_1
    # except Exception as e:
    #     print "add_attr_course",e

    course_user_task_list = add_attr_course_child(course_user_task)

    for course_id, this_week_course_list in course_user_task_list.iteritems():
        if this_week_course_list[5] == "init":
            text1 = "视频观看与随堂作业(0/" + str(this_week_course_list[0][1]) + ")"      #视频观看
            text2 = "项目制作(0/" + str(this_week_course_list[1][1]) + ")"          #项目制作
            utl.append(_set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 0))
        else:
            if _is_plan_course(course_id,course_user_task):     #如果是计划内的
                #不是额外任务,但还需判断用户是否完成了这个课程计划之外的章节
                if int(this_week_course_list[0][2]) > 0 or int(this_week_course_list[1][2]) > 0:  #这个计划课程存在额外视频
                    #finish_date = course_user_task[3]
                    text2 = "项目制作(" + str(this_week_course_list[1][2]) + "/ 0 )"          #项目制作
                    text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][2]) + "/ 0 )"      #视频观
                    # user_task["finish_date"]= finish_date
                    # user_task["href"] = "{% url 'lps2.lps2_learning_detail' "+ str(course_user_task.user_class.career_course.id) + " %}"  #
                    # user_task["type"], "course"
                    # user_task["title"]= this_week_course_list[2] # 安卓基础开发与环境搭建
                    # user_task["text1"]= text1 # 视频观看与随堂作业（1/15）
                    # user_task["text2"] =text2 # 项目制作（1/5）
                    # user_task["is_ext"] = 1 # 是否额外任务
                    # user_task["create_datetime"]= create_time
                    utl.append(_set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 1))

                #实际/计划
                text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][0]) + "/" + str(this_week_course_list[0][1]) + ")"      #视频观看
                text2 = "项目制作(" + str(this_week_course_list[1][0]) + "/" + str(this_week_course_list[1][1]) + ")"          #项目制作
                # setattr(user_task, "finish_date", finish_date)
                # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(course_user_task.user_class.career_course.id) + " %}")  #
                # setattr(user_task, "type", "course")
                # setattr(user_task, "title", this_week_course_list[2]) # 安卓基础开发与环境搭建
                # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                # setattr(user_task, "text2", text2) # 项目制作（1/5）
                # setattr(user_task, "is_ext", is_ext) # 是否额外任务
                # setattr(user_task, "create_datetime", create_time)
                utl.append(_set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 0))
            else:
            # 不是计划课程,即这是个额外任务
                text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][2]) + "/ 0 )"      #视频观看
                text2 = "项目制作(" + str(this_week_course_list[1][2]) + "/ 0 )"          #项目制作
                # setattr(user_task, "finish_date", finish_date)
                # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(course_user_task.user_class.career_course.id) + " %}")  #
                # setattr(user_task, "type", "course")
                # setattr(user_task, "title", this_week_course_list[2]) # 安卓基础开发与环境搭建
                # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                # setattr(user_task, "text2", text2) # 项目制作（1/5）
                # setattr(user_task, "is_ext", 1) # 是否额外任务
                # setattr(user_task, "create_datetime", create_time)
                utl.append(_set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 1))

    course_user_task.finish_content= json.dumps(utl)

    course_user_task.save()

def _get_attr_course(user_task, each_course_user_task):
    user_task = UserTask()
    setattr(user_task, "finish_date", each_course_user_task['finish_date'])
    setattr(user_task, "href", each_course_user_task['href']) #
    setattr(user_task, "type", each_course_user_task['type'])
    setattr(user_task, "title",each_course_user_task['title']) # 安卓基础开发与环境搭建
    setattr(user_task, "text1",each_course_user_task['text1']) # 视频观看与随堂作业（1/15）
    setattr(user_task, "text2", each_course_user_task['text2']) # 项目制作（1/5）
    setattr(user_task, "is_ext", each_course_user_task['is_ext']) # 是否额外任务
    setattr(user_task, "create_datetime", datetime.strptime(each_course_user_task['create_datetime'],"%Y-%m-%d %H:%M:%S"))#
    setattr(user_task, "status",each_course_user_task['status'])
    return user_task

#只取本周和上一周
# def find_attr_class2(user_task, career_clazz=[]):
#     try:
#         # course_user_task = CourseUserTask.objects.get(id = user_task.id)
#         course_user_task = CourseUserTask.objects.order_by('-week.create_datetime')[0:2].filter(id = user_task.id)
#         if course_user_task:
#             return user_task
#     except Exception as e:
#         print e
#         return None

def find_attr_class(user_task, career_clazz=[]):
    try:
        course_user_task = CourseUserTask.objects.get(id = user_task.id)

    except Exception as e:
        print e
        logger.error(e)
    utl = []
    try:
        if course_user_task:
            if course_user_task.user_class in career_clazz:
                finish_content=json.loads(course_user_task.finish_content)

                for each_course_user_task in finish_content:
                    user_task = UserTask()
                    utl.append(_get_attr_course(user_task, each_course_user_task))
                return utl
    except Exception as e:
        logging.error(e)
    return utl

def match_task_with_classinfo(user_task, clazz_list, career_id=None ):
    #create_time = user_task.create_datetime
    #获取职业课程Id
    utl = []
    is_ext = 0


    try:
        course_user_task = CourseUserTask.objects.get(id = user_task.id)
        #course_t = course_user_task_1
    except Exception as e:
        print "add_attr_course",e
    if course_user_task.user_class in clazz_list:
        course_user_task_list = add_attr_course_child(course_user_task)
        #YS:给utl赋值stageid属性
        def set_utl_stageid(user_task, course_id, career_id):
            refs = filter(lambda x:x.stage in Stage.objects.filter(career_course_id=career_id),Course_Stages_m.objects.filter(course_id = course_id))
            if not refs:
                return user_task
            stage_id = refs[0].stage_id
            setattr(user_task,"stage_id",stage_id)
            return user_task

        for course_id, this_week_course_list in course_user_task_list.iteritems():
            if this_week_course_list[5] == "init":
                #finish_date = course_user_task[3]
                text1 = "视频观看与随堂作业("+str(this_week_course_list[0][0])+"/" + str(this_week_course_list[0][1]) + ")"      #视频观看
                text2 = "项目制作("+str(this_week_course_list[1][0])+"/" + str(this_week_course_list[1][1]) + ")"          #项目制作
                if _filter_str(text1):
                    text1 = ""
                if _filter_str(text2):
                    text2 = ""
                # setattr(user_task, "finish_date", finish_date)
                # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(career_course.id) + " %}")  #
                # setattr(user_task, "type", "course")
                # setattr(user_task, "title", course_user_task[2]) # 安卓基础开发与环境搭建
                # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                # setattr(user_task, "text2", text2) # 项目制作（1/5）
                # setattr(user_task, "is_ext", 0) # 是否额外任务
                # setattr(user_task, "create_datetime", create_time)
                # setattr(user_task, "status", course_user_task[4])
                each_course_user_task = _set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 0)
                utl.append(set_utl_stageid(_get_attr_course(user_task, each_course_user_task),course_id,career_id))
            else:
                if _is_plan_course(course_id,course_user_task):     #如果是计划内的
                    #不是额外任务,但还需判断用户是否完成了这个课程计划之外的章节
                    if int(this_week_course_list[0][2]) > 0 or int(this_week_course_list[1][2]) > 0:  #这个计划课程存在额外视频
                        #finish_date = course_user_task[3]
                        text2 = "项目制作(" + str(this_week_course_list[1][2]) + "/0 )"          #项目制作
                        text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][2]) + "/0 )"      #视频观
                        if _filter_str(text1):
                            text1 = ""
                        if _filter_str(text2):
                            text2 = ""
                        # setattr(user_task, "finish_date", finish_date)
                        # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(career_course.id) + " %}")  #
                        # setattr(user_task, "type", "course")
                        # setattr(user_task, "title", course_user_task[2]) # 安卓基础开发与环境搭建
                        # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                        # setattr(user_task, "text2", text2) # 项目制作（1/5）
                        # setattr(user_task, "is_ext", 1) # 是否额外任务
                        # setattr(user_task, "create_datetime", create_time)
                        # setattr(user_task, "status", course_user_task[4])
                        each_course_user_task = _set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 1)



                        utl.append(set_utl_stageid(_get_attr_course(user_task, each_course_user_task),course_id,career_id))

                    #实际/计划
                    user_task = UserTask()
                    #finish_date = course_user_task[3]
                    text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][0]) + "/" + str(this_week_course_list[0][1]) + ")"      #视频观看
                    text2 = "项目制作(" + str(this_week_course_list[1][0]) + "/" + str(this_week_course_list[1][1]) + ")"          #项目制作
                    if _filter_str(text1):
                        text1 = ""
                    if _filter_str(text2):
                        text2 = ""
                    # setattr(user_task, "finish_date", finish_date)
                    # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(career_course.id) + " %}")  #
                    # setattr(user_task, "type", "course")
                    # setattr(user_task, "title", course_user_task[2]) # 安卓基础开发与环境搭建
                    # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                    # setattr(user_task, "text2", text2) # 项目制作（1/5）
                    # setattr(user_task, "is_ext", is_ext) # 是否额外任务
                    # setattr(user_task, "create_datetime", create_time)
                    # setattr(user_task, "status", course_user_task[4])
                    each_course_user_task = _set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 0)
                    utl.append(set_utl_stageid(_get_attr_course(user_task, each_course_user_task),course_id,career_id))
                else:
                # 不是计划课程,即这是个额外任务
                    user_task = UserTask()
                    #finish_date = course_user_task[3]
                    text1 = "视频观看与随堂作业(" + str(this_week_course_list[0][2]) + "/0 )"      #视频观看
                    text2 = "项目制作(" + str(this_week_course_list[1][2]) + "/0 )"          #项目制作
                    if _filter_str(text1):
                        text1 = ""
                    if _filter_str(text2):
                        text2 = ""
                    # setattr(user_task, "finish_date", finish_date)
                    # setattr(user_task, "href", "{% url 'lps2.lps2_learning_detail' "+ str(career_course.id) + " %}")  #
                    # setattr(user_task, "type", "course")
                    # setattr(user_task, "title", course_user_task[2]) # 安卓基础开发与环境搭建
                    # setattr(user_task, "text1", text1) # 视频观看与随堂作业（1/15）
                    # setattr(user_task, "text2", text2) # 项目制作（1/5）
                    # setattr(user_task, "is_ext", 1) # 是否额外任务
                    # setattr(user_task, "create_datetime", create_time)
                    # setattr(user_task, "status", course_user_task[4])
                    each_course_user_task = _set_attr_course(text1, text2, course_user_task, this_week_course_list, course_id, 1)
                    utl.append(set_utl_stageid(_get_attr_course(user_task, each_course_user_task),course_id,career_id))

        # save_attr_course(course_user_task)
    return utl


def _filter_str(text):
    if "(0/0" in text:
        return True
    else:
        return False

# 这个课程是否是额外任务
def _is_plan_course(course_id,course_user_task):
    content = json.loads(course_user_task.relate_content)
    p_keys = content["P"].keys()
    v_keys = content["V"].keys()
    p_keys.extend(v_keys)
    for course_id_1 in p_keys:
        if int(course_id) == int(course_id_1):
            return True
    return False


def check_lesson_done(user, lesson, existing_ele=None):
    """
    检查章节视频是否完成
    """
    if existing_ele == "video": # 视频默认已观看
        # 判断该章节是否有课后作业
        if lesson.have_homework:
            try:
                homework = Homework.objects.get(examine_type=1, relation_type=1,\
                                               relation_id=lesson.id)
            except:
                return True
            else:
                try:
                    homework_record = HomeworkRecord.objects.filter(homework=homework, student=user)
                except Exception, e:
                    if settings.DEBUG == True:
                        print e
                        assert False
                    else:
                        logger.error(e)
                        return False
                return homework_record and True or False
        else:
            return True
    elif existing_ele == "homework": # 默认课后作业已上传
        try:
            user_learning_lesson = UserLearningLesson.objects.get(user=user, lesson=lesson)
        except:
            return False
        return user_learning_lesson.is_complete and True or False
    else:
        try:
            user_learning_lesson = UserLearningLesson.objects.get(user=user, lesson=lesson)
        except:
            return False
        if not user_learning_lesson.is_complete:
            return False
        else:
            # 判断该章节是否有课后作业
            if lesson.have_homework:
                try:
                    homework = Homework.objects.get(examine_type=1, relation_type=1,\
                                                   relation_id=lesson.id)
                except:
                    return True
                else:
                    try:
                        homework_record = HomeworkRecord.objects.filter(homework=homework, student=user)
                    except Exception, e:
                        if settings.DEBUG == True:
                            print e
                            assert False
                        else:
                            logger.error(e)
                            return False
                    return homework_record and True or False
            else:
                return True

def add_attr_course_child(course_user_task):

    # CourseUserTask
    if not course_user_task:
        return []
    lesson_list = []

    proj_real_num = 0
    proj_extra_num = 0

    c_u_task_object = course_user_task
    learning_plan = {}
    user = course_user_task.user
    if not c_u_task_object.relate_content:
        return learning_plan
    content = json.loads(c_u_task_object.relate_content)
    print "content_lins",content
    lesson_list_v = []
    lesson_list_p = []
    for course_id, lessons_set_v in content["V"].iteritems():     #多个课程
        lesson_list_v.extend(lessons_set_v)
    for course_id, lessons_set_p in content["P"].iteritems():
        lesson_list_p.extend(lessons_set_p)
#{u'P': {}, u'V': {u'176': [1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320], u'175': [1306, 1307, 1308, 1309, 1310]}}
#{176L: [[0, 10, 0], [0, 0, 0], u'windows phone 8\u5e94\u7528\u5f00\u53d1\u91cd\u70b9\u96be\u70b9', '2015-05-06', 2, 'init'], 175L: [[0, 10, 7], [0, 0, 0], u'windows phone 8\u5e94\u7528\u5f00\u53d1\u6982\u8981', '2015-05-06', 2, '']}

    try:
        course_task_done_set = CourseTaskDone.objects.filter(course_user_task=c_u_task_object,relate_type = 1)
    except Exception as e:
        print e
        logger.error(e)
    #######################################################################视频
    for course_task_done in course_task_done_set:
        done_lesson_num = 0
        extra_lesson_num = 0
        # if course_task_done.relate_type == 1:
        try:
            lesson = Lesson.objects.get(pk = int(course_task_done.relate_id))
        except Exception as e:
            print e
            logger.error(e)
            continue
        # if check_lesson_done(user, lesson, 'video'):
        # if not (lesson.id in lesson_list):
        #     lesson_list.append(lesson.id)
        if course_task_done.relate_id in lesson_list_v:       #是否是计划任务
            done_lesson_num = 1
        elif not (course_task_done.relate_id in lesson_list_v):
            extra_lesson_num = 1


        if learning_plan.has_key(str(lesson.course.id)):    #视频观看  [实际完成,计划完成,额外完成]
            done_lesson_num += int(learning_plan[str(lesson.course.id)][0][0])
            extra_lesson_num += int(learning_plan[str(lesson.course.id)][0][2])
            learning_plan[str(lesson.course.id)][0][0] =  done_lesson_num
            learning_plan[str(lesson.course.id)][0][2] =  extra_lesson_num

        else:
            learning_plan[str(lesson.course.id)] = [[done_lesson_num, 0, extra_lesson_num], [0, 0, 0], lesson.course.name,
                            get_weekdate_bybausertask(c_u_task_object).strftime("%Y-%m-%d"), _get_real_coursestatus(user,lesson.course,c_u_task_object.status), ""]

    #如果循环了,还需判断计划任务课程的是否存在于learning_plan
    for course_id, lessons_set in content["V"].iteritems():
        try:
            course = Course.objects.get(pk = course_id)
        except Exception as e:
            print e
            logger.error(e)
            continue
        if learning_plan.has_key(str(course_id)):
            learning_plan[str(course_id)][0][1] = len(lessons_set)
        else:
            learning_plan[str(course_id)] = [[0, len(lessons_set), 0], [0, 0, 0], course.name,
                get_weekdate_bybausertask(c_u_task_object).strftime("%Y-%m-%d"), _get_real_coursestatus(user,course,c_u_task_object.status), "init"]



##########################################################################项目
    course_task_done_set = CourseTaskDone.objects.filter(course_user_task=c_u_task_object, relate_type = 3)
    for course_task_done in course_task_done_set:
        proj_extra_num = 0
        proj_real_num = 0
        try:
            project_record = ProjectRecord.objects.get(pk = course_task_done.relate_id)
            course = Course.objects.get(pk = project_record.project.relation_id)
        except Exception as e:
            print e
            logger.error(e)
            continue

        if project_record.project.id in lesson_list_p:       #不是额外
            proj_real_num = 1
        else:
            proj_extra_num = 1

        if learning_plan.has_key(str(course.id)):    #项目制作  [实际完成,计划完成,额外完成]
            proj_real_num += int(learning_plan[str(course.id)][1][0])
            learning_plan[str(course.id)][1][0] = proj_real_num

            proj_extra_num += int(learning_plan[str(course.id)][1][2])
            learning_plan[str(course.id)][1][2] = proj_extra_num
        else:
            learning_plan[str(course.id)] = [[0, 0, 0],
                                    [proj_real_num,
                                     0,
                                     proj_extra_num],
                                    course.name,
                                    get_weekdate_bybausertask(c_u_task_object).strftime("%Y-%m-%d"),
                                    _get_real_coursestatus(user,course,c_u_task_object.status), ""]


    for course_id, lessons_set_p in content["P"].iteritems():
        try:
            course = Course.objects.get(pk = int(course_id))
        except Exception as e:
            print e
            logger.error(e)
            continue
        if learning_plan.has_key(str(course.id)):    #项目制作  [实际完成,计划完成,额外完成]
            learning_plan[str(course.id)][1][1] = len(lessons_set_p)
        else:
            learning_plan[str(course_id)] = [[0, 0, 0], [0, len(lessons_set_p), 0], course.name,
                get_weekdate_bybausertask(c_u_task_object).strftime("%Y-%m-%d"), _get_real_coursestatus(user,course,c_u_task_object.status), ""]

    print "learning_plan",learning_plan
    return learning_plan

def _get_real_coursestatus(user,course,task_status):
    '''
    获取课程用户的实际状态(Lps优化--2.1.2学习完成度计算优化-guotao 2015.6.29)
    --对于已经通过的课程我们需要将未完成（0）改变为已经完成（1）
    '''
    result=False
    if check_exam_is_complete(user, course) == 1:
        try:
            rebuild_count = get_rebuild_count(user, course.id)
            course_score = CourseScore.objects.filter(user=user, course=course.id, rebuild_count=rebuild_count)
        except Exception,e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e)
        if course_score!=[] and get_course_score(course_score[0],course) >= 60:
            result=True
    if result and task_status == 0:
        return 1
    else:
        return task_status

# 老师、学生端都要使用
def insert_classmeeting_in_list(class_meeting, user_task_show_list, career_course, user):
    setattr(class_meeting, "type", "classmeeting")
    try:
        live_room = LiveRoom.objects.get(live_class=class_meeting.user_class)
    except Exception, e:
        if settings.DEBUG:
            print e
            pass
        else:
            logger.error(e)
            pass
    else:
        if user.is_teacher():
            setattr(class_meeting, "join_url", live_room.teacher_join_url)
            setattr(class_meeting, "token", live_room.teacher_token)
        else:
            setattr(class_meeting, "join_url", live_room.student_join_url)
            setattr(class_meeting, "token", live_room.student_client_token)
        setattr(class_meeting, "nick_name", user.nick_name)

    # 判断班会是否在当前职业课程下
    if class_meeting.user_class.career_course == career_course:
        # 插入班会到指定的位置
        index = 0
        for each_task in user_task_show_list:
            if class_meeting.create_datetime >= each_task.create_datetime:
                break
            index += 1
        try:
            user_task_show_list.insert(index, class_meeting)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e)
                return False
    return True

def acquire_user_task(user_task_list, career_course,clazz):
    utl_man=[]#主要数据
    utl_new = []  # 其他数据(用来保存任务未完成时，课程以及考核通过的情况)

    need_complete_profile = False
    need_complete_checkcontract = False
    for user_task in user_task_list:
        if is_specific_task(user_task ,JoinClassUserTask):
            utl_man.append(add_attr_joinclass(user_task, career_course))
        elif is_specific_task(user_task ,ViewContractUserTask):
            user_task = add_attr_viewcontract(user_task,clazz)
            if user_task is not None:
                utl_man.append(user_task)
        elif clazz and is_specific_task(user_task ,FullProfileUserTask):
            need_complete_profile = True
            utl_man.append(add_attr_fullprofile(user_task))
        elif is_specific_task(user_task ,CourseUserTask):
            if user_task.status ==2:#进行中
            # if _get_cur_user_task_id(user_task):
                utl_man.extend(match_task_with_classinfo(user_task, clazz, career_course.id))
            if user_task.status ==1:#已完成
                utl_man.extend(find_attr_class(user_task,clazz))
            if user_task.status ==0:#未完成：需要内部区分课程完成情况（#Lps优化--2.1.2学习完成度计算优化-guotao 2015.6.29）
            # course_user_task = CourseUserTask.objects.order_by('-week.create_datetime')[0:2].get(id=user_task.id)
                if clazz:
                    course_user_task = CourseUserTask.objects.filter(id=user_task.id)
                    if course_user_task:
                        cmts = ClassMeetingTask.objects.filter(user_class=clazz[0], is_temp=False).order_by('-create_datetime')
                        if len(cmts) > 2:
                            cmt = []
                            if cmts[0].status == 2:
                                cmt = [c for c in cmts][0:2]
                            else:
                                cmt = [c for c in cmts][1:3]
                            if course_user_task[0].week not in cmt:
                                continue
                                # course_user_task = None
                tmp_utl = find_attr_class(user_task,clazz)
                for tmp_user_task in tmp_utl:
                    if tmp_user_task.status==1:
                        utl_new.append(tmp_user_task)
                    else:
                            utl_man.append(tmp_user_task)
        elif is_specific_task(user_task, CheckContractUserTask):
            user_task = add_attr_checkcontractusertask(user_task,clazz)
            if user_task is not None:
                utl_man.append(user_task)
                need_complete_checkcontract = True
        
        elif is_specific_task(user_task,GiveScoreStudentsUserTask):
            user_task=add_attr_givescorestu(user_task,clazz)
            if user_task is not None:
                utl_man.append(user_task)
    return need_complete_profile, utl_man, utl_new, need_complete_checkcontract

#
# def _get_cur_user_task_id(user_task):
#     course_user_task_num = 0
#     try:
#         course_user_task_num = CourseUserTask.objects.filter(id = user_task.id, status = 2).count()
#     except Exception as e:
#         print e
#         logger.error(e)
#     return course_user_task_num == 1


# 老师，学生端都要用，取单个学生的图表数据
def create_chart_data(user, cur_careercourse):
# 加入班级的同学能够看到更多的内容
    user_chart_data={}
    user_chart_data['is_lock_screen'] = True

    #个人素质雷达图返回一个json数据

    user_chart_data['cobweb_json'] = \
        [{
             'chart_capacity_alto': 60, # 汇总的沟通能力数值
             'exe_capacity_alto': 80, # 汇总的执行能力数值
             'initiative_alto': 90 #汇总的主动性数值
         },{
             'chart_capacity_alto': 40, # 汇总的沟通能力数值
             'exe_capacity_alto': 50, # 汇总的执行能力数值
             'initiative_alto': 58 # 汇总的主动性数值
         }]


    #个人素质曲线图返回一个list
    user_chart_data['different_list'] = \
        [{
             'chart_capacity': 50,
             'exe_capacity': 80,
             'initiative': 60,
             'date':'04/06'
         },{
             'chart_capacity': 53,
             'exe_capacity': 90,
             'initiative': 58,
             'date':'04/13'
         },{
             'chart_capacity': 50,
             'exe_capacity': 80,
             'initiative': 62,
             'date':'04/13'
         },{
             'chart_capacity': 53,
             'exe_capacity': 80,
             'initiative': 60,
             'date':'04/13'
         },{
             'chart_capacity': 50,
             'exe_capacity': 82,
             'initiative': 70,
             'date':'04/13'
         },{
             'chart_capacity': 55,
             'exe_capacity': 80,
             'initiative': 80,
             'date':'04/13'
         },{
             'chart_capacity': 50,
             'exe_capacity': 80,
             'initiative': 90,
             'date':'04/13'
         },{
             'chart_capacity': 55,
             'exe_capacity': 84,
             'initiative': 100,
             'date':'04/13'
         },{
             'chart_capacity': 50,
             'exe_capacity': 80,
             'initiative': 90,
             'date':'04/13'
         },{
             'chart_capacity': 55,
             'exe_capacity': 84,
             'initiative': 100,
             'date':'04/13'
         },{
             'chart_capacity': 50,
             'exe_capacity': 80,
             'initiative': 90,
             'date':'04/13'
         },{
             'chart_capacity': 55,
             'exe_capacity': 84,
             'initiative': 100,
             'date':'04/13'
         }]


    #完成计划曲线图返回一个list
    user_chart_data['accomplish_percenet_list'] = \
        [{
             'date': '04/01',
             'plan_study_time': 40,
             'real_study_time': 80
         },{
             'date': '04/02',
             'plan_study_time': 43,
             'real_study_time': 75
         },{
             'date': '04/03',
             'plan_study_time': 45,
             'real_study_time': 80
         },{
             'date': '04/04',
             'plan_study_time': 45,
             'real_study_time': 80
         },{
             'date': '04/05',
             'plan_study_time': 43,
             'real_study_time': 80
         },{
             'date': '04/06',
             'plan_study_time': 50,
             'real_study_time': 80
         },{
             'date': '04/07',
             'plan_study_time': 70,
             'real_study_time': 90
         },{
             'date': '04/08',
             'plan_study_time': 105,
             'real_study_time': 100
         },{
             'date': '04/05',
             'plan_study_time': 43,
             'real_study_time': 80
         },{
             'date': '04/06',
             'plan_study_time': 80,
             'real_study_time': 80
         },{
             'date': '04/07',
             'plan_study_time': 70,
             'real_study_time': 90
         },{
             'date': '04/08',
             'plan_study_time': 95,
             'real_study_time': 100
         }]

    # 获得评测分数
    user_chart_data['course_score_list'] = \
        [{
             'course_name': 'IOS基础',
             'course_score':60
         },{
             'course_name': 'Android基础',
             'course_score':90
         },{
             'course_name': 'PHP基础',
             'course_score':40
         },{
             'course_name': 'Javascript',
             'course_score':65
         },{
             'course_name': '艺术设计',
             'course_score':30
         },{
             'course_name': 'PHP基础',
             'course_score':40
         },{
             'course_name': 'Javascript',
             'course_score':65
         },{
             'course_name': '艺术设计',
             'course_score':30
         }]

    #学力增长
    user_chart_data['study_point_list'] = \
        [{
             'date' : '04/01',
             'study_point' : 35
         },{
             'date' : '04/02',
             'study_point' : 40
         },{
             'date' : '04/03',
             'study_point' : 45
         },{
             'date' : '04/04',
             'study_point' : 50
         },{
             'date' : '04/05',
             'study_point' : 55
         },{
             'date' : '04/06',
             'study_point' : 65
         },{
             'date' : '04/07',
             'study_point' : 85
         },{
             'date' : '04/08',
             'study_point' : 120
         },{
             'date' : '04/07',
             'study_point' : 180
         },{
             'date' : '04/08',
             'study_point' : 260
         }]


    user_class_list = ClassStudents.objects.filter(user = user).values("student_class")

    cobweb_json = []
    different_list = []
    accomplish_percenet_list =[]
    course_score_list = []
    study_point_list = []
    if len(user_class_list) > 0:
        #如果同学加入的班级和目前进入的职业课程一致，显示对应的数据
        class_list = Class.objects.filter(students = user, career_course = cur_careercourse)

        if len(class_list) > 0:
            course_list = CourseUserTask.objects.filter(user = user,user_class = class_list[0],status = 2).order_by("-id")
            if len(course_list) > 0:
                user_chart_data['is_lock_screen'] = False
                temp = find_self_student_chart(user,class_list[0],cur_careercourse)
                user_chart_data['cobweb_json'] = temp['cobweb_json'] # calc_stu_radarchart(user,clazz)    #个人素质雷达图返回一个json数据
                user_chart_data['different_list'] = temp['different_list'] # calc_stu_quality_diff(user,clazz)   #个人素质曲线图返回一个list
                user_chart_data['accomplish_percenet_list'] = temp['accomplish_percenet_list'] # find_all_week_task(user)        #完成计划曲线图返回一个list
                user_chart_data['course_score_list'] = temp['course_score_list'] # find_all_course_score(user,careercourse)  #评测分数返回一个List
                user_chart_data['study_point_list'] = temp['study_point_list'] # find_all_study_point(user) #学力增长
                return user_chart_data
            else:
                user_chart_data['cobweb_json'] = [{
                    'chart_capacity_alto': 80, # 汇总的沟通能力数值
                    'exe_capacity_alto': 80, # 汇总的执行能力数值
                    'initiative_alto': 80 #汇总的主动性数值
                }]
                user_chart_data['different_list'] = [{
                    'chart_capacity': 0,
                    'exe_capacity': 0,
                    'initiative': 0,
                    'date': ''
                    }]
                user_chart_data['accomplish_percenet_list'] = [{}]
                user_chart_data['course_score_list'] = [{
                        'course_name': '          ',
                        'course_score':0
                    }]
                user_chart_data['study_point_list'] = [{
                        'date' : '',
                        'study_point' : -1
                    }]
                user_chart_data['is_lock_screen'] = False
                return user_chart_data
    return 0

def filter_week(utl,career_clazz):

    for user_task in utl:
        if career_clazz and user_task.type=='course':
            try:
                course_user_task = CourseUserTask.objects.get(id=user_task.id)
                if course_user_task.week not in ClassMeetingTask.objects.filter(user_class=career_clazz[0]).order_by('-create_datetime')[2:4]:
                    #course_user_task = None
                    utl.remove(user_task)
            except Exception as e:
                print e
    return utl

@csrf_exempt
def student_class_view(request, careercourse_id):
    '''
    # function:渲染学生页面
    # param:careercourse_id 职业课程id
    # ret:careercourse_id 职业课程id
    '''
    user = request.user
    cur_careercourse = None    # 当前职业课程
    # cur_stage = None       # 当前阶段
    # cur_class = None       # 当前班级
    # cur_careercourse_stage_list = []   # 当前职业课程阶段列表

    if not user.is_authenticated() or not user.is_student():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})

    # 获取当前职业课程对象
    try:
        cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except CareerCourse.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该职业课程'})
    #获取当前学生所在的班级 add guotao
    clazz = Class.objects.xall().filter(
        students=user, career_course=cur_careercourse, class_type=Class.CLASS_TYPE_NORMAL)


    # lps3.1修改
    if clazz and clazz[0].lps_version == '3.0':
        current_class_id = clazz[0].id
        # 如果班级id在NORMAL_CLASS_DICT里，则跳lps4页面
        if current_class_id in NORMAL_CLASS_DICT.values():
            return redirect(reverse('lps4_index', kwargs=dict(career_id=clazz[0].career_course_id)))
        # 否则跳lps3页面
        else:
            return redirect(reverse("lps3:student_class", kwargs=dict(class_id=current_class_id)))

    if not clazz:
        return render(request, 'mz_common/failure.html',{'reason':'支付未完成, 请重新支付'})
    need_complete_profile = False
    # 得到未完成的任务,
    user_task_show_list = []
    # 得到已完成的任务,
    user_task_finish_list = []
    #进行中
    user_task_list = UserTask.objects.filter(user = user, status = 2).order_by("-id")
    need_complete_profile, user_task_show_list, _, need_complete_checkcontract = acquire_user_task(user_task_list,cur_careercourse,clazz)
    #已经完成
    user_task_lists = UserTask.objects.filter(user = user, status = 1).order_by("-id")
    user_task_list = []
    #add by yuanming, check if there are two CheckContractUserTask
    for user_task_lis in user_task_lists:
        if is_specific_task(user_task_lis, CheckContractUserTask):
            check_contracts = CheckContractUserTask.objects.filter(user=user, user_class=clazz).order_by('-create_datetime')
            if check_contracts:
                if not check_contracts[0].create_datetime == user_task_lis.create_datetime:
                    continue
        user_task_list.append(user_task_lis)
    _,user_task_finish_list,_, _ = acquire_user_task(user_task_list, cur_careercourse,clazz)
    #未完成
    user_task_list = UserTask.objects.filter(user = user, status = 0).order_by("-id")
    _,user_task_list,user_task_list_new, _ = acquire_user_task(user_task_list, cur_careercourse,clazz)
    # user_task_list = filter_week(clazz,user_task_list)
    user_task_show_list.extend(user_task_list)
    #未完成中已完成的课程需要显示在最前面
    user_task_list_new.extend(user_task_finish_list)
    user_task_finish_list=user_task_list_new
    # 加入班级的同学能够看到更多的内容
    is_lock_screen = False

    # 整体数据
    data_all_stu = \
        {'real_extra_study_percent':80,
          'is_pause':'正常',
          'class_sort_stu':3,
          'total_study_time':250,
          'plan_gradute_time':'10/4/2014',
        }

    #个人素质雷达图返回一个json数据

    cobweb_json = \
        [{
             'chart_capacity_alto': 60, # 汇总的沟通能力数值
         'exe_capacity_alto': 80, # 汇总的执行能力数值
    'initiative_alto': 90 #汇总的主动性数值
    },{
        'chart_capacity_alto': 40, # 汇总的沟通能力数值
    'exe_capacity_alto': 50, # 汇总的执行能力数值
    'initiative_alto': 58 # 汇总的主动性数值
    }]



    #个人素质曲线图返回一个list
    different_list = \
        [{
         'chart_capacity': 50,
         'exe_capacity': 80,
         'initiative': 60,
         'date':'04/06'
    },{
         'chart_capacity': 53,
         'exe_capacity': 90,
         'initiative': 58,
         'date':'04/13'
    },{
         'chart_capacity': 50,
         'exe_capacity': 80,
         'initiative': 62,
         'date':'04/13'
    },{
         'chart_capacity': 53,
         'exe_capacity': 80,
         'initiative': 60,
         'date':'04/13'
    },{
         'chart_capacity': 50,
         'exe_capacity': 82,
         'initiative': 70,
         'date':'04/13'
    },{
         'chart_capacity': 55,
         'exe_capacity': 80,
         'initiative': 80,
         'date':'04/13'
    },{
         'chart_capacity': 50,
         'exe_capacity': 80,
         'initiative': 90,
         'date':'04/13'
    },{
         'chart_capacity': 55,
         'exe_capacity': 84,
         'initiative': 100,
         'date':'04/13'
    },{
         'chart_capacity': 50,
         'exe_capacity': 80,
         'initiative': 90,
         'date':'04/13'
    },{
         'chart_capacity': 55,
         'exe_capacity': 84,
         'initiative': 100,
         'date':'04/13'
    },{
         'chart_capacity': 50,
         'exe_capacity': 80,
         'initiative': 90,
         'date':'04/13'
    },{
         'chart_capacity': 55,
         'exe_capacity': 84,
         'initiative': 100,
         'date':'04/13'
    }]


    #完成计划曲线图返回一个list
    accomplish_percenet_list = \
    [{
         'date': '04/01',
         'plan_study_time': 40,
         'real_study_time': 80
    },{
         'date': '04/02',
         'plan_study_time': 43,
         'real_study_time': 75
    },{
         'date': '04/03',
         'plan_study_time': 45,
         'real_study_time': 80
    },{
         'date': '04/04',
         'plan_study_time': 45,
         'real_study_time': 80
    },{
         'date': '04/05',
         'plan_study_time': 43,
         'real_study_time': 80
    },{
         'date': '04/06',
         'plan_study_time': 50,
         'real_study_time': 80
    },{
         'date': '04/07',
         'plan_study_time': 70,
         'real_study_time': 90
    },{
         'date': '04/08',
         'plan_study_time': 105,
         'real_study_time': 100
    },{
         'date': '04/05',
         'plan_study_time': 43,
         'real_study_time': 80
    },{
         'date': '04/06',
         'plan_study_time': 80,
         'real_study_time': 80
    },{
         'date': '04/07',
         'plan_study_time': 70,
         'real_study_time': 90
    },{
         'date': '04/08',
         'plan_study_time': 95,
         'real_study_time': 100
    }]

    # 获得评测分数
    course_score_list = \
        [{
               'course_name': 'IOS基础',
                              'course_score':60
    },{
          'course_name': 'Android基础',
          'course_score':90
      },{
          'course_name': 'PHP基础',
          'course_score':40
      },{
          'course_name': 'Javascript',
          'course_score':65
      },{
          'course_name': '艺术设计',
          'course_score':30
      },{
          'course_name': 'PHP基础',
          'course_score':40
      },{
          'course_name': 'Javascript',
          'course_score':65
      },{
          'course_name': '艺术设计',
          'course_score':30
      }]

    #学力增长
    study_point_list = \
        [{
         'date' : '04/01',
         'study_point' : 35
    },{
         'date' : '04/02',
         'study_point' : 40
    },{
         'date' : '04/03',
         'study_point' : 45
    },{
         'date' : '04/04',
         'study_point' : 50
    },{
         'date' : '04/05',
         'study_point' : 55
    },{
         'date' : '04/06',
         'study_point' : 65
    },{
         'date' : '04/07',
         'study_point' : 85
    },{
         'date' : '04/08',
         'study_point' : 120
    },{
         'date' : '04/07',
         'study_point' : 180
    },{
         'date' : '04/08',
         'study_point' : 260
    }]

    # 获取课程加锁和解锁状态，包括体验到期时间 add by humingxing
    setattr(cur_careercourse, "is_unlock", False)   # 职业课程是否解锁，默认未解锁
    setattr(cur_careercourse, "deadline", None)   # 职业课程解锁的到期时间
    # clazz = Class.objects.filter(students=user, career_course=cur_careercourse)
    if len(clazz) < 1:
        is_lock_screen = True
    else:
        class_students_list = ClassStudents.objects.filter(user=user, student_class=clazz[0], student_class__career_course=cur_careercourse)
        if len(class_students_list) < 1:
            is_lock_screen = True
        else:
            #判断这个用户是否解锁这个职业课程下面的所有阶段
            careercourse_stages = cur_careercourse.stage_set.all().order_by("index", "id")
            user_unlock_stages = UserUnlockStage.objects.filter(user=user, stage=careercourse_stages)
            if class_students_list[0].deadline is None or len(careercourse_stages) == len(user_unlock_stages):
                cur_careercourse.is_unlock = True
            else:
                cur_careercourse.deadline = class_students_list[0].deadline

    user_class_list = ClassStudents.objects.filter(user = user).values("student_class")

    cobweb_json = []
    different_list = []
    accomplish_percenet_list =[]
    course_score_list = []
    study_point_list = []
    if len(user_class_list) > 0:
        #获取该生加入班级的时间
        class_meeting_list = ClassMeetingTask.objects.filter(user_class__in = user_class_list, status__in = [0,2])
        for class_meeting in class_meeting_list:
            #暂停的班级用户，不在能看到直播班会任务
            user_class=ClassStudents.objects.filter(student_class=class_meeting.user_class,user=user)
            if user_class and user_class[0].is_pause:
                pass
            else:
                insert_classmeeting_in_list(class_meeting, user_task_show_list, cur_careercourse, request.user)
                if class_meeting.content is None:
                    class_meeting.content = "周直播班会"

        class_meeting_list = ClassMeetingTask.objects.filter(user_class__in = user_class_list, status = 1)
        for class_meeting in class_meeting_list:
            insert_classmeeting_in_list(class_meeting, user_task_finish_list, cur_careercourse, request.user)
            if class_meeting.content is None:
                class_meeting.content = "周直播班会"

        # #如果同学加入的班级和目前进入的职业课程一致，显示对应的数据
        # class_list = Class.objects.filter(students = user, career_course = cur_careercourse)

        if len(clazz) > 0:
            temp = all_data(user,clazz[0])
            if temp:
                data_all_stu = temp

                all_user_data = find_self_student_chart(user,clazz[0],cur_careercourse)

                cobweb_json = all_user_data['cobweb_json'] # calc_stu_radarchart(user,clazz)    #个人素质雷达图返回一个json数据
                different_list = all_user_data['different_list'] # calc_stu_quality_diff(user,clazz)   #个人素质曲线图返回一个list

                accomplish_percenet_list = all_user_data['accomplish_percenet_list'] # find_all_week_task(user)        #完成计划曲线图返回一个list
                course_score_list = all_user_data['course_score_list'] # find_all_course_score(user,careercourse)  #评测分数返回一个List
                study_point_list = all_user_data['study_point_list'] # find_all_study_point(user) #学力增长
            else:
                course_score_list = [{
                        'course_name': '          ',
                        'course_score':0
                    }]
                different_list = [{
                    'chart_capacity': 0,
                    'exe_capacity': 0,
                    'initiative': 0,
                    'date':''
                    }]
                study_point_list = [{
                        'date' : '',
                        'study_point' : -1
                    }]
                data_all_stu = \
                    {'real_extra_study_percent':0,
                    'is_pause':'正常',
                    'class_sort_stu':0,
                    'total_study_time':0,
                    'plan_gradute_time':'xx/xx/xxxx',
                    }
                cobweb_json = [{
                     'chart_capacity_alto': 0, # 汇总的沟通能力数值
                    'exe_capacity_alto': 0, # 汇总的执行能力数值
                    'initiative_alto': 0 #汇总的主动性数值
                    }]
                accomplish_percenet_list = \
                    [{
                    'date': '',
                    'plan_study_time': 0,
                    'real_study_time': 0
                     }]

    # data_all_stu['real_extra_study_percent'] = 100-data_all_stu['real_extra_study_percent'] if data_all_stu['real_extra_study_percent'] < 100 else 0
    # data_all_stu['real_extra_study_percent'] = str(data_all_stu['real_extra_study_percent']) + '%'
    # data_all_stu['real_extra_study_percent_over'] = data_all_stu['real_extra_study_percent'] if data_all_stu['real_extra_study_percent'] < 100 else 0
    # data_all_stu['real_extra_study_percent_over'] = str(data_all_stu['real_extra_study_percent_over']) + '%'



    return render(request, "mz_lps2/learning_data.html",
                  {'cur_careercourse':cur_careercourse,
                   'class_coding': clazz[0].coding if len(clazz) > 0 else cur_careercourse.name,
                   'user_task_list':user_task_show_list,
                   'user_task_finish_list':user_task_finish_list,
                   'overview_data':data_all_stu,
                   'need_complete_profile':need_complete_profile,
                   'need_complete_checkcontract': need_complete_checkcontract,
                   'is_look_screen':is_lock_screen,
                   'cobweb_json':cobweb_json,
                   'different_list':different_list,
                   'accomplish_percenet_list':accomplish_percenet_list,
                   'course_score_list':course_score_list,
                   'study_point_list': study_point_list,
                   })

@csrf_exempt
def student_class_data_view(request, careercourse_id):

    user = request.user
    cur_careercourse = None    # 当前职业课程

    if not user.is_authenticated() or not user.is_student():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})

    # 获取当前职业课程对象
    try:
        cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except CareerCourse.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该职业课程'})


    # 加入班级的同学能够看到更多的内容
    is_lock_screen = True
    this_week = None
    last_week_date = ""
    this_week_kpi_list= \
    [{
         'name':'姚 No.3',
         'kpi':100,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.2',
         'kpi':90,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.4',
         'kpi':80,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.5',
         'kpi':70,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.1',
         'kpi':60,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.6',
         'kpi':53,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.7',
         'kpi':45,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.1',
         'kpi':36,
         'img' : '/static/lps2/images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.6',
         'kpi':30,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.7',
         'kpi':25,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.1',
         'kpi':20,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.6',
         'kpi':17,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.7',
         'kpi':14,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.1',
         'kpi':12,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.6',
         'kpi':10,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    },{
         'name':'姚 No.7',
         'kpi':8,
         'img' : 'images/photo.jpg',
         'url' : 'teacher-2.html'
    }]

    rank_in_class = \
        [{
             'name':'限制六个汉字',
             'study_point':150,
             'ava_score':90
         },{
             'name':'限制六个汉字',
             'study_point':80,
             'ava_score':60
         },{
             'name':'限制六个汉字',
             'study_point':50,
             'ava_score':70
         },{
             'name':'姚 No.2',
             'study_point':55,
             'ava_score':60
         },{
             'name':'姚 No.1',
             'study_point':50,
             'ava_score':40
         },{
             'name':'姚 No.6',
             'study_point':30,
             'ava_score':25
         },{
             'name':'姚No.7',
             'study_point':25,
             'ava_score':20
         },{
             'name':'姚No.7',
             'study_point':25,
             'ava_score':17
         },{
             'name':'姚No.7',
             'study_point':18,
             'ava_score':15
         },{
             'name':'姚No.7',
             'study_point':17,
             'ava_score':13
         },{
             'name':'姚No.7',
             'study_point':15,
             'ava_score':10
         },{
             'name':'姚No.7',
             'study_point':12,
             'ava_score':10
         },{
             'name':'姚No.7',
             'study_point':8,
             'ava_score':5
         }]
    chart_maxvalue = 100
    #如果同学加入的班级和目前进入的职业课程一致，显示对应的数据
    class_list = Class.objects.filter(students = user, career_course = cur_careercourse)
    cur_class = None
    cm_list = None
    is_step = 0
    class_start_date = None
    class_end_date = None
    if len(class_list) > 0:
        is_lock_screen =False
        cm_list = ClassMeetingTask.objects.filter(user_class = class_list[0])
        cur_class= class_list[0]
        if len(cm_list)>0:
            this_week = cm_list[0]
        if len(cm_list)>1:
            last_week_date = str(cm_list[1].real_start_date)

        this_week_kpi_list, is_step, class_start_date, class_end_date = find_all_student_progress(class_list[0])
        for this_week_kpi_temp in this_week_kpi_list:
            this_week_kpi_temp['url'] = ''
        rank_in_class,chart_maxvalue = find_all_student_rank(class_list[0])
        this_week = cm_list[0]
    else:
        this_week = ClassMeetingTask(id=-1)

    # is_step = [1, 0]
    live_room = LiveRoom.objects.filter(live_class=cur_class)
    auth_token=''
    last_class_videos = []
    video_list = []
    if live_room:
        live_room = live_room[0]
        auth_token = live_room.student_token
        last_class_videos = ClassMeetingTaskVideo.objects.filter(live_room=live_room).order_by('-create_time')
        month_dict = {}
        for video in last_class_videos:
            month = video.create_time.month
            if month in month_dict:
                month_dict[month].append(video)
            else:
                month_dict[month] = [video]

        video_list = collections.OrderedDict(sorted(month_dict.items()))

    
    return render(request, "mz_lps2/learning_data_class.html",
                  {'cur_careercourse':cur_careercourse,
                   'this_week_kpi_list':json.dumps(this_week_kpi_list),
                   'rank_in_class':json.dumps(rank_in_class),
                   'chart_maxvalue':chart_maxvalue,
                   'is_lock_screen':is_lock_screen,
                   'this_week':this_week,
                   'last_week_date':last_week_date,
                   'classmeeting_count': len(cm_list) if cm_list is not None else 0,
                   'cur_class':cur_class,
                   'is_step': is_step,
                   'class_start_date': class_start_date,
                   'class_end_date': class_end_date,
                   'this_week': this_week,
                   'last_class_videos':video_list,
                   'auth_token':auth_token
                   })


# 验证用户身份
@csrf_exempt
def another_week_data_get(request,class_id):

    user = request.user
    cur_class = None    # 当前职业课程

    if not user.is_authenticated() or not user.is_student():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})

    # 获取当前职业课程对象
    try:
        cur_class = Class.objects.get(pk = class_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except Class.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该班级'})

    try:
        week_id = request.REQUEST.get('week_id')
        step = int(request.REQUEST.get('step'))
        n_step = int(request.REQUEST.get('n_step'))

        that_week_kpi_list= \
        [{
             'name':'姚 No.3',
             'kpi':100,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.12',
             'kpi':90,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.4',
             'kpi':80,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.5',
             'kpi':70,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.1',
             'kpi':60,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.6',
             'kpi':53,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.7',
             'kpi':45,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.1',
             'kpi':36,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.6',
             'kpi':30,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.7',
             'kpi':25,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.1',
             'kpi':20,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.6',
             'kpi':17,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.7',
             'kpi':14,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.1',
             'kpi':12,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.6',
             'kpi':10,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         },{
             'name':'姚 No.7',
             'kpi':8,
             'img' : 'images/photo.jpg',
             'url' : 'teacher-2.html'
         }]
        that_week_kpi_list, is_step, class_start_date, class_end_date = find_all_student_progress(cur_class, week_id, step, n_step) #, week_id, step)
        # is_step = [0, 1]
        # return HttpResponse('{"status":"success","message":'+json.dumps(that_week_kpi_list)+',"is_step":'+json.dumps(is_step)+'}', content_type='application/json')
        return HttpResponse('{"status":"success","is_step":'+json.dumps(is_step)+
                            ',"message":'+json.dumps(that_week_kpi_list)+
                            ',"class_start_date":"'+class_start_date+
                            '","class_end_date":"'+class_end_date+'"}',content_type='application/json')

    except Exception as e:
        logger.error(e)
        return HttpResponse('{"status":"failure","message":"发生异常"}', content_type="application/json")

# author: zhangyu
# function: 处理入学协议用户任务
# param:
# ret:
@login_required
@csrf_exempt
def check_contract_handler(request):
    if request.method == 'POST':
        careercourse_id = request.POST['careercourse_id']
        try:
            career_course = CareerCourse.objects.get(id=int(careercourse_id))
            user_class = Class.objects.get(career_course=career_course, students=request.user)
            check_contract_user_tasks = CheckContractUserTask.objects\
                        .filter(user=request.user, user_class=user_class)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                return HttpResponse("{'message':'failure'}", content_type="application/json")
        #modified by yuanming
        for check_contract_user_task in check_contract_user_tasks:
            if check_contract_user_task.status != 1:
                check_contract_user_task.status = 1
                check_contract_user_task.finish_date = date.today()
                check_contract_user_task.save()
        return HttpResponse("{'message':'success'}", content_type="application/json")
    else:
        return HttpResponse("{'message':'failure'}", content_type="application/json")

# author: chenyu
# function: 处理学生协议查看任务
# param:
# ret:
@login_required
@csrf_exempt
def student_contract_handler(request):
    if request.method == 'POST':
        careercourse_id = request.POST['careercourse_id']
        try:
            career_course = CareerCourse.objects.get(id=int(careercourse_id))
            user_class = Class.objects.get(career_course=career_course, students=request.user)
            view_contract_user_task = ViewContractUserTask.objects\
                        .filter(user=request.user, user_class=user_class)[0]
            class_stu = ClassStudents.objects.get(user=request.user, student_class=user_class)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                return HttpResponse("{'message':'failure'}", content_type="application/json")
        if view_contract_user_task.status != 1:
            view_contract_user_task.status = 1
            view_contract_user_task.finish_date = date.today()
            view_contract_user_task.save()
            class_stu.is_view_contract = True
            class_stu.save()
        return HttpResponse("{'message':'success'}", content_type="application/json")
    else:
        return HttpResponse("{'message':'failure'}", content_type="application/json")

# function: 处理学生个人资料完成任务
# param:
# ret:
@login_required(login_url="/")
@csrf_exempt
def student_profile_handler(request):
    try:
        if request.method == 'POST':
            user = request.user
            try:
                stu_profile_task = FullProfileUserTask.objects.filter(user=user)[:1]
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    return HttpResponse("{'message':'failure'}", content_type="application/json")

            if stu_profile_task:
                valid_msg = None
                avatar = request.POST.get('Filedata_hidden', None)
                real_name = request.POST.get('real_name', None)
                # description = request.POST.get('description', None)
                study_goal = request.POST.get('study_goal', None)
                study_base = request.POST.get('study_base',None)
                goal_text = request.POST.get('goal_text',None)
                base_text = request.POST.get('base_text',None)

                if avatar is None or avatar == "":
                    valid_msg = {'avatar': '必须选择头像'}
                elif real_name is None or real_name == "":
                    valid_msg = {'real_name': '真实姓名不能为空'}
                elif len(real_name) > 10:
                    valid_msg = {'real_name': '真实姓名长度不能超过10个字符'}
                # if study_goal is None or study_goal == "":
                #     valid_msg = {'study_goal': '学习目标不能为空'}
                # if len(study_goal) > 100:
                #     valid_msg = {'study_goal': '学习目标长度不能超过100个字符'}
                # elif description is None or description == "":
                #     valid_msg = {'description': '个人介绍不能为空'}
                # elif len(description) > 500:
                #     valid_msg = {'description': '个人介绍不能超过500字符'}
                #学习目标
                if str(study_goal) == "其他":
                    if goal_text is None or goal_text == "":
                        valid_msg = {'goal_text': '学习目标不能为空'}
                    if len(goal_text) > 20:
                        valid_msg = {'goal_text': '学习目标长度不能超过20个字符'}
                    user.study_goal = goal_text
                else:
                    user.study_goal = study_goal
                study_goal_opt = None
                try:
                    study_goal_opt = StudyGoal.objects.get(name=study_goal)
                except Exception as e:
                    logger.error(e)
                user.study_goal_opt = study_goal_opt
                #学生基础
                if str(study_base) == "其他":
                    if base_text is None or base_text == "":
                        valid_msg = {'base_text': '学习目标不能为空'}
                    if len(base_text) > 20:
                        valid_msg = {'base_text': '学习目标长度不能超过20个字符'}
                    user.study_base = base_text
                else:
                    user.study_base = study_base
                study_base_opt = None
                try:
                    study_base_opt = StudyBase.objects.get(name=study_base)
                except Exception as e:
                    logger.error(e)
                user.study_base_opt = study_base_opt

                if valid_msg is not None:
                    return HttpResponse(json.dumps(valid_msg), content_type="application/json")

                # 更新个人资料
                user.nick_name = real_name
                user.save()
                # 裁切头像
                # 如果是默认头像不进行头像裁切处理
                if request.user.avatar_middle_thumbnall.url.find(avatar) == -1:
                    avatar_crop(request)
                stu_profile_task[0].finish_date = date.today()
                stu_profile_task[0].status = 1
                stu_profile_task[0].save()
                return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except IntegrityError:
        return HttpResponse('{"real_name":"昵称（姓名）不能重复"}', content_type="application/json")
    except Exception as e:
        print e
        logger.error(e)
    return HttpResponse(json.dumps({'status': 'failure'}), content_type="application/json")

# 个人资料 - 头像裁切
@login_required(login_url="/")
def avatar_crop(request):

    marginTop=0      # 缩放后图片距离裁切框的上边距
    marginLeft=0     # 缩放后图片距离裁切框的左边距
    width=0          # 裁切框宽度
    height=0         # 裁切框高度
    zoompicheight=0  # 缩放后图片显示的高度
    zoompicwidth=0   # 缩放后图片显示的宽度

    if request.POST.get('marginTop'):
        marginTop=abs(int(request.POST.get('marginTop')))
    if request.POST.get('marginLeft'):
        marginLeft=abs(int(request.POST.get('marginLeft')))
    if request.POST.get('boxwidth'):
        width=abs(int(request.POST.get('boxwidth')))
    if request.POST.get('boxheight'):
        height=abs(int(request.POST.get('boxheight')))
    if request.POST.get('zoompicheight'):
        zoompicheight=abs(int(request.POST.get('zoompicheight')))
    if request.POST.get('zoompicwidth'):
        zoompicwidth=abs(int(request.POST.get('zoompicwidth')))

    avatar_up_small = ""   #upload Thumbnail
    avatar_target_path = ""
    avatar_middle_target_path = ""
    avatar_small_target_path = ""
    try:
        # 获取头像临时图片名称
        avatar_tmp = request.session.get("avatar_tmp",None)
        source_path = os.path.join(settings.MEDIA_ROOT,'temp',avatar_tmp)
        avatar_up_small = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_thumbnail.jpg"
        avatar_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_big.jpg"
        avatar_middle_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_middle.jpg"
        avatar_small_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_small.jpg"
        f = Image.open(source_path)
        f.resize((zoompicwidth, zoompicheight), Image.ANTIALIAS).save(avatar_up_small, 'jpeg', quality=100)
        ft = Image.open(avatar_up_small)
        box = (marginLeft, marginTop, marginLeft+width, marginTop+height)
        ft.crop(box).resize((220, 220), Image.ANTIALIAS).save(avatar_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((104, 104), Image.ANTIALIAS).save(avatar_middle_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((70, 70), Image.ANTIALIAS).save(avatar_small_target_path, 'jpeg', quality=100)

        # 读取原来的头像信息并删除
        if str(request.user.avatar_url).count('/')>1 and avatar_tmp != str(request.user.avatar_url).split("/")[-1] :
            avatar_url_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_url)
            avatar_middle_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_middle_thumbnall)
            avatar_small_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_small_thumbnall)
            if os.path.exists(avatar_url_path) :
                os.remove(avatar_url_path)
            if os.path.exists(avatar_middle_thumbnall_path) :
                os.remove(avatar_middle_thumbnall_path)
            if os.path.exists(avatar_small_thumbnall_path) :
                os.remove(avatar_small_thumbnall_path)
    except Exception as e:
        logger.error(e)

    # 将裁切后的图片路径信息更新图片字段
    request.user.avatar_url = avatar_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.avatar_middle_thumbnall = avatar_middle_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.avatar_small_thumbnall = avatar_small_target_path.split("..")[-1].replace('/uploads','').replace('\\','/')[1:]
    request.user.save()

    if request.user.uid:
        sync_avatar(request.user.uid, avatar_target_path)

    return {"status": "success"}

# 学生端的学生详情
#@student_required
def student_detail_view(request, careercourse_id):
    result = None
    try:
        user = request.user
        stage_id = request.GET.get('stage_id', None)
        result = careercourse_detail_new(user, careercourse_id, stage_id)
        # 为暂时解决用户角色信息反复读取问题，加的用户权限判断方式
        if request.user.is_student():
            result['user_role'] = 'student'
        if 'status' in result and result['status'] == 'error':
            return render(request, 'mz_common/failure.html', {'reason': result['data']})
    except Exception as e:
        pass
        # 20160324 解决报错(用错误来控制只能是学生进入页面,却把错误写在日志里,不应该)
        # logger.error(e)
    return render(request, 'mz_lps2/learning_data_student_detail_new.html', result)


def careercourse_stage_handler(request, careercourse_id, stage_id, user_id):
    """
    获取职业课程的阶段信息
    :param request:
    :param careercourse_id:
    :param stage_id:
    :param user_id:
    :return:
    """
    result = {}
    try:
        user = UserProfile.objects.get(pk=user_id)
        cur_careercourse = get_cur_careercourse(user, careercourse_id)

        cur_stage = Stage.objects.get(pk=stage_id)

        # 获取该职业课程下所有阶段信息
        cur_careercourse_stage_list = list(cur_careercourse.stage_set.all().order_by("index", "id").values_list("id"))

        # 获取当前阶段的前后阶段的ID
        setattr(cur_stage, "prev_stage", None)   # 默认前面已没有阶段
        setattr(cur_stage, "next_stage", None)   # 默认后面已没有阶段
        cur_stage_index = cur_careercourse_stage_list.index((cur_stage.id,))
        if cur_stage_index - 1 >= 0:
            cur_stage.prev_stage = cur_careercourse_stage_list[cur_stage_index - 1][0]

        if cur_stage_index + 1 <= len(cur_careercourse_stage_list)-1:
            cur_stage.next_stage = cur_careercourse_stage_list[cur_stage_index + 1][0]
        from serializers import StageSerializer,CareerCourseSerializer
        result = {'status':'success',
                'cur_careercourse': CareerCourseSerializer(cur_careercourse).data,
                'cur_stage': StageSerializer(cur_stage).data}
    except Exception as e:
        logger.error(e)
        result['status'] = 'fail'
        result['message'] = '系统出现异常'

    return JsonResponse(result)


def stage_course_handler(request, careercourse_id, stage_id, user_id):
    """
    获取该阶段的课程信息
    :param request:
    :param stage_id:
    :return:
    """
    result = {}
    cur_stage_course_list = []
    try:
        user = UserProfile.objects.get(pk=user_id)
        cur_careercourse = get_cur_careercourse(user, careercourse_id)
        cur_stage_course_list = get_stage_course(user, cur_careercourse, stage_id)
    except:
        tb = traceback.format_exc()
        print tb
        logger.error(tb)

    result['cur_stage_course_list'] = []
    from serializers import CourseSerializer,CareerCourseSerializer
    # 序列化并拼接字符串
    for course in cur_stage_course_list:
        serializer = CourseSerializer(course)
        result['cur_stage_course_list'].append(serializer.data)
    if request.user.is_student():
        result['user_role'] = "student"
    else:
        result['user_role'] = "teacher"
    result['student'] = StudentSerializer(user).data
    result['cur_careercourse'] = CareerCourseSerializer(cur_careercourse).data
    return JsonResponse(result)

def _check_finish(lesson_id,student):
    '''
    # function:判断这个Lesson是否完成
    # param:lesson_id
    # ret: true false
    '''
    #判断这个章节是否有随堂作业
    try:
        homework = Homework.objects.filter(examine_type=1, relation_type=1,\
                                           relation_id=lesson_id)
    except Exception,e:
        return False

    if not homework:        #没有随堂作业
        return True
    else:                   #有随堂作业
        #这个学生是否完成随堂作业
        try:
            homework_record = HomeworkRecord.objects.filter(\
            homework=homework[0], student=student).order_by('-id')
        except Exception,e:
            return False
        if len(homework_record) > 0:
            return True

# def req_join_clazz(user):
#     arr = {}
#      #学生加入班级任务
#     print "学生id",user.id
#     join_class_user_task_1 = JoinClassUserTask.objects.filter(user = user,status = 2)
#     if len(join_class_user_task_1) >= 1:
#         join_class_user_task = {}
#         join_class_user_task['title'] = '<a href="http://www.baidu.com">报名班级</a>'
#         join_class_user_task['content'] = '报名以后可以享受企业开发人员指导,真实项目制作,学员交流及就业保障'
#         join_class_user_task['start_time'] = join_class_user_task_1[0].startline.strftime("%Y-%m-%d")
#         join_class_user_task['status'] = join_class_user_task_1[0].status
#         arr['join_class_user_task'] = join_class_user_task
#     return arr
# def all_task_view(user,clazz):
#     '''
#     # function:获取当前学生未完成的任务
#     # param:stu 学生  status :0,"未完成"),(1,"已完成"),(2,"进行中"
#     # param:clazz
#     '''
#     arr = {}
#     #判断用户是否加入这个职业课程对应的班级
#     if user in clazz.students.all():
#         print "ccccccccccccccccccccc"
#         #学生班会任务
#         class_meeting_task_1 = ClassMeetingTask.objects.filter(user_class = clazz).exclude(status = 1).order_by("-id")
#         if len(class_meeting_task_1) >= 1:
#             class_meeting_task = {}
#             class_meeting_task['title'] = class_meeting_task_1[0].content
#             if class_meeting_task_1[0].startline:
#                 class_meeting_task['start_time'] = class_meeting_task_1[0].startline.strftime('%Y-%m-%d')
#                 class_meeting_task['start_time_hms'] = class_meeting_task_1[0].startline.strftime('%H:%M:%S')
#                 class_meeting_task['status'] = class_meeting_task_1[0].status
#                 arr['class_meeting_task'] = class_meeting_task
#         #学生完善资料任务
#         full_profile_user_task_1 = FullProfileUserTask.objects.filter(user = user).exclude(status = 1)
#         if len(full_profile_user_task_1) >= 1:
#             full_profile_user_task = {}
#             full_profile_user_task['title'] = '完善个人资料'
#             full_profile_user_task['content'] = '请快去晚上您的个人资料,以便于老师更好的与您交流,沟通'
#             full_profile_user_task['start_line'] = full_profile_user_task_1[0].startline.strftime("%Y-%m-%d")
#             full_profile_user_task['status'] = full_profile_user_task_1[0].status
#             arr['full_profile_user_task'] = full_profile_user_task
#
#         #学生查看协议任务
#         view_contract_user_task_1 = ViewContractUserTask.objects.filter(user = user,user_class = clazz).exclude(status = 1)
#         if len(view_contract_user_task_1) >= 1:
#             view_contract_user_task = {}
#             view_contract_user_task['title'] = '查看学习协议'
#             view_contract_user_task['content'] = '请快去了解学习协议,关于您的学习期间的一些规定,以及您以后就业保障的达成'
#             view_contract_user_task['start_time'] = view_contract_user_task_1[0].startline.strftime("%Y-%m-%d")
#             view_contract_user_task['status'] = view_contract_user_task_1[0].status
#             arr['view_contract_user_task'] = view_contract_user_task
#         #学生课程任务
#
#         try:
#             course_user_task_list = CourseUserTask.objects.filter(user = user,user_class = clazz).exclude(status = 1)  #排除1
#         except Exception as msg:
#             print "course_user_task-->",msg
#         learning_plan_list = _course_user_task_unfinish(course_user_task_list,user)
#         arr['learning_plan_list'] = learning_plan_list
#
#     return arr

# def _get_stu_overview():
#     pass
# def _get_task_list():
#     pass

# 整体数据
def all_data(user,clazz):
    data_all_stu = {}
    if user and clazz:
        course_list = CourseUserTask.objects.filter(user = user,user_class = clazz,status = 2).order_by("-id")
        if len(course_list) > 0:
            course = course_list[0]
            #计划学时
            plan_study_time = course.plan_study_time
            #实际学时
            real_study_time = course.real_study_time
            #超额学时
            real_study_time_ext = course.real_study_time_ext

            #班级排名
            class_sort_stu = course.rank_in_class
            #本周任务完成度
            #如果实际完成学时小于计划学时
            if plan_study_time != 0:    # 如果为0已经毕业
                if real_study_time < plan_study_time:
                    real_extra_study_percent = int(float(real_study_time)/float(plan_study_time)*100)
                elif real_study_time >= plan_study_time:
                    real_extra_study_percent = int(float(real_study_time+real_study_time_ext)/float(plan_study_time)*100)
            else:
                real_extra_study_percent = 100
            #是否暂停学习
            class_student = ClassStudents.objects.filter(user=user, student_class=clazz)[0]
            if class_student.is_pause:
                is_pause = '暂停'
            else:
                is_pause = '正常'


            #预计毕业日期
            plan_gradute_time = course.plan_gradute_time
            if plan_gradute_time:
                data_all_stu['plan_gradute_time'] = plan_gradute_time.strftime("%m/%d/%Y")
            else:
                data_all_stu['plan_gradute_time'] = datetime.now().strftime("%m/%d/%Y")
            data_all_stu['total_study_time'] = int(course.total_study_time)
            data_all_stu['class_sort_stu'] = int(class_sort_stu)
            data_all_stu['real_extra_study_percent'] = real_extra_study_percent
            data_all_stu['is_pause'] = is_pause
            return data_all_stu
    return 0


def careercourse_detail_new(user, careercourse_id, stage_id):
    cur_careercourse = None    # 当前职业课程
    cur_stage = None       # 当前阶段
    cur_stage_course_list = []   # 当前阶段课程列表
    user_class = None
    try:
        # 获取当前职业课程对象
        cur_careercourse = get_cur_careercourse(user, careercourse_id)

        # 获取该职业课程下所有阶段信息
        cur_careercourse_stage_list = list(cur_careercourse.stage_set.all().order_by("index", "id").values_list("id"))
        if len(cur_careercourse_stage_list) == 0:
            return {'status': 'error', 'data': '该课程还没有阶段信息'}

        # 获取课程加锁和解锁状态

        class_students = ClassStudents.objects.filter(user=user, student_class__career_course=cur_careercourse)
        if len(class_students) > 0:
            user_class = class_students[0].student_class

        # 获取当前正在看哪个学习阶段
        if stage_id is None:
            # 获取正在进行中的课程所对应的阶段
            stagelist = cur_careercourse.stage_set.all()
            courselist = Course.objects.filter(stages_m__in=stagelist)
            recent_learned_lesson = UserLearningLesson.objects.filter(user=user,
                                                                      lesson__course__in=courselist).order_by("-date_learning")
            if recent_learned_lesson:
                # 同一职业课程下如果有两个阶段都包括该课程，会出现多条记录
                cur_stage = recent_learned_lesson[0].lesson.course.stages_m.get(career_course=cur_careercourse)
            else:
                cur_stage = Stage.objects.get(pk=cur_careercourse_stage_list[0][0])
        else:
            cur_stage = Stage.objects.get(pk=stage_id)

        # 获取当前阶段的前后阶段的ID
        setattr(cur_stage, "prev_stage", None)   # 默认前面已没有阶段
        setattr(cur_stage, "next_stage", None)   # 默认后面已没有阶段
        cur_stage_index = cur_careercourse_stage_list.index((cur_stage.id,))
        if cur_stage_index - 1 >= 0:
            cur_stage.prev_stage = cur_careercourse_stage_list[cur_stage_index - 1][0]

        if cur_stage_index + 1 <= len(cur_careercourse_stage_list)-1:
            cur_stage.next_stage = cur_careercourse_stage_list[cur_stage_index + 1][0]

    except Exception as e:
        pass
        # 20160324 解决报错(用错误来控制只能是学生进入页面,却把错误写在日志里,不应该)
        # logger.error(e)

    result = {'cur_careercourse': cur_careercourse,
              'cur_stage': cur_stage,
              'student': user,
              'class_coding': user_class and user_class.coding or ''}

    return result

def get_cur_careercourse(user, careercourse_id):
    """
    获取当前职业课程
    :param careercourse_id:
    :return:
    """
    # 获取当前职业课程对象
    try:
        cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except CareerCourse.DoesNotExist:
        return {'status': 'error', 'data': '没有该职业课程'}

    # 获取课程加锁和解锁状态
    setattr(cur_careercourse, "is_unlock", False)   # 职业课程是否解锁，默认未解锁
    setattr(cur_careercourse, "deadline", None)   # 职业课程解锁的到期时间
    setattr(cur_careercourse, "is_pause", False)   # 职业课程是否处于暂停状态，默认处于暂停
    class_students = ClassStudents.objects.filter(user=user, student_class__career_course=cur_careercourse)
    if len(class_students) > 0:
        #判断这个用户是否解锁这个职业课程下面的所有阶段
        careercourse_stages = cur_careercourse.stage_set.all().order_by("index", "id")
        user_unlock_stages = UserUnlockStage.objects.filter(user=user, stage=careercourse_stages)
        if class_students[0].deadline is None or len(careercourse_stages) == len(user_unlock_stages):
            cur_careercourse.is_unlock = True
        elif class_students[0].deadline and class_students[0].deadline > datetime.now():
            cur_careercourse.is_unlock = True
            cur_careercourse.deadline = class_students[0].deadline
        cur_careercourse.is_pause = class_students[0].is_pause

    return cur_careercourse

def get_stage_course(user, cur_careercourse, stage_id):
    """
    获取该阶段下所有的课程
    :param user:
    :param stage_id:
    :return:
    """
    cur_stage = Stage.objects.get(pk=stage_id)

    cur_stage_course_list = []
    # 获取当前阶段下面的所有课程
    cur_stage_course_list_temp = Course.objects.filter(stages_m=cur_stage).all().order_by("index", "id")
    if len(cur_stage_course_list_temp) == 0:
        return {'status': 'error', 'data': '该阶段下还没有课程'}
    # 获取当前阶段所有课程-所有章节及其观看状态
    from django.db import models
    for course in cur_stage_course_list_temp:
        setattr(course, "lesson", [])   # 课程下章节列表
        setattr(course, "lesson_count", course.lesson_set.all().count())  # 课程下章节总数
        setattr(course, "lesson_has_exam_count", 0)  # 课程下有测验题的章节总数
        setattr(course, "lesson_has_homework_count", 0)  # 课程下有课后作业的章节总数
        setattr(course, "lesson_complete_count", 0)  # 已完成课程总数
        setattr(course, "homework_complete_count", 0)  # 已上传课后作业总数
        setattr(course, "lesson_exam_complete_count", 0)  # 已完成随堂测验总数
        setattr(course, "project", {"description": "",
                                    "upload_file": models.FileField(),
                                    "score": 0,
                                    "record_id": "",
                                    "setting_url": settings.SITE_URL+settings.MEDIA_URL, "remark": ""})  # 项目需求描述
        setattr(course, "score", 0)         # 课程评测得分
        setattr(course, "is_complete", False)   # 是否完成该课程
        setattr(course, "rebuild_count", get_rebuild_count(user, course.id))   # 获取当前学生第几次重修
        setattr(course, "has_paper", False)  # 该课程是否已经出了试卷
        setattr(course, "is_complete_paper", False)  # 学生是否已经完成该试卷的课堂总测验
        setattr(course, "paper_accuracy", "0%")  # 学生完成该试卷的课堂总测验的准确率
        setattr(course, "alllesson_is_complete_paper", True)  # 学生是否已经完成所有随堂测验
        setattr(course, "uncomplete_quiz", [])  # 该试卷下学生未做完的题目列表
        setattr(course, "is_underway", False)

        # 获取课程总测验测试试卷和题目
        paper = Paper.objects.filter(examine_type=2, relation_type=2, relation_id=course.id)
        if len(paper) > 0:
            course.has_paper = True
            # 已经做过的题目则不再显示
            course.uncomplete_quiz = get_uncomplete_quiz(user, paper, course.rebuild_count)
            if len(course.uncomplete_quiz) == 0:
                course.is_complete_paper = True
                # 获取课堂总测验准确率
                paper_record = PaperRecord.objects.filter(paper=paper)
                if len(paper_record) > 0:
                    course.paper_accuracy = str(int(paper_record[0].accuracy * 100)) + "%"

        # 检查是否完成项目考核作品上传
        project_score=0#优化BUG：编辑项目制作后，不能计算总测验分的问题 by guotao
        project = Project.objects.filter(examine_type=5,
                                         relation_type=2,
                                         relation_id=course.id)
        if len(project) > 0:
            course.project["description"] = project[0].description
            project_record = ProjectRecord.objects.filter(project=project[0],
                                                          student=user,
                                                          rebuild_count=course.rebuild_count)
            if len(project_record) > 0:
                course.project["upload_file"] = project_record[0].upload_file
                course.project["score"] = project_record[0].score
                project_score=project_record[0].score
                course.project["remark"] = project_record[0].remark
                course.project["record_id"] = project_record[0].id

        check_course_score(user, course) # 检查是否有course_score记录,没有则创建

        # 获取该课程是否完成，并计算当前得分
        course_score = CourseScore.objects.filter(user=user,
                                                  course=course.id,
                                                  rebuild_count=course.rebuild_count)
        if len(course_score) > 0 and cur_careercourse.is_unlock:
            if check_exam_is_complete(user, course) == 1:
                course.is_complete = True
            if course.is_complete:
                if course_score[0].lesson_score is None: course_score[0].lesson_score = 0
                if course_score[0].course_score is None: course_score[0].course_score = 0
                if course_score[0].project_score is None: course_score[0].project_score = 0
                if course_score[0].project_score != project_score:#优化BUG：编辑项目制作后，不能计算总测验分的问题 by guotao
                    course_score[0].project_score = project_score
                    course_score[0].save()
                course.score = get_course_score(course_score[0], course)   # 计算当前测验分得分

        for lesson in course.lesson_set.order_by("index", "id"):
            setattr(lesson, "is_complete", False)   # 是否完成章节学习
            setattr(lesson, "has_exam", False)   # 是否有测验题
            setattr(lesson, "has_homework", False)   # 是否有课后作业
            setattr(lesson, "is_complete_paper", False)  # 学生是否已经完成该试卷的测验
            setattr(lesson, "code_exercise_type", lesson.code_exercise_type)
            learning_lesson = UserLearningLesson.objects.filter(user=user, lesson=lesson)
            if len(learning_lesson) > 0:
                lesson.is_complete = learning_lesson[0].is_complete
                if lesson.is_complete:
                    course.lesson_complete_count += 1

            setattr(lesson, "homework", models.FileField())         # 是否完成作业提交，下载地址不为空则表示作业已经提交
            setattr(lesson, "result", None)
            # 获取当前课程的Homework信息
            if lesson.have_homework:
                homework = Homework.objects.filter(examine_type=1,
                                                   relation_type=1,
                                                   relation_id=lesson.id)
                if len(homework) > 0:
                    lesson.has_homework = True
                    course.lesson_has_homework_count += 1
                    # 后续需求改动，重修后课后作业不需要再上传
                    homework_record = HomeworkRecord.objects.filter(homework=homework[0],
                                                                    student=user)
                    if len(homework_record) > 0:
                        lesson.homework = homework_record[0].upload_file  #by ym
                        result = homework_record[0].result   #.encode('utf-8')
                        if result:
                            result = cgi.escape(result)
                        course.homework_complete_count += 1
                        setattr(lesson, "result", result)


            setattr(lesson, "exam_accuracy", None)         # 随堂测验准确率
            # 获取当前课程的随堂测验信息
            paper = Paper.objects.filter(examine_type=2,
                                         relation_type=1,
                                         relation_id=lesson.id)
            if len(paper) > 0:
                lesson.has_exam = True
                course.lesson_has_exam_count += 1
                quiz_count = Quiz.objects.filter(paper=paper).count() #试卷拥有的题目数量
                paper_record = PaperRecord.objects.filter(Q(paper=paper[0]),
                                                          Q(student=user),
                                                          Q(rebuild_count=course.rebuild_count),
                                                          ~Q(score=None)) #试卷对应考核记录
                if len(paper_record) > 0:
                    quizrecord_count = QuizRecord.objects.filter(paper_record=paper_record).count() # 学生已做的试题数量
                    if quiz_count > quizrecord_count:
                        lesson.is_complete_paper = False
                        course.alllesson_is_complete_paper = False
                    elif quiz_count == quizrecord_count:
                        lesson.is_complete_paper = True
                        if paper_record[0].accuracy is not None:
                            lesson.exam_accuracy = str(int(paper_record[0].accuracy * 100)) + "%"
                            course.lesson_exam_complete_count += 1
                else:
                    lesson.is_complete_paper = False
                    course.alllesson_is_complete_paper = False
            course.lesson.append(lesson)
            # zhangyu 为课程设置是否必修属性
        if Course_Stages_m.objects.get(course=course, stage=cur_stage).is_required:
            setattr(course, 'is_required', True)
        else:
            setattr(course, 'is_required', False)
        cur_stage_course_list.append(course)

    stage_set = cur_careercourse.stage_set.all()  # 获取当前职业课程下所有的阶段
    is_break = 0
    cur_stage_temp = None
    for stage in stage_set:
        if is_break == 1:
            break
        # 获取该阶段下所有课程
        cur_stage_course_list_my = Course.objects.filter(stages_m=stage).all().order_by("index", "id")

        for course in cur_stage_course_list_my:
            if course.lesson_set.all().count() > 0:
                # 检测该课程是否已完成
                course_stage_m = Course_Stages_m.objects.filter(course=course, stage=cur_stage)
                if course_stage_m:
                    if not course_stage_m[0].is_required:
                        continue
                if check_exam_is_complete(user, course) != 1:
                    # 记录当前正在进行的课程和阶段
                    cur_course = course
                    cur_stage_temp = stage
                    is_break = 1
                    break
    if cur_stage_temp is not None:
        # 传进来的阶段id是否为正在进行中课程的id
        if cur_stage.id == cur_stage_temp.id:
            for course in cur_stage_course_list:
                # 记录第一个未完成课程的id
                if cur_course.id == course.id:
                    course.is_underway = True

    return cur_stage_course_list



# author:胡明星
# function: 根据企业直通班ID和阶段ID来获取评测详情信息
# param:
# ret:
#
# def careercourse_detail(user, careercourse_id, stage_id):
#
#     cur_careercourse = None    # 当前职业课程
#     cur_stage = None       # 当前阶段
#     cur_stage_course_list = []   # 当前阶段课程列表
#     user_class = None
#     try:
#
#         # 获取当前职业课程对象
#         try:
#             cur_careercourse = CareerCourse.objects.get(pk=careercourse_id)
#             # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
#         except CareerCourse.DoesNotExist:
#             return {'status': 'error', 'data': '没有该职业课程'}
#
#         # 获取该职业课程下所有阶段信息
#         cur_careercourse_stage_list = list(cur_careercourse.stage_set.all().order_by("index", "id").values_list("id"))
#         if len(cur_careercourse_stage_list) == 0:
#             return {'status': 'error', 'data': '该课程还没有阶段信息'}
#
#         # 获取课程加锁和解锁状态
#         setattr(cur_careercourse, "is_unlock", False)   # 职业课程是否解锁，默认未解锁
#         setattr(cur_careercourse, "deadline", None)   # 职业课程解锁的到期时间
#         setattr(cur_careercourse, "is_pause", False)   # 职业课程是否处于暂停状态，默认处于暂停
#         class_students = ClassStudents.objects.filter(user=user, student_class__career_course=cur_careercourse)
#         if len(class_students) > 0:
#             if class_students[0].deadline is None or class_students[0].deadline > datetime.now():
#                 cur_careercourse.is_unlock = True
#                 cur_careercourse.deadline = class_students[0].deadline
#                 cur_careercourse.is_pause = class_students[0].is_pause
#             user_class = class_students[0].student_class
#
#         # 获取当前正在看哪个学习阶段
#         if stage_id is None:
#             # 获取正在进行中的课程所对应的阶段
#             stagelist = cur_careercourse.stage_set.all()
#             courselist = Course.objects.filter(stages_m__in=stagelist)
#             recent_learned_lesson = UserLearningLesson.objects.filter(user=user,
#                                                                       lesson__course__in=courselist).order_by("-date_learning")
#             if recent_learned_lesson:
#                 # 同一职业课程下如果有两个阶段都包括该课程，会出现多条记录
#                 cur_stage = recent_learned_lesson[0].lesson.course.stages_m.get(career_course=cur_careercourse)
#             else:
#                 cur_stage = Stage.objects.get(pk=cur_careercourse_stage_list[0][0])
#         else:
#             cur_stage = Stage.objects.get(pk=stage_id)
#
#         # 获取当前阶段的前后阶段的ID
#         setattr(cur_stage, "prev_stage", None)   # 默认前面已没有阶段
#         setattr(cur_stage, "next_stage", None)   # 默认后面已没有阶段
#         cur_stage_index = cur_careercourse_stage_list.index((cur_stage.id,))
#         if cur_stage_index - 1 >= 0:
#             cur_stage.prev_stage = cur_careercourse_stage_list[cur_stage_index - 1][0]
#
#         if cur_stage_index + 1 <= len(cur_careercourse_stage_list)-1:
#             cur_stage.next_stage = cur_careercourse_stage_list[cur_stage_index + 1][0]
#
#         cur_stage_course_list = []
#         # 获取当前阶段下面的所有课程
#         cur_stage_course_list_temp = Course.objects.filter(stages_m=cur_stage).all().order_by("index", "id")
#         if len(cur_stage_course_list_temp) == 0:
#             return {'status': 'error', 'data': '该阶段下还没有课程'}
#         # 获取当前阶段所有课程-所有章节及其观看状态
#         for course in cur_stage_course_list_temp:
#             setattr(course, "lesson", [])   # 课程下章节列表
#             setattr(course, "lesson_count", course.lesson_set.all().count())  # 课程下章节总数
#             setattr(course, "lesson_has_exam_count", 0)  # 课程下有测验题的章节总数
#             setattr(course, "lesson_has_homework_count", 0)  # 课程下有课后作业的章节总数
#             setattr(course, "lesson_complete_count", 0)  # 已完成课程总数
#             setattr(course, "homework_complete_count", 0)  # 已上传课后作业总数
#             setattr(course, "lesson_exam_complete_count", 0)  # 已完成随堂测验总数
#             setattr(course, "project", {"description": "",
#                                         "upload_file": "",
#                                         "score": 0,
#                                         "record_id": "",
#                                         "setting_url": settings.SITE_URL+settings.MEDIA_URL, "remark": ""})  # 项目需求描述
#             setattr(course, "score", 0)         # 课程评测得分
#             setattr(course, "is_complete", False)   # 是否完成该课程
#             setattr(course, "rebuild_count", get_rebuild_count(user.id, course.id))   # 获取当前学生第几次重修
#             setattr(course, "has_paper", False)  # 该课程是否已经出了试卷
#             setattr(course, "is_complete_paper", False)  # 学生是否已经完成该试卷的课堂总测验
#             setattr(course, "paper_accuracy", "0%")  # 学生完成该试卷的课堂总测验的准确率
#             setattr(course, "alllesson_is_complete_paper", True)  # 学生是否已经完成所有随堂测验
#             setattr(course, "uncomplete_quiz", [])  # 该试卷下学生未做完的题目列表
#             setattr(course, "is_underway", False)
#
#             # 获取课程总测验测试试卷和题目
#             paper = Paper.objects.filter(examine_type=2, relation_type=2, relation_id=course.id)
#             if len(paper) > 0:
#                 course.has_paper = True
#                 # 已经做过的题目则不再显示
#                 course.uncomplete_quiz = get_uncomplete_quiz(user, paper, course.rebuild_count)
#                 if len(course.uncomplete_quiz) == 0:
#                     course.is_complete_paper = True
#                     # 获取课堂总测验准确率
#                     paper_record = PaperRecord.objects.filter(paper=paper)
#                     if len(paper_record) > 0:
#                         course.paper_accuracy = str(int(paper_record[0].accuracy * 100)) + "%"
#
#             check_course_score(user, course) # 检查是否有course_score记录,没有则创建
#             # 获取该课程是否完成，并计算当前得分
#             course_score = CourseScore.objects.filter(user=user,
#                                                       course=course.id,
#                                                       rebuild_count=course.rebuild_count)
#             if len(course_score) > 0 and cur_careercourse.is_unlock:
#                 if check_exam_is_complete(user, course) == 1:
#                     course.is_complete = True
#                 if course.is_complete:
#                     if course_score[0].lesson_score is None: course_score[0].lesson_score = 0
#                     if course_score[0].course_score is None: course_score[0].course_score = 0
#                     if course_score[0].project_score is None: course_score[0].project_score = 0
#                     course.score = get_course_score(course_score[0], course)   # 计算当前测验分得分
#
#             # 检查是否完成项目考核作品上传
#             project = Project.objects.filter(examine_type=5,
#                                              relation_type=2,
#                                              relation_id=course.id)
#             if len(project) > 0:
#                 course.project["description"] = project[0].description
#                 project_record = ProjectRecord.objects.filter(project=project[0],
#                                                               student=user,
#                                                               rebuild_count=course.rebuild_count)
#                 if len(project_record) > 0:
#                     course.project["upload_file"] = project_record[0].upload_file
#                     course.project["score"] = project_record[0].score
#                     course.project["remark"] = project_record[0].remark
#                     course.project["record_id"] = project_record[0].id
#
#             for lesson in course.lesson_set.order_by("index", "id"):
#                 setattr(lesson, "is_complete", False)   # 是否完成章节学习
#                 setattr(lesson, "has_exam", False)   # 是否有测验题
#                 setattr(lesson, "has_homework", False)   # 是否有课后作业
#                 setattr(lesson, "is_complete_paper", False)  # 学生是否已经完成该试卷的测验
#                 learning_lesson = UserLearningLesson.objects.filter(user=user, lesson=lesson)
#                 if len(learning_lesson) > 0:
#                     lesson.is_complete = learning_lesson[0].is_complete
#                     if lesson.is_complete:
#                         course.lesson_complete_count += 1
#
#                 setattr(lesson, "homework", "")         # 是否完成作业提交，下载地址不为空则表示作业已经提交
#                 # 获取当前课程的Homework信息
#                 if lesson.have_homework:
#                     homework = Homework.objects.filter(examine_type=1,
#                                                        relation_type=1,
#                                                        relation_id=lesson.id)
#                     if len(homework) > 0:
#                         lesson.has_homework = True
#                         course.lesson_has_homework_count += 1
#                         # 后续需求改动，重修后课后作业不需要再上传
#                         homework_record = HomeworkRecord.objects.filter(homework=homework[0],
#                                                                         student=user)
#                         if len(homework_record) > 0:
#                             lesson.homework = homework_record[0].upload_file
#                             lesson.result = homework_record[0].result
#                             course.homework_complete_count += 1
#                             setattr(lesson, "result", lesson.result)
#
#                 setattr(lesson, "exam_accuracy", None)         # 随堂测验准确率
#                 # 获取当前课程的随堂测验信息
#                 paper = Paper.objects.filter(examine_type=2,
#                                              relation_type=1,
#                                              relation_id=lesson.id)
#                 if len(paper) > 0:
#                     lesson.has_exam = True
#                     course.lesson_has_exam_count += 1
#                     quiz_count = Quiz.objects.filter(paper=paper).count() #试卷拥有的题目数量
#                     paper_record = PaperRecord.objects.filter(Q(paper=paper[0]),
#                                                               Q(student=user),
#                                                               Q(rebuild_count=course.rebuild_count),
#                                                               ~Q(score=None)) #试卷对应考核记录
#                     if len(paper_record) > 0:
#                         quizrecord_count = QuizRecord.objects.filter(paper_record=paper_record).count() # 学生已做的试题数量
#                         if quiz_count > quizrecord_count:
#                             lesson.is_complete_paper = False
#                             course.alllesson_is_complete_paper = False
#                         elif quiz_count == quizrecord_count:
#                             lesson.is_complete_paper = True
#                             if paper_record[0].accuracy is not None:
#                                 lesson.exam_accuracy = str(int(paper_record[0].accuracy * 100)) + "%"
#                                 course.lesson_exam_complete_count += 1
#                     else:
#                         lesson.is_complete_paper = False
#                         course.alllesson_is_complete_paper = False
#                 course.lesson.append(lesson)
#                 # zhangyu 为课程设置是否必修属性
#                 if Course_Stages_m.objects.get(course=course, stage=cur_stage).is_required:
#                     setattr(course, 'is_required', True)
#                 else:
#                     setattr(course, 'is_required', False)
#             cur_stage_course_list.append(course)
#
#     except Exception as e:
#         print e
#         logger.error(e)
#
#     stage_set = cur_careercourse.stage_set.all()  # 获取当前职业课程下所有的阶段
#     is_break = 0
#     cur_stage_temp = None
#     for stage in stage_set:
#         if is_break == 1:
#             break
#         # 获取该阶段下所有课程
#         cur_stage_course_list_my = Course.objects.filter(stages_m=stage).all().order_by("index", "id")
#
#         for course in cur_stage_course_list_my:
#             if course.lesson_set.all().count() > 0:
#                 # 检测该课程是否已完成
#                 if check_exam_is_complete(user, course) != 1 and Course_Stages_m.objects.get(course=course, stage=cur_stage).is_required:
#                     # 记录当前正在进行的课程和阶段
#                     cur_course = course
#                     cur_stage_temp = stage
#                     is_break = 1
#                     break
#     if cur_stage_temp is not None:
#         # 传进来的阶段id是否为正在进行中课程的id
#         if cur_stage.id == cur_stage_temp.id:
#             for course in cur_stage_course_list:
#                 # 记录第一个未完成课程的id
#                 if cur_course.id == course.id:
#                     course.is_underway = True
#
#
#     result = {'cur_careercourse': cur_careercourse,
#               'cur_stage': cur_stage,
#               'cur_stage_course_list': cur_stage_course_list,
#               'student': user,
#               'class_coding': user_class and user_class.coding or ''}
#
#     return result


# 根据lesson_id获取该lesson对应的未做完的试题列表
@csrf_exempt
def get_uncomplete_quiz_by_lesson(request, lesson_id):
    response_data = ""
    try:
        lesson = None
        uncomplete_quiz = []
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return HttpResponse("{'status': 'failure', 'data': '没有找到该章节'}",
                                content_type="application/json")
        rebuild_count = get_rebuild_count(request.user, lesson.course.id)
        # 获取课程总测验测试试卷和题目
        paper = Paper.objects.filter(examine_type=2, relation_type=1, relation_id=lesson_id)
        if len(paper) > 0:
            uncomplete_quiz = get_uncomplete_quiz(request.user, paper, rebuild_count)

        response_data = {
            "course_id": str(lesson.course.id),
            "list": [{"id": str(quiz.id),
                              "question": str(quiz.question),
                              "item_list": str(quiz.item_list)} for quiz in uncomplete_quiz]
        }

    except Exception as e:
        logger.error(e)

    return HttpResponse('{"status": "success", "data": '+json.dumps(response_data)+'}',
                        content_type="application/json")

# function: 处理学生给老师打分任务
@login_required(login_url="/")
@csrf_exempt
def giveScore_students_handler(request,careercourse_id):
    try:
        # user = request.user
        p_id=request.POST.get('pid', None)
        givescore_stu=GiveScoreStudentsUserTask.objects.get(pk=p_id)
        score_dict={u'1':5,u'2':4,u'3':3,u'4':2,u'5':1}
        timeliness = request.POST.get('ra1', None)
        givescore_stu.timeliness=score_dict[timeliness] if timeliness else 0
        professional_level = request.POST.get('ra2', None)
        givescore_stu.professional_level=score_dict[professional_level] if professional_level else 0
        explain_level = request.POST.get('ra3', None)
        givescore_stu.explain_level=score_dict[explain_level] if explain_level else 0
        harvest = request.POST.get('ra4',None)
        givescore_stu.harvest=score_dict[harvest] if harvest else 0
        givescore_stu.suggestion = request.POST.get('txt','')
        givescore_stu.finish_date=datetime.now()
        givescore_stu.status=1
        givescore_stu.save()
        #计算本班本周的平均的评分
        week=givescore_stu.week
        givescore_stu_lst=GiveScoreStudentsUserTask.objects.filter(week=week).aggregate(Avg("timeliness"),
                                                                                        Avg("professional_level"),
                                                                                        Avg("explain_level"),
                                                                                        Avg("harvest"))
        timeliness_avg=givescore_stu_lst["timeliness__avg"]
        professional_level_avg=givescore_stu_lst["professional_level__avg"]
        explain_level_avg=givescore_stu_lst["explain_level__avg"]
        harvest_avg=givescore_stu_lst["harvest__avg"]
        ava_toatal=(timeliness_avg+professional_level_avg+explain_level_avg+harvest_avg)/4
        givescore_sturesult_lst=GiveScoreStudentsResult.objects.filter(week=week)
        if givescore_sturesult_lst:
            givescore_sturesult_lst[0].timeliness=timeliness_avg
            givescore_sturesult_lst[0].professional_level=professional_level_avg
            givescore_sturesult_lst[0].explain_level=explain_level_avg
            givescore_sturesult_lst[0].harvest=harvest_avg
            givescore_sturesult_lst[0].ava_total=ava_toatal
            givescore_sturesult_lst[0].save()
        else:
            GiveScoreStudentsResult.objects.create(week=week,timeliness=timeliness_avg,professional_level=professional_level_avg,
                                                   explain_level=explain_level_avg,harvest=harvest_avg,ava_total=ava_toatal)
    except Exception as e:
        logger.error(e)
    return HttpResponseRedirect('/lps2/learning/plan/'+careercourse_id+'/')


@login_required(login_url="/")
def class_plan_player(request,ownerid):
    # ownerid = "vBVV5jdMJp"
    class_video = ClassMeetingTaskVideo.objects.get(play_id=ownerid)
    return render(request,"mz_lps2/class_plan_player.html",{"ownerid":ownerid,"class_video":class_video})
