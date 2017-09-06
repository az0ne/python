# -*- coding:utf-8 -*-

import datetime
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("list_my_message_by_page")
@dec_make_conn_cursor
def list_my_message_by_page(conn, cursor, user_id, page_index, page_size, message_types=None):
    """
    :param user_id: 用户ID
    :param page_index: 第几页
    :param page_size: 每页大小
    :param message_types: 字符串列表，默认为空
    """
    if not message_types:
        log.warn("no message_types.")
        return APIResult(code=False)

    start_index, end_index = get_page_info(page_index, page_size)
    
    try:
        in_p = ", ".join(map(lambda x: "%s", message_types))

        sql = """
            SELECT msg.id, msg.action_content, msg.date_action
            FROM mz_common_mymessage AS msg
            WHERE msg.action_type IN (%s) and msg.userB=%s
            ORDER BY msg.date_action DESC
            LIMIT %s,%s
              """
        
        count_sql = """
            SELECT count(*) AS count
            FROM mz_common_mymessage AS msg
            WHERE msg.action_type IN (%s) and msg.userB=%s
            """

        sql = sql % (in_p, user_id, start_index, end_index)
        count_sql = count_sql % (in_p, user_id)

        cursor.execute(sql, message_types)
        messages = cursor.fetchall()
        
        log.debug("query:%s" % cursor._last_executed)
        
        cursor.execute(count_sql, message_types)
        rows_count = cursor.fetchone()
        
        log.debug("query:%s" % cursor._last_executed)
        
        page_count = get_page_count(rows_count['count'], page_size)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
        
    page_dict = {
        'messages': messages,
        'rows_count': rows_count['count'],
        'page_count': page_count}                                       # todo 导入写进__init__.py

    return APIResult(result=page_dict)


@dec_timeit("update_message")
@dec_make_conn_cursor
def update_message(conn, cursor, user_id, message_types):
    """
    将消息未读变为已读
    :param user_id:
    :param message_types
    :return:
    """
    if not message_types:
        log.warn("no message_types.")
        return True

    try:
        sql = """
            UPDATE mz_common_mymessage
            SET is_new = 0
            WHERE userB=%s AND action_type IN (%s) AND is_new = 1
              """

        in_p = ", ".join(map(lambda x: "%s", message_types))
        sql = sql % ("%s", in_p)
        message_types.insert(0, user_id)

        cursor.execute(sql, message_types)
        conn.commit()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return True


def create_my_message(**kwargs):
    """
    添加新的my_信息
    :return:
    """
    def kwargs_get(key):
        return kwargs.get(key, 'Null')

    my_message = (
        kwargs_get('userA'),
        kwargs_get('userB'),
        kwargs_get('action_type'),
        kwargs_get('action_id'),
        kwargs_get('action_content'),
        kwargs.get('date_action', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        kwargs.get('is_new', 1)
    )

    @dec_make_conn_cursor
    def main(conn, cursor):
        # 插入回复数据
        sql_insert = """
        INSERT INTO mz_common_mymessage(
            userA,
            userB,
            action_type,
            action_id,
            action_content,
            date_action,
            is_new
        )VALUES (%s)
        """ % (','.join(map(lambda x: '%s', my_message)))

        try:
            # 插入回复
            cursor.execute(sql_insert, my_message)
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=True)

    return main()


@dec_make_conn_cursor
def get_my_message_count(conn, cursor, user_id, message_types=None):
    """
    :param user_id: 用户ID
    :param message_types: 字符串列表，默认为空
    """
    if not message_types:
        log.warn("no message_types.")
        return APIResult(code=False)

    try:
        in_p = ", ".join(map(lambda x: "%s", message_types))

        count_sql = """
            SELECT count(*) AS count
            FROM mz_common_mymessage AS msg
            WHERE msg.action_type IN (%s) and msg.userB=%s AND is_new = 1
            """

        count_sql = count_sql % (in_p, user_id)
        cursor.execute(count_sql, message_types)
        rows_count = cursor.fetchone()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return APIResult(result=rows_count['count'])
