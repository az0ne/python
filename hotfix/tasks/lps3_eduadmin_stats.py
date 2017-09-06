# -*- coding: utf-8 -*-
import djevn
djevn.load()

from mz_lps3.functions_nj import exec_sql
from mz_eduadmin.stats.interface import class_tuple_have_classmeeting_this_month, write_record_to_studentcompletion, \
    create_studentquestionnaire_record, DateDefine
from mz_eduadmin.stats.models import TeacherQuestionnaireRecord


# 写入完成度记录moniter
def moniter_cal_month_completion():
    """
    每月1号零点执行write_record_to_studentcompletion(), 写入完成度记录
    :return:
    """
    dd = DateDefine()
    print str(dd.NOW) + ': start moniter_cal_month_completion'
    desig_class_tuple = class_tuple_have_classmeeting_this_month('')
    write_record_to_studentcompletion(desig_class_tuple)


def moniter_create_studentquestionnaire_record():
    """
    每个月的倒数第七天, 调用create_studentquestionnaire_record
    :return:
    """
    dd = DateDefine()
    print str(dd.NOW) + ': start moniter_create_studentquestionnaire_record'
    create_studentquestionnaire_record()


def moniter_cal_tea_month_satisfy():
    """
    每月1号零点算所有老师所有班级该月的满意度
    :return:
    """
    dd = DateDefine()
    print str(dd.NOW) + ': start moniter_cal_tea_month_satisfy'
    createtime = '%s-%02d-01' % (dd.YEAR_YESTERDAY, dd.MONTH_YESTERDAY)

    # 清空TeacherQuestionnaireRecord本月冗余记录
    p = TeacherQuestionnaireRecord.objects.filter(createtime=createtime)
    p.delete()

    # 写入TeacherQuestionnaireRecord记录
    sql = """
    INSERT stats_teacherquestionnairerecord (
        teacher_id,
        class_id,
        createtime,
        questionnaire_topic_id,
        topic_score,
        scored_student_count
    ) SELECT
        teacher_id,
        class_id,
        sq_createtime,
        qt_id,
        FORMAT(

            IF (
                COUNT(base.qt_score) <> 2,
                (
                    SUM(qt_score) - MAX(qt_score) - MIN(qt_score)
                ) / (COUNT(base.qt_score) - 2),
                SUM(qt_score) / 2
            ),
            2
        ),
        COUNT(class_id)
    FROM
        (
            SELECT
                ct.teacher_id,
                c.id AS class_id,
                sq.createtime AS sq_createtime,
                qt.id AS qt_id,
                SUM(sqis.score) AS qt_score
            FROM
                stats_studentquestionnaireitemscore AS sqis
            JOIN stats_studentquestionnaire AS sq ON sqis.student_questionnaire_id = sq.id
            JOIN stats_questionnaireitem AS qi ON sqis.questionnaire_item_id = qi.id
            JOIN stats_questionnairetopic AS qt ON qi.topic_id = qt.id
            JOIN mz_lps_classstudents AS cs ON sq.classstudent_id = cs.id
            JOIN mz_lps_class AS c ON cs.student_class_id = c.id
            JOIN mz_lps_classteachers AS ct ON ct.teacher_class_id = c.id
            WHERE
                teacher_id IS NOT NULL
            AND sq.createtime = '%(createtime)s'
            GROUP BY
                class_id,
                qt.id,
                cs.id,
                ct.id
        ) AS base
    GROUP BY
        base.class_id,
        base.qt_id,
        base.teacher_id;
    """ % dict(createtime=createtime)
    exec_sql(sql)


if __name__ == '__main__':
    pass
    # moniter_create_studentquestionnaire_record()
    # moniter_cal_month_completion()
    moniter_cal_tea_month_satisfy()
