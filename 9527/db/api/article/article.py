# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor






@dec_timeit
@dec_make_conn_cursor
def insert_Article(conn, cursor, title, sub_title, content, abstract, title_image, user_id, nick_name, user_head,
                   publish_date, article_type_id, is_top, retrieval):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_common_newarticle (title,sub_title, content,abstract,title_image,user_id,nick_name,user_head,publish_date,
                article_type_id,is_top,tidy_content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (title, sub_title, content, abstract, title_image, user_id, nick_name, user_head, publish_date,
                  article_type_id, is_top, retrieval))
        cursor.execute(
            """
                select last_insert_id() as mz_common_newarticle_id;
            """)
        newArticle_id = cursor.fetchone()["mz_common_newarticle_id"]
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=newArticle_id)


@dec_timeit
@dec_make_conn_cursor
def update_Article(conn, cursor, _id, title, sub_title, content, abstract, title_image, article_type_id, is_top, retrieval):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                  UPDATE mz_common_newarticle set title=%s,sub_title=%s,content=%s,abstract=%s,title_image=%s,
                  article_type_id=%s,is_top=%s,tidy_content=%s WHERE id = %s;
            """, (title, sub_title, content, abstract, title_image, article_type_id, is_top, retrieval, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_pic(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT title_image1,title_image2,title_image3,id,title
                FROM mz_common_newarticle
                WHERE id = %s;
            """, (_id,))
        article = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=article)


@dec_timeit
@dec_make_conn_cursor
def article_likeinfo(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT view_count AS `view`, praise_count AS praise FROM mz_common_newarticle WHERE id = %s
            """, (_id,))
        article = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=article)


@dec_timeit
@dec_make_conn_cursor
def article_chginfo(conn, cursor, _id, view, praise):
    """
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_newarticle SET view_count = %s, praise_count = %s WHERE id = %s
            """, (view, praise, _id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_Articletitleimg(conn, cursor, _id, title_imageone, title_imagetwo, title_imagethree):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_newarticle SET title_image1=%s,title_image2=%s,title_image3=%s WHERE id=%s;
            """, (title_imageone, title_imagetwo, title_imagethree, _id))
        # cursor.execute(
        #     """
        #         select last_insert_id() as mz_common_newarticle_id;
        #     """)
        # newArticle_id = cursor.fetchone()["mz_common_newarticle_id"]
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)  # newArticle_id


@dec_timeit
@dec_make_conn_cursor
def get_userprofileinfo_by_id(conn, cursor, user_id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT nick_name,avatar_small_thumbnall
                FROM mz_user_userprofile
                WHERE id=%s
            """, (user_id,))
        Article = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=Article)


@dec_timeit
@dec_make_conn_cursor
def delete_Article(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_newarticle WHERE id=%s;
            """, (_id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_Article(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT content,abstract,title_image,user_id,publish_date,article_type_id,is_top
                FROM mz_common_newarticle
            """)
        article = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=article)


@dec_timeit
@dec_make_conn_cursor
def list_Article_by_page(conn, cursor, title, article_type_id, career_course_id, sort, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
                SELECT {fields}
    FROM   mz_common_newarticle AS newart
    LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
    LEFT JOIN mz_common_careerobjrelation AS cor ON cor.obj_id = newart.id
    AND cor.obj_type = 'ARTICLE'
    LEFT JOIN mz_course_careercourse AS cr ON cor.career_id = cr.id
    WHERE 1=1
            """
    base_param = []
    if title:
        base_sql += ' AND newart.title LIKE  %s'
        title = '%' + title + '%'
        base_param.append(title)
    if article_type_id != 0:
        base_sql += ' AND newart.article_type_id= %s'
        base_param.append(article_type_id)
    if career_course_id != 0:
        base_sql += ' AND cor.career_id=%s'
        base_param.append(career_course_id)
    # sort==1 显示为ID排序，实现是用发布时间倒序排序
    if sort == 1:
        base_sql += ' ORDER BY newart.publish_date DESC'
    if sort == 2:
        base_sql += ' ORDER BY newart.praise_count DESC'
    if sort == 3:
        base_sql += ' ORDER BY newart.view_count DESC'

    sql = base_sql.format(fields="""newart.id,
        newart.title,
        newart.sub_title,
        newart.praise_count,
        newart.view_count,
        newart.nick_name,
        newart.publish_date,
        newart.is_career,
        arttype. NAME AS articletype_name,
        cr.`name` AS careerCourse_name""")
    count_sql = base_sql.format(fields='count(newart.id) as count')
    sql_param = base_param[:]
    sql += ' LIMIT %s,%s'
    sql_param.extend([start_index, page_size])

    try:
        cursor.execute(sql, sql_param)
        article = cursor.fetchall()
        log.info('query:%s' % cursor.statement)

        cursor.execute(count_sql, base_param)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
        log.info('query:%s' % cursor.statement)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_id(conn, cursor, _id):
    """
    """
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.nick_name AS user_nick_name
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.id = %s
            """, (_id,))
        Article = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        print e
        raise e

    return APIResult(result=Article)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s
            GROUP BY newart.id
            ORDER BY newart.id DESC
            limit %s,%s
            """, (title, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_articletype(conn, cursor, title, article_type, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s AND article_type_id = %s
            GROUP BY newart.id
            ORDER BY newart.id DESC
            limit %s,%s
            """, (title, article_type, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s AND article_type_id = %s
            """, (title, article_type))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_articletype_praise_count(conn, cursor, title, article_type, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s AND article_type_id = %s
            GROUP BY newart.id
            ORDER BY praise_count DESC
            limit %s,%s
            """, (title, article_type, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s AND article_type_id = %s
            """, (title, article_type))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_articletype_view_count(conn, cursor, title, article_type, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s AND article_type_id = %s
            GROUP BY newart.id
            ORDER BY view_count DESC
            limit %s,%s
            """, (title, article_type, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s AND article_type_id = %s
            """, (title, article_type))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_praise_count(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s
            GROUP BY newart.id
            ORDER BY praise_count DESC
            limit %s,%s
            """, (title, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_view_count(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s
            GROUP BY newart.id
            ORDER BY view_count DESC
            limit %s,%s
            """, (title, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_articletype_publish_date(conn, cursor, title, article_type, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s AND article_type_id = %s
            GROUP BY newart.id
            ORDER BY publish_date DESC
            limit %s,%s
            """, (title, article_type, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s AND article_type_id = %s
            """, (title, article_type))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def get_Article_by_title_publish_date(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
            newart.*,
            objseo.seo_title,
            objseo.seo_keywords,
            objseo.seo_description,
            tag. NAME AS tag_name,
            course. NAME AS course_name,
            arttype. NAME AS articletype_name,
            userpf.username AS username
            FROM   mz_common_newarticle AS newart
            LEFT JOIN mz_common_objseo AS objseo ON objseo.obj_type = 'ARTICLE'
            AND newart.id = objseo.obj_id
            LEFT JOIN mz_common_objtagrelation AS obtr ON obtr.obj_type = 'ARTICLE'
            AND newart.id = obtr.obj_id
            LEFT JOIN mz_course_tag AS tag ON obtr.tag_id = tag.id
            LEFT JOIN mz_common_careerobjrelation AS objcr ON newart.id = objcr.obj_id
            LEFT JOIN mz_course_careercourse AS course ON objcr.obj_type = 'ARTICLE'
            AND objcr.career_id = course.id
            LEFT JOIN mz_common_articletype AS arttype ON newart.article_type_id = arttype.id
            LEFT JOIN mz_user_userprofile AS userpf ON newart.user_id = userpf.id
            WHERE newart.title LIKE %s
            GROUP BY newart.id
            ORDER BY publish_date DESC
            limit %s,%s
            """, (title, start_index, page_size))
        article = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newarticle WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": article,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=article_dict)


@dec_timeit
@dec_make_conn_cursor
def checked_param(conn, cursor, chkid):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_newarticle SET is_career = 1 WHERE id = %s
            """, (chkid,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def check_param(conn, cursor, chkedid):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_newarticle SET is_career = 0 WHERE id = %s
            """, (chkedid,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=chkedid)
