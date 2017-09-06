# -*- coding:utf-8 -*-
__author__ = 'qlp'
from django.http import HttpResponseRedirect
from utils import tool
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from db.api.lps4.career import lps4_studentData
from django.conf import settings
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required

def get_type(action, type):
    if action == "type":
        if type == 0:
            return "非就业学员"
        elif type == 1:
            return "就业学员"
        else:
            return "非付费用户"
    elif action == "stop":
        if type == 0:
            return "否"
        elif type == 1:
            return "是"
        else:
            return ""

@dec_login_required
@handle_http_response_exception(501)
def student_list(request):
    action = tool.get_param_by_request(request.GET, 'action', "query", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    careername = tool.get_param_by_request(request.GET, 'careerName', "", str)
    username = tool.get_param_by_request(request.GET, 'userName', "", str)
    studentid = tool.get_param_by_request(request.GET, 'studentid', "", str)
    if action == "query":   # lps4学员列表展示
        studentlist = lps4_studentData.student_list_data(page_index, settings.PAGE_SIZE)
        studentli = studentlist.result()["result"]
        for studentli in studentli:
            studentli["type"] = get_type("type", studentli["type"])
            studentli["is_stop"] = get_type("stop", studentli["is_stop"])
        studentdata = {
            "studentlist": studentlist.result()["result"],
            "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                     "rows_count": studentlist.result()["rows_count"], "page_count": studentlist.result()["page_count"],
            },
        }
        if studentlist.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    if action == "search":    # 搜索结果列表
        studentlist = lps4_studentData.search_student_data(page_index, settings.PAGE_SIZE, "%"+careername+"%", "%"+username+"%")
        studentli = studentlist.result()["result"]
        for studentli in studentli:
            studentli["type"] = get_type("type", studentli["type"])
            studentli["is_stop"] = get_type("stop", studentli["is_stop"])
        studentdata = {
            "studentlist": studentlist.result()["result"],
            "careerName": careername,
            "userName": username,
            "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                     "rows_count": studentlist.result()["rows_count"], "page_count": studentlist.result()["page_count"],
            },
        }
        if studentlist.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    if action == "revise":    # 学员详情展示
        revisestudent = lps4_studentData.student_revise(studentid)
        if revisestudent.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        if revisestudent:
            revisest = revisestudent.result()["result"]
            revisedata = {
                "action": action,
                "result": revisest,
            }
            return render_to_response("mz_lps4/career/lps4studentrevise.html", revisedata, context_instance=RequestContext(request))
    if action == "reviseCareer":  # 修改lps4学员专业
        careerdata = lps4_studentData.career_list()
        studentdate = lps4_studentData.student_career_date(studentid)
        if studentdate.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        revisedata = {
            "action": action,
            "result": studentdate.result(),
            "careerlist": careerdata.result()["result"],
        }
        print revisedata
        return render_to_response("mz_lps4/career/lps4studentrevise.html", revisedata, context_instance=RequestContext(request))
    if action == "add":  # 新增lp4学员
        careerdata = lps4_studentData.career_list()
        revisedata = {
            "action": action,
            "careerlist": careerdata.result()["result"]
        }
        return render_to_response("mz_lps4/career/lps4studentrevise.html", revisedata, context_instance=RequestContext(request))
    if action == "delete":  # 删除lps4学员
        car_user_id = lps4_studentData.student_id_career_id(studentid)
        if car_user_id.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        career_id = car_user_id.result()
        print career_id
        delstudent = lps4_studentData.delstudent(studentid, career_id["career_id"], career_id["user_id"])
        if delstudent.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect("/lps4career/student/list")
    return render_to_response("mz_lps4/career/lps4studentList.html", studentdata, context_instance=RequestContext(request))

@dec_login_required
@handle_http_response_exception(501)
def revise_student(request):
    action = tool.get_param_by_request(request.POST, 'action', "", str)
    studentid = tool.get_param_by_request(request.POST, 'studentId', "", int)
    userid = tool.get_param_by_request(request.POST, 'userId', "", str)
    start_time = tool.get_param_by_request(request.POST, 'startTime', "NULL", str)
    end_time = tool.get_param_by_request(request.POST, 'endTime', "NULL", str)
    type = tool.get_param_by_request(request.POST, 'type', "", int)
    career_id = tool.get_param_by_request(request.POST, 'careerId', "", int)
    teacher_id = tool.get_param_by_request(request.POST, 'teacherId', "", str)
    stop_start_time = tool.get_param_by_request(request.POST, 'stopStartTime', "NULL", str)
    stop_end_time = tool.get_param_by_request(request.POST, 'stopEndTime', "NULL", str)
    is_stop = tool.get_param_by_request(request.POST, 'isStop', 0, int)
    if action == "revise":
        if stop_start_time == "NULL" or stop_start_time == "None":
            stop_start_time = None
        if stop_end_time == "NULL" or stop_start_time == "None":
            stop_end_time = None
        teacherid = lps4_studentData.query_exits(teacher_id)
        if teacherid.is_error():
            teacher_data = "教师数据错误，请输入正确教师账号！"
        else:
            teacherids = teacherid.result()
        if teacherids["count"] == 1:
            revisestudent = lps4_studentData.up_student(studentid, teacherids["id"], start_time, end_time, type, stop_start_time, stop_end_time, is_stop)
            if revisestudent.is_error():
                return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            if teacherids["count"] != 1:
                teacher_data = "教师账号有误，请输入正确教师账号！"
            revisestudent = lps4_studentData.student_revise(studentid)
            if revisestudent.is_error():
                return render_to_response("404.html", {}, context_instance=RequestContext(request))
            if revisestudent:
                revisest = revisestudent.result()["result"]
                revisest["teachername"] = teacher_id
                # for revisest in revisest:
                revisedata = {
                    "action": "revise",
                    "result": revisest,
                    "teacherr": teacher_data,
                }
                return render_to_response("mz_lps4/career/lps4studentrevise.html", revisedata, context_instance=RequestContext(request))
    if action == "add":   # 新增 uesrId, teacherId
        user_data = []
        teacher_data = []
        user_exit = lps4_studentData.query_exits(userid)
        careerdata = lps4_studentData.career_list()
        if user_exit.is_error():
            user_data = "用户数据错误"
        else:
            user_exits = user_exit.result()
        teacher_exit = lps4_studentData.query_exits(teacher_id)
        if teacher_exit.is_error():
            teacher_data = "教师数据错误"
        else:
            teacher_exits = teacher_exit.result()

        if user_exits["count"] == 1 and teacher_exits["count"] == 1:
            mcount = lps4_studentData.select_career_count(career_id)
            max_count = mcount.result()["result"]
            judeg_data = lps4_studentData.judeg_student(career_id, user_exits["id"])
            judeg_datas = judeg_data.result()
            if judeg_datas:
                judeg = "该用户在该专业下已有数据！"
                add_data = {
                "teacherId": teacher_id, "userId": userid, "startTime": start_time, "endTime": end_time,
                "type": type, "judeg": judeg,
                "careerlist": careerdata.result()["result"], "action": action,
                }
                return render_to_response("mz_lps4/career/lps4studentrevise.html", add_data, context_instance=RequestContext(request))
            else:
                addstudent = lps4_studentData.insert_student(user_exits["id"], start_time, end_time, type, career_id, teacher_exits["id"])
                if addstudent.is_error():
                    return render_to_response("404.html", {}, context_instance=RequestContext(request))
                else:
                    onevone_datas = lps4_studentData.onevone_count(career_id, user_exits["id"])
                    if onevone_datas.is_error():
                        print "onevone_meeting_user_count 数据错误"
                    else:
                        onevone_data = onevone_datas.result()
                        if onevone_data["count"] == 0:
                            addonevonecount = lps4_studentData.insert_onevone_count(career_id, user_exits["id"], max_count[0]["count"])
        else:
            if user_exits["count"] != 1:
                user_data = "用户不存在！"
            if teacher_exits["count"] != 1:
                teacher_data = "教师不存在！"
            # careerdata = lps4_studentData.career_list()
            add_data = {
                "teacherId": teacher_id, "userId": userid, "startTime": start_time, "endTime": end_time,
                "type": type, "user_data": user_data, "teacher_data": teacher_data,
                "careerlist": careerdata.result()["result"], "action": action,
            }
            return render_to_response("mz_lps4/career/lps4studentrevise.html", add_data, context_instance=RequestContext(request))
    if action == "reviseCareer":
        upcareer = lps4_studentData.up_student_career(studentid, career_id)
        if upcareer.is_error():
                    return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/lps4career/student/list")