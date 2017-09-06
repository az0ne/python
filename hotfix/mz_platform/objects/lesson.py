#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper
from mz_platform.apis.course_sys_api import CourseSysApi


class Lesson(SqlResultWrapper):
    """
    id'
    name'
    video_url
    video_length
    play_count
    share_count
    index
     is_popup
     course_id
     seo {seo_description, seo_keyword, seo_title}
     have_homework
     code_exercise_type
    """

    @property
    def course(self):
        if not self._course:
            api = CourseSysApi.default_instance()
            r = api.get_one_course(id=self.course_id)
            if not r:
                return None
            self._course = r.obj
        return self._course

    @property
    def course_id(self):
        return self['course_id']

    @property
    def play_count(self):
        return int(self['play_count'])

    @play_count.setter
    def play_count(self, value):
        x = self.play_count
        x += 1
        self['play_count'] = str(x)

    @property
    def homework(self):
        """
        @brief get homework obj if exsit, otherwise None

        @todo need api support
        """
        return None
        # if not self.have_homework:
        #     return None

        # if not self._homework:
        #     api = CourseSysApi.default_instance()
        #     self._homework = .get
        #     {"description": "", "upload_file": "", "code_exercise_type": 0}
        # return self._homework
