# -*- coding: utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()
import datetime
import calendar
import xlwt
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from mz_lps3.functions_nj import exec_sql
from mz_user.models import UserProfile
from mz_eduadmin.stats.models import StudentCompletion, StudentQuestionnaire, QuestionnaireTopic, QuestionnaireItem


class DateDefine:
    def __init__(self):
        self.NOW = datetime.datetime.now()

        self.ONE_DAY = datetime.timedelta(days=1)

        self.YEAR_NOW = self.NOW.year
        self.MONTH_NOW = self.NOW.month

        self.LAST_DAY_OF_THIS_MONTH = calendar.monthrange(self.YEAR_NOW, self.MONTH_NOW)[1]
        self.LAST_DATE_OF_MONTH = datetime.date(self.YEAR_NOW, self.MONTH_NOW, self.LAST_DAY_OF_THIS_MONTH)

        self.YESTERDAY_TIME = self.NOW - self.ONE_DAY
        self.YEAR_YESTERDAY = self.YESTERDAY_TIME.year
        self.MONTH_YESTERDAY = self.YESTERDAY_TIME.month


# 班级通用筛选条件:status为1(进行中),class_type为0(CLASS_TYPE_NORMAL),lps_version为'3.0'
# classstudent通用筛选条件:is_pause为0(未暂停),status为1(STATUS_NORMAL)

# -*- 完成度模块begin -*-
# 写入完成度记录模块
def class_tuple_have_classmeeting_this_month(alt_class):
    """
    找出所统计月份的符合条件的class_tuple
    条件: 本月除开最后的7天,开过有效班会,班会的时间以finish_date计
    有效班会: 班会status为1(已结束),且finish_date栏有记录
    若要在所有班级里选,alt_class为''
    :param alt_class: eg.135
    :return: desig_class_tuple
    """
    disig_day_tuple = days_tuple_of_month_less_last_7_days()
    sql = """
    SELECT
        class_id,
        COUNT(class_id)
    FROM
        mz_lps3_classmeeting AS cm
    JOIN mz_lps3_classmeetingrelation AS cmr ON cmr.class_meeting_id = cm.id
    JOIN mz_lps_class AS c ON c.id = cmr.class_id
    WHERE
        c.is_active = TRUE
    AND c.`status` = 1
    AND class_type = 0
    AND lps_version = '3.0'
    AND DATE_FORMAT(cm.finish_date, '%(date)s') IN %(disig_day_tuple)s
    %(class_id)s
    GROUP BY
        class_id;
    """ % dict(date='%Y-%m-%d', class_id='AND class_id = ' + str(alt_class) if alt_class else '',
               disig_day_tuple=disig_day_tuple)
    result = list()
    for class_id, class_id_count in exec_sql(sql):
        result.append(int(class_id))
    return tuple(result)


def days_tuple_of_month_less_last_7_days():
    """
    取该月除掉最后7天剩下的日期tuple
    该月: 该月为当前时间倒推一天所在的月份
    :return: disig_day_tuple
    """
    dd = DateDefine()
    last_day = calendar.monthrange(dd.YEAR_YESTERDAY, dd.MONTH_YESTERDAY)[1]
    disig_day_list = map(lambda x: datetime.date(dd.YEAR_YESTERDAY, dd.MONTH_YESTERDAY, x).strftime('%Y-%m-%d'),
                         range(1, last_day - 6))
    return tuple(disig_day_list)


def write_record_to_studentcompletion(classes):
    """
    20160330新版需求:
    需求：找出目标task的名字以及此task在此职业课里的排序(排序规则同上一版交付需求).

    目标task设定: 找出此学生连续pass的最后一个task(设为task_A), 若此task之后紧邻的task(设为task_B)有task记录(即'已开始','已完成',
    '未通过','重修中'四种状态中的一种), 则目标task为task_B, 否则目标task为task_A.

    在完成度记录表StudentCompletion里写入学生的该月的完成度
    学生须在classes的班级里,且为正常在读学员
    正常在读学员的条件: is_pause为0(未暂停),status为1(STATUS_NORMAL)
    该月: 该月为当前时间倒推一天所在的月份
    完成度计算规则: 老师所有打过分的task的个数和减一,这个规则同样适合于新加入的任务
    :param classes: eg.(134, 135)
    :return:
    """
    if classes:
        dd = DateDefine()
        cur_month_time = '%s-%02d-01' % (dd.YEAR_YESTERDAY, dd.MONTH_YESTERDAY)
        # 清空StudentCompletion本月冗余记录
        s = StudentCompletion.objects.filter(createtime=cur_month_time)
        s.delete()
        # 处理班级元组只有一个班级的例外
        classes = classes if isinstance(classes, tuple) else eval('(%s,)' % classes)
        # 为防止一次处理数据过多, 设定为5个班处理一次数据
        for i in range(0, len(classes), 5):
            slice_classes = classes[i: i + 5]
            sql = """
            SELECT
                _ur.id AS utr_id,
                _ur.`status` AS utr_status,
                _ur.student_id AS user_id,
                _ur.class_id AS class_id,
                _sr.id AS sr_id,
                _sr.`index` AS stagetask_index,
                _stage.`index` AS stage_index
            FROM
                mz_lps3_usertaskrecord AS _ur
            JOIN mz_lps3_stagetaskrelation AS _sr ON _ur.stage_task_id = _sr.id
            JOIN mz_course_stage AS _stage ON _stage.id = _sr.stage_id
            JOIN mz_lps_classstudents AS _cs ON (
                _cs.user_id = _ur.student_id
                AND _cs.student_class_id = _ur.class_id
            )
            WHERE
                _ur.class_id IN (%(slice_classes) s)
            AND _cs.is_pause = 0
            AND _cs.`status` = 1
            AND _ur.is_in_sequence = 1
            ORDER BY
                stage_index,
                stagetask_index
            """ % dict(slice_classes=','.join(str(x) for x in slice_classes))
            result = dict()

            for utr_id, utr_status, user_id, class_id, sr_id, stagetask_index, stage_index in exec_sql(sql):
                _key = '%s+%s' % (class_id, user_id)
                _index = '%s%s' % (stage_index, stagetask_index)
                if result.has_key(_key):
                    result[_key].append([_index, sr_id, utr_status])
                else:
                    result[_key] = [[_index, sr_id, utr_status]]

            task_dict = {}
            querysetlist = []
            for _k, _v in result.iteritems():
                for i, task_info in enumerate(_v):
                    if task_info[2] == 'PASS':
                        task_dict[_k] = task_info + [i]
                    else:
                        task_dict[_k] = task_info + [i]
                        break
                querysetlist.append(
                    StudentCompletion(class_id=_k.split('+')[0], student_id=_k.split('+')[1],
                                      cur_task_id=task_dict[_k][3], createtime=cur_month_time,
                                      stage_task_id=task_dict[_k][1]))
            StudentCompletion.objects.bulk_create(querysetlist)


# def write_record_to_studentcompletion(desig_class_tuple):
#     """
#     在完成度记录表StudentCompletion里写入学生的该月的完成度
#     学生须在desig_class_tuple的班级里,且为正常在读学员
#     正常在读学员的条件: is_pause为0(未暂停),status为1(STATUS_NORMAL)
#     该月: 该月为当前时间倒推一天所在的月份
#     完成度计算规则: 老师所有打过分的task的个数和减一,这个规则同样适合于新加入的任务
#     :param desig_class_tuple: eg.(134, 135)
#     :return:
#     """
#     if desig_class_tuple:
#         cur_month_time = YESTERDAY_TIME.strftime('%Y-%m') + '-01'
#         # 清空StudentCompletion本月冗余记录
#         s = StudentCompletion.objects.filter(createtime=cur_month_time)
#         s.delete()
#         sql = """
#         SELECT
#             a.utr_student_id,
#             a.utr_class_id,
#             a.utr_stage_task_id,
#             b.count_id - 1
#         FROM
#             (
#                 SELECT
#                     utr.student_id AS utr_student_id,
#                     utr.class_id AS utr_class_id,
#                     utr.stage_task_id AS utr_stage_task_id,
#                     CONCAT(s.`index`, str.`index`) AS i
#                 FROM
#                     mz_lps3_usertaskrecord AS utr
#                 JOIN mz_lps3_stagetaskrelation AS str ON utr.stage_task_id = str.id
#                 JOIN mz_course_stage AS s ON str.stage_id = s.id
#                 JOIN mz_lps_classstudents AS cs ON utr.student_id = cs.user_id
#                 AND utr.class_id = cs.student_class_id
#                 WHERE
#                     utr.score IS NOT NULL
#                 AND cs.is_pause = 0
#                 AND cs.`status` = 1
#                 ORDER BY
#                     - i
#             ) AS a
#         JOIN (
#             SELECT
#                 utr.student_id AS utr_student_id,
#                 utr.class_id AS utr_class_id,
#                 COUNT(utr.id) AS count_id
#             FROM
#                 mz_lps3_usertaskrecord AS utr
#             JOIN mz_lps3_stagetaskrelation AS str ON utr.stage_task_id = str.id
#             JOIN mz_course_stage AS s ON str.stage_id = s.id
#             JOIN mz_lps_classstudents AS cs ON utr.student_id = cs.user_id
#             AND utr.class_id = cs.student_class_id
#             WHERE
#                 utr.score IS NOT NULL
#             AND cs.is_pause = 0
#             AND cs.`status` = 1
#             %(desig_class_tuple_condition)s
#             GROUP BY
#                 utr.student_id,
#                 utr.class_id
#         ) AS b ON a.utr_student_id = b.utr_student_id
#         AND a.utr_class_id = b.utr_class_id;
#         """ % dict(
#             desig_class_tuple_condition='AND utr.class_id IN ' + str(desig_class_tuple) if desig_class_tuple else '')
#         result = dict()
#         querysetlist = []
#         for utr_student_id, utr_class_id, utr_stage_task_id, count_id in exec_sql(sql):
#             sc_key = str(utr_student_id) + ',' + str(utr_class_id)
#             if not result.has_key(sc_key):
#                 result[sc_key] = ''
#                 querysetlist.append(
#                     StudentCompletion(class_id=utr_class_id, student_id=utr_student_id, cur_task_id=count_id,
#                                       createtime=cur_month_time, stage_task_id=utr_stage_task_id))
#         StudentCompletion.objects.bulk_create(querysetlist)


# 展示完成度模块
def completion_record(cur_month, eu_id):
    """
    根据cur_month和eu_id查找完成度记录相关
    :param cur_month: eg.'2016-03'
    :param eu_id: eg.'24589'
    :return: det完成度记录dict
    """
    cur_month_time = cur_month + '-01'
    sql = """
    SELECT a.*,
        GROUP_CONCAT(IFNULL(tu.nick_name,'')),
        GROUP_CONCAT(IFNULL(tu.real_name,''))
    FROM
      (SELECT DISTINCT
            sc.class_id,
            sc.createtime,
            eu.nick_name,
            eu.real_name,
            c.coding,
            cc.name
        FROM
            stats_studentcompletion AS sc
        JOIN mz_lps_class AS c ON sc.class_id = c.id
        JOIN mz_course_careercourse AS cc ON c.career_course_id = cc.id
        JOIN mz_user_userprofile AS eu ON c.edu_admin_id = eu.id
        WHERE
            sc.createtime = '%(createtime)s'
        AND c.edu_admin_id = %(eu_id)s
        AND c.status = 1
        AND c.class_type = 0
        AND c.lps_version = '3.0'
        GROUP BY
            sc.class_id) as a
    JOIN mz_lps_classteachers AS ct ON a.class_id=ct.teacher_class_id
    JOIN mz_user_userprofile AS tu ON ct.teacher_id = tu.id
    GROUP BY a.class_id
    """ % dict(createtime=cur_month_time, eu_id=eu_id)
    record_dict = dict()
    ccourse_list = list()
    teacher_list = list()
    for class_id, createtime, eu_nname, eu_rname, class_coding, careercourse, teacher_nnames, teacher_rnames, in exec_sql(
            sql):

        teachers = []
        rname_list = teacher_rnames.split(',')
        nname_list = teacher_nnames.split(',')
        for i in xrange(len(rname_list)):
            teacher = rname_list[i] if rname_list[i] !='' else nname_list[i]
            teachers.append(teacher)

        record_dict[class_id] = dict(
            class_id=class_id,
            teacher=','.join(teachers),
            teachers=teachers,
            edu_admin=eu_rname or eu_nname,
            class_coding=class_coding,
            careercourse=careercourse,
            c_year=createtime.strftime('%Y'),
            c_month=createtime.strftime('%m')
        )
        ccourse_list.append(careercourse)
        teacher_list.append(','.join(teachers))
    ccourse_list = json.dumps(list(set(ccourse_list)))
    teacher_list = json.dumps(list(set(teacher_list)))
    return record_dict, ccourse_list, teacher_list


# 导出完成度excel模块
def export_excel_completion_inter(class_id, createtime):
    """
    导出学生完成度为excel
    :param class_id:
    :param createtime:
    :return:
    """
    class_info = class_base_info(class_id)
    careercourse, teacher, edu_admin, class_coding = \
        class_info['careercourse'], class_info['teacher'], class_info['edu_admin'], class_info['class_coding']

    info = completion_excel_info(class_id, createtime)

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet((u"完成度-%s-%s" % (class_coding,createtime)).encode('utf-8'))

    font = xlwt.Font()
    font.name = u'宋体'
    font.height = 220

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    style = xlwt.XFStyle()
    style.font = font
    style.alignment = alignment

    sheet.write_merge(
        0, 0, 0, 6,
        '专业: %s  老师: %s  教务: %s  统计时间: %s' % (careercourse, teacher, edu_admin, createtime),
        style=style)
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 540

    item_list = [u'序号', u'学生', u'班级编号', u'本月完成任务ID', u'任务名称', u'导出时间', u'学生缴费情况']
    for column in range(0, len(item_list)):
        sheet.write_merge(1, 1, 0 + column, 0 + column, item_list[column], style=style)
        sheet.col(column).width = 7000
        if column == 0:
            sheet.col(column).width = 5000
    sheet.row(1).height_mismatch = True
    sheet.row(1).height = 540

    for i, row in enumerate(info):
        for column in range(0, len(item_list)):
            sheet.write_merge(1 + row[0], 1 + row[0], 0 + column, 0 + column, row[column], style=style)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = \
        (u'attachment; filename=完成度-%s-%s-%s.xls' % (class_coding, edu_admin, createtime)).encode('utf-8')

    book.save(response)
    return response


def class_base_info(class_id):
    """
    查该班级基本信息
    :param class_id:
    :return:
    """
    sql = """
    SELECT
        c.coding,
        cc.`name`,
        GROUP_CONCAT(IFNULL(tu.nick_name,'')),
        GROUP_CONCAT(IFNULL(tu.real_name,'')),
        eu.nick_name,
        eu.real_name
    FROM
        mz_lps_class AS c
    JOIN mz_course_careercourse AS cc ON c.career_course_id = cc.id
    JOIN mz_lps_classteachers AS ct ON c.id=ct.teacher_class_id
    JOIN mz_user_userprofile AS tu ON ct.teacher_id = tu.id
    JOIN mz_user_userprofile AS eu ON c.edu_admin_id = eu.id
    WHERE
        c.id = %(class_id)s
    GROUP BY
        c.id
    """ % dict(class_id=class_id)
    result = dict()
    for class_coding, careercourse, teacher_nnames,teacher_rnames, edu_admin,e2 in exec_sql(sql):

        teachers = []
        rname_list = teacher_rnames.split(',')
        nname_list = teacher_nnames.split(',')
        for i in xrange(len(rname_list)):
            teacher = rname_list[i] if rname_list[i] !='' else nname_list[i]
            teachers.append(teacher)

        result = dict(
            class_coding=class_coding,
            careercourse=careercourse,
            teacher=','.join(teachers),
            edu_admin=e2 or edu_admin
        )
    return result


def completion_excel_info(class_id, createtime):
    """
    为该班该月的完成度excel准备数据
    :param class_id:
    :param createtime:
    :return: excel信息list
    """
    sql = """
    SELECT
        scl.student_id,
        scl.class_id,
        u.nick_name,
        u.real_name,
        u.mobile,
        c.coding,
        scl.cur_task_id,
        t.`name`,
        CONCAT(
            '[',
            GROUP_CONCAT(
                CONCAT(
                    '[',
                    up.pay_type,
                    ',',
                    up.pay_way,
                    ']'
                )
            ),
            ']'
        )
    FROM
        stats_studentcompletion AS scl
    JOIN mz_user_userprofile AS u ON scl.student_id = u.id
    JOIN mz_lps_class AS c ON scl.class_id = c.id
    JOIN mz_course_careercourse AS cc ON c.career_course_id = cc.id
    JOIN mz_lps_classstudents AS cs ON (
        scl.student_id = cs.user_id
        AND scl.class_id = cs.student_class_id
    )
    JOIN mz_lps3_stagetaskrelation AS str ON scl.stage_task_id = str.id
    JOIN mz_lps3_task AS t ON str.task_id = t.id
    LEFT JOIN mz_pay_userpurchase AS up ON (
        scl.student_id = up.user_id
        AND cc.id = up.pay_careercourse_id
        AND up.pay_status = 1
    )
    WHERE
        scl.class_id = %(class_id)s
    AND scl.createtime = '%(createtime)s'
    AND cs.is_pause = 0
    AND cs.`status` = 1
    GROUP BY
        scl.class_id,
        scl.student_id
    ORDER BY
        scl.cur_task_id;
    """ % dict(class_id=class_id, createtime=createtime)
    result = list()
    i = 1
    # pay_type {0: u"全款", 1: u"试学首付款", 2: u"尾款"}
    # pay_way {5: u"么么贷"}
    # pay_status ((0, u"未支付"), (1, u"支付成功"), (2, u"支付失败"))
    for student_id, class_id, nick_name, real_name, mobile, class_coding, cur_task_id, task_name, pay_l in exec_sql(
            sql):
        pay = u'未支付'
        if not pay_l == None:
            pay_list = eval(pay_l)
            for type, way in pay_list:
                if type == 1:
                    pay = u'试学'
                    break
            for type, way in pay_list:
                # 如果type出现尾款,视为全款
                if type == 0 or type == 2:
                    pay = u'全款'
                    break
            for type, way in pay_list:
                if way == 5:
                    pay = u'分期'
                    break
        item_list = [i, str(real_name if real_name else nick_name) + str(mobile), class_coding, cur_task_id, task_name,
                     datetime.datetime.now().strftime('%Y-%m-%d'), pay]
        result.append(item_list)
        i += 1
    return result


# -*- 完成度模块end -*-


# -*- 满意度模块begin -*-
# 展示问卷模块
def questionnaire_topic_item():
    """
    选出问卷版块与题目
    :return: 题目dict
    """
    sql = """
    SELECT
        qt.`name`,
        qi.question_stem,
        qt.`index`,
        qi.id
    FROM
        stats_questionnaireitem AS qi
    JOIN stats_questionnairetopic AS qt ON qi.topic_id = qt.id
    ORDER BY
        qt.`index`,
        qi.`index`;
    """
    ret = dict()
    for topic_name, ques_item, qt_index, qi_id in exec_sql(sql):
        if ret.has_key(qt_index):
            ret[qt_index]['question_stem'].append((qi_id, ques_item))
        else:
            ret[qt_index] = {'name': topic_name, 'question_stem': [(qi_id, ques_item)]}
    return ret


# 弹出提示做问卷弹框模块
def create_studentquestionnaire_record():
    """
    找出所有符合条件的班级里正常学习的学生, 创建StudentQuestionnaire记录, 默认is_finished=0
    :return:
    """
    class_ids = class_tuple_have_classmeeting_this_month('')
    if class_ids:
        dd = DateDefine()
        createtime = '%s-%02d-01' % (dd.YEAR_NOW, dd.MONTH_NOW)
        sql = """
        INSERT stats_studentquestionnaire (
            classstudent_id,
            createtime,
            is_finished
        ) SELECT
            id,
            '%(createtime)s',
            0
        FROM
            mz_lps_classstudents AS cs
        WHERE
            student_class_id IN %(class_ids)s
        AND `status` = 1
        AND is_pause = 0
        AND id NOT IN (
            SELECT
                classstudent_id
            FROM
                stats_studentquestionnaire
            WHERE
                createtime = '%(createtime)s'
        );
        """ % dict(class_ids=class_ids, createtime=createtime)
        exec_sql(sql)


def is_questionnaire_to_be_done(classstudent_id):
    """
    有学生进入到lps3学习页面时, 判断是否有StudentQuestionnaire记录, 且is_finished=0, 若是, 则弹出问卷
    :param classstudent_id:
    :return:
    """
    dd = DateDefine()
    createtime = '%s-%02d-01' % (dd.YEAR_NOW, dd.MONTH_NOW)
    # 9: 6
    # if NOW.date() in map(lambda x: datetime.date(YEAR_NOW, MONTH_NOW, x),
    #                      range(LAST_DAY_OF_THIS_MONTH - 6, LAST_DAY_OF_THIS_MONTH + 1)) and \
    if dd.NOW.day in range(dd.LAST_DAY_OF_THIS_MONTH - 6, dd.LAST_DAY_OF_THIS_MONTH + 1) and \
            StudentQuestionnaire.objects.filter(classstudent_id=classstudent_id, createtime=createtime, is_finished=0):
        return True
    return False


# 展示满意度模块
def sel_tea_ques_rec(createtime, eu_id):
    """
    展示老师满意度
    :param createtime:
    :param eu_id:
    :return:
    """
    createtime = createtime + '-01'
    sql = """
    SELECT
        tu.nick_name,
        tu.real_name,
        eu.nick_name,
        eu.real_name,
        cc.`name`,
        c.coding,
        CONCAT('{', GROUP_CONCAT(CONCAT(qt.index, ': ("', qt.`name`, '", "', topic_score, '")')), '}'),
        SUM(topic_score),
        c.id,
        createtime
    FROM
        stats_teacherquestionnairerecord AS tqr
    JOIN stats_questionnairetopic AS qt ON qt.id = tqr.questionnaire_topic_id
    JOIN mz_lps_class AS c ON c.id = tqr.class_id
    JOIN mz_user_userprofile AS tu ON tu.id = tqr.teacher_id
    JOIN mz_user_userprofile AS eu ON eu.id = c.edu_admin_id
    JOIN mz_course_careercourse AS cc ON cc.id = c.career_course_id
    WHERE createtime = '%(createtime)s'
    AND eu.id = %(eu_id)s
    GROUP BY c.coding,
    tu.id;
    """ % dict(createtime=createtime, eu_id=eu_id)
    record_dict = dict()
    ccourse_list = list()
    teacher_list = list()
    for teacher,t2, eduadmin, e2, careercourse, class_coding, topic_scores, total_score, class_id, tqr_createtime in exec_sql(
            sql):
        record_dict[(class_coding, teacher)] = dict(
            teacher=t2 or teacher,
            eduadmin=e2 or eduadmin,
            careercourse=careercourse,
            topic_scores=eval(topic_scores),
            total_score=str(total_score),
            class_id=class_id,
            c_year=tqr_createtime.strftime('%Y'),
            c_month=tqr_createtime.strftime('%m')
        )
        ccourse_list.append(careercourse)
        teacher_list.append(teacher)
    ccourse_list = json.dumps(list(set(ccourse_list)))
    teacher_list = json.dumps(list(set(teacher_list)))
    return record_dict, ccourse_list, teacher_list


def sel_class_stu_satisfy_record(classs_id, createtime):
    """
    20160401: 修改dev和线上报500, 不再在sql里执行iteritems
    查该班级该月学生的满意度评分详情
    :param classs_id:
    :param createtime:
    :return:
    """

    qt = QuestionnaireTopic.objects.all().order_by('index').values('id', 'name')
    qi = QuestionnaireItem.objects.all().order_by('index').values('id', 'question_stem', 'index', 'topic_id')

    qt_result = {}
    for i in qt:
        qt_result[i['id']] = i['name']

    qi_result = {}
    for i in qi:
        qi_result[i['id']] = i['question_stem']
    sq_sql = """
    SELECT
        sq.id AS sq_id,
        sq.subjective_item_1,
        sq.subjective_item_2,
        u.real_name,
        u.nick_name,
        u.mobile,
        SUM(sqis.score)
    FROM
        stats_studentquestionnaire AS sq
    JOIN mz_lps_classstudents AS cs ON cs.id = sq.classstudent_id
    JOIN mz_user_userprofile AS u ON u.id = cs.user_id
    JOIN stats_studentquestionnaireitemscore AS sqis ON sqis.student_questionnaire_id = sq.id
    WHERE
        sq.is_finished = 1
    AND sq.createtime = '%(createtime)s'
    AND cs.student_class_id = %(classs_id)s
    GROUP BY sq.id
    """ % dict(createtime=createtime, classs_id=classs_id)
    sq_result = dict()
    for sq_id, sq_1, sq_2, real_name, nick_name, mobile, sum_score in exec_sql(sq_sql):
        sq_result[sq_id] = dict(
            name=real_name or nick_name,
            mobile=mobile,
            sq_1=sq_1 if sq_1 else '',
            sq_2=sq_2 if sq_2 else '',
            sum_score=sum_score,
        )

    sqis_sql = """
    SELECT
        sqis.student_questionnaire_id,
        sqis.score,
        sqis.questionnaire_item_id,
        qi.topic_id,
        qi.`index`
    FROM
        stats_studentquestionnaireitemscore AS sqis
    JOIN stats_questionnaireitem AS qi ON sqis.questionnaire_item_id = qi.id
    WHERE sqis.student_questionnaire_id IN (%s)
    ORDER BY qi.`index`
    """ % ','.join(str(x) for x in sq_result.keys())

    sqis_result = dict()
    for sq_id, score, item_id, topic_id, item_index in exec_sql(sqis_sql):
        ques_stem = qi_result[item_id]
        score_det = [item_index, score, item_id, ques_stem]
        if sqis_result.has_key(sq_id):
            if sqis_result[sq_id].has_key(topic_id):
                sqis_result[sq_id][topic_id]['score_det'].append(score_det)
                sqis_result[sq_id][topic_id]['topic_sum'] += score
            else:
                sqis_result[sq_id][topic_id] = {'topic_sum': score, 'score_det': [score_det]}
        else:
            sqis_result[sq_id] = {topic_id: {'topic_sum': score, 'score_det': [score_det]}}

    for k, y in sq_result.iteritems():
        sq_result[k]['det'] = sqis_result[k]

    return sq_result, qt_result, qi_result


# 20160401: 在sql里执行iteritems的版本
# def sel_class_stu_satisfy_record(classs_id, createtime):
#     """
#     查该班级该月学生的满意度评分详情
#     :param classs_id:
#     :param createtime:
#     :return:
#     """
#     sql = """
#     SELECT
#         CONCAT(
#             '{',
#             GROUP_CONCAT(
#                 CONCAT(
#                     base.qi_to_id,
#                     ': ',
#                     base.score_list
#                 )
#             ),
#             '}'
#         ),
#         SUM(base.sum_score),
#         u.nick_name,
#         u.real_name,
#         u.mobile,
#         base.sq_1,
#         base.sq_2,
#         u.id
#     FROM
#         (
#             SELECT
#                 SUM(score) AS sum_score,
#                 qt.`index` AS qi_to_id,
#                 CONCAT(
#                     '[u"',
#                     qt.`name`,
#                     '",',
#                     SUM(score),
#                     ', sorted({',
#                     GROUP_CONCAT(
#                         CONCAT(
#                             qi.`index`,
#                             ': (u"',
#                             qi.question_stem,
#                             '", ',
#                             score,
#                             ')'
#                         )
#                     ),
#                     '}.iteritems(), key=operator.itemgetter(0))]'
#                 ) AS score_list,
#                 sq.id AS sq_id,
#                 sq.classstudent_id AS sq_cs,
#                 sq.subjective_item_1 AS sq_1,
#                 sq.subjective_item_2 AS sq_2
#             FROM
#                 stats_studentquestionnaireitemscore AS sqis
#             JOIN stats_studentquestionnaire AS sq ON sq.id = sqis.student_questionnaire_id
#             JOIN stats_questionnaireitem AS qi ON qi.id = sqis.questionnaire_item_id
#             JOIN stats_questionnairetopic AS qt ON qt.id = qi.topic_id
#             WHERE
#                 sq.classstudent_id IN (
#                     SELECT DISTINCT
#                         cs.id
#                     FROM
#                         stats_teacherquestionnairerecord AS tqr
#                     JOIN mz_lps_classstudents AS cs ON tqr.class_id = cs.student_class_id
#                     WHERE
#                         tqr.class_id = %(classs_id)s
#                     AND tqr.createtime = '%(createtime)s'
#                 )
#             AND sq.createtime = '%(createtime)s'
#             GROUP BY
#                 sq.id,
#                 qi.topic_id
#         ) AS base
#     JOIN mz_lps_classstudents AS cs ON cs.id = base.sq_cs
#     JOIN mz_user_userprofile AS u ON u.id = cs.user_id
#     GROUP BY
#         base.sq_id;
#     """ % dict(createtime=createtime, classs_id=classs_id)
#     result = dict()
#     for det, sum_score, nick_name, real_name, mobile, sq_1, sq_2, u_id in exec_sql(sql):
#         result[u_id] = dict(
#             det=eval(det),
#             sum_score=sum_score,
#             nick_name=real_name if real_name else nick_name,
#             mobile=mobile,
#             sq_1=sq_1,
#             sq_2=sq_2,
#         )
#     print result
#     return result


# 学生满意度excel模块
def export_excel_satisfaction_inter(eu_id, createtime):
    """
    导出学生满意度为excel
    :return:
    """
    sql = """
    SELECT
        tu.nick_name,
        tu.real_name,
        eu.nick_name,
        eu.real_name,
        cc.`name`,
        c.coding,
        CONCAT('{', GROUP_CONCAT(CONCAT(qt.index, ': ("', qt.`name`, '", "', topic_score, '")')), '}'),
        SUM(topic_score),
        c.id,
        createtime,
        tqr.scored_student_count
    FROM
        stats_teacherquestionnairerecord AS tqr
    JOIN stats_questionnairetopic AS qt ON qt.id = tqr.questionnaire_topic_id
    JOIN mz_lps_class AS c ON c.id = tqr.class_id
    JOIN mz_user_userprofile AS tu ON tu.id = tqr.teacher_id
    JOIN mz_user_userprofile AS eu ON eu.id = c.edu_admin_id
    JOIN mz_course_careercourse AS cc ON cc.id = c.career_course_id
    WHERE createtime = '%(createtime)s'
    AND eu.id = %(eu_id)s
    GROUP BY c.coding,
    tu.id;
    """ % dict(createtime=createtime, eu_id=eu_id)
    record_dict = list()
    topic_scores_items_list = list()
    i = 1
    for teacher,t2, eduadmin,e2, careercourse, class_coding, topic_scores, total_score, class_id, tqr_createtime, s_s_count \
            in exec_sql(sql):
        topic_scores_list = list()
        if not topic_scores_items_list:
            for s_v in eval(topic_scores).values():
                topic_scores_items_list.append(s_v[0])
        for s_v in eval(topic_scores).values():
            topic_scores_list.append(s_v[1])
        item_list_1 = [i, class_coding, s_s_count, careercourse, t2 or teacher, e2 or eduadmin]
        item_list_2 = [str(total_score)]
        item_list = item_list_1 + topic_scores_list + item_list_2
        record_dict.append(item_list)
        i += 1

    eu_name = get_object_or_404(UserProfile, id=eu_id).staff_name

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet((u"满意度分数统计-%s-%s" % (eu_name, createtime)).encode('utf-8'))

    # add new colour to palette and set RGB colour value
    xlwt.add_palette_colour("custom_colour", 0x21)
    book.set_colour_RGB(0x21, 141, 180, 227)

    font = xlwt.Font()
    font.name = u'宋体'
    font.height = 220

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['custom_colour']

    style = xlwt.XFStyle()
    style.font = font
    style.alignment = alignment

    field_name_style = xlwt.XFStyle()
    field_name_style.font = font
    field_name_style.alignment = alignment
    field_name_style.pattern = pattern

    topic_list_1 = [u'序号', u'班级', u'评分人数', u'专业', u'老师', u'教务']
    topic_list_2 = [u'总分']
    topic_list = topic_list_1 + topic_scores_items_list + topic_list_2

    for column in range(0, len(topic_list)):
        sheet.write_merge(1, 1, 0 + column, 0 + column, topic_list[column], style=field_name_style)
        sheet.col(column).width = 4500
        if column == 0:
            sheet.col(column).width = 3000
    sheet.row(1).height_mismatch = True
    sheet.row(1).height = 540

    for item in record_dict:
        for column in range(0, len(topic_list)):
            sheet.write_merge(1 + item[0], 1 + item[0], 0 + column, 0 + column, item[column], style=style)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = \
        (u'attachment; filename=满意度分数统计-%s-%s.xls' % (eu_name, createtime)).encode('utf-8')

    book.save(response)
    return response


# -*- 满意度模块end -*-

# todo
# 试卷展示排序 √
# 满意度详情页其它信息 (上一个页面有的,怎么把它传到新开页面,是post还是缓存) √
# topic排序 √
# item排序 √
# 满意度详情页url √
# 在相应的时间叫学生填问卷 √
# 到了规定时间就创建StudentQuestionnaire记录,创建时间填一号 创建满意度记录 创建完成度记录(跑起三个moniter) √
# 监听每月1号,调用cal_tea_month_satisfy() √
# 总分这边去掉hover √
# 确认刷新信息是同步还是异步, 若是异步, 动态填充 √
# 把nick_name替换为real_name √
# 返回教务选择集 √
# 取试卷时模块排序从id改为idex √
# index唯一
# 统一排序的标准
# 满意度概览页面的总分显示有问题
# 终极问题:先order_by再group_by不起作用

# 前端
# 问卷调查显示返回的错误信息
# 年、月选择框规则，单选且必有值 √
# ‘确定’按钮的激活条件：教务输入框不为空时 √
# 试卷展示样式出了问题 √
# 完成度这边的前端筛选不起作用 √
# 页面删除一行信息之后样式出问题 √

# 问题统计:
# 为什么classmeeting表status为1而finish_date没有记录(此情况为非常规情况)
# 班会是不是不管是is_temp
# 完成度记录表,会出现最后一个打分任务相同而打过分的任务的个数不相同的情况,此种情况发生的原因为:至少有一个学生老师没有挨着打分
# 有可能出现mz_pay_userpurchase里有此班级此用户的pay记录而mz_lps_classstudents里却没有记录的情况


if __name__ == "__main__":
    pass
    # create_studentquestionnaire_record()
    # is_questionnaire_to_be_done(11844)
    # create_studentquestionnaire_record()
    # write_record_to_studentcompletion(class_tuple_have_classmeeting_this_month(''))
    # write_record_to_studentcompletion((135))
    # class_tuple_have_classmeeting_this_month('')
    sel_class_stu_satisfy_record(135, '2016-03-01')
