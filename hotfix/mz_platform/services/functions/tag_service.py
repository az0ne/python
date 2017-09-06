# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService

from mz_platform.orms.course_models import Tag


class TagService(MZService):
    """Article 服务

    @note 方法get_article, get_all_article由基类支持
    """

    factory_functions = dict(tag=Tag)

    def __init__(self):
        """
        :return:
        """
        super(TagService, self).__init__()
