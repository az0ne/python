# -*- coding: utf-8 -*-
from datetime import datetime

from utils.logger import logger as log
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor
from db.cores.cache import cache
from mz_lps3.models import Task

def get_newest_normal_or_newest_experience_lps_3_1_class_id_by_user_id(user_id):
    """
    根据user_id获取最近报名的正式班和体验班的3.1的class_id(正式班优先）
    ：lps3.1该专业的正式班和试学班只能二存一
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              c.id,
              c.class_type,
              c.career_course_id
            FROM mz_lps_class AS c
              JOIN mz_lps_classstudents AS cs ON (
                cs.user_id = %s
                AND c.lps_version = '3.0'
                AND c.class_type IN (0, 4)
                AND c.is_active = 1
                AND c.student_limit = 9999
                AND cs.student_class_id = c.id)
            ORDER BY c.class_type,
              -cs.id
            LIMIT 1;
            """, (user_id, ))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps_3_1_careers_by_user_id(user_id):
    """
    根据user_id获取所报所有的lps3.1的职业课程
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              cc.id,
              cc.name,
              s.type
            FROM mz_lps4_student AS s
              JOIN mz_course_careercourse AS cc ON cc.id = s.career_id
            WHERE user_id = %s
            ORDER BY s.type;
            """, (user_id, ))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps_3_newest_normal_class_id_by_user_id(user_id):
    """
    根据user_id获取最新的lps3的class_id（正式班）
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              c.id
            FROM mz_lps_class AS c
              JOIN mz_lps_classstudents AS cs ON (
                cs.student_class_id = c.id
                AND cs.user_id = %s
                AND c.lps_version = '3.0'
                AND c.class_type = 0
                AND c.is_active = 1)
            ORDER BY -cs.id
            LIMIT 1;
            """, (user_id, ))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_newest_normal_or_newest_experience_lps_3_1_class_id_by_user_id_and_career_id(user_id, career_id):
    """
    根据user_id和career_id获取最近报名的正式班和体验班的3.1的class_id(正式班优先）
    ：lps3.1该专业的正式班和试学班只能二存一
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
        career_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              c.id,
              c.class_type,
              c.career_course_id
            FROM mz_lps_class AS c
              JOIN mz_lps_classstudents AS cs ON (
                cs.user_id = %s
                AND c.lps_version = '3.0'
                AND c.class_type IN (0, 4)
                AND c.is_active = 1
                AND c.student_limit = 9999
                AND cs.student_class_id = c.id
                AND c.career_course_id = %s)
            ORDER BY c.class_type,
              -cs.id
            LIMIT 1;
            """, (user_id, career_id))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps_3_newest_normal_class_id_by_user_id_and_career_id(user_id, career_id):
    """
    根据user_id和career_id获取最新的lps3的class_id（正式班）
    :param user_id:
    :return:
    """
    try:
        user_id = int(user_id)
        career_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute("""
            SELECT
              c.id
            FROM mz_lps_class AS c
              JOIN mz_lps_classstudents AS cs ON (
                cs.student_class_id = c.id
                AND cs.user_id = %s
                AND c.lps_version = '3.0'
                AND c.class_type = 0
                AND c.is_active = 1
                AND c.career_course_id = %s)
            ORDER BY -cs.id
            LIMIT 1;
            """, (user_id, career_id))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps_3_1_experience_class_id_by_career_id(career_id):
    """
    找到lps3.1试学班的class_id
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
            SELECT id
            FROM mz_lps_class
            WHERE career_course_id = %s
              AND lps_version = '3.0'
              AND is_active = 1
              AND class_type = 4
            ORDER BY -id
            LIMIT 1;
            """, (career_id, ))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def create_lps_3_1_experience_class_id_by_career_id(career_id, short_name, date):
    """
    创建lps3.1试学班的
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
            INSERT mz_lps_class
            SET career_course_id = %s,
              lps_version = '3.0',
              is_active = 1,
              class_type = 4,
              student_limit = 9999,
              status = 1,
              is_closed = 0,
              current_student_count = 0,
              coding="lps3.1_%s_exp",
              name="lps3.1_%s_体验班",
              date_publish=%s,
              date_open=%s,
              qq=12345,
              meeting_enabled=0,
              qq_qrcode='';
            """, (career_id, short_name, short_name, date, date))
            cursor.execute("""
            SELECT last_insert_id() AS last_class_id
            """)
            result = cursor.fetchone()['last_class_id']
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_lps4_student_info_by_user_id(user_id, career_id, data_list=[]):
    """
    获取lps4学生信息
    :param user_id:
    :param career_id:
    :param data_list: 需要查询的数据
    :return:
    """

    try:
        user_id = int(user_id)
        career_id = int(career_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        if data_list:
            str_select = ','.join(data_list)
        else:
            str_select = """*"""
        sql = """
        SELECT
          """+str_select+"""
        FROM mz_lps4_student
        WHERE user_id=%s and career_id=%s
        """
        try:
            cursor.execute(sql, (user_id, career_id))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def insert_user_to_try_class(class_id, user_id, career_id, teacher_id, time_now):
    """
    加试学班，lps4的班和lps3的班都要加
    :param user_id:
    :param career_id:
    :param data_list: 需要查询的数据
    :return:
    """

    try:
        class_id = int(class_id)
        user_id = int(user_id)
        career_id = int(career_id)
        teacher_id = int(teacher_id)
    except ValueError:
        return APIResult(code=False)
    if class_id <= 0 or user_id <= 0 or career_id <= 0 or teacher_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_lps4 = """
        REPLACE mz_lps4_student
        SET user_id = %s,
        type = 2,
        career_id = %s,
        teacher_id = %s,
        start_time = %s;
        """
        sql_lps3 = """
        REPLACE mz_lps_classstudents
        SET user_id = %s,
        student_class_id = %s,
        study_point = 0,
        is_pause = 0,
        is_view_contract = 0,
        is_view_employment_contract = 0,
        status = 1,
        is_qq_hints = 0,
        is_send_sms = 0,
        is_view_not_employment_contract = 0,
        soft_del = 0,
        created = %s;
        """
        try:
            cursor.execute(sql_lps4, (user_id, career_id, teacher_id, time_now))
            cursor.execute(sql_lps3, (user_id, class_id, time_now))
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(code=True)

    return main()


def get_lps_3_1_teacher_by_career_id(career_id):
    """
    根据career_id取老师
    :param career_id:
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
        sql = """
        SELECT * FROM mz_lps4_career_teacher WHERE career_id = %s;
        """
        try:
            cursor.execute(sql, (career_id, ))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def get_lps_3_institute_name_by_career_id(career_id):
    """
    根据career_id获取职业课程所在学院名称
    :param career_id:
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
        sql = """
        SELECT mz_course_institute.name
        FROM mz_course_careercourse as career
        inner join mz_course_institute on  career.institute_id=mz_course_institute.id
        WHERE career.id = %s;
        """
        try:
            cursor.execute(sql, (career_id, ))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def get_lps4_teacher_by_career_student_id(career_id, student_id):
    """
    根据career_id + student_id取老师
    :param career_id:
    :param student_id:
    :return:
    """
    try:
        career_id = int(career_id)
        student_id = int(student_id)
    except ValueError:
        return APIResult(code=False)
    if career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT teacher.*
        FROM mz_lps4_student AS s
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = s.teacher_id
        WHERE s.career_id = %s AND s.user_id = %s;
        """
        try:
            cursor.execute(sql, (career_id, student_id))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def get_lps4_teacher_by_student_id(student_id):
    """
    根据student_id取老师
    :param student_id:
    :return:
    """
    try:
        student_id = int(student_id)
    except ValueError:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT teacher.*
        FROM mz_lps4_student AS s
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = s.teacher_id
        WHERE s.user_id = %s;
        """
        try:
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def insert_user_to_normal_class(user_id, lps4_student_type, career_id, teacher_id, time_now, time_graduate):
    """
    加lps3.1的正常班
    :param user_id:
    :param career_id:
    :param data_list: 需要查询的数据
    :return:
    """

    try:
        user_id = int(user_id)
        career_id = int(career_id)
        teacher_id = int(teacher_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or career_id <= 0 or teacher_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        REPLACE mz_lps4_student
        SET user_id = %s,
        type = %s,
        career_id = %s,
        teacher_id = %s,
        start_time = %s,
        end_time = %s;
        """
        try:
            cursor.execute(sql, (user_id, lps4_student_type, career_id, teacher_id, time_now, time_graduate))
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(code=True)

    return main()


@dec_make_conn_cursor
def get_students_by_lps4(conn, cursor, teacher_id, career_id):
    """
    获取老师所带的某个专业的学生
    :param conn:
    :param cursor:
    :param teacher_id:
    :param career_id:
    :return:
    """

    sql = """
        SELECT
            *
        FROM
            mz_lps4_student
        WHERE
            teacher_id = %s
        AND career_id = %s
        AND type != 2
        AND '{:%Y-%m-%d %H:%M:%S}' < end_time
    """.format(datetime.now())

    try:
        cursor.execute(sql, (teacher_id, career_id))
        result = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_make_conn_cursor
def get_students_info(cnn, cursor, career_id, user_ids):
    """

    :param cnn:
    :param cursor:
    :param career_id:
    :param user_ids:
    :return:
    """

    sql = """
        SELECT
            student.id,
            student.real_name,
            student.nick_name,
            student.qq,
            student.avatar_small_thumbnall,
            student.email AS real_email,
            student.mobile AS real_mobile,
            cstudent.is_pause,
            cstudent.pause_datetime,
            cstudent.deadline,
            province.`name` AS province_name,
            city.`name` AS city_name,
            jobinfo.`degree` AS degree,
            cstudent.is_employment_contract AS is_employment_contract,
            _institute.name AS institute_name,
            cstudent.created,
            cstudent.status,
            cstudent.quit_datetime
        FROM
            mz_user_userprofile AS student
        LEFT JOIN mz_lps_classstudents AS cstudent ON cstudent.user_id = student.id
        LEFT JOIN mz_user_citydict AS city ON city.id = student.city_id
        LEFT JOIN mz_user_provincedict AS province ON province.id = city.province_id
        LEFT JOIN mz_course_careercourse AS _c_course ON _c_course.id = %s
        LEFT JOIN mz_course_institute AS _institute ON _institute.id = _c_course.institute_id
        LEFT JOIN mz_user_userjobinfo AS jobinfo ON jobinfo.user_id = student.id and jobinfo.career_course_id = _c_course.id
        WHERE
            student.id IN %s GROUP BY student.id
    """

    ids = '({0})'.format(', '.join([str(_id) for _id in user_ids]))

    try:
        cursor.execute(sql % (career_id, ids))
        result = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


def is_join_lps4_job_class(user_id):
    """
    是否加入lps4的就业班
    :param user_id:
    :return:
    """

    try:
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
          1
        FROM mz_lps4_student
        WHERE user_id=%s and type=1 and is_stop=0
        limit 1
        """
        try:
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def app_get_my_student_by_teacher_id(teacher_id):
    """
    获取我的学生by老师
    :param teacher_id:
    :return:
    """

    try:
        teacher_id = int(teacher_id)
    except ValueError:
        return APIResult(code=False)
    if teacher_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
          s.career_id,
          s.user_id,
          u.avatar_small_thumbnall,
          u.real_name,
          u.nick_name,
          s.end_time,
          cc.name
        FROM mz_lps4_student AS s
          JOIN mz_user_userprofile AS u ON u.id = s.user_id
          JOIN mz_course_careercourse AS cc ON cc.id = s.career_id
        WHERE teacher_id = %s
        AND type != 2
        AND (s.end_time - s.start_time) > 0;
        """
        try:
            cursor.execute(sql, (teacher_id,))
            result = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)

    return main()


@dec_make_conn_cursor
def student_study_goal(conn, cursor, user_id, career_id):
    """
    获取学习目标
    :param user_id:
    :param career_id:
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: student_study_goal : career_id must be int')
        return APIResult(code=False)
    if not isinstance(user_id, int):
        log.warn('type error: student_study_goal : user_id must be int')
        return APIResult(code=False)

    sql_domin = """
        SELECT institute.name FROM mz_course_careercourse AS cc
        INNER JOIN mz_course_institute AS institute ON institute.id = cc.institute_id
        WHERE cc.id=%s
        """

    sql_goal = """
        SELECT studygoal.name FROM mz_user_userstudygoal AS userstudygoal
        INNER JOIN mz_user_studygoal AS studygoal ON userstudygoal.goal_id = studygoal.id
        WHERE userstudygoal.user_id=%s AND userstudygoal.domain_name=%s

        """

    try:
        cursor.execute(sql_domin, (career_id,))
        result = cursor.fetchone()
        cursor.execute(sql_goal, (user_id, result['name']))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


def check_is_lps4_paid_user(career_id, user_id):
    """
    check 是否是lps4付费学生
    :param career_id:
    :param user_id:
    :return:
    """

    try:
        career_id = int(career_id)
        user_id = int(user_id)
    except ValueError:
        return APIResult(code=False)
    if user_id <= 0 or career_id <= 0:
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT 1
FROM mz_lps4_student
WHERE career_id = %s AND user_id = %s AND type != 2;
        """
        try:
            cursor.execute(sql, (career_id, user_id))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()
