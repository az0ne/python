# -*- coding: utf8 -*-

import db.api

from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render

from utils import tool
from utils.logger import logger as log
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from mz_course.functions import ExportUserCareer


@dec_login_required
@handle_http_response_exception(501)
def user_career_list(request):
    action = tool.get_param_by_request(request.GET, 'action', default_val='show')
    export_type = tool.get_param_by_request(
        request.GET, 'export_type', default_val='current_page')

    mobile = tool.get_param_by_request(request.GET, 'mobile', 0, _type=int)
    career_name = tool.get_param_by_request(request.GET, 'career_name')
    nick_name = tool.get_param_by_request(request.GET, 'nick_name')
    email = tool.get_param_by_request(request.GET, 'email')

    start_date = tool.get_param_by_request(request.GET, 'start_date')
    end_date = tool.get_param_by_request(request.GET, 'end_date')

    page_index = tool.safe_positive_int(request.GET.get('page_index'), 1)
    page_size = tool.safe_positive_int(request.GET.get('page_size'), settings.PAGE_SIZE)

    if export_type == 'all' and action == 'export':  # 是否导出全部
        user_career_data = db.api.get_record_user_career_data(
            page_index, page_size, mobile, career_name, nick_name,
            email, date_range=(start_date, end_date), is_all=True)
    else:
        user_career_data = db.api.get_record_user_career_data(
            page_index, page_size, mobile, career_name, nick_name,
            email, date_range=(start_date, end_date))

    if user_career_data.is_error():
        log.warn('get record user career data failed. '
                 'mobile: {}'.format(mobile))
        user_career_data = {}
    else:
        user_career_data = user_career_data.result()

    user_career_data.update(s_mobile=mobile, s_career_name=career_name,
                            s_nick_name=nick_name, s_email=email,
                            s_start_date=start_date, s_end_date=end_date)

    if action == 'export':
        bio = ExportUserCareer(user_career_data['user_career_list']).export_bio()
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')

        fn = '学生感兴趣课程列表'
        condition = [mobile, mobile, career_name, nick_name,
                     email, start_date, end_date]
        try:
            fn += '_' + '_'.join([str(d) for d in condition if d])
        except:
            log.warn('create excel filename failed. '
                     'conditions:{}'.format(condition))
        if export_type != 'all':
            fn += '_第{}页'.format(page_index)
        fn += '.xls'

        response['Content-Disposition'] = 'attachment; filename=' + fn
        response['Content-Length'] = len(bio.getvalue())

        return response

    return render(
        request, 'mz_course/record/record_user_career_list.html', user_career_data)
