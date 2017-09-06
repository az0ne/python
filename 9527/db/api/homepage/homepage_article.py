# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def search_article_by_article_type_id(conn, cursor, article_type_id, page_size):
    """
    根据文章类型id来搜索数据
    :param conn:
    :param cursor:
    :param title: 文章title
    :param article_type_id: 文章类型id
    :param page_index: 当前页数
    :param page_size: 每页显示条数
    :return:
    """
    sql = """select art.id,art.title,art.sub_title,art.publish_date,
                art.homepage_index,at.name as articletype_name
                from mz_common_newarticle as art
                LEFT JOIN mz_common_articletype as at ON at.id=art.article_type_id
                WHERE  art.article_type_id = %s
                ORDER BY art.homepage_index=0,art.homepage_index,art.publish_date DESC
                limit %s
                """
    try:
        cursor.execute(sql, (article_type_id, page_size))
        articles = cursor.fetchall()

        rows_count = page_size
        page_count = tool.get_page_count(rows_count, page_size)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    article_dict = {
        "result": articles,
        "rows_count": rows_count,
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def search_article_by_title(conn, cursor, title, page_index, page_size):
    """
    根据文章title来搜索数据
    :param conn:
    :param cursor:
    :param title: 文章title
    :param page_index: 当前页数
    :param page_size: 每页显示条数
    :return:
    """
    sql = """select art.id,art.title,art.sub_title,art.publish_date,
                art.homepage_index,at.name as articletype_name
                from mz_common_newarticle as art
                LEFT JOIN mz_common_articletype as at ON at.id=art.article_type_id
                WHERE art.title LIKE %s
                ORDER BY art.homepage_index=0,art.homepage_index,art.publish_date DESC
                limit %s,%s
                """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(sql, (title, start_index, page_size))
        articles = cursor.fetchall()

        cursor.execute(
            """
                select count(*) as count from mz_common_newarticle as art
                WHERE  art.title LIKE %s
            """, (title,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    article_dict = {
        "result": articles,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_homepage_article_types(conn, cursor):
    """
        获取文章类型ID
    """

    try:
        cursor.execute(
            """
            SELECT id FROM mz_common_articletype
            WHERE is_homepage=1
            ORDER BY id
        """
        )
        article_types = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=article_types)


@dec_timeit
@dec_make_conn_cursor
def list_article_for_homepage_by_page(conn, cursor, page_size, page_index):
    """
    分页查询
    :param conn:
    :param cursor:
    :param page_size: 每页条数
    :param page_index: 当前是第几页
    :return: id,title,sub_title,public_data,homepage_index字段的集合
    """
    articleType_list = []
    article_types = get_homepage_article_types().result()
    for _type in article_types:
        articleType_list.append(_type['id'])
    sql = """
    select art.id,art.title,art.sub_title,art.publish_date,art.homepage_index,at.name as articletype_name
                from mz_common_newarticle as art
                LEFT JOIN mz_common_articletype as at ON at.id=art.article_type_id
                WHERE at.is_homepage=1 and at.id = %s
                ORDER BY art.homepage_index=0,art.homepage_index,art.publish_date DESC
                limit %s
    """
    _type = articleType_list[page_index - 1:page_index]
    try:
        cursor.execute(sql, (_type[0], page_size))
        articles = cursor.fetchall()

        rows_count = page_size * len(articleType_list)
        page_count = tool.get_page_count(rows_count, page_size)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    article_dict = {
        "result": articles,
        "rows_count": rows_count,
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_article_homepage_index(conn, cursor, _id):
    """
    获取文章表id,homepage_index字段值,根据id
    :param conn:
    :param cursor:
    :param _id: newarticle表中的id值
    :return:
    """
    try:
        cursor.execute(
            """
                select id,title,sub_title,homepage_index from mz_common_newarticle
                WHERE id=%s
            """, (_id,)
        )
        homepage_article = cursor.fetchone()

    except Exception as e:
        log.warn(
            "cursor exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=homepage_article)


@dec_timeit
@dec_make_conn_cursor
def update_homepage_article_of_homepage_index(conn, cursor, _id, homepage_index):
    """
    更新文章表中的首页文章序号
    :param conn:
    :param cursor:
    :param _id:
    :param homepage_index: 首页文章序号
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_newarticle set homepage_index=%s WHERE id=%s
            """, (homepage_index, _id)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)
