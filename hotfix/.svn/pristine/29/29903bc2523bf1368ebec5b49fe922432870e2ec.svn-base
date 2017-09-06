# -*- coding: utf-8 -*-
"""
@time: 2016/7/6 0006 14:57
@note:  问答
"""
import json
import datetime

from django.core.urlresolvers import reverse
from db.api.apiutils import dec_get_cache, dec_make_conn_cursor, APIResult
from db.cores.cache import cache
from utils.logger import logger


def _handling_discuss_data(discuss_dict, luser_id=None):
    """
    处理SQL查询出讨论数据
    :param discuss_dict: 讨论数据的字典（值传递）
    :param user_id: 当前登录的用户 id 课程库用
    :return:
    """
    small_materials = discuss_dict['materials']
    real_materials = discuss_dict['real_materials']
    _small_materials = small_materials.split(',') if small_materials else []
    _real_materials = real_materials.split(',') if real_materials else []
    len_materials = max(len(_small_materials), len(_real_materials))
    _materials = [''] * len_materials
    small_materials = _small_materials or _materials
    real_materials = _real_materials or _materials
    discuss_dict['materials'] = zip(real_materials, small_materials)
    # 数据处理
    discuss_dict['object_content'] = discuss_dict['object_content'] or ''
    # 时间处理
    discuss_dict['problem_date'] = ''
    discuss_dict['problem_time'] = ''
    if isinstance(discuss_dict['create_date'], datetime.datetime):
        discuss_dict['problem_date'] = discuss_dict['create_date'].strftime('%Y-%m-%d')
        discuss_dict['problem_time'] = discuss_dict['create_date'].strftime('%H:%M')
    # 位置链接
    object_location = discuss_dict.get('object_location')
    if object_location:
        dic_location = json.loads(object_location)
        if dic_location.has_key('lps'):
            discuss_dict['object_href'] = reverse('lps3:student_knowledgeitem', args=dic_location['lps'])+\
                                          '?p_id=%s'%discuss_dict['id']
        if dic_location.has_key('course'):
            discuss_dict['object_href'] = reverse('course:lesson_video_view', args=dic_location['course'])+\
                                          '?p_id=%s'%discuss_dict['id']
    # 用户group_name
    if not is_normal_class_user(discuss_dict['user_id']).result():
        discuss_dict['group_name'] = None
    if luser_id:
        discuss_dict['is_praise'] = is_praise_problem(luser_id, discuss_dict['id']).result()
    else:
        discuss_dict['is_praise'] = False

    discuss_dict['child_post_list'] = get_all_child_post(discuss_dict['id'])
    discuss_dict['child_post_count'] = len(discuss_dict['child_post_list'])

    if discuss_dict['child_post_list']:
        for cp in discuss_dict['child_post_list']:
            _handling_child_discuss_data(cp, luser_id)


def _handling_child_discuss_data(discuss_dict, luser_id):
    # 用户group_name
    if not is_normal_class_user(discuss_dict['user_id']).result():
        discuss_dict['group_name'] = None
    if luser_id:
        discuss_dict['is_praise'] = is_praise_problem(luser_id, discuss_dict['id']).result()
    else:
        discuss_dict['is_praise'] = False


def get_all_child_post(discuss_id):
    """
    获取问题下的所有回答
    :param discuss_id:
    :return:
    """
    # TODO 取消函数内部import
    import db.api.common.new_discuss_post

    # 获取第一级回答
    first_answers = db.api.common.new_discuss_post.get_one_question_first_level_answer_of_one_project_id(
        discuss_id, -1, 0)
    if first_answers.is_error():
        logger.warn('get_one_question_first_level_answer_of_one_project_id is error. '
                    'discuss_id: %s' % discuss_id)
        first_answers = []
    else:
        first_answers = first_answers.result()

    id_list = [a['id'] for a in first_answers]

    first_answers = list(first_answers)

    # 获取第二级回答
    if id_list:
        second_answers = db.api.common.new_discuss_post.get_one_question_second_level_answer_of_one_project_id(id_list)
        if second_answers.is_error():
            logger.warn('get_one_question_second_level_answer_of_one_project_id is error. '
                        'discuss_id: %s' % discuss_id)
            second_answers = []
        else:
            second_answers = second_answers.result()

        first_answers.extend(list(second_answers))

    first_answers.sort(key=lambda x: x['create_date'])

    return first_answers


def get_my_problem_list_by_user_id(user_id, status=None, end_id=0, page_size=20):
    """
    根据我的获取提问List
    :param user_id:
    :param status: None:所有状态,1：未读；2:已读; 3:未回复；4：已经回复（int）
    :param end_id: 前一页结束ID
    :param page_size: 每页条数(int)
    :return:
    """

    cache_key = 'get_my_problem_list_by_user_id_%s_%s_%s_%s' % (user_id, status, end_id, page_size)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        # 处理状态
        try:
            #更加最后的返还的ID加载数据
            end_str = ''
            if end_id > 0:
                end_str = 'AND newdiscuss.id<%s' % end_id
            if status:
                end_str += """ AND userstatus.status=%s""" % status
        except Exception, e:
            logger.warn(e)
            raise e
        sql = """
        SELECT
            newdiscuss.id,
            newdiscuss.object_id,
            newdiscuss.object_type,
            newdiscuss.object_content,
            newdiscuss.object_name,
            newdiscuss.object_location,
            newdiscuss.comment,
            newdiscuss.user_id,
            newdiscuss.nick_name,
            newdiscuss.head,
            newdiscuss.group_name,
            newdiscuss.create_date,
            userstatus.status,
            newdiscuss.discuss_count,
            newdiscuss.user_praise_count,
            GROUP_CONCAT(material.small_material) AS materials,
            GROUP_CONCAT(material.material) AS real_materials,
            newdiscuss_child.id as child_id,
            newdiscuss_child.comment as child_comment,
            newdiscuss_child.user_id as child_user_id,
            newdiscuss_child.nick_name as child_nick_name,
            newdiscuss_child.head as child_head ,
            newdiscuss_child.group_name as child_group_name,
            newdiscuss_child.create_date as child_create_date

        FROM mz_common_newdiscuss as newdiscuss
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id
        LEFT JOIN mz_common_newdiscuss as newdiscuss_child ON newdiscuss.last_answer_id=newdiscuss_child.id
        LEFT JOIN mz_common_newdiscussuserstatus as userstatus ON (
            newdiscuss.id=userstatus.new_discuss_id
            AND newdiscuss.user_id=userstatus.user_id)
        WHERE newdiscuss.object_type != 'ARTICLE' AND newdiscuss.user_id=%s AND newdiscuss.parent_id=0 """+end_str+"""
        GROUP BY newdiscuss.id
        ORDER BY newdiscuss.create_date DESC
        LIMIT %s
        """
        try:
            cursor.execute(sql, (user_id, page_size))
            discuss_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
            for discuss_dict in discuss_list:
                _handling_discuss_data(discuss_dict, user_id)

        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, discuss_list)
        return APIResult(result=discuss_list)

    return main(_enable_cache=True)


def get_my_answer_list_by_user_id(user_id, status=None, end_id=0, page_size=20):
    """
    根据我的的回复获取提问List
    :param user_id:
    :param end_id: 前一页结束ID
    :param page_size: 每页条数(int)
    :return:
    """
    cache_key = 'get_my_answer_list_by_user_id_%s_%s_%s_%s' % (user_id, status, end_id, page_size)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        # 处理状态
        try:
            # 更加最后的返还的ID加载数据
            end_str = ''
            if end_id > 0:
                end_str = 'AND newdiscuss.id<%s' % end_id

            if status:
                end_str += """ AND userstatus.status=%s""" % status

        except Exception, e:
            logger.warn(e)
            raise e

        sql = """
        SELECT
            newdiscuss.id,
            newdiscuss.object_id,
            newdiscuss.object_type,
            newdiscuss.object_content,
            newdiscuss.object_name,
            newdiscuss.object_location,
            newdiscuss.comment,
            newdiscuss.user_id,
            newdiscuss.nick_name,
            newdiscuss.head,
            newdiscuss.group_name,
            newdiscuss.create_date,
            userstatus.`status`,
            newdiscuss.discuss_count,
            newdiscuss.user_praise_count,
            GROUP_CONCAT(material.small_material) AS materials,
            GROUP_CONCAT(material.material) AS real_materials,
            newdiscuss_child.id as child_id,
            newdiscuss_child.comment as child_comment,
            newdiscuss_child.user_id as child_user_id,
            newdiscuss_child.nick_name as child_nick_name,
            newdiscuss_child.head as child_head ,
            newdiscuss_child.group_name as child_group_name,
            newdiscuss_child.create_date as child_create_date
        FROM mz_common_newdiscuss as newdiscuss_child
        INNER JOIN
        (
        SELECT
            MAX(create_date) as create_date,
            problem_id
        FROM mz_common_newdiscuss
        WHERE user_id=@user_id AND parent_id!=0
        GROUP BY problem_id
        ) as a ON newdiscuss_child.problem_id=a.problem_id AND a.create_date=newdiscuss_child.create_date
        LEFT JOIN mz_common_newdiscuss as newdiscuss ON newdiscuss.id=newdiscuss_child.problem_id
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id
        LEFT JOIN mz_common_newdiscussuserstatus as userstatus ON (
                            newdiscuss.id=userstatus.new_discuss_id
                            AND userstatus.user_id=@user_id)
        WHERE newdiscuss.object_type != 'ARTICLE' AND newdiscuss.user_id != @user_id """+end_str+"""
        GROUP BY newdiscuss.id
        ORDER BY newdiscuss.create_date DESC
        LIMIT %s
        """
        try:
            cursor.execute("SET @user_id=%s;", (user_id,))
            cursor.execute(sql, (page_size,))
            discuss_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
            for discuss_dict in discuss_list:
                _handling_discuss_data(discuss_dict, user_id)

        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, discuss_list)
        return APIResult(result=discuss_list)

    return main(_enable_cache=True)


def get_ta_problem_list_by_user_id(user_id, cur_user_id, end_id=0, page_size=20):
    """
    根据TA的用户ID获取提问List
    :param user_id:
    :param cur_user_id: 当前登录用户id，获取当前用户是否点赞
    :param end_id: 前一页结束ID
    :param page_size: 每页条数(int)
    :return:
    """
    cache_key = 'get_ta_problem_list_by_user_id_%s_%s_%s' % (user_id, end_id, page_size)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        # 更加最后的返还的ID加载数据
        end_str = ''
        if end_id > 0:
            end_str = 'AND newdiscuss.id<%s' % end_id
        sql = """
        SELECT
            newdiscuss.id,
            newdiscuss.object_id,
            newdiscuss.object_type,
            newdiscuss.object_content,
            newdiscuss.object_name,
            newdiscuss.object_location,
            newdiscuss.comment,
            newdiscuss.user_id,
            newdiscuss.nick_name,
            newdiscuss.head,
            newdiscuss.group_name,
            newdiscuss.create_date,
            newdiscuss.discuss_count,
            newdiscuss.user_praise_count,
            GROUP_CONCAT(material.small_material) AS materials,
            GROUP_CONCAT(material.material) AS real_materials,
            newdiscuss_child.id as child_id,
            newdiscuss_child.comment as child_comment,
            newdiscuss_child.user_id as child_user_id,
            newdiscuss_child.nick_name as child_nick_name,
            newdiscuss_child.head as child_head ,
            newdiscuss_child.group_name as child_group_name,
            newdiscuss_child.create_date as child_create_date

        FROM mz_common_newdiscuss as newdiscuss
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id
        LEFT JOIN mz_common_newdiscuss as newdiscuss_child ON newdiscuss.last_answer_id=newdiscuss_child.id
        WHERE newdiscuss.object_type != 'ARTICLE' AND newdiscuss.user_id=%s AND newdiscuss.parent_id=0 """+end_str+"""
        GROUP BY newdiscuss.id
        ORDER BY newdiscuss.create_date DESC
        LIMIT %s
        """

        try:
            cursor.execute(sql, (user_id, page_size))
            discuss_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
            for discuss_dict in discuss_list:
                _handling_discuss_data(discuss_dict, cur_user_id)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, discuss_list)
        return APIResult(result=discuss_list)

    return main(_enable_cache=True)


def get_ta_answer_list_by_user_id(user_id, cur_user_id, end_id=0, page_size=20):
    """
    根据TA的用户的回复获取提问List
    :param user_id:
    :param end_id: 前一页结束ID
    :param page_size: 每页条数(int)
    :return:
    """
    cache_key = 'get_ta_answer_list_by_user_id_%s_%s_%s' % (user_id, end_id, page_size)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        # 更加最后的返还的ID加载数据
        end_str = ''
        if end_id > 0:
            end_str = 'AND newdiscuss.id<%s' % end_id
        sql = """
        SELECT
            newdiscuss.id,
            newdiscuss.object_id,
            newdiscuss.object_type,
            newdiscuss.object_content,
            newdiscuss.object_name,
            newdiscuss.object_location,
            newdiscuss.comment,
            newdiscuss.user_id,
            newdiscuss.nick_name,
            newdiscuss.head,
            newdiscuss.group_name,
            newdiscuss.create_date,
            newdiscuss.discuss_count,
            newdiscuss.user_praise_count,
            GROUP_CONCAT(material.small_material) AS materials,
            GROUP_CONCAT(material.material) AS real_materials,
            newdiscuss_child.id as child_id,
            newdiscuss_child.comment as child_comment,
            newdiscuss_child.user_id as child_user_id,
            newdiscuss_child.nick_name as child_nick_name,
            newdiscuss_child.head as child_head ,
            newdiscuss_child.group_name as child_group_name,
            newdiscuss_child.create_date as child_create_date
        FROM mz_common_newdiscuss as newdiscuss_child
        INNER JOIN
        (
        SELECT
            MAX(create_date) as create_date,
            problem_id
        FROM mz_common_newdiscuss
        WHERE user_id=@user_id AND parent_id!=0
        GROUP BY problem_id
        ) as a ON newdiscuss_child.problem_id=a.problem_id AND a.create_date=newdiscuss_child.create_date
        LEFT JOIN mz_common_newdiscuss as newdiscuss ON newdiscuss.id=newdiscuss_child.problem_id
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id
        WHERE newdiscuss.object_type != 'ARTICLE' AND newdiscuss.user_id != @user_id """+end_str+"""
        GROUP BY newdiscuss.id
        ORDER BY newdiscuss.create_date DESC
        LIMIT %s
        """

        try:
            cursor.execute("SET @user_id=%s;", (user_id,))
            cursor.execute(sql, (page_size,))
            discuss_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
            for discuss_dict in discuss_list:
                _handling_discuss_data(discuss_dict, cur_user_id)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, discuss_list)
        return APIResult(result=discuss_list)

    return main(_enable_cache=True)


def get_answer_count(problem_id):
    """
    获取回复的数量
    :param problem_id:
    :return:
    """
    cache_key = 'get_answer_count%s' % problem_id

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            count(id)
        FROM mz_common_newdiscuss
        WHERE problem_id=%s
        """

        try:
            cursor.execute(sql, (problem_id,))
            answer_count = cursor.fetchone().get('count(id)', 0)
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        cache.set(cache_key, answer_count)
        return APIResult(result=answer_count)

    return main()


# def get_user_praise_count(problem_id):
#     """
#     获取用户点赞的数量
#     :param problem_id:
#     :return:
#     """
#
#     @dec_make_conn_cursor
#     def main(conn, cursor):
#         sql = """
#         SELECT
#             count(id)
#         FROM mz_common_newdiscussuserpraise
#         WHERE new_discuss_id=%s
#         """
#
#         try:
#             cursor.execute(sql, (problem_id,))
#             user_praise_count = cursor.fetchone().get('count(id)', 0)
#             logger.info("query:%s" % cursor._last_executed)
#         except Exception as e:
#             logger.warn(
#                 "execute exception: %s. "
#                 "statement:%s" % (e, cursor._last_executed))
#             raise e
#
#         return APIResult(result=user_praise_count)
#
#     return main()

def get_user_status_count(user_id, status=1):
    """
    获取用户的状态数
    :param user_id:
    :param status: 1 未读 ；2 已读 2；未回复
    :return:
    """
    cache_key = 'get_user_status_count_%s_%s' % (user_id, status)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            count(id)
        FROM mz_common_newdiscussuserstatus
        WHERE user_id=%s AND status=%s
        """

        try:
            cursor.execute(sql, (user_id, status))
            user_praise_count = cursor.fetchone().get('count(id)', 0)
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, user_praise_count)
        return APIResult(result=user_praise_count)

    return main(_enable_cache=True)

def is_normal_class_user(user_id):
    """
    判断用户是否是正常班级学生
    :param user_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            *
        FROM mz_lps_classstudents as cs,mz_lps_class as c
        WHERE
            cs.user_id=%s AND cs.status=1  AND c.id = cs.student_class_id AND c.class_type=0
        LIMIT 1
        """

        try:
            bool_result = False
            if cursor.execute(sql, (user_id,)) > 0:
                bool_result = True
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=bool_result)

    return main()


def get_student_discuss_list_by_teacher(teacher_id, class_type=0, status=None, end_id=0, page_size=20):
    """
    根据老师获取学生问答
    :param teacher_id:
    :param class_type: {0:企业直通班，1：免费试学班，2：毕业的班，3，普通用户}
    :param status: None:所有状态,1：未读；2:已读; 3:未回复；4：已经回复（int）
    :param end_id: 前一页结束ID
    :param page_size: 每页条数(int)
    :return:
    """
    cache_key = 'get_student_discuss_list_by_teacher_%s_%s_%s_%s_%s' % (teacher_id, class_type,
                                                                        status, end_id, page_size)

    @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        # 处理状态
        try:
            # 更加最后的返还的ID加载数据
            end_str = ''
            if end_id > 0:
                end_str = 'AND newdiscuss.id<%s' % end_id
            if status:
                end_str += ' AND userstatus.status=%s' % status

            class_str = """
            in (SELECT
                DISTINCT cs.user_id
            FROM mz_lps_class as c
            INNER JOIN mz_lps_classstudents as cs ON cs.student_class_id=c.id
            INNER JOIN mz_lps_classteachers as ct ON ct.teacher_class_id=c.id
            WHERE
                c.class_type = %s AND c.status = %s
                AND c.is_active=1 AND c.lps_version=3.0 AND cs.is_pause=0 AND cs.status=1
                AND ct.teacher_id=@user_id
                )
            """
            # 企业直通班
            if class_type == 0:
                class_str = class_str % (0, 1)
            # 免费试学班
            if class_type == 1:
                class_str = class_str % (3, 1)
            # 毕业的班
            if class_type == 2:
                class_str = class_str % (0, 2)
            # 普通用户
            if class_type == 3:
                class_str = """
                not in (SELECT
                    DISTINCT cs.user_id
                FROM mz_lps_class as c
                INNER JOIN mz_lps_classstudents as cs ON cs.student_class_id=c.id
                INNER JOIN mz_lps_classteachers as ct ON ct.teacher_class_id=c.id
                WHERE
                    (c.class_type in (0,3) AND c.status = 1 OR c.class_type=0 AND c.status = 2)
                    AND c.is_active=1 AND c.lps_version=3.0 AND cs.is_pause=0 AND cs.status=1
                    AND ct.teacher_id=@user_id
                    )
                """
        except Exception, e:
            logger.warn(e)
            raise e
        sql = """
        SELECT
            newdiscuss.id,
            newdiscuss.object_id,
            newdiscuss.object_type,
            newdiscuss.object_content,
            newdiscuss.object_name,
            newdiscuss.object_location,
            newdiscuss.comment,
            newdiscuss.user_id,
            newdiscuss.nick_name,
            newdiscuss.head,
            newdiscuss.group_name,
            newdiscuss.create_date,
            GROUP_CONCAT(material.small_material) AS materials,
            GROUP_CONCAT(material.material) AS real_materials,
            newdiscuss.discuss_count,
            newdiscuss.user_praise_count,
            userstatus.status

        FROM mz_common_newdiscuss as newdiscuss
        INNER JOIN mz_common_newdiscussuserstatus as userstatus ON (
            newdiscuss.id=userstatus.new_discuss_id
            AND userstatus.user_id=@user_id)
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id

        WHERE newdiscuss.object_type != 'ARTICLE' AND newdiscuss.parent_id=0
                AND newdiscuss.user_id """+class_str+""" """+end_str+"""
        GROUP BY newdiscuss.id
        ORDER BY newdiscuss.create_date DESC
        LIMIT %s
        """
        try:
            cursor.execute("SET @user_id=%s;", (teacher_id,))
            cursor.execute(sql, (page_size,))
            discuss_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
            for discuss_dict in discuss_list:
                _handling_discuss_data(discuss_dict, teacher_id)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        cache.set(cache_key, discuss_list)
        return APIResult(result=discuss_list)

    return main(_enable_cache=True)


def get_problem_by_id(problem_id, user_id=None):
    """
    获取问题数据
    :param problem_id:
    :param user_id: 当前登录用户id，用于获取当前用户是否点赞
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
                newdiscuss.id,
                newdiscuss.object_id,
                newdiscuss.object_type,
                newdiscuss.object_name,
                newdiscuss.object_content,
                newdiscuss.object_location,
                newdiscuss.comment,
                newdiscuss.user_id,
                newdiscuss.nick_name,
                newdiscuss.head,
                newdiscuss.group_name,
                newdiscuss.create_date,
                newdiscuss.discuss_count,
                newdiscuss.user_praise_count,
                GROUP_CONCAT(material.small_material) AS materials,
                GROUP_CONCAT(material.material) AS real_materials
        FROM
             mz_common_newdiscuss as newdiscuss
        LEFT JOIN mz_common_newdiscussmaterial as material ON newdiscuss.id=material.new_discuss_id
        WHERE newdiscuss.id=%s
        """

        try:
            cursor.execute(sql, (problem_id,))
            discuss_dict = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)

            _handling_discuss_data(discuss_dict, user_id)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=discuss_dict)

    return main()


def get_new_discuss_last_answer(problem_id):
    """
    获取问答的最后回复的child_group_name
    :param problem_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            newdiscuss_child.group_name as child_group_name
        FROM mz_common_newdiscuss as newdiscuss
        INNER  JOIN mz_common_newdiscuss as newdiscuss_child ON newdiscuss.last_answer_id=newdiscuss_child.id
        WHERE newdiscuss.id=%s
        """

        try:
            cursor.execute(sql, (problem_id,))
            child_group_name = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=child_group_name)

    return main()


@dec_make_conn_cursor
def is_praise_problem(conn, cursor, user_id, problem_id):
    """
    用户是否给某问题点过赞
    :param conn:
    :param cursor:
    :param user_id: 用户id
    :param problem_id:  问题id
    :return:
    """

    sql = """
        SELECT
            COUNT(id) as praise_count
        FROM
            mz_common_newdiscussuserpraise
        WHERE
            user_id = % s
        AND new_discuss_id = % s
    """

    try:
        cursor.execute(sql, (user_id, problem_id))
        result = cursor.fetchone()['praise_count']
        logger.info("query: %s" % cursor._last_executed)
    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=bool(result))


def add_user_praise(user_id, problem_id):
    """
    添加用户点赞信息
    :param user_id:
    :param problem_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            INSERT INTO mz_common_newdiscussuserpraise(
              user_id,
              new_discuss_id
            )VALUES (%s,%s)
        """
        up_sql = """
            UPDATE mz_common_newdiscuss
            SET user_praise_count = user_praise_count + 1
            WHERE
                id = %s
        """
        sel_sql = """
            SELECT
                user_praise_count
            FROM
                mz_common_newdiscuss
            WHERE id = %s
        """

        try:
            conn.begin()
            res = cursor.execute(sql, (user_id, problem_id))
            if res:
                cursor.execute(up_sql, (problem_id,))
                conn.commit()
            else:
                conn.rollback()
            # 获取当前点赞次数
            cursor.execute(sel_sql, (problem_id,))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            conn.rollback()
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def del_user_praise(user_id, problem_id):
    """
    删除用户点赞信息
    :param user_id:
    :param problem_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            DELETE
            FROM
                mz_common_newdiscussuserpraise
            WHERE
                user_id = %s
            AND new_discuss_id = %s
        """
        up_sql = """
            UPDATE mz_common_newdiscuss
            SET user_praise_count = user_praise_count - 1
            WHERE
                id = %s
        """
        sel_sql = """
            SELECT
                user_praise_count
            FROM
                mz_common_newdiscuss
            WHERE id = %s
        """

        try:
            conn.begin()
            res = cursor.execute(sql, (user_id, problem_id))
            if res:
                cursor.execute(up_sql, (problem_id,))
                conn.commit()
            else:
                conn.rollback()
            # 获取当前点赞次数
            cursor.execute(sel_sql, (problem_id,))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            conn.rollback()
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def add_answer(**kwargs):
    """
    添加回复
    :param answer_dict: 回复的插入内容
    :return:
    """

    def kwargs_get(key):
        return kwargs.get(key, 'Null')

    new_discuss = (
        kwargs_get('object_id'),
        kwargs_get('object_type'),
        kwargs_get('object_content'),
        kwargs_get('object_name'),
        kwargs_get('object_location'),
        kwargs_get('comment'),
        kwargs_get('user_id'),
        kwargs_get('nick_name'),
        kwargs_get('head'),
        kwargs_get('create_date'),
        kwargs_get('parent_id'),
        kwargs_get('group_name'),
        kwargs.get('weight', 0),
        kwargs_get('problem_id'),
        kwargs_get('answer_user_id'),
        kwargs_get('answer_nick_name')
    )

    user_status = (
        kwargs_get('user_id'),
        kwargs_get('problem_id'),
        kwargs_get('group_name')
    )

    @dec_make_conn_cursor
    def main(conn, cursor):
        # 插入回复数据
        sql_insert = """
        INSERT INTO mz_common_newdiscuss(
            object_id,
            object_type,
            object_content,
            object_name,
            object_location,
            comment,
            user_id,
            nick_name,
            head,
            create_date,
            parent_id,
            group_name,
            weight,
            problem_id,
            answer_user_id,
            answer_nick_name
        )VALUES (%s)
        """ % (','.join(map(lambda x: '%s', new_discuss)))

        # 获取最新回复的id
        last_answer_id = """
            SELECT last_insert_id() AS last_answer_id
        """

        # 更新最后回复
        sql_update = """
        UPDATE mz_common_newdiscuss
        SET last_answer_id=%s,last_answer_datetime=%s
        WHERE id=%s
        """

        # 插入我对当前问题的状态
        sql_insert_status = """
        INSERT INTO mz_common_newdiscussuserstatus(
            user_id,
            new_discuss_id,
            group_name,
            status
        )VALUES(%s,%s,%s,3) ON DUPLICATE KEY UPDATE status=3
        """

        # 更新其他关注此问题的学生用户状态（未读）
        sql_update_status_student = """
        UPDATE mz_common_newdiscussuserstatus
        SET status=1
        WHERE user_id!=%s AND new_discuss_id=%s AND status!=1 AND group_name!='teacher'
        """

        # 回复数量+1
        sql_update_discuss_count = """
        UPDATE mz_common_newdiscuss
        SET discuss_count=discuss_count+1
        WHERE id=%s
        """
        try:
            # 插入回复
            cursor.execute(sql_insert, new_discuss)
            logger.info("query:%s" % cursor._last_executed)
            cursor.execute(last_answer_id)
            new_discuss_id = cursor.fetchone()['last_answer_id']
            logger.info("query:%s" % cursor._last_executed)
            # 更新最后回复（如果当前问答的最后回复人不是老师或者当前回复人就是老师）   `
            cursor.execute(sql_update, (new_discuss_id, kwargs_get('create_date'), kwargs_get('problem_id')))
            logger.info("query:%s" % cursor._last_executed)
            # 插入我对当前问题的状态（已读）
            cursor.execute(sql_insert_status, user_status)
            logger.info("query:%s" % cursor._last_executed)
            # 更新其他关注此问题的学生用户状态（未读）
            cursor.execute(sql_update_status_student, (kwargs_get('user_id'), kwargs_get('problem_id')))
            logger.info("query:%s" % cursor._last_executed)
            # 回复数+1
            cursor.execute(sql_update_discuss_count, (kwargs_get('problem_id'),))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=new_discuss_id)

    return main()


def update_status(user_id, new_discuss_id, status, where_status):
    """
    根据用户和讨论ID更新状态
    :param user_id: 用户ID
    :param new_discuss_id: 讨论ID
    :param status: 修改后的状态
    :param where_status: 修改千的状态
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_update_status = """
        UPDATE mz_common_newdiscussuserstatus
        SET status=%s
        WHERE user_id=%s AND new_discuss_id=%s AND status=%s
        """

        try:
            cursor.execute(sql_update_status, (status, user_id, new_discuss_id, where_status))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()
