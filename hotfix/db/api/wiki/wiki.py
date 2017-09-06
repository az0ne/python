# -*- coding: utf-8 -*-

from db.cores.cache import cache
from mz_common.functions import safe_int
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_wiki_course_types")
@dec_make_conn_cursor
def get_wiki_course_types(conn, cursor):
    """
    获取wiki课程分类
    :param conn:
    :param cursor:
    :return: wiki课程分类列表
    """

    sql = """
        SELECT
          wct.id, wct.name, wct.short_name, wct.img_url, wct.img_title
        FROM mz_wiki_course_type AS wct
        ORDER BY wct.index
    """

    try:
        cursor.execute(sql)
        wiki_types = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=wiki_types)


@dec_timeit("get_wiki_course_by_type_short_name")
@dec_make_conn_cursor
def get_wiki_courses_by_type_short_name(conn, cursor, short_name):
    """
    根据wiki课程分类查询分类下的所有课程
    :param conn:
    :param cursor:
    :param short_name: 课程类型的short_name
    :return: 课程列表
    """

    sql = """
        SELECT
          wc.id, wc.name, wc.short_name, wc.type_id,
          wc.img_url, wc.img_title, wc.info
        FROM mz_wiki_course AS wc
        INNER JOIN mz_wiki_course_type AS wct ON wct.id = wc.type_id
        WHERE wct.short_name = %s ORDER BY wc.index
    """

    try:
        cursor.execute(sql, (short_name,))
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_wiki_course_by_short_name")
@dec_make_conn_cursor
def get_wiki_course_by_short_name(conn, cursor, short_name):
    """
    根据wiki课程short_name查出该课程
    :param conn:
    :param cursor:
    :param short_name: wiki课程的short_name
    :return: 课程
    """

    sql = """
        SELECT
          wc.name, wc.short_name, wc.img_url,
          wc.img_title, wc.course_id, wc.info
        FROM mz_wiki_course AS wc
        WHERE wc.short_name = %s LIMIT 1
    """

    try:
        cursor.execute(sql, (short_name,))
        result = cursor.fetchone()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result) if result else APIResult(code=False)


@dec_timeit("get_lps_course_by_wiki_course_short_name")
@dec_make_conn_cursor
def get_lps_course_by_wiki_course_short_name(conn, cursor, short_name):
    """
    根据wiki课程short_name查lps小课程
    :param conn:
    :param cursor:
    :param short_name: wiki课程的short_name
    :return: lps小课程 字段：id, name
    """

    sql = """
        SELECT cc.id, cc.name FROM mz_course_course AS cc
        INNER JOIN mz_wiki_course AS wc ON wc.course_id = cc.id
        WHERE wc.short_name = %s
    """

    try:
        cursor.execute(sql, (short_name,))
        result = cursor.fetchone()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_recommend_course_by_wiki_course_short_name")
@dec_make_conn_cursor
def get_recommend_course_by_wiki_course_short_name(conn, cursor, short_name):
    """
    根据wiki课程short_name查lps小课程
    :param conn:
    :param cursor:
    :param short_name: wiki课程的short_name
    :return: lps小课程 字段：id, name
    """

    course_id_sql = """
        SELECT
            recommend_course_id1,
            recommend_course_id2,
            recommend_course_id3,
            recommend_course_id4
        FROM
            mz_wiki_course
        WHERE
            short_name = %s
    """
    sql = """
        SELECT
            id,
            `name`
        FROM
            mz_course_course
        WHERE
            id IN ({0})
    """

    try:
        cursor.execute(course_id_sql, (short_name,))
        ids = cursor.fetchone()

        ids = [str(_id) for _id in ids.values() if _id]
        sql = sql.format(', '.join(ids))

        cursor.execute(sql)
        result = cursor.fetchall()

        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_all_wiki_course")
@dec_make_conn_cursor
def get_all_wiki_course(conn, cursor, is_homepage=False):
    """
    获取所有课程
    :param conn:
    :param cursor:
    :param is_homepage: 是否在首页展示
    :return: 课程列表
    """

    sql = """
        SELECT
          wc.id, wc.type_id, wc.name, wc.short_name,
          wc.img_url, wc.img_title, wc.info
        FROM mz_wiki_course AS wc {0} ORDER BY wc.index
    """.format('WHERE is_homepage = 1' if is_homepage else '')

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_wiki_chapter_by_course_short_name")
@dec_make_conn_cursor
def get_wiki_chapters_by_course_short_name(conn, cursor, short_name):
    """
    根据wiki课程查询课程下的所有章节
    :param conn:
    :param cursor:
    :param short_name: 课程的short_name
    :return: 章节列表
    """

    sql = """
        SELECT wcp.id, wcp.name FROM mz_wiki_chapter AS wcp
        INNER JOIN mz_wiki_course AS wc ON wc.id = wcp.course_id
        WHERE wc.short_name = %s ORDER BY wcp.index
    """

    try:
        cursor.execute(sql, (short_name,))
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_wiki_chapter_by_course_short_name")
@dec_make_conn_cursor
def get_wiki_chapter_by_item_id(conn, cursor, item_id):
    """
    根据wiki知识点id查询对应的章节
    :param conn:
    :param cursor:
    :param item_id: 知识点id
    :return: 章节
    """

    sql = """
        SELECT wcp.id, wcp.name FROM mz_wiki_chapter AS wcp
        INNER JOIN mz_wiki_item AS wi ON wi.chapter_id = wcp.id
        WHERE wi.id = %s
    """

    try:
        cursor.execute(sql, (item_id,))
        result = cursor.fetchone()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_timeit("get_wiki_item_by_course_short_name")
@dec_make_conn_cursor
def get_wiki_items_by_course_short_name(conn, cursor, short_name,
                                        full_field=False, is_first=False):
    """
    根据wiki课程查询课程下的所有知识点
    :param conn:
    :param cursor:
    :param short_name: 课程的short_name
    :param full_field: 是否是去全部字段，False为只取id,name,short_name,chapter_id
    :param is_first: 是否只取第一个知识点
    :return: 课程列表
    """

    if full_field:
        field = 'wi.*'
    else:
        field = 'wi.id, wi.name, wi.short_name, wi.chapter_id'

    sql = """
        SELECT {field}
        FROM mz_wiki_item AS wi
        INNER JOIN mz_wiki_course AS wc ON wc.id = wi.course_id
        INNER JOIN mz_wiki_chapter AS wcp ON wcp.id = wi.chapter_id
        WHERE wc.short_name = %s ORDER BY wcp.index, wi.index {limit}
    """.format(field=field, limit='limit 1' if is_first else '')

    try:
        cursor.execute(sql, (short_name,))
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


def get_wiki_item_by_short_name(course_short_name, item_short_name):
    """
    根据wiki知识点short_name获取知识点
    :param course_short_name: 课程(wiki_course)的short_name
    :param item_short_name: 知识点(item)的short_name
    :return: 课程列表
    """

    if not isinstance(course_short_name, basestring):
        log.warn("wiki item short_name is not a string")
        return APIResult(code=False)

    if not isinstance(item_short_name, basestring):
        log.warn("wiki item short_name is not a string")
        return APIResult(code=False)

    cache_key = 'get_wiki_item_by_short_name_{}_{}'.format(
        course_short_name, item_short_name)

    @dec_timeit("get_wiki_item_by_short_name")
    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
            SELECT wi.* FROM mz_wiki_item AS wi
            INNER JOIN mz_wiki_course AS wc ON wc.id = wi.course_id
            WHERE wc.short_name = %s AND wi.short_name = %s
            ORDER BY wi.index LIMIT 1
        """

        try:
            cursor.execute(sql, (course_short_name, item_short_name))
            result = cursor.fetchone()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        if result:
            # set cache
            cache.set(cache_key, result, 1 * 60)
            return APIResult(result=result)
        else:
            return APIResult(code=False)

    return main()


@dec_timeit("get_all_course_first_item_short_name")
@dec_make_conn_cursor
def get_all_course_first_item_short_name(conn, cursor):
    """
    获取所有课程的第一个知识点的short_name
    :param conn:
    :param cursor:
    :return: 返回字段为：course_id, first_item_short_name
    """

    sql = """
        SELECT * FROM
          (SELECT wi.course_id, wi.short_name AS first_item_short_name
          FROM mz_wiki_item AS wi
          INNER JOIN mz_wiki_chapter AS wcp ON wcp.id = wi.chapter_id
          ORDER BY wcp.index, wi.index, wi.id) AS wi
        GROUP BY wi.course_id
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

    return APIResult(result=result)


def get_wiki_links():
    """
    获取wiki页面的友情链接
    :return: 友情链接列表
    """

    redis_key = 'get_wiki_links'

    @dec_timeit("get_wiki_links")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
            SELECT wl.title, wl.url FROM mz_wiki_link AS wl ORDER BY wl.index
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
        cache.set(redis_key, result, 60 * 60 * 1)  # cache 1小时

        return APIResult(result=result)

    return main()


def get_wiki_course_by_lps_course_id(course_id, num=10):
    """
    根据lps课程id 获取num条wiki课程
    :param course_id: lps课程id
    :param num: 取几条，默认10条
    :return: wiki知识点列表
    """

    if not safe_int(course_id):
        log.warn(
            'course_id is not a int. course_id: {0}. type: {1}.'
            .format(course_id, type(course_id)))
        return APIResult(result=[])

    if not safe_int(num):
        log.debug(
            'num is not a int. num: {0}. type: {1}'.format(num, type(num)))
        return APIResult(result=[])

    redis_key = 'get_wiki_by_course_id_{}'.format(course_id)

    @dec_timeit('get_wiki_course_by_lps_course_id')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
            SELECT * FROM
            (
                SELECT
                    wc.id,
                    wc.name,
                    wc.short_name,
                    wc.info,
                    wi.short_name AS first_item_short_name
                FROM
                    (
                        SELECT
                            wc.id, wc.name, wc.short_name, wc.info
                        FROM mz_wiki_course AS wc
                        WHERE wc.course_id = %s
                    ) AS wc, mz_wiki_item AS wi
                WHERE wi.course_id = wc.id ORDER BY wi.index, wi.id
            ) AS wc GROUP BY wc.id LIMIT %s
        """

        try:
            cursor.execute(sql, (course_id, num))
            result = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise

        # set cache
        cache.set(redis_key, result, 60 * 5)  # cache 5分钟

        return APIResult(result=result)

    return main()


@dec_timeit("get_wiki_ad_by_course_short_name")
@dec_make_conn_cursor
def get_wiki_ad_by_course_short_name(conn, cursor, course_short_name):
    """
    获取wiki广告
    :param conn:
    :param cursor:
    :param course_short_name: 课程short_name
    :return: 返回字段为：广告描述，url，图片
    """

    sql = """
        SELECT
            ad.*
        FROM
            mz_wiki_ad AS ad
        INNER JOIN mz_wiki_course_type AS ct ON ct.id = ad.course_type_id
        INNER JOIN mz_wiki_course AS wc ON wc.type_id = ct.id
        AND wc.short_name = %s
        LIMIT 1
    """

    try:
        cursor.execute(sql, (course_short_name,))
        result = cursor.fetchone()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=result)


@dec_timeit("get_home_page_wiki_by_career_id")
@dec_make_conn_cursor
def get_home_page_wiki_by_career_id(conn, cursor, career_id):
    """
    首页banner
    """
    ARTICLE_LIMIT = 6

    sql = """
        SELECT
            id,
            title,
            title_image,
            'wiki' AS `name`,
            wiki_url
        FROM
            mz_common_wiki
        WHERE
            career_id = %s
        LIMIT %s;
    """
    try:
        cursor.execute(sql, (career_id, ARTICLE_LIMIT))
        data = cursor.fetchall()
        log.debug("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    else:
        wiki = ({'name': 'wiki笔记'}, data)

    return APIResult(result=wiki)


@dec_timeit("get_wiki_by_lps_course_id")
@dec_make_conn_cursor
def get_wiki_by_lps_course_id(conn, cursor, course_id, limit=20):
    """
    根据lps小课程id获取wiki
    :param conn:
    :param cursor:
    :param course_id: 课程short_name
    :param limit: 获取多少条
    :return: 返回字段为：广告描述，url，图片
    """

    sql = """
        SELECT
            wi.`name`,
            wi.short_name AS item_short_name,
            SUBSTRING(wi.tidy_content, 1, 150) AS tidy_content,
            wc.short_name AS course_short_name,
            wc.img_url,
            wc.img_title
        FROM
            mz_wiki_chapter AS wcp
        INNER JOIN mz_wiki_item AS wi ON wi.chapter_id = wcp.id
        INNER JOIN mz_wiki_course AS wc ON wc.id = wi.course_id
        WHERE
            wcp.video_course_id = %s
        LIMIT %s
    """

    try:
        cursor.execute(sql, (course_id, limit))
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=result)
