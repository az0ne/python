# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_make_conn_cursor, dec_get_cache


def get_career_course_detail(career_id):
    redis_key = 'career_course_detail_%s' % career_id

    @dec_timeit("get_career_course_detail")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        获取职业课程价格
        :param conn:
        :param cursor:
        :return:
        """
        sql = """
             SELECT cc.name,cc.net_price, cc.jobless_price
             FROM mz_course_careercourse AS cc
             WHERE id=%s
              """
        try:
            cursor.execute(sql, (career_id,))
            result = cursor.fetchone()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)
    return main(_enable_cache=True)


@dec_timeit("get_current_class_coding")
@dec_make_conn_cursor
def get_current_class_coding(conn, cursor, career_id):
    """
    获得职业课程当前正在招生的班级编号
    :param career_id:
    :return:
    """
    sql = """
        SELECT
            cl.coding, u.mobile, u.avatar_url, u.position, u.teach_feature, u.description,u.nick_name
        FROM mz_lps_class AS cl
        INNER JOIN mz_lps_classteachers AS ct ON cl.id=ct.teacher_class_id
        INNER JOIN mz_user_userprofile AS u ON u.id=ct.teacher_id
        WHERE cl.status=1 AND cl.is_active=1 AND cl.is_closed=0 AND cl.career_course_id=%s AND
            cl.class_type=0 AND cl.current_student_count < cl.student_limit
        GROUP BY cl.id
        LIMIT 1
        """
    try:
        cursor.execute(sql, (career_id,))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
