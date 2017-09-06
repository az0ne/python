# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor
from db.cores.cache import cache
import db.api.course.career_catagory
from collections import  OrderedDict




@dec_timeit("get_banner")
@dec_get_cache("get_banner")
@dec_make_conn_cursor
def get_banner(conn, cursor):
    """
    首页banner
    """

    sql = """
        SELECT
            *
        FROM
            mz_common_banner
        WHERE
            type=1
        ORDER BY
            `index`;
    """
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_banner", data, 60 * 5)

    return APIResult(result=data)


@dec_timeit("get_wap_banner")
@dec_get_cache("get_wap_banner")
@dec_make_conn_cursor
def get_wap_banner(conn, cursor):
    """
    wap首页banner
    """

    sql = """
        SELECT
            *
        FROM
            mz_common_banner
        WHERE
            type=2
        ORDER BY
            `index`;
    """
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_wap_banner", data, 60 * 5)

    return APIResult(result=data)


@dec_timeit("get_career_newad")
@dec_get_cache("get_career_newad")
@dec_make_conn_cursor
def get_career_newad(conn, cursor):
    """
    获取首页大课程广告
    """

    sql = """
        SELECT
            *
        FROM
            mz_common_career_newad
        """
    try:
        cursor.execute(sql,)
        data = cursor.fetchall()
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_career_newad", data, 60 * 5)

    return APIResult(result=data)


@dec_timeit("get_home_page_articles")
@dec_get_cache("get_home_page_articles")
@dec_make_conn_cursor
def get_home_page_articles(conn, cursor):
    """
    首页文章
    """

    TYPE_LIMIT = 8
    ARTICLE_LIMIT = 6
    DEFAULT_NAME = u"麦子分享".encode("utf8")

    article_types = db.api.get_homepage_article_types()
    if article_types.is_error():
        return article_types

    sql = """
        SELECT DISTINCT
            na.id,
            na.title,
            CONCAT(LEFT(na.tidy_content,30), '...') AS abstract,
            na.title_image,
            (
                CASE
                WHEN cc.`name` IS NULL THEN
                    %s
                ELSE
                    cc.`name`
                END
            ) AS `name`
        FROM
            mz_common_newarticle AS na
        LEFT JOIN mz_common_careerobjrelation AS cor ON (
            cor.obj_id = na.id
            AND cor.obj_type = 'ARTICLE'
            AND cor.is_actived = 1
        )
        LEFT JOIN mz_course_careercourse AS cc ON cor.career_id = cc.id
        WHERE
            na.article_type_id = %s
        ORDER BY
            na.homepage_index = 0,
            na.homepage_index,
            na.publish_date DESC
        LIMIT %s
    """

    articles = []

    for _type in article_types.result()[:TYPE_LIMIT]:
        try:
            cursor.execute(sql, (DEFAULT_NAME, _type["id"], ARTICLE_LIMIT))
            data = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        else:
            articles.append((_type, data))

    # set cache
    cache.set("get_home_page_articles", articles, 60 * 5)
    return APIResult(result=articles)


@dec_timeit("get_hot_course_list")
@dec_get_cache("get_hot_course_list")
@dec_make_conn_cursor
def get_hot_course_list(conn, cursor):
    """
    首页精品课程
    """

    qsql = """
        SELECT DISTINCT
            cc.id,
            cc.`name`,
            cc.image,
            cc.click_count as student_count,
            cc.description
        FROM
            mz_homepage_course AS hc
        INNER JOIN mz_course_course AS cc ON hc.course_id = cc.id
        Where hc.careercatagory_id=%s
    """
    try:
        data = []
        hot_career_dict = OrderedDict()
        hot_career_dict[10] = ["UI设计", "design"]
        hot_career_dict[20] = ["Web 前端开发", "web"]
        hot_career_dict[30] = ["Python Web开发", "python"]
        hot_career_dict[40] = ["产品经理", "product"]
        hot_career_dict[50] = ["互联网运营", "product"]
        for hot_career_index, hot_career_name in hot_career_dict.items():
            cursor.execute(qsql, (hot_career_index,))
            result = cursor.fetchall()
            data.append([hot_career_name, result])
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    # set cache
    cache.set("get_hot_course_list", data, 60 * 5)

    return APIResult(result=data)


@dec_timeit("get_home_page_wiki")
@dec_get_cache("get_home_page_wiki")
@dec_make_conn_cursor
def get_home_page_wiki(conn, cursor):
    """
    首页wiki
    """
    ARTICLE_LIMIT = 6

    sql = """
        SELECT
            id,
            title,
            abstract,
            title_image,
            'wiki' AS `name`,
            wiki_url
        FROM
            mz_homepage_wiki
        LIMIT
            %s;
    """
    try:
        cursor.execute(sql, (ARTICLE_LIMIT,))
        data = cursor.fetchall()
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    else:
        wiki = ({'name': '参考文档'}, data)

    # set cache
    cache.set("get_home_page_wiki", wiki, 60 * 5)

    return APIResult(result=wiki)


@dec_timeit("get_homepage_links")
@dec_get_cache("get_homepage_links")
@dec_make_conn_cursor
def get_homepage_links(conn, cursor):
    """
    获取首页推广链接
    :param conn:
    :param cursor:
    :return: 首页推广链接列表
    """
    sql = """
        SELECT * FROM mz_homepage_link hl ORDER BY hl.index
    """
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_homepage_links", result, 60 * 5)

    return APIResult(result=result)
