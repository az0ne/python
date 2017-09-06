# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_career_course(conn, cursor, name, index):
    sql = """
            INSERT INTO mz_wechat_career_course (`name`, `index`) VALUES (%s, %s)
          """
    try:
        cursor.execute(sql, (name, index,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_course(conn, cursor, dict_info):
    sql = """
            INSERT INTO mz_wechat_course (`name`, image_url, description, is_active, date_publish, student_count,
            `index`,teacher_id, career_course_id,price,web_career_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
          """
    try:
        cursor.execute(sql,
                       (dict_info['name'], dict_info['image_url'], dict_info['description'], dict_info['is_active'],
                        dict_info['date_publish'], dict_info['student_count'], dict_info['index'],
                        dict_info['teacher_id'],
                        dict_info['career_course_id'], dict_info['price'], dict_info['web_career_id']))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_lesson(conn, cursor, dict_info):
    sql = """
            INSERT INTO mz_wechat_lesson (`name`,video_url,video_length,`index`,need_pay,course_id )
            VALUES (%s,%s,%s,%s,%s,%s)
          """
    try:
        cursor.execute(sql, (dict_info['name'], dict_info['video_url'], dict_info['video_length'], dict_info['index'],
                             dict_info['need_pay'], dict_info['course_id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wechat_career_course(conn, cursor, name, index, _id):
    sql = """
            UPDATE mz_wechat_career_course SET `name`=%s, `index`=%s
            WHERE id=%s
          """
    try:
        cursor.execute(sql, (name, index, _id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wechat_course(conn, cursor, dict_info):
    sql = """
            UPDATE mz_wechat_course SET `name`=%s, image_url=%s, description=%s, is_active=%s, date_publish=%s, student_count=%s,
            `index`=%s,teacher_id=%s, career_course_id=%s,price=%s,web_career_id=%s
            WHERE id=%s
          """
    try:
        cursor.execute(sql,
                       (dict_info['name'], dict_info['image_url'], dict_info['description'], dict_info['is_active'],
                        dict_info['date_publish'], dict_info['student_count'], dict_info['index'],
                        dict_info['teacher_id'],
                        dict_info['career_course_id'], dict_info['price'], dict_info['web_career_id'], dict_info['id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wechat_lesson(conn, cursor, dict_info):
    sql = """
            UPDATE mz_wechat_lesson SET `name`=%s,video_url=%s,video_length=%s,`index`=%s,need_pay=%s,course_id=%s
            WHERE id=%s
          """
    try:
        cursor.execute(sql, (dict_info['name'], dict_info['video_url'], dict_info['video_length'], dict_info['index'],
                             dict_info['need_pay'], dict_info['course_id'], dict_info['id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_all_course(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT career.name as career_name, course.name as course_name,image_url, course.description as course_description, course.is_active as course_is_active,
            date_publish, course.student_count as course_student_count, career.index as career_id,course.index as course_index,teacher_id,
            career_course_id,price,web_career_id, userprofile.nick_name,careercourse.name as web_career_name, course.id as course_id
            FROM mz_wechat_career_course as career
            RIGHT JOIN mz_wechat_course as course
            ON course.career_course_id=career.id
            LEFT JOIN mz_user_userprofile as userprofile
            ON course.teacher_id=userprofile.id
            LEFT JOIN mz_course_careercourse as careercourse
            ON careercourse.id = course.web_career_id
            ORDER BY career_name DESC, course_index ASC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (start_index, page_size,))
        wechat_courses = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_course
            """, )
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechart_courses_dict = {
        "result": wechat_courses,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechart_courses_dict)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_all_course_by_search(conn, cursor, page_index, page_size, career_course_id):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT career.name as career_name, course.name as course_name,image_url, course.description as course_description, course.is_active as course_is_active,
            date_publish, course.student_count as course_student_count, career.index as career_id,course.index as course_index,teacher_id,
            career_course_id,price,web_career_id, userprofile.nick_name,careercourse.name as web_career_name, course.id as course_id
            FROM mz_wechat_career_course as career
            RIGHT JOIN mz_wechat_course as course
            ON course.career_course_id=career.id
            LEFT JOIN mz_user_userprofile as userprofile
            ON course.teacher_id=userprofile.id
            LEFT JOIN mz_course_careercourse as careercourse
            ON careercourse.id = course.web_career_id
            WHERE career.id=%s
            ORDER BY career_name DESC, course_index ASC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (career_course_id, start_index, page_size,))
        wechat_courses = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_course as course
                LEFT JOIN mz_wechat_career_course as career
                ON course.career_course_id=career.id
                WHERE career.id=%s
            """, (career_course_id,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechart_courses_dict = {
        "result": wechat_courses,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechart_courses_dict)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_all_lesson(conn, cursor, page_index, page_size, course_id):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT lesson.name as name,video_url,video_length,lesson.`index` as lesson_index,
            need_pay,course_id,play_count,course.name as course_name, lesson.id as lesson_id
            FROM mz_wechat_lesson as lesson
            LEFT JOIN  mz_wechat_course as course
            ON lesson.course_id=course.id
            WHERE lesson.course_id=%s
            limit %s, %s
         """
    try:
        cursor.execute(sql, (course_id, start_index, page_size,))
        wechat_lessons = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_lesson
                WHERE course_id=%s
            """, (course_id,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechart_lesson_dict = {
        "result": wechat_lessons,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechart_lesson_dict)


@dec_timeit
@dec_make_conn_cursor
def list_all_wechat_career_coures(conn, cursor):
    sql = """
            SELECT id, `name`, `index`
            FROM mz_wechat_career_course
         """
    try:
        cursor.execute(sql)
        wechat_courses = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=wechat_courses)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_course_by_id(conn, cursor, course_id):
    sql = """
            SELECT career.name as career_name, course.name as course_name,image_url, description, is_active,
            date_publish, student_count, career.index as career_id,course.index as course_index,teacher_id,
            career_course_id,price,web_career_id, career.id as career_id, course.id as course_id
            FROM mz_wechat_career_course as career
            RIGHT JOIN mz_wechat_course as course
            ON course.career_course_id=career.id
            WHERE course.id=%s
         """
    try:
        cursor.execute(sql, (course_id,))
        wechat_course = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=wechat_course)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_lesson_by_id(conn, cursor, lesson_id):
    sql = """
            SELECT lesson.name as lesson_name,video_url,video_length,lesson.index as lesson_index,
            need_pay,course_id,course.name as course_name, play_count
            FROM mz_wechat_lesson as lesson
            LEFT JOIN mz_wechat_course as course
            ON lesson.course_id = course.id
            WHERE lesson.id=%s
         """
    try:
        cursor.execute(sql, (lesson_id,))
        wechat_lesson = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=wechat_lesson)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_career_by_id(conn, cursor, career_id):
    sql = """
            SELECT `name`, `index`
            FROM mz_wechat_career_course
            WHERE id=%s
         """
    try:
        cursor.execute(sql, (career_id,))
        wechat_career = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=wechat_career)


@dec_timeit
@dec_make_conn_cursor
def del_wechat_lesson_by_id(conn, cursor, lesson_id):
    sql = """
            DELETE FROM mz_wechat_lesson
            WHERE id=%s
         """
    try:
        cursor.execute(sql, (lesson_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def del_wechat_course_by_id(conn, cursor, course_id):
    sql = """
            DELETE FROM mz_wechat_course
            WHERE id=%s
         """
    sql2 = """
                DELETE FROM mz_wechat_lesson
                WHERE course_id=%s
             """
    try:
        cursor.execute(sql, (course_id,))
        cursor.execute(sql2, (course_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
