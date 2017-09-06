# -*- coding: utf-8 -*-

"""
定义与Django基于角色访问控制机制有关的类，该类应该是在django框架内实现的

@todo 研究django的基于角色访问控制机制，以更加优雅的方式实现这些中间类，而不是简单的实现
"""
__author__ = 'changfu'

from mz_platform.orms.mz_db_model import MZDBModel

class UserProfileGroups(MZDBModel):
    db_table = 'mz_user_userprofile_groups'


class AuthGroup(MZDBModel):
    db_table = 'auth_group'