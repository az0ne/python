# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_rebate_type(conn, cursor, name, renate_no):
    try:
        cursor.execute(
            """
               INSERT INTO mz_fxsys_rebatetype (name,rebate_no)
               values (%s,%s)
            """, (name, renate_no))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_rebate_type(conn, cursor, _id, name, renate_no):
    try:
        cursor.execute(
            """
               UPDATE mz_fxsys_rebatetype
               SET name=%s,renate_no=%s
               WHERE id=%s
            """, (name, renate_no, _id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_rebate_type_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              DELETE FROM mz_fxsys_rebatetype
              WHERE id=%s
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_rebate_type_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              SELECT id, name, rebate_no,last_date
              FROM mz_fxsys_rebatetype
              WHERE id=%s
            """, (_id,))
        data = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def list_rebate_type(conn, cursor):
    try:
        cursor.execute(
            """
              SELECT * FROM mz_fxsys_rebatetype
            """)
        data = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def is_exist_user_rebate_type(conn, cursor, rebate_type_id):
    try:
        cursor.execute(
            """
              SELECT 1 FROM mz_fxsys_user WHERE rebate_type_id=%s LIMIT 1;
            """, (rebate_type_id,))
        data = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=data)

