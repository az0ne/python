# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_news_count(conn, cursor):
    """
    获取数据库中图文消息的数量
    :param conn:
    :param cursor:
    """

    sql = """
        SELECT count(*) as count
        FROM mz_wechat_material_news
    """

    try:
        cursor.execute(sql)
        news_count = cursor.fetchone()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=news_count['count'])


@dec_make_conn_cursor
@dec_timeit
def store_wechat_news(conn, cursor, news):
    """
    保存
    :param conn:
    :param cursor:
    :param news: json格式的微信图文数据
    """

    sql = """
        INSERT INTO mz_wechat_material_news (content) VALUES %s
    """

    try:
        sql1 = sql % ','.join(map(lambda x: '(%s)', news))
        cursor.execute(sql1, news)
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult()


@dec_make_conn_cursor
@dec_timeit
def get_wechat_news(conn, cursor, page_index=1, page_size=10, content=None):
    """
    获取图文
    :param conn:
    :param cursor:
    :param page_index: 第几页
    :param page_size: 每页多少条
    :param content: 搜索
    :return: 图文消息列表
    """

    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
        SELECT {fields} FROM mz_wechat_material_news WHERE 1=1
    """

    base_wheres = []
    if content:
        base_sql += ' AND content LIKE %s '
        content = tool.sql_unicode_encoding(content)
        content = '%' + content + '%'
        base_wheres.append(content)

    sql = base_sql.format(fields='id, content')
    count_sql = base_sql.format(fields='COUNT(id) as count')

    # 生成查询list用的where条件(->sql)，base_wheres为count查询用(->count_sql)
    wheres = base_wheres[:]
    sql += 'LIMIT %s, %s'
    wheres.extend([start_index, page_size])

    try:
        cursor.execute(sql, wheres)
        result = cursor.fetchall()
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
        result=dict(news_list=result,
                    page=dict(rows_count=rows_count, page_count=page_count,
                              page_size=page_size, page_index=page_index))
    )


@dec_make_conn_cursor
@dec_timeit
def del_news(conn, cursor):
    """
    删除数据库中所有图文消息
    :param conn:
    :param cursor:
    """

    sql = """
        TRUNCATE TABLE mz_wechat_material_news
    """

    try:
        cursor.execute(sql)
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
