# -*- coding: utf8 -*-

from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception


# @dec_login_required
@handle_http_response_exception(501)
def edit_reply(request):
    return render(request, 'mz_wechat/reply_edit.html', dict(action='add'))
