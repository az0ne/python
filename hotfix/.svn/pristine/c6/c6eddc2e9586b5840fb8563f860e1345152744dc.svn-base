# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_course_task_by_career_course_id")
@dec_get_cache("get_course_task_by_career_course_id")
@dec_make_conn_cursor
def get_course_task_by_career_course_id(conn, cursor, career_course_id):
    """
    根据职业课程ID，查询该课程的所有阶段,再通过所有阶段的id,
    到任务与阶段的关系表（mz_lps3_stagetaskrelation）中，
    查询到所有的任务
    :param conn:
    :param cursor:
    :param career_course_id:职业课程ID
    :return:返回各个阶段的id,name和任务的id,name,并根据index排序
    """
    try:
        cursor.execute(
            """
                SELECT
                    stage.id AS careerCourse_id,
                    stage. NAME AS careerCourse_name,
                    task.id AS task_id,
                    task. NAME AS task_name
                FROM
                    mz_course_stage AS stage
                LEFT JOIN mz_lps3_stagetaskrelation AS str ON stage.id = str.stage_id
                LEFT JOIN mz_lps3_task AS task ON str.task_id = task.id
                WHERE
                    stage.career_course_id = %s
                    AND stage.lps_version = 3.0
                ORDER BY
                    stage.`index`,
                    str.`index`
            """, (career_course_id,)
        )
        courseStages = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=courseStages)


def get_career_course_knowledge_task_count(career_id):
    redis_key = 'get_career_course_knowledge_task_count_%s' % career_id

    @dec_timeit("get_career_course_knowledge_task_count")
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        获取职业课程lps3知识点数量和task数量
        :param conn:
        :param cursor:
        :return:
        """
        sql1 = """
            SELECT
                count(ki.id) AS count
            FROM
                mz_lps3_taskknowledgerelation AS tkr
            JOIN mz_lps3_stagetaskrelation AS str ON str.task_id = tkr.task_id
            JOIN mz_course_stage AS s ON s.id = str.stage_id AND s.career_course_id = %s
            JOIN mz_lps3_knowledgeitem AS ki ON ki.parent_id = tkr.knowledge_id
            """
        sql2 = """
            SELECT
                  count(ki.id) AS count
            FROM
                mz_lps3_taskknowledgerelation AS tkr
            JOIN mz_lps3_stagetaskrelation AS str ON str.task_id = tkr.task_id
            JOIN mz_course_stage AS s ON s.id = str.stage_id AND s.career_course_id = %s
            JOIN mz_lps3_knowledgeitem AS ki ON (
                ki.parent_id = tkr.knowledge_id
                and ki.obj_type=%s
            )
        """
        sql3 = """
            SELECT
              COUNT(task.id) AS count
            FROM mz_lps3_task AS task
            JOIN mz_lps3_stagetaskrelation AS str ON str.task_id = task.id
            JOIN mz_course_stage AS s ON s.id = str.stage_id AND s.career_course_id = %s
        """
        try:
            cursor.execute(sql1, (career_id,))
            knowledge_item_count = cursor.fetchone()
            cursor.execute(sql2, (career_id, 'LESSON'))
            knowledge_lesson_count = cursor.fetchone()
            cursor.execute(sql2, (career_id, 'PROJECT'))
            knowledge_project_count = cursor.fetchone()
            cursor.execute(sql3, (career_id,))
            task_count = cursor.fetchone()
            data = {'knowledge_item_count': knowledge_item_count['count'],
                    'knowledge_lesson_count': knowledge_lesson_count['count'],
                    'project_count': knowledge_project_count['count'] + task_count['count'],
                    }
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
            raise e
        # set cache
        cache.set(redis_key, data, 60 * 5)
        return APIResult(result=data)
    return main(_enable_cache=True)
