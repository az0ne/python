# -*- coding: utf-8 -*-

__author__ = 'changfu'

import os, sys
import unittest
print sys.path.insert(0, os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django
django.setup()

from base_test_case import CustomerTestCase
from django.db import connection
from mz_platform.services.functions.article_type_service import ArticleTypeService



class TestArticleTypeService(CustomerTestCase):

    cases = dict(get_article_type=[dict(arg=None,
                                        sql='''select na.* from %(tb_articletype)s as na'''
                                            % dict(tb_articletype='mz_common_articletype')
                                        ),
                                   dict(arg=dict(what=['id', 'name'],
                                                 conditions=['id>1'],
                                                 limit='2',
                                                 order_by='-id'),
                                        sql='''select na.id, na.name from %(tb_articletype)s as na
                                               where na.id>1 order by -id  limit 2'''
                                            % dict(tb_articletype='mz_common_articletype')
                                        )
                                   ],
                 get_all_article_type=[dict(arg=None,
                                            sql='''select na.* from %(tb_articletype)s as na'''
                                            % dict(tb_articletype='mz_common_articletype')
                                            ),
                                       dict(arg=dict(what=['id', 'name'],
                                                     limit='2',
                                                     order_by='-id'),
                                            sql='''select na.id, na.name from %(tb_articletype)s as na
                                                   order by -id  limit 2'''
                                                % dict(tb_articletype='mz_common_articletype')
                                            ),
                                       ],
                 get_related_articles=[dict(arg=dict(article_type_id=2),
                                            sql='''select na.* from %(tb_article)s as na
                                                   where na.article_type_id=2'''
                                                % dict(tb_article='mz_common_newarticle')
                                            ),
                                       dict(arg=dict(article_type_id=2,
                                                     what=['id', 'title'],
                                                     conditions=['id>1'],
                                                     limit='2',
                                                     order_by='-id'),
                                            sql='''select na.id, na.title from %(tb_article)s as na
                                                   where na.article_type_id=2 and na.id>1
                                                   order by -na.id limit 2''' % dict(tb_article='mz_common_newarticle')
                                            ),
                                       ],
                 )

    def setUp(self):
        """

        @return:
        """
        self.cursor = connection.cursor()
        self.service = ArticleTypeService()

    def test_all(self):
        for case in self.cases:
            self.run_case(case)

if __name__ == '__main__':
    unittest.main()
