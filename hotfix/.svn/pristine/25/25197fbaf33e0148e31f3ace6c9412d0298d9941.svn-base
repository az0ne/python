#!/usr/bin/env python
# -*- coding: utf8 -*-

import base_sys_api

from mz_platform.utils.decorator_tool import api_except_catcher


class BannerSysApi(base_sys_api.BaseSysApi):
    """
    @brief BannerSysApi
    """

    _api = None

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not BannerSysApi._api:
            BannerSysApi._api = BannerSysApi()
        return BannerSysApi._api

    @api_except_catcher
    def get_all_banner(self):
        """
        @brief 获取所有banner对象

        """
        r = self.banner_service.get_all_banner(order_by='mz_common_banner.index')  # index为mysql保留字，暂时用mz_common_banner.index
        return self.n_obj('Banner', r)
