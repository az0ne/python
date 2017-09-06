# -*- coding:utf-8 -*-
__author__ = 'qlp'
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from db.api.apiutils import APIResult
from utils.logger import logger as log

# 3.1学员列表
@dec_timeit
@dec_make_conn_cursor
def student_list_data(conn, cursor, page_index, page_size):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT lps4st.id,career.name,userpro.username,userpro.nick_name,lps4st.start_time,lps4st.end_time,
            lps4st.type,teacher.nick_name AS thname,lps4st.stop_start_time,lps4st.stop_end_time,lps4st.is_stop
            FROM mz_lps4_student AS lps4st
            LEFT JOIN mz_user_userprofile AS userpro ON lps4st.user_id = userpro.id
            LEFT JOIN mz_lps4_career AS career ON lps4st.career_id = career.id
            LEFT JOIN mz_user_userprofile AS teacher ON teacher.id = lps4st.teacher_id
            ORDER BY lps4st.id DESC limit %s,%s;
            """
        , (start_index, page_size))
        studentlist = cursor.fetchall()
        cursor.execute(
            """
            SELECT count(*) AS count FROM mz_lps4_student;
            """
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    student = {"result": studentlist,
               "rows_count": rows_count["count"],
               "page_count": page_count,
               }
    return APIResult(result=student)

# 3.1学员列表（条件搜索）
@dec_timeit
@dec_make_conn_cursor
def search_student_data(conn, cursor, page_index, page_size, careername,username):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT lps4st.id,career.name,userpro.username,userpro.nick_name,lps4st.start_time,lps4st.end_time,
            lps4st.type,teacher.nick_name AS thname,lps4st.stop_start_time,lps4st.stop_end_time,lps4st.is_stop
            FROM mz_lps4_student AS lps4st
            LEFT JOIN mz_user_userprofile AS userpro ON lps4st.user_id = userpro.id
            LEFT JOIN mz_user_userprofile AS teacher ON teacher.id = lps4st.teacher_id
            INNER JOIN mz_lps4_career AS career ON lps4st.career_id = career.id
            AND (((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s)
            OR ((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s)
            OR ((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s))
            ORDER BY lps4st.id DESC limit %s,%s;
            """
        , (username, username, username, careername, username, username, username, careername, username, username, username, careername, start_index, page_size))
        studentlist = cursor.fetchall()
        cursor.execute(
            """
            SELECT count(lps4st.id) AS count FROM mz_lps4_student AS lps4st
            INNER JOIN mz_user_userprofile AS userpro ON lps4st.user_id = userpro.id
            INNER JOIN mz_lps4_career AS career ON lps4st.career_id = career.id
            AND (((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s)
            OR ((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s)
            OR ((userpro.email LIKE %s OR userpro.mobile LIKE %s OR userpro.nick_name LIKE %s) AND career.name LIKE %s));
            """
        , (username, username, username, careername, username, username, username, careername, username, username, username, careername))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    student = {"result": studentlist,
               "rows_count": rows_count["count"],
               "page_count": page_count,
               }
    return APIResult(result=student)

# 3.1学员详情
@dec_timeit
@dec_make_conn_cursor
def student_revise(conn, cursor, id):
    try:
        cursor.execute(
            """
            SELECT lps4st.id,career.name,userpro.username,userpro.nick_name,lps4st.start_time,lps4st.end_time,
            lps4st.type,teach.username AS teachername,lps4st.career_id,lps4st.stop_start_time,lps4st.stop_end_time,lps4st.is_stop
            FROM mz_lps4_student AS lps4st
            INNER JOIN mz_user_userprofile AS userpro ON lps4st.user_id = userpro.id AND lps4st.id = %s
            LEFT JOIN mz_lps4_career AS career ON lps4st.career_id = career.id
            LEFT JOIN mz_user_userprofile AS teach ON teach.id = lps4st.teacher_id;
            """
        , (id,))
        reviselist = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    revisedata = {
        "result": reviselist
    }
    return APIResult(result=revisedata)

# 更新3.1学员数据
@dec_timeit
@dec_make_conn_cursor
def up_student(conn, cursor, id, teacherid, start_time, end_time, type, stop_start_time, stop_end_time, is_stop):
    try:
        cursor.execute(
            """
            UPDATE mz_lps4_student
            SET teacher_id = %s,start_time = %s,end_time = %s,type = %s,stop_start_time = %s, stop_end_time = %s, is_stop = %s
            WHERE  id = %s;
            """
        , (teacherid, start_time, end_time, type, stop_start_time, stop_end_time, is_stop, id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

# 查询职业课程列表
@dec_timeit
@dec_make_conn_cursor
def career_list(conn, cursor):
    try:
        cursor.execute(
            """
            SELECT id,name FROM mz_lps4_career WHERE type = "CAREER";
            """
        )
        careerdata = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    careerdata = {
        "result": careerdata
    }
    return APIResult(result=careerdata)

# 插入3.1学员信息
@dec_timeit
@dec_make_conn_cursor
def insert_student(conn, cursor, user_id, start_time, end_time, type, career_id, teacher_id):
    try:
        cursor.execute(
            """
            INSERT INTO mz_lps4_student(user_id,start_time,end_time,type,career_id,teacher_id)
            VALUES(%s,%s,%s,%s,%s,%s)
            """
        , (user_id, start_time, end_time, type, career_id, teacher_id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

# 查询专业可预约次数
@dec_timeit
@dec_make_conn_cursor
def select_career_count(conn, cursor, career_id):
    try:
        cursor.execute(
            """
            SELECT count FROM  mz_onevone_meeting_count WHERE career_id = %s;
            """
        , (career_id,))
        career_count = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    car_count = {
        "result": career_count
    }
    return APIResult(result=car_count)

# 插入1v1直播次数
@dec_timeit
@dec_make_conn_cursor
def insert_onevone_count(conn, cursor, career_id, user_id, max_count):
    try:
        cursor.execute(
            """
            INSERT INTO mz_onevone_meeting_user_count(career_id,user_id,max_count)
            VALUES(%s,%s,%s)
            """
        , (career_id, user_id, max_count))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

# 检测用户账号是否存在
@dec_timeit
@dec_make_conn_cursor
def query_exits(conn, cursor, name):
    try:
        cursor.execute(
            """
            SELECT count(*) AS count,id FROM mz_user_userprofile WHERE  email = %s OR mobile = %s;
            """
        , (name, name))
        datacount = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=datacount)

# 检测某用户在某专业下是否有数据
@dec_timeit
@dec_make_conn_cursor
def judeg_student(conn, cursor, career_id, user_id):
    try:
        cursor.execute(
            """
            SELECT user_id,career_id FROM  mz_lps4_student WHERE career_id = %s AND  user_id = %s;
            """
        , (career_id, user_id))
        judeg_data = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=judeg_data)

# 检测某专业下某学员是否已写入1v1次数
@dec_timeit
@dec_make_conn_cursor
def onevone_count(conn, cursor, career_id, user_id):
    try:
        cursor.execute(
            """
            SELECT count(*) AS count FROM  mz_onevone_meeting_user_count WHERE career_id = %s AND  user_id = %s;
            """
        , (career_id, user_id))
        onevone_data = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=onevone_data)

# 删除lps4学员
@dec_timeit
@dec_make_conn_cursor
def delstudent(conn, cursor, id, careerid, userid):
    try:
        cursor.execute(
            """
            DELETE FROM mz_lps4_student WHERE id = %s;
            """
        , (id,))
        conn.commit()
        cursor.execute(
            """
            DELETE FROM mz_onevone_meeting_user_count WHERE career_id = %s AND user_id = %s;
            """
        , (careerid, userid))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

# 通过student表获取lps4学员id和专业id
@dec_timeit
@dec_make_conn_cursor
def student_id_career_id(conn, cursor, id):
    try:
        cursor.execute(
            """
            SELECT career_id,user_id FROM mz_lps4_student WHERE id = %s;
            """
        ,(id,))
        iddata = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception :%s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=iddata)

# 获取学员账号信息和专业信息
@dec_timeit
@dec_make_conn_cursor
def student_career_date(conn, cursor, id):
    try:
        cursor.execute(
            """
            SELECT lps4st.id,lps4st.career_id,userpro.username FROM mz_lps4_student AS lps4st
            INNER JOIN mz_user_userprofile AS userpro ON lps4st.user_id = userpro.id AND lps4st.id = %s;
            """
        ,(id,))
        studentcareerdate = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception :%s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=studentcareerdate)

# 修改学员专业信息
@dec_timeit
@dec_make_conn_cursor
def up_student_career(conn, cursor, id, careerid):
    try:
        cursor.execute(
            """
            UPDATE mz_lps4_student SET career_id = %s WHERE id = %s;
            """
        , (careerid, id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception :%s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

