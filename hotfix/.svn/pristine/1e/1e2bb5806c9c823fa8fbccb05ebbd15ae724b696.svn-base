# -*- coding: utf-8 -*-
from mz_common.functions import safe_int

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
import db.api
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_courses")
@dec_get_cache("get_courses")
@dec_make_conn_cursor
def get_courses(conn, cursor):
    """
    """

    qsql = """
        SELECT *
        FROM mz_course_course as c
        WHERE c.is_active=True
          AND c.is_click=True
    """

    try:
        cursor.execute(qsql)
        courses = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    course_dict = {
        "result": courses,
    }

    # set cache
    cache.set("get_courses", course_dict)

    return APIResult(result=course_dict)



#旧有get_hot_course(精品课程)展示接口
# @dec_timeit("get_hot_courses")
# @dec_get_cache("get_hot_courses")
# @dec_make_conn_cursor
# def get_hot_courses(conn, cursor):
#     """
#     """
#
#     CATAGORY_LIMIT = 8
#     COURSE_LIMIT = 8
#     NICK_NAME = u"暂无".encode("utf8")
#
#     career_catagories = db.api.get_career_catagories()
#     if career_catagories.is_error():
#         return career_catagories
#
#     courses = []
#
#     for cc in career_catagories.result()[:CATAGORY_LIMIT]:
#         qsql = """
#             SELECT DISTINCT cc.*
#             FROM mz_course_course AS cc
#             INNER JOIN mz_common_objtagrelation AS cot ON
#                 cot.obj_id=cc.id
#             INNER JOIN mz_user_userprofile AS uu ON
#                 cc.teacher_id = uu.id AND uu.nick_name != %s
#             WHERE cot.careercatagory_id=%s
#                 AND cot.obj_type="COURSE"
#             ORDER BY cc.is_homeshow DESC, cc.click_count DESC LIMIT %s
#             """
#         try:
#             cursor.execute(qsql, (NICK_NAME, cc["id"], COURSE_LIMIT))
#             data = cursor.fetchall()
#             log.debug("query: %s" % cursor._last_executed)
#         except Exception as e:
#             log.warn(
#                 "execute exception: %s. "
#                 "statement: %s" % (e, cursor._last_executed))
#             raise e
#         else:
#             courses.append((cc, data))
#
#     # set cache
#     cache.set("get_hot_courses", courses)
#
#     return APIResult(result=courses)


#新new_get_hot_course(精品课程)展示接口
@dec_timeit("new_get_hot_courses")
@dec_get_cache("new_get_hot_courses")
@dec_make_conn_cursor
def new_get_hot_courses(conn, cursor):
    """
    """

    CATAGORY_LIMIT = 8
    COURSE_LIMIT = 8
    NICK_NAME = u"暂无".encode("utf8")

    career_catagories = db.api.get_career_catagories()
    if career_catagories.is_error():
        return career_catagories

    courses = []

    for cc in career_catagories.result()[:CATAGORY_LIMIT]:
        qsql = """
            SELECT DISTINCT
                cc.*
            FROM mz_homepage_course AS hc
            INNER JOIN mz_course_course AS cc ON hc.course_id=cc.id
            INNER JOIN mz_user_userprofile AS uu ON cc.teacher_id = uu.id AND uu.nick_name != %s
            INNER JOIN mz_common_objtagrelation AS cot ON cot.obj_id=cc.id
            WHERE hc.careercatagory_id=%s AND cot.obj_type='COURSE'
            ORDER BY hc.index DESC
            LIMIT %s
            """
        try:
            cursor.execute(qsql, (NICK_NAME, cc["id"], COURSE_LIMIT))
            data = cursor.fetchall()
            log.debug("query: %s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        else:
            courses.append((cc, data))

    # set cache
    cache.set("new_get_hot_courses", courses)

    return APIResult(result=courses)






def get_course():
    @dec_timeit('get_course')
    @dec_get_cache('get_course')
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    c.id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count,
                    c.need_pay,
                    c.course_status,
                    c.description,
                    up.nick_name
                FROM
                    mz_course_course AS c
                    LEFT JOIN mz_user_userprofile AS up ON up.id = c.teacher_id
                WHERE
                    c.is_active = '1'
                AND c.is_click = '1';
            """
            cursor.execute(sql)
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set('get_course', course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)



def get_id_course(course_id):
    course_id = safe_int(course_id, 0)
    redis_key = 'get_id_course%s' % course_id

    @dec_timeit('get_id_course')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    c.id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count,
                    c.need_pay,
                    c.course_status,
                    c.description
                FROM
                    mz_course_course AS c
                WHERE
                    c.id = %s;
            """
            cursor.execute(sql, (course_id,))
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)


def get_catagory_course(catagory_name):
    if not isinstance(catagory_name, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    redis_key = 'get_catagory_course_%s' % catagory_name

    @dec_timeit('get_catagory_course')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    c.id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count,
                    c.need_pay,
                    c.course_status,
                    c.description,
                    up.nick_name
                FROM
                    mz_common_objtagrelation AS otr
                JOIN mz_course_course AS c ON c.id = otr.obj_id
                JOIN mz_course_newcareer AS ncc ON ncc.id = otr.career_id
                LEFT JOIN mz_user_userprofile AS up ON up.id = c.teacher_id
                WHERE
                    otr.obj_type = 'COURSE'
                AND c.is_active = '1'
                AND c.is_click = '1'
                AND ncc.short_name = %s;
            """
            cursor.execute(sql, catagory_name)
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)


def get_tag_course(tag_name):
    if not isinstance(tag_name, basestring):
        log.warn("tag is not a string")
        return APIResult(code=True)
    redis_key = 'get_tag_course_%s' % tag_name

    @dec_timeit('get_tag_course')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    c.id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count,
                    c.need_pay,
                    c.course_status,
                    c.description,
                    up.nick_name
                FROM
                    mz_common_objtagrelation AS otr
                JOIN mz_course_course AS c ON c.id = otr.obj_id
                JOIN mz_course_tag AS t ON t.id = otr.tag_id
                LEFT JOIN mz_user_userprofile AS up ON up.id = c.teacher_id
                WHERE
                    otr.obj_type = 'COURSE'
                AND c.is_active = '1'
                AND c.is_click = '1'
                AND t.short_name = %s;
            """
            cursor.execute(sql, tag_name)
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)


def get_tag_catagory_course(tag_name, catagory_name):
    if not isinstance(tag_name, basestring):
        log.warn("tag is not a string")
        return APIResult(code=True)
    if not isinstance(catagory_name, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    redis_key = 'get_tag_catagory_course_%s_%s' % (tag_name, catagory_name)

    @dec_timeit('get_tag_catagory_course')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    c.id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count,
                    c.need_pay,
                    c.course_status,
                    c.description,
                    up.nick_name
                FROM
                    mz_common_objtagrelation AS otr
                JOIN mz_course_course AS c ON c.id = otr.obj_id
                JOIN mz_course_tag AS t ON t.id = otr.tag_id
                JOIN mz_course_newcareer AS ncc ON ncc.id = otr.career_id
                LEFT JOIN mz_user_userprofile AS up ON up.id = c.teacher_id
                WHERE
                    otr.obj_type = 'COURSE'
                AND c.is_active = '1'
                AND c.is_click = '1'
                AND t.short_name = %s
                AND ncc.short_name = %s;
            """
            cursor.execute(sql, (tag_name, catagory_name))
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)

@dec_timeit('update_course_click_count')
@dec_make_conn_cursor
def update_course_click_count(conn, cursor, course_id):
    """
    @brief 更新课程点击次数
    :param course_id:
    :return:
    """
    sql = '''
        UPDATE mz_course_course SET click_count = click_count + 1 WHERE id = %s
        '''
    try:
        cursor.execute(sql, (course_id, ))
        conn.commit()
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit('get_course_course')
@dec_make_conn_cursor
def get_course_course(conn, cursor, course_id_list):
    """
    从课程id列表中取出小课程信息
    :param conn:
    :param cursor:
    :return:
    """

    if not course_id_list:
        log.info("course_id_list is None.")
        return APIResult(result=None)

    sql = """select id,name,image from mz_course_course
             WHERE id in %s
        """

    try:
        cursor.execute(sql, (course_id_list,))
        course = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s.'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    return APIResult(result=course)


def get_all_course_course_id_list():
    """
    获取所有的小课程id
    :return: 返回小课程id, type:list [12,23,11,....]
    """
    redis_key = 'course_course_all_id'

    @dec_timeit('get_course_id')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def _func(conn, cursor):
        sql = """
            select id from mz_course_course
        """
        all_course_id = []
        try:
            cursor.execute(sql)
            course_id = cursor.fetchall()
            log.debug('query:%s' % cursor._last_executed)
        except Exception as e:
            log.warn(
                'execute exception: %s.'
                'statement: %s' % (e, cursor._last_executed)
            )
            raise e

        for _cou in course_id:
            all_course_id.append(_cou['id'])

        # cache.set(redis_key, all_course_id, 60 * 60 * 5)

        return APIResult(result=all_course_id)

    return _func()


@dec_timeit('get_course_resource_by_course_id')
@dec_make_conn_cursor
def get_course_resource_by_course_id(conn, cursor, course_id):
    """
    @brief 获取课程的资源
    :param course_id:
    :return:
    """
    sql = """
        SELECT
            id,
            `name`,
            download_url
        FROM
            mz_course_courseresource
        WHERE
            course_id = %s
        """
    try:
        cursor.execute(sql, (course_id, ))
        course_resource = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=course_resource)

@dec_timeit('get_course_by_stage_id')
@dec_make_conn_cursor
def get_course_by_stage_id(conn, cursor, stage_id):
    """
    @brife　通过stage_id获取课程信息，
    :param conn:
    :param cursor:
    :param stage_id:
    :return:
    """
    sql = '''
            SELECT c.id, c.name, c.need_days, c.image, c.course_status, c.need_pay
            FROM mz_course_course AS c
            INNER JOIN mz_course_course_stages_m AS csm
            ON c.id = csm.course_id AND c.is_active = True
            WHERE csm.stage_id = %s
            ORDER BY c.index ASC, c.id ASC
        '''
    try:
        cursor.execute(sql, (stage_id, ))
        result = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)

@dec_timeit('get_course_by_career_course_id')
@dec_make_conn_cursor
def get_course_by_career_course_id(conn, cursor, career_course_id):
    """
    @brief 通过career_course_id获取course
    :param conn:
    :param cursor:
    :param career_course_id:
    :return:
    @note: 通过mz_common_careerobjrelation表过滤，仅获取激活对应关系下的course
    """
    sql = '''
        SELECT c.id, c.name, c.image, c.click_count
        FROM mz_course_course AS c
        INNER JOIN mz_common_careerobjrelation AS cor
        ON c.id = cor.obj_id AND cor.obj_type = 'COURSE' AND cor.is_actived = 1
        INNER JOIN mz_course_careercourse AS cc
        ON cc.id = cor.career_id
        WHERE cc.id = %s
        LIMIT 11
        '''
    try:
        cursor.execute(sql, (career_course_id, ))
        result = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
