#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def homepage_wiki_list(conn, cursor):
    """
        获取所有的homepage_wiki
    """

    try:
        cursor.execute(
            """
            SELECT id,title,abstract,title_image,wiki_url FROM mz_homepage_wiki
            """
        )
        homepage_wiki = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=homepage_wiki)


@dec_timeit
@dec_make_conn_cursor
def get_homepage_wiki_by_id(conn, cursor, _id):
    '''
    根据id获取homepage_wiki的数据
    :param conn:
    :param cursor:
    :param _id: homepage_wiki 的 id
    :return: None/dict()
    '''

    try:
        cursor.execute(
            """
                SELECT id,title,abstract,title_image,wiki_url
                FROM mz_homepage_wiki
                WHERE id=%s;
            """, (_id,)
        )
        homepage_wiki = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=homepage_wiki)


@dec_timeit
@dec_make_conn_cursor
def update_homepage_wiki(conn, cursor, data):
    """
    根据id更新首页wiki的信息
    :param data: {"title":title,……}
    :param conn:
    :param cursor:
    :param _id:
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_homepage_wiki set title=%s, abstract=%s,wiki_url=%s,title_image=%s WHERE id=%s
            """, (data['title'], data['abstract'], data['wiki_url'], data['image_path'], data['id'],)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)
