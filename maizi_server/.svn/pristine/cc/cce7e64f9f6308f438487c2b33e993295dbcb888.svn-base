# -*- coding: utf-8 -*-

from contextlib import closing
from maiziserver.utils.logger import logger as log
# from maiziserver.db.cores.cache import cache
from maiziserver.db.cores.mysqlconn import get_conn


class APIResult(object):
    def __init__(self, result={}, code=True):
        self._result = result
        self._code = code

    def is_error(self):
        return not self._code

    def result(self):
        return self._result


# def dec_get_cache(key):
#     def wrap(func):
#         def _func(*args, **kwargs):
#             if kwargs.get("_enable_cache", False) == False:
#                return func(*args, **kwargs)

#             try:
#                 del kwargs["_enable_cache"]
#             except Exception:
#                 pass

#             # get cache
#             try:
#                 val = cache.get(key)
#             except Exception as e:
#                 return func(*args, **kwargs)

#             if val:
#                 return APIResult(result=val)
#             else:
#                 return func(*args, **kwargs)

#         return _func

#     return wrap

def dec_make_conn_cursor(func, *args, **kwargs):
    def _func(*args, **kwargs):
        # make connection and cursor
        _conn = get_conn()

        if not _conn:
            log.warn(
                "get database connection timeout.")
            return APIResult(code=False)

        with closing(_conn) as conn:
            _cursor = conn.cursor()
            if not (conn and _cursor):
                log.warn(
                    "cursor is none.")
                return APIResult(code=False)
            else:
                with closing(_cursor) as cursor:
                    try:
                        res = func(conn, cursor, *args, **kwargs)
                    except Exception as e:
                        return APIResult(code=False)
                    else:
                        return res
    return _func

# def use_cache(key, expire):
#     """
#     :param func:
#     :param key:
#     :param expire:
#     :return:
#     """
#     def wrap(func):
#         def _func(*args, **kwargs):
#             try:
#                 val = cache.get(key)
#             except Exception as e:
#                 return func(*args, **kwargs)
#             if val:
#                 return val
#             else:
#                 val = func(*args, **kwargs)
#                 if val:  # 只有函数执行成功时，才设置缓存
#                     try:
#                         cache.set(key, val, expire)
#                     except Exception as e:
#                         pass
#                 return val
#         return _func
#     return wrap
