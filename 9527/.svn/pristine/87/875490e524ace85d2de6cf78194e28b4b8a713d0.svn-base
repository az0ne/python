# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from mz_wechat import constants
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_rules_list(conn, cursor, page_index=1, page_size=10, keywords=None):
    """
    获取规则列表
    :param conn:
    :param cursor:
    :param page_index: 第几页
    :param page_size: 每页多少条
    :param keywords: 关键字
    :return: course广告列表
    """

    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
        SELECT
            {fields}
        FROM
            mz_wechat_message AS msg
        INNER JOIN mz_wechat_reply_message AS rm ON rm.wechat_message_id = msg.id
        INNER JOIN mz_wechat_reply AS r ON r.id = rm.wechat_reply_id
    """

    base_wheres = []
    if keywords:
        base_sql += ' AND msg.key LIKE %s '
        img_title = '%' + str(keywords) + '%'
        base_wheres.append(img_title)

    sql = base_sql.format(fields='msg.id, msg.type AS message_type, `key`, '
                                 'match_type, r.type AS reply_type, content')
    count_sql = base_sql.format(fields='COUNT(msg.id) as count')

    # 生成查询list用的where条件(->sql)，base_wheres为count查询用(->count_sql)
    wheres = base_wheres[:]
    sql += 'LIMIT %s, %s'
    wheres.extend([start_index, page_size])

    try:
        cursor.execute(sql, wheres)
        result = cursor.fetchall()
        for r in result:
            r['message_type_name'] = constants.MessageType.map[r['message_type']]
            r['match_type_name'] = constants.MatchType.map[r['match_type']]
            r['reply_type_name'] = constants.ReplyType.map[r['reply_type']]
        log.info("query: %s" % cursor.statement)

        cursor.execute(count_sql, base_wheres)
        rows_count = cursor.fetchone()["count"]
        log.info("query: %s" % cursor.statement)

        page_count = tool.get_page_count(rows_count, page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(
        result=dict(rules_list=result,
                    page=dict(rows_count=rows_count, page_count=page_count,
                              page_size=page_size, page_index=page_index))
    )


@dec_make_conn_cursor
@dec_timeit
def add_message(conn, cursor, _type, key='', match_type=0):
    """
    添加用户消息
    :param conn:
    :param cursor:
    :param _type: 消息类型 mz_wechat.constants.MessageType
    :param key: 关键字 普通回复时为空 关键字回复为对应关键字 关注为空 上传图片为空
    :param match_type: 关键字匹配规则 mz_wechat.constants.MatchType
    :return: message id
    """

    sql = """
        INSERT INTO mz_wechat_message (
            `type`,
            `key`,
            `match_type`
        )
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (_type, key, match_type))
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
def update_message(conn, cursor, m_id, _type, key, match_type):
    """
    修改用户消息
    :param conn:
    :param cursor:
    :param m_id: id
    :param _type: 消息类型 mz_wechat.constants.MessageType
    :param key: 关键字 普通回复时为空 关键字回复为对应关键字 关注为空 上传图片为空
    :param match_type: 关键字匹配规则 mz_wechat.constants.MatchType
    :return:
    """

    sql = """
        UPDATE mz_wechat_message
        SET `type` = %s,
         `key` = %s,
         `match_type` = %s
        WHERE
            id = %s
    """

    try:
        cursor.execute(sql, (_type, key, match_type, m_id))
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
def del_message(conn, cursor, m_id):
    """
    删除用户消息
    :param conn:
    :param cursor:
    :param m_id: id
    :return:
    """

    sql = """
        DELETE FROM mz_wechat_message WHERE id = %s
    """

    try:
        cursor.execute(sql, (m_id,))
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
def get_rules(conn, cursor, m_id):
    """
    根据message id获取规则
    :param conn:
    :param cursor:
    :param m_id:
    :return:
    """

    sql = """
        SELECT
            msg.id,
            msg.type AS message_type,
            `key`,
            match_type,
            r.type AS reply_type,
            content
        FROM
            mz_wechat_message AS msg
        INNER JOIN mz_wechat_reply_message AS rm ON rm.wechat_message_id = msg.id
        INNER JOIN mz_wechat_reply AS r ON r.id = rm.wechat_reply_id
        WHERE
            msg.id = %s
    """

    try:
        cursor.execute(sql, (m_id,))
        result = cursor.fetchone()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def del_rules(conn, cursor, m_id):
    """
    删除用户消息
    :param conn:
    :param cursor:
    :param m_id: id
    :return:
    """

    sql = """
        DELETE
            msg.*, r.*, rm.*
        FROM
            mz_wechat_message AS msg
        INNER JOIN mz_wechat_reply_message AS rm ON rm.wechat_message_id = msg.id
        INNER JOIN mz_wechat_reply AS r ON r.id = rm.wechat_reply_id
        WHERE
            msg.id = %s
    """

    try:
        cursor.execute(sql, (m_id,))
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
def add_rules(conn, cursor, msg, reply):
    """
    添加规则
    :param conn:
    :param cursor:
    :param msg: _type, key='', match_type=0
    :param reply: _type, content
    :return:
    """

    m_sql = """
        INSERT INTO mz_wechat_message (
            `type`,
            `key`,
            `match_type`
        )
        VALUES (%s, %s, %s)
    """

    r_sql = """
        INSERT INTO mz_wechat_reply (
            `type`,
            `content`
        )
        VALUES
            (%s, %s)
    """

    rm_sql = """
        INSERT INTO mz_wechat_reply_message (
            `wechat_message_id`,
            `wechat_reply_id`
        )
        VALUES
            (%s, %s)
    """

    try:
        cursor.execute(m_sql, (msg['type'], msg.get('key', ''), msg.get('match_type', 0)))
        m_id = cursor.lastrowid

        cursor.execute(r_sql, (reply['type'], reply['content']))
        r_id = cursor.lastrowid

        cursor.execute(rm_sql, (m_id, r_id))

        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        conn.rollback()
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)
