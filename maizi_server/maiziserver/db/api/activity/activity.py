# -*- coding: utf-8 -*-
"""
Created on 2017-

@author: tyan4g@sina.com
"""

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

from django.conf import settings

print settings.MAIZISERVERDB  # dev_account_center
print settings.MAIZILPSDB  # dev_lps_20170707


class InvalidParamException(Exception):
    """

    :param Exception:
    :return: 自定义的异常
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MysqlQueryException(Exception):
    """

        :param Exception:
        :return: 自定义的异常
        """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def list_learn_activity(student_name, career_job, career_id, skip):
    """
    :param student_name: 学生的姓名
    :param career_job: 课程类型，包括线上和线下
    :param skip: 分页的标记
    :param career_id: 专业的编号
    :return: 查询出来的学习活跃记录列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

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

        sql_count = sql_count.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707',
                                                                                            settings.MAIZILPSDB)

        sql = """
            select
                serverStudent.phone,
                serverStudent.student_name as studentName,
                lpsUserProfile.last_login,
                lpsUserProfile.id as student_id,
                serverStudent.assistant_id,
                serverAssistant.name as assistant_name,
                serverCareer.name as career_name,
                serverAssistantCommunication.communicate_at as last_communication_date,
                sum(serverActive.total_score) as total_score,
                sum(serverActive.consecutive_days) as consecutive_days,

                case serverStudent.career_job
                when 1 then '就业'
                else '非就业'
                end
                as job_type
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
                inner join `dev_account_center`.mz_server_active_point as serverActive
                on serverStudent.id = serverActive.student_id
                where serverAssistantCommunication.communicate_at
                =
                (select
                max(communicate_at)
                from `dev_account_center`.mz_server_assistant_communication
                where student_id
                =
                serverStudent.id)
                and (serverStudent.student_name = %s or %s = '')
                and (career_job = %s or %s = -1)
                and (serverCareer.id = %s or %s = -1)
                GROUP BY serverStudent.student_name
                limit %s, %s
        """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707',
                                                                                settings.MAIZILPSDB)

        try:
            cursor.execute(sql_count, (student_name, student_name,
                                       career_job, career_job,
                                       career_id, career_id
                                       )
                           )
            rows_count = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql, (student_name, student_name,
                                 career_job, career_job,
                                 career_id, career_id,
                                 skip["limit"], skip["offset"],
                                 )
                           )
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
            "result": info,
            "rows_count": rows_count["studentcount"],
        }

        return APIResult(result=result_dict)

    return main()


def list_watched_videos(started_at):
    """
    :param started_at 某天的日期, 必须是python date,
    :return: 返回某天学员观看视频数量的列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
              select count(kr.`student_id`) as watch_num  , kr.`student_id`, userProfile.username  from `dev_lps_20170707`.mz_lps3_userknowledgeitemrecord as kr
                inner join `dev_lps_20170707`.mz_lps3_knowledgeitem as k
                on kr.knowledge_item_id = k.id
                and k.obj_type="LESSON"
                inner join `dev_lps_20170707`.mz_user_userprofile as userProfile
                on userProfile.id = kr.student_id
                inner join `dev_account_center`.mz_server_career_student as serverStudent
                on serverStudent.account = userProfile.username
                where kr.status="DONE"
                and kr.done_time >= date(%s)
                and kr.done_time < date_add(%s, INTERVAL 1 DAY)
                group by student_id
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at), str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_c ount["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_finish_exercises(started_at):
    """

    :param started_at: 某一天的时间必须是python datetime.date对象
    :return: 学员完成的练习的列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                  select count(kr.`student_id`) as watch_num  , kr.`student_id`, userProfile.username  from `dev_lps_20170707`.mz_lps3_userknowledgeitemrecord as kr
                    inner join `dev_lps_20170707`.mz_lps3_knowledgeitem as k
                    on kr.knowledge_item_id = k.id
                    and k.obj_type="TEST"
                    inner join `dev_lps_20170707`.mz_user_userprofile as userProfile
                    on userProfile.id = kr.student_id
                    inner join `dev_account_center`.mz_server_career_student as serverStudent
                    on serverStudent.account = userProfile.username
                    where kr.status="DONE"
                    and kr.done_time >= date(%s)
                    and kr.done_time < date_add(%s, INTERVAL 1 DAY)
                    group by student_id
                    """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at), str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_finish_task(started_at):
    """

    :param started_at: 某一天的时间必须是python datetime.date对象
    :return: 学员完成的任务的列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                select count(userRecord.student_id) as num, userRecord.student_id ,userProfile.username from dev_lps_20170707.mz_lps3_usertaskrecord as userRecord
                inner join dev_lps_20170707.mz_user_userprofile as userprofile
                on userRecord.student_id = userprofile.id
                inner join dev_account_center.mz_server_career_student as serverStudent
                on serverStudent.account = userprofile.username
                where userRecord.status="PASS"
                and userRecord.done_time >= date(%s)
                and userRecord.done_time < date_add(%s, INTERVAL 1 DAY)
                group by userRecord.student_id;
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at), str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_booking_cources(started_at):
    """

    :param started_at: 某一天的时间必须是python datetime.date对象
    :return: 学员约课次数列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                select count(backlog.user_id) as num,backlog.user_id ,userprofile.username from dev_lps_20170707.mz_lps4_teacher_warning_backlog as backlog
                inner join dev_lps_20170707.mz_user_userprofile as userprofile
                on backlog.user_id = userprofile.id
                inner join dev_account_center.mz_server_career_student as serverstudent
                on userprofile.username = serverstudent.account
                where backlog.type='5' and backlog.is_done='1'
                and backlog.create_date >= date(%s)
                and backlog.create_date < date_add(%s, INTERVAL 1 DAY)
                group by backlog.user_id;
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at), str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_ask_question(started_at):
    """

    :param started_at: 某一天的时间必须是python datetime.date对象
    :return: 学员发起辅导次数列表
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                select count(coach.student_id) as num,student_id, userprofile.username from dev_lps_20170707.mz_coach as coach
                inner join dev_lps_20170707.mz_user_userprofile as userprofile
                on coach.student_id = userprofile.id
                inner join dev_account_center.mz_server_career_student as serverstudent
                on serverstudent.account = userprofile.username
                where coach.source_type in (10,11)
                and coach.create_date >= date(%s)
                and coach.create_date < date_add(%s, INTERVAL 1 DAY)
                group by coach.student_id
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at), str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def consecutive_days():
    """
    :return: 学员连续未学习的天数
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select userprofile.last_login ,userprofile.username, student_id
                from dev_account_center.mz_server_career_student as serverStudent
                inner join dev_lps_20170707.mz_user_userprofile as userprofile
                on serverStudent.account = userprofile.username
                group by serverStudent.student_id;
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, )
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_active_student(started_at):
    """
    :param 当天的时间，必须是python的字符串
    :return: 返回所有的学员（不包含结业，毕业和休学的学员）
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                    SELECT id, phone, student_name, account FROM dev_account_center.mz_server_career_student
                    where id not in (
                    select student_id
                    from dev_account_center.mz_server_assistant_suspend
                    )
                    and graduate_at > date(%s);
                    """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def list_active_monitor(started_at):
    """
    返回当天的活跃用户数据列表
    :param started_at:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if not isinstance(started_at, datetime.date):
            raise InvalidParamException('params is not a valid python date')

        sql = """
                SELECT id, student_name, student_phone, current_vedio_num, current_test_num, current_task_num, current_book_course, current_ask_question, total_score FROM dev_account_center.mz_server_active_point
                where create_at = %s;
                """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(started_at)))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def get_total_active_point_by_phone(phone):
    """

    :param phone: 学生的手机i
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                    SELECT sum(total_score) as score , student_id
                    FROM dev_account_center.mz_server_active_point
                    group by student_phone
                    having student_phone = %s;
                    """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (phone))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }

        return APIResult(result=result_dict)

    return main()


def get_active_point_by_month(student_phone, year, month):
    """
    获取每个月的活跃记录
    :param student_phone:  学生的phone
    :param year: 年份
    :param month: 月份
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        t = datetime.date(year, month, 1)
        print str(t)

        sql = """
                select
                student_id,
                sum(current_vedio_num) as n1,
                sum(current_test_num) as n2,
                sum(current_task_num) as n3,
                sum(current_book_course) as n4,
                sum(current_ask_question) as n5,
                sum(total_score) as n6
                from mz_server_active_point
                        where create_at >= %s
                        and create_at < date_add(%s, interval 1 month)
                        group by student_phone
                        having student_phone = %s;
                        """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (str(t), str(t), student_phone))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            # "rows_count": rows_count["count"],
        }
        print result_dict

        return APIResult(result=result_dict)

    return main()


def insert_student_activity_data(student_id, student_name, student_phone, student_account, started_at):
    """
    插入一条学生的数据记录
    :param student_id 学生的ID
    :param student_name 学生的姓名
    :param student_phone 学生的手机号
    :param student_account 学生的帐号
    :param started_at: 创建的日期
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                    INSERT INTO `dev_account_center`.`mz_server_active_point`
                    (`student_id`,`student_name`,`student_phone`,`current_vedio_num`,`current_test_num`,
                    `current_task_num`,`current_book_course`,`current_ask_question`,`total_score`,
                    `create_at`,`student_account`,`consecutive_days`)
                    VALUES
                    (%s,%s,%s,0,0,0,0,0,0,%s,%s,0);
                    """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (student_id, student_name, student_phone, str(started_at), student_account))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_activity_video_num(student_account, started_at, num):
    """
    NOTE: 更新数据的SQL如果条件不存在也可以正常执行，所以我们就全部更新不用关系数据有无的问题
    :param student_account 用户帐号
    :param started_at 日期
    :param num 观看视频的数量
    :return: 更新数据
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                  UPDATE `dev_account_center`.`mz_server_active_point`
                    SET `current_vedio_num` = %s
                    WHERE `student_account` = %s and `create_at` = %s;
                        """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (num, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_activity_exceicse_num(student_account, started_at, num):
    """
    NOTE: 更新数据的SQL如果条件不存在也可以正常执行，所以我们就全部更新不用关系数据有无的问题
    :param student_account 用户帐号
    :param started_at 日期
    :param num 完成联系的数量
    :return: 更新数据
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                  UPDATE `dev_account_center`.`mz_server_active_point`
                    SET `current_test_num` = %s
                    WHERE `student_account` = %s and `create_at` = %s;
                        """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (num, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_activity_finish_task_balls(student_account, started_at, num):
    """
    更新完成的任务球个数
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                      UPDATE `dev_account_center`.`mz_server_active_point`
                        SET `current_task_num` = %s
                        WHERE `student_account` = %s and `create_at` = %s;
                            """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (num, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_activity_book_course(student_account, started_at, num):
    """
    更新每天的约课的次数
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                      UPDATE `dev_account_center`.`mz_server_active_point`
                        SET `current_book_course` = %s
                        WHERE `student_account` = %s and `create_at` = %s;
                            """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (num, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_activity_ask_question(student_account, started_at, num):
    """
    更新每天的辅导次数
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                      UPDATE `dev_account_center`.`mz_server_active_point`
                        SET `current_ask_question` = %s
                        WHERE `student_account` = %s and `create_at` = %s;
                            """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (num, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_student_active_monitor_total_score_data(id, total_score):
    """
    更新每一个人的总分
    :param id: 那条记录的ID,唯一，所以就不加入ID了
    :param total_score: 那个人的总分
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                  UPDATE `dev_account_center`.`mz_server_active_point`
                    SET `total_score` = %s
                    WHERE `id` = %s;
            """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (total_score, id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update_consecutive_none_learn_days(consecutive_time, student_account, started_at):
    """
    更新连续未学习天数
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                      UPDATE `dev_account_center`.`mz_server_active_point`
                        SET `consecutive_days` = %s
                        WHERE `student_account` = %s and `create_at` = %s;
                            """

        sql = sql.replace('dev_account_center', settings.MAIZISERVERDB).replace('dev_lps_20170707', settings.MAIZILPSDB)

        try:
            cursor.execute(sql, (consecutive_time, student_account, str(started_at)))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def batch_insert_student_activity_data(student_list, started_at):
    """
    :param student_list 带插入的学生列表
    :param started_at 数据加入的时间
    :return: 批量插入数据
    """
    for data in student_list:
        insert_student_activity_data(data.get('id'), data.get('student_name'), data.get('phone'), data.get('account'),
                                     started_at)
    log.info("insert " + str(len(student_list)) + "student data into the active point table")
    return True


def _init_daily_data(started_at):
    """
    :return: 初始化每天的活跃学分记录，不包含结业，毕业和休学的学员
    """

    all_active_student = list_active_student(started_at)
    if all_active_student.is_error():
        raise MysqlQueryException("error accoour during sql query")
    batch_insert_student_activity_data(all_active_student.result()['result'], started_at)


def _insert_watched_videos(started_at):
    """
    :param started_at 日期
    :return: 便利数据插入每天的观看视频数量
    """
    all_watched_data = list_watched_videos(started_at)

    if all_watched_data.is_error():
        raise MysqlQueryException('Error during query')

    result_data = all_watched_data.result()['result']
    for watched_data in result_data:
        update_student_activity_video_num(watched_data.get('username'), started_at, watched_data.get('watch_num'))


def _insert_finished_test(started_at):
    """
    :return: 插入学院每天完成的练习数
    """
    all_finished_tests = list_finish_exercises(started_at)

    if all_finished_tests.is_error():
        raise MysqlQueryException("Error during query")

    result_data = all_finished_tests.result()['result']
    for data in result_data:
        update_student_activity_exceicse_num(data.get('username'), started_at, data.get('watch_num'))


def _insert_finish_task_ball(started_at):
    """

    :return: 插入每天完成的任务数量
    """
    all_finish_tasks = list_finish_task(started_at)

    if all_finish_tasks.is_error():
        raise MysqlQueryException('Error during query')

    result_data = all_finish_tasks.result()['result']
    for data in result_data:
        update_student_activity_finish_task_balls(data.get('username'), started_at, data.get('num'))


def _insert_booking_cources(started_at):
    """
    :return: 插入每天约课的数量
    """
    all_book_cources = list_booking_cources(started_at)

    if all_book_cources.is_error():
        raise MysqlQueryException('Error during query')

    result_data = all_book_cources.result()['result']
    for data in result_data:
        update_student_activity_book_course(data.get('username'), started_at, data.get('num'))


def _insert_ask_question_num(started_at):
    """

    :return: 插入每天辅导的次数
    """
    all_ask_question = list_ask_question(started_at)
    if all_ask_question.is_error():
        raise MysqlQueryException('Error during query')

    result_data = all_ask_question.result()['result']
    for data in result_data:
        update_student_activity_ask_question(data.get('username'), started_at, data.get('num'))


def __cal_total_point(current_vedio_num, current_test_num, current_task_num, current_book_course, current_ask_question):
    """
    返回计算的总分
    :param current_vedio_num: 观看视频数量
    :param current_test_num: 完成联系数量
    :param current_task_num: 完成任务球
    :param current_book_course: 约课
    :param current_ask_question: 辅导
    :return:
    """
    total_score = 0
    total_score += int(current_vedio_num) * 0.5
    total_score += int(current_test_num) * 3
    total_score += int(current_task_num) * 5
    total_score += int(current_book_course) * 8
    total_score += int(current_ask_question) * 3
    return total_score


def _insert_total_point_daily(started_at):
    """

    :return: 插入每个学生记录的总分
    """
    all_active_monitor = list_active_monitor(started_at)
    if all_active_monitor.is_error():
        raise MysqlQueryException('Error during sql query')

    result_data = all_active_monitor.result()['result']
    for data in result_data:
        id = data.get('id')
        total_score = __cal_total_point(
            data.get('current_vedio_num'),
            data.get('current_test_num'),
            data.get('current_task_num'),
            data.get('current_book_course'),
            data.get('current_ask_question')
        )
        update_student_active_monitor_total_score_data(id, total_score)
    return True


def _insert_consecutive_days(started_at):
    """
    :return: 插入连续未学习时间天数
    """
    all_finish_tasks = consecutive_days()

    if all_finish_tasks.is_error():
        raise MysqlQueryException('Error during query')

    result_data = all_finish_tasks.result()['result']

    for data in result_data:
        start_time = started_at
        last_time = data.get('last_login')
        consecutive_time = start_time - last_time

        update_consecutive_none_learn_days(consecutive_time, data.get('username'), started_at)


def getYesterday():
    """
    返回昨天的日期
    :return:
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday


def daily_data_count():
    """
    :return: 初始化并且插入每天的数据
    """
    print 'daily_data_count' * 100
    started_at = getYesterday()

    _init_daily_data(started_at)

    _insert_watched_videos(started_at)
    _insert_finished_test(started_at)
    _insert_finish_task_ball(started_at)
    _insert_booking_cources(started_at)
    _insert_ask_question_num(started_at)
    _insert_total_point_daily(started_at)
    _insert_consecutive_days(started_at)


def update_activity_score(started_at):
    """
    更新活跃学分
    :return:
    """
    all_active_monitor = list_active_monitor(started_at)
    if all_active_monitor.is_error():
        raise MysqlQueryException('Error during sql query')

    pass


# def update_consecutive_none_learn_days():
#     """
#     更新连续未学习的天数
#     :return:
#     """
#     pass


def daily_sms_notify():
    """
    每日短信通知的定时任务
    :return:
    """
    print "开始发送短信"

    started_at = getYesterday()

    all_active_monitor = list_active_monitor(started_at)
    if all_active_monitor.is_error():
        raise MysqlQueryException('Error during sql query')

    result_data = all_active_monitor.result()['result']
    for data in result_data:

        if data.get('total_score') > 0:
            # 有活跃学分的参数
            params = {
                'name': data.get('student_name'),
                'vedio': data.get('current_vedio_num'),
                'test': data.get('current_test_num'),
                'task': data.get('current_task_num'),
                'order': data.get('current_book_course'),
                'coach': data.get('current_ask_question')
            }
        else:
            # 没有活跃学分
            params = {
                'name': data.get('student_name')
            }

        from maiziserver.tools.send_sms_message import send_sms_daily

        print data.get('student_phone')

        if data.get('student_phone') == '18782685754':
            send_sms_daily(data.get('student_phone'), data.get('total_score'), params)


def week_sms_notify():
    """
    每周短信通知
    :return:
    """
    pass


def month_sms_notify():
    """
    每月短信通知的定时任务
    :return:
    """
    pass
