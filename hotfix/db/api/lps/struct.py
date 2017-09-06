# -*- coding: utf-8 -*-

"""
@version: 2016/6/7
@author: Jackie
@contact: jackie@maiziedu.com
@file: struct.py
@time: 2016/6/7 11:43
@note:  ??
"""
from db.cores.cache import cache
from db.api.apiutils import dec_get_cache, dec_make_conn_cursor, APIResult


def get_course_syllabus(ccourse_id):
    """
    获取课程大纲
    :param ccourse_id:职业课程id
    :note:三层结构
    :return: [{'id':stage_id,'name':stage_name,'tasks':[{'id':task_id,'name':task_name,'project_name':xxx,knowledges:[]}]},]
    """
    # cache_key = "get_course_syllabus_%s" % ccourse_id

    # @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            _s.id AS sid,
            _s.`name` AS sname,
            _s.`index` AS sindex,
            _t.id AS tid,
            _t.`name` AS tname,
            _p.title AS project_name,
            _p.description AS project_description,
            _str.`index` AS tindex,
            _k.id AS kid,
            _k.`name` AS kname,
            _tkr.`index` AS kindex
        FROM
            mz_course_stage AS _s
        INNER JOIN mz_lps3_stagetaskrelation AS _str ON _str.stage_id = _s.id
        INNER JOIN mz_lps3_task AS _t ON _t.id = _str.task_id
        LEFT JOIN mz_lps3_taskknowledgerelation AS _tkr ON _tkr.task_id = _t.id
        LEFT JOIN mz_lps3_knowledge AS _k ON _k.id = _tkr.knowledge_id
        LEFT JOIN mz_lps_examine AS _p ON _p.id = _t.project_id
        WHERE
            _s.lps_version = '3.0'
        AND _s.career_course_id = %s
        """
        cursor.execute(_sql, (ccourse_id,))
        rows = cursor.fetchall()
        tmp = dict()
        for row in rows:
            stage_id, stage_name, stage_index = row['sid'], row['sname'], row['sindex']
            task_id, task_name, task_index = row['tid'], row['tname'], row['tindex']
            knowledge_id, knowledge_name, knowledge_index = row['kid'], row['kname'], row['kindex']
            tmp.setdefault(stage_id, dict(name=stage_name, index=stage_index, tasks=dict()))
            tmp[stage_id]['tasks'].setdefault(
                task_id, dict(name=task_name, index=task_index, project_name=row['project_name'],
                              project_description=row['project_description'], knowledges=dict()))
            if knowledge_id:
                tmp[stage_id]['tasks'][task_id]['knowledges'].setdefault(
                    knowledge_id, dict(name=knowledge_name, index=knowledge_index))

        result = []
        for sid, sinfo in sorted(tmp.iteritems(), key=lambda x: x[1]['index']):
            result.append({'id': sid, 'name': sinfo['name'], 'tasks': []})
            tasks = sinfo['tasks']
            for tid, tinfo in sorted(tasks.iteritems(), key=lambda x: x[1]['index']):
                result[-1]['tasks'].append(
                    {'id': tid, 'name': tinfo['name'], 'project_name': tinfo['project_name'],
                     'project_description': tinfo['project_description'], 'knowledges': []})
                knowledges = tinfo['knowledges']
                for kid, kinfo in sorted(knowledges.iteritems(), key=lambda x: x[1]['index']):
                    result[-1]['tasks'][-1]['knowledges'].append({'id': kid, 'name': kinfo['name']})
        # cache.set(cache_key, result, 60 * 3)
        return APIResult(result=result)

    return main()


def get_task_syllabus(task_id):
    """
    TODO 不可用
    :param task_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        _sql = """
        SELECT
            item.id,
            item.obj_type,
            item.obj_id,
            item.expect_time,
            item.`index`,
            item.parent_id,
            lesson.`name` AS lesson_name,
            lesson.video_length AS lesson_video_length,
            exam.title AS exam_title,
            COUNT(q.id) AS quiz_count,
        FROM
            mz_lps3_knowledgeitem AS item
        INNER JOIN mz_lps3_taskknowledgerelation AS tkr ON tkr.knowledge_id=item.parent_id
        LEFT JOIN mz_course_lesson AS lesson ON lesson.id = item.obj_id
        AND item.obj_type = 'LESSON'
        LEFT JOIN mz_lps_examine AS exam ON exam.id = item.obj_id
        AND item.obj_type IN ('PROJECT', 'TEST')
        LEFT JOIN mz_lps_quiz AS q ON q.paper_id = exam.id
        WHERE
            tkr.task_id = %s
        GROUP BY
            item.id
        """
        cursor.execute(_sql, (task_id,))
        result = cursor.fetchall()
        return result

    return main()



