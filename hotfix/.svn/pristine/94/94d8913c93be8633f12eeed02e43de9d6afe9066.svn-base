# -*- coding: utf-8 -*-
import datetime
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_make_conn_cursor, dec_get_cache


@dec_timeit("student_service_count")
@dec_make_conn_cursor
def student_service_count(conn, cursor, career_id, student_id, teacher_id):
    """
    学习建议总数
    :param conn:
    :param cursor:
    :param career_id:
    :param student_id:
    :param teacher_id:
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: student_service_count : career_id must be int')
        return APIResult(code=False)
    if not isinstance(student_id, int):
        log.warn('type error: student_service_count : student_id must be int')
        return APIResult(code=False)
    if not isinstance(teacher_id, int):
        log.warn('type error: student_service_count : teacher_id must be int')
        return APIResult(code=False)

    sql_1 = """
        SELECT total_count FROM mz_onevone_service_message_teacher_count
        WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """
    sql_2 = """
        SELECT COUNT(*) AS total_count FROM mz_onevone_service WHERE
        career_id=%s AND user_id=%s
    """
    try:
        if teacher_id:
            sql = sql_1 % (career_id, student_id, teacher_id)
        else:
            sql = sql_2 % (career_id, student_id)
        cursor.execute(sql)
        count = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=count)


@dec_timeit("student_service_list")
@dec_make_conn_cursor
def service_list(conn, cursor, career_id, student_id, teacher_id, start_index, end_index):
    """
    学习建议列表
    :param conn:
    :param cursor:
    :param start_index:
    :param end_index:
    :param career_id: 职业课程ID
    :param student_id: 学生ID
    :param teacher_id: 老师ID
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: student_service_count : career_id must be int')
        return APIResult(code=False)
    if not isinstance(student_id, int):
        log.warn('type error: student_service_count : student_id must be int')
        return APIResult(code=False)
    if not isinstance(teacher_id, int):
        log.warn('type error: student_service_count : teacher_id must be int')
        return APIResult(code=False)
    if not isinstance(start_index, int):
        log.warn('type error: student_service_count : start_index must be int')
        return APIResult(code=False)
    if not isinstance(end_index, int):
        log.warn('type error: student_service_count : end_index must be int')
        return APIResult(code=False)
    
    sql1 = """
        SELECT s.id AS id,
               sc.user_id AS user_id,
               s.teacher_unread AS teacher_unread,
               s.student_unread AS student_unread,
               sc.comment AS content,
               s.source AS source,
               sc.create_date AS create_date,
               sc.nick_name AS nick_name,
               sc.head AS head
        FROM mz_onevone_service AS s
            INNER JOIN mz_onevone_service_comment AS sc ON sc.service_id = s.id
            WHERE s.career_id=%s AND s.user_id=%s AND s.teacher_id=%s
            GROUP BY sc.service_id
            ORDER BY s.create_date DESC
            LIMIT %s,%s
        """

    sql2 = """
        SELECT s.id AS id,
               sc.user_id AS user_id,
               s.teacher_unread AS teacher_unread,
               s.student_unread AS student_unread,
               sc.comment AS content,
               s.source AS source,
               sc.create_date AS create_date,
               sc.nick_name AS nick_name,
               sc.head AS head
        FROM mz_onevone_service AS s
            INNER JOIN mz_onevone_service_comment AS sc ON sc.service_id = s.id
            WHERE s.career_id=%s AND s.user_id=%s
            GROUP BY sc.service_id
            ORDER BY s.create_date DESC
            LIMIT %s,%s
        """
    try:
        if teacher_id:
            sql = sql1 % (career_id, student_id, teacher_id, start_index, end_index)
        else:
            sql = sql2 % (career_id, student_id, start_index, end_index)
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("one_ro_one_service_detail")
@dec_make_conn_cursor
def clean_new_service_count(conn, cursor, career_id, user_id, teacher_id, user):
    """
    进入列表清除新服务数
    :param conn:
    :param cursor:
    :param career_id:
    :param user_id:
    :param teacher_id:
    :param user:
    :return:
    """
    sql_select = """
    SELECT 1 FROM mz_onevone_service_message_teacher_count WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """
    sql_update = """
    UPDATE mz_onevone_service_message_teacher_count SET new_service_count=0 WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_select_student = """
    SELECT 1 FROM mz_onevone_service_message_user_count WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_update_student = """
    UPDATE mz_onevone_service_message_user_count SET new_service_count=0 WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """
    try:
        if user.is_student():
            cursor.execute(sql_select_student, (career_id, user_id, teacher_id))
            is_exists = cursor.fetchone()
            if is_exists:
                cursor.execute(sql_update_student, (career_id, user_id, teacher_id))
                conn.commit()
        else:
            cursor.execute(sql_select, (career_id, user_id, teacher_id))
            is_exists = cursor.fetchone()
            if is_exists:
                cursor.execute(sql_update, (career_id, user_id, teacher_id))
                conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_service_detail_and_count")
@dec_make_conn_cursor
def get_service_detail_and_count(conn, cursor, service_id):
    """
    获取service详情 和 回复总数
    :param conn:
    :param cursor:
    :param service_id:
    :return:
    """
    sql = """
    SELECT * FROM mz_onevone_service WHERE id=%s
    """
    sql_count = """
    SELECT COUNT(*) AS total_count FROM mz_onevone_service_comment WHERE service_id=%s
    """
    try:
        cursor.execute(sql, (service_id,))
        service = cursor.fetchone()
        cursor.execute(sql_count, (service_id,))
        total_count = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result={'service': service, 'total_count': total_count['total_count']})


@dec_timeit("one_ro_one_service_detail")
@dec_make_conn_cursor
def one_to_one_service_detail(conn, cursor, service_id, start_index, end_index):
    """
    学生学习建议详情
    :param conn:
    :param cursor:
    :param service_id: 学习建议ID
    :param start_index:
    :param end_index:
    :return:
    """

    sql_comment = """
        SELECT * FROM mz_onevone_service_comment
            WHERE service_id=%s
            LIMIT %s,%s
        """
    try:
        cursor.execute(sql_comment, (service_id, start_index, end_index))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("clean_service_message_count")
@dec_make_conn_cursor
def clean_service_message_count(conn, cursor, service, user):
    """
    清除相关回复数
    :param conn:
    :param cursor:
    :param service:
    :param user:
    :return:
    """
    sql_teacher = """
        UPDATE mz_onevone_service SET teacher_unread=0 WHERE
        id=%s
        """
    sql_student = """
        UPDATE mz_onevone_service SET student_unread=0 WHERE
        id=%s
        """
    sql_student_message = """
        UPDATE mz_onevone_service_message_user_count SET new_comment_count=new_comment_count-%s
        WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """
    sql_teacher_message = """
        UPDATE mz_onevone_service_message_teacher_count SET new_comment_count=new_comment_count-%s
        WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """
    try:
        if user.is_student():
            cursor.execute(sql_student, (service['id'],))
            sql_student_message = sql_student_message % (service['student_unread'], service['career_id'],
                                                         service['user_id'], service['teacher_id'])
            cursor.execute(sql_student_message)
        else:
            cursor.execute(sql_teacher, (service['id'],))
            sql_teacher_message = sql_teacher_message % (service['teacher_unread'], service['career_id'],
                                                         service['user_id'], service['teacher_id'])
            cursor.execute(sql_teacher_message)
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("create_new_service")
@dec_make_conn_cursor
def create_new_service(conn, cursor, **kwargs):
    """
    新建学习建议
    :param conn:
    :param cursor:
    :param kwargs:
    :return:
    """
    sql_service = """
        INSERT INTO mz_onevone_service (career_id, user_id, teacher_id, teacher_name, teacher_head, create_date,
                                        comment_date, source_type, source, student_unread, teacher_unread)
        VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

    sql_comment = """
        INSERT INTO mz_onevone_service_comment
        (service_id, comment, user_id, nick_name, head, create_date)
        VALUE
        (%s,%s,%s,%s,%s,%s)
        """

    sql_user = """
    SELECT 1 FROM mz_onevone_service_message_user_count WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_user_insert = """
    INSERT INTO mz_onevone_service_message_user_count (career_id, user_id, teacher_id, new_service_count, new_comment_count)
    VALUE (%s,%s,%s,%s,%s)
    """

    sql_user_update = """
    UPDATE mz_onevone_service_message_user_count SET
    new_service_count=new_service_count+1,new_comment_count=new_comment_count+1
    WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_teacher = """
    SELECT 1 FROM mz_onevone_service_message_teacher_count WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_teacher_insert = """
    INSERT INTO mz_onevone_service_message_teacher_count
    (career_id, user_id, teacher_id, total_count, new_service_count, new_comment_count)
    VALUE (%s,%s,%s,%s,%s,%s)
    """

    sql_teacher_update = """
    UPDATE mz_onevone_service_message_teacher_count SET
    total_count=total_count+1
    WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """

    student_sql_teacher_update = """
    UPDATE mz_onevone_service_message_teacher_count SET
    total_count=total_count+1,new_comment_count=new_comment_count+1,new_service_count=new_service_count+1
    WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """
    try:
        cursor.execute(sql_service, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                     kwargs['teacher_nick_name'], kwargs['teacher_avatar_url'],
                                     kwargs['now'], kwargs['now'], kwargs['source_type'], kwargs['source'],
                                     kwargs['student_unread'], kwargs['teacher_unread']))
        cursor.execute('SELECT LAST_INSERT_ID()')
        service_id = cursor.fetchall()
        cursor.execute(sql_comment, (service_id[0]['LAST_INSERT_ID()'], kwargs['content'], kwargs['user_id'], kwargs['user_nick_name'],
                                     kwargs['user_avatar_url'], kwargs['now']))
        # 学生
        if kwargs['is_student']:
            # 老师
            cursor.execute(sql_teacher, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            is_exists = cursor.fetchone()
            if is_exists:
                cursor.execute(student_sql_teacher_update, (kwargs['career_id'], kwargs['student_id'],
                                                            kwargs['teacher_id']))
            else:
                cursor.execute(sql_teacher_insert, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                                    1, 1, 1))
            # 学生
            cursor.execute(sql_user, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            is_exists = cursor.fetchone()
            if not is_exists:
                cursor.execute(sql_user_insert, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                                 0, 0))
        else:
            # 学生
            cursor.execute(sql_user, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            is_exists = cursor.fetchone()
            if is_exists:
                cursor.execute(sql_user_update, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            else:
                cursor.execute(sql_user_insert, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                                 1, 1))
            # 老师
            cursor.execute(sql_teacher, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            is_exists = cursor.fetchone()
            if is_exists:
                cursor.execute(sql_teacher_update, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id']))
            else:
                cursor.execute(sql_teacher_insert, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                                    1, 0, 0))

        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=service_id)


@dec_timeit("add_service_reply")
@dec_make_conn_cursor
def add_service_reply(conn, cursor, service, user, content):
    """
    新增学习建议回复
    :param conn:
    :param cursor:
    :param service:
    :param user:
    :param content:
    :return:
    """
    sql = """
        INSERT INTO mz_onevone_service_comment
        (service_id, comment, user_id, nick_name, head, create_date)
        VALUE
        (%s,%s,%s,%s,%s,%s)
        """
    sql_service_stu = """
        UPDATE mz_onevone_service SET student_unread = student_unread+1
        WHERE id=%s
    """
    sql_service_tea = """
        UPDATE mz_onevone_service SET teacher_unread = teacher_unread+1
        WHERE id=%s
    """
    sql_user_update = """
    UPDATE mz_onevone_service_message_user_count SET
    new_comment_count=new_comment_count+1
    WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_teacher_update = """
    UPDATE mz_onevone_service_message_teacher_count SET
    new_comment_count=new_comment_count+1
    WHERE career_id=%s AND user_id=%s AND teacher_id=%s
    """
    try:
        cursor.execute(sql, (service['id'], content, user.id, user.real_name or user.nick_name, user.avatar_url,
                             datetime.datetime.now()))
        if user.is_student():
            cursor.execute(sql_service_tea, (service['id'],))
            cursor.execute(sql_teacher_update, (service['career_id'], service['user_id'], service['teacher_id']))
        else:
            cursor.execute(sql_service_stu, (service['id'],))
            cursor.execute(sql_user_update, (service['career_id'], service['user_id'], service['teacher_id']))
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_user_name")
@dec_make_conn_cursor
def get_user_name(conn, cursor, user_id):
    sql = """
    SELECT nick_name, real_name, avatar_url, mobile FROM mz_user_userprofile WHERE id=%s
    """
    try:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("check_into_service")
@dec_make_conn_cursor
def check_into_service(conn, cursor, career_id, teacher_id, student_id):
    """
    检查进入权限
    :param conn:
    :param cursor:
    :param career_id:
    :param teacher_id:
    :param student_id:
    :return:
    """
    sql = """
        SELECT 1 FROM mz_lps4_student WHERE
        career_id=%s AND teacher_id=%s AND user_id=%s AND mz_lps4_student.type != 2
        """
    try:
        data = False
        cursor.execute(sql, (career_id, teacher_id, student_id))
        result = cursor.fetchone()
        if result:
            data = True
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_teacher_by_lps4")
@dec_make_conn_cursor
def get_teacher_by_lps4(conn, cursor, career_id, student_id):
    """
    获取老师ID
    :param conn:
    :param cursor:
    :param career_id:
    :param student_id: 23811   684  2
    :return:
    """
    sql = """
        SELECT teacher_id FROM mz_lps4_student WHERE
        career_id=%s AND user_id=%s AND mz_lps4_student.type != 2
        """
    try:
        cursor.execute(sql, (career_id, student_id))
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_lps4_student_career")
@dec_make_conn_cursor
def get_lps4_student_career(conn, cursor, user_id):
    """
    获取LPS4学生付费专业
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    sql = """
        SELECT career_id FROM mz_lps4_student
        WHERE user_id=%s AND type!=2
        """
    try:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_teacher_unread")
@dec_make_conn_cursor
def get_teacher_unread(conn, cursor, career_id, student_list, teacher_id):
    """
    老师端未读数
    :param conn:
    :param cursor:
    :param student_list:
    :return:
    """
    sql = """
    SELECT user_id, total_count, new_coach_count, new_comment_count
    FROM mz_coach_message_teacher_count WHERE
    career_id=%s AND teacher_id=%s AND user_id IN (%s)
    """
    try:
        sql = sql % (career_id, teacher_id, ','.join(map(lambda x: '%s', student_list)))
        cursor.execute(sql, student_list)
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_teacher_total_unread_count")
@dec_make_conn_cursor
def get_teacher_total_unread_count(conn, cursor, teacher_id):
    """
    老师端未读数
    :param conn:
    :param cursor:
    :param teacher_id:
    :return:
    """
    sql = """
    SELECT SUM(new_comment_count) AS total_count FROM mz_onevone_service_message_teacher_count
    WHERE teacher_id=%s
    """
    try:
        cursor.execute(sql, (teacher_id,))
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_student_unread")
@dec_make_conn_cursor
def get_student_unread(conn, cursor, career_id, teacher_id, student_id):
    """
    学生端未读数
    :param conn:
    :param cursor:
    :param student_id:
    :return:
    """
    sql = """
    SELECT new_comment_count FROM mz_coach_message_user_count
    WHERE career_id=%s AND user_id=%s
    """
    try:
        cursor.execute(sql, (career_id, student_id))
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result['new_comment_count'])


@dec_timeit("update_service_score")
@dec_make_conn_cursor
def update_service_score(conn, cursor, service_id, star, suggest):
    """
    学生为学习建议打分
    :param conn:
    :param cursor:
    :param service_id:
    :param star:
    :param suggest:
    :return:
    """

    sql = """
        UPDATE mz_onevone_service SET star=%s, suggest=%s
        WHERE id=%s
    """
    try:
        cursor.execute(sql, (star, suggest, service_id))
        conn.commit()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_service_teacher")
@dec_make_conn_cursor
def get_service_teacher(conn, cursor, career_id):
    """
    获取老师列表
    :param conn:
    :param cursor:
    :param career_id:
    :return:
    """
    sql = """
    SELECT ct.teacher_id AS teacher_id,
           ct.qq AS qq,
           ct.qq_image_url AS qq_image_url,
           ct.qq_key AS qq_key,
           u.avatar_url AS avatar,
           u.real_name AS real_name,
           u.nick_name AS nick_name
     FROM mz_lps4_career_teacher AS ct
    INNER JOIN mz_user_userprofile AS u ON u.id=ct.teacher_id
    WHERE career_id=%s
    """
    try:
        cursor.execute(sql, (career_id,))
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_make_conn_cursor
def get_onevone_service_comment(conn, cursor, service_id, teacher_id):
    """
    获取service的commit
    :param conn:
    :param cursor:
    :param service_id:
    :param teacher_id:
    :return:
    """
    try:
        service_id = int(service_id)
        teacher_id = int(teacher_id)
    except Exception as e:
        log.warn(str(e))
        return APIResult(code=False)
    try:
        cursor.execute(
            """
SELECT 1
FROM mz_onevone_service_comment
WHERE service_id = %s AND user_id = %s;
            """ % (service_id, teacher_id)
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
def get_first_onevone_service_by_teacher_and_student(conn, cursor, teacher_id, user_id, source_type, career_id):
    """
    获取service的commit
    :param conn:
    :param cursor:
    :param teacher_id:
    :param user_id:
    :param source_type:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        user_id = int(user_id)
        source_type = int(source_type)
    except Exception as e:
        log.warn(str(e))
        return APIResult(code=False)
    try:
        cursor.execute(
            """
SELECT id
FROM mz_onevone_service
WHERE teacher_id = %s AND user_id = %s AND source_type = %s AND career_id=%s
ORDER BY id;
            """ % (teacher_id, user_id, source_type, career_id)
        )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=result)


@dec_timeit("get_teacher_info_by_lps4")
@dec_make_conn_cursor
def get_teacher_info_by_lps4(conn, cursor, career_id, student_id):
    """
    获取老师信息
    :param conn:
    :param cursor:
    :param career_id:
    :param student_id: 23811   684  2
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: get_teacher_info_by_lps4 : career_id must be int')
        return APIResult(code=False)
    if not isinstance(student_id, int):
        log.warn('type error: get_teacher_info_by_lps4 : student_id must be int')
        return APIResult(code=False)

    sql = """
        SELECT teacher.mobile, teacher.real_name, teacher.nick_name, teacher.id, teacher.avatar_url FROM mz_lps4_student
        INNER JOIN mz_user_userprofile AS teacher ON teacher.id=mz_lps4_student.teacher_id
        WHERE
        career_id=%s AND user_id=%s AND mz_lps4_student.type != 2
        """
    try:
        cursor.execute(sql, (career_id, student_id))
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)