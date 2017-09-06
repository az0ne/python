# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_try_learn_list(conn, cursor, page_index=1, page_size=10, mobile=None,
                       try_learn_name=None, try_learn_time=None, is_all=False):
    """
    获取试学表单
    :param conn:
    :param cursor:
    :param page_index: 第几页
    :param page_size: 每页多少条
    :param mobile: 查询条件：手机
    :param try_learn_name: 查询条件：试学课程名
    :param try_learn_time: 查询条件：试学时间
    :param is_all: 是否返回所有数据
    :return: 试学表单。
            字段：姓名（昵称）、手机、麦子账号、
                 试学课程、试学班老师、试学时间
    """

    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
        SELECT
            {where}
        FROM
            mz_lps_class AS mlc
        INNER JOIN mz_lps_classstudents AS mlcs ON mlcs.student_class_id = mlc.id
        INNER JOIN mz_lps_classteachers AS mlct ON mlct.teacher_class_id = mlc.id AND mlct.is_active = 1
        INNER JOIN mz_user_userprofile AS teacher ON teacher.id = mlct.teacher_id
        INNER JOIN mz_user_userprofile AS student ON student.id = mlcs.user_id
        INNER JOIN mz_course_careercourse AS mccc ON mccc.id = mlc.career_course_id
        WHERE
            mlc.class_type = 3 AND mlcs.soft_del = 0
    """

    base_field = []
    if mobile:
        base_sql += " AND student.mobile LIKE %s "
        mobile = '%' + str(mobile) + '%'
        base_field.append(mobile)
    if try_learn_name:
        base_sql += " AND mccc.`name` LIKE %s "
        try_learn_name = '%' + try_learn_name + '%'
        base_field.append(try_learn_name)
    if try_learn_time:
        base_sql += " AND mlc.`name` LIKE %s "
        try_learn_time = '%' + try_learn_time + '%'
        base_field.append(try_learn_time)

    sql = base_sql.format(
        where="""student.id,
                mlc.id AS class_id,
                student.nick_name,
                student.mobile,
                student.username,
                mccc.`name` AS try_learn_name,
                teacher.nick_name AS teacher_name,
                mlc.`name` AS try_learn_time,
                mlcs.created AS join_class_date,
                (SELECT
                        startline
                    FROM
                        mz_lps3_classmeeting
                    WHERE id IN (
                        SELECT
                            mlcmr.class_meeting_id
                        FROM
                            mz_lps3_classmeetingrelation AS mlcmr
                        WHERE
                            mlcmr.class_id = mlcs.student_class_id
                    ) AND content = '首次班会'
                ) AS first_startline,
                (SELECT
                        startline
                    FROM
                        mz_lps3_classmeeting
                    WHERE id IN (
                        SELECT
                            mlcmr.class_meeting_id
                        FROM
                            mz_lps3_classmeetingrelation AS mlcmr
                        WHERE
                            mlcmr.class_id = mlcs.student_class_id
                    ) AND content = '答疑班会'
                ) AS QA_startline""")

    sql += ' GROUP BY mlc.id, student.mobile '

    sql += ' ORDER BY first_startline DESC, try_learn_name,  join_class_date DESC'

    field = base_field[:]
    if not is_all:
        sql += ' LIMIT %s, %s '
        field.extend([start_index, page_size])

    count_sql = base_sql.format(where='student.id')
    count_sql = 'SELECT COUNT(*) as `count` FROM ({0}) AS a'.format(count_sql)

    try:
        cursor.execute(sql, field)
        result = cursor.fetchall()
        log.info("query: %s" % cursor.statement)

        if base_field:
            cursor.execute(count_sql, base_field)
        else:
            cursor.execute(count_sql)
        rows_count = cursor.fetchone()["count"]
        log.info("query: %s" % cursor.statement)

        page_count = tool.get_page_count(rows_count, page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=dict(try_learn_list=result,
                                 page=dict(rows_count=rows_count, page_count=page_count,
                                           page_size=page_size, page_index=page_index)))


@dec_make_conn_cursor
@dec_timeit
def get_try_learn_detail(conn, cursor, class_id, student_id):
    """
    获取试学详情
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: 试学详情。
            字段：姓名（昵称）、手机、麦子账号、
                 试学课程、试学班老师、试学时间
    """

    sql = """
        SELECT
            student.id,
            student.nick_name,
            student.mobile,
            student.username,
            mccc.`name` AS try_learn_name,
            teacher.nick_name AS teacher_name,
            mlc.`name` AS try_learn_time,
            mlc.id AS class_id,
            mlcs.created AS join_class_date,
            (SELECT
                    startline
                FROM
                    mz_lps3_classmeeting
                WHERE id IN (
                    SELECT
                        mlcmr.class_meeting_id
                    FROM
                        mz_lps3_classmeetingrelation AS mlcmr
                    WHERE
                        mlcmr.class_id = mlcs.student_class_id
                ) AND content = '首次班会'
            ) AS first_startline,
            (SELECT
                    startline
                FROM
                    mz_lps3_classmeeting
                WHERE id IN (
                    SELECT
                        mlcmr.class_meeting_id
                    FROM
                        mz_lps3_classmeetingrelation AS mlcmr
                    WHERE
                        mlcmr.class_id = mlcs.student_class_id
                ) AND content = '答疑班会'
            ) AS QA_startline
        FROM
            mz_lps_class AS mlc
        INNER JOIN mz_lps_classstudents AS mlcs ON mlcs.student_class_id = mlc.id
        INNER JOIN mz_user_userprofile AS teacher ON teacher.id = mlc.teacher_id
        INNER JOIN mz_user_userprofile AS student ON student.id = mlcs.user_id
        INNER JOIN mz_course_careercourse AS mccc ON mccc.id = mlc.career_course_id
        WHERE
            mlc.class_type = 3 AND mlc.id = %s AND student.id = %s
    """

    try:
        cursor.execute(sql, (class_id, student_id))
        result = cursor.fetchone()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def is_in_meeting(conn, cursor, class_id, student_id):
    """
    是否参加班会
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: 是否参加班会 0表示未参加，大于0表示参加过
             {in_first_meeting: 是否参加首次班会
             in_QA_meeting: 是否参加答疑班会}
    """

    sql = """
        SELECT
            SUM(!ISNULL(mlcmg.id)) AS in_first_meeting,
            SUM(!ISNULL(mlcmg2.id)) AS in_QA_meeting
        FROM
            mz_lps3_classmeetingrelation AS mlcmr
        INNER JOIN mz_lps3_classmeeting AS mlcm ON mlcm.id = mlcmr.class_meeting_id
        LEFT OUTER JOIN mz_lps3_classmeetingattendance AS mlcmg ON mlcmg.class_meeting_id = mlcm.id
          AND mlcmg.student_id = %s AND mlcmg.status != 'absent' AND mlcm.content = '首次班会'
        LEFT JOIN mz_lps3_classmeetingattendance AS mlcmg2 ON mlcmg2.class_meeting_id = mlcm.id
          AND mlcmg2.student_id = %s AND mlcmg2.status != 'absent' AND mlcm.content = '答疑班会'
        WHERE
            mlcmr.class_id = %s
    """

    try:
        cursor.execute(sql, (student_id, student_id, class_id))
        result = cursor.fetchone()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def is_submit_task(conn, cursor, class_id, student_id):
    """
    是否提交作业
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: 是否提交作业 0表示未提交，大于0表示提交过
    """

    sql = """
        SELECT
            COUNT(utr.id) AS is_submit_task
        FROM
            mz_lps3_usertaskrecord utr
        WHERE utr.class_id = %s
          AND utr.student_id = %s
          AND utr.`status` = 'PASS'
          AND utr.`status` = 'DONE'
    """

    try:
        cursor.execute(sql, (class_id, student_id))
        result = cursor.fetchone()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def is_submit_questionnaire(conn, cursor, class_id, student_id):
    """
    是否提交满意度调查表
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: 是否提交满意度调查表 0表示未提交，大于0表示提交过
    """

    sql = """
        SELECT
            COUNT(mfqr.id) AS is_submit_questionnaire
        FROM
            mz_free_questionnaire_record AS mfqr
        WHERE mfqr.class_id = %s
          AND mfqr.student_id = %s
    """

    try:
        cursor.execute(sql, (class_id, student_id))
        result = cursor.fetchone()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def get_questionnaire_records(conn, cursor, class_id, student_id):
    """
    获取满意度调查表
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: 满意度调查表
             id，问卷名，题干名，题干选项，学生选择
    """

    sql = """
        SELECT
            mfq.id,
            mfq.`name`,
            mfqi.stem,
            mfqi.ques_options,
            mfqr.record
        FROM
            mz_free_questionnaire_record AS mfqr
        INNER JOIN mz_free_questionnaire AS mfq ON mfq.id = mfqr.questionnaire_id
        INNER JOIN mz_free_questionnaire_item AS mfqi ON mfqi.id = mfqr.questionnaire_item_id
        WHERE
            mfqr.class_id = %s AND mfqr.student_id = %s
    """

    try:
        cursor.execute(sql, (class_id, student_id))
        result = cursor.fetchall()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def del_student_from_class(conn, cursor, class_id, student_id):
    """
    从一个班删除一个学生（软删除） 1为已删除
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: True or False
    """

    sql = """
        UPDATE mz_lps_classstudents
        SET soft_del = 1
        WHERE
            student_class_id = %s
        AND user_id = %s
    """

    try:
        cursor.execute(sql, (class_id, student_id))
        conn.commit()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def del_try_learn_record(conn, cursor, class_id, student_id):
    """
    清除某个学生在某个班的试学产生的所有数据
    :param conn:
    :param cursor:
    :param class_id:
    :param student_id:
    :return: True or False
    """

    # 学生知识点完成度记录
    del_item_record = """
        DELETE
        FROM
            mz_lps3_userknowledgeitemrecord
        WHERE
            class_id = %s
        AND student_id = %s;
    """

    # 学生参加班会记录表
    del_class_meeting_record = """
        DELETE cma.*
        FROM
            mz_lps3_classmeetingrelation AS cmr
        INNER JOIN mz_lps3_classmeetingattendance AS cma
          ON cma.class_meeting_id = cmr.class_meeting_id
        WHERE
            cmr.class_id = %s AND cma.student_id = %s;
    """

    # 学生提交作业记录表
    del_user_task_record = """
        DELETE FROM
            mz_lps3_usertaskrecord
        WHERE
            class_id = %s
        AND student_id = %s;
    """

    # 学生满意度调查表填写记录
    del_user_questionnaire_record = """
        DELETE FROM
            mz_free_questionnaire_record
        WHERE
            class_id = %s
        AND student_id = %s;
    """

    # 班级学生关联表
    del_student_record = """
        DELETE FROM
            mz_lps_classstudents
        WHERE
            student_class_id = %s
        AND user_id = %s;
    """

    try:
        cursor.execute(del_item_record, (class_id, student_id))
        cursor.execute(del_class_meeting_record, (class_id, student_id))
        cursor.execute(del_user_task_record, (class_id, student_id))
        cursor.execute(del_user_questionnaire_record, (class_id, student_id))
        cursor.execute(del_student_record, (class_id, student_id))
        conn.commit()

        log.info("query:%s" % cursor.statement)
    except Exception as e:
        conn.rollback()

        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)
