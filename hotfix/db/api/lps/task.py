# -*- coding: utf-8 -*-

"""
@version: 2016/6/8
@author: Jackie
@contact: jackie@maiziedu.com
@file: task.py
@time: 2016/6/8 14:42
@note:  ??
"""
from db.api.apiutils import dec_make_conn_cursor, APIResult
from mz_lps3.models import Task


def get_free488_task_id(ccourse_id):
    """
    根据课程id获取免费488体系中的免费任务
    :param ccourse_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            _s.id AS sid,
            _s.`name` AS sname,
            _t.id AS tid,
            _str.id as stagetask_id,
            _t.`name` AS tname,
            _t.type
        FROM
            mz_course_stage AS _s,
            mz_lps3_stagetaskrelation AS _str,
            mz_lps3_task AS _t
        WHERE
            _s.lps_version = '3.0'
        AND _s.career_course_id = %s
        AND _s.id = _str.stage_id
        AND _str.task_id = _t.id
        ORDER BY
            _s.`index` ASC,
            _str.`index` ASC
        LIMIT 1
        """ % ccourse_id
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            return APIResult(code=False)
        task = data[0]
        if task.get('type') == Task.TASK_TYPE_FREE_488:
            return APIResult(result=(task.get('tid'),task.get('stagetask_id')))
        else:
            return APIResult(code=False)

    return main()


def get_task_info(task_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            *
        FROM
            mz_lps3_task
        WHERE
            id = %s
        """
        cursor.execute(_sql, (task_id,))
        result = cursor.fetchall()
        if result:
            return APIResult(result=result[0])
        else:
            return APIResult(code=False)

    return main()


TASK_ARTICLE_TYPE_BASE = 0  # 基础准备
TASK_ARTICLE_TYPE_AFTER_TASK = 1  # 任务完成解锁推荐


def get_task_rel_articles(task_id, tp):
    """
    获取任务相关文章资料
    :param task_id: 任务id
    :param tp:文章类型
    :return:
    """
    if tp not in (TASK_ARTICLE_TYPE_BASE, TASK_ARTICLE_TYPE_AFTER_TASK):
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            *
        FROM
            mz_free_task_article
        WHERE
            task_id = %s
        AND
            type = %s
        ORDER BY `index` ASC
        """
        cursor.execute(_sql, (task_id, tp))
        result = cursor.fetchall()
        return APIResult(result=result)

    return main()


def get_task_excellent_works(task_id):
    """
    获取任务的优秀作品
    :param task_id:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            *
        FROM
            mz_free_task_excellent_works
        WHERE
            task_id = %s
        """
        cursor.execute(_sql, (task_id,))
        result = cursor.fetchall()
        return APIResult(result=result)

    return main()


def get_free488_task_desc(task_id):
    """
    获取免费488任务相关推广描述
    :param task_id:任务原id
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            *
        FROM
            mz_free_task_desc
        WHERE
            task_id = %s
        """
        cursor.execute(_sql, (task_id,))
        result = cursor.fetchall()
        if result:
            return APIResult(result=result[0])
        else:
            return APIResult(code=False)

    return main()
