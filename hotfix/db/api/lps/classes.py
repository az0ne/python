# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


def get_free_teacher_class(class_id):
    try:
        class_id = int(class_id)
    except ValueError:
        log.warn('class_id is not a int')
        return APIResult(code=False)

    @dec_timeit('get_free_teacher_class')
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
                SELECT
                    c. NAME AS class_name,
                    cc. NAME AS ccourse_name,
                    str.id AS stage_task_id,
                    COUNT(DISTINCT cs.id) AS student_count,
                    GROUP_CONCAT(DISTINCT cm1.id) AS first_meeting_id,
                    GROUP_CONCAT(DISTINCT cm2.id) AS answer_meeting_id,
                    GROUP_CONCAT(DISTINCT cm1.`status`) AS first_meeting_status,
                    GROUP_CONCAT(DISTINCT cm2.`status`) AS answer_meeting_status
                FROM
                    mz_lps_class AS c
                JOIN mz_course_careercourse AS cc ON cc.id = c.career_course_id
                JOIN mz_course_stage AS s ON (
                    s.career_course_id = cc.id
                    AND s.lps_version = '3.0'
                )
                JOIN mz_lps3_stagetaskrelation AS str ON str.stage_id = s.id
                JOIN mz_lps3_task AS t ON (
                    t.id = str.task_id
                    AND t.type = 1
                )
                LEFT JOIN mz_lps_classstudents AS cs ON (
                    cs.student_class_id = c.id
                    AND cs.`status` = 1
                )
                LEFT JOIN mz_lps3_classmeetingrelation AS cmr ON c.id = cmr.class_id
                LEFT JOIN mz_lps3_classmeeting AS cm1 ON (
                    cmr.class_meeting_id = cm1.id
                    AND cm1.content = "首次班会"
                )
                LEFT JOIN mz_lps3_classmeeting AS cm2 ON (
                    cmr.class_meeting_id = cm2.id
                    AND cm2.content = "答疑班会"
                )
                WHERE
                    c.id = % s
                AND c.class_type = 3;
            """
            cursor.execute(sql, (class_id,))
            free_teacher_class = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=free_teacher_class)

    return main()


def get_free_class_student(class_id, stage_task_id):
    try:
        class_id = int(class_id)
        stage_task_id = int(stage_task_id)
    except ValueError:
        log.warn('class_id is not a int')
        return APIResult(code=False)

    @dec_timeit('get_free_class_student')
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
                SELECT
                    u.id AS user_id,
                    u.real_name AS real_name,
                    u.nick_name AS nick_name,
                    u.avatar_small_thumbnall AS avatar,
                    u.mobile AS mobile,
                    GROUP_CONCAT(cma1.`status`) AS status_1,
                    GROUP_CONCAT(cma2.`status`) AS status_2,
                    utr.`status` AS task_status
                FROM
                    mz_lps_classstudents AS cs
                JOIN mz_user_userprofile AS u ON u.id = cs.user_id
                LEFT JOIN mz_lps3_usertaskrecord AS utr ON (
                    utr.class_id = cs.student_class_id
                    AND utr.student_id = u.id
                    AND utr.stage_task_id = %s
                    AND utr.is_in_sequence = 1
                )
                LEFT JOIN mz_lps3_classmeetingrelation AS cmr ON cs.student_class_id = cmr.class_id
                LEFT JOIN mz_lps3_classmeeting AS cm1 ON (
                    cmr.class_meeting_id = cm1.id
                    AND cm1.content = "首次班会"
                )
                LEFT JOIN mz_lps3_classmeeting AS cm2 ON (
                    cmr.class_meeting_id = cm2.id
                    AND cm2.content = "答疑班会"
                )
                LEFT JOIN mz_lps3_classmeetingattendance AS cma1 ON (
                    cm1.id = cma1.class_meeting_id
                    AND cma1.student_id = cs.user_id
                )
                LEFT JOIN mz_lps3_classmeetingattendance AS cma2 ON (
                    cm2.id = cma2.class_meeting_id
                    AND cma2.student_id = cs.user_id
                )
                WHERE
                    cs.student_class_id = %s
                AND cs.is_pause = 0
                AND cs.`status` = 1
                GROUP BY
                    cs.id;
            """
            cursor.execute(sql, (stage_task_id, class_id))
            free_class_student = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=free_class_student)

    return main()


def get_free_class_teacher_info_by_career_course_id(career_course_id):
    """
    获取免费试学班信息
    :param career_course_id:
    :return:
    """
    redis_key = 'get_free_class_teacher_info_by_career_course_id%s' % career_course_id

    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT
                    GROUP_CONCAT(_class.id ORDER BY _cm1.startline) AS str_class_id,
                    _teacher.id,
                    _teacher.nick_name,
                    _teacher.real_name,
                    _teacher.avatar_url,
                    _teacher.position,
                    _teacher.description
            FROM
                    mz_lps_class AS _class
            INNER  JOIN mz_lps3_classmeetingrelation AS _cmrel ON _cmrel.class_id = _class.id
            INNER  JOIN mz_lps3_classmeeting AS _cm1 ON (_cm1.id = _cmrel.class_meeting_id
             AND _cm1.content='首次班会' AND _cm1.status=0)
            LEFT JOIN mz_lps_classteachers AS ct ON ct.teacher_class_id = _class.id
            LEFT JOIN mz_user_userprofile AS _teacher ON _teacher.id = ct.teacher_id
            WHERE
                    _class.career_course_id=%s
                    AND _class.meeting_enabled=True
                    AND _class.class_type=3
                    AND _class.lps_version=3.0

            GROUP BY _teacher.id
        """
        try:
            cursor.execute(sql, (career_course_id,))
            result = cursor.fetchall()
            # logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)

    return main(_enable_cache=True)


def get_class_and_student_info_by_user_id_and_class_id(user_id, class_id):
    """
    取班级和学生信息
    :param user_id:
    :param class_id:
    :return:
    """
    try:
        user_id = int(user_id)
        class_id = int(class_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or class_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT *
        FROM mz_lps_class AS c, mz_lps_classstudents AS cs
        WHERE c.id = %s
              AND cs.user_id = %s
              AND cs.student_class_id = %s;
        """
        try:
            cursor.execute(sql, (class_id, user_id, class_id))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_user_info(id_list):
    """
    获取用户基本信息
    """
    if id_list:
        for i in id_list:
            try:
                user_id = int(i)
            except ValueError:
                return APIResult(code=False)
            if user_id <= 0:
                return APIResult(code=False)
    else:
        return APIResult(code=False)
    redis_key = 'get_user_info_%s' % '_'.join(map(lambda x: '%s', id_list))

    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
          nick_name,
          real_name,
          avatar_url,
          mobile,
          `position`,
          description
        FROM
          mz_user_userprofile
        WHERE id IN (%s);
        """ % ','.join(map(lambda x: '%s', id_list))
        try:
            cursor.execute(sql, id_list)
            result = cursor.fetchall()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        cache.set(redis_key, result, 60 * 60)
        return APIResult(result=result)

    return main()
