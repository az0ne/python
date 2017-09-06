# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from db.api.usercenter.message import list_my_message_by_page, update_message
from utils.tool import get_param_by_request
from django.http.response import Http404


@login_required(login_url="/")
def my_message(request):
    page_index = get_param_by_request(request.GET, 'page', 1, int)
    pre_page = page_index - 1
    if page_index <= 1:
        page_index = 1
        pre_page = 1
    page_size = 10
    user = request.user
    if user.is_teacher():
        message_type = ['51', '22', '23']
    else:   # 教务暂无添加
        message_type = ['50', '11', '21', '22']
    api_ret = list_my_message_by_page(user.id, page_index, page_size, message_type)
    if api_ret.is_error():
        raise Http404
    messages = api_ret.result()['messages']
    page_count = api_ret.result()['page_count']
    rows_count = api_ret.result()['rows_count']
    if (not messages) and rows_count > 0:
        api_ret = list_my_message_by_page(user.id, page_count, page_size, message_type)
        messages = api_ret.result()['messages']
        page_count = api_ret.result()['page_count']
        rows_count = api_ret.result()['rows_count']

    page_count_list = range(1, page_count + 1)

    next_page = page_index + 1
    if next_page > page_count:
        next_page = page_count
    if pre_page >= page_count:
        pre_page = page_count - 1
    if page_count in [0, 1]:
        pre_page = 1
        next_page = 1

    # 更新消息状态为已读
    update_message(user.id, message_type)
    return render(request, 'mz_user/user_mymessage_view.html', {'message_list': messages,
                                                                'page_count': page_count,
                                                                'rows_count': rows_count,
                                                                'page_index': page_index,
                                                                'pre_page': pre_page,
                                                                'next_page': next_page,
                                                                'page_count_list': page_count_list})
