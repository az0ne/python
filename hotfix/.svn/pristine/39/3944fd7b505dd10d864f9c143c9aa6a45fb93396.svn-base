# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.course_models import Lesson
from mz_platform.orms.mz_common import Discuss

class LessonService(MZService):
    """章节service

    """

    factory_functions = dict(lesson=Lesson)

    def __init__(self):
        """
        :return:
        """
        super(LessonService, self).__init__()

    def get_related_discuss(self, lesson_id, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取课程相关的评论

        @param lesson_id: 章节的ID
        @param what:
        @param conditions:
        @param limit:
        @param order_by:
        @return:
        """
        more_conditions = [(Discuss, ('object_id', 'object_type'), (lesson_id, 'LESSON')), ]
        data = Orm2Str.orm2str(what=what,
                               where=Discuss,
                               join=None,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)
