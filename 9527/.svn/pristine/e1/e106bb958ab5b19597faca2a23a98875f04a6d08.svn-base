# -*- coding:utf-8 -*-
__author__ = 'qlp'
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from db.api.apiutils import APIResult
from utils.logger import logger as log

@dec_timeit
@dec_make_conn_cursor
def searchclass(conn, cursor, codition):
    try:
        cursor.execute(
            """
            SELECT class.id,class.coding,userpro.nick_name,class.career_course_id,userpro.id as userid,carrcourse.name FROM mz_lps_class AS class
            INNER JOIN mz_lps_classstudents AS classstu ON class.id = classstu.student_class_id AND class.class_type=0
            INNER JOIN mz_user_userprofile AS userpro ON classstu.user_id = userpro.id AND (userpro.mobile = %s OR userpro.email = %s)
            INNER JOIN mz_course_careercourse AS carrcourse ON class.career_course_id = carrcourse.id;
            """
        , (codition, codition))
        search_data = cursor.fetchall()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    searchdata = {
        "result": search_data
    }
    return APIResult(result=searchdata)


@dec_timeit
@dec_make_conn_cursor
def stagelist(conn, cursor, carrcourseid, userid):
    try:
        cursor.execute(
            """
            SELECT id,name FROM mz_course_stage WHERE career_course_id = %s AND lps_version = 3.0;
            """
        , (carrcourseid,))
        stage_data = cursor.fetchall()
        cursor.execute(
            """
            SELECT nick_name,id FROM mz_user_userprofile WHERE id = %s;
            """
        , (userid,))
        name_data = cursor.fetchone()
    #     cursor.execute(
    #         """
    #         SELECT stage_id FROM mz_user_userunlockstage WHERE user_id = %s;
    #         """
    #     , (userid,))
    #     stage_old = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    stagedata = {
        "result": stage_data,
        "name_data": name_data,
        # "stageold": stage_old,
    }
    return APIResult(result=stagedata)

@dec_timeit
@dec_make_conn_cursor
def selestage(conn, cursor, stageuserid, stagecarid):
    try:
        cursor.execute(
            """
            SELECT userstage.stage_id FROM mz_user_userunlockstage AS userstage
            INNER JOIN mz_course_stage AS stage ON userstage.stage_id = stage.id AND userstage.user_id = %s AND stage.career_course_id = %s AND stage.lps_version = 3.0;
            """
        ,(stageuserid,stagecarid))
        stage_exit = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    stageexit = {
        "stageexit": stage_exit
    }
    return APIResult(result=stageexit)

@dec_timeit
@dec_make_conn_cursor
def insertstage(conn, cursor, stagedata, stageuserid):
    try:
        cursor.execute(
            """
            INSERT INTO mz_user_userunlockstage(date_unlock,stage_id,user_id) VALUES(NOW(),%s,%s);
            """
        , (stagedata, stageuserid))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def delestage(conn, cursor, stagedata, stageuserid):
    try:
        cursor.execute(
            """
            DELETE FROM mz_user_userunlockstage WHERE stage_id =%s  AND user_id = %s;
            """
        , (stagedata, stageuserid))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def seledeadline(conn,cursor,studentclass,userid):
    try:
        cursor.execute(
            """
            SELECT us.nick_name,cl.coding,clst.student_class_id,clst.user_id,clst.deadline,clst.status FROM mz_lps_classstudents AS clst
            INNER JOIN mz_lps_class AS cl ON clst.student_class_id = cl.id
            INNER JOIN mz_user_userprofile AS us ON clst.user_id = us.id AND clst.student_class_id = %s AND clst.user_id = %s;
            """
        , (studentclass, userid))
        deadlinedata = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    print deadlinedata
    return APIResult(result=deadlinedata)

@dec_timeit
@dec_make_conn_cursor
def updeadline(conn, cursor, deadline, status, user_id, class_id, quit_datetime):
    try:
        cursor.execute(
            """
            UPDATE mz_lps_classstudents SET deadline = %s,status = %s,quit_datetime = %s WHERE user_id = %s AND student_class_id = %s;
            """
        , (deadline, status, quit_datetime, user_id, class_id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

