# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
@dec_timeit
@dec_make_conn_cursor
def insert_careerTagRelation(conn, cursor, tag_id,careercatagory_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_common_careertagrelation (tag_id,careercatagory_id) values (%s,%s);
            """, (tag_id,careercatagory_id,))

        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def update_careerTagRelation(conn, cursor,_id,tag_id,careercatagory_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                  UPDATE mz_common_careertagrelation set tag_id=%s,careercatagory_id=%s  WHERE id = %s;

            """, (tag_id,careercatagory_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

def delete_objTagRelation_by_careercatagory_id(conn, cursor,obj_id):
    """
    returns: true/false
    """
    try:
        cursor.execute(
            """
                  DELETE FROM mz_common_careertagrelation  WHERE careercatagory_id = %s;

            """, (obj_id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def get_objTagRelation_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT  obj_id,obj_type,tag_id,careercatagory_id
                FROM mz_common_objtagrelation WHERE id = %s
            """, (_id,))
        objTagRelation = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=objTagRelation)