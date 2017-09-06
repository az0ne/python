# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from mz_common.decorators import student_required, eduadmin_required
from mz_eduadmin.stats.interface import questionnaire_topic_item, sel_tea_ques_rec, sel_class_stu_satisfy_record, \
    completion_record, class_base_info, export_excel_completion_inter, export_excel_satisfaction_inter, \
    DateDefine
from mz_eduadmin.stats.models import StudentQuestionnaireItemScore, StudentQuestionnaire, QuestionnaireItem
from mz_lps.models import Class, ClassStudents
from mz_user.models import UserProfile


def eval_year_month_euid(request):
    """
    根据year,month,euid构造查询以及页面需要的数据
    :param request:
    :return: year, month, createtime, eu_id, eu_name, year_list, month_list, nav, cu_month
    """
    user = request.user
    dd = DateDefine()
    year, month = dd.YEAR_NOW, dd.MONTH_NOW
    cur_month = '%s-%02d' % (year, month)
    eu_id = user.id
    eu_name = user.staff_name

    if request.GET.has_key('year') and request.GET.has_key('month') and request.GET.has_key('eu_id'):
        year = int(request.GET['year'])
        month = int(request.GET['month'])
        cur_month = '%s-%02d' % (year, month)
        eu_id = request.GET['eu_id']
        eu_name = get_object_or_404(UserProfile, id=eu_id).staff_name

    year_list = range(2015, dd.YEAR_NOW + 1)
    month_list = range(1, 13)
    cu_month = dd.MONTH_NOW
    nav = 'stats'

    return year, month, cur_month, eu_id, eu_name, year_list, month_list, nav, cu_month


@eduadmin_required
def index(request):
    """
    展示完成度
    :param request:
    :return:
    """
    year, month, cur_month, eu_id, eu_name, year_list, month_list, nav, cu_month = eval_year_month_euid(request)
    record_dict, teacher_list, ccourse_list = completion_record(cur_month, eu_id)

    return render(request, 'mz_eduadmin/stats/indexCompletion.html', locals())


@eduadmin_required
def export_excel_completion(request, class_id, year, month):
    """
    导出完成度excel
    :param request:
    :param class_id:
    :param year:
    :param month:
    :return:
    """
    return export_excel_completion_inter(class_id, str(year) + str(month) + '01')


@student_required
def get_questionnaire_det(request, class_id):
    """
    展示问卷
    :param request:
    :param class_id:
    :return:
    """
    class_id = int(class_id)
    student_name = request.user.real_name
    class_name = Class.objects.xall().get(id=class_id).coding
    classstudent_id = get_object_or_404(ClassStudents, user_id=request.user.id, student_class_id=class_id).id
    ques_items = questionnaire_topic_item()
    ques_choices = StudentQuestionnaireItemScore.SCORES
    return render(request, 'mz_eduadmin/stats/questionnaire_det.html', locals())


# 提交问卷
@student_required
def questionnaire_submit(request):
    data = request.POST

    # 判断是否所有的选择题都已经有选项
    ques_post = data.keys()
    ques_items = QuestionnaireItem.objects.all().values('id')
    ques_items_list = []
    for ques_item in ques_items:
        ques_items_list.append(unicode(ques_item['id']))
    sum_ques_list = set(ques_post + ques_items_list)
    # 如果QuestionnaireItem里所有的id都包含在ques_post里则表示所有选择题都已经提交
    val_post_items_length = len(ques_post) == len(sum_ques_list)

    if val_post_items_length:
        dd = DateDefine()
        createtime = '%s-%02d-01' % (dd.YEAR_NOW, dd.MONTH_NOW)

        student_questionnaire = StudentQuestionnaire.objects.filter(classstudent_id=data['classstudent_id'],
                                                                    createtime=createtime)

        if student_questionnaire:
            if not student_questionnaire[0].is_finished:

                student_questionnaire.update(
                    is_finished=1, subjective_item_1=data['subjective_item_1'] if data['subjective_item_1'] else '',
                    subjective_item_2=data['subjective_item_2'] if data['subjective_item_2'] else '')

                stu_ques_score_list = []
                for ques_item in ques_items:
                    stu_ques_score_list.append(
                        StudentQuestionnaireItemScore(score=int(data[unicode(ques_item['id'])]),
                                                      questionnaire_item_id=int(ques_item['id']),
                                                      student_questionnaire_id=int(student_questionnaire[0].id)))
                StudentQuestionnaireItemScore.objects.bulk_create(stu_ques_score_list)

                # return redirect(reverse("lps3:student_class", kwargs=dict(class_id=data['class_id'])))
                return HttpResponse(json.dumps({"status": u"success", "msg": u"提交成功"}), content_type="application/json")

            else:
                return HttpResponse(json.dumps({"status": u"failure", "msg": u"已经提交,请勿再次提交"}),
                                    content_type="application/json")

        else:
            return HttpResponse(json.dumps({"status": u"failure", "msg": u"创建满意度问卷记录出错,请联系教务"}),
                                content_type="application/json")

    else:
        return HttpResponse(json.dumps({"status": u"failure", "msg": u"选择题没有做完"}), content_type="application/json")


# 刷新页面或点击‘确定’时，请求后台，传出日期，教务名字，传进该月该教务满意度详细数据
@eduadmin_required
def tea_ques_rec(request):
    """满意度"""
    year, month, cur_month, eu_id, eu_name, year_list, month_list, nav, cu_month = eval_year_month_euid(request)
    record_dict, teacher_list, ccourse_list = sel_tea_ques_rec(cur_month, eu_id)

    return render(request, 'mz_eduadmin/stats/index.html', locals())


# 展示该班级该月学生的满意度评分
@eduadmin_required
def class_stu_satisfy_record(request, class_id, year, month):
    sq_result, qt_result, qi_result = sel_class_stu_satisfy_record(class_id, str(year) + str(month) + '01')
    satisfaction_class_info = class_base_info(class_id)
    year = year
    month = month

    return render(request, 'mz_eduadmin/stats/indexDetail.html', locals())


def export_excel_satisfaction(request, eu_id, year, month):
    return export_excel_satisfaction_inter(eu_id, '%s-%s-01' % (year, month))
