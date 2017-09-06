# -*- coding:utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_make_conn_cursor, dec_get_cache


def get_career_course_info(career_short_name):
    redis_key = 'career_course_info_of_%s' % career_short_name

    @dec_timeit("get_career_course_info")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        获取职业课程相关数据
        :param conn:
        :param cursor:
        :return:
        """
        sql = """
            SELECT cc.id,cc.enable_free_488,cc.name,cc.seo_title_px,
                   cc.seo_keyword_px,cc.seo_description_px,
                   cc.course_color_px, cc.image_px, cc.student_count, cc.description,
                   cc.seo_title, cc.seo_keyword, cc.seo_description
            FROM mz_course_careercourse AS cc
            where cc.short_name=%s
            """
        try:
            cursor.execute(sql, (career_short_name,))
            result = cursor.fetchone()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)
    return main(_enable_cache=True)


@dec_timeit("user_class_type")
@dec_make_conn_cursor
def user_class_type(conn, cursor, user_id, career_id):
    """
    判断用户是否报名该职业课程下某班级类型的班级
    :param class_type: 班级类型  0: 正常付费班级 3：488免费试学班
    :param career_id: 职业课程ID
    :return:
    """
    sql = """
        SELECT cs.id, cs.deadline, cs.student_class_id FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON c.id=cs.student_class_id
        WHERE
        c.class_type=0 AND cs.status=1 AND cs.user_id=%s AND c.career_course_id=%s
        LIMIT 1
        """
    sql1 = """
        SELECT cs.student_class_id FROM mz_lps_classstudents AS cs
        INNER JOIN mz_lps_class AS c ON c.id=cs.student_class_id
        WHERE
        c.class_type=3 AND cs.status=1 AND cs.user_id=%s AND c.career_course_id=%s
        LIMIT 1
        """
    try:
        is_pay = False
        is_full_paid = True
        is_488_free = False
        class_id = None
        sql = sql % (user_id, career_id)
        cursor.execute(sql)
        sql_result = cursor.fetchone()
        if sql_result:
            is_pay = True
            class_id = sql_result['student_class_id']
            if sql_result['deadline']:
                is_full_paid = False
        else:
            sql1 = sql1 % (user_id, career_id)
            cursor.execute(sql1)
            sql1_result = cursor.fetchone()
            if sql1_result:
                is_488_free = True
                class_id = sql1_result['student_class_id']
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    result = {'is_normal_class': is_pay,
              'is_full_paid': is_full_paid,
              'is_488_free_class': is_488_free,
              'class_id': class_id,
              }
    return APIResult(result=result)


def get_career_intro(career_id):
    redis_key = 'get_career_intro%s' % career_id

    @dec_timeit("get_career_intro")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        获取职业课程新的介绍页相关数据
        :param career_id:
        :return:
        """
        sql = """
            SELECT cp.*,cc.net_price FROM mz_career_page AS cp
            INNER JOIN mz_course_careercourse AS cc ON cc.id=%s
            WHERE cp.id=%s
            """ % (career_id, career_id)
        sql1 = """
            SELECT pt.big_img_url,pt.info,pt.name,pt.teacher_id,pt.title,u.avatar_url FROM mz_career_page_teacher AS pt
            INNER JOIN mz_user_userprofile AS u ON u.id=pt.teacher_id
            WHERE career_id=%s
            """ % career_id
        sql2 = """
            SELECT * FROM mz_career_page_student WHERE career_id=%s
            """ % career_id
        sql3 = """
            SELECT * FROM mz_career_page_enterprise WHERE career_id=%s LIMIT 3
            """ % career_id
        sql4 = """
            SELECT * FROM mz_career_page_duty WHERE career_id=%s LIMIT 2
            """ % career_id

        try:

            cursor.execute(sql)
            sql_result = cursor.fetchone()

            cursor.execute(sql1)
            sql_result1 = cursor.fetchall()

            cursor.execute(sql2)
            sql_result2 = cursor.fetchall()

            cursor.execute(sql3)
            sql_result3 = cursor.fetchall()

            cursor.execute(sql4)
            sql_result4 = cursor.fetchall()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        result = {'page_intro': sql_result,
                  'teachers': sql_result1,
                  'students': sql_result2,
                  'enterprises': sql_result3,
                  'duties': sql_result4}
        # set cache
        cache.set(redis_key, result, 60 * 5)

        return APIResult(result=result)

    return main(_enable_cache=True)


def get_career_intro_discuss(discuss_ids):
    redis_key = 'get_career_intro_discuss%s' % '-'.join(discuss_ids)

    @dec_timeit("get_career_intro_discuss")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        获取职业课程新介绍页下的视频评论及最早的一个子评论
        :param conn:
        :param cursor:
        :param discuss_ids: 父评论ID列表
        :return:
        """
        sql = """
            SELECT parent.object_id,
                   parent.comment,
                   parent.create_date,
                   parent.head,
                   parent.nick_name,
                   parent.user_id,
                   parent.id,
                   child.comment AS child_comment,
                   child.create_date AS child_create_date,
                   child.head AS child_head,
                   child.nick_name AS child_nick_name,
                   child.user_id AS child_user_id,
                   lesson.name,
                   lesson.course_id
            FROM mz_common_newdiscuss AS parent
            INNER JOIN mz_common_newdiscuss AS  child ON child.parent_id = parent.id
            INNER JOIN mz_course_lesson AS lesson ON lesson.id = parent.object_id
            WHERE parent.id=%s  LIMIT 1
            """
        discuss_list = []
        try:
            for discuss_id in discuss_ids:
                _sql = sql % discuss_id
                cursor.execute(_sql)
                result = cursor.fetchone()
                if result:
                    discuss_list.append(result)
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, discuss_list, 60 * 5)
        return APIResult(result=discuss_list)
    return main(_enable_cache=True)


def get_career_intro_tech_article(career_id):
    redis_key = 'get_career_intro_tech_article%s' % career_id

    @dec_timeit("get_career_intro_tech_article")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        职业课程新介绍页相关文章
        :param conn:
        :param cursor:
        :param career_id:
        :return:
        """
        sql = """
            SELECT  article.id,
                    article.title,
                    article.abstract,
                    article.publish_date,
                    article.content,
                    article.praise_count,
                    article.replay_count,
                    article.view_count,
                    article.user_id,
                    article.user_head,
                    article.nick_name,
                    article.title_image1,
                    article.title_image2,
                    article.title_image3,
                    article.is_top,
                    articletype.name,
                    articletype.short_name,
            GROUP_CONCAT(t.id,'_',t.name) AS tag
            FROM mz_common_newarticle AS article
            INNER JOIN mz_common_careerobjrelation AS obj ON obj.career_id = %s AND obj.obj_type='ARTICLE'
            AND  article.id=obj.obj_id AND article.is_career=1
            INNER join mz_common_articletype AS articletype ON articletype.id = article.article_type_id
            LEFT JOIN mz_common_objtagrelation AS otr ON article.id = otr.obj_id AND otr.obj_type = 'ARTICLE'
            LEFT JOIN mz_course_tag AS t ON otr.tag_id = t.id
            GROUP BY article.id
            order by article.is_top DESC,article.id DESC
            limit 0,3
            """ % career_id
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)
    return main(_enable_cache=True)


def get_career_intro_student_article(career_id):
    redis_key = 'get_career_intro_student_article%s' % career_id

    @dec_timeit("get_career_intro_student_article")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        职业课程新介绍页相关作品
        :param conn:
        :param cursor:
        :param career_id:
        :return:
        """
        sql = """
            SELECT  article.id,
                    article.title,
                    article.title_image,
                    article.user_id,
                    article.user_head,
                    article.nick_name,
                    article.praise_count,
                    article.replay_count,
                    article.view_count,
                    articletype.name,
                    articletype.short_name
            FROM mz_common_newarticle AS article
            INNER JOIN mz_common_careerobjrelation AS obj ON obj.career_id = %s AND obj.obj_type='ARTICLE'
            AND  article.id=obj.obj_id AND article.article_type_id = 100
            INNER join mz_common_articletype AS articletype ON article.article_type_id = articletype.id
            order by article.is_top DESC,article.id DESC
            limit 0,6
        """ % career_id
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, result, 60 * 5)
        return APIResult(result=result)
    return main(_enable_cache=True)


@dec_timeit("free_class_start_time")
@dec_make_conn_cursor
def free_class_start_time(conn, cursor, career_id):
    """
    获取免488班级最近开课时间
    :param conn:
    :param cursor:
    :param career_id:
    :return:
    """
    sql = """
        SELECT c_m.startline AS startline
        FROM mz_lps3_classmeeting AS c_m
        LEFT JOIN mz_lps3_classmeetingrelation AS c_m_rel ON c_m_rel.class_meeting_id = c_m.id
        LEFT JOIN mz_lps_class AS _class ON _class.id = c_m_rel.class_id
        WHERE _class.class_type=3
        AND _class.lps_version=3.0
        AND _class.career_course_id=%s
        AND c_m.status=0
        AND c_m.content='首次班会'
        ORDER BY c_m.startline
        LIMIT 1
        """ % career_id
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("get_career_teachers")
@dec_make_conn_cursor
def get_career_teachers(conn, cursor):

    sql = """
        SELECT cpt.teacher_id,
               cpt.name,
               cpt.title,
               cpt.info,
               cpt.career_id,
               uup.avatar_url
        FROM mz_career_page_teacher AS cpt
        LEFT JOIN mz_user_userprofile AS uup
        ON uup.id=cpt.teacher_id
        """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)
