# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_common import Banner

class BannerService(MZService):
    """课程service

    @note get_course 和 get_all_course 在基类MZService中动态生成, 定义如下：
          get_course(what='*', conditions=None, limit=None, order_by=None)
          get_all_course(what='*', limit=None, order_by=None)
    """

    factory_functions = dict(banner=Banner)

    def __init__(self):
        """
        :return:
        """
        super(BannerService, self).__init__()
