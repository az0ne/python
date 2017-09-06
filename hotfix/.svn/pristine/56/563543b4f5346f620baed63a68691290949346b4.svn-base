# -*- coding: utf-8 -*-

"""
@version: 2016/3/31
@author: Jackie
@contact: jackie@maiziedu.com
@file: middleware.py
@time: 2016/3/31 0:20
@note:  ??
"""
import sys
import time
from django.http.response import Http404
from django.conf import settings

logger = settings.SYSLOGGER
acs_logger = settings.ACSLOGGER


class LogMiddleware(object):
    """记录所有异常,并抛出友好错误页面"""

    def process_request(self, request):
        request._startline = time.time()

    def process_response(self, request, response):
        method = request.method
        url = request.get_host() + request.get_full_path()
        referer = request.META.get('HTTP_REFERER')
        status_code = response.status_code
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated() else None
        time_cost = time.time() - request._startline
        remote_ip = request.META.get('REMOTE_ADDR')
        x_forward_for = request.META.get('HTTP_X_FORWARD_FOR')
        x_real_ip = request.META.get('HTTP_X_REAL_IP')

        msg = '[%s][%s][%s][%s][%sms][%s][%s][%s]' % (
            method, url, status_code, user_id,
            int(time_cost * 1000), remote_ip, x_forward_for, x_real_ip
        )

        acs_logger.info(msg)
        return response

    def process_exception(self, request, exception):
        """
        在response过程截取错误信息
        :param request:
        :param exception:
        :return:
        """
        if request.is_ajax():
            return

        try:
            # sys.exc_info()包含了traceback信息
            logger.error('Internal Server Error: %s', request.path,
                         exc_info=sys.exc_info(),
                         extra={
                             'status_code': 500,
                             'request': request,
                         },
                         )
        # 如果写入错误日志的过程出错, 写入特殊的LoggerMiddleware error信息
        except Exception:
            logger.error('LoggerMiddleware Error: %s', request.path,
                         exc_info=sys.exc_info(),
                         )

        # 上线时请把settings.DEBUG调成False
        if settings.DEBUG == False:
            raise Http404
