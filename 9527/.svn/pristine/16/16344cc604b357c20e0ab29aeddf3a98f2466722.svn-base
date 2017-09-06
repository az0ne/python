# -*- coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from mz_lps4.interface import get_lps4_student_info_for_health, update_student_health_info, \
    export_lps4_student_info_for_health, student_health_excel_export_format
import datetime


@dec_login_required
@handle_http_response_exception(501)
def student_health_list(request):
    action = get_param_by_request(request.GET, 'action', 'query', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    keyword = get_param_by_request(request.GET, 'keyword', '', str)
    start_time = get_param_by_request(request.GET, 'start_time',
                                      datetime.date.today().replace(day=1).strftime('%Y-%m-%d'), str)
    end_time = get_param_by_request(request.GET, 'end_time', datetime.date.today().strftime('%Y-%m-%d'), str)
    try:
        if 'excel' in action:
            students_info = export_lps4_student_info_for_health(keyword="%" + keyword + "%")
        else:
            students_info = get_lps4_student_info_for_health(page_index=page_index, keyword="%" + keyword + "%")
        students = students_info.get('result')
        students = update_student_health_info(students, start_time=start_time, end_time=end_time)
        if 'excel' in action:
            return student_health_excel_export_format(students=students, start_time=start_time, end_time=end_time,
                                                      keyword=keyword)
    except Exception as e:
        return render(request, '404.html', {'message': e})
    c = {"students": students, 'keyword': keyword, 'start_time': start_time, 'end_time': end_time,
         "page": {"page_index": page_index, "rows_count": students_info["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": students_info["page_count"]}}
    return render(request, "mz_lps4/student_health_list.html", c)
