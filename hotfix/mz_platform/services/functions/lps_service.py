# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_lps import ClassStudents
from mz_platform.orms.mz_lps import Class

from mz_platform.orms.course_models import CareerCourse


class LpsService(MZService):
    """LPS service

    """

    def __init__(self):
        super(LpsService, self).__init__()

    def get_registered_class(self, user_id, *args, **kwargs):
        """
        @brief 返回用户报名的班级

        @param user_id:
        @param args:
        @param kwargs:
        @return:
        """
        pass

    def get_registered_career_course(self, user_id, what='*'):
        """
        @brief 返回用户报名的职业课程, 报名的条件为：完全付款，且班级类型为正常班级

        @param user_id: 用户的id
        @param what: 查询字段
        @param conditions: 附加条件
        @param limit: 切片
        @param order_by: 排序
        @return:　职业课程信息字典的列表
        """
        sql = '''
            select cc.* from mz_course_careercourse as cc
            inner join mz_lps_class as c on cc.id = c.career_course_id and c.class_type = 0
            inner join mz_lps_classstudents as cs on c.id = cs.student_class_id and cs.deadline is Null
            where cs.user_id = %s
            ''' % user_id
        return self.execute(sql)
