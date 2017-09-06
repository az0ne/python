# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_make_conn_cursor, dec_get_cache


@dec_timeit("ios_version")
@dec_get_cache("ios_version")
@dec_make_conn_cursor
def ios_version(conn, cursor, app_type=1):
    """
    IOS 版本查询
    :param conn:
    :param cursor:
    :param app_type:
    :return:
    """
    sql = """
SELECT *
FROM mz_common_iosversion
WHERE type = %s
ORDER BY id DESC
LIMIT 2
        """
    try:
        cursor.execute(sql, (app_type,))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    cache.set('ios_version_type%s' % app_type, result, 60 * 5)
    return APIResult(result=result)


@dec_timeit("app_direction_career_course")
@dec_get_cache("app_direction_career_course")
@dec_make_conn_cursor
def app_direction_career_course(conn, cursor):
    """
    APP方向对应职业课程
    :param conn:
    :param cursor:
    :return:
    """
    sql = """
        SELECT cd.id AS direction_id, cd.name AS direction_name, cd.image AS direction_image,
        cc.id AS career_id, cc.name AS career_name, cc.app_career_image AS app_career_image,
        cc.is_class AS is_class, cc.short_name AS short_name, cc.image AS career_image,cc.student_count AS student_count
        FROM mz_course_coursedirection AS cd
        LEFT JOIN mz_course_coursedirection_career_course AS cdcc ON cd.id = cdcc.coursedirection_id
        LEFT JOIN mz_course_careercourse AS  cc ON cdcc.careercourse_id = cc.id
        """
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    cache.set('app_direction_career_course', result, 60 * 5)
    return APIResult(result=result)


@dec_timeit("app_direction_career_course_ios_check")
@dec_make_conn_cursor
def app_direction_career_course_ios_check(conn, cursor):
    """
    APP方向对应职业课程,IOS 审核时候使用
    :param conn:
    :param cursor:
    :return:
    """
    sql = """
        SELECT cd.id AS direction_id, cd.name AS direction_name, cd.image AS direction_image,
        cc.id AS career_id, cc.name AS career_name, cc.app_career_image AS app_career_image,
        cc.is_class AS is_class, cc.short_name AS short_name, cc.image AS career_image,cc.student_count AS student_count
        FROM mz_course_coursedirection AS cd
        LEFT JOIN mz_course_coursedirection_career_course AS cdcc ON cd.id = cdcc.coursedirection_id
        INNER JOIN mz_course_careercourse AS  cc ON cdcc.careercourse_id = cc.id AND cc.short_name NOT LIKE '%Android%'
        """
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("app_last_career_course")
@dec_make_conn_cursor
def app_last_career_course(conn, cursor, user_id):
    """
    获取最新报班课程id
    :param conn:
    :param cursor:
    :return:
    """
    sql1 = """
        SELECT c.career_course_id FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON cs.student_class_id = c.id
        WHERE c.class_type=0 AND c.status=1 AND cs.user_id=%s
        ORDER BY cs.id DESC
        LIMIT 1
        """
    sql2 = """
        SELECT c.career_course_id FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON cs.student_class_id = c.id
        WHERE c.class_type=2 AND c.status=1 AND cs.user_id=%s
        ORDER BY cs.id DESC
        LIMIT 1
        """
    try:
        cursor.execute(sql1, (user_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute(sql2, (user_id,))
            result = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


def app_course_by_click_or_new(order, page_index, page_size):
    """
    根据点击数或者发布时间获取课程
    :param order:
    :param page_index:
    :param page_size:
    :return:
    """
    redis_key = 'app_course_by_%s_%s' % (order, page_index)
    start_index, end_index = get_page_info(page_index, page_size)

    @dec_timeit("app_course_by_click_or_new")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                    SELECT id,name,image,click_count FROM mz_course_course WHERE is_active=1 AND is_click=1
                    ORDER BY %s DESC LIMIT %s,%s
        """

        try:
            sql = sql % (order, start_index, end_index)
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            log.warn(
                    'execute exception: %s. '
                    'statement: %s' % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)
    return main(_enable_cache=True)


@dec_timeit("app_course_by_click_or_new_for_ios_check")
@dec_make_conn_cursor
def app_course_by_click_or_new_for_ios_check(conn, cursor, order, page_index, page_size):

    start_index, end_index = get_page_info(page_index, page_size)
    sql = """
        SELECT mz_course_course.id,mz_course_course.name,mz_course_course.image,mz_course_course.click_count FROM mz_course_course
        WHERE NOT (mz_course_course.id IN (SELECT U1.course_id AS course_id
        FROM mz_course_course_search_keywords U1
        INNER JOIN mz_common_keywords U2 ON ( U1.keywords_id = U2.id ) WHERE U2.name LIKE '%Android%'))
        AND is_active=1 AND is_click=1
        ORDER BY mz_course_course.{0} DESC
        LIMIT {1},{2}
        """

    try:
        sql = sql.format(order, start_index, end_index)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


def app_course_by_career_id(career_id, page_index, page_size):
    redis_key = 'app_course_by_career_id_%s_%s' % (career_id, page_index)
    start_index, end_index = get_page_info(page_index, page_size)

    @dec_timeit("app_course_by_career_id")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT mz_course_course.id,mz_course_course.name,mz_course_course.image,mz_course_course.click_count FROM mz_course_course
            INNER JOIN mz_course_course_stages_m ON mz_course_course.id = mz_course_course_stages_m.course_id
            INNER JOIN mz_course_stage ON mz_course_course_stages_m.stage_id = mz_course_stage.id AND mz_course_stage.career_course_id=%s
            WHERE mz_course_course.is_active=1 AND mz_course_course.is_click=1
            ORDER BY mz_course_course.click_count DESC
            LIMIT %s,%s
        """

        try:
            sql = sql % (career_id, start_index, end_index)
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            log.warn(
                    'execute exception: %s. '
                    'statement: %s' % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 60)
        return APIResult(result=result)
    return main(_enable_cache=True)


@dec_timeit("app_user_class_type")
@dec_make_conn_cursor
def app_user_class_type(conn, cursor, user_id, career_id):
    """
    判断用户是否报名该职业课程下某班级类型的班级
    :param class_type: 班级类型  0: 正常付费班级 2：app免费试学班
    :param career_id: 职业课程ID
    :return:
    """
    sql = """
        SELECT cs.id, cs.deadline, cs.student_class_id , c.lps_version FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON c.id=cs.student_class_id
        WHERE
        c.class_type=0 AND cs.status=1 AND cs.user_id=%s AND c.career_course_id=%s
        LIMIT 1
        """
    sql1 = """
        SELECT cs.student_class_id FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON c.id=cs.student_class_id
        WHERE
        c.class_type=2 AND cs.status=1 AND cs.user_id=%s AND c.career_course_id=%s
        LIMIT 1
        """
    try:
        is_pay = False
        is_full_paid = True
        is_app_free = False
        class_id = None
        lps_version = None
        sql = sql % (user_id, career_id)
        cursor.execute(sql)
        sql_result = cursor.fetchone()
        if sql_result:
            is_pay = True
            class_id = sql_result['student_class_id']
            lps_version = sql_result['lps_version']
            if sql_result['deadline']:
                is_full_paid = False
        else:
            sql1 = sql1 % (user_id, career_id)
            cursor.execute(sql1)
            sql1_result = cursor.fetchone()
            if sql1_result:
                is_app_free = True
                class_id = sql1_result['student_class_id']
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    result = {'is_normal_class': is_pay,
              'is_full_paid': is_full_paid,
              'is_app_free': is_app_free,
              'class_id': class_id,
              'lps_version': lps_version
              }
    return APIResult(result=result)


@dec_timeit("app_update_user_token")
@dec_make_conn_cursor
def app_update_user_token(conn, cursor, user_id, token, app):
    """
    更新APP设备token
    :param conn:
    :param cursor:
    :param user_id:
    :param token:
    :param app: 'Android: 1, IOS: 2',
    :return:
    """
    sql_select = '''
        SELECT 1 FROM mz_user_token WHERE user_id=%s FOR UPDATE
        '''

    sql_insert = '''
        INSERT INTO mz_user_token (user_id, token, `type`) VALUE (%s,%s,%s)
        '''

    sql_update = '''
        UPDATE mz_user_token SET token=%s, `type`=%s WHERE user_id=%s
        '''
    try:
        cursor.execute(sql_select, (user_id,))
        is_exists = cursor.fetchone()
        if is_exists:
            cursor.execute(sql_update, (token, app, user_id))
        else:
            cursor.execute(sql_insert, (user_id, token, app))
        conn.commit()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("app_get_user_token")
@dec_make_conn_cursor
def app_get_user_token(conn, cursor, user_id):
    """
    获取APP设备token
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    sql_select = '''
        SELECT * FROM mz_user_token WHERE user_id=%s
        '''
    try:
        cursor.execute(sql_select, (user_id,))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("app_consult_info_stream_insert")
@dec_make_conn_cursor
def app_consult_info_stream_insert(conn, cursor, dict_info):
    """
    添加手机活动页面信息统计，信息流
    :param dict_info:
    :param conn:
    :param cursor:
    :return:
    """
    sql_insert = '''
        INSERT INTO mz_common_appconsultinfo_stream (`name`, phone, qq, interest, date_publish, source, market_from)
        VALUE (%s,%s,%s,%s,%s,%s,%s)
        '''
    try:
        cursor.execute(sql_insert,
                       (dict_info.get('name'), dict_info.get('phone'), dict_info.get('qq'), dict_info.get('interest'),
                        dict_info.get('date_publish'), dict_info.get('source'), dict_info.get('market_from'),))
        conn.commit()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)
