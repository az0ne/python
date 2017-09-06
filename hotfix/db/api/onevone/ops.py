# -*- coding: utf-8 -*-
"""
@time: 2016/10/14 0006 14:57
@note:  运营1v1收集信息
"""
import datetime
from db.api.apiutils import dec_make_conn_cursor, APIResult
from utils.logger import logger


def create_onevone_ops(user_id, career_id, source, mobile, time_interval, is_work):
    """
    添加运营部收集1v1数据
    :param user_id:
    :param career_id:
    :param source:
    :param mobile:
    :param time_interval:时段，1:午休; 2:下午; 3:下班
    :param is_work: 0:在读, 1:在职
    :return:
    """

    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_insert = """
        INSERT INTO mz_onevone_ops(
            user_id,
            career_id,
            source,
            datetime,
            mobile,
            time_interval,
            is_work
        )VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        try:
            cursor.execute(sql_insert, (user_id, career_id, source, create_time, mobile, time_interval, is_work))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def is_exist_onevone_ops(user_id, career_id, source):
    """
    是否已经预约过运营1v1
    :param user_id:
    :param career_id:
    :param source:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            1
        from mz_onevone_ops
        where user_id=%s and career_id=%s and source=%s
        limit 1
        """
        try:
            cursor.execute(sql, (user_id, career_id, source))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()
