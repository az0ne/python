# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
import db.api
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor

@dec_timeit("get_homepage_article_types")
@dec_get_cache("get_homepage_article_types")
@dec_make_conn_cursor
def get_homepage_article_types(conn, cursor, ):
    """
    """
    # qsql = """
    #     SELECT * FROM mz_common_articletype
    #     WHERE is_homepage=1
    # """

    qsql1 = """
        SELECT * FROM mz_common_articletype
        WHERE is_homepage=1 and is_career=1
        ORDER BY mz_common_articletype.index=0,mz_common_articletype.index
    """
    try:
        cursor.execute(qsql1)
        article_types = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=article_types)

@dec_timeit("get_all_article_types")
@dec_get_cache("get_all_article_types")
@dec_make_conn_cursor
def get_all_article_types(conn, cursor):
    """
    @brief 获取全部的is_visible为true文章类型 -- 文章列表页(以文章类别),

    :param conn:
    :param cursor:
    :return:

    @note 注意和get_homepage_article_types的区分
    """
    qsql = '''
        SELECT * FROM mz_common_articletype WHERE is_visible=1;
        '''
    try:
        cursor.execute(qsql)
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit("get_all_article_type_with_short_name")
@dec_get_cache("get_all_article_type_with_short_name")
@dec_make_conn_cursor
def get_all_article_type_with_short_name(conn, cursor, short_name):
    """
    @brief 获取全部的文章类型 -- 文章列表页(以文章类别),

    :param conn:
    :param cursor:
    :return:

    @note 注意和get_homepage_article_types的区分
    """
    qsql = '''
        SELECT * FROM mz_common_articletype WHERE short_name = %s;
        '''
    try:
        cursor.execute(qsql, (short_name, ))
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


def get_article_with_type(type_name, _enable_cache=False):
    """
    @brief 以文章类型为条件获取文章列表 -- 文章列表(以文章类别),
    :param conn:
    :param cursor:
    :param type_name:
    :return:
    """
    redis_key = '%s-%s' % ('get_article_with_type', type_name)

    @dec_timeit("get_article_with_type")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def _func(conn, cursor):
        sql = '''
            SELECT na.id, na.title, na.title_image, na.abstract, na.publish_date, na.nick_name, GROUP_CONCAT(t.id, '_', t.name) AS tag
            FROM mz_common_newarticle AS na
            INNER JOIN mz_common_articletype AS at ON na.article_type_id = at.id AND at.short_name = %s
            LEFT JOIN mz_common_objtagrelation AS otr ON na.id = otr.obj_id AND otr.obj_type = 'ARTICLE'
            LEFT JOIN mz_course_tag AS t ON otr.tag_id = t.id
            GROUP BY na.id
            ORDER BY na.is_top DESC, na.id DESC
            '''
        try:
            cursor.execute(sql, (type_name,))
            data = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        if _enable_cache:
            cache.set(redis_key, data, 60 * 60)
        return APIResult(result=data)
    return _func(_enable_cache=_enable_cache)

def get_article_with_tag(tag_id, _enable_cache=False):
    """
    @brief  获取某个tag的全部文章, 同时获取该文章的标签
    :param conn:
    :param cursor:
    :param tag_id:
    :return:

    @todo 该sql语句执行速度会慢,等待讨论优化
    """
    redis_key = '%s-%s' % ('get_article_with_tag', tag_id)

    @dec_timeit("get_article_with_tag")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def _func(conn, cursor):
        sql = '''
            SELECT na.id, na.title, na.title_image, na.abstract, na.publish_date, na.nick_name, GROUP_CONCAT(t.id, '_', t.name) AS tag
            FROM mz_common_newarticle AS na
            INNER JOIN mz_common_objtagrelation AS otr ON na.id = otr.obj_id AND otr.obj_type = 'ARTICLE'
            INNER JOIN mz_course_tag AS t ON otr.tag_id = t.id
            GROUP BY na.id
            HAVING tag LIKE %s
            ORDER BY na.is_top DESC, na.id DESC
            '''
        try:
            cursor.execute(sql, ('%%%s_%%' % tag_id,))
            data = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        if _enable_cache:
            cache.set(redis_key, data, 60 * 60)
        return APIResult(result=data)
    return _func(_enable_cache=_enable_cache)

@dec_timeit("get_article_with_course")
@dec_get_cache("get_article_with_course")
@dec_make_conn_cursor
def get_article_with_course(conn, cursor, course_id):
    """
    @brief 获取课程的相关的文章 -- 小课程介绍页

    :param conn:
    :param cursor:
    :param course_id:
    :return:

    @note 首先获取与该课程相关的职业课程,如果为不存在,则默认取id为0, 然后获取与该职业课程相关的文章.
    """
    sql = '''
        SELECT (CASE WHEN cc.id IS NULL THEN 0 ELSE cc.id END) AS id, cc.name FROM mz_common_careerobjrelation AS cor
        LEFT JOIN mz_course_careercourse AS cc ON cor.career_id = cc.id
        WHERE cor.obj_id = %s AND cor.obj_type = 'COURSE' AND cor.is_actived=1
        LIMIT 1
        '''
    try:
        cursor.execute(sql, (course_id,))
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    if not data:  # 如果不存在关联关系，则认为相关的职业课程为0
        data = (dict(id=0), )

    sql = '''
        SELECT na.id, na.title, na.title_image, na.abstract, GROUP_CONCAT(t.id, '_', t.name) AS tag FROM mz_common_newarticle AS na
        INNER JOIN mz_common_careerobjrelation AS cor ON na.id = cor.obj_id AND cor.obj_type = 'ARTICLE' AND cor.is_actived=1 AND cor.career_id = %s
        INNER JOIN mz_common_articletype AS cat ON na.article_type_id = cat.id AND cat.id < 100
        LEFT JOIN mz_common_objtagrelation AS otr ON na.id = otr.obj_id AND otr.obj_type = 'ARTICLE'
        LEFT JOIN mz_course_tag AS t ON otr.tag_id = t.id
        GROUP BY na.id
        ORDER BY na.is_top DESC, na.id DESC
        LIMIT 10
        '''
    try:
        cursor.execute(sql, (data[0].get('id', 0),))
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit("get_article_list_ad")
@dec_get_cache("get_article_list_ad")
@dec_make_conn_cursor
def get_article_list_ad(conn, cursor):
    """
    @brief 获取文章列表页的广告, 性能考虑, 防御性限制为8条
    :param conn:
    :param cursor:
    :return:
    """
    limit = 8
    sql = '''
        SELECT img_url, img_title, url FROM mz_common_newad
        WHERE type='ARTICLE' AND is_actived=1
        ORDER BY id DESC
        LIMIT %s;
        '''
    try:
        cursor.execute(sql, (limit,))
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit('add_view_count')
@dec_make_conn_cursor
def add_count(conn, cursor, article_id, data_type='view_count'):
    """
    @brief 增加文章的操作次数, 包含view_count, reply_count 以及 praise_count

    :param conn:
    :param cursor:
    :param article_id:
    :return:

    @todo 需要做+1操作的,还有文章的praise_count, reply_count 考虑是否请这三个功能合并为一个函数
    """
    count_map = dict(view_count='view_count = view_count + 1',
                     replay_count='replay_count = replay_count + 1',
                     praise_count='praise_count = praise_count + 1')
    try:
        sql = '%s %s %s' % ('UPDATE mz_common_newarticle SET', count_map[data_type.lower()], 'WHERE id=%s')
    except Exception as e:
        log.warn('exception: invalid count for article: %s.' % data_type)
        raise e
    try:
        cursor.execute(sql, (article_id, ))
        conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

@dec_timeit("get_career_course_article_types")
@dec_make_conn_cursor
def get_career_course_article_types(conn, cursor):
    """
    @brief 获取课程大纲页的文章类型 /course/ios/
    :param conn:
    :param cursor:
    :return:

    @todo @todo 跟get_homepage_article_types非常相似,考虑整合
    """
    qsql = """
        SELECT * FROM mz_common_articletype
        WHERE is_career=1
    """
    try:
        cursor.execute(qsql)
        article_types = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=article_types)


@dec_timeit("get_career_course_article")
@dec_make_conn_cursor
def get_career_course_article(conn, cursor, career_course_id=None):
    """
    @brief 获取职业课程大纲页(lps2.0)的文章 /course/ios/

    :param conn:
    :param cursor:
    :return:

    @todo 跟get_home_page_articles非常相似,考虑整合
    """
    TYPE_LIMIT = 8
    ARTICLE_LIMIT = 6
    DEFAULT_NAME = u"麦子分享".encode("utf8")

    article_types = db.api.get_career_course_article_types()
    if article_types.is_error():
        return article_types

    qsql_temp = """
            SELECT DISTINCT na.id, na.title, na.title_image,
            (CASE WHEN cc.name IS NULL THEN %s ELSE cc.name END) AS name
            FROM mz_common_newarticle AS na
            LEFT JOIN mz_common_careerobjrelation AS cor
            ON cor.obj_id = na.id AND cor.obj_type='ARTICLE' AND cor.is_actived = 1
            LEFT JOIN mz_course_careercourse AS cc ON cor.career_id = cc.id
            WHERE na.article_type_id = %s {_and} ORDER BY na.publish_date DESC LIMIT %s
        """

    if career_course_id:
        qsql = qsql_temp.format(_and=' AND cor.career_id = %s ')
    else:
        qsql = qsql_temp.format(_and='')

    articles = []

    for _type in article_types.result()[:TYPE_LIMIT]:
        try:
            if career_course_id:
                cursor.execute(qsql, (DEFAULT_NAME, _type["id"],
                                      career_course_id, ARTICLE_LIMIT))
            else:
                cursor.execute(qsql, (DEFAULT_NAME, _type["id"], ARTICLE_LIMIT))
            data = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        else:
            articles.append((_type, data))
    return APIResult(result=articles)
