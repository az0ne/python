# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: lewis
@contact: lewis@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  学生端VIEWS
"""
import datetime
import db.api.common.new_discuss
import db.api.usercenter.resume
from db.api.usercenter.resume import update_user_start_work_time
from mz_common.function_discuss import get_one_question
from django.views.decorators.http import require_POST
from django.http.response import Http404

from mz_lps.models import Class
from mz_lps4.interface_lps import get_lps4_teacher_by_career_student_id_interface
from mz_usercenter.student.interface_resume import list_user_work_interface, list_user_edu_interface, \
    get_resume_user_info_interface, get_user_class_info_interface
from mz_usercenter.student.interface_study import show_study_goal, save_study_goal
from utils.logger import logger
from django.shortcuts import render
from mz_common.decorators import student_required, ajax_login_required
from django.contrib.auth.decorators import login_required
from interface_study import get_study_info, show_study_base, get_study_base_level_list, save_study_base
from interface_job_info import get_job_info_list, save_job_info_part
from core.common.http.response import success_json, failed_json
from mz_usercenter.base.context import get_usercenter_context
from mz_lps4.class_dict import LPS4_DICT


@student_required
def view_study_info(request):
    """
    学习信息
    :param request:
    :return:
    """
    user_id = request.user.id
    class_id = request.GET.get('class', 0)
    try:
        klass = Class.objects.xall().get(id=class_id)
        career_id = klass.career_course_id
    except Class.DoesNotExist:
        career_id = 0
    study_info_list = get_study_info(user_id, class_id)
    is_lps4 = False
    if LPS4_DICT.get(int(class_id)):
        is_lps4 = True
        teacher = get_lps4_teacher_by_career_student_id_interface(career_id, user_id)
    return render(request, 'mz_usercenter/student/my_studying.html', locals(),
                  context_instance=get_usercenter_context(request))


@student_required
def view_job_info(request):
    """
    就业信息
    :param request:
    :return:
    """
    user_id = request.user.id
    job_info_list = get_job_info_list(user_id)
    return render(request, 'mz_usercenter/student/employment.html', locals(),
                  context_instance=get_usercenter_context(request))


@student_required
def view_resume_info(request):
    """
    简历信息
    :param request:
    :return:
    """
    user_id = request.user.id

    user_class_info = get_user_class_info_interface(user_id)
    if user_class_info:
        is_from_intro = request.GET.get('intro', 0)
        if is_from_intro:
            db.api.usercenter.resume.update_is_view_resume_intro(user_id)

        elif not user_class_info['is_view_resume_intro']:
            return render(request, 'mz_usercenter/student/employment_create_index.html', {},
                          context_instance=get_usercenter_context(request))

        user_info = get_resume_user_info_interface(user_id)
        user_work = list_user_work_interface(user_id)
        user_edu = list_user_edu_interface(user_id)

        user_info_finish = True
        user_work_finish = True
        user_edu_finish = True

        if not user_info:
            user_info_finish = False

        if not user_work:
            user_work_finish = False

        if not user_edu:
            user_edu_finish = False

        start_work_time = user_class_info["start_work_time"]
        year_now = datetime.datetime.now().year
        work_exp_year = year_now - start_work_time
        try:
            age = (year_now - user_info['birthday'].year) or 24
        except (AttributeError, KeyError) as e:
            logger.warn(str(e))
            age = 24

        context = {
            "user_info": user_info,
            "start_work_time": start_work_time,
            "work_exp_year": u'%s年' % work_exp_year if work_exp_year > 0 else u'无',
            "age": age,
            "user_work": user_work,
            "user_edu": user_edu,
            "user_info_finish": user_info_finish,
            "user_work_finish": user_work_finish,
            "user_edu_finish": user_edu_finish
        }

        is_preview = request.GET.get('preview', 0)
        if is_preview:
            return render(request, 'mz_usercenter/student/employment_preview.html', context,
                          context_instance=get_usercenter_context(request))

        return render(request, 'mz_usercenter/student/employment_create_detail.html', context,
                      context_instance=get_usercenter_context(request))

    raise Http404


@student_required
def ajax_save_resume_user_info(request):
    """
    保存简历个人信息
    :param request:
    :return:
    """
    _post = request.POST
    user_id = request.user.id
    real_name = _post.get('username', '')
    gender = _post.get('sex', '1')
    birthday = _post.get('birthday', '')
    start_work_time = _post.get('worksTime', '0')
    failed = False

    if real_name and birthday and start_work_time:
        user_info = db.api.usercenter.resume.update_user_info(user_id, real_name, gender, birthday)
        if user_info.is_error():
            failed = True

        start_work_time = update_user_start_work_time(user_id, start_work_time)
        if start_work_time.is_error():
            failed = True

        if user_info.result() and start_work_time.result() and not failed:
            return success_json()

    return failed_json('保存用户信息失败')


@student_required
def ajax_save_resume_work(request):
    """
    保存简历工作信息
    :param request:
    :return:
    """
    _post = request.POST
    user_id = request.user.id
    company = _post.get('company', '')
    start_time = _post.get('experStartTime', '')
    end_time = _post.get('experEndTime', '')
    title = _post.get('worlPast', '')
    content = _post.get('jobDesc', '')
    resume_work_id = _post.get('resume_work_id', '')
    failed = False

    if company and start_time and end_time and title and content:
        if resume_work_id:
            work_info = db.api.usercenter.resume.update_user_work(user_id, company, start_time, end_time, title,
                                                                  content, resume_work_id)
        else:
            work_info = db.api.usercenter.resume.add_user_work(user_id, company, start_time, end_time, title, content)
        if work_info.is_error():
            failed = True

        if work_info.result() and not failed:
            return success_json(dict(last_insert_id=work_info.result()))

    return failed_json('保存工作信息失败')


@student_required
def ajax_del_resume_work(request):
    """
    删除简历工作信息
    :param request:
    :return:
    """
    user_id = request.user.id
    resume_work_id = request.POST.get('last_insert_id', 0)
    failed = False

    if resume_work_id:
        work_info = db.api.usercenter.resume.delete_user_work(resume_work_id, user_id)
        if work_info.is_error():
            failed = True

        if work_info.result() and not failed:
            return success_json()

    return failed_json('删除工作信息失败')


@student_required
def ajax_save_resume_edu(request):
    """
    保存简历教育信息
    :param request:
    :return:
    """
    _post = request.POST
    user_id = request.user.id
    school = _post.get('school', '')
    start_time = _post.get('educStartTime', '')
    end_time = _post.get('educEndTime', '')
    title = _post.get('education', '')
    major = _post.get('major', '')
    resume_edu_id = _post.get('resume_edu_id', '')
    failed = False

    if school and start_time and end_time and title and major:
        if resume_edu_id:
            work_info = db.api.usercenter.resume.update_user_edu(user_id, school, start_time, end_time, title, major,
                                                                 resume_edu_id)
        else:
            work_info = db.api.usercenter.resume.add_user_edu(user_id, school, start_time, end_time, title, major)
        if work_info.is_error():
            failed = True

        if work_info.result() and not failed:
            return success_json(dict(last_insert_id=work_info.result()))

    return failed_json('保存学历信息失败')


@student_required
def ajax_del_resume_edu(request):
    """
    删除简历教育信息
    :param request:
    :return:
    """
    user_id = request.user.id
    resume_work_id = request.POST.get('last_insert_id', 0)
    failed = False

    if resume_work_id:
        work_info = db.api.usercenter.resume.delete_user_edu(resume_work_id, user_id)
        if work_info.is_error():
            failed = True

        if work_info.result() and not failed:
            return success_json()

    return failed_json('删除学历信息失败')


@student_required
def view_order_info(request):
    """
    订单记录
    :param request:
    :return:
    """
    user_id = request.user.id
    import interface_order

    user_pay_infos = interface_order.get_user_orders(user_id)

    just_now = datetime.datetime.now()
    return render(request, 'mz_usercenter/student/my_order.html', locals(),
                  context_instance=get_usercenter_context(request))


@student_required
def view_my_discuss(request):
    """
    我的问答
    :param request:
    :return:
    """
    user_id = request.user.id
    problem_id = request.GET.get('p_id')
    if problem_id:
        result = db.api.common.new_discuss.get_problem_by_id(problem_id, user_id)
        if result.is_error():
            logger.warn('get_problem_by_id not data,problem_id is %s' % problem_id)
            raise Http404
        problem_info = result.result()
        try:
            answer_list = get_one_question(user_id, problem_id)
        except Exception, e:
            logger.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
            answer_list = []
        return render(request, 'mz_usercenter/student/my_discuss_detail.html',
                      {'problem_info': problem_info, 'answer_list': answer_list},
                      context_instance=get_usercenter_context(request))
    else:
        # 我的提问（全部）
        my_problem_list = []
        my_problem_result = db.api.common.new_discuss.get_my_problem_list_by_user_id(user_id)
        if not my_problem_result.is_error():
            my_problem_list = my_problem_result.result()
        # 我的回复（全部）
        my_answer_list = []
        my_answer_result = db.api.common.new_discuss.get_my_answer_list_by_user_id(user_id)
        if not my_answer_result.is_error():
            my_answer_list = my_answer_result.result()

        return render(request, 'mz_usercenter/student/my_discuss.html',
                      {'my_problem_list': my_problem_list, 'my_answer_list': my_answer_list},
                      context_instance=get_usercenter_context(request))


# ================================================================================================
@login_required(login_url="/")
def ajax_studying_div(request):
    """
    获取学习基础，修改的渲染DIV
    :param request:
    :param domain_name: 领域名称
    """
    user_id = request.user.id
    domain_name = request.POST.get('domain_name')
    # user_id = 115899
    # domain_name = u'技术类'
    study_base_list = show_study_base(user_id, domain_name)
    goal_list = show_study_goal()

    study_goal_data = [goal_list[i:i+4] for i in xrange(0, len(goal_list), 4)]

    level_list = get_study_base_level_list()
    return render(request, 'mz_usercenter/student/alter_studying_div.html', locals())


@login_required(login_url="/")
def ajax_save_studybase(request):
    """保存学习基础"""
    user_id = request.user.id
    # user_id = 115899
    query_data = request.POST.dict()
    try:
        domain_name = query_data['domain_name']
        goal = query_data['goal']
        del query_data['domain_name'], query_data['goal']
    except KeyError as e:
        return failed_json(u'缺少参数{0}'.format(e))
    save_study_goal(request.user, domain_name, goal)

    for k, v in query_data.iteritems():
        if 'skill' in k:
            save_study_base(user_id, int(k[len('skill') - len(k):]), int(v))
    return success_json()


@login_required(login_url="/")
def ajax_save_job(request):
    """保存就业信息"""
    user_id = request.user.id
    career_course_id = request.POST.get('career_course_id')
    position = request.POST.get('position')
    industry = request.POST.get('industry')
    result, msg = save_job_info_part(user_id, career_course_id, position, industry)
    if result:
        return success_json()
    else:
        return failed_json(msg)


@login_required(login_url="/")
def ajax_get_my_problem(request):
    user_id = request.user.id
    try:
        status = request.GET.get('status')
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_my_problem_list_by_user_id(user_id, status=status, end_id=end_id)
    my_problem_list = result.result()
    return render(request, 'mz_usercenter/student/ajax_div_discuss.html', {'my_discuss_list': my_problem_list})


@login_required(login_url="/")
def ajax_get_my_answer(request):
    user_id = request.user.id
    try:
        status = request.GET.get('status')
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_my_answer_list_by_user_id(user_id, status=status, end_id=end_id)
    my_answer_list = result.result()
    return render(request, 'mz_usercenter/student/ajax_div_discuss.html', {'my_discuss_list': my_answer_list})


@require_POST
@ajax_login_required
def ajax_praise(request):
    user_id = request.user.id
    problem_id = request.POST.get('problem_id')

    # 判断用户对问题是否点过赞
    is_praise = db.api.common.new_discuss.is_praise_problem(user_id, problem_id)
    if is_praise.is_error():
        logger.warn('Determine whether the user praise failed. '
                    'user_id: {0}, problem_id: {1}'.format(user_id, problem_id))
        is_praise = False
    else:
        is_praise = is_praise.result()

    if is_praise:
        # 取消点赞
        action = 'cancel'
        result = db.api.common.new_discuss.del_user_praise(user_id, problem_id)
        if result.is_error():
            logger.warn('del user praise failed. '
                        'user_id: {0}, problem_id: {1}'.format(user_id, problem_id))
            result = False
        else:
            result = result.result()
    else:
        # 点赞
        action = 'mark'
        result = db.api.common.new_discuss.add_user_praise(user_id, problem_id)
        if result.is_error():
            logger.warn('add user praise failed. '
                        'user_id: {0}, problem_id: {1}'.format(user_id, problem_id))
            result = False
        else:
            result = result.result()

    if not result:
        return failed_json(u'可能是快速重复点击造成的错误。')

    return success_json(dict(action=action, praise_count=result['user_praise_count']))
