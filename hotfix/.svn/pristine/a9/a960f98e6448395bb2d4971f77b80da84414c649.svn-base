# -*- coding: utf-8 -*-

__author__ = 'changfu'

import unittest
from mz_platform.utils.debug_tool import deb_print

class CustomerTestCase(unittest.TestCase):
    """

    """

    def sql_execute(self, sql):
        """

        @param sql:
        @return:
        """
        deb_print(sql=sql)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return list(dict(zip([x[0] for x in self.cursor.description], item)) for item in data)

    def log_result(self, case_name, case_number):
        """

        @param case_name:
        @param case_number:
        @return:
        """
        print '*' * 20
        print 'SUCCESS: %s: %s' % (case_name, case_number)
        print '*' * 20

    def run_case(self, f_name):
        for index, case in enumerate(self.cases[f_name]):
            func = getattr(self.service, f_name)
            if case['arg']:
                rrs = func(**case['arg'])
            else:
                rrs = func()
            ers = self.sql_execute(case['sql'])
            self.assertTrue(rrs)
            self.assertEqual(rrs, ers)
            self.log_result(f_name, index+1)
