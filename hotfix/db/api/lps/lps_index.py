# -*- coding: utf-8 -*-
from utils.logger import logger as log
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor
from db.cores.cache import cache
from mz_lps3.models import Task
from utils.tool import dec_timeit


def get_career_by_class_id(class_id):
    """
    根据班级取职业课
    :param user_id:
    :return:
    """
    try:
        user_id = int(class_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              career_course_id
            FROM mz_lps_class
            WHERE id = %s;
            """, (class_id,))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps_3_1_career_info(career_id):
    """
    获取lps3.1职业课程信息
    :param user_id:
    :return:
    """
    try:
        career_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              *
            FROM mz_lps4_career
            WHERE id = %s;
            """, (career_id,))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_teachers_info_by_career_id(career_id):
    """
    获取lps3.1教师团队信息
    :param career_id:职业课程id
    :return:
    """
    try:
        user_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    redis_key = 'get_teachers_info_by_career_id%s' % career_id

    @dec_timeit("get_teachers_info_by_career_id")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
            teacher.teacher_id,
            teacher.is_hot,
            userprofile.avatar_url,
            userprofile.nick_name,
            userprofile.position,
            userprofile.description,
            career_teacher.id as career_teacher_id
            FROM mz_lps4_teacher_team as teacher
            INNER JOIN  mz_user_userprofile as userprofile
            ON teacher.teacher_id=userprofile.id
            LEFT JOIN mz_lps4_career_teacher as career_teacher
            ON userprofile.id=career_teacher.teacher_id
            WHERE teacher.career_id=%s
            """, (career_id,))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)

    return main()


def get_skill_radar_by_career_id(career_id):
    """
    取雷达图
    :param career_id:
    :return:
    """
    try:
        career_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if career_id <= 0:
        return APIResult(code=False)

    redis_key = 'get_skill_radar_by_career_id%s' % career_id

    @dec_timeit("get_skill_radar_by_career_id")
    # @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              *
            FROM mz_lps4_skill_radar
            WHERE career_id = %s;
            """, (career_id,))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        # cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)

    return main()


def get_skill_tree_by_class_id_career_id_user_id(class_id, career_id, user_id):
    """
    取技能树
    :param career_id:
    :return:
    """
    try:
        class_id = int(class_id)
        career_id = int(career_id)
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if class_id <= 0 or career_id <= 0 or user_id <= 0:
        return APIResult(code=False)

    @dec_timeit("get_skill_tree_by_class_id_career_id_user_id")
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              str.stage_id AS s_id,
              str.id       AS str_id,
              t.id         AS t_id,
              str.type,
              utr.status,
              tree.stage_name,
              e.title
            FROM
              mz_lps3_stagetaskrelation AS str
              JOIN mz_lps3_task AS t ON t.id = str.task_id AND t.type = 0
              JOIN mz_lps4_tree AS tree ON tree.stage_id = str.stage_id
              JOIN mz_lps_examine AS e ON e.id = t.project_id
              LEFT JOIN mz_lps3_usertaskrecord AS utr
                ON str.id = utr.stage_task_id AND utr.student_id = %s AND utr.class_id = %s AND is_in_sequence = 1
            WHERE tree.career_id = %s
            ORDER BY -tree.`index`,
              -str.`index`;
            """, (user_id, class_id, career_id))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)

    return main()


def get_lps_3_1_student(user_id):
    """
    获取用户的lps4报名信息
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)
    redis_key = 'get_lps_3_1_student_%s' % user_id

    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
SELECT 1
FROM mz_lps4_student
WHERE type != 2
AND user_id = %s;
            """, (user_id, ))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)

    return main(_enable_cache=True)


def get_lps_3_student(user_id, nor_class_list):
    """
    获取用户的lps4报名信息
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
        assert isinstance(nor_class_list, list)
    except (ValueError, AssertionError):
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)
    redis_key = 'get_lps_3_student_%s' % user_id

    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
SELECT 1
FROM mz_lps_classstudents AS cs
  JOIN mz_lps_class AS c ON cs.student_class_id = c.id
WHERE user_id = %s
      AND cs.status = 1
      AND soft_del = 0
      AND c.class_type = 0
      AND c.is_active = 1
      AND c.id NOT IN (%s);
            """ % ('%s', ','.join(map(lambda x: '%s', nor_class_list))), tuple([user_id] + nor_class_list))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)

    return main(_enable_cache=True)
