# -*- coding: utf-8 -*-
from django.db import transaction
from mz_eduadmin.students.interface import ClassStudentsInterface
from mz_lps.models import Class, ClassTeachers
from mz_course.models import CareerCourse
from mz_user.models import UserProfile

def _get_class_queryset(edu_admin_id):
    classes = Class.objects.xall().filter(lps_version='3.0',
                                          is_active=True,
                                          class_type=Class.CLASS_TYPE_NORMAL,
                                          edu_admin__id=edu_admin_id).order_by('-date_publish')

    return classes

def _get_class_status(cls):
    if 2 == cls.status:
        status = '已毕业'
    elif cls.is_closed:
        status = '停止招生'
    else:
        status = '招生中'
    return status

def _get_class_operation(status):
    operation = [{'name': '', 's_name': 'ce'}]
    if '招生中' == status:
        operation = [{'name': '关闭报名', 's_name': 'ce'}]
    elif '停止招生' == status:
        operation = [{'name':'开启报名', 's_name': 'oe'},
                     {'name':'设为毕业', 's_name': 'graduation'}]

    return operation

def get_class_info(edu_admin_id, is_self):
    """获取班级列表信息
    :param query_list_dict
    """
    class_info_list=[]
    classes = _get_class_queryset(edu_admin_id)

    career_course_list = []
    teacher_list = []

    if not classes:
        return class_info_list, career_course_list, teacher_list

    for c in classes:
        teachers = [teacher.staff_name for teacher in c.teachers.all()]
        teacher = ','.join(teachers)
        class_dict = dict(class_id=c.id,
                          career_course=c.career_course.name,
                          class_no=c.coding,
                          current_student_count=c.current_student_count,
                          student_count_limit=c.student_limit,
                          teacher=teacher,
                          teachers=teachers,
                          edu_admin=c.edu_admin.staff_name,
                          class_status=_get_class_status(c))
        career_course_list.append(c.career_course.name)
        teacher_list.append(teacher)

        class_dict['class_operation'] = [{'name': '', 's_name': 'ce'}]
        if is_self:
            class_dict['class_operation'] = _get_class_operation(class_dict['class_status'])
        class_info_list.append(class_dict)

    career_course_list = list(set(career_course_list))
    teacher_list = list(set(teacher_list))

    return class_info_list, career_course_list, teacher_list

def _cal_students_status_count(cls, edu_admin_class_info_dict):
    cs = ClassStudentsInterface(cls.id)
    edu_admin_class_info_dict['graduate_students_count'] += cs.dashboard['graduate']
    edu_admin_class_info_dict['finish_students_count'] += cs.dashboard['finish']
    edu_admin_class_info_dict['normal_students_count'] += cs.dashboard['normal']
    edu_admin_class_info_dict['behind_students_count'] += cs.dashboard['behind']
    edu_admin_class_info_dict['paused_students_count'] += cs.dashboard['paused']
    edu_admin_class_info_dict['quit_students_count'] += cs.dashboard['quit']
    edu_admin_class_info_dict['students_count'] += cs.dashboard['total']

def get_edu_admin_class_info(edu_admin_id):
    edu_admin_class_info_dict = dict(classes_count=0,
                                     students_count=0,
                                     graduate_students_count=0,
                                     finish_students_count=0,
                                     normal_students_count=0,
                                     behind_students_count=0,
                                     paused_students_count=0,
                                     quit_students_count=0)

    classes = _get_class_queryset(edu_admin_id)
    for c in classes:
        _cal_students_status_count(c, edu_admin_class_info_dict)
        edu_admin_class_info_dict['classes_count'] += 1

    return edu_admin_class_info_dict

def get_search_list_by_keyword(func_get_data, keyword):
    data_list = func_get_data()
    search_list = []

    for item in data_list:
        if 0 == item['name'].find(keyword):
            search_list.append(item)

    return search_list

def update_class_state(class_id, state):
    cls = Class.objects.xall().get(id=class_id)
    if 'graduation' == state:
        cls.status = 2
    elif 'oe' == state:
        cls.is_closed = False
    elif 'ce' == state:
        cls.is_closed = True
    cls.save()

def check_class_create_parameters(create_parameters):
    msg = ''
    class_nos = Class.objects.xall().filter(coding=create_parameters['class_no'])
    if class_nos:
        msg = '班级编号已存在'
        return False, msg

    for teacher in create_parameters['teachers']:
        teachers = UserProfile.objects.filter(id=teacher)
        if not teachers:
            msg = '教师ID"%s"不存在' % teacher
            return False, msg

    edu_admins = UserProfile.objects.filter(id=create_parameters['edu_admin'])
    if not edu_admins:
        msg = '教务不存在'
        return False, msg

    career_courses = CareerCourse.objects.filter(id=create_parameters['career_course'])
    if not career_courses:
        msg = '专业不存在'
        return False, msg

    return True, msg

@transaction.commit_manually
def create_class(create_parameters):
    createclass = Class()
    timedate = create_parameters['open_yaer'] + '-' \
               + create_parameters['open_month'] + '-' \
               + create_parameters['open_day']
    createclass.coding = create_parameters['class_no']
    createclass.qq = create_parameters['qq_group']
    createclass.qq_key = create_parameters['key_group']
    createclass.qq_qrcode = create_parameters['image']
    createclass.date_open = timedate
    meeting_duration = create_parameters['open_time'] * 30
    createclass.class_type = Class.CLASS_TYPE_NORMAL
    createclass.is_active = True

    if meeting_duration > 0:
        createclass.lps_version = '3.0'
        createclass.meeting_duration = meeting_duration
    try:
        createclass.edu_admin = UserProfile.objects.get(id=create_parameters['edu_admin'])
        createclass.career_course = CareerCourse.objects.get(id=create_parameters['career_course'])
        createclass.save()
        for teacher in create_parameters['teachers']:
            ClassTeachers.objects.create(teacher_id=teacher, teacher_class_id=createclass.id)
    except Exception, e:
        transaction.rollback()
        raise e
    transaction.commit()

def get_edu_admin_name_by_id(edu_admin_id):
    return UserProfile.objects.get(id=edu_admin_id).staff_name

def get_teachers_para(create_parameters, para_name='teacher'):
    teachers = []
    for i in xrange(1, 11):
        if create_parameters.has_key(para_name+str(i)):
            teachers.append(long(create_parameters.get(para_name+str(i))))
    return teachers

def get_teachers_by_class_id(class_id):
    try:
        class_info = Class.objects.xall().get(id=class_id)
    except Class.DoesNotExist:
        return []
    teachers = class_info.teachers.values('id', 'nick_name', 'real_name')
    return list((obj['id'], obj['real_name'] or obj['nick_name']) for obj in teachers)

@transaction.commit_manually
def update_teacher(class_id, teachers):
    try:
        ClassTeachers.objects.filter(teacher_class_id=class_id).delete()
        for teacher in teachers:
            ClassTeachers.objects.create(teacher_id=teacher, teacher_class_id=class_id)
    except Exception, e:
        transaction.rollback()
        raise e
    transaction.commit()

if __name__ == "__main__":
    pass
