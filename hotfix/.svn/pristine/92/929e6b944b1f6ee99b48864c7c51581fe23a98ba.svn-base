# -*- coding: utf-8 -*-
from db.api.apiutils import dec_make_conn_cursor, APIResult
from db.api.common.new_discuss import _handling_discuss_data
from utils.logger import logger as log
from utils.tool import dec_timeit


@dec_timeit("get_all_question_and_answer_of_one_project_id")
@dec_make_conn_cursor
def get_all_question_and_answer_of_one_project_id(conn, cursor, object_id, limit, last_id=-1, luser_id=None):
    """
    获取一个item(以lesson_id/examine_id为标记)的所有问答
    :param luser_id: 当前登录的用户id，课程库问答用
    :return:
    """
    try:
        object_id = int(object_id)
        last_id = int(last_id)
        limit = int(limit)
    except ValueError as e:
        log.warn(e)
        raise e

    last_id_sql = 'AND nd.id < %s' if last_id > 0 else ''
    _param = (object_id, last_id, limit) if last_id > 0 else (object_id, limit)

    sql = """
        SELECT
            nd.id,
            nd.object_id,
            nd.object_content,
            nd.`comment`,
            nd.user_id,
            nd.nick_name,
            nd.head,
            nd.create_date,
            nd.group_name,
            nd.discuss_count,
            nd.user_praise_count,
            nd.answer_user_id,
            nd.answer_nick_name,
            nd_c.id AS c_id,
            nd_c.object_id AS c_object_id,
            nd_c.object_content AS c_object_content,
            nd_c.`comment` AS c_comment,
            nd_c.user_id AS c_user_id,
            nd_c.nick_name AS c_nick_name,
            nd_c.head AS c_head,
            nd_c.create_date AS c_create_date,
            nd_c.group_name AS c_group_name,
            GROUP_CONCAT(ndm.small_material) AS materials,
            GROUP_CONCAT(ndm.material) AS real_materials
        FROM
            mz_common_newdiscuss AS nd
        LEFT JOIN mz_common_newdiscuss AS nd_c ON nd_c.id = nd.last_answer_id
        LEFT JOIN mz_common_newdiscussmaterial AS ndm ON ndm.new_discuss_id = nd.id
        WHERE
            nd.object_id = %s
        """ + last_id_sql + """
        AND nd.problem_id = 0
        GROUP BY
            nd.id
        ORDER BY
            - nd.create_date
        LIMIT %s;
    """
    try:
        cursor.execute(sql, _param)
        discuss_list = cursor.fetchall()
        for discuss_dict in discuss_list:
            _handling_discuss_data(discuss_dict, luser_id)
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=discuss_list)


@dec_timeit("get_my_question_and_answer_of_one_project_id")
@dec_make_conn_cursor
def get_my_question_and_answer_of_one_project_id(conn, cursor, object_id, limit, user_id, last_id=-1):
    """
    获取一个item(以lesson_id/examine_id为标记)的我参加的问答
    :return:
    """
    try:
        object_id = int(object_id)
        last_id = int(last_id)
        limit = int(limit)
    except ValueError as e:
        log.warn(e)
        raise e

    last_id_sql = 'AND nd.id < %s' if last_id > 0 else ''
    _param = (object_id, user_id, last_id, limit) if last_id > 0 else (object_id, user_id, limit)

    sql_1 = """
        SELECT
            nd.id,
            nd.object_id,
            nd.object_content,
            nd.`comment`,
            nd.user_id,
            nd.nick_name,
            nd.head,
            nd.create_date,
            nd.group_name,
            nd.discuss_count,
            nd.user_praise_count,
            nd.answer_user_id,
            nd.answer_nick_name,
            nd_c.id AS c_id,
            nd_c.object_id AS c_object_id,
            nd_c.object_content AS c_object_content,
            nd_c.`comment` AS c_comment,
            nd_c.user_id AS c_user_id,
            nd_c.nick_name AS c_nick_name,
            nd_c.head AS c_head,
            nd_c.create_date AS c_create_date,
            nd_c.group_name AS c_group_name,
            GROUP_CONCAT(ndm.small_material) AS materials,
            GROUP_CONCAT(ndm.material) AS real_materials
        FROM
            mz_common_newdiscuss AS nd
        LEFT JOIN mz_common_newdiscuss AS nd_c ON nd_c.id = nd.last_answer_id
        LEFT JOIN mz_common_newdiscussmaterial AS ndm ON ndm.new_discuss_id = nd.id
        WHERE
            nd.object_id = %s
        AND nd.problem_id = 0
        AND nd.user_id = %s
        """ + last_id_sql + """
        GROUP BY
            nd.id
        ORDER BY
            - nd.create_date
        LIMIT %s;
    """

    sql_2 = """
        SELECT
            nd.id,
            nd.object_id,
            nd.object_content,
            nd.`comment`,
            nd.user_id,
            nd.nick_name,
            nd.head,
            nd.create_date,
            nd.group_name,
            nd.discuss_count,
            nd.user_praise_count,
            nd.answer_user_id,
            nd.answer_nick_name,
            nd_c.id AS c_id,
            nd_c.object_id AS c_object_id,
            nd_c.object_content AS c_object_content,
            nd_c.`comment` AS c_comment,
            nd_c.user_id AS c_user_id,
            nd_c.nick_name AS c_nick_name,
            nd_c.head AS c_head,
            nd_c.create_date AS c_create_date,
            nd_c.group_name AS c_group_name,
            GROUP_CONCAT(DISTINCT(ndm.small_material)) AS materials,
            GROUP_CONCAT(DISTINCT(ndm.material)) AS real_materials
        FROM
            mz_common_newdiscuss AS nd
        LEFT JOIN mz_common_newdiscuss AS nd_c ON nd_c.problem_id = nd.id
        LEFT JOIN mz_common_newdiscussmaterial AS ndm ON ndm.new_discuss_id = nd.id
        WHERE
            nd.object_id = %s
        AND nd.problem_id = 0
        AND nd_c.user_id = %s
        """ + last_id_sql + """
        GROUP BY
            nd.id
        ORDER BY
            - nd.create_date
        LIMIT %s;
    """
    try:
        cursor.execute(sql_1, _param)
        discuss_list_1 = cursor.fetchall()
        cursor.execute(sql_2, _param)
        discuss_list_2 = cursor.fetchall()
        discuss_list = discuss_list_1 + discuss_list_2
        discuss_list = sorted(discuss_list, key=lambda x: x['id'], reverse=True)
        _discuss_list = []
        _len = range(len(discuss_list))
        if len(_len) > 1:
            map(lambda x, y: _discuss_list.append(x) if discuss_list[y] != discuss_list[y - 1] else x,
                discuss_list, _len)
        else:
            _discuss_list = discuss_list
        final_discuss_list = _discuss_list[:limit]
        for discuss_dict in final_discuss_list:
            _handling_discuss_data(discuss_dict, user_id)
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=final_discuss_list)


@dec_timeit('get_one_question_first_level_answer_of_one_project_id')
@dec_make_conn_cursor
def get_one_question_first_level_answer_of_one_project_id(conn, cursor, discuss_id, limit, last_id):
    """
    获取一个item的第一级问答
    :return:
    """
    try:
        discuss_id = int(discuss_id)
        limit = int(limit)
        last_id = int(last_id)
    except ValueError as e:
        log.warn(e)
        raise e

    _sql = ""
    _param = [discuss_id, limit]
    if last_id:
        _sql = "AND id < %s"
        _param.insert(1, last_id)

    sql = """
        SELECT
            id,
            object_id,
            object_content,
            `comment`,
            user_id,
            nick_name,
            head,
            create_date,
            group_name,
            problem_id,
            answer_user_id,
            answer_nick_name
        FROM
            mz_common_newdiscuss
        WHERE
            parent_id = %s
        """ + _sql + """
        ORDER BY
            - id
    """

    if limit >= 0:
        sql += 'LIMIT %s;'
    else:
        _param.pop()

    try:
        cursor.execute(sql, _param)
        discuss_list = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=discuss_list)


@dec_timeit('get_one_question_second_level_answer_of_one_project_id')
@dec_make_conn_cursor
def get_one_question_second_level_answer_of_one_project_id(conn, cursor, id_list):
    """
    获取一个item的第二级问答
    :return:
    """
    try:
        _id_list = []
        for _id in id_list:
            _id_list.append(int(_id))
    except ValueError as e:
        log.warn(e)
        raise e

    sql = """
        SELECT
            id,
            object_id,
            object_content,
            `comment`,
            user_id,
            nick_name,
            head,
            create_date,
            group_name,
            parent_id,
            problem_id,
            answer_user_id,
            answer_nick_name
        FROM
            mz_common_newdiscuss
        WHERE
            parent_id IN (%s)
        ORDER BY
            - id;
    """ % ','.join(map(lambda x: '%s', _id_list))
    try:
        cursor.execute(sql, _id_list)
        discuss_list = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=discuss_list)


@dec_timeit('is_enterprise_student')
@dec_make_conn_cursor
def is_enterprise_student(conn, cursor, user_id, now):
    """
    判断（是否）是企业直通班学生
    :param user_id:
    :param now:
    :return: ''
    """
    sql = """
        SELECT
            'student'
        FROM
            mz_lps_classstudents AS cs
        JOIN mz_lps_class AS c ON c.id = cs.student_class_id
        WHERE
            cs.user_id = %s
        AND (
            cs.deadline IS NULL
            OR cs.deadline < %s
        )
        AND cs.`status` = 1
        AND c.is_active = 1
        AND c.class_type = 0
        AND c.lps_version = '3.0';
    """
    try:
        cursor.execute(sql, (user_id, now))
        group_name = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=group_name)


@dec_timeit('is_teacher')
@dec_make_conn_cursor
def is_teacher(conn, cursor, user_id):
    """
    判断是否是老师
    :param user_id:
    :return: 'teacher'/'student'
    """
    sql = """
        SELECT
            'teacher'
        FROM
            mz_user_userprofile_groups AS upg
        WHERE
            upg.userprofile_id = %s
        AND upg.group_id = 2;
    """
    try:
        cursor.execute(sql, (user_id,))
        group_name = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=group_name)


@dec_timeit('get_chance_count')
@dec_make_conn_cursor
def get_chance_count(conn, cursor, user_id):
    """
    获取一级提问的数量
    :param user_id:
    :return:
    """
    sql = """
        SELECT
            COUNT(nd.id) AS chance_count
        FROM
            mz_common_newdiscuss AS nd
        LEFT JOIN mz_user_userprofile_groups AS ug ON ug.userprofile_id = nd.answer_user_id
        WHERE
            nd.user_id = %s
        AND nd.object_location LIKE '{"course":[%%'
        AND (
            nd.problem_id = 0
            OR ug.group_id = 2
        );
    """
    try:
        cursor.execute(sql, (user_id,))
        chance_count = cursor.fetchone()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=chance_count)


@dec_timeit('get_question_info')
@dec_make_conn_cursor
def get_question_info(conn, cursor, user_id):
    """
    获取问题的对像属性
    :param user_id:
    :return:
    """
    sql = """
        SELECT
            object_id,
            object_content,
            object_location,
            object_name,
            object_type,
            user_id
        FROM
            mz_common_newdiscuss
        WHERE
            id = %s;
    """
    try:
        cursor.execute(sql, (user_id,))
        question_info = cursor.fetchone()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=question_info)


def add_question(**kwargs):
    """
    添加提问
    :param answer_dict: 提问的插入内容
    :return:
    """

    def kwargs_get(key):
        return kwargs.get(key, 'Null')

    material = kwargs.get('material', [])
    small_material = kwargs.get('small_material', [])

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

    @dec_make_conn_cursor
    def main(conn, cursor):
        # 插入讨论数据
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

        # 获取最新讨论的id
        last_answer_id = """
        SELECT last_insert_id() AS last_answer_id
        """

        # 插入图片
        insert_material = """
        INSERT mz_common_newdiscussmaterial (new_discuss_id, material, small_material)
        VALUES
            (%s, %s, %s)
        """

        # 插入我对当前问题的状态
        sql_insert_status = """
        INSERT INTO mz_common_newdiscussuserstatus(
            user_id,
            new_discuss_id,
            group_name,
            status
        )VALUES(%s,%s,%s,2)
        """

        try:
            # 插入问题
            cursor.execute(sql_insert, new_discuss)
            log.info("query:%s" % cursor._last_executed)
            cursor.execute(last_answer_id)
            new_discuss_id = cursor.fetchone()['last_answer_id']
            log.info("query:%s" % cursor._last_executed)
            if material:
                map(lambda x, y: cursor.execute(insert_material, (new_discuss_id, x, y)), material, small_material)
                log.info("query:%s" % cursor._last_executed)
            # 插入我对当前问题的状态（已读）
            cursor.execute(sql_insert_status, (kwargs_get('user_id'), new_discuss_id, kwargs_get('group_name')))
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=new_discuss_id)

    return main()


@dec_timeit('get_lesson')
@dec_make_conn_cursor
def get_lesson(conn, cursor, object_id):
    """
    获取lesson相关
    """
    sql = """
        SELECT
            `name`,
            course_id
        FROM
            mz_course_lesson
        WHERE
            id = %s;
    """
    try:
        cursor.execute(sql, (object_id,))
        object_info = cursor.fetchone()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=object_info)


@dec_timeit('get_lesson_teachers')
@dec_make_conn_cursor
def get_lesson_teachers(conn, cursor, career_courses_id):
    """
    获取lesson相关老师
    """
    sql = """
        SELECT DISTINCT
            (up.id),
            up.nick_name,
            up.avatar_small_thumbnall,
            up.description
        FROM
            mz_lps_class AS class
        JOIN mz_lps_classteachers AS ct ON class.id = ct.teacher_class_id
        JOIN mz_user_userprofile AS up ON ct.teacher_id=up.id
        WHERE
            class.career_course_id IN (%s)
        AND class_type IN (0, 3)
    """ % ','.join(map(lambda x: '%s', career_courses_id))
    try:
        cursor.execute(sql, career_courses_id)
        teachers = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=teachers)


@dec_timeit('get_lesson_teachers')
@dec_make_conn_cursor
def get_teachers_by_class_id(conn, cursor, class_id):
    """
    通过class_id获取老师
    """
    sql = """
        SELECT
            c.teacher_id AS id
        FROM
            mz_lps_classteachers AS c
        WHERE
            c.teacher_class_id = %s
    """
    try:
        cursor.execute(sql, (class_id,))
        teachers = cursor.fetchall()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=teachers)
