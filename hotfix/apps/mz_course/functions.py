# -*- coding: utf-8 -*-
from db.api.course.course import get_id_course
from mz_course.models import Institute, CareerCourse

def _get_career_courses_info_by_institute(institute_id):
    institute = Institute.objects.get(id=institute_id)
    career_course_lst = CareerCourse.objects.filter(course_scope=None,
                                                    institute_id=institute.id,).order_by("-click_count")

    keywords_lst = (institute.keywords or '').split(',')
    link_course_lst = (institute.link_course or '').split(',')

    keywords = []
    for (k, l) in zip(keywords_lst, link_course_lst):
        keywords.append({'keyword': k, 'link': l})


    areer_courses_info = dict(career_course_lst=career_course_lst,
                        keywords = keywords,
                        online_count=institute.online_count)

    return areer_courses_info

def get_all_career_courses_info():
    #软件设计
    software_development = _get_career_courses_info_by_institute(1)
    #智能硬件
    intelligent_hardware = _get_career_courses_info_by_institute(2)
    #设计
    design = _get_career_courses_info_by_institute(3)
    #产品运营
    product_operation = _get_career_courses_info_by_institute(4)

    return software_development, intelligent_hardware, design, product_operation


def calc_course_video_length(lessons):
    if lessons:
        vl = reduce(lambda x, y: x + y, [l.video_length for l in lessons])
    else:
        return 0
    h = vl / 3600
    if vl % 3600 != 0:
        return h+1
    return h

def get_keyword_course_list(keyword, keyword_list, keyword_max_length=3):
    """
    通过关键字找到课程信息
    :param keyword: 接收的关键字 = str(以空格分隔)
    :param keyword_list: 自身有的关键字 = [{"keywords": "python,php,设计", "obj_id": 785},...]
    :return: keyword_course_list = [
        {
            'student_count': 7846L,
            'name': u'Java语言基础',
            'click_count': 125256L,
            'date_publish': 'datetime.datetime(2015, 5, 19, 16, 28, 35)',
            'image': u'course/2015/07/1.3Java基础.jpg',
            'need_pay': 0,
            'course_status': 1,
            'id': 4L,
            'favorite_count': 746L
        },...]
    """
    course_id_list = []
    if keyword and keyword_list:
        for i in keyword_list:
            n = 0
            for k in keyword.split(' '):
                if k:  # 排除多余空格
                    n += 1
                    for word in i['keywords'].split(','):
                        if k.lower() in word.lower():
                            if n > keyword_max_length:  # 限定关键字个数,多的将不予搜索
                                break
                            course_id_list.append(i['obj_id'])
                            break
    course_id_list = list(set(course_id_list))
    keyword_course_list = []
    for i in course_id_list:
        keyword_course_list.extend(get_id_course(i).result())

    return keyword_course_list

