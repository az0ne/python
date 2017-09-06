# -*- coding: utf-8 -*-
"""
@version: 2016/5/12 0012
@author: lewis
@contact: lewis@maiziedu.com
@file: interface_study.py
@time: 2016/5/12 0012 9:44
@note:  学生信息中的学习信息部分
"""
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
# import django
#
# django.setup()
from mz_lps.models import ClassStudents, Class
from mz_user.models import UserProfessionalSkill, ProfessionalSkill, StudyGoal, UserStudyGoal
from core.common.db.util import exec_sql

# level_list = ['不知道', '了解', '熟练', '精通']
# goal_list = ['技能提升', '就业']


def is_show_study_info(user_id):
    """
    是否需要展示学习信息
    :param user_id:用户ID
    :return: Ture or Flase
    """
    # 正常学生，并且非体验班级
    if ClassStudents.objects.filter(user__id=user_id, status=1,
                                    student_class__class_type=Class.CLASS_TYPE_NORMAL).exists():
        return True
    return False


def get_study_info(user_id, class_id=None):
    """
    获取学生的学习信息
    :param user_id:用户ID
    :param class_id:班级ID（一般为入学流程保存学习信息时使用）
    :return:study_info_list[{
        study_base_list=[{
            id：学习基础ID（int）
            name：学习基础的技能（utf8）
            level：当前技能的水平（utf8）
        },{...}]
        class_info_list=[{
            career_course_id:职业课程ID（int）
            career_course_name：职业课程名称（utf8）
            join_time：加入时间（utf8）
            teacher_name：老师名称（utf8）
            edu_admin_name：教务名称（utf8）
        },...]
    },{...}
    ]
    """
    sql = """
    SELECT
        _c_course.id AS career_course_id,
        _c_course.name AS career_course_name,
        _cs.created AS created,
        GROUP_CONCAT(IFNULL(_teacher.nick_name,'')) AS teacher_nick_name,
        GROUP_CONCAT(IFNULL(_teacher.real_name,'')) AS teacher_real_name,
        _edu_admin.nick_name AS edu_admin_nick_name,
        _edu_admin.real_name AS edu_admin_real_name,
        _institute.name AS institute_name
    FROM
      mz_lps_classstudents AS _cs
    INNER JOIN mz_lps_class AS _class ON _cs.student_class_id = _class.id
    LEFT JOIN mz_lps_classteachers AS ct ON ct.teacher_class_id = _class.id
    LEFT JOIN mz_user_userprofile AS _teacher ON ct.teacher_id = _teacher.id
    LEFT JOIN mz_user_userprofile AS _edu_admin ON _class.edu_admin_id = _edu_admin.id
    LEFT JOIN mz_course_careercourse AS _c_course ON _class.career_course_id = _c_course.id
    LEFT JOIN mz_course_institute AS _institute ON _c_course.institute_id = _institute.id
    WHERE
       _cs.status = 1 AND _class.class_type = 0 AND _cs.user_id = %s
    """ % user_id

    if class_id:
        sql += 'AND _class.id=%s' % class_id
    sql += ' GROUP BY _class.id'

    # 合并课程的领域的班级数据（同一个领域下可能会有多个班级以及职业课程）
    class_institute_dict = dict()
    for career_course_id, career_course_name, created, teacher_nick_name, teacher_real_name, \
        edu_admin_nick_name, edu_admin_real_name, institute_name in exec_sql(sql):

        teachers = []
        rname_list = teacher_real_name.split(',')
        nname_list = teacher_nick_name.split(',')
        for i in xrange(len(rname_list)):
            teacher = rname_list[i] if rname_list[i] !='' else nname_list[i]
            teachers.append(teacher)

        # 班级信息
        class_info = dict(career_course_id=career_course_id,
                          career_course_name=career_course_name,
                          join_time=created.strftime("%Y-%m-%d") if created else '',
                          teacher_name=','.join(teachers),
                          edu_admin_name=edu_admin_real_name if edu_admin_real_name else edu_admin_nick_name,
                          )
        domain_name = get_course_domain(institute_name)
        class_institute_dict.setdefault(domain_name, [])
        class_institute_dict[domain_name].append(class_info)
    # 按照课程的领域，解析学习基础
    study_info_list = []
    for domain_name, class_info_list in class_institute_dict.iteritems():
        study_base_list, is_complete_studybase = get_study_base_by_domain(user_id, domain_name)
        study_goal = get_student_study_goal(user_id, domain_name)

        study_info_list.append(dict(study_base_list=study_base_list, class_info_list=class_info_list,
                                    domain_name=domain_name, is_complete_studybase=is_complete_studybase,
                                    study_goal=study_goal))

    return study_info_list


def get_course_domain(institute_name):
    """
    获取课程分析领域
    :param institute_name:学院名称
    :return 领域类型
    """
    if not institute_name:
        return u'技术类'
    if institute_name in [u'软件开发', u'智能硬件']:
        return u'技术类'
    elif institute_name in [u'设计']:
        return u'设计类'
    elif institute_name in [u'产品运营']:
        return u'产品运营'


def get_study_base_by_domain(user_id, domain):
    """
    根据课程的领域和用户获取，该用户学习基础的掌握程度
    :param user_id:用户ID
    :param domain:领域类型
    :return: study_base_list=[{
            id：学习基础ID（int）
            name：学习基础的技能（utf8）
            level：当前技能的水平（utf8）
        },{...}];
        is_complete_studybase bool 是否完成学习基础
    """
    user_skills = UserProfessionalSkill.objects.filter(
        skill__domain=domain, user_id=user_id
    ).values('level', 'skill_id', 'skill__skill').order_by('skill_id')
    study_base_list = []
    is_complete_studybase = False
    if not user_skills:
        skills = ProfessionalSkill.objects.filter(domain=domain).order_by('id')
        for s in skills:
            study_base_list.append(dict(id=s.id, name=s.skill, level=u'未填写'))
    else:
        for s in user_skills:
            study_base_list.append(
                dict(id=s['skill_id'], name=s['skill__skill'],
                     level=UserProfessionalSkill.LEVEL_CHOICES.get(s['level'], u'未填写')))
        is_complete_studybase = True
    return study_base_list, is_complete_studybase


def get_study_base(user_id, institute_name):
    """
    根据课程的领域和用户获取，该用户学习基础的掌握程度
    :param user_id:用户ID
    :param institute_name:学院名称
    :return: study_base_list=[{
            id：学习基础ID（int）
            name：学习基础的技能（utf8）
            level：当前技能的水平（utf8）
        },{...}]
    """
    study_base_list, is_complete_studybase = get_study_base_by_domain(user_id, get_course_domain(institute_name))
    return study_base_list


def batch_get_study_base(user_ids, institute_name):
    """批量处理
    根据课程的领域和用户获取，用户学习基础的掌握程度
    :param user_ids:用户id列表
    :param institute_name:
    :return:
    """
    domain = get_course_domain(institute_name)
    sql = """
        SELECT
        u.id,
        p.skill,
        uup.`level`
    FROM
        (
            mz_user_userprofile AS u,
            mz_user_professionalskill AS p
        )
    LEFT JOIN mz_user_userprofessionalskill AS uup ON uup.user_id = u.id
    AND uup.skill_id = p.id
    WHERE
        u.id IN %s
    AND p.domain = '%s'
    """
    in_text_user_ids = "(" + ','.join(map(str, user_ids)) + ")"
    sql = sql % (in_text_user_ids, domain)
    result = dict()
    for user_id, skill, level in exec_sql(sql):
        result.setdefault(user_id, [])
        level = UserProfessionalSkill.LEVEL_CHOICES.get(level, u'未填写')
        result[user_id].append(u"%s:%s" % (skill, level))
    return result


def show_study_base(user_id, domain):
    """
    展示学习基础
    :param user_id:用户ID
    :param domain:领域类型
    :return: study_base_list=[{
            id：学习基础ID（int）
            name：学习基础的技能（utf8）
        },{...}];
    """
    study_base_list = []
    # 如果已经填写学习基础则返回
    if UserProfessionalSkill.objects.filter(skill__domain=domain, user_id=user_id).exists():
        return study_base_list

    skills = ProfessionalSkill.objects.filter(domain=domain).order_by('id')
    for s in skills:
        study_base_list.append(dict(id=s.id, name=s.skill))
    return study_base_list


def save_study_base(user_id, skill_id, level):
    """
    保存学习基础
    :param user_id:用户ID
    :param skill_id:技能ID
    :param level：技能水平
    :return:None
    """
    user_skills = UserProfessionalSkill.objects.filter(user_id=user_id,
                                                       skill_id=skill_id)
    if not user_skills:
        UserProfessionalSkill(
            user_id=user_id, skill_id=skill_id,
            level=level).save()
    else:
        user_skills[0].level = level
        user_skills[0].save()


def get_study_base_level_list():
    """获取学习基础中每个技能的列表"""
    return UserProfessionalSkill.LEVEL_CHOICES.values()


def show_study_goal():
    """
    获取学习目标选项列表
    :return:
    """
    return StudyGoal.objects.all().order_by('index')


def save_study_goal(user, domain_name, goal_id):
    """
    保存学生学习目标
    :param user:
    :param domain_name:
    :param goal_id:
    :return:
    """
    if UserStudyGoal.objects.filter(
            user=user, domain_name=domain_name).count() == 0:
        UserStudyGoal.objects.create(
            user=user, domain_name=domain_name, goal_id=goal_id)


def get_student_study_goal(user_id, domain_name):
    return UserStudyGoal.objects.filter(
        user_id=user_id, domain_name=domain_name).first()


def test():
    print get_study_info(104231)
    print batch_get_study_base((117454, 117643, 5566), None)


if __name__ == "__main__":
    test()
