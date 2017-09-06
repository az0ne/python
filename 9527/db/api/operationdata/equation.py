# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_equation_list(conn, cursor):
    """
    获取所有公式
    :param conn:
    :param cursor:
    :return: wiki广告列表
    """

    sql = """
        SELECT id, equation, description FROM mz_operation_equation
    """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.info("query: %s" % cursor.statement)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def add_equation(conn, cursor, equation, description):
    """
    新增公式
    :param conn:
    :param cursor:
    :param equation: 公式
    :param description: 公式描述
    :return: True or False
    """

    sql = """
        INSERT INTO mz_operation_equation (
            equation, description
        )
        VALUES (%s, %s)
    """

    try:
        cursor.execute(sql, (equation, description))
        e_id = cursor.lastrowid
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=e_id)


@dec_make_conn_cursor
@dec_timeit
def del_equation(conn, cursor, e_id):
    """
    删除公式
    :param conn:
    :param cursor:
    :param e_id: 公式id
    :return: True or False
    """

    sql = """
        DELETE FROM mz_operation_equation WHERE id = %s
    """

    try:
        cursor.execute(sql, (e_id,))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)
