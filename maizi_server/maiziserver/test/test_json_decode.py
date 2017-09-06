# -*- coding: UTF-8 -*-
from django.test import TestCase
import json

from maiziserver.db.api.activity.activity import getYesterday
from maiziserver.tools.send_sms_message import send_sms_daily


class UtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_json_loads(self):
        """
        测试短信的返回的decode
        :return:
        """
        str = '{"Message":"触发业务级流控限制","RequestId":"CF4FEE2A-1BE0-422F-9E43-3D48BA21A2D2","Code":"isv.BUSINESS_LIMIT_CONTROL"}'

        a = json.loads(str)

        self.assertEqual(a['Code'], 'isv.BUSINESS_LIMIT_CONTROL')

    def test_send_message(self):
        """
        测试每日短信的发送
        :return:
        """

        params = {
            'name': '邓麒文',
            'vedio': 3,
            'test': 3,
            'task': 5,
            'order': 1,
            'coach': 2
        }

        result = send_sms_daily('15390496865', 10, params)
        self.assertEqual('OK', result['Code'])

    def test_send_message_0(self):
        """
        测试每日短信发送，学分为0
        :return:
        """

        params = {
            'name': '邓麒文'
        }
        result = send_sms_daily('15390496865', 0, params)
        self.assertEqual('OK', result['Code'])


    def test_get_yesterday(self):
        """
        测试获取昨天的日期
        :return:
        """

        result = getYesterday()
        print result



    def test_db_name_replace(self):

        from django.conf import settings


        sql_count = """
                        select 
                count(serverStudent.id) as studentcount
                from
                `dev_account_center`.mz_server_career_student as serverStudent
                left join 
                `dev_lps_20170707`.mz_user_userprofile as lpsUserProfile
                on serverStudent.account = lpsUserProfile.username
                inner join `dev_account_center`.mz_server_assistant as serverAssistant
                on serverStudent.assistant_id = serverAssistant.id
                inner join `dev_account_center`.mz_server_career as serverCareer 
                on serverStudent.career_id = serverCareer.id
                inner join `dev_account_center`.mz_server_assistant_communication as serverAssistantCommunication
                on serverAssistantCommunication.student_id = serverStudent.id
                where serverAssistantCommunication.communicate_at 
                =
                (select 
                max(communicate_at) 
                from `dev_account_center`.mz_server_assistant_communication
                where student_id 
                = 
                serverStudent.id)  
                and (student_name = %s or %s = '')
                and (career_job = %s or %s = -1)
                and (serverCareer.id = %s or %s = -1)
                """

        print settings.MAIZISERVERDB

        print sql_count.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)



