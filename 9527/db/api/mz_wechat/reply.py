# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def add_reply(conn, cursor, _type, content):
    """
    添加回复
    :param conn:
    :param cursor:
    :param _type: 消息类型 mz_wechat.constants.ReplyType
    :param content: 回复内容 json串
    :return: reply id
    """

    sql = """
        INSERT INTO mz_wechat_reply (
            `type`,
            `content`
        )
        VALUES
            (%s, %s)
    """

    try:
        cursor.execute(sql, (_type, content))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=cursor.lastrowid)


@dec_make_conn_cursor
@dec_timeit
def update_reply(conn, cursor, r_id, _type, content):
    """
    修改回复
    :param conn:
    :param cursor:
    :param r_id: id
    :param _type: 消息类型 mz_wechat.constants.ReplyType
    :param content: 回复内容 json串
    :return:
    """

    sql = """
        UPDATE mz_wechat_reply
        SET `type` = %s,
         `content` = %s
        WHERE
            id = %s
    """

    try:
        cursor.execute(sql, (_type, content, r_id))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def del_reply(conn, cursor, r_id):
    """
    删除回复
    :param conn:
    :param cursor:
    :param r_id: id
    :return:
    """

    sql = """
        DELETE FROM mz_wechat_reply WHERE id = %s
    """

    try:
        cursor.execute(sql, (r_id,))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def add_reply_message(conn, cursor, m_id, r_id):
    """
    添加一条规则
    :param conn:
    :param cursor:
    :param m_id: message id
    :param r_id: reply id
    :return: id
    """

    sql = """
        INSERT INTO mz_wechat_reply_message (
            `wechat_message_id`,
            `wechat_reply_id`
        )
        VALUES
            (%s, %s)
    """

    try:
        cursor.execute(sql, (m_id, r_id))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=cursor.lastrowid)


@dec_timeit
@dec_make_conn_cursor
def get_reply(conn, cursor, _id):
    """
    根据id获取reply的信息
    :param conn:
    :param cursor:
    :param _id:
    :return:
    """
    try:
        cursor.execute(
                """
                SELECT id,type,content
                FROM  mz_wechat_reply
                WHERE id=%s;
                """, (_id,))
        reply = cursor.fetchone()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=reply)