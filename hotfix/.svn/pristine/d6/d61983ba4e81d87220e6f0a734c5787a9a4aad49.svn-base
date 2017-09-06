# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_user import UserProfile
from mz_platform.orms.mz_user import UserProfileGroups
from mz_platform.orms.mz_user import AuthGroup
from mz_platform.orms.mz_common import ObjSEO


class UserService(MZService):
    """
    业务逻辑耦合服务类，数据由ModelXXXService类提供
    """

    factory_functions = {'user': UserProfile,
                         }

    def __init__(self):
        """
        :return:
        """
        super(UserService, self).__init__()

    def get_all_teacher(self, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取全部teacher

        @param what: 查询字段
        @param conditions: 条件
        @param limit: 数据分片
        @param order_by: 排序
        @return 包含老师信息字典的列表
        """
        more_conditions = [(AuthGroup, ('name', ), ('老师', )), ]
        data = Orm2Str.orm2str(what=what,
                               where=UserProfile,
                               join=[('inner', (UserProfileGroups, UserProfile), ('userprofile_id', 'id')),
                                     ('inner', (AuthGroup, UserProfileGroups), ('id', 'group_id'))],
                               more_conditions=more_conditions,
                               conditions=conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_registered_career_course(self, what='*'):
        pass

    def get_teacher_seo(self, teacher_id, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取teacher的seo

        @param teacher_id:
        @return:
        """
        more_conditions = [(ObjSEO, ('obj_id', 'obj_type'), (teacher_id, 'TEACHER')), ]
        data = Orm2Str.orm2str(what=what,
                               where=ObjSEO,
                               join=None,
                               more_conditions=more_conditions,
                               conditions=conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)
