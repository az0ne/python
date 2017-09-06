# -*- coding: utf-8 -*-
# import json
# from django.core import serializers
from django.shortcuts import render, redirect
from django.http import JsonResponse
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime, date # modify by chenyu
# from django.db.models import Q
# from mz_common.models import *
# from mz_user.forms import *
# from mz_course.models import *
# from mz_lps.models import *
# from mz_lps2.models import *
# import json, logging, os, uuid,urllib2,urllib
# from mz_user.models import *
# from mz_common.views import *
# from mz_course.views import get_real_amount
# import time
from django.db.utils import IntegrityError
from chart_view import *
from models import CourseUserTask,ClassMeetingTask
from django.contrib.auth.decorators import login_required
from mz_common.decorators import student_required, teacher_required, lps_student_teacher_required
from datetime import timedelta
from mz_lps2.signal_view import *
# from mz_lps2.calc_view import check_lesson_done
from views import match_task_with_classinfo, insert_classmeeting_in_list, create_chart_data,is_specific_task,avatar_crop,careercourse_detail_new
from mz_common.views import sys_send_message
from calc_view import calc_liveroom_join_info,restore_pan_task
from django.core.urlresolvers import reverse
#
logger = logging.getLogger('mz_lps2.teacher_views')

#####################################################
#        教师端
#####################################################
def add_attr_read_me(user_task):

    try:
        readme_user_task = ReadMeUserTask.objects.get(id = user_task.id)
    except Exception as e:
        print "add_attr_read_me",e
    times = user_task.create_datetime.strftime("%Y-%m-%d")
    setattr(user_task,"type","read_me")
    setattr(user_task,"href","")            #跳转的位置
    setattr(user_task,"title","阅读老师教学须知")           #title
    setattr(user_task,"time",times)         #start time
    setattr(user_task,"content","")
    setattr(user_task,"status",readme_user_task.status)
    #.....还有其他属性
    return user_task

def add_attr_profile(user_task):
    try:
        teacher_pro_user_task = TeacherProfileUserTask.objects.get(id = user_task.id)
    except Exception as e:
        print "add_attr_read_me",e
    times = user_task.create_datetime.strftime("%Y-%m-%d")
    setattr(user_task,"type","tea_profile")
    setattr(user_task,"href","")                     #跳转的位置
    setattr(user_task,"title","完善老师个人资料")      #title
    setattr(user_task,"time", times)
    setattr(user_task,"content","")
    setattr(user_task,"status",teacher_pro_user_task.status)
    #...还有其他属性
    return user_task

def add_attr_givescoreusertask(user_task, clazz):
    '''
    为学院打分任务设置属性 zhangyu
    :param user_task:
    :return:
    '''
    try:
        gsut = GiveScoreUserTask.objects.get(id=user_task.id)
    except Exception as e:
        print "add_attr_givescoreusertask",e
    if gsut.week.user_class.id == clazz.id:
        times = user_task.create_datetime.strftime("%Y-%m-%d")
        setattr(user_task, "type", "givescoreuser")
        setattr(user_task, "href", "")            #跳转的位置
        setattr(user_task, "title", "班会打分任务")           #title
        setattr(user_task, "time", times)         #start time
        setattr(user_task, "content", "直播班会已经结束了，快去给学员打分吧~")
        setattr(user_task, "status", gsut.status)
        setattr(user_task, "classmeeting_id", gsut.week.id)
        return user_task
    return None



def add_attr_stustatus(user_task, clazz):
    student_set = clazz.students.all()
    try:
        stu_status_user_task = StuStatusUserTask.objects.get(pk = user_task)
        student = UserProfile.objects.get(pk = stu_status_user_task.student_id)
        if not (student in student_set):
            return None
        stu_profile = UserProfile.objects.get(pk = stu_status_user_task.student_id)
    except Exception as e:
        print e
        logger.error(e)
    type = ""
    title = ""
    content = ""
    if stu_status_user_task.stu_status == 1:
        type = "stu_status_pro"
        title = "学员完成项目制作"
        content = stu_profile.nick_name+"同学完成了项目制作,快去看看吧"
        try:
            course = Course.objects.get(id=stu_status_user_task.relate_id)
            career_course = clazz.career_course
            for each_stage in course.stages_m.all():
                if each_stage.career_course == career_course:
                    setattr(user_task,"relate_stage_id",each_stage.id)
                    break
        except Exception, e:
            print e
            logger.error(e)

        setattr(user_task,"relate_id",stu_status_user_task.relate_id)
    elif stu_status_user_task.stu_status ==2:
        type = "stu_status_progress"
        title = "学员进度落后"
        content = stu_profile.nick_name+"同学进度落后太多,去找他谈谈吧" # XXX同学在XXX课程挂了科
    else:
        pass
    setattr(user_task,"student_id",stu_status_user_task.student_id)
    setattr(user_task,"stustatus_id", stu_status_user_task.id)
    setattr(user_task,"type",type)
    setattr(user_task,"title",title)
    setattr(user_task,"content",content)
    setattr(user_task,"time",stu_status_user_task.create_datetime.strftime("%Y-%m-%d"))
    return user_task

def acquire_teacher_task(user_task_list, career_course, clazz):
    utl=[]
    for user_task in user_task_list:
        if is_specific_task(user_task,ReadMeUserTask):
            utl.append(add_attr_read_me(user_task))
        elif is_specific_task(user_task,TeacherProfileUserTask):
            utl.append(add_attr_profile(user_task))
        elif is_specific_task(user_task,StuStatusUserTask):
            stu_status_set = add_attr_stustatus(user_task,clazz)
            if stu_status_set:
                utl.append(stu_status_set)
        elif is_specific_task(user_task, GiveScoreUserTask):
            user_task = add_attr_givescoreusertask(user_task, clazz)
            if user_task:
                utl.append(user_task)
        else:
            pass
    return utl

# 老师端的学生详情，应该和student_detail_view调用同一个子方法，获取所有的数据
@lps_student_teacher_required
def teacher_class_student_view(request, class_id, user_id):
    result = None
    try:
        stage_id = request.GET.get('stage_id', None)
        try:
            user = UserProfile.objects.get(pk=user_id)
            _class = Class.objects.xall().get(pk=class_id)
        except UserProfile.DoesNotExist:
            return render(request, 'mz_common/failure.html', {'reason': '没有找到该学生信息'})
        except Class.DoesNotExist:
            return render(request, 'mz_common/failure.html', {'reason': '没有找到该班级'})

        # 3.0 跳转
        if _class.lps_version == '3.0':
            return redirect(reverse("lps3:teacher_class", kwargs=dict(class_id=_class.id)))

        temp = careercourse_detail_new(user, _class.career_course.id, stage_id)
        # 为暂时解决用户角色信息反复读取问题，加的用户权限判断方式
        if request.user.is_teacher():
            temp['user_role'] = 'teacher'
        result =dict(temp)
        result.update(create_chart_data(user, _class.career_course))
        result.update({'class_coding':_class.coding, 'class_id':_class.id })

        if 'status' in result and result['status'] == 'error':
            return render(request, 'mz_common/failure.html', {'reason': result['data']})
        print result
    except Exception as e:
        logger.error(e)

    return render(request, 'mz_lps2/learning_data_student_detail_new.html', result)

# author:简超
# function:教师直播班会管理,需要把班会_id放到页面隐藏域  当老师点击打分时,将班会id传递到打分页面
# param:request.POST['class_id']
# ret:
def teacher_class_view(request,class_id):
    user = request.user
    clazz = None
    if not user.is_authenticated() and not user.is_teacher():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限或者没有登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})
    if not class_id:
        return render(request,'mz_common/failure.html',{'reason':'请传入班级id'})
    try:
        clazz = Class.objects.xall().get(pk = class_id)
        # 跳转lps3 班级 zhangyu
        if clazz.lps_version == '3.0':
            return HttpResponsePermanentRedirect(reverse('lps3:teacher_class',kwargs={"class_id": class_id}))
        cur_careercourse = clazz.career_course
    except Exception as e:
        logger.error(e)
        return render(request,'mz_common/failure.html',{'reason':'没有这个班级'})


    # 得到未完成的任务
    un_user_task_list = UserTask.objects.filter(user = user, status__in = [0,2]).order_by("-id")
    user_task_show_list = acquire_teacher_task(un_user_task_list,cur_careercourse, clazz)


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
    #直播班会管理,返回一个list
    class_meeting_manage_list = []
    user_curinfo_lst=[]
    # user_class_list = Class.objects.filter(teacher = user)
    # if clazz.count() > 0:
    class_meeting_list = ClassMeetingTask.objects.filter(user_class = clazz, status__in = [0,2])
    for class_meeting in class_meeting_list:
        insert_classmeeting_in_list(class_meeting, user_task_show_list, cur_careercourse, request.user)
        if not class_meeting.content:
            class_meeting.content = "周直播班会"
            class_meeting.save()

    classmeetingtask_list = ClassMeetingTask.objects.filter(user_class=clazz, is_temp=False).order_by('-startline')
    if classmeetingtask_list.count() > 0 and clazz.students.all().count():
        this_week = classmeetingtask_list[0]
        this_week_kpi_list, is_step, class_start_date, class_end_date = find_all_student_progress(clazz)
        rank_in_class,chart_maxvalue = find_all_student_rank(clazz)
        # #获取学生的数据
        # user_curinfo_lst=_acquire_user_curinfo(clazz,this_week_kpi_list,classmeetingtask_list)
        #将kpi排序由前端转至后端
        this_week_kpi_list.sort(cmp=lambda x,y:cmp(x['kpi'],y['kpi']),reverse=True)
        #将学习状态为暂停的学生抽出排在最末
        kpi_pause_user_lst = []
        for i in this_week_kpi_list:
            if i["pause"]:
                kpi_pause_user_lst.append(i)
        this_week_kpi_list = filter(lambda x: x not in kpi_pause_user_lst, this_week_kpi_list)
        this_week_kpi_list += kpi_pause_user_lst
    else:
        this_week = ClassMeetingTask(id=-1)
        is_step = [0, 0]
        class_start_date = date.today().strftime("%Y-%m-%d")
        class_end_date = date.today().strftime("%Y-%m-%d")

    # 直播班会管理,返回一个list
    class_meeting_manage_list = acquire_tea_class_meet_task(clazz)

    # 获取创建直播班会年份
    nowyear = datetime.now().strftime("%Y")
    class_meeting_year_list = [str(int(nowyear) + i) for i in range(2)]



    return render(request, 'mz_lps2/teach_plan.html',{"cur_careercourse":cur_careercourse ,
                                                      "user_task_show_list":user_task_show_list,
                               # "user_task_finish_list":user_task_finish_list,
                               "class_meeting_manage_list":class_meeting_manage_list,
                               "this_week_kpi_list": json.dumps(this_week_kpi_list),
                               "rank_in_class":json.dumps(rank_in_class),
                                # "user_curinfo_lst":user_curinfo_lst,
                                "chart_maxvalue":chart_maxvalue,
                               "this_week": this_week,
                               "class_id":class_id,
                               "class_coding":clazz.coding,
                               "clazz":clazz,
                               "is_step": is_step,
                               "class_start_date": class_start_date,
                               "class_end_date": class_end_date,
                               "class_meeting_year_list": class_meeting_year_list
                               })


def _acquire_user_curinfo(clazz,this_week_kpi_list,class_meeting_list,n_step=0):
    '''
    老师端获取指定班级和日期（周）所有学生的数据(需要按照KPI排序从大到小在循环输出，KPI显示时)
    '''
    #当周任务（进行中）
    #by guotao 2015.7.8
    #n_step参数传入日期加载步数，依据步数调出非最新周的当周数据
    #by ethe
    user_curinfo_lst = []
    for index,user in enumerate(clazz.students.all()):
        try:
            user_dict={}
            user_dict["kpi"]=this_week_kpi_list[index]['kpi']
            user_dict["image"]=user.avatar_small_thumbnall.url
            #当周的用户任务对应上周班会
            user_curtask_lst=[]
            if class_meeting_list.count()>n_step+1:
                user_task_list=CourseUserTask.objects.filter(user = user,user_class=clazz,
                                                                week=class_meeting_list[n_step+1])
            else:
                user_task_list=CourseUserTask.objects.filter(user = user,user_class=clazz,week=None)
            for user_task in user_task_list:
                from serializers import CourseUserTaskSerializer
                user_curtask_lst.extend([CourseUserTaskSerializer(cur_usertask).data for cur_usertask in
                                         match_task_with_classinfo(user_task, [clazz])])
            user_dict["user_task_list"]=user_curtask_lst
            user_dict["user_name"]=user.nick_name
            user_dict["study_goal"]=user.study_goal if user.study_goal else ''
            user_dict["study_base"]=user.study_base if user.study_base else ''

            is_pause=ClassStudents.objects.filter(user=user,student_class=clazz)[0].is_pause
            if is_pause:
                user_dict["status"]='暂停'
            else:
                user_dict["status"]='正常'

            user_curinfo_lst.append(user_dict)
        except Exception,e:
            logger.error(e)
    #排序

    user_curinfo_lst.sort(cmp=lambda x,y:cmp(x["kpi"],y["kpi"]),reverse=True)
    #将学生状态为暂停的用户抽出排在最末
    pause_user_lst = []
    for i in user_curinfo_lst:
        if i["status"] == '暂停':
            pause_user_lst.append(i)
    user_curinfo_lst = filter(lambda x: x["status"] == '正常', user_curinfo_lst)
    user_curinfo_lst += pause_user_lst

    return  user_curinfo_lst



# 老师获取Kpi分页数据
@csrf_exempt
def teacher_another_week_data_get(request,class_id):

    user = request.user
    cur_class = None    # 当前职业课程

    if not user.is_authenticated() or not user.is_teacher():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})

    # 获取当前职业课程对象
    try:
        cur_class = Class.objects.get(pk = class_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except Class.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该班级'})

    try:
        week_id = request.REQUEST.get('weekid')
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
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.7',
             'kpi':25,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.1',
             'kpi':20,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.6',
             'kpi':17,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.7',
             'kpi':14,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.1',
             'kpi':12,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.6',
             'kpi':10,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            },{
             'name':'姚 No.7',
             'kpi':8,
             'img' : '/static/lps2/images/photo.jpg',
             'url' : 'teacher-2.html'
            }]
        is_step = [0, 1]
        that_week_kpi_list, is_step, class_start_date, class_end_date = find_all_student_progress(class_id, week_id, step, n_step) #, week_id, step)
        #将kpi排序由前端转至后端
        that_week_kpi_list.sort(cmp=lambda x,y:cmp(x['kpi'],y['kpi']),reverse=True)
        #将学习状态为暂停的学生抽出排在最末
        kpi_pause_user_lst = []
        for i in that_week_kpi_list:
            if i["pause"]:
                kpi_pause_user_lst.append(i)
        that_week_kpi_list = filter(lambda x: x not in kpi_pause_user_lst, that_week_kpi_list)
        that_week_kpi_list += kpi_pause_user_lst
        # class_meeting_list = ClassMeetingTask.objects.filter(user_class__id=class_id, is_temp=False).order_by('-startline')
        # user_curinfo_lst=_acquire_user_curinfo(cur_class,that_week_kpi_list,class_meeting_list,n_step=n_step)
        # task_list = []
        #
        # #将user_curinfo_lst_in_serial手动序列化传入
        # #by ethe
        # user_curinfo_lst_in_serial = []
        # for i in user_curinfo_lst:
        #     user_curinfo = {'user_name':i.user_name, 'image':i.image, 'status':i.status, 'study_goal':i.study_goal,
        #                     'study_base':i.study_base,'user_task_list':[]}
        #     for j in i.user_task_list:
        #         user_dic = {'title': j.title, 'text1': j.text1, 'text2': j.text2, 'is_ext': j.is_ext, 'status':j.status}
        #         user_curinfo['user_task_list'].append(user_dic)
        #     user_curinfo_lst_in_serial.append(user_curinfo)

        return HttpResponse('{"status":"success","is_step":'+json.dumps(is_step)+
                            ',"message":'+json.dumps(that_week_kpi_list)+
                            # ',"task_list":'+json.dumps(user_curinfo_lst)+
                            ',"class_start_date":"'+class_start_date+
                            '","class_end_date":"'+class_end_date+'"}',content_type='application/json')

    except Exception as e:
        logger.error(e)
        return HttpResponse('{"status":"failure","message":"发生异常"}', content_type="application/json")

#异步加载老师端，所有学生的任务情况by guotao 2015.7.21
@csrf_exempt
def asyn_get_usertask_info(request,class_id):
    user = request.user
    if not user.is_authenticated() or not user.is_teacher():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})

    # 获取当前职业课程对象
    try:
        cur_class = Class.objects.get(pk = class_id)
        # 如果没有观看过视频，也没有传递stage_id过来，则默认跳到第一阶段
    except Class.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该班级'})
    result={}
    try:
        week_id = request.POST.get('weekid')
        step = int(request.POST.get('step'))
        n_step = int(request.POST.get('n_step'))
        that_week_kpi_list, is_step, class_start_date, class_end_date = find_all_student_progress(class_id, week_id, step, n_step) #, week_id, step)
        class_meeting_list = ClassMeetingTask.objects.filter(user_class__id=class_id, is_temp=False).order_by('-startline')
        user_curinfo_lst=_acquire_user_curinfo(cur_class,that_week_kpi_list,class_meeting_list,n_step=n_step)

        result["status"]="success"
        result["user_curinfo_lst"]=user_curinfo_lst
    except Exception as e:
        logger.error(e)
        result["status"]="failure"
        result["message"]=str(e)
    return JsonResponse(result)

#异步加载老师已经完成的任务 by guotao 2015.7.17
@csrf_exempt
def asyn_get_usertask_finish(request,class_id):
    user = request.user
    if not user.is_authenticated() or not user.is_teacher():
        return render(request, 'mz_common/failure.html',{'reason':'没有访问权限，请先登录。<a href="'+str(settings.SITE_URL)+'">返回首页</a>'})
    # 获取当前职业课程对象
    try:
        cur_class = Class.objects.get(pk = class_id)
        cur_careercourse = cur_class.career_course
    except Class.DoesNotExist:
        return render(request, 'mz_common/failure.html',{'reason':'没有该班级'})
    # 得到已完成的任务
    try:
        user_task_list = UserTask.objects.filter(user = user, status = 1).order_by("-id")
        user_task_finish_list = acquire_teacher_task(user_task_list, cur_careercourse, cur_class)

        #获取完成的班会
        class_meeting_list = ClassMeetingTask.objects.filter(user_class = cur_class, status = 1)
        for class_meeting in class_meeting_list:
            insert_classmeeting_in_list(class_meeting, user_task_finish_list, cur_careercourse, request.user)
            if not class_meeting.content:
                class_meeting.content = "周直播班会"
                class_meeting.save()
        #序列化数据
        user_task_finish_list_new=[]
        from serializers import TeacherUserTaskSerializer,Stu_StatusUserTaskSerializer,GiveScoreUserTaskSerializer,\
                        ClassMeetingkSerializer
        for user_task_finish in  user_task_finish_list:
            if user_task_finish.type=="read_me":
                user_task_finish_list_new.append(TeacherUserTaskSerializer(user_task_finish).data)
                continue
            if user_task_finish.type=="tea_profile":
                user_task_finish_list_new.append(TeacherUserTaskSerializer(user_task_finish).data)
                continue
            if user_task_finish.type=="stu_status_progress":
                user_task_finish_list_new.append(Stu_StatusUserTaskSerializer(user_task_finish).data)
                continue
            if user_task_finish.type=="givescoreuser":
                user_task_finish_list_new.append(GiveScoreUserTaskSerializer(user_task_finish).data)
                continue
            if user_task_finish.type=="classmeeting":
                user_task_finish_list_new.append(ClassMeetingkSerializer(user_task_finish).data)

        return HttpResponse('{"status":"success","user_task_finish_list":'+json.dumps(user_task_finish_list_new)+'}',content_type='text/html')

    except Exception as e:
        logger.error(e)
        return HttpResponse('{"status":"failure","message":"已完成的任务发生异常"}', content_type="text/html")


def acquire_tea_class_meet_task(clazz):
    '''
    # function:获取老师班会任务
    # param: clazz班级对象
    '''

    class_meeting_task_list = []
    try:
        class_meeting_task_list = clazz.classmeetingtask_set.all().order_by("-startline")
        class_meeting_task_list_nottemp = [clazz for clazz in class_meeting_task_list if not clazz.is_temp]
        if len(class_meeting_task_list_nottemp) == 0:
            return class_meeting_task_list
        clazz_meeting_id = class_meeting_task_list_nottemp[-1].id
        for class_meeting in class_meeting_task_list:
            if class_meeting.content is None:
                class_meeting.content = "周直播班会"
            # import pdb;pdb.set_trace()
            if _check_is_grade(class_meeting):
                setattr(class_meeting, "is_fill_score", True)
            else:
                setattr(class_meeting, "is_fill_score", False)
            if class_meeting.id == clazz_meeting_id:
                setattr(class_meeting, "is_first", True)
            else:
                setattr(class_meeting, "is_first", False)
            # 时间显示格式 2015.3.29 20：30
            # add_attr_XXX("is_fill_score")


    except Exception as e:
        print "add_attr_read_me",e
    return class_meeting_task_list

#在这个班会下面所有的学员都打分了才算这个班会已打分
def _check_is_grade(class_meeting):
    if class_meeting:
        #通过每周的CourseUsertask来找应该打分的学生
        course_user_task_list = CourseUserTask.objects.filter(week = class_meeting)
        user_quality_num = UserQualityModelItems.objects.filter(quality_type=2, week=class_meeting).count()
        if len(course_user_task_list) <= user_quality_num:
            return True

        #找到这个班级的所有学生
        # clazz = class_meeting.user_class
        # student_num = clazz.students.all().count()
        # user_quality_num = UserQualityModelItems.objects.filter(quality_type=2, week=class_meeting).count()
        # if student_num == user_quality_num:
        #     return True
    return False

# author:简超
# function:为教师端页面-我的直播班会管理 提供数据  ClassMeetingTask
# param:teacher_user_profile(教师对象)  clazz班级对象
# ret:{}
#
def teacher_class_meeting_read(teacher_user_profile,clazz):
    if teacher_user_profile and clazz:
        try:
            class_meeting_task = ClassMeetingTask.objects.filter(user_class = clazz).order_by("-startline")
        except ClassMeetingTask.DoesNotExist:
            return HttpResponse('不存在值', content_type="application/json")
        return class_meeting_task

# author:zhangyu
# function:创建班会
# ret:
@login_required
@csrf_exempt
def create_temp_class_meeting(request):
    if not request.user.is_authenticated():
        return HttpResponse('请登录', content_type="application/json")
    if request.method == 'POST':
        try:
            if request.POST.has_key("class_id") and request.POST.has_key("content") and request.POST.has_key("class_meeting_time"):
                class_id = request.POST['class_id']
                content = request.POST['content']
                class_meeting_time = request.POST['class_meeting_time']
                class_meeting_time = datetime.strptime(class_meeting_time + ':00', "%Y-%m-%d %H:%M:%S")
                now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if now_date > class_meeting_time.strftime("%Y-%m-%d %H:%M:%S"):
                    return HttpResponse('{"status":"failure","message":"请传入正确的时间格式"}', content_type="application/json")
                # import pdb;pdb.set_trace()
                clazz = Class.objects.get(id=class_id)
                create_datetime = date.today().strftime("%Y-%m-%d %H:%M:%S")
                class_meeting_task = ClassMeetingTask(user_class=clazz, create_datetime=create_datetime,
                                                      startline=class_meeting_time, status=0, content=content,
                                                      is_temp=True)
                class_meeting_task.save()
        except Exception as e:
            print e
            return HttpResponse('{"status":"failure","message":"请传入正确的时间格式"}', content_type="application/json")
        return HttpResponse('{"status":"success","message":""}', content_type="application/json")


# author:简超
# function:修改时间
# param:1.modify_class_meeting_time  2.content
# ret:
@login_required
@csrf_exempt
def modifier_class_meeting_time(request):
    if not request.user.is_authenticated():
        return HttpResponse('请登录', content_type="application/json")
    if request.method == 'POST':
        try:
            if request.POST.has_key("class_meeting_id") and request.POST.has_key("content") and request.POST.has_key("modify_class_meeting_time"):
                class_meeting_id = request.POST['class_meeting_id']
                content = request.POST.get('content')
                modify_class_meeting_time_str = request.POST['modify_class_meeting_time']
                print "修改时间", modify_class_meeting_time_str
                modify_class_meeting_time = datetime.strptime(modify_class_meeting_time_str, "%Y-%m-%d %H:%M:%S")

                class_meeting = ClassMeetingTask.objects.get(pk = int(class_meeting_id))  #获取班会对象,并将其时间修改为modify_class_meeting_time
                if class_meeting:
                    #如果要修改的时间比开始时间早,不允许
                    if modify_class_meeting_time < datetime.now():
                        return HttpResponse("不能往前修改",content_type="application/json")
                    class_meeting.startline = modify_class_meeting_time
                    class_meeting.content = content
                    print "这是",content
                    class_meeting.save()

        except Exception as e:
            print e
            return HttpResponse('{"status":"failure","message":"请传入正确的时间格式"}', content_type="application/json")

        return HttpResponse(
            json.dumps({"class_meeting_time":class_meeting.startline.strftime("%Y-%m-%d %H:%M:%S"),
                        "content":class_meeting.content}),content_type="application/json")   #返回的页面,以及返回修改后的时间和内容

# author:简超
# function:结束直播 1.将其状态置为status = 1
# param:
# ret:
def end_live_telecast(request):
    if not request.user.is_authenticated():
        return HttpResponse('请登录', content_type="application/json")
    class_meeting_id = request.POST.get('class_meeting_id')
    if class_meeting_id:
        try:
            class_meeting = ClassMeetingTask.objects.filter(id = class_meeting_id,status = 2)[0]
            if class_meeting.status == 2:
                class_meeting.status = 1        #完成的状态以及完成的时间
                class_meeting.finish_date = datetime.now()
                class_meeting.save()
                return HttpResponse(json.dumps({"status":class_meeting.status}),content_type="application/json")
        except:
            return HttpResponse("你是不是做了异常操作或者是你操作不对")
    else:
        return HttpResponse('班会id不能为空')

# author:简超
    # function: 点击学员打分需要取出的数据
# param: 班级id
# ret:{}
@csrf_exempt
def student_socre_required_data(request):
    if not request.user.is_authenticated():
        return HttpResponse('{"status":"failure","message":"没有权限"}', content_type="application/json")
    if request.POST.has_key('class_meeting_id'):
        class_meeting_id = request.POST['class_meeting_id']
    else:
        return HttpResponse('{"status":"failure","message":"请传入班级id"}',content_type="application/json")

    if request.POST.has_key('mt'):
        mt=request.POST['mt']
    else:
        mt="stufill"
    try:
        if class_meeting_id:
            class_meeting = ClassMeetingTask.objects.get(id = int(class_meeting_id))
            clazz = class_meeting.user_class
            course_user_task_list = CourseUserTask.objects.filter(week = class_meeting)
            if mt=="stufill":
                calc_liveroom_join_info(class_meeting,clazz)

            stu_join_list = []
            stu_vacancy_list = []

            for course_user_task in course_user_task_list:
                student = course_user_task.user
                join_meeting = (course_user_task and course_user_task.liveroom_in_time) and 1 or 0
                if join_meeting:
                    join_length = (course_user_task.liveroom_out_time - course_user_task.liveroom_in_time).seconds
                    join_length = int(join_length/60)
                    stu_join_list.append({
                        "icon":student.avatar_small_thumbnall.url,
                        "name":student.nick_name,
                        "id":student.id,
                        "chat_capacity":_get_stu_chart_capacity(student,class_meeting),
                        "has_meeting":join_meeting,
                        "join_length":join_length
                    })
                else:
                    stu_vacancy_list.append({
                        "icon":student.avatar_small_thumbnall.url,
                        "name":student.nick_name,
                        "id":student.id,
                        "chat_capacity":_get_stu_chart_capacity(student,class_meeting),
                        "has_meeting":join_meeting
                    })
    except Exception as e:
        return HttpResponse('{"status":"failure","message":'+str(e)+'}',content_type="application/json")
    return HttpResponse(json.dumps({"status":"success", "stu_join_list":stu_join_list,"stu_vacancy_list":stu_vacancy_list,"class_meeting_id":class_meeting_id}),
                            content_type="application/json")

        # if clazz and class_meeting_id:
    #     # import pdb;pdb.set_trace()
    #     try:
    #         student_list = clazz.students.filter(classstudents__is_pause=False)
    #         stu_join_list = []
    #         stu_vacancy_list = []
    #         for student in student_list:
    #             # try:
    #             #     class_student = ClassStudents.objects.get(user=student, student_class=clazz)
    #             # except Exception as e:
    #             #     return HttpResponse('{"status":"failure","message":"学生不在这个班级"}',content_type="application/json")
    #
    #             course_user_task = CourseUserTask.objects.filter(user=student, user_class=class_meeting.user_class)
    #             if course_user_task.count() > 1: # 班级新学员第一周班会后不打分
    #                 cur_course_user_task = course_user_task.filter(week=class_meeting)
    #                 has_meeting = (cur_course_user_task and cur_course_user_task[0].liveroom_in_time) and 1 or 0
    #                 if has_meeting:
    #
    #                     in_time= cur_course_user_task[0].liveroom_in_time
    #                     out_time = cur_course_user_task[0].liveroom_out_time
    #                     join_length = (out_time-in_time).minutes
    #                     stu_join_list.append({
    #                         "icon":student.avatar_small_thumbnall.url,
    #                         "name":student.nick_name,
    #                         "id":student.id,
    #                         "chat_capacity":_get_stu_chart_capacity(student,class_meeting),
    #                         "has_meeting":has_meeting,
    #                         "join_length":join_length
    #                     })
    #                 else:
    #                     stu_vacancy_list.append({
    #                         "icon":student.avatar_small_thumbnall.url,
    #                         "name":student.nick_name,
    #                         "id":student.id,
    #                         "chat_capacity":_get_stu_chart_capacity(student,class_meeting),
    #                         "has_meeting":has_meeting
    #                     })
            # student_list_json = [{
            #     "icon":student.avatar_small_thumbnall.url,
            #     "name":student.username,
            #     "id":student.id,
            #     "chat_capacity":_get_stu_chart_capacity(student,class_meeting),
            #     "has_meeting":has_meeting
            # } for student in student_list]
        # except:
        #     return HttpResponse('{"status":"failure","message":"没有这个班级"}',content_type="application/json")
        # return HttpResponse(json.dumps({"status":"success", "stu_join_list":stu_join_list,"stu_vacancy_list":stu_vacancy_list,"class_meeting_id":class_meeting_id}),
        #                     content_type="application/json")            #返回的页面?   返回状态码
    # else:
    #     return HttpResponse('{"status":"failure","message":"请传入班级id"}',content_type="application/json")


# author:简超
# function: 学员打分
# param:2.沟通力分数
# ret:
#UserQualityModelItems
def student_score_chat(request):
    if not request.user.is_authenticated():
        return HttpResponse('请登录', content_type="application/json")
    if not(request.POST.has_key('chat_capacity') and request.POST.has_key('student_id') and request.POST.has_key('class_meeting_id')):
        return HttpResponse('操作错误',content_type='application/json')
    chat_capacity = request.POST['chat_capacity']           #沟通力分数
    student_id = request.POST['student_id']
    class_meeting_id = request.POST['class_meeting_id']

    if chat_capacity and student_id and class_meeting_id:
        try:
            student = UserProfile.objects.get(id = student_id)   #
            class_meeting = ClassMeetingTask.objects.get(id = class_meeting_id)
            course_user_task = CourseUserTask.objects.filter(user = student,user_class = class_meeting.user_class).count()
            if course_user_task > 1:
                check = UserQualityModelItems.objects.filter(week = class_meeting,quality_type = 2,user = student).count()
                if check == 0:
                    try:
                        user_quality_chat = UserQualityModelItems.objects.create(user = student,quality_type = 2,
                                                                             subject_score = int(chat_capacity),
                                                                             week = class_meeting)
                    except Exception, e:
                        if settings.DEBUG:
                            print e
                            assert False
                        else:
                            logger.error(e)
                            return HttpResponse('{"status":"failure","message":"创建记录失败"}',content_type="application/json")
                    return HttpResponse(json.dumps({"score":user_quality_chat.subject_score}),content_type="application/json")
                else:
                    return HttpResponse('已存在记录',content_type="application/json")
        except:
            return HttpResponse('{"status":"failure","message":"学生对象或者班会对象不存在"}',content_type="application/json")
    else:
        return HttpResponse('{"status":"failure","message":"学生id或者班会id不存在"}',content_type="application/json")



# author:简超
# function: 查看学员数据   1.学员信息  2.互动客户端返回的数据   3.素质项得分(默认-1,页面显示0)
# param:
# ret:  week
def query_student_data(request):
    if not request.user.is_authenticated():
        return HttpResponse('{"status":"failure","message":"没有权限"}', content_type="application/json")
    if request.POST.has_key('class_meeting_id'):
        class_meeting_id = request.POST['class_meeting_id']  #获取班会Id
        class_meeting = ClassMeetingTask.objects.get(id = class_meeting_id)
        clazz = class_meeting.user_class
    if clazz and class_meeting:
        try:
            student_list = clazz.students.all()
            student_list_json = [{
                "icon":student.avatar_small_thumbnall.url,
                "name":student.username,
                "id":student.id,
                "chart_capacity":_get_stu_chart_capacity(student,class_meeting),
                "execute_capacity":_get_stu_execute_capacity(student,class_meeting),
            } for student in student_list]
            return HttpResponse(json.dumps({"student_list":student_list_json}),content_type="application/json")        #返回的页面
        except Exception as e:
            raise e
    else:
        return HttpResponse('{"status":"failure","message":"班级id或者班会id不存在"}',content_type="application/json")


def _get_stu_chart_capacity(student,class_meeting):
    if student and class_meeting:
        user_quality = UserQualityModelItems.objects.filter(user = student,quality_type = 2,week = class_meeting)
        if len(user_quality) > 0:
            return user_quality[0].subject_score
    return -1

def _get_stu_execute_capacity(student,class_meeting):
    if student and class_meeting:
        user_quality = UserQualityModelItems.objects.filter(user = student,quality_type = 1,week = class_meeting)
        if len(user_quality) > 0:
            return user_quality[0].score
    return 0


# author: chenyu
# function: 处理查看教师须知任务
# param:
# ret:
@login_required
@csrf_exempt
def teacher_contract_handler(request):
    if request.method == 'POST':
        try:
            view_readme_user_task = ReadMeUserTask.objects.filter(user=request.user)[0]
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                return HttpResponse("{'message':'failure'}", content_type="application/json")
        if view_readme_user_task.status != 1:
            view_readme_user_task.status = 1
            view_readme_user_task.finish_date = date.today()
            view_readme_user_task.save()
        return HttpResponse("{'message':'success'}", content_type="application/json")
    else:
        return HttpResponse("{'message':'failure'}", content_type="application/json")

# author: chenyu
# function: 处理教师个人资料完成任务
# param:
# ret:
@login_required(login_url="/")
@csrf_exempt
def teacher_profile_handler(request):
    try:
        if request.method == 'POST':
            user = request.user
            try:
                teach_profile_task = TeacherProfileUserTask.objects.filter(user=user)[:1]
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    return HttpResponse("{'message':'failure'}", content_type="application/json")
            if teach_profile_task:

                valid_msg = None
                avatar = request.POST.get('Filedata_hidden', None)
                real_name = request.POST.get('real_name', None)
                description = request.POST.get('description', None)

                if avatar is None or avatar == "":
                    valid_msg = {'avatar': '必须选择头像'}
                elif real_name is None or real_name == "":
                    valid_msg = {'real_name': '真实姓名不能为空'}
                elif len(real_name) > 10:
                    valid_msg = {'real_name': '真实姓名长度不能超过10个字符'}
                elif description is None or description == "":
                    valid_msg = {'description': '讲师介绍不能为空'}
                elif len(description) > 500:
                    valid_msg = {'description': '讲师介绍不能超过500字符'}

                if valid_msg is not None:
                    return HttpResponse(json.dumps(valid_msg), content_type="application/json")

                # 更新个人资料
                user.nick_name = real_name
                user.description = description
                user.save()

                # 如果是默认头像不进行头像裁切处理
                if request.user.avatar_middle_thumbnall.url.find(avatar) == -1:
                    avatar_crop(request)
                teach_profile_task[0].finish_date = date.today()
                teach_profile_task[0].status = 1
                teach_profile_task[0].save()
                return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except IntegrityError:
        return HttpResponse('{"real_name":"昵称（姓名）不能重复"}', content_type="application/json")
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps({'status': 'failure'}), content_type="application/json")

# author: chenyu
# function: 关闭直播班会及直播室
# param:
# ret:
@login_required
@csrf_exempt
def finish_classmeeting_handler(request):
    if request.method == 'POST':
        user = request.user
        try:
            classmeeting_id = int(request.POST["classmeeting_id"])
            classmeeting = ClassMeetingTask.objects.get(id=classmeeting_id)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e)
                return HttpResponse("{'status':'failure'}", content_type="application/json")
        if not classmeeting.status == 1:
            classmeeting.finish_date = datetime.today()
            classmeeting.status = 1 # 关闭直播班会
            classmeeting.save()
            try:
                liveroom = LiveRoom.objects.get(live_class=classmeeting.user_class)
            except Exception, e:
                print e
            else:
                liveroom.live_is_open = 0 # 关闭直播室
                liveroom.save()
        dict = {}
        dict['status'] = 'success'
        return HttpResponse(json.dumps(dict), content_type="application/json")
    return HttpResponse("{'status':'failure'}", content_type="application/json")

# author:chenyu
# function: 修改直播班会时间
# param:
# ret:
@login_required
@csrf_exempt
def modify_classmeeting_time_handler(request):
    if request.method == "POST":
        pass

# author:chenyu
# function: 给学员打分
# param:
# ret:
# @login_required
# @csrf_exempt
def submit_stu_score_handler(request):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        user = request.user
        try:
            classmeeting_id = int(request.POST.get('classmeeting_id'))
            classmeeting = ClassMeetingTask.objects.get(id=classmeeting_id)
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e)
                return HttpResponse("{'status':'failure'}", content_type="application/json")

        # 完成打分任务 zhangyu
        GiveScoreUserTask.objects.filter(week__id=classmeeting_id).update(status=1)


        user_score_dict = dict(request.POST)
        del user_score_dict['classmeeting_id']

        for user_id, score in user_score_dict.iteritems():
            try:
                subject_score = int(score[0]) # 必须不为空
            except:
                continue
            try:
                user = UserProfile.objects.get(id=int(user_id))
                try:
                    uqml=UserQualityModelItems.objects.get(user=user, \
                            quality_type=2, week=classmeeting)
                    uqml.subject_score = subject_score
                    uqml.save()
                except UserQualityModelItems.DoesNotExist:
                    # 正常路径
                    user_quality_chat = UserQualityModelItems.objects.create(user=user,\
                            quality_type=2, week=classmeeting, subject_score=subject_score\
                            , calc_datetime=date.today())

            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e)
                    return HttpResponse("{'status':'failure'}", content_type="application/json")

        course_user_task_list = CourseUserTask.objects.filter(week = classmeeting, liveroom_in_time = None)
        for course_user_task in course_user_task_list:
            try:

                uqml=UserQualityModelItems.objects.get(user=course_user_task.user, \
                                                       quality_type=2, week=classmeeting)
                # uqml.subject_score = 0
                # uqml.save()
            except UserQualityModelItems.DoesNotExist:
                # 正常路径
                user_quality_chat = UserQualityModelItems.objects.create(user=course_user_task.user, \
                    quality_type=2, week=classmeeting, subject_score=0 \
                    , calc_datetime=date.today())
            except Exception as e:
                return HttpResponse("{'status':'failure'}", content_type="application/json")


        return HttpResponse("{'status':'success'}", content_type="application/json")
    return HttpResponse("{'status':'failure'}", content_type="application/json")

@login_required
@csrf_exempt
def get_classmeeting_time(request):
    day = []

    class_meeting_id = request.POST.get('class_meeting_id')
    try:
        class_meeting = ClassMeetingTask.objects.get(pk = int(class_meeting_id))
        cur_time = datetime.now()
        class_meeting_time = class_meeting.startline
        for i in range(1, 8, 1):
            temp = {}
            if i == cur_time.isoweekday():
                time = cur_time
            if i > cur_time.isoweekday():
                time = cur_time+timedelta(days=(i-cur_time.isoweekday()))
            if i < cur_time.isoweekday():
                time = cur_time+timedelta(days=(7-cur_time.isoweekday()+i))
            temp['time'] = time.strftime("%Y-%m-%d")
            temp['week'] = i
            day.append(temp)
        pre_class_meeting = {}
        pre_class_meeting['pre_week'] = class_meeting_time.isoweekday()
        pre_class_meeting['pre_hours'] = class_meeting_time.strftime("%H")
        pre_class_meeting['pre_minutes'] = class_meeting_time.strftime("%M")
    except Exception as e:
        print e
        logger.error(e)
    return HttpResponse(json.dumps({"startline":datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "day":day, "pre_class_meeting":pre_class_meeting, "content":class_meeting.content}), content_type="json/application")




@csrf_exempt
@teacher_required
def pause_restore_planning(request, type):
    ''' 暂停学习进度 '''

    reason = request.POST.get("reason") or ""
    student_id = request.POST.get("student_id") or ""
    career_id = request.POST.get("career_id") or ""

    try:

        student_id = int(student_id)
        career_id = int(career_id)

        user = UserProfile.objects.get(pk=student_id)
        career_course = CareerCourse.objects.get(pk=career_id)

        # 根据student_id和career_id找到学生所在的班级
        class_student = ClassStudents.objects.get(user=user, student_class__career_course=career_course)
        if type == 'pause':
            class_student.is_pause = True
            class_student.pause_reason = reason
            class_student.pause_datetime = datetime.now()
        elif type == 'restore':
            class_student.is_pause = False
            restore_pan_task(user,class_student.student_class)#回复后安排任务
            class_student.restore_datetime=datetime.now()
            # 如果该学生处于试学阶段，根据暂停和恢复时间重新计算
            if class_student.deadline is not None:
                interval_time = (class_student.restore_datetime-class_student.pause_datetime).seconds
                class_student.deadline = class_student.deadline + timedelta(seconds=interval_time)
        class_student.save()

        return HttpResponse(json.dumps("ok"),
                            content_type="application/json")

    except Exception as e:
        print e
        logging.error(e)
        res = HttpResponse(u"操作失败",
                           content_type="application/json")
        res.status_code = 500
        return res

@csrf_exempt
@teacher_required
def teacher_suggest(request):
    '''
    学生进度落后太多,老师的警告
    '''
    if not request.POST.has_key('suggest_content') and not request.POST.has_key(
            'stustatus_id') and not request.POST.has_key('suggest_type') and not request.POST.has_key('class_number'):
        return HttpResponse("{'status':'failure'}", content_type="application/json")
    suggest_content = request.POST.get('suggest_content')
    stustatus_id = request.POST.get('stustatus_id')
    suggest_type = request.POST.get('suggest_type')
    try:
        stustatususertask = StuStatusUserTask.objects.get(pk=stustatus_id)
    except Exception as e:
        print e
        logger.error(e)

    stustatususertask.trace_desc = suggest_content
    try:
        suggest_type = TraceTypeDict.objects.get(id=int(suggest_type))
    except Exception as e:
        print e
        logger.error(e)
    stustatususertask.trace_type = suggest_type
    stustatususertask.save()
    #发送消息给学生
    if suggest_content == "":
        send_message = "本周你的学习进度落后太多，老师与你沟通的结果是：" + suggest_type.name
        # send_message = request.POST.get("class_number") + "*" + send_message
    else:
        send_message = "本周你的学习进度落后太多，老师与你沟通的结果是：" + suggest_type.name + "-" + suggest_content
    send_message = request.POST.get("class_number") + "*" + send_message
    if sys_send_message(request.user.id, stustatususertask.student_id, 4, send_message):
        stustatususertask.status = 1
        stustatususertask.save()
        return HttpResponse(json.dumps({"suc": "1"}), content_type="json/application")
    else:
        return HttpResponse(json.dumps({"suc": "0"}), content_type="json/application")
@csrf_exempt
@teacher_required
def teacher_suggest_type(request):
    '''
    取出老师督促学生的类型
    '''
    list = TraceTypeDict.objects.all().order_by("index")
    list_type = []
    for trace in list:
        dict = {}
        dict['id'] = trace.id
        dict['name'] = trace.name
        list_type.append(dict)
    return HttpResponse(json.dumps(list_type), content_type="json/application")


@csrf_exempt
@teacher_required
def get_send_context(request):
    '''
    已完成任务中，取出老师给学生发送的消息
    '''
    task_id = request.REQUEST.get("stustatus_id")
    try:
        message_info = StuStatusUserTask.objects.get(pk=task_id)
    except Exception as e:
        logger.error(e)

    mess_dict = {
        "select_type": message_info.trace_type.name,
        "suggest_text": message_info.trace_desc
    }
    return HttpResponse(json.dumps(mess_dict), content_type="json/application")

@teacher_required
def close_display(request,class_id):
    try:
        is_close = request.GET.get("is_close","false")
        is_close = True if is_close == 'true' else False
        clazz = Class.objects.get(pk = class_id)
        clazz.is_closed = is_close
        clazz.save()
    except:
        pass
    return HttpResponseRedirect(reverse('lps2:lps2_teach_plan',kwargs={"class_id": class_id}))


