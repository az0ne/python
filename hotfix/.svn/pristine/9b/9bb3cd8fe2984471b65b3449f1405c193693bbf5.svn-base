# -*- coding:utf-8 -*-
from django.http.response import Http404

from utils.logger import logger
from db.api.apiutils import APIResult, dec_make_conn_cursor


def get_user_graduate(user_id):
    """
    获取学生毕业时间
    :param user_id:
    :return:end_time
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select end_time
                from mz_lps4_student
                where user_id=%s
                """

        try:
            cursor.execute(sql, (user_id,))
            end_time = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=end_time)

    return main()


def get_user_class_info(user_id):
    """
    学生开始工作时间
    :param user_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            start_work_time,
            is_view_resume_intro
        from mz_lps_classstudents
        where user_id=%s
        ORDER BY id
        """

        try:
            cursor.execute(sql, (user_id,))
            info = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=info)

    return main()


def get_user_info(user_id):
    """
    学生基本信息
    :param user_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            info.id as user_id,
            info.real_name,
            info.gender,
            CASE info.gender
              WHEN '1' THEN '男'
              WHEN '2' THEN '女'
            END as gender_name,
            info.birthday
        from mz_user_userprofile as info
        where id=%s
        """

        try:
            cursor.execute(sql, (user_id,))
            info = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=info)

    return main()


def list_user_work(user_id):
    """
    学生工作经历
    :param user_id:
    :return:
    """

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
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=works)

    return main()


def list_user_edu(user_id):
    """
    学生教育背景
    :param user_id:
    :return:
    """

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
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=edus)

    return main()


def update_user_info(user_id, real_name, gender, birthday):
    """
    修改学生基本信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          update mz_user_userprofile set real_name = %s, gender = %s, birthday = %s where id = %s
        """

        try:
            cursor.execute(sql, (real_name, gender, birthday, user_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def update_user_start_work_time(user_id, start_work_time):
    """
    修改学生基本信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          update mz_lps_classstudents set start_work_time = %s where user_id = %s
        """

        try:
            cursor.execute(sql, (start_work_time, user_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def add_user_work(user_id, company, start_time, end_time, title, content):
    """
    新增学生工作信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          insert into mz_resume_work(user_id, company, start_time, end_time, title, content) values (%s,%s,%s,%s,%s,%s)
        """
        last_insert_id = """
                    SELECT last_insert_id() AS last_insert_id
                """

        try:
            cursor.execute(sql, (user_id, company, start_time, end_time, title, content))
            logger.info("query:%s" % cursor._last_executed)
            cursor.execute(last_insert_id)
            last_insert_id = cursor.fetchone()['last_insert_id']
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=last_insert_id)

    return main()


def add_user_edu(user_id, school, start_time, end_time, title, major):
    """
    新增学生教育信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          insert into mz_resume_edu(user_id, school, start_time, end_time, title, major) values (%s,%s,%s,%s,%s,%s)
        """
        last_insert_id = """
                            SELECT last_insert_id() AS last_insert_id
                        """

        try:
            cursor.execute(sql, (user_id, school, start_time, end_time, title, major))
            logger.info("query:%s" % cursor._last_executed)
            cursor.execute(last_insert_id)
            last_insert_id = cursor.fetchone()['last_insert_id']
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=last_insert_id)

    return main()


def update_user_work(user_id, company, start_time, end_time, title, content, resume_work_id):
    """
    修改学生工作信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          update mz_resume_work set user_id = %s, company = %s, start_time = %s, end_time = %s, title = %s , content = %s where id = %s
        """

        try:
            cursor.execute(sql, (user_id, company, start_time, end_time, title, content, resume_work_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=resume_work_id)

    return main()


def update_user_edu(user_id, school, start_time, end_time, title, major, resume_edu_id):
    """
    修改学生教育信息
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          update mz_resume_edu set user_id = %s, school = %s, start_time = %s, end_time = %s, title = %s , major = %s where id = %s
        """

        try:
            cursor.execute(sql, (user_id, school, start_time, end_time, title, major, resume_edu_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=resume_edu_id)

    return main()


def delete_user_work(resume_work_id, user_id):
    """
    删除学生工作信息
    """
    try:
        resume_work_id = int(resume_work_id)
        user_id = int(user_id)
    except ValueError:
        logger.warn('parameter is not int %s, %s' % (resume_work_id, user_id))
        raise Http404
    if resume_work_id < 0 or user_id < 0:
        logger.warn('parameter is small than 0 %s, %s' % (resume_work_id, user_id))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          delete FROM mz_resume_work where id = %s and user_id = %s
        """

        try:
            cursor.execute(sql, (resume_work_id, user_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def delete_user_edu(resume_work_id, user_id):
    """
    删除学生教育信息
    """
    try:
        resume_work_id = int(resume_work_id)
        user_id = int(user_id)
    except ValueError:
        logger.warn('parameter is not int %s, %s' % (resume_work_id, user_id))
        raise Http404
    if resume_work_id < 0 or user_id < 0:
        logger.warn('parameter is small than 0 %s, %s' % (resume_work_id, user_id))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
          delete FROM mz_resume_edu where id = %s and user_id = %s
        """

        try:
            cursor.execute(sql, (resume_work_id, user_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def update_is_view_resume_intro(user_id):
    """
    更新学生是否看过resume_intro
    :param user_id:
    :return:
    """

    try:
        user_id = int(user_id)
    except ValueError:
        raise Http404
    if user_id < 0:
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        UPDATE mz_lps_classstudents
        SET is_view_resume_intro = 1
        WHERE user_id = %s;
        """

        try:
            cursor.execute(sql, (user_id,))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()
