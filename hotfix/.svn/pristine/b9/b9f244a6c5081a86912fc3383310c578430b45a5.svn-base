# -*- coding: utf-8 -*-
__author__ = 'Steven'
# from django.shortcuts import render
# from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect
# from django.db.models import Sum
from django.conf import settings
# from django.core.paginator import Paginator
# from django.core.paginator import PageNotAnInteger
# from django.core.paginator import EmptyPage
# from django.contrib.auth.models import Group
# from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# from mz_common.models import *
# from mz_user.forms import *
# from mz_course.models import *
# from mz_lps.models import *
# from utils.tool import upload_generation_dir
# from utils import xinge
import sys # modify by chenyu
from mz_common.views import get_rebuild_count,check_course_score,get_course_score,check_exam_is_complete,\
    sys_send_message,check_stage_exam_is_complete
from mz_lps2.views import save_attr_course # add by chenyu
# import time
from datetime import date # modify by chenyu
from datetime import time as datetime_time # add by chenyu
from models import * # modify by chenyu
from collections import OrderedDict # add by chenyu
from mz_common.mz_log2mongo import MzL2M,UserOpType,UserCalcType,ClassOpType,ClassCalcType
import json, requests
#############
# 后台计算
#############

# 全局变量设置
# 学时认定相关参数设置
HOURS_PER_VIDEO = 1
HOURS_PER_PROJ = 5
DEFAULT_HOURS_PER_WEEK = 15
Min_HOURS_PER_WEEK = 5
# 默认班会开始时间（周日晚上20:00:00）
DEFAULT_CLASS_MEETING_TIME = (7, datetime_time(hour=20))
LOGGER_TORNADO = ['calc_view']  #指定loger位置,目的是为了解决tornado多进程时log日志文件句柄被占用的问题

# 章节-项目制作清单：职业课程下全体章节及项目制作的汇总清单
# 目的：驻留内存，以避免频繁访问数据库
# 注意：键名是字符串，使用有序字典保证有序化
# 数据格式：LESSON_PROJ_LIST = {'career_course_id':{'stage_id':{'course_id':[[lesson,], [proj,]],},},}
global LESSON_PROJ_LIST

# 班级-学生日志
# 数据格式： CLASS_STU_LOGGER = {'c{classid}_s{stuid}':logger, }
# global CLASS_STU_LOGGER
# 班级-学生-日期日志
# 数据格式： CLASS_STU_DATE_LOGGER = {'c{classid}_s{stuid}':[logger, 'date'], }
global CLASS_STU_DATE_LOGGER

logger=MzL2M.getLogger("mongodb_logger")

##############
# 直播班会结束后
##############
def get_sum_after_classmeeting(class_set, pre_startline=None):
    """
    创建下周直播班会，
    统计直播室信息，
    更新落后学员提醒任务状态为已完成
    """
    # 获得班级集合
    if not isinstance(class_set, list):
        try:
            class_set = Class.objects.select_related().all()
        except Exception, e:
            if settings.DEBUG == True:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0])
                return False
    classmeeting_task_list = []
    for each_class in class_set:
        # calc_liveroom_info(each_class) # 统计直播室记录
        _update_stu_progress(each_class) # 更新进度落后学员提醒任务状态
        classmeeting_task = _create_classmeeting(each_class, pre_startline) # 创建下周直播班会任务
        create_givescorestu_task(each_class)#创建学生给老师打分的任务
        if classmeeting_task:
            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=each_class.id,
                      class_oper_type=ClassOpType.MEETING_CREATED,
                        classmeetingtask_id=classmeeting_task.id)
            logger.cache(infodict)
            classmeeting_task_list.append(classmeeting_task)
    return classmeeting_task_list

def _update_stu_progress(user_class):
    try:
        StuStatusUserTask.objects.filter(user=user_class.teacher, status__in=[0,2], stu_status=2)\
            .update(status=1, finish_date=datetime.today())
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
            return False

def _create_classmeeting(user_class, pre_startline=None):
    """
    创建下周直播班会
    """
    flags_create=True
    if not pre_startline or not isinstance(pre_startline, datetime):
        today = date.today()
        startline = today + timedelta(DEFAULT_CLASS_MEETING_TIME[0]\
                                      - today.isoweekday())
        startline = datetime.strptime(str(startline) + ' '+ \
                str(DEFAULT_CLASS_MEETING_TIME[1]), '%Y-%m-%d %H:%M:%S')
        if user_class.students.count()<1:#如果是新建的班级并且没有学生则不创建班会 lps优化
            flags_create = False
    else: # 依据上次直播班会时间创建下周班会
        startline = pre_startline + timedelta(7)
    classmeeting_task=None
    try:
        if flags_create:
            classmeeting_task = ClassMeetingTask.objects.create(user_class=user_class, startline=startline, real_start_date=startline, status=0)
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
            return False
    else:
        return classmeeting_task

def create_givescorestu_task(user_class):
    # 在学员入学后一周后（即在第一次进行任务结算时），生成第一次打分任务；然后分别在第三周和第五周生成第二次和第三次的打分任务；
    # 此后每隔四周生成一次打分任务（即生成打分任务的周期为：1、2、2、4...）
    class_stu_set = ClassStudents.objects.select_related().filter(student_class=user_class).exclude(is_pause=True)
    for each_class_stu in class_stu_set:
        user=each_class_stu.user
        classmeeting_list=ClassMeetingTask.objects.filter(user_class=user_class).order_by("-id")
        countweek=CourseUserTask.objects.filter(user_class=user_class,user=user).count()
        #所以的用户在创建新的班会后，第一次都需要生成给老师的打分任务（在这个功能前的数据）
        if countweek>0 and GiveScoreStudentsUserTask.objects.filter(user=user,week__in=classmeeting_list).count()<1:
            GiveScoreStudentsUserTask.objects.create(user=user,week=classmeeting_list[0],status=2)
            continue
        # if countweek-1==0:
        #     GiveScoreStudentsUserTask.objects.create(user=user,week=classmeeting_list[0],status=2)
        #     continue
        if  countweek-3==0:
            GiveScoreStudentsUserTask.objects.create(user=user,week=classmeeting_list[0],status=2)
            continue
        if countweek-5==0:
            GiveScoreStudentsUserTask.objects.create(user=user,week=classmeeting_list[0],status=2)
            continue
        if (countweek-5)%4==0:
           GiveScoreStudentsUserTask.objects.create(user=user,week=classmeeting_list[0],status=2)

#####################
# 定时任务，每30分钟触发
#####################
def calc_rank_in_class(class_set=None):
    """
    计算本周班级排名，按综合分数,
    返回值：{'class_id':{‘user_id’:ranking,},}
    """
    ranking_list = {}
    # 获得班级集合jisa
    if not isinstance(class_set, list):
        try:
            class_set = Class.objects.select_related().all()
        except Exception, e:
            if settings.DEBUG == True:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0])
                return None

    for each_class in class_set:
        try:
            class_ranking_dict = _calc_rank_in_class(each_class)
        except Exception, e:
            if settings.DEBUG == True:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=each_class.id)
                return None
        if class_ranking_dict:
            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=each_class.id,
                    class_calc_type=ClassCalcType.STUDENT_RANKING,
                    class_ranking_dict=class_ranking_dict)
            logger.cache(infodict)
            ranking_list.update({str(each_class.id):class_ranking_dict})
    return ranking_list

def _calc_rank_in_class(user_class):
    """
    计算特定班级本周排名（从0开始），按综合分数,
    返回值：{‘user_id’:ranking,}
    """
    try:
        class_stu_set = ClassStudents.objects.select_related()\
                    .filter(student_class=user_class).exclude(is_pause=True)
        sorted_class_stu_set = sorted(class_stu_set, cmp=_handle_stu_score_cmp, \
                            key=lambda e:e, reverse=True)
        stu_set = [x.user for x in sorted_class_stu_set]
        class_ranking_dict = OrderedDict(zip(stu_set, range(1, len(stu_set)+1)))
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
            return False
    for stu, ranking in class_ranking_dict.iteritems():
        try:
            course_user_task = CourseUserTask.objects.select_related()\
                .filter(user=stu, user_class=user_class)\
                .order_by('-id')[:1]
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
                return False
        if course_user_task:
            course_user_task[0].rank_in_class = ranking
            course_user_task[0].save()
    return class_ranking_dict


##############################
# 定时任务，直播班会结束后，每3分钟
##############################
def calc_student_quality(class_set=None):
    # 获得班级集合
    if not isinstance(class_set, list):
        try:
            class_set = Class.objects.select_related().all()
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0])
                return None

    for each_class in class_set:
        # 获得该班级下学员清单
        class_stu_set = ClassStudents.objects.select_related()\
                .filter(student_class=each_class).exclude(is_pause=True)
        for each_class_stu in class_stu_set:
            calc_single_student_quality(each_class_stu.user, each_class)

def calc_single_student_quality(user, user_class):
    """
    计算特定班级-学员个人素质：沟通力，执行力，主动性
    当周素质项关联当周班会
    """
    try:
        class_meeting_task_set = ClassMeetingTask.objects.select_related()\
                            .filter(user_class=user_class, is_temp=False)\
                            .order_by('-id')
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return False
    # 三项素质分捆绑计算，一旦沟通力项可得（老师已打分），一次性计算三项
    try:
         user_quality_talk_set = UserQualityModelItems.objects.select_related()\
                    .filter(user=user, quality_type=2,\
                    week__in=class_meeting_task_set,\
                    score=-1).exclude(subject_score=-1).order_by('-id')
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return False
    if user_quality_talk_set:
        for each_user_quality_talk in user_quality_talk_set:
            each_user_quality_talk.score = each_user_quality_talk.subject_score
            each_user_quality_talk.save()
            week = each_user_quality_talk.week
            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=week.id,
                                quality_talk_score=each_user_quality_talk.score)
            logger.cache(infodict)
            # 本周班会关联本周素质项
            try:
                course_user_task_set = CourseUserTask.objects.select_related()\
                                .filter(user=user, user_class=user_class)\
                                .order_by('-id')
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                    return False
            # 由于直播班会后，最新的一条CourseUserTask记录为下周任务记录（直播班会前半小时创建）
            # 若记录数未大于1，则表明是班级新学员，首周不布置任务，不计算素质项
            if course_user_task_set.count() > 1:
                # 班会-任务关联逻辑：本周ClassMeetingTask关联下周CourseUserTask
                next_course_user_task = course_user_task_set.get(week=week)
                course_user_task_set = [x for x in course_user_task_set]
                cur_course_user_task = course_user_task_set[course_user_task_set\
                                                .index(next_course_user_task)+1]


                # 主动性计算
                startline = cur_course_user_task.week.finish_date # 开始日期为上周直播班会结束
                deadline = week.finish_date # 截止日期为本周直播班会结束
                cur_course_user_task.comment_count = _get_comment_count(user, user_class, startline, deadline)
                cur_course_user_task.save()

                if cur_course_user_task.comment_count == -1:
                    cur_course_user_task.comment_count = 0

                if not cur_course_user_task.comment_count == -1:
                # if not cur_course_user_task.comment_count == -1 and \
                #     not cur_course_user_task.liveroom_comment_count == -1:
                    # 有效区间分别为[0,9]和[0,6]
                    # liveroom_comment_count = cur_course_user_task.liveroom_comment_count > 9 \
                    #                          and 9 or cur_course_user_task.liveroom_comment_count
                    comment_count = cur_course_user_task.comment_count > 6 \
                                            and 6 or cur_course_user_task.comment_count
                    # score = int(round(70 + 2.5*(liveroom_comment_count - 3) + 2.5*comment_count))
                    score = int(round(70 + 5.0*comment_count))

                    try:
                        UserQualityModelItems.objects.create(user=user, \
                                    quality_type=3, score=score, week=week)
                    except Exception, e:
                        if settings.DEBUG:
                            assert False
                        else:
                            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                            return False
                    infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=week.id,
                                quality_active_score=score)
                    logger.cache(infodict)

                # 执行力计算
                kpi = _calc_kpi(cur_course_user_task)
                # 判断学员是否参加了此次直播班会
                meeting_score = next_course_user_task.liveroom_in_time and 100 or 0
                score = int(round(kpi*100*0.9 + meeting_score*0.1))
                try:
                    UserQualityModelItems.objects.create(user=user, quality_type=1,\
                                                score=score, week=week)
                except Exception, e:
                    if settings.DEBUG:
                        print e
                        assert False
                    else:
                        logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                        return False
                infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=week.id,
                                quality_exe_score=score)
                logger.cache(infodict)

        # 计算平均分，只更新最近可得一周的素质项平均分
        # 执行力平均分
        try:
            user_quality_exe_set = UserQualityModelItems.objects.select_related().filter(user=user,\
                    quality_type=1, week__in=class_meeting_task_set)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                return False
        ava_score = 0.0
        for each_user_quality_exe in user_quality_exe_set:
            ava_score += each_user_quality_exe.score
        ava_score = int(round(ava_score/user_quality_exe_set.count()))
        i = 0
        loop = True
        while loop:
            try:
               valid_week = class_meeting_task_set[i]
               tmp_user_quality = user_quality_exe_set.get(week=valid_week)
            except:
                pass
            else:
                loop = False
            i += 1
        tmp_user_quality.ava_score = ava_score
        tmp_user_quality.save()
        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=valid_week.id,
                                quality_exe_avascore=ava_score)
        logger.cache(infodict)
        # 沟通力平均分
        try:
            user_quality_talk_set = UserQualityModelItems.objects.select_related()\
                .filter(user=user, quality_type=2, week__in=class_meeting_task_set)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                return False
        ava_score = 0.0
        for each_user_quality_talk in user_quality_talk_set:
            ava_score += each_user_quality_talk.score
        ava_score = int(round(ava_score/user_quality_talk_set.count()))
        try:
           tmp_user_quality = user_quality_talk_set.get(week=valid_week)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                return False
        tmp_user_quality.ava_score = ava_score
        tmp_user_quality.save()
        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=valid_week.id,
                                quality_talk_avascore=ava_score)
        logger.cache(infodict)

        # 主动性平均分
        try:
            user_quality_active_set = UserQualityModelItems.objects.select_related()\
                .filter(user=user, quality_type=3, week__in=class_meeting_task_set)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                return False
        ava_score = 0.0
        for each_user_quality_active in user_quality_active_set:
            ava_score += each_user_quality_active.score
        ava_score = int(round(ava_score/user_quality_active_set.count()))
        try:
           tmp_user_quality = user_quality_active_set.get(week=valid_week)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
                return False
        tmp_user_quality.ava_score = ava_score
        tmp_user_quality.save()
        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.QUALITY,
                                classmeetingtask_id=valid_week.id,
                                quality_active_avascore=ava_score)
        logger.cache(infodict)

def _get_comment_count(user, user_class, startline, deadline):
    """
    获得班级下学员当周评论数
    """
    try:
        _check_global_var(user_class)
        lesson_list = []
        for val_stage in LESSON_PROJ_LIST[str(user_class.career_course.id)].values():
            for val_course in val_stage.values():
                lesson_list.extend(val_course[0])
        #默认使用FPS评论
        discuzz_provider = getattr(settings, 'DISCUZZ_PROVIDER', 'FPS')
        if discuzz_provider == 'LPS':
            comment_count = Discuss.objects.filter(user=user, lesson__in=lesson_list,\
                                date_publish__range=(startline, deadline)).count()
        if discuzz_provider == 'FPS':
            lesson_list = [lesson.id for lesson in lesson_list]
            lesson_list = json.dumps(lesson_list)
            _host = settings.FPS_HOST
            #_host = 'http://localhost:8000/'
            _url = _host + "course_discuss/user_comment_count/"
            _params = dict(user_id=user, lesson_list=lesson_list, startline=str(startline), deadline=str(deadline))
            r = requests.post(_url, _params)
            if r.status_code == 200:
                ret = json.loads(r.text)
                if ret['message'] == 'success':
                    return int(ret['count'])
            return 0
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return -1
    return comment_count

##############
# 班会后三天触发
##############
def get_risk_in_week(class_meeting_task_set):
    risk_list = {}
    for each_class_meeting_task in class_meeting_task_set:
        class_risk_list = _get_risk_in_week(each_class_meeting_task)
        if class_risk_list:
            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=each_class_meeting_task.user_class.id,
                    class_calc_type=ClassCalcType.PROGRESS_RISK,
                    class_risk_list=class_risk_list)
            logger.cache(infodict)
            risk_list.update({str(each_class_meeting_task.user_class.id):class_risk_list})
    # print risk_list
    return risk_list

def _get_risk_in_week(class_meeting_task):
    """
    统计特定班级-学员的进度，给老师建立任务
    """
    class_risk_list = []
    class_stu_set = ClassStudents.objects.select_related()\
            .filter(student_class=class_meeting_task.user_class).exclude(is_pause=True)
    for each_class_stu in class_stu_set:
        if _check_risk_in_week(each_class_stu.user, class_meeting_task):
            # 如果该学员进度落后太多，则向老师发消息提醒
            try:
                StuStatusUserTask.objects.create(user=class_meeting_task.user_class.teacher,\
                    stu_status=2, student_id=each_class_stu.user.id, status=2)
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=class_meeting_task.user_class.id,students_id=each_class_stu.user.id)
            class_risk_list.append(each_class_stu.user.id)
    return class_risk_list

def _check_risk_in_week(user, class_meeting_task):
    """
    检查某个特定学员的本周任务进度是否落后
    """
    try:
        course_user_task_set = CourseUserTask.objects.get(user=user, week=class_meeting_task)
    except: # 该学员本周无任务，故不计算kpi
        return False
    kpi = _calc_kpi(course_user_task_set)
    return kpi < 0.25 and True or False


######################
# 定时任务：班会前15分钟
######################
def get_sum_before_classmeeting(class_set=None, classmeeting_task_set=None):
    """
    本周任务处理
    计算下周任务
    计算预计毕业时间
    """
    # 获得班级集合
    if not isinstance(class_set, list):
        try:
            class_set = Class.objects.select_related().all()
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0])
                return False

    for each_class in class_set:
        # 更新该班级对应的章节-项目制作清单
        _create_lesson_proj_list(each_class.career_course)
        # 获得该班级下学员清单：
        class_stu_set = ClassStudents.objects.select_related()\
                .filter(student_class=each_class).exclude(is_pause=True)
        for each_class_stu in class_stu_set:
            #当恢复前有未完成的任务，并且恢复暂停时间，在生成任务前一天，默认不再生成新任务，等待下个时间点再生成任务（add guotao 2015.6.18）
            course_user_task=CourseUserTask.objects.filter(user=each_class_stu.user, user_class=each_class,status=2).order_by('-id')
            if course_user_task:
                if each_class_stu.restore_datetime != None \
                        and datetime.now()-each_class_stu.restore_datetime < timedelta(days=1):
                    continue
            # class_stu_logger = check_class_stu_date_logger(each_class.id, each_class_stu.user.id)

            # 判断学员是否已生成对应的学习任务 (当周的班会对应下一周学习任务)
            try:
                course_user_task = CourseUserTask.objects.filter(user=each_class_stu.user, week=classmeeting_task_set[0])
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=each_class.id)
                    continue
            if not course_user_task:
                relate_content, learning_hours = plan_for_nextweek(each_class_stu.user, each_class) # 计算下周任务，并处理本周任务
                remaining_days = calc_plan_graduate_time(each_class_stu.user, each_class) # 计算预计毕业时间

        start_liveroom(each_class)

def start_liveroom(user_class):
    try:
        liveroom = LiveRoom.objects.get(live_class=user_class)
    except Exception, e:
        if settings.DEBUG:
            print e
            return False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
            return False
    liveroom.live_is_open = 1 # 开启直播室
    liveroom.save()

def close_liveroom(user_class):
    try:
        liveroom = LiveRoom.objects.get(live_class=user_class)
    except Exception, e:
        if settings.DEBUG:
            print e
            return False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id)
            return False
    liveroom.live_is_open = 0 # 关闭直播室
    liveroom.save()

def plan_for_nextweek(user, user_class):
    """
    生成特定班级-学员的下周任务
    """
    #根据前几周学习情况预设下周学习时长
    pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point = _calc_pre_learning_hours(user, user_class)
    # 根据预算的学习时长生成下周任务清单
    learning_plans, learning_hours =  _get_task_for_nextweek(user, user_class,pre_learning_hours)

    # 新建一条CourseUserTask记录
    try:
        class_meeting_task = ClassMeetingTask.objects.filter(user_class=user_class,\
                is_temp=False).order_by('-id')[0]
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return False

    relate_content = learning_hours > 0 and json.dumps(learning_plans) or None
    course_user_task=None
    try:
        course_user_task=CourseUserTask.objects.create(user=user, user_class=user_class, plan_study_time=learning_hours, \
            relate_content=relate_content, status=2, week=class_meeting_task, \
            total_study_time=total_study_time, rank_in_class=rank_in_class,\
            ava_score=ava_score, study_point=study_point)
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            pass
    infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                              user_calc_type=UserCalcType.NEXT_WEEK_TASK,
                                course_user_task_id=course_user_task.id if course_user_task else '',
                                plan_learning_hours=learning_hours)
    logger.cache(infodict)
    # 解决新用户无操作时，无法更新学力值和平均评测分的问题
    if not (ava_score and study_point):
        class_students = ClassStudents.objects.filter(user=user, student_class=user_class)
        _update_study_info(user, user_class, class_students[0].study_point)

    return [relate_content, learning_hours]

def _get_task_for_nextweek(user, user_class, pre_learning_hours):
    """
    生成下周任务清单
    """
    # 计划任务与计划学时数
    learning_plans = {'V':{}, 'P':{}}
    learning_hours = 0
    # if settings.DEBUG:
    #     _check_global_var(user_class) # 用于正常运行测试用例
    _check_global_var(user_class)

    for key_stage, val_stage in LESSON_PROJ_LIST[str(user_class.career_course.id)].iteritems():
        for key_course, val_course in val_stage.iteritems():
            try:
                course = Course.objects.select_related().get(id=int(key_course))
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    continue
            course_stages_m =Course_Stages_m.objects.filter(course=course, stage=key_stage)
            if course_stages_m!=[] and course_stages_m[0].is_required == False: # 跳过选修课
                continue
            #需求变更，编号：REQ-A-001；如果课程通过考核则不安排任务 add 郭涛 2015.5.25
            if  _is_pass_course(user,course):
                continue
            for each_lesson in val_course[0]:
                if not check_lesson_done(user, each_lesson):#需求变更，编号：REQ-A-004；生成任务时需要判断章节是否完成
                    try:
                        learning_plans['V'][key_course].append(each_lesson.id)
                    except:
                        learning_plans['V'][key_course] = [each_lesson.id]
                    learning_hours += HOURS_PER_VIDEO
                    if learning_hours >= pre_learning_hours:
                        return [learning_plans, learning_hours]
            for each_proj in val_course[1]:
                if not check_proj_done(user, each_proj):
                    try:
                        learning_plans['P'][key_course].append(each_proj.id)
                    except:
                        learning_plans['P'][key_course] = [each_proj.id]
                    learning_hours += HOURS_PER_PROJ
                    if learning_hours >= pre_learning_hours:
                        return [learning_plans, learning_hours]
    return [learning_plans, learning_hours]

def _is_pass_course(user, course):
    ''''
    判断用户是否通过了课程（所有考核项已经完成，并且成绩大于60分 add 郭涛 2015.6.30）
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
                logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
        if course_score!=[] and get_course_score(course_score[0],course) >= 60:
            result=True
    return  result

def _calc_pre_learning_hours(user, user_class):
    """
    根据前几周学习情况预设下周学习时长
    """
    #默认设置
    top_num = 3
    pre_learning_hours = DEFAULT_HOURS_PER_WEEK
    total_study_time = 0
    rank_in_class = 0
    ava_score = 0
    study_point = 0
    try:
        pre_course_user_task_set = CourseUserTask.objects.select_related().filter(user=user, user_class=user_class)\
                                .order_by('-id')
    except Exception, e:
        if settings.DEBUG == True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return [pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point]
    if pre_course_user_task_set:
        #最新的数据不是第一周时，按原来要求计算学时
        if pre_course_user_task_set[0].is_first ==False:
            # 根据前三周实际完成学时数，生成下周计划学时数，可据此小幅调整（由于不可切分项目制作缘故）
            pre_learning_hours=0
            tmp_count= 0
            for each_course_user_task in pre_course_user_task_set[:top_num]:
                if each_course_user_task.is_first==True:#如果遇到第一周的数据，则后面都不参与计算
                    break
                pre_learning_hours += (each_course_user_task.real_study_time + each_course_user_task.real_study_time_ext)
                tmp_count+=1
            pre_learning_hours = int(round(pre_learning_hours * 1.0/tmp_count))
            # 如果平均任务量低于阈值，则按本周计划时间确定下周计划时间
            if pre_learning_hours < Min_HOURS_PER_WEEK:
                pre_learning_hours = pre_course_user_task_set[0].plan_study_time

        total_study_time = pre_course_user_task_set[0].total_study_time
        rank_in_class = pre_course_user_task_set[0].rank_in_class
        ava_score = pre_course_user_task_set[0].ava_score
        study_point = pre_course_user_task_set[0].study_point
        # 处理本周任务
        _handle_course_user_task(pre_course_user_task_set[0])
    return [pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point]

def _calc_tswk_learning_hours(user, user_class):
    """
    计划当周学习时长(新加班或者转班级是调用)
    """
    pre_learning_hours = DEFAULT_HOURS_PER_WEEK
    total_study_time = 0
    rank_in_class = 0
    ava_score = 0
    study_point = 0
    try:
        pre_course_user_task_set = CourseUserTask.objects.select_related().filter(user=user, user_class=user_class)\
                                .order_by('-id')
    except Exception, e:
        if settings.DEBUG == True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return [pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point]
    #刚开始进入该职业课程
    # 查询下次班会的开始时间
    try:
        class_meeting_task = ClassMeetingTask.objects.filter(user_class=user_class,is_temp=False).order_by('-id')[0]
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return [pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point]
    #如果加入时间距离班会时间大于1天则安排学习时间，否则不安排
    timedelta_pre=class_meeting_task.startline - datetime.now()
    if timedelta_pre >= timedelta(days=1):
        pre_learning_hours = int(round(DEFAULT_HOURS_PER_WEEK * 1.0/7*timedelta_pre.days))
    else:
        pre_learning_hours = 0
    if pre_course_user_task_set:#可能以前在这个班呆过，因此需要做一个统计和处理
        total_study_time = pre_course_user_task_set[0].total_study_time
        rank_in_class = pre_course_user_task_set[0].rank_in_class
        ava_score = pre_course_user_task_set[0].ava_score
        study_point = pre_course_user_task_set[0].study_point
        # 处理本周任务
        _handle_course_user_task(pre_course_user_task_set[0])

    return [pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point]

def _handle_course_user_task(course_user_task):
    """
    处理本周任务：更新状态
    """
    if course_user_task.real_study_time < course_user_task.plan_study_time:
        status = 0 # 未完成
    else:
        status = 1 # 已完成
    course_user_task.status = status
    course_user_task.save()
    save_attr_course(course_user_task)

#这是一个加了日子的方法，View中有一个没有加日志的，目测这样这个类使用  add 郭涛 2015.5.25
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
                        logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
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
            return True
            #需求变更，编号：REQ-A-004；描述：判断章节的完成不考虑作业是否完成 add 郭涛2015.5.25
            # 判断该章节是否有课后作业
            # if lesson.have_homework:
            #     try:
            #         homework = Homework.objects.get(examine_type=1, relation_type=1,\
            #                                        relation_id=lesson.id)
            #     except:
            #         return True
            #     else:
            #         try:
            #             homework_record = HomeworkRecord.objects.filter(homework=homework, student=user)
            #         except Exception, e:
            #             if settings.DEBUG == True:
            #                 print e
            #                 assert False
            #             else:
            #                 f = sys._getframe()
            #                 logger.error(str(e) +' method: ' + str(f.f_code.co_name) + ' line num: ' + str(f.f_lineno))
            #                 return False
            #         return homework_record and True or False
            # else:
            #     return True

def check_proj_done(user, proj):
    """
    检查项目制作是否完成
    """
    try:
        cur_course = Course.objects.get(pk=proj.relation_id)
        rebuild_count = \
            get_rebuild_count(user, cur_course)
        proj_recored = ProjectRecord.objects.filter(project=proj, student=user, rebuild_count=rebuild_count)
    except Exception, e:
        if settings.DEBUG == True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
            return False
    return proj_recored and True or False

def calc_plan_graduate_time(user, user_class):
    """
    计算特定班级-学员预计毕业时间，按前三周实际学习速度估算
    """
    # if settings.DEBUG:
    #     _check_global_var(user_class) # 用于正常运行测试用例
    _check_global_var(user_class)
    # 根据前三周任务信息
    top_num = 3
    career_course = user_class.career_course
    # 获得上周任务表
    try:
        # 默认按建立时间从近到远返回结果集前三项
        pre_course_user_task_set = CourseUserTask.objects.select_related().\
                        filter(user=user, user_class=user_class).order_by('-id')
    except Exception, e:
        if settings.DEBUG == True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return -1
    if pre_course_user_task_set:
        # 平均每周学习时长
        ave_study_time_perweek = 0.0
        for each_course_user_task in pre_course_user_task_set[:top_num]:
            ave_study_time_perweek += (each_course_user_task.real_study_time\
                                    + each_course_user_task.real_study_time_ext)
        ave_study_time_perweek = ave_study_time_perweek/pre_course_user_task_set.count()
        # 平均每天学习时长
        ave_study_time_perday = ave_study_time_perweek/7

        # 已完成学时数
        # career_course_real_time = 0.0
        # for each_course_user_task in pre_course_user_task_set:
        #     career_course_real_time += (each_course_user_task.real_study_time\
        #                              + each_course_user_task.real_study_time_ext)
    else:
        ave_study_time_perday = DEFAULT_HOURS_PER_WEEK/7.0
        # career_course_real_time = 0.0

    # 获得职业课程剩余的学习时长#Lps优化--2.1.2学习完成度计算优化-guotao 2015.7.2)
    career_course_other_time = 0.0
    for val_stage in LESSON_PROJ_LIST[str(career_course.id)].values():
        for key_course,val_course in val_stage.iteritems():
            # career_course_total_time += (HOURS_PER_VIDEO*len(val_course[0]) + HOURS_PER_PROJ*len(val_course[1]))
            #通过的课程(没有观看的章节)不需要加入毕业时间的计算(#Lps优化--2.1.2学习完成度计算优化-guotao 2015.7.1)
            try:
                course = Course.objects.select_related().get(id=int(key_course))
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    continue
            if not _is_pass_course(user,course):#统计当前课程的剩余学时(已经通过的课程不参与计算)
                for lesson in val_course[0]:
                    learning_lesson = UserLearningLesson.objects.filter(user=user, lesson=lesson)
                    if learning_lesson.count() > 0 :
                        if not learning_lesson[0].is_complete:
                            career_course_other_time += HOURS_PER_VIDEO
                    else:
                        career_course_other_time += HOURS_PER_VIDEO
                career_course_other_time += HOURS_PER_PROJ*len(val_course[1])
    # 计算预计毕业时间（剩余多少天）
    if ave_study_time_perday == 0.0:
        ave_study_time_perday = DEFAULT_HOURS_PER_WEEK/7.0
    try:
        remaining_days = int(round(career_course_other_time /ave_study_time_perday))
    except Exception, e:
        if settings.DEBUG is True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=user.id)
            return -1
    if pre_course_user_task_set:
        pre_course_user_task_set[0].plan_gradute_time = date.today() + timedelta(remaining_days)
        pre_course_user_task_set[0].save()
        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                user_calc_type=UserCalcType.REMAINING_DAYS,
                course_user_task_id=pre_course_user_task_set[0].id,
                plan_learning_hours=pre_course_user_task_set[0].plan_gradute_time)
        logger.cache(infodict)
    return remaining_days


def _check_global_var(user_class):
    """
    检查驻留内存的全局变量是否准备就绪
    """
    career_course = user_class.career_course
    if not 'LESSON_PROJ_LIST' in globals() or \
            not LESSON_PROJ_LIST.has_key(str(career_course.id)):
        _create_lesson_proj_list(career_course)

def _create_lesson_proj_list(career_course):
    """
    分次创建LESSON_PROJ_LIST（分职业课程）
    """
    local_lesson_proj_list = OrderedDict()
    local_lesson_proj_list[str(career_course.id)] = OrderedDict()
    stage_set = Stage.objects.select_related().filter(career_course=\
                                        career_course).order_by('index', 'id')
    for each_stage in stage_set:
        local_lesson_proj_list[str(career_course.id)][str(each_stage.id)] = OrderedDict()
        course_set = Course.objects.select_related().filter(stages_m=\
                                        each_stage).order_by('index', 'id')
        for each_course in course_set:
            local_lesson_proj_list[str(career_course.id)][str(each_stage.id)][str(each_course.id)] = [[], []]
            lesson_set = Lesson.objects.select_related().filter(course=\
                                        each_course).order_by('index', 'id')
            proj_set = Project.objects.select_related().filter(examine_type=5,\
                                        relation_type=2, relation_id=each_course.id)
            local_lesson_proj_list[str(career_course.id)][str(each_stage.id)][str(each_course.id)][0]\
                                        = [x for x in lesson_set]
            local_lesson_proj_list[str(career_course.id)][str(each_stage.id)][str(each_course.id)][1]\
                                        = [x for x in proj_set]
    global LESSON_PROJ_LIST
    # 如果LESSON_PROJ_LIST未定义
    if not 'LESSON_PROJ_LIST' in globals():
        LESSON_PROJ_LIST = OrderedDict()
    LESSON_PROJ_LIST.update(local_lesson_proj_list)

def _handle_stu_score_cmp(a, b):
    """
    比较两个学生综合分数间的先后顺序
    :param a: 学生a
    :param b: 学生b
    注意：study_point 不能为空
    """
    try:
        course_user_task_a = CourseUserTask.objects.select_related()\
            .filter(user=a.user, user_class=a.student_class)\
            .order_by('-id')[:1]
        course_user_task_b = CourseUserTask.objects.select_related()\
            .filter(user=b.user, user_class=b.student_class)\
            .order_by('-id')[:1]
    except Exception, e:
        if settings.DEBUG == True:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0])
            return 0
    if not course_user_task_a:
        return -1
    if not course_user_task_b:
        return 1
    # 综合分数=累计学力值×0.1 + 平均评测分×0.9
    study_point_a = course_user_task_a[0].study_point or 0
    study_point_b = course_user_task_b[0].study_point or 0
    ava_score_a = course_user_task_a[0].ava_score or 0
    ava_score_b = course_user_task_b[0].ava_score or 0

    com_score_a = study_point_a*0.1 + ava_score_a*0.9
    com_score_b = study_point_b*0.1 + ava_score_b*0.9
    return com_score_a >= com_score_b and 1 or -1

def _calc_kpi(course_user_task):
    """
    计算一周kpi
    """
    if course_user_task.plan_study_time == 0.0:
        kpi = 1.0
    else:
        kpi = 1.0 * course_user_task.real_study_time / course_user_task.plan_study_time
    if kpi > 1.0:
        kpi = 1.0
    return kpi


##################
# 定时任务，每3秒触发
##################
def _is_belong(course_user_task, course):
    for stage in course.stages_m.all():
        if stage in course_user_task.user_class.career_course.stage_set.all():
                if course_user_task.user in course_user_task.user_class.students.all():
                    return True
    return False

def update_study_point_score_calc(student, study_point=None, score=None, examine=None, examine_record=None, teacher=None, course=None, rebuild_count=None, lesson_id=0, update_type=0): # update_type=1,视频；2，作业；3，项目
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
    if course is None:
        cur_course = Course()
    else:
        cur_course = course
    # 根据考核对象类型找到相应对象
    # 章节
    if examine is not None and examine_record is not None:
        if examine.relation_type == 1:
            cur_lesson = Lesson.objects.filter(pk=examine.relation_id)
            if len(cur_lesson) > 0:
                cur_course = cur_lesson[0].course
        #课程
        elif examine.relation_type == 2:
            cur_course = Course.objects.filter(pk=examine.relation_id)
            if len(cur_course) > 0:
                cur_course = cur_course[0]
        if rebuild_count is None:
            rebuild_count = get_rebuild_count(student, cur_course)
    #更新CourseTaskDone以及实际学时等信息
    _update_coursetaskdone_study_time(student, examine=examine, examine_record=examine_record, cur_course=cur_course,
                                      lesson_id=lesson_id, update_type=update_type)
    #更新课程学分对象
    _update_course_score(student, study_point=study_point, score=score, examine=examine, examine_record=examine_record,
                         teacher=teacher, cur_course=cur_course,rebuild_count=rebuild_count)
    # 更新班级学力汇总信息及平均评测分
    _update_calss_study_info(student, study_point=study_point, cur_course=cur_course,rebuild_count=rebuild_count)


def _update_coursetaskdone_study_time(student, examine=None, examine_record=None, cur_course=None,  lesson_id=0, update_type=0):
    """
    更新CourseTaskDone已经学时信息
    add by  guotao 2015.7.1
    """
    try:
        # 更新CourseTaskDone
        if update_type > 0:
            course_user_task_list = CourseUserTask.objects.filter(user=student, status=2)
            # if update_type == 1:
            #     cur_course = Lesson.objects.get(pk= lesson_id).course
            for course_user_task in course_user_task_list:
                if _is_belong(course_user_task, cur_course):
                    user_class=course_user_task.user_class#用户处理的班级
                    if update_type == 3: # 向老师添加学生状态提醒（完成项目制作）
                        try:
                            StuStatusUserTask.objects.create(user=course_user_task.user_class.teacher, stu_status=1, student_id=student.id, relate_id=cur_course.id, status=2)
                        except Exception, e:
                            logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=student.id)

                    if _is_pass_course(student,cur_course):
                        #如果是计划中的通过的课程(视频)，需要记录课程任务
                        if update_type == 1:
                            learning_plans = json.loads(course_user_task.relate_content)
                            if learning_plans.has_key('V') and learning_plans['V'].\
                                        has_key(str(cur_course.id)) and int(lesson_id) in \
                                        learning_plans['V'][str(cur_course.id)]:
                                course_task_done = CourseTaskDone()
                                course_task_done.course_user_task = course_user_task
                                course_task_done.course = cur_course
                                course_task_done.relate_type = update_type
                                course_task_done.relate_id = lesson_id
                                course_task_done.save()
                                infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=student.id,
                                    user_oper_type=UserOpType.WATCH_VIDEO,course_id=cur_course.id,lesson_id=lesson_id)
                                logger.cache(infodict)
                    else:#如果未通过的课程，则更新课程任务和增加学时
                        course_task_done = CourseTaskDone()
                        course_task_done.course_user_task = course_user_task
                        course_task_done.course = cur_course
                        course_task_done.relate_type = update_type
                        if update_type == 1:
                            course_task_done.relate_id = lesson_id
                            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=student.id,
                                    user_oper_type=UserOpType.WATCH_VIDEO,course_id=cur_course.id,lesson_id=lesson_id)
                            logger.cache(infodict)
                        else:
                            course_task_done.relate_id = examine_record.id
                            infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=student.id,
                                    user_oper_type=UserOpType.SUBMIT_PROJECT,course_id=cur_course.id,lesson_id=examine_record.id)
                            logger.cache(infodict)
                        course_task_done.save()
                        # 更新real_study_time，real_study_time_ext，total_study_time
                        if update_type == 3: # 项目
                            if course_user_task.calc_log:
                                if ';' in course_user_task.calc_log:
                                    course_user_task.calc_log += ',%s'%examine.id # 记录有效学时proj_id
                                else:
                                    course_user_task.calc_log += ';%s'%examine.id # 记录有效学时proj_id
                            else:
                                course_user_task.calc_log = ';%s'%examine.id
                            learning_plans = json.loads(course_user_task.relate_content)
                            if learning_plans.has_key('P') and learning_plans['P']\
                               .has_key(str(cur_course.id)) and int(examine.id) in \
                                learning_plans['P'][str(cur_course.id)]:
                                course_user_task.real_study_time += HOURS_PER_PROJ
                            else:
                                course_user_task.real_study_time_ext += HOURS_PER_PROJ
                            course_user_task.total_study_time += HOURS_PER_PROJ
                        #现在homework和学时无关，需求变更,编号：REQ-A-004.add 郭涛 2015.5.25
                        elif update_type != 2:# 视频
                            # if update_type == 2: # 作业
                            #     continue
                            #     # lessonid = examine.relation_id
                            #     # existing_ele = "homework"
                            # else:
                            lessonid = lesson_id
                            existing_ele = "homework"#默认课后作业已经完成
                            log_type='video'#判断的视频
                            try:
                                lesson = Lesson.objects.get(id=lessonid)
                            except Exception, breake:
                                if settings.DEBUG:
                                    print e
                                    assert False
                                else:
                                    logger.error(e,task_type=LOGGER_TORNADO[0],calss_id=user_class.id,students_id=student.id)
                                    break
                            if check_lesson_done(student, lesson, existing_ele):
                                if course_user_task.calc_log:
                                    if ';' in course_user_task.calc_log:
                                        tmp_calc_log = course_user_task.calc_log.split(';')
                                        if tmp_calc_log[0]:
                                            course_user_task.calc_log = tmp_calc_log[0] + ',%s;'%lessonid + tmp_calc_log[1]
                                        else:
                                            course_user_task.calc_log = '%s;'%lessonid + tmp_calc_log[1]
                                    else:
                                        course_user_task.calc_log += ',%s'%lessonid # 记录有效学时lesson_id
                                else:
                                    course_user_task.calc_log = str(lessonid)
                                learning_plans = json.loads(course_user_task.relate_content)
                                if learning_plans.has_key('V') and learning_plans['V'].\
                                    has_key(str(cur_course.id)) and int(lessonid) in \
                                    learning_plans['V'][str(cur_course.id)]:
                                        course_user_task.real_study_time += HOURS_PER_VIDEO
                                else:
                                    course_user_task.real_study_time_ext += HOURS_PER_VIDEO
                                course_user_task.total_study_time += HOURS_PER_VIDEO
                        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=student.id,
                                          user_calc_type=UserCalcType.STUDY_TIME,course_user_task_id=course_user_task.id,
                                          course_id=cur_course.id,real_study_time=course_user_task.real_study_time,
                                          real_study_time_ext=course_user_task.real_study_time_ext,
                                          total_study_time=course_user_task.total_study_time)
                        logger.cache(infodict)
                        course_user_task.save()

    except Exception as e:
        logger.error(e,task_type=LOGGER_TORNADO[0],students_id=student.id)


def _update_calss_study_info(student, study_point=None, cur_course=None,rebuild_count=None):
     # 更新班级学力汇总信息及平均评测分
     #add by  guotao 2015.7.1
    for stage in cur_course.stages_m.all():
        stage_id = stage.id
        class_students = ClassStudents.objects.filter(user=student,student_class__career_course=Stage.objects.get(pk = stage_id).career_course)
        if len(class_students)>0:
            if study_point and study_point > 0 and rebuild_count == 0:
                class_students[0].study_point += study_point
                class_students[0].save()
            user_class = class_students[0].student_class
            _update_study_info(student, user_class, class_students[0].study_point)

def _update_course_score(student, study_point=None, score=None, examine=None, examine_record=None, teacher=None, cur_course=None,rebuild_count=None):
    """
    更新课程学分对象
    add by  guotao 2015.7.1
    """
    # 章节
    if examine is not None and examine_record is not None:

        # 更新考核记录学力
        if score is not None:
            examine_record.score = score  # 计算该试卷测验得分
            if teacher is not None:
                examine_record.teacher = teacher
        if study_point is not None:
            examine_record.study_point = study_point   # 学力
        examine_record.save()

        # 在coursescore中更新测验分
        check_course_score(student, cur_course) # 检查是否有course_score记录,没有则创建
        if examine.examine_type in(2,5) and score is not None:
            course_score = CourseScore.objects.filter(user=student,course=cur_course,rebuild_count=rebuild_count)
            if len(course_score):
                # 考试测验
                # 试卷类型测验分
                if examine.examine_type == 2:
                    # 随堂测验
                    if examine.relation_type == 1:
                        # 获取所有章节id列表
                        lesson_list = cur_course.lesson_set.all().values_list("id")
                        lesson_total_score = 0
                        # 获取所有章节对应的paper
                        paper_list = Paper.objects.filter(examine_type=2, relation_type=1, relation_id__in=lesson_list).values_list("id")
                        # 获取所有章节对应的paperrecord
                        paper_record_list = PaperRecord.objects.filter(Q(student=student),Q(paper__in=paper_list),Q(rebuild_count=rebuild_count),~Q(score=None))
                        # 计算随堂测验总分
                        for paper_record in paper_record_list:
                            lesson_total_score += (100 / len(paper_list)) * paper_record.accuracy
                        course_score[0].lesson_score = int(round(lesson_total_score))
                        infodict=dict(task_type=LOGGER_TORNADO[0],students_id=student.id,user_oper_type=UserOpType.SUBMIT_CLASS_TEST,
                                    course_id=cur_course.id,lesson_score=int(round(lesson_total_score)))
                        logger.cache(infodict)
                    # 课程总测验
                    elif examine.relation_type == 2:
                        infodict=dict(task_type=LOGGER_TORNADO[0],students_id=student.id,user_oper_type=UserOpType.SUBMIT_COURSE_FINAL_TEST,
                                    course_id=cur_course.id,course_score=score)
                        logger.cache(infodict)
                        course_score[0].course_score = score
                # 项目类型测验分
                elif examine.examine_type == 5:
                    course_score[0].project_score = score
                    infodict=dict(task_type=LOGGER_TORNADO[0],students_id=student.id,user_oper_type=UserOpType.SUBMIT_PROJECT_TEST,
                                    course_id=cur_course.id,project_score=score)
                    logger.cache(infodict)
                    # 检查测验分考核项是否已经完全考核
                if check_exam_is_complete(student, cur_course) == 1:
                    course_score[0].is_complete = True  # 所有测验完成状态
                    course_score[0].complete_date = datetime.now()  # 测验完成时间

                    for stage in cur_course.stages_m.all():
                        stage_id = stage.id
                        career_course = Stage.objects.get(pk = stage_id).career_course
                        # 如已完成所有考核项，则发送课程通过与否的站内消息
                        total_score = get_course_score(course_score[0], cur_course)
                        if total_score >= 60:
                            #Lps优化--2.1.2学习完成度计算优化-guotao 2015.6.29
                            _update_real_study_time(student,cur_course)
                            sys_send_message(0, student.id, 1, "恭喜您已通过<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"/'>"+
                                                               str(cur_course.name)+"</a>课程，总获得测验分"+str(total_score)+
                                                               "分！<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"/'>继续学习下一课</a>")
                        else:
                            sys_send_message(0, student.id, 1, "您的课程<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"'>"+str(cur_course.name)+
                                                               "</a>挂科啦。不要灰心，<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"'>去重修</a>")
                            # 继续检查是否完成该阶段的所有考核项
                        if check_stage_exam_is_complete(student, cur_course, stage):
                            # 如果完成了所有考核项，则检查该课程对应职业课程的所有阶段和解锁信息
                            stage_list = Stage.objects.filter(career_course=stage.career_course)
                            cur_stage_count = 0
                            for i,stage in enumerate(stage_list):
                                if stage.id == stage_id:
                                    cur_stage_count = i
                                    break
                            if (cur_stage_count+1) < len(stage_list):
                                # 检查下一个阶段是否已经解锁
                                if UserUnlockStage.objects.filter(user=student, stage=stage_list[cur_stage_count+1]).count()>0:
                                    # 已经解锁
                                    msg = "恭喜您能努力坚持学完"+career_course.name+"的第"+str(cur_stage_count+1)+"阶段，赶快继续深造吧，你离梦想仅一步之遥了哦！<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_list[cur_stage_count+1].id)+"'>立即学习下一阶段</a>"
                                else:
                                    # 还未解锁
                                    msg = "恭喜您能努力坚持学完"+career_course.name+"的第"+str(cur_stage_count+1)+"阶段，赶快续费继续深造吧，你离梦想仅一步之遥了哦！<a href='http://www.maiziedu.com/lps2/learning/plan/"+str(career_course.id)+"/?stage_id="+str(stage_list[cur_stage_count+1].id)+"'>立即购买下一阶段</a>"
                            else:
                                msg = "恭喜您能努力坚持学完"+career_course.name+"所有课程，你还可以继续深造哦！<a href='http://www.maiziedu.com/course/'>去选课程</a>"
                            sys_send_message(0, student.id, 1, msg)
                else:
                    # 如果是未完成所有考核项，但是测验分已经超过了60分，则可以判定课程通过，提前更新课程测验完成状态（老代码无视）
                    if get_course_score(course_score[0], cur_course) >= 60:
                        course_score[0].is_complete = True  # 所有测验完成状态
                course_score[0].save()

def _update_real_study_time(user,cur_course):
    """
    如果当周安排的任务中：课程通过考核；则需要更新实际完成的学时为：当前课程安排（当周）的最大学时
    （在计算完成度KPI等需要使用）
    :
    :param user:用户对象
    :param cur_course:课程对象
    add by  guotao 2015.7.1
    """
    course_user_task_list = CourseUserTask.objects.filter(user=user, status=2)
    for course_user_task in course_user_task_list:
        if _is_belong(course_user_task, cur_course):
            cur_course_plantime = 0#当周通过课程的总计划学时
            learning_plans = json.loads(course_user_task.relate_content)
            #计划视频
            if learning_plans.has_key('V') and learning_plans['V'].has_key(str(cur_course.id)):
                cur_course_plantime += len(learning_plans['V'][str(cur_course.id)]) * HOURS_PER_VIDEO
            # 计划项目
            if learning_plans.has_key('P') and learning_plans['P'].has_key(str(cur_course.id)):
                cur_course_plantime += len(learning_plans['P'][str(cur_course.id)]) * HOURS_PER_PROJ

            cur_course_realtime = 0#已完成的实际学时
            #完成的视频
            try:
                course_task_done_set = CourseTaskDone.objects.filter(course_user_task=course_user_task,
                                                                     course=cur_course,relate_type=1)
                for course_task_done in course_task_done_set:
                    if learning_plans.has_key('V') and learning_plans['V'].has_key(str(cur_course.id)) and \
                                    course_task_done.relate_id in learning_plans['V'][str(cur_course.id)]:
                        cur_course_realtime+= HOURS_PER_VIDEO
            except Exception as e:
                logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
            #完成的项目
            try:
                course_task_done_set = CourseTaskDone.objects.filter(course_user_task=course_user_task,
                                                                     course=cur_course,relate_type=3)
                for course_task_done in course_task_done_set:
                    try:
                        project_record = ProjectRecord.objects.get(pk = course_task_done.relate_id)
                        course = Course.objects.get(pk = project_record.project.relation_id)
                    except Exception as e:
                        print e
                        logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
                    if learning_plans.has_key('P') and learning_plans['P'].has_key(str(cur_course.id)) and \
                                    project_record.project.id in learning_plans['P'][str(cur_course.id)]:
                        cur_course_realtime+=  HOURS_PER_PROJ
            except Exception as e:
                logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
            course_user_task.real_study_time += cur_course_plantime-cur_course_realtime
            course_user_task.total_study_time += cur_course_plantime-cur_course_realtime
            course_user_task.save()

def _update_study_info(user, user_class, study_point):
    # 更新CourseUserTask表的累计学力值字段
    try:
        course_user_task = CourseUserTask.objects.select_related().filter(user=user, \
            user_class=user_class).order_by('-id')[:1]
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id)
            return False
    if course_user_task:
        # 更新CourseUserTask表的平均评测分字段
        _check_global_var(user_class) # 检查驻留内存的全局变量
        # 计算平均评测分
        valid_count = 0 # 有效课程数
        total_score = 0 # 评测总分
        for val_stage in LESSON_PROJ_LIST[str(user_class.career_course.id)].values():
            for each_course_id in val_stage.keys():
                try:
                    cur_course = Course.objects.get(pk=each_course_id)
                except Exception, e:
                    if settings.DEBUG:
                        print e
                        assert False
                    else:
                        logger.error(e,task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id)
                        continue
                #如果所以考核已经完成 add 郭涛 2015.5.22
                if  1==check_exam_is_complete(user, cur_course):
                    rebuild_count = get_rebuild_count(user, cur_course)
                    try:
                        course_score = CourseScore.objects.get(user=user, course=cur_course, \
                                                rebuild_count=rebuild_count)
                    except:
                        continue
                    total_score += get_course_score(course_score, cur_course)
                    valid_count += 1
        if valid_count == 0:
            ava_score = 0
        else:
            ava_score = total_score/valid_count
        # 更新学力值与平均评测分
        course_user_task[0].study_point = study_point
        course_user_task[0].ava_score = ava_score
        course_user_task[0].save()
        infodict=dict(task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id,
                                          user_calc_type=UserCalcType.STUDY_POINT_AVERAGE_SCORE,
                                            course_user_task_id=course_user_task[0].id,
                                          study_point=study_point,ava_score=ava_score)
        logger.cache(infodict)

def calc_study_point_score():
    try:
        async_methods=AsyncMethod.objects.filter(is_calc = False) #.order_by("-priority","submit_datetime")
        #time.sleep(60)
        # if len(async_methods):
            # am=async_methods[0]
        count = 0 # 成功次数
        count1 = 0 # 失败次数
        for am in async_methods:
            if am.calc_type==1:
                amdict=json.loads(am.methods)
                # if amdict["student"] == None:
                #     am.is_calc = True
                #     am.save()
                #     count1 += 1
                #     continue
                try:
                    update_study_point_score_calc(student=UserProfile.objects.get(pk=amdict["student"]),
                                             study_point=amdict["study_point"],
                                             score=amdict["score"],
                                             examine= None if amdict["examine"]<0 else Examine.objects.get(pk=amdict["examine"]),
                                             examine_record= None if amdict["examine_record"]<0 else ExamineRecord.objects.get(pk=amdict["examine_record"]),
                                             teacher= None if amdict["teacher"]<0 else UserProfile.objects.get(pk=amdict["teacher"]),
                                             course= None if amdict["course"]<0 else Course.objects.get(pk=amdict["course"]),
                                             rebuild_count=amdict["rebuild_count"],
                                             lesson_id= amdict["lesson_id"],
                                             update_type=amdict["update_type"],)
                except Exception, e:
                    logger.error(e,task_type=LOGGER_TORNADO[0],students_id=int(amdict["student"]))
                    am.is_calc = True
                    am.error_reason = str(e)
                    am.save()
                    count1 += 1
                    continue
                else:
                    count += 1
            am.calc_datetime = datetime.now()
            am.is_calc = True
            am.save()
    except Exception as e:
        logger.error(e,task_type=LOGGER_TORNADO[0])

    return [count, count1]

def _record_user_livemeeting_status(classmeeting, userinfo):

    try:
        student = UserProfile.objects.filter( nick_name = userinfo['nickname'])
        if student and student[0].is_student():
            course_user_task = CourseUserTask.objects.filter(user = student[0], week = classmeeting )
            if course_user_task:
                inittime = datetime(1970,1,1)
                delta_join = timedelta(microseconds = long(userinfo['joinTime'] * 1000))
                delta_leave = timedelta(microseconds = long(userinfo['leaveTime'] * 1000))
                course_user_task[0].liveroom_in_time = inittime + delta_join + timedelta(hours=8)
                course_user_task[0].liveroom_out_time = inittime + delta_leave + timedelta(hours=8)
                course_user_task[0].save()

    except Exception as e:
        logger.error(e,task_type=LOGGER_TORNADO[0])



def calc_liveroom_join_info(classmeeting, user_class):
    _calc_liveroom_join_info(classmeeting, user_class)

def _calc_liveroom_join_info(classmeeting, user_class):
    try:
        classmeeting_starttime = classmeeting.startline

        # 接受当前的班级号
        liveroom = LiveRoom.objects.filter(live_class = user_class)[:1] or None
        if (liveroom is not None):
            url = settings.LIVE_ROOM_JOININFO_API
            values = {
                'loginName':settings.LIVE_ROOM_USERNAME,
                'password':settings.LIVE_ROOM_PASSWORD,
                'sec':'true',
                'roomId': liveroom[0].live_id,
                }

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.loads(response.read().replace('\t', ''))

            inittime = datetime(1970,1,1)
            cmdelta1 = classmeeting_starttime - timedelta(minutes = 15) - inittime
            cmdelta2 = classmeeting_starttime + timedelta(minutes = 15) - inittime

            if result['code'] == '0':
                user_list = result['list']
                # ulen = len(user_list)
                user_list.reverse()
                for userinfo in user_list:

                    delta1=timedelta(microseconds = long(userinfo['joinTime'] * 1000))+timedelta(hours=8)

                    if cmdelta2 < delta1:
                        continue
                    if cmdelta1 > delta1:
                        break
                        # continue
                    _record_user_livemeeting_status(classmeeting, userinfo)
                    # break

    except Exception as e:
        logger.error(e,task_type=LOGGER_TORNADO[0],class_id=user_class.id)

# def _calc_liveroom_qa_info(classmeeting, user_class ):
#
#     try:
#         # 接受当前的班级号
#         liveroom = LiveRoom.objects.filter(live_class = user_class)[:1] or None
#         if (liveroom is not None):
#             url = settings.LIVE_ROOM_EXPORTQA_API
#             values = {
#                 'loginName':settings.LIVE_ROOM_USERNAME,
#                 'password':settings.LIVE_ROOM_PASSWORD,
#                 'sec':'true',
#                 'roomId': liveroom[0].live_id,
#                 }
#
#             data = urllib.urlencode(values)
#             req = urllib2.Request(url, data)
#             response = urllib2.urlopen(req)
#             result = json.loads(response.read())
#
#             if result['code'] == '0':
#                 qa_list = result['list']
#                 # ulen = len(user_list)
#                 qa_list.reverse()
#
#                 _record_user_qa_status(classmeeting, qa_list)
#
#     except Exception as e:
#         f = sys._getframe()
#         logger.error(str(e) +' method: ' + str(f.f_code.co_name) + ' line num: ' + str(f.f_lineno))

# 调用此方法之前，确认以下事宜
# 当前班会已经结束，新的班会还未创建
# 当前班会对应的CourseUserTask已经存在
def calc_liveroom_info( user_class ):
    classmeeting = ClassMeetingTask.objects.filter(user_class = user_class, is_temp = False).order_by("-startline")
    if classmeeting:
        _calc_liveroom_join_info(classmeeting[0], user_class)
    # _calc_liveroom_qa_info(classmeeting, user_class)


#########################
# 班级-学生日志
########################
# def check_class_stu_logger(class_id, stu_id):
#     """
#     检查驻留内存的班级-学生日志句柄是否可得，返回有效句柄
#     """
#     global CLASS_STU_LOGGER
#     if not 'CLASS_STU_LOGGER' in globals() or \
#         not CLASS_STU_LOGGER.has_key('c%s_s%s'%(class_id, stu_id)):
#         logger = _get_class_stu_logger(class_id, stu_id)
#     else:
#         logger = CLASS_STU_LOGGER['c%s_s%s'%(class_id, stu_id)]
#     return logger

# def check_class_stu_date_logger(class_id, stu_id):
#     """
#     检查驻留内存的班级-学生日志句柄是否可得，返回有效句柄
#     """
#     global CLASS_STU_DATE_LOGGER
#     today = date.strftime(date.today(), '%Y-%m-%d')
#     if not 'CLASS_STU_DATE_LOGGER' in globals() or \
#         not CLASS_STU_DATE_LOGGER.has_key('c%s_s%s'%(class_id, stu_id)):
#         logger = _get_class_stu_date_logger(class_id, stu_id, today)
#     else:
#         if CLASS_STU_DATE_LOGGER['c%s_s%s'%(class_id, stu_id)][1] == today:
#             logger = CLASS_STU_DATE_LOGGER['c%s_s%s'%(class_id, stu_id)][0]
#         else:
#             logger = _get_class_stu_date_logger(class_id, stu_id, today)
#     return logger

# def _get_class_stu_logger(class_id, stu_id):
#     """
#     获得班级-学生日志句柄
#     """
#     global CLASS_STU_LOGGER
#     # 如果CLASS_STU_LOGGER未定义
#     if not 'CLASS_STU_LOGGER' in globals():
#         CLASS_STU_LOGGER = {}
#     logger = _create_class_stu_logger(class_id, stu_id)
#     CLASS_STU_LOGGER.update({'c%s_s%s'%(class_id, stu_id):logger})
#     return logger


# def _get_class_stu_date_logger(class_id, stu_id, day):
#     """
#     获得班级-学生日志句柄
#     """
#     global CLASS_STU_DATE_LOGGER
#     # 如果CLASS_STU_DATE_LOGGER未定义
#     if not 'CLASS_STU_DATE_LOGGER' in globals():
#         CLASS_STU_DATE_LOGGER = {}
#     logger = _create_class_stu_date_logger(class_id, stu_id, day)
#     CLASS_STU_DATE_LOGGER.update({'c%s_s%s'%(class_id, stu_id):[logger, day]})
#     return logger

# def _create_class_stu_logger(class_id, stu_id):
#     """
#     动态建立班级-学生日志
#     """
#     if not os.path.exists(settings.CLASS_STU_LOG_ROOT):
#         os.mkdir(settings.CLASS_STU_LOG_ROOT)
#     logger = logging.getLogger('mz_lps2.c%s_s%s_logger'%(class_id, stu_id))
#     fh = logging.FileHandler(settings.CLASS_STU_LOG_ROOT+'c%s_s%s.log'%(class_id, stu_id))
#     ch = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh.setFormatter(formatter)
#     ch.setFormatter(formatter)
#     logger.addHandler(fh)
#     logger.addHandler(ch)
#     return logger


# 建立班级-学生-日期日志
# def _create_class_stu_date_logger(class_id, stu_id, day):
#     """
#     动态建立班级-学生-日期日志
#     :param day 是字符串
#     """
#     filepath = settings.CLASS_STU_LOG_ROOT + LOGGER_TORNADO[0] + '/c%s_s%s/'%(class_id, stu_id)
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)
#     logger = logging.getLogger('mz_lps2.c%s_s%s_d%s_logger'%(class_id, stu_id, day))
#     fh = logging.FileHandler(filepath+'c%s_s%s_d%s.log'%(class_id, stu_id, day))
#     ch = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh.setFormatter(formatter)
#     ch.setFormatter(formatter)
#     logger.addHandler(fh)
#     logger.addHandler(ch)
#     return logger

# def _create_calc_view_logger():
#     """
#     建立calc_view日志
#     """
#     logger = logging.getLogger('mz_lps2.calc_views')
#     fh = logging.FileHandler(settings.CALC_VIEW_LOG_PATH)
#     ch = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh.setFormatter(formatter)
#     ch.setFormatter(formatter)
#     logger.addHandler(fh)
#     logger.addHandler(ch)
#     return logger

# logger = _create_calc_view_logger()

# 用户加入班级，转换班级时的任务推送计划
def get_next_pan_task(user, new_classobj):
    """
    学生新加入班级后，生成从加入班级当天到下一个默认生成计划时间点之间的任务（即不跨周）;
    若学生在生成任务前一天加入班级，不生成任务，等到默认时间点再生成
    """
    try:
        relate_content, learning_hours = _plan_for_tswk(user, new_classobj) # 计划本周任务
        remaining_days = calc_plan_graduate_time(user, new_classobj) # 计算预计毕业时间
    except Exception as msg:
        print "calc_plan_for_tswk----->", msg
        logger.error(msg,task_type=LOGGER_TORNADO[0],class_id=new_classobj.id,students_id=user.id)

def _plan_for_tswk(user, user_class):
    """
    新加入用户班级的本周任务 by add guotao 2015.6.17
    """
    #如果是新班级，由于有学生加入需要创建一个班会
    class_meeting_task_list=ClassMeetingTask.objects.filter(user_class=user_class,is_temp=False).order_by('-id')
    if class_meeting_task_list.count()<1:
        today = date.today()
        startline = today + timedelta(DEFAULT_CLASS_MEETING_TIME[0] - today.isoweekday())
        startline = datetime.strptime(str(startline) + ' '+ str(DEFAULT_CLASS_MEETING_TIME[1]), '%Y-%m-%d %H:%M:%S')
        ClassMeetingTask.objects.create(user_class=user_class, startline=startline, real_start_date=startline, status=0)
    #根据前几周学习情况预设下周学习时长
    pre_learning_hours, total_study_time, rank_in_class, ava_score, study_point = _calc_tswk_learning_hours(user, user_class)
    relate_content, learning_hours=None,0
    if pre_learning_hours!=0:#如果有学时才安排计划
    # 根据预算的学习时长生成下周任务清单
        learning_plans, learning_hours =  _get_task_for_nextweek(user, user_class,pre_learning_hours)

        # 新建一条CourseUserTask记录
        class_meeting_task = None
        try:
            class_meeting_task = ClassMeetingTask.objects.filter(user_class=user_class,is_temp=False).order_by('-id')[1]
        except Exception, e:
            pass
        relate_content = learning_hours > 0 and json.dumps(learning_plans) or None
        try:
            CourseUserTask.objects.create(user=user, user_class=user_class, plan_study_time=learning_hours,
                relate_content=relate_content, status=2,week=class_meeting_task,
                total_study_time=total_study_time, rank_in_class=rank_in_class,
                ava_score=ava_score, study_point=study_point,is_first=True)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],class_id=user_class.id,students_id=user.id)
                pass
    return [relate_content, learning_hours]

#回复暂停状态时，安排任务计划 add guotao 2015.6.18
def restore_pan_task(user, classobj):
    """
    1.暂停前本无学习计划，恢复正常后，按照新加入学生计划的逻辑生成计划
    2.暂停前有学习计划，恢复正常后，仍显示之前的学习计划
    :param user: 用户对象（学生）
    :param classobj: 班级对象
    :return:
    """
    try:
        course_user_task=CourseUserTask.objects.filter(user=user, user_class=classobj,status=2).order_by('-id')
        if not course_user_task:#没有学习计划
            get_next_pan_task(user,classobj)
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0],class_id=classobj.id,students_id=user.id)
			
def update_rank_studypoint():
    """
    更新每个用户的学力排名
    by add guotao 2015.8.4
    """
    user_lst=ClassStudents.objects.all().values("user").distinct()
    for user in user_lst:
        try:
            user_id=user["user"]
            class_stu_lst=ClassStudents.objects.filter(user=user_id)
            study_point=0
            for class_stu  in class_stu_lst:
                study_point+=class_stu.study_point
            if UserSocialProfile.objects.filter(user=user_id).count()>0:
                user_socialprofile=UserSocialProfile.objects.get(user=user_id)
                user_socialprofile.study_point=study_point
                user_socialprofile.save()
            else:
                user=UserProfile.objects.get(id=user_id)
                UserSocialProfile.objects.create(user=user,study_point=study_point)
        except Exception,e:
            logger.error(e,task_type=LOGGER_TORNADO[0],students_id=user.id)
    #排序并且求出排名
    user_soc_lst=UserSocialProfile.objects.all().order_by("-study_point")
    for index,user_soc in enumerate(user_soc_lst):
        user_soc.rank=index+1
        user_soc.save()

