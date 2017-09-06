# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mongodbconn import get_mongo_db
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("make_course_career_names")
@dec_make_conn_cursor
def make_course_career_names(conn, cursor):
    """
    获取小课程对应的职业课程名称
    :param conn:
    :param cursor:
    :return:返回数据类型：{'course_id':[]}
    """
    courses = {}
    try:
        cursor.execute("""
                        SELECT obj_id as course_id, name, short_name from mz_common_careerobjrelation
                        LEFT JOIN mz_course_careercourse
                        ON mz_course_careercourse.id=mz_common_careerobjrelation.career_id
                        WHERE obj_type="COURSE" AND is_actived=1;
                  """)
        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s.'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    for res in res_list:
        if not res["name"] or not res["short_name"]:
            continue

        cr = courses.get(res['course_id'], set())
        cr.add((res["name"], res["short_name"]))
        courses[res['course_id']] = cr

    return APIResult(result=courses)


@dec_timeit("make_course_charset")
@dec_make_conn_cursor
def make_course_chapter(conn, cursor):
    """
    获取小课程下有多少个章节
    :param conn:
    :param cursor:
    :return:
    """
    courses = {}
    try:
        cursor.execute("""
            SELECT course_id, count(id) as count FROM mz_course_lesson group by course_id
        """)

        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s.'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    for res in res_list:
        courses[res['course_id']] = res['count']

    return APIResult(result=courses)


@dec_timeit("make_wiki_course_meta")
@dec_make_conn_cursor
def make_wiki_course_meta(conn, cursor):
    """
    获取wiki_item的wiki课程信息
    :param conn:
    :param cursor:
    :return:
    """
    wiki_dict = {}

    try:
        cursor.execute("""
            SELECT id, name, short_name, img_url FROM mz_wiki_course;
        """)

        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s.'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    for res in res_list:
        wiki_dict[res['id']] = (res["name"], res["short_name"], res["img_url"])

    return APIResult(result=wiki_dict)


@dec_timeit("make_article_tags")
@dec_make_conn_cursor
def make_article_tags(conn, cursor):
    """
    获取文章tag
    :param conn:
    :param cursor:
    :return:
    """
    articles = {}

    try:
        cursor.execute("""
            SELECT otr.obj_id, ct.id,ct.name
            FROM mz_course_tag as ct
            INNER JOIN mz_common_objtagrelation AS otr
            ON ct.id = otr.tag_id AND otr.obj_type = 'ARTICLE';
        """)

        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    for res in res_list:
        cr = articles.get(res["obj_id"], set())
        cr.add((res["id"], res["name"]))
        articles[res["obj_id"]] = cr

    return APIResult(result=articles)


@dec_timeit("make_course_teacher")
@dec_make_conn_cursor
def make_course_teacher(conn, cursor):
    """
    获取小课程老师
    :param conn:
    :param cursor:
    :return:
    """

    teacher = {}

    try:
        cursor.execute("""
            SELECT cc.id,up.nick_name from mz_course_course as cc
            INNER JOIN mz_user_userprofile as up ON up.id = cc.teacher_id
        """)

        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    for res in res_list:
        teacher[res['id']] = res['nick_name']

    return APIResult(result=teacher)

LIMIT = 64
@dec_timeit("get_course_career_names")
def get_course_career_names(course_id_list):
    """
    获取小课程ID，对应的职业课程名称和小课程下的章节数
    :param course_id_list: 小课程id的list集合
    :return: {'course_id':{}}
    """

    mongodb = get_mongo_db('search_meta')
    if not isinstance(course_id_list, list):
        log.warn('course_id_list is not list object!')
        course_id_list = []
    try:
        career_course_name = mongodb.search_meta.find({'key': {"$in": course_id_list[:LIMIT]}})

    except Exception as e:
        log.warn(
            'get course career names from mongodb failed!'
            'course_id_list: %s' % course_id_list
        )
        raise e

    return APIResult(result=career_course_name)


@dec_timeit("get_wiki_course_meta")
def get_wiki_course_meta(course_id_list):
    """
    获取wiki课程名称
    :param course_id_list: wiki的course_id的list集合
    :return: {'course_id':{}}
    """
    mongodb = get_mongo_db('search_meta')
    if not isinstance(course_id_list, list):
        log.warn('course_id_list is not list object!')
        course_id_list = []
    try:
        wiki_course = mongodb.search_meta.find({'key': {"$in": course_id_list[:LIMIT]}})

    except Exception as e:
        log.warn(
            'get wiki course from mongodb failed!'
            'course_id_list: %s' % course_id_list
        )
        raise e

    return APIResult(result=wiki_course)


@dec_timeit("get_article_tags")
def get_article_tags(article_id_list):
    """
    获取课程tag
    :param article_id_list: article_id的list集合
    :return: {'course_id':{}}
    """

    mongodb = get_mongo_db('search_meta')
    if not isinstance(article_id_list, list):
        log.warn('article_id_list is not list object!')
        article_id_list = []
    try:
        article_tag = mongodb.search_meta.find({'key': {"$in": article_id_list[:LIMIT]}})

    except Exception as e:
        log.warn(
            'get article tag from mongodb failed!'
            'course_id_list: %s' % article_id_list
        )
        raise e

    return APIResult(result=article_tag)


@dec_timeit("make_course_career_infos")
@dec_make_conn_cursor
def get_course_career_infos(conn, cursor):
    """
    """

    try:
        cursor.execute("""
                        SELECT cco.obj_id as course_id,
                               ccc.id,
                               ccc.name,
                               ccc.short_name,
                               ccc.image,
                               cp.short_info,
                               ccc.description,
                               cp.student_count
                        FROM mz_common_careerobjrelation AS cco
                        LEFT JOIN mz_career_page AS cp
                        ON cp.id=cco.career_id
                        LEFT JOIN mz_course_careercourse AS ccc
                        ON ccc.id=cco.career_id
                        WHERE cco.obj_type="COURSE";
                  """)
        res_list = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s.'
            'statement: %s' % (e, cursor._last_executed)
        )
        raise e

    return APIResult(result=res_list)
