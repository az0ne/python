# -*- coding: utf-8 -*-
import json
from datetime import datetime

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor
from utils.constants import CoachCommentUserType, CoachUserType


@dec_timeit("add_coach_comment")
@dec_make_conn_cursor
def get_coach(conn, cursor, coach_id, user_id, is_student):
    """
    coach详情
    :param conn:
    :param cursor:
    :param coach_id:
    :param user_id:
    :param is_student:
    :return:
    """
    sql = """
        SELECT *
        FROM mz_coach WHERE id = %s
    """

    # 未读数清除
    teacher_replay_count = """
        UPDATE mz_coach_message_teacher_count AS cmtc, mz_coach AS c
        SET
          cmtc.new_comment_count = cmtc.new_comment_count - c.teacher_replay_count,
          c.teacher_replay_count = 0
        WHERE cmtc.career_id = c.career_id AND cmtc.teacher_id = c.teacher_id AND cmtc.user_id=c.student_id
              AND c.id = %s;
    """
    student_replay_count = """
        UPDATE mz_coach_message_user_count AS cmuc, mz_coach AS c
        SET
          cmuc.new_comment_count = cmuc.new_comment_count - c.student_replay_count,
          c.student_replay_count = 0
        WHERE cmuc.career_id = c.career_id AND cmuc.user_id = c.student_id AND c.id = %s;
    """

    try:
        if is_student:
            cursor.execute(sql+' AND student_id=%s', (coach_id, user_id))
        else:
            cursor.execute(sql + ' AND teacher_id=%s', (coach_id, user_id))

        data = cursor.fetchone()

        if data:
            if is_student:
                cursor.execute(student_replay_count, (coach_id,))
            else:
                cursor.execute(teacher_replay_count, (coach_id,))

            source_location = data['source_location']
            if source_location:
                source_location = json.loads(source_location)
                data['source_location_lps'] = source_location.get(
                    'lps', [None, None, None])
                data['source_location_project'] = source_location.get('project')
            conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        conn.rollback()
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=data)


@dec_timeit("add_coach_comment")
@dec_make_conn_cursor
def add_coach_comment(conn, cursor, coach_id, comment, user_type, user_id,
                      nick_name, head, career_id, files_list=None):
    """
    新增辅导评论
    :param conn:
    :param cursor:
    :param coach_id:
    :param comment:
    :param user_type: 用户类型：10：学生; 20：老师
    :param user_id:
    :param nick_name:
    :param head:
    :param career_id:
    :param files_list: 项目制作下载地址
    :return: bool
    """

    sql = """
        INSERT INTO mz_coach_comment
          (coach_id, comment, user_type, user_id,
           nick_name, head, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    create_date = datetime.now()
    param = (coach_id, comment, user_type, user_id,
             nick_name, head, create_date)

    coach_user_sql = """
        SELECT student_id, teacher_id
        FROM mz_coach WHERE id = %s;
    """
    update_teacher_count = """
        INSERT INTO mz_coach_message_teacher_count
          (career_id, user_id, teacher_id, new_comment_count)
        VALUES (%s, %s, %s, 1) ON DUPLICATE KEY UPDATE
        new_comment_count = new_comment_count+1;
    """
    update_student_count = """
        INSERT INTO mz_coach_message_user_count
          (career_id, user_id, new_comment_count)
        VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE
        new_comment_count = new_comment_count+1;
    """
    update_coach_student = """
        UPDATE mz_coach
        SET student_comment_count = student_comment_count + 1,
            last_student_comment_date = '{0}',
            last_comment_date = '{0}',
            teacher_replay_count = teacher_replay_count + 1
        WHERE id = %s;
    """.format(datetime.now())
    update_coach_teacher = """
        UPDATE mz_coach
        SET teacher_comment_count = teacher_comment_count + 1,
            last_teacher_comment_date = '{0}',
            last_comment_date = '{0}',
            student_replay_count = student_replay_count + 1
        WHERE id = %s;
    """.format(datetime.now())
    sql_project = """
    INSERT INTO mz_coach_project(coach_comment_id, file_name, file_type, file_url) values (%s,%s,%s,%s)
    """
    if user_type not in CoachCommentUserType.mapper.keys():
        log.warn('user_type failed.')
        return APIResult(code=False, result=False)

    try:
        cursor.execute(coach_user_sql, (coach_id,))
        coach_user = cursor.fetchone()
        comment_id = 0
        if coach_user and user_id in coach_user.values():
            cursor.execute(sql, param)
            cursor.execute('SELECT LAST_INSERT_ID()')
            comment_id = cursor.fetchone()['LAST_INSERT_ID()']
            if files_list:
                for x in files_list:
                    cursor.execute(sql_project, (comment_id, x['file_name'], x['file_type'],
                                                 x['file_url']))
            if user_type == CoachCommentUserType.STUDENT:
                cursor.execute(
                    update_teacher_count,
                    (career_id, user_id, coach_user.get('teacher_id'))
                )
                cursor.execute(update_coach_student, (coach_id,))
            else:
                cursor.execute(
                    update_student_count,
                    (career_id, coach_user.get('student_id'))
                )

                cursor.execute(update_coach_teacher, (coach_id,))
            conn.commit()

        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        conn.rollback()
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=comment_id)


@dec_timeit("get_coach_comments")
@dec_make_conn_cursor
def get_coach_comments(conn, cursor, coach_id, start_index=None, end_index=None):
    """
    获取辅导评论列表
    :param conn:
    :param cursor:
    :param coach_id:
    :return:
    """

    sql = """
        SELECT
          id,
          coach_id,
          comment,
          user_type,
          user_id,
          nick_name,
          head,
          create_date
        FROM mz_coach_comment
        WHERE coach_id = %s
        ORDER BY create_date
    """
    sql_page = sql+""" LIMIT %s,%s"""
    try:
        if start_index and end_index:
            cursor.execute(sql_page, (coach_id, start_index, end_index))
        else:
            cursor.execute(sql, (coach_id,))
        data = cursor.fetchall()

        for d in data:
            d['user_type_name'] = \
                CoachCommentUserType.mapper.get(d['user_type'])

        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=data)


@dec_timeit("get_message_user_count")
@dec_make_conn_cursor
def get_message_user_count(conn, cursor, career_id, user_id):
    """
    获取用户辅导未读未回复数等
    :param conn:
    :param cursor:
    :param career_id:
    :param user_id:
    :return:
    """

    sql = """
        SELECT
          new_coach_count,
          new_comment_count
        FROM mz_coach_message_user_count
        WHERE career_id = %s AND user_id = %s;
    """

    try:
        cursor.execute(sql, (career_id, user_id))
        data = cursor.fetchone()

        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=data)


@dec_timeit("get_message_teacher_count")
@dec_make_conn_cursor
def get_message_teacher_count(conn, cursor, career_id, user_id, teacher_id):
    """
    获取老师辅导未读未回复数等
    :param conn:
    :param cursor:
    :param career_id:
    :param user_id:
    :param teacher_id:
    :return:
    """

    sql = """
        SELECT
          total_count,
          new_coach_count,
          new_comment_count
        FROM mz_coach_message_teacher_count
        WHERE career_id = %s AND user_id = %s AND teacher_id = %s;
    """

    try:
        cursor.execute(sql, (career_id, user_id, teacher_id))
        data = cursor.fetchone()

        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=data)


@dec_timeit("create_new_coach")
@dec_make_conn_cursor
def create_new_coach(conn, cursor, **kwargs):
    """
    新建学习辅导
    :param conn:
    :param cursor:
    :param kwargs:
    :return:
    """
    sql_coach = """
        INSERT INTO mz_coach (career_id, student_id, teacher_id, nick_name, head, source_type, source, abstract,
        student_comment_count, teacher_comment_count, create_date, last_comment_date,last_student_comment_date, last_teacher_comment_date,
        teacher_replay_count,student_replay_count, source_location)
        VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

    sql_comment = """
        INSERT INTO mz_coach_comment
        (coach_id, comment, user_type, user_id, nick_name, head, create_date)
        VALUE
        (%s,%s,%s,%s,%s,%s,%s)
        """

    sql_user = """
    INSERT INTO mz_coach_message_user_count (career_id, user_id, new_coach_count, new_comment_count)
    VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
    new_coach_count=new_coach_count+1,new_comment_count=new_comment_count+1
    """

    sql_teacher_insert = """
    INSERT INTO mz_coach_message_teacher_count
    (career_id, user_id, teacher_id, total_count, new_coach_count, new_comment_count)
    VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
    total_count=total_count+1,new_comment_count=new_comment_count+1,new_coach_count=new_coach_count+1
    """

    sql_teacher_update = """
    INSERT INTO mz_coach_message_teacher_count
    (career_id, user_id, teacher_id, total_count, new_coach_count, new_comment_count)
    VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
    total_count=total_count+1
    """

    sql_project = """
    INSERT INTO mz_coach_project(coach_comment_id, file_name, file_type, file_url) values (%s,%s,%s,%s)
    """
    try:
        if kwargs['is_student']:
            user_type = 10
            student_comment_count = 1
            teacher_comment_count = 0
            student_replay_count = 0
            teacher_replay_count = 1
            last_student_comment_date = kwargs['now']
            last_teacher_comment_date = None
        else:
            user_type = 20
            student_comment_count = 0
            teacher_comment_count = 1
            student_replay_count = 1
            teacher_replay_count = 0
            last_student_comment_date = None
            last_teacher_comment_date = kwargs['now']

        cursor.execute(sql_coach, (kwargs['career_id'], kwargs['student_id'], kwargs['teacher_id'],
                                   kwargs['nick_name'], kwargs['head'], kwargs['source_type'],
                                   kwargs['source'], kwargs['abstract'],
                                   student_comment_count, teacher_comment_count,
                                   kwargs['now'], kwargs['now'], last_student_comment_date, last_teacher_comment_date,
                                   teacher_replay_count, student_replay_count, kwargs['source_location']))

        cursor.execute('SELECT LAST_INSERT_ID()')
        coach_id = cursor.fetchone()
        cursor.execute(sql_comment, (coach_id['LAST_INSERT_ID()'], kwargs['comment'], user_type,
                                     kwargs['user_id'], kwargs['nick_name'], kwargs['head'], kwargs['now'],
                                     ))
        if kwargs['files_list']:
            cursor.execute('SELECT LAST_INSERT_ID()')
            comment_id = cursor.fetchone()
            for x in kwargs['files_list']:
                cursor.execute(sql_project, (comment_id['LAST_INSERT_ID()'], x['file_name'], x['file_type'],
                                             x['file_url']))
        if kwargs['is_student']:
            # 记录老师数目
            cursor.execute(sql_teacher_insert, (kwargs['career_id'], kwargs['student_id'],
                                                kwargs['teacher_id'], 1, 1, 1))
        else:
            # 记录老师数目
            cursor.execute(sql_teacher_update, (kwargs['career_id'], kwargs['student_id'],
                                                kwargs['teacher_id'], 1, 0, 0))
            # 记录学生数目
            cursor.execute(sql_user, (kwargs['career_id'], kwargs['student_id'], 1, 1))

        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=coach_id['LAST_INSERT_ID()'])


@dec_timeit("student_coach_list")
@dec_make_conn_cursor
def student_coach_list(conn, cursor, career_id, student_id, start_index, end_index):
    """
    学生辅导列表
    :param conn:
    :param cursor:
    :param start_index:
    :param end_index:
    :param career_id: 职业课程ID
    :param student_id: 学生ID
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: student_service_count : career_id must be int')
        return APIResult(code=False)
    if not isinstance(student_id, int):
        log.warn('type error: student_service_count : student_id must be int')
        return APIResult(code=False)
    if not isinstance(start_index, int):
        log.warn('type error: student_service_count : start_index must be int')
        return APIResult(code=False)
    if not isinstance(end_index, int):
        log.warn('type error: student_service_count : end_index must be int')
        return APIResult(code=False)

    sql = """
        SELECT id,
               student_replay_count,
               source_location,
               abstract,
               source,
               create_date,
               source_type,
               nick_name,
               head,
               student_replay_count
        FROM mz_coach AS coach
        WHERE career_id=%s AND student_id=%s
        ORDER BY create_date DESC
        LIMIT %s,%s
        """
    try:
        cursor.execute(sql, (career_id, student_id, start_index, end_index))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("teacher_coach_list")
@dec_make_conn_cursor
def teacher_coach_list(conn, cursor, career_id, student_id, teacher_id, start_index, end_index, order_by):
    """
    老师辅导列表
    :param conn:
    :param cursor:
    :param start_index:
    :param end_index:
    :param career_id: 职业课程ID
    :param student_id: 学生ID
    :param teacher_id: 老师ID
    :param order_by: 排序方式 'all':全部 'todo': 未解决 'done': 已解决
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

    sql_all = """
        SELECT id,
               teacher_replay_count,
               source_location,
               abstract,
               source,
               create_date,
               source_type,
               nick_name,
               head
        FROM mz_coach
        WHERE career_id=%s AND student_id=%s AND teacher_id=%s
        ORDER BY create_date DESC
        LIMIT %s,%s
        """

    sql_todo = """
    SELECT id,
       teacher_replay_count,
       source_location,
       abstract,
       source,
       create_date,
       source_type,
       nick_name,
       head
    FROM mz_coach
    WHERE
      career_id = %s
      AND student_id = %s
      AND teacher_id = %s
      AND IFNULL(last_student_comment_date, '2001-11-11 11:11:11') > IFNULL(last_teacher_comment_date, '2001-11-11 11:11:11')
    LIMIT %s,%s
    """

    sql_done = """
    SELECT id,
       teacher_replay_count,
       source_location,
       abstract,
       source,
       create_date,
       source_type,
       nick_name,
       head
    FROM mz_coach
    WHERE
      career_id = %s
      AND student_id = %s
      AND teacher_id = %s
      AND IFNULL(last_student_comment_date, '2001-11-11 11:11:11') < IFNULL(last_teacher_comment_date, '2001-11-11 11:11:11')
    LIMIT %s,%s
    """
    try:
        if order_by == 'todo':
            sql = sql_todo
        elif order_by == 'done':
            sql = sql_done
        else:
            sql = sql_all
        cursor.execute(sql, (career_id, student_id, teacher_id, start_index, end_index))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("student_coach_count")
@dec_make_conn_cursor
def student_coach_count(conn, cursor, career_id, student_id):
    """
    学生辅导总数
    :param conn:
    :param cursor:
    :param career_id:
    :param student_id:
    :return:
    """
    if not isinstance(career_id, int):
        log.warn('type error: student_service_count : career_id must be int')
        return APIResult(code=False)
    if not isinstance(student_id, int):
        log.warn('type error: student_service_count : student_id must be int')
        return APIResult(code=False)

    sql = """
        SELECT COUNT(*) AS total_count FROM mz_coach WHERE
        career_id=%s AND student_id=%s
    """

    try:
        cursor.execute(sql, (career_id, student_id))
        count = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=count)


@dec_timeit("teacher_coach_count")
@dec_make_conn_cursor
def teacher_coach_count(conn, cursor, career_id, student_id, teacher_id, order_by):
    """
    老师辅导总数
    :param conn:
    :param cursor:
    :param career_id:
    :param student_id:
    :param teacher_id:
    :param order_by: 排序方式 'all':全部 'todo': 未解决 'done': 已解决
    :return:
    """
    sql_all = """
        SELECT COUNT(*) AS total_count
        FROM mz_coach
        WHERE career_id=%s AND student_id=%s AND teacher_id=%s
        """

    sql_todo = """
        SELECT COUNT(*) AS total_count
        FROM mz_coach
        WHERE
          career_id = %s
        AND student_id = %s
        AND teacher_id = %s
        AND IFNULL(last_student_comment_date, '2001-11-11 11:11:11') > IFNULL(last_teacher_comment_date, '2001-11-11 11:11:11')
    """

    sql_done = """
        SELECT COUNT(*) AS total_count
        FROM mz_coach
        WHERE
          career_id = %s
        AND student_id = %s
        AND teacher_id = %s
        AND IFNULL(last_student_comment_date, '2001-11-11 11:11:11') < IFNULL(last_teacher_comment_date, '2001-11-11 11:11:11')
    """
    try:
        if order_by == 'todo':
            sql = sql_todo
        elif order_by == 'done':
            sql = sql_done
        else:
            sql = sql_all
        cursor.execute(sql, (career_id, student_id, teacher_id))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("clean_new_coach_count")
@dec_make_conn_cursor
def clean_new_coach_count(conn, cursor, career_id, user_id, teacher_id):
    """
    进入列表清除新服务数
    :param conn:
    :param cursor:
    :param career_id:
    :param user_id:
    :param teacher_id:
    :return:
    """
    sql_teacher = """
    UPDATE mz_coach_message_teacher_count SET new_coach_count=0 WHERE
    career_id=%s AND user_id=%s AND teacher_id=%s
    """

    sql_student = """
    UPDATE mz_coach_message_user_count SET new_coach_count=0 WHERE
    career_id=%s AND user_id=%s
    """
    try:
        if teacher_id:
            cursor.execute(sql_teacher, (career_id, user_id, teacher_id))
        else:
            cursor.execute(sql_student, (career_id, user_id))
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_project_coach")
@dec_make_conn_cursor
def get_project_coach(conn, cursor, career_id, student_id, teacher_id, source_location, is_student, is_clean=True):
    """
    获取项目制作辅导
    :param conn:
    :param cursor:
    :param career_id:
    :param teacher_id:
    :param student_id:
    :param source_location:
    :param is_student:
    :param is_clean: 是否需要清零未读
    :return:
    """
    sql = """
        SELECT * FROM mz_coach WHERE career_id=%s AND student_id=%s AND teacher_id=%s
        AND mz_coach.source_location=%s
        AND mz_coach.source_type=30
        """
    # 未读数清除
    teacher_replay_count = """
        UPDATE mz_coach_message_teacher_count AS cmtc, mz_coach AS c
        SET
          cmtc.new_comment_count = cmtc.new_comment_count - c.teacher_replay_count,
          c.teacher_replay_count = 0
        WHERE cmtc.career_id = c.career_id AND cmtc.teacher_id = c.teacher_id AND cmtc.user_id=c.student_id
              AND c.id = %s;
    """
    student_replay_count = """
        UPDATE mz_coach_message_user_count AS cmuc, mz_coach AS c
        SET
          cmuc.new_comment_count = cmuc.new_comment_count - c.student_replay_count,
          c.student_replay_count = 0
        WHERE cmuc.career_id = c.career_id AND cmuc.user_id = c.student_id AND c.id = %s;
    """
    try:
        cursor.execute(sql, (career_id, student_id, teacher_id, source_location))
        data = cursor.fetchone()
        if data and is_clean:
            coach_id = data['id']
            if is_student:
                cursor.execute(student_replay_count, (coach_id,))
            else:
                cursor.execute(teacher_replay_count, (coach_id,))
            conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_project_coach_comment")
@dec_make_conn_cursor
def get_project_coach_comment(conn, cursor, coach_id):
    """
    获取项目制作辅导回复列表
    :param conn:
    :param cursor:
    :param coach_id:
    :return:
    """
    sql = """
    SELECT * FROM mz_coach_comment
    LEFT JOIN mz_coach_project ON mz_coach_project.coach_comment_id = mz_coach_comment.id
    WHERE coach_id=%s
    ORDER BY mz_coach_comment.id
    """
    try:
        cursor.execute(sql, (coach_id,))
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_last_coach_comment")
@dec_make_conn_cursor
def get_last_coach_comment(conn, cursor, coach_id):
    """

    :param conn:
    :param cursor:
    :param coach_id:
    :return:
    """
    sql = """
        SELECT
          id,
          nick_name,
          head,
          create_date
        FROM mz_coach_comment
        WHERE coach_id = %s
        ORDER BY -create_date LIMIT 1;
    """

    count_sql = """
        SELECT
          count(id) AS comment_count
        FROM mz_coach_comment
        WHERE coach_id = %s
    """

    try:
        cursor.execute(count_sql, (coach_id,))
        if cursor.fetchone()['comment_count'] > 1:
            cursor.execute(sql, (coach_id,))
            data = cursor.fetchone()
        else:
            data = {}
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_make_conn_cursor
def get_coach_task_lib_info(conn, cursor, career_id, task_id):
    """
    获取老师辅导信息库
    :param conn:
    :param cursor:
    :param career_id:
    :param task_id:
    :return:
    """
    sql = """
        SELECT * FROM mz_coach_task_lib
        where career_id=%s and task_id=%s
    """
    try:
        cursor.execute(sql, (career_id, task_id))
        data = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_coach_data")
@dec_make_conn_cursor
def get_coach_data(conn, cursor, coach_id):
    """
    获取项目数据
    :param conn:
    :param cursor:
    :param coach_id:
    :return:
    """
    sql = """
        SELECT *
        FROM mz_coach WHERE id = %s
    """
    try:
        cursor.execute(sql, (coach_id,))
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
