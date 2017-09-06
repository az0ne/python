# -*- coding:utf-8 -*-
import datetime

from django.conf import settings
from django.http.response import JsonResponse, HttpResponse

from mz_operation.functions import get_7_days_ago, get_now, shortcut_date, build_volume_info, \
    build_customer_info, build_sem_info, get_new_students_list, get_student_info
from mz_operation.operation_api import OperationAPI
from utils.json_response import failed_json, success_json

__author__ = 'Administrator'

import time
import db.api.operationdata.equation
from django.http import HttpResponseRedirect, JsonResponse
from utils import tool
from db.api.operationdata import operationData
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from utils.decorators import dec_login_required, ajax_login_required, ajax_login_required_post
from utils.handle_exception import handle_http_response_exception
from utils.logger import logger as log
from utils.tool import get_param_by_request
import requests


@dec_login_required
@handle_http_response_exception(501)
def query_userclass(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    condition = ''
    if action == 'search':
        condition = tool.get_param_by_request(request.GET, 'condition', "", str)
        searchclasslist = operationData.searchclass(condition)
        if searchclasslist.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        c = {
            "classdata": searchclasslist.result()["result"],
            "condition": condition,
        }
        return render_to_response("mz_operation/operationuser.html", c, context_instance=RequestContext(request))
    else:
        return render_to_response("mz_operation/operationuser.html", {}, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def class_stage(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    careercourseid = tool.get_param_by_request(request.GET, 'careercourseid', "", int)
    userid = tool.get_param_by_request(request.GET, 'userid', "", int)
    if action == 'list':
        stagelist = operationData.stagelist(careercourseid, userid)
        stageold = operationData.selestage(userid, careercourseid)
        if stagelist.is_error() or stageold.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        c = {
            "stagelist": stagelist.result()["result"],
            "name": stagelist.result()["name_data"],
            "stageold": stageold.result()["stageexit"],
            "careercourseid": careercourseid,
        }
        return render_to_response("mz_operation/stagelist.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def change_stage(request):
    stagedata = request.POST.getlist("stageName")
    stageuserid = tool.get_param_by_request(request.POST, 'UserId', "", int)
    stagecarid = tool.get_param_by_request(request.POST, 'CarId', "", int)
    stageexitdata = operationData.selestage(stageuserid, stagecarid)
    exitdata = {
        "exitdata": stageexitdata.result()["stageexit"],
    }
    a = []
    for i in exitdata["exitdata"]:
        a.append(str(i["stage_id"]))
    if len(stagedata) > len(a):
        for item in stagedata:
            if item not in a:
                datalist = operationData.insertstage(item, stageuserid)
                if datalist.is_error():
                    return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif len(stagedata) < len(a):
        for item in a:
            if item not in stagedata:
                delelist = operationData.delestage(item, stageuserid)
                if delelist.is_error():
                    return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/operation/operation/list/")


@dec_login_required
@handle_http_response_exception(501)
def classdeadline(request):
    studentclass = tool.get_param_by_request(request.GET, 'classid', "", int)
    userid = tool.get_param_by_request(request.GET, 'userid', "", int)
    deadlinedata = operationData.seledeadline(studentclass, userid)
    deadline = deadlinedata.result()['deadline']
    deadlinetime = None
    if deadline:
        deadlinetime = deadline.strftime("%Y-%m-%dT%H:%M:%S")

    deadlineda = {
        "dldata": deadlinedata.result(),
        "deadline": deadlinetime,
        "userid": userid
    }
    if deadlinedata.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    else:
        return render_to_response("mz_operation/datadeadline.html", deadlineda,
                                  context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def updeadline(request):
    deadlinetime = tool.get_param_by_request(request.POST, 'deadline', "NULL", str)
    status = tool.get_param_by_request(request.POST, 'status', "", int)
    user_id = tool.get_param_by_request(request.POST, 'userId', "", int)
    class_id = tool.get_param_by_request(request.POST, 'classId', "", int)
    deadline = ""
    quit_datetime = ""
    if deadlinetime == "None" or deadlinetime == "NULL":
        deadline = None
    else:
        deadline = deadlinetime
    if status == 1:
        quit_datetime = None
    elif status == 2:
        quit_datetime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
    operationData.updeadline(deadline, status, user_id, class_id, quit_datetime)
    return HttpResponseRedirect("/operation/operation/list/")


@dec_login_required
@handle_http_response_exception(501)
def charts(request, chart_type):
    operation_api = OperationAPI()

    channels = operation_api.get_channels()
    # channels = None
    data = dict()

    if chart_type == 'line':
        variable_btns = operation_api.get_variable_btns()
        btns = variable_btns.items()
        variable_btns = [btns[i:i + 4] for i in xrange(0, len(btns), 4)]
        # variable_btns = [[['pv', 'pv'], ['uv', 'uv'], ['display', '渠道展示总量']]]

        equation_list = db.api.operationdata.equation.get_equation_list()
        if equation_list.is_error():
            log.warn('get equation list failed.')
            equation_list = []
        else:
            equation_list = equation_list.result()
        data.update(dict(variable_btns=variable_btns, equation_list=equation_list))

    data.update(channels=channels, chart_type=chart_type)

    return render(request, 'mz_operation/charts.html', data)


@ajax_login_required
def get_charts_data(request):
    operation_api = OperationAPI()

    channel = request.GET.get('channel', 'all')
    _type = request.GET.get('type', 'summarized')
    start_date = tool.get_param_by_request(request.GET, 'start_date', get_7_days_ago())
    end_date = tool.get_param_by_request(request.GET, 'end_date', get_now())
    shortcut = tool.get_param_by_request(request.GET, 'shortcut')

    if shortcut:
        start_date, end_date = shortcut_date(shortcut)

    params = {'from': start_date.replace('-', ''),
              'to': end_date.replace('-', ''),
              'channel': channel}

    if _type == 'mixedin':
        data = operation_api.get_mixed(params)

    elif _type == 'line':
        data = operation_api.get_timeline(params)

    elif _type == 'calc_line':
        data = operation_api.get_calc(params)

    elif _type == 'channel_summarized':
        data = operation_api.get_summarized(params, channel=True)

    else:
        data = operation_api.get_summarized(params)

    data.update(start_date=start_date, end_date=end_date)

    return JsonResponse(data)


@ajax_login_required
def equation_options(request):
    action = request.POST.get('action', 'add')

    if action == 'add':
        equation = request.POST.get('equation')
        description = request.POST.get('description')

        if equation and description:
            e_id = db.api.operationdata.equation.add_equation(equation, description)
            if e_id.is_error():
                log.warn('add equation failed. '
                         'equation: {0}, description: {1}'.format(equation, description))
                return failed_json(u'添加公式失败，请重试。', code=500)
            else:
                e_id = e_id.result()
                return success_json({'id': e_id})
        return failed_json(u'公式和描述为必填项。')

    elif action == 'delete':
        e_id = request.POST.get('id')

        res = db.api.operationdata.equation.del_equation(e_id)
        if res.is_error():
            log.warn('del equation failed. e_id: {0}'.format(e_id))
            return failed_json(u'删除公式失败，请重试。', code=500)
        return success_json()

    else:
        return failed_json(u'无此action。')


@ajax_login_required_post
def execl_import(request):
    if request.method == 'GET':
        _type = request.GET.get('type', 'entry')
        return render(request, 'mz_operation/excel_import.html', dict(type=_type))
    else:
        excel = request.FILES.get('excel')
        _type = request.POST.get('type')
        api = OperationAPI()

        dispatch = {
            'volume_info': lambda x: api.upload_volume_info(build_volume_info(x)),
            'customer_info': lambda x: api.upload_customer_info(build_customer_info(x)),
            'sem_info': lambda x: api.upload_sem_info(build_sem_info(x))
        }

        if excel and _type in dispatch.keys():
            try:
                return JsonResponse(dispatch[_type](excel.file.getvalue()))
            except Exception, e:
                return failed_json(unicode(e))
        return failed_json(u'请选择要上传的excel。')


@dec_login_required
@handle_http_response_exception(501)
def new_student_render(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    try:
        if action == 'query':
            page_index = get_param_by_request(request.GET, 'page_index', 1, int)
            template = 'mz_operation/new_students.html'
            data = get_new_students_list(page_index=page_index)
        elif action == 'show':
            template = 'mz_operation/new_student_show.html'
            student_id = get_param_by_request(request.GET, 'student_id', 0, int)
            career_id = get_param_by_request(request.GET, 'career_id', 0, int)
            data = get_student_info(student_id, career_id)
    except Exception as e:
        message = 'get data from new students API failed.info:%s' % e
        log.warn(message)
        return HttpResponse(message)
    data.update(dict(action=action))
    return render(request, template, data)


@dec_login_required
@handle_http_response_exception(501)
def test_funnel_charts(request):
    start_date = datetime.datetime.today().replace(day=1).strftime("%Y-%m-%d")
    today = datetime.datetime.today()
    
    if today.month == 12:
        end_date_funnel = today.replace(year=today.year+1, month=1, day=1)
    else:
        end_date_funnel = today.replace(month=today.month+1, day=1)

    end_date_funnel = end_date_funnel.strftime("%Y-%m-%d")

    end_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        user_deps = requests.get(
            "%s/api/data/ikcrm/userdeps" % settings.OPERATION_API_HOST,
            timeout=2).json()["result"]["data"]
    except Exception as e:
        return HttpResponse("some error from api. details: %s" % e)

    deps = map(lambda x: x[0], user_deps)
    users = map(lambda x: x[1], user_deps)[0]

    return render(
        request,
        'mz_operation/funnel_charts.html',
        {'start_date': start_date, 'end_date': end_date, 'end_date_funnel': end_date_funnel, 'user_deps': deps, "users": users})


@dec_login_required
@handle_http_response_exception(501)
def funnel_chart_ajax(request):
    start_date = get_param_by_request(request.GET, 'funnel_start_date', "", str)
    end_date = get_param_by_request(request.GET, 'funnel_end_date', "", str)
    department_name = get_param_by_request(request.GET, 'funnel_department_name', "", str)
    username = get_param_by_request(request.GET, 'funnel_username', "", str)

    if start_date and end_date:
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        api_url = "%s/api/data/ikcrm/funnel/seller" % settings.OPERATION_API_HOST
        try:
            data = {
                'from': start_date.replace("-", ""),
                'to': end_date.replace("-", ""),
                "department_name": department_name,
                "user_name": username
            }
            result_json = requests.get(url=api_url, params=data, timeout=5).json()
            data = result_json.get('result').get('data')
            funnel_data = []
            for i in xrange(len(data)):
                if i % 2 == 0:
                    funnel_data.append(dict(name=data[i], value=data[i + 1]))
            return JsonResponse(
                {'status': 'success', 'data': funnel_data, 'start_date': start_date, 'end_date': end_date})
        except Exception as e:
            log.warn('get data from operation failed. info: %s' % e)
    return JsonResponse({'status': 'failed'})


@dec_login_required
@handle_http_response_exception(501)
def user_chart_ajax(request):
    department_name = get_param_by_request(request.GET, 'department_name', "", str)

    api_url = "%s/api/data/ikcrm/users" % settings.OPERATION_API_HOST    

    try:
        data = {'department_name': department_name}
        result_json = requests.get(url=api_url, params=data, timeout=5).json()
        users = result_json.get('result').get('data')
        return JsonResponse(
            {'status': 'success', 'users': users})
    except Exception as e:
        log.warn('get data from operation failed. info: %s' % e)
        
    return JsonResponse({'status': 'failed'})


@dec_login_required
@handle_http_response_exception(501)
def sale_line_chart(request):
    start_date = get_param_by_request(request.GET, 'line_start_date',
                                      datetime.datetime.today().replace(day=1).strftime("%Y-%m-%d"), str)
    end_date = get_param_by_request(request.GET, 'line_end_date', datetime.datetime.today().strftime("%Y-%m-%d"), str)
    department_name = get_param_by_request(request.GET, 'line_department_name', "", str)
    username = get_param_by_request(request.GET, 'line_username', "", str)
    type = get_param_by_request(request.GET, 'api_type', 'count', str)
    if type == "count":
        api_url = "%s/api/data/ikcrm/timeline/count" % settings.OPERATION_API_HOST
    elif type == "amount":
        api_url = "%s/api/data/ikcrm/timeline/amount" % settings.OPERATION_API_HOST
    elif type == "seller":
        api_url = "%s/api/data/ikcrm/timeline/seller" % settings.OPERATION_API_HOST
    elif type == "history":
        api_url = "%s/api/data/ikcrm/timeline/history/seller" % settings.OPERATION_API_HOST
    if start_date and end_date:
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        try:
            data = {
                'from': start_date.replace("-", ""),
                'to': end_date.replace("-", ""),
                "department_name": department_name,
                "user_name": username
            }
            result_json = requests.get(url=api_url, params=data, timeout=5).json()
            api_data = result_json.get('result').get("data")
            dates = []  # 折线图x轴数据，日期
            data = []  # 折线图数据部分 包含name和value列表
            for date in api_data:
                dates.append(date)
            dates.sort()
            if not data:
                if len(dates) != 0:
                    for name in api_data.get(dates[0]):
                        data.append({'name': name, 'type': 'line', 'data': []})
                
            for date in dates:
                result = api_data.get(date, [])
                for name in result:
                    for d in data:
                        if name in d.get('name'):
                            d.get('data').append(result.get(name))
            return JsonResponse(
                {'dates': dates, 'data': data, 'status': 'success', 'start_date': start_date, 'end_date': end_date})
        except Exception as e:
            log.warn('get data from operation failed. info: %s' % e)
    return JsonResponse({'status': 'failed'})
