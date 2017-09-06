# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_career_courses")
@dec_get_cache("get_career_courses")
@dec_make_conn_cursor
def get_career_courses(conn, cursor):
    qsql = """
        SELECT *
        FROM mz_course_careercourse;    
    """

    try:
        cursor.execute(qsql)
        career_courses = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn("execute exception: %s. statement: %s" % (e, cursor._last_executed))
        raise e

    career_course_dict = {
        "result": career_courses,
    }

    # set cache
    cache.set("get_career_courses", career_course_dict)

    return APIResult(result=career_course_dict)


@dec_timeit("get_hot_career_course")
@dec_get_cache("get_hot_career_course")
@dec_make_conn_cursor
def get_hot_career_course(conn, cursor):
    """
    :param conn:
    :param cursor:
    :return:
    """
    limit = 10
    sql = '''
        SELECT image, name, short_name, course_color
        FROM mz_course_careercourse WHERE is_hot=1
        LIMIT %s;
        '''
    try:
        cursor.execute(sql, (limit,))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn('execute exception: %s. statement: %s' % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_career_courses", data)

    return APIResult(result=data)


@dec_timeit("get_career_course_name_by_id")
@dec_get_cache("get_career_course_name_by_id")
@dec_make_conn_cursor
def get_career_course_name_by_id(conn, cursor, career_course_id):
    try:
        cursor.execute(
            """
              select id,name from mz_course_careercourse where id=%s
            """, (career_course_id,)
        )
        careerCourse = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerCourse)


def get_career_course_name_short_name_and_image(limit=10):
    """
    获取职业课程，根据id排序
    :param limit: 默认显示10条
    :return: 返回职业课程的名称，简称，图片，课程背景颜色
    """
    redis_key = 'get_career_course_name_short_name_and_image'

    @dec_timeit("get_career_course_name_short_name_and_image")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def _func(conn, cursor):
        sql = """
            select cp.name,cc.short_name,cc.image,cc.course_color
            from mz_career_page as cp
            INNER JOIN mz_course_careercourse as cc ON cc.id=cp.id
            order by cp.id
            limit %s
        """

        try:
            cursor.execute(sql, (limit,))
            career_course = cursor.fetchall()
            log.debug('query:%s' % cursor._last_executed)
        except Exception as e:
            log.warn(
                'execute exception: %s.'
                'statement:%s' % (e, cursor._last_executed)
            )
            raise e
        cache.set(redis_key, career_course, 60 * 2)

        return APIResult(result=career_course)

    return _func(_enable_cache=True)
	
	
@dec_timeit("get_career_course_by_course_id_through_careerobjrelation")
@dec_make_conn_cursor
def get_career_course_by_course_id_through_careerobjrelation(conn, cursor, course_id):
    try:
        cursor.execute(
            """
            SELECT
                cc.id,
                cc.`name`,
                cc.ad,
                cc.short_name,
                cc.student_count,
                cc.image
            FROM
                mz_common_careerobjrelation AS cor
            JOIN mz_course_careercourse AS cc ON cor.career_id = cc.id
            WHERE
                cor.obj_id = %s
            AND cor.obj_type = 'COURSE'
            """, (course_id,)
        )
        career_id = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=career_id)


@dec_timeit('is_enterprise_student')
@dec_make_conn_cursor
def is_career_student_of_these_career_courses(conn, cursor, user_id, now, career_courses_id):
    """
    判断（是否）是该企业直通班学生(不限3.0)
    :param user_id:
    :param now:
    :return: ''
    """
    sql = """
        SELECT
            cs.id
        FROM
            mz_lps_classstudents AS cs
        JOIN mz_lps_class AS c ON c.id = cs.student_class_id
        WHERE
            cs.user_id = %s
        AND (
            cs.deadline IS NULL
            OR cs.deadline < %s
        )
        AND cs.`status` = 1
        AND c.is_active = 1
        AND c.class_type = 0
        AND c.career_course_id IN (%s);
    """ % ('%s', '%s', ','.join(map(lambda x: '%s', career_courses_id)))
    try:
        cursor.execute(sql, [user_id, now] + career_courses_id)
        group_name = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=group_name)


@dec_timeit('get_page_teacher_by_teacher_id')
@dec_make_conn_cursor
def get_page_teacher_by_teacher_id(conn, cursor, teacher_id):
    """
    :param conn:
    :param cursor:
    :param teacher_id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT name,title,info,big_img_url
            FROM mz_career_page_teacher
            WHERE teacher_id=%s;
            """,(teacher_id,))
         teacher = cursor.fetchone()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
         raise e
    return APIResult(result=teacher)


@dec_make_conn_cursor
def get_app_career_ad(conn, cursor, career_id):
    """
    获取app职业课广告
    :param conn:
    :param cursor:
    :param career_id:
    :return:
    """
    try:
        career_id = int(career_id)
    except Exception as e:
        log.warn(str(e))
        return APIResult(code=False)

    try:
        cursor.execute(
            """
SELECT *
FROM mz_app_career_ad
WHERE career_id = %s;
            """, (career_id,)
        )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=result)
	

@dec_make_conn_cursor
def get_institute_by_career_id(conn, cursor, career_id):
    """
    获取Institute
    :param conn:
    :param cursor:
    :param career_id:
    :return:
    """
    try:
        career_id = int(career_id)
    except Exception as e:
        log.warn(str(e))
        return APIResult(code=False)
    try:
        cursor.execute(
            """
SELECT i.*
FROM mz_course_institute AS i
  JOIN mz_course_careercourse AS cc ON cc.institute_id = i.id
WHERE cc.id = %s;
            """ % (career_id,)
        )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=result)	
