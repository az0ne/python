#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging

from mz_platform.objects.mz_object import MZObject


def log_it(content):
    """
    @brief shortcut for call default logger

    """
    LogService.get_sys_log().debug(content)


class LogService(MZObject):

    @staticmethod
    def get_biz_log():
        """
        获取mz_sys_log
        :return:
        """
        return logging.getLogger('mz_biz_log')

    @staticmethod
    def get_sys_log():
        """
        获取mz_sys_log
        :return:
        """
        return logging.getLogger('mz_sys_log')

    @staticmethod
    def get_acs_log():
        """
        获取mz_sys_log
        :return:
        """
        return logging.getLogger('mz_acs_log')
