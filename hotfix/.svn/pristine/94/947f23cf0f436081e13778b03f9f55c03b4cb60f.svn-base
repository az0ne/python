# -*- coding: utf-8 -*-
import os
import time
import django
from django.utils.html import strip_tags

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
django.setup()
from db.api.apiutils import APIResult, dec_make_conn_cursor
from utils.logger import logger as log


@dec_make_conn_cursor
def get_service(conn, cursor):
    sql = """
    SELECT *
    FROM mz_onevone_service
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


@dec_make_conn_cursor
def get_service_related(conn, cursor, service_id, student_id, teacher_id):
    sql_student_count = """
    SELECT COUNT(*) AS total_count
    FROM mz_onevone_service_comment WHERE service_id=%s AND user_id=%s
    """

    sql_teacher_count = """
    SELECT COUNT(*) AS total_count
    FROM mz_onevone_service_comment WHERE service_id=%s AND user_id=%s
    """

    sql_student_last = """
    SELECT create_date
    FROM mz_onevone_service_comment WHERE service_id=%s AND user_id=%s
    ORDER BY id DESC
    LIMIT 1
    """

    sql_teacher_last = """
    SELECT create_date
    FROM mz_onevone_service_comment WHERE service_id=%s AND user_id=%s
    ORDER BY id DESC
    LIMIT 1
    """

    sql_first = """
    SELECT nick_name, head, comment
    FROM mz_onevone_service_comment WHERE service_id=%s
    LIMIT 1
    """

    sql_last = """
    SELECT create_date
    FROM mz_onevone_service_comment WHERE service_id=%s
    ORDER BY id DESC
    LIMIT 1
    """

    try:
        cursor.execute(sql_student_count, (service_id, student_id))
        student_count = cursor.fetchone()
        cursor.execute(sql_teacher_count, (service_id, teacher_id))
        teacher_count = cursor.fetchone()
        cursor.execute(sql_student_last, (service_id, student_id))
        student_last = cursor.fetchone()
        cursor.execute(sql_teacher_last, (service_id, teacher_id))
        teacher_last = cursor.fetchone()
        cursor.execute(sql_first, (service_id,))
        first = cursor.fetchone()
        cursor.execute(sql_last, (service_id,))
        last = cursor.fetchone()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result={'student_count': student_count['total_count'], 'teacher_count': teacher_count['total_count'],
                             'student_last': student_last, 'teacher_last': teacher_last,
                             'first': first, 'last': last})


@dec_make_conn_cursor
def get_service_comment(conn, cursor, service_id):
    sql = """
    SELECT *
    FROM mz_onevone_service_comment
    WHERE service_id=%s
    """
    try:
        cursor.execute(sql, (service_id,))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_make_conn_cursor
def coach_insert(conn, cursor, career_id, student_id, teacher_id, nick_name, head, source_type, source, abstract,
                 student_comment_count, teacher_comment_count, create_date, last_comment_date, last_student_comment_date,
                 last_teacher_comment_date, teacher_replay_count, student_replay_count, source_location):
    sql_coach = """
    INSERT INTO mz_coach (career_id, student_id, teacher_id, nick_name, head, source_type, source, abstract,
    student_comment_count, teacher_comment_count, create_date, last_comment_date,last_student_comment_date, last_teacher_comment_date,
    teacher_replay_count,student_replay_count, source_location)
    VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    try:
        cursor.execute(sql_coach, (career_id, student_id, teacher_id, nick_name, head, source_type, source, abstract,
                                   student_comment_count, teacher_comment_count, create_date, last_comment_date,
                                   last_student_comment_date, last_teacher_comment_date, teacher_replay_count,
                                   student_replay_count, source_location))
        cursor.execute('SELECT LAST_INSERT_ID()')
        coach_id = cursor.fetchone()['LAST_INSERT_ID()']
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=coach_id)


@dec_make_conn_cursor
def comment_insert(conn, cursor, value_list):
    sql_comment = """
        INSERT INTO mz_coach_comment
        (coach_id, comment, user_type, user_id, nick_name, head, create_date)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """
    try:
        cursor.executemany(sql_comment, value_list)
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_make_conn_cursor
def teacher_message(conn, cursor):
    sql = """
    INSERT INTO mz_coach_message_teacher_count
    (career_id, user_id, teacher_id, total_count, new_coach_count, new_comment_count)
    SELECT
    career_id,
    user_id,
    teacher_id,
    total_count,
    new_service_count,
    new_comment_count
    FROM mz_onevone_service_message_teacher_count;
    """
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_make_conn_cursor
def student_message(conn, cursor):
    sql = """
    INSERT INTO mz_coach_message_user_count
    (career_id, user_id, new_coach_count, new_comment_count)
    SELECT
    career_id,
    user_id,
    SUM(new_service_count),
    SUM(new_comment_count)
    FROM mz_onevone_service_message_user_count
    GROUP BY career_id, user_id;
    """
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


def test():
    start = time.time()

    result = teacher_message()
    if result.is_error():
        print 'teacher_message error'
    result = student_message()
    if result.is_error():
        print 'student_message error'

    services = get_service()
    if services.is_error():
        print 'get_service error'
        return None
    for service in services.result():
        print service['id']
        result = get_service_related(service['id'], service['user_id'], service['teacher_id'])
        if result.is_error():
            print 'get_service_related error : service_id=%s' % service['id']
            continue
        service_related = result.result()
        student_last = None
        teacher_last = None
        if service_related['teacher_last']:
            teacher_last = service_related['teacher_last']['create_date']
        if service_related['student_last']:
            student_last = service_related['student_last']['create_date']
        source = None
        if service['source_type'] == 0:
            if service_related['first']['comment'].find('麻烦老师帮我制定下符合我个人情况的学习建议吧') != -1:
                source_type = 50
            else:
                source = service['source']
                source_type = 40
        else:
            source_type = 20
        abstract = strip_tags(service_related['first']['comment'])
        abstract = abstract.replace('&nbsp;', '')
        result = coach_insert(career_id=service['career_id'], student_id=service['user_id'],
                              teacher_id=service['teacher_id'], nick_name=service_related['first']['nick_name'],
                              head=service_related['first']['head'], source_type=source_type, source=source,
                              abstract=abstract, student_comment_count=service_related['student_count'],
                              teacher_comment_count=service_related['teacher_count'],
                              create_date=service['create_date'],
                              last_comment_date=service_related['last']['create_date'],
                              last_student_comment_date=student_last,
                              last_teacher_comment_date=teacher_last,
                              teacher_replay_count=service['teacher_unread'],
                              student_replay_count=service['student_unread'],
                              source_location=None)
        if result.is_error():
            print 'coach_insert error : service_id=%s' % service['id']
            continue

        coach_id = result.result()
        result = get_service_comment(service['id'])
        if result.is_error():
            print 'get_service_comment error : service_id=%s' % service['id']
            continue
        comments = result.result()
        comment_list = []
        for comment in comments:
            if comment['user_id'] == service['user_id']:
                user_type = 10
            else:
                user_type = 20
            comment_list.append((coach_id, comment['comment'], user_type, comment['user_id'], comment['nick_name'],
                                 comment['head'], comment['create_date']))
        if comment_list:
            result = comment_insert(value_list=comment_list)
            if result.is_error():
                print 'comment_insert error : coach_id=%s' % coach_id

    end = time.time()
    print end - start

if __name__ == '__main__':
    test()
    print 'end'
