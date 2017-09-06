# -*- coding:utf-8-*-

from django.http import JsonResponse, HttpResponse
from utils.logger import logger as log
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

COMMON_RESPONSE = HttpResponse(
    content="service error",
    status=501,
    content_type="text/html")


# def set_response_status_code(response, code, error):
#     if isinstance(response, JsonResponse):
#         response.data = {"code": code, "error": error}
#     elif isinstance(response, HttpResponse):
#         response.content = error
#         response.status_code =
#     pass

def handle_ajax_response_exception(func):
    def _func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            code = 0
            return JsonResponse(dict(code=code, result=result))
        except ValueError, e:
            code = -1
            error = '参数错误'
            exception = e
        except IndexError, e:
            code = -2
            error = '索引错误'
            exception = e
        except TypeError, e:
            code = -3
            error = '类型错误'
            exception = e
        except MultiValueDictKeyError, e:
            code = -4
            error = '传值错误'
            exception = e
        except ObjectDoesNotExist, e:
            code = -5
            error = '数据不存在'
            exception = e
        except Exception as e:
            code = -6
            error = '数据不存在'
            exception = e
        log.error("views raised error: %s" % exception)
        return JsonResponse(dict(code=code, error=error))

    return _func


def handle_http_response_exception(status_code=501):
    """
    """

    def wrap(func):
        def _func(*args, **kwargs):
            try:
                resp = func(*args, **kwargs)
            except Exception, e:
                log.error("views raised error: %s" % e)
                resp = HttpResponse(content="service error")
                resp.status_code = status_code
                return resp
            else:
                return resp

        return _func

    return wrap


def ajaxErrorify(func):
    """
        集中处理异常装饰器
        成功返回{code:0, result:列表或者字典}
        错误返回{code:负数, error:错误信息}
    """

    def _deco(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            code = 0
            return JsonResponse(dict(code=code, result=result))
        except ValueError, e:
            code = -1
            error = '参数错误'
        except IndexError, e:
            code = -2
            error = '索引错误'
        except TypeError, e:
            code = -3
            error = '类型错误'
        except MultiValueDictKeyError, e:
            code = -4
            error = '传值错误'
        except ObjectDoesNotExist, e:
            code = -5
            error = '数据不存在'
        except Exception, e:
            code = -999
            error = e.message
        return JsonResponse(dict(code=code, error=error))

    return _deco
