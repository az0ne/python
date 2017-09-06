#! /usr/bin/evn python
# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor
from django.conf import settings


def get_user_info(user_id):
    """
    学生基本信息
    :param user_id:
    :return:
    """

    @dec_timeit
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            info.id as user_id,
            info.real_name,
            info.mobile,
            info.city_id,
            info.gender,
            CASE info.gender
              WHEN '1' THEN '男'
              WHEN '2' THEN '女'
            END as gender_name,
            info.birthday,
            student.start_work_time,
            jobinfo.to_industry,
            jobinfo.intention_job_city as city
        from mz_user_userprofile as info
        LEFT JOIN  mz_lps_classstudents as student
        ON info.id=student.user_id
        LEFT JOIN mz_user_userjobinfo as jobinfo
        ON info.id = jobinfo.user_id
        where info.id=%s
        GROUP BY user_id
        """

        try:
            cursor.execute(sql, (user_id,))
            info = cursor.fetchone()
            logger.info("query:%s" % cursor.statement)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
            raise e
        return APIResult(result=info)

    return main()


def list_user_work(user_id):
    """
    学生工作经历
    :param user_id:
    :return:
    """

    @dec_timeit
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            worker.id,
            worker.user_id,
            worker.company,
            worker.start_time,
            worker.end_time,
            worker.title,
            worker.content
        from mz_resume_work as worker
        where worker.user_id=%s
        order by worker.id
        """


        try:
            cursor.execute(sql, (user_id,))
            works = cursor.fetchall()
            logger.info("query:%s" % cursor.statement)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
            raise e
        return APIResult(result=works)

    return main()


def list_user_edu(user_id):
    """
    学生教育背景
    :param user_id:
    :return:
    """

    @dec_timeit
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            edu.id,
            edu.user_id,
            edu.school,
            edu.start_time,
            edu.end_time,
            edu.title,
            edu.major
        from mz_resume_edu as edu
        where edu.user_id=%s
        order by edu.id
        """

        try:
            cursor.execute(sql, (user_id,))
            edus = cursor.fetchall()
            logger.info("query:%s" % cursor.statement)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
            raise e
        return APIResult(result=edus)

    return main()


@dec_timeit
@dec_make_conn_cursor
def list_resume_info(conn, cursor, page_index):
    page_size = settings.PAGE_SIZE
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT edu.user_id,career.name as career_name,student.end_time, jobinfo.intention_job_city as city,
                      user_info.real_name
               FROM mz_resume_edu as edu
               LEFT JOIN mz_user_userprofile as user_info
               ON edu.user_id=user_info.id
               LEFT JOIN mz_lps_classstudents as lps_student
               ON edu.user_id=lps_student.user_id
               LEFT JOIN mz_lps_class as class
               ON lps_student.student_class_id=class.id
               LEFT JOIN mz_user_userjobinfo as jobinfo
               ON edu.user_id=jobinfo.user_id
               LEFT JOIN mz_course_careercourse as career
               ON class.career_course_id=career.id
               left JOIN mz_lps4_student as student
               ON edu.user_id=student.user_id
               GROUP BY edu.user_id
               ORDER BY edu.id DESC
               limit %s, %s;
            """, (start_index, page_size))
        resumes = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*)as count
                FROM (SELECT id, user_id FROM mz_resume_edu GROUP BY user_id)resume_edu_temp
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": resumes,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)


@dec_timeit
@dec_make_conn_cursor
def list_resume_info_by_search(conn, cursor, keyword, page_index):
    page_size = settings.PAGE_SIZE
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT edu.user_id,career.name as career_name,student.end_time, jobinfo.intention_job_city as city,
                      user_info.real_name
               FROM mz_resume_edu as edu
               LEFT JOIN mz_user_userprofile as user_info
               ON edu.user_id=user_info.id
               LEFT JOIN mz_lps4_student as student
               ON edu.user_id=student.user_id
               LEFT JOIN mz_user_userjobinfo as jobinfo
               ON edu.user_id=jobinfo.user_id
               LEFT JOIN mz_lps4_career as career
               ON student.career_id=career.id
               WHERE user_info.real_name LIKE %s
               GROUP BY edu.user_id
               limit %s, %s;
            """, (keyword, start_index, page_size))
        resumes = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*)as count
                FROM (SELECT id, user_id FROM mz_resume_edu GROUP BY user_id)resume_edu_temp
                LEFT JOIN mz_user_userprofile as user_info
                ON resume_edu_temp.user_id=user_info.id
                WHERE user_info.real_name like %s
            """, (keyword,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": resumes,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)
