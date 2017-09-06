# -*-coding:utf-8-*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool

@dec_timeit
@dec_make_conn_cursor
def insert_career_obj_relation(conn, cursor, obj_type,obj_id,career_id,is_actived):
    '''
    '''

    try:
        cursor.execute("""
        INSERT INTO mz_common_careerobjrelation (obj_type,obj_id,career_id,is_actived)
        VALUE (%s,%s,%s,%s)
        """, (obj_type,obj_id,career_id,is_actived))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_careerobjrelation_by_obj(conn,cursor,_id, obj_type):
    """
    returns: true/false
    """
    try:
        cursor.execute(
            """
                DELETE FROM mz_common_careerobjrelation WHERE obj_id=%s AND obj_type=%s;
            """, (_id,obj_type))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_careercourse_by_obj(conn, cursor, _id, obj_type):
     """

     """
     try:
        cursor.execute(
            """
            SELECT careercourse.name,careercourse.id
            FROM mz_common_careerobjrelation AS careerobjrelation LEFT JOIN mz_course_careercourse AS careercourse ON careerobjrelation.career_id=careercourse.id
            WHERE careerobjrelation.obj_id=%s AND careerobjrelation.obj_type=%s;
            """, (_id,obj_type))
        careercourse = cursor.fetchall()
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=careercourse)
