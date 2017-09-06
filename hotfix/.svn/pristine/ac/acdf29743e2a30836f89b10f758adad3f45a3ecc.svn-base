# -*- coding: utf-8 -*-

"""
service 单元测试用例

@note 目前所有的case均基于unittest.TestCase(而非基于), 因为service采用sql实现，并未强依赖django的Model及ORM实现。
"""

__author__ = 'changfu'

import os, sys
import unittest
print sys.path.insert(0, os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django
django.setup()

from base_test_case import CustomerTestCase
from django.db import connection
from mz_platform.services.functions.course_service import CourseService





class TestCourseService(CustomerTestCase):

    cases = dict(get_course=[dict(arg=None,
                                  sql='''select * from mz_course_course'''
                                  ),
                             dict(arg=dict(what=['id', 'name'],
                                           conditions=['id>1'],
                                           limit='2',
                                           order_by='-id'),
                                  sql='''select id, name from mz_course_course where id>1 order by -id limit 2'''
                                  ),
                             ],
                 get_all_course=[dict(arg=None,
                                      sql='''select * from mz_course_course'''
                                      ),
                                 dict(arg=dict(what=['id', 'name'],
                                               limit='2, 3',
                                               order_by='-id'),
                                      sql='''select id, name from mz_course_course order by -id limit 2, 3'''
                                      ),
                                 ],
                 get_related_career_courses=[dict(arg=dict(course_id=396),
                                                  sql='''select %(tb_career_course)s.* from %(tb_career_course)s
                                                         inner join %(tb_career_obj_relation)s
                                                         on %(tb_career_obj_relation)s.career_id = %(tb_career_course)s.id
                                                         where %(tb_career_course)s.id = %(id)s'''
                                                      % dict(tb_career_course='mz_course_course',
                                                             tb_career_obj_relation='mz_common_careerobjrelation',
                                                             id=396)
                                                  ),
                                             dict(arg=dict(course_id=396,
                                                           what=['id', 'name'],
                                                           conditions=['name like "%python%"'],
                                                           limit='2',
                                                           order_by='-id'),
                                                  sql='''select %(tb_career_course)s.id, %(tb_career_course)s.name
                                                         from %(tb_career_course)s
                                                         inner join %(tb_career_obj_relation)s
                                                         on %(tb_career_obj_relation)s.career_id = %(tb_career_course)s.id
                                                         where %(tb_career_course)s.id = %(id)s
                                                         and %(tb_career_course)s.name like "%%python%%"
                                                         order by -%(tb_career_course)s.id
                                                         limit 2'''
                                                      % dict(tb_career_course='mz_course_course',
                                                             tb_career_obj_relation='mz_common_careerobjrelation',
                                                             id=396)

                                                  ),
                                             ],
                 get_related_tags=[dict(arg=dict(course_id=736),
                                        sql='''select t.* from %(tb_tag)s as t
                                               inner join %(tb_objtagrelation)s as otr
                                               on otr.tag_id = t.id
                                               where otr.obj_id = %(course_id)s and otr.obj_type='COURSE'
                                        ''' % dict(tb_tag='mz_course_tag',
                                                   tb_objtagrelation='mz_common_objtagrelation',
                                                   course_id=736)
                                        ),
                                   dict(arg=dict(course_id=736,
                                                 what=['id', 'name'],
                                                 conditions=['name like "%python%"'],
                                                 limit='2',
                                                 order_by='-id'),
                                        sql='''select t.id, t.name from %(tb_tag)s as t
                                                inner join %(tb_objtagrelation)s as otr
                                                on otr.tag_id = t.id
                                                where otr.obj_id = %(course_id)s and otr.obj_type='COURSE'
                                                and t.name like '%%python%%'
                                                order by -t.id
                                                limit 2'''
                                            % dict(tb_tag='mz_course_tag',
                                                   tb_objtagrelation='mz_common_objtagrelation',
                                                   course_id=736)
                                        ),
                                   ],
                 get_course_by_career_tag=[dict(arg=None,
                                                sql='''select c.* from %(tb_course)s as c
                                                       inner join %(tb_objtagrelation)s as otr
                                                       on otr.obj_id = c.id
                                                       where otr.obj_type = "COURSE"'''
                                                    % dict(tb_course='mz_course_course',
                                                           tb_objtagrelation='mz_common_objtagrelation')
                                                ),
                                           dict(arg=dict(career_category_id=10,
                                                         tag_id=10,
                                                         what=['id', 'name'],
                                                         conditions=['name like "%python%"'],
                                                         limit='2',
                                                         order_by='-id'),
                                                sql='''select c.id, c.name from %(tb_course)s as c
                                                       inner join %(tb_objtagrelation)s as otr
                                                       on otr.obj_id = c.id
                                                       where otr.obj_type = "COURSE" and otr.tag_id = 10
                                                       and otr.careercatagory_id = 10 and c.name like "%%python%%"
                                                       order by -c.id
                                                       limit 2'''
                                                    % dict(tb_course='mz_course_course',
                                                           tb_objtagrelation='mz_common_objtagrelation')
                                                ),
                                           ],
                 )

    def setUp(self):
        """

        @return:
        """
        self.cursor = connection.cursor()
        self.service = CourseService()

    def test_all(self):
        for case in self.cases:
            self.run_case(case)


if __name__ == '__main__':
    unittest.main()
