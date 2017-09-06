# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_course_ad_list(conn, cursor, page_index=1, page_size=10, img_title=None):
    """
    小课程介绍页广告列表
    :param conn:
    :param cursor:
    :param page_index: 第几页
    :param page_size: 每页多少条
    :param img_title: 广告描述
    :return: course广告列表
    """

    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
        SELECT
            {fields}
        FROM
            mz_common_careerad AS ad
        INNER JOIN mz_course_careercourse AS cc ON cc.id = ad.career_id

    """

    base_wheres = []
    if img_title:
        base_sql += ' AND ad.img_title LIKE %s '
        img_title = '%' + str(img_title) + '%'
        base_wheres.append(img_title)

    sql = base_sql.format(fields='ad.id, cc.`name` AS career_name, ad.img_url,'
                                 'ad.img_title, ad.is_actived, ad.url, ad.`type` AS ad_type,'
                                 'ad.career_id, cc.short_name')
    count_sql = base_sql.format(fields='COUNT(ad.id) as count')

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
        result=dict(course_ad_list=result,
                    page=dict(rows_count=rows_count, page_count=page_count,
                              page_size=page_size, page_index=page_index))
    )


@dec_make_conn_cursor
@dec_timeit
def get_course_ad(conn, cursor, ad_id):
    """
    course广告详情
    :param conn:
    :param cursor:
    :param ad_id: wiki广告id
    :return: course广告详情
    """

    sql = """
        SELECT
            ad.id,
            cc.`name` AS career_name,
            ad.img_url,
            ad.img_title,
            ad.is_actived,
            ad.career_id,
            ad.url,
            ad.`type`,
            cc.short_name
        FROM
            mz_common_careerad AS ad
        INNER JOIN mz_course_careercourse AS cc ON cc.id = ad.career_id
        WHERE
            ad.id = %s
    """

    try:
        cursor.execute(sql, (ad_id,))
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
def get_career_courses(conn, cursor, is_all=True):
    """
    获取未添加广告的wiki分类
    :param conn:
    :param cursor:
    :param is_all: 是否获取全部wiki分类，False表示只获取未添加过广告的wiki分类
    :return: 未添加广告的wiki分类列表
    """

    base_sql = """
        SELECT
            id,
            `name`
        FROM
            mz_course_careercourse
        {where}
    """

    if is_all:
        sql = base_sql.format(where='')
    else:
        sql = base_sql.format(
            where='''
              WHERE
                id NOT IN (
                    SELECT
                        career_id
                    FROM
                        mz_common_careerad
                )'''
        )

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
@dec_timeit
def add_course_ad(conn, cursor, img_url, url, img_title, career_id, type):
    """
    新增小课程广告
    :param conn:
    :param cursor:
    :param img_url: 图片地址
    :param url: 跳转url
    :param img_title: 图片描述
    :param career_id: 职业课程id
    :return: True or False
    """

    sql = """
        INSERT INTO mz_common_careerad (
            `type`,
            is_actived,
            img_url,
            url,
            img_title,
            career_id
        )
        VALUES (%s, 1, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (type, img_url, url, img_title, career_id))
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
def update_course_ad(conn, cursor, ad_id, img_url, url, img_title, career_id, is_actived, type):
    """
    更新course广告
    :param conn:
    :param cursor:
    :param ad_id: id
    :param img_url: 图片地址
    :param url: 跳转url
    :param img_title: 图片描述
    :param career_id: 职业课程id
    :return: True or False
    """

    sql = """
        UPDATE mz_common_careerad
        SET img_url = %s,
         url = %s,
         img_title = %s,
         career_id = %s,
         is_actived = %s,
         `type` = %s
        WHERE id = %s
    """

    try:
        cursor.execute(sql, (img_url, url, img_title, career_id, is_actived, type, ad_id))
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
def update_course_ad_status(conn, cursor, ad_id, is_actived):
    """
    更新course广告
    :param conn:
    :param cursor:
    :param ad_id: id
    :param is_actived: 广告是否启用，1表示启用
    :return: True or False
    """

    sql = """
        UPDATE mz_common_careerad
        SET is_actived = %s
        WHERE id = %s
    """

    try:
        cursor.execute(sql, (is_actived, ad_id))
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
def del_course_ad(conn, cursor, ad_id):
    """
    删除小课程广告
    :param conn:
    :param cursor:
    :param ad_id: id
    :return: True or False
    """

    sql = """
        DELETE FROM mz_common_careerad WHERE id = %s
    """

    try:
        cursor.execute(sql, (ad_id,))
        conn.commit()
        log.info("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


