# -*- coding: utf-8 -*-

"""
@version: 2016/6/14
@author: Jackie
@contact: jackie@maiziedu.com
@file: usertask.py
@time: 2016/6/14 19:16
@note:  ??
"""
from db.api.apiutils import APIResult, dec_make_conn_cursor


def _convert_time_length(seconds):
    try:
        length = int(seconds)
        return "%d:%02d" % (length / 60, length % 60)
    except:
        return "00:00"


def get_user_task_detail(stagetask_id, class_id, user_id):
    """
    获取用户一个任务下的详情
    :param stagetask_id:
    :param class_id:
    :param user_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
            knowledge.id AS knowledge_id,
            knowledge.`name` AS knowledge_name,
            tkr.`index` AS knowledge_index,
            item.id AS item_id,
            item.obj_type,
            item.obj_id,
            item.expect_time,
            item.`index` AS item_index,
            item.parent_id,
            lesson.`name` AS lesson_name,
            lesson.video_length AS lesson_video_length,
            exam.title AS exam_title,
            COUNT(q.id) AS quiz_count,
            uki.`status`,
            FLOOR(pr.accuracy) AS accuracy
        FROM
            mz_lps3_knowledgeitem AS item
        INNER JOIN mz_lps3_taskknowledgerelation AS tkr ON tkr.knowledge_id = item.parent_id
        INNER JOIN mz_lps3_knowledge AS knowledge ON knowledge.id = item.parent_id
        INNER JOIN mz_lps3_stagetaskrelation AS _str ON _str.task_id = tkr.task_id
        INNER JOIN mz_lps3_usertaskrecord AS ut ON ut.stage_task_id = _str.id AND is_in_sequence = 1
        LEFT JOIN mz_course_lesson AS lesson ON lesson.id = item.obj_id
        AND item.obj_type = 'LESSON'
        LEFT JOIN mz_lps_examine AS exam ON exam.id = item.obj_id
        AND item.obj_type IN ('PROJECT', 'TEST')
        LEFT JOIN mz_lps_quiz AS q ON q.paper_id = exam.id
        LEFT JOIN mz_lps3_userknowledgeitemrecord AS uki ON uki.user_task_record_id = ut.id
        AND uki.knowledge_item_id = item.id
        LEFT JOIN mz_lps_examinerecord AS er ON er.examine_id = exam.id AND er.student_id = ut.student_id
        LEFT JOIN mz_lps_paperrecord AS pr ON pr.examinerecord_ptr_id = er.id
        WHERE
            _str.id = %s
        AND ut.class_id = %s
        AND ut.student_id = %s
        GROUP BY
            item.id
        ORDER BY
            knowledge_index ASC,
            item_index ASC,
            item_id ASC
        """
        cursor.execute(sql, (stagetask_id, class_id, user_id))
        rows = cursor.fetchall()
        tmp = {}
        for row in rows:
            knowledge_id = row.get('knowledge_id')
            tmp.setdefault(
                knowledge_id,
                dict(
                    id=knowledge_id,
                    name=row.get('knowledge_name'),
                    index=row.get('knowledge_index'),
                    items=[]
                )
            )
            if row['obj_type'] == 'LESSON':
                row['lesson_video_length'] = _convert_time_length(row['lesson_video_length'])
            tmp[knowledge_id]['items'].append(row)

        result = sorted(tmp.itervalues(), key=lambda x: x['index'])

        return APIResult(result=result)

    return main()


def get_user_task_info(stagetask_id, class_id, user_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT
            _utask.created,
            _utask.`status`,
            _utask.score,
            _utask.done_time,
            _task.`id` AS task_id,
            _task.`name` AS task_name,
            _exam.id AS project_id,
            _exam.title AS project_name,
            _uproject.remark
        FROM
            mz_lps3_usertaskrecord AS _utask
        INNER JOIN mz_lps3_stagetaskrelation AS _str ON _str.id = _utask.stage_task_id
        INNER JOIN mz_lps3_task AS _task ON _task.id = _str.task_id
        INNER JOIN mz_lps_examine AS _exam ON _exam.id = _task.project_id
        LEFT JOIN mz_lps_examinerecord AS _uexam ON _uexam.examine_id = _exam.id
        AND _uexam.student_id = _utask.student_id
        LEFT JOIN mz_lps_projectrecord AS _uproject ON _uproject.examinerecord_ptr_id = _uexam.id
        WHERE
            _utask.stage_task_id = %s
        AND _utask.class_id = %s
        AND _utask.student_id = %s
        """

        cursor.execute(sql, (stagetask_id, class_id, user_id))
        data = cursor.fetchall()
        if data:
            return APIResult(result=data[0])
        else:
            return APIResult(code=False)

    return main()
