# -*- coding: utf-8 -*-

from db.api.common.new_discuss import get_answer_count
from db.api.lps.lps_index import get_teachers_info_by_career_id
from db.api.course.career_course_intro import get_career_intro_tech_article, get_career_intro, get_career_intro_discuss, \
    get_career_intro_student_article
from utils.logger import logger as log
from django.core.urlresolvers import reverse
from django.conf import settings


# 相关文章,同PX页
def get_career_relate_article(career_id):
    result = get_career_intro_tech_article(career_id)
    if result.is_error():
        raise Exception('get_career_intro_tech_article')
    tech_articles = []
    for article in result.result():
        if article['tag']:
            temp = article['tag'].split(',')
            article['tag'] = [dict(
                name=id_name.split('_')[1],
                id=id_name.split('_')[0]
            ) for id_name in temp]
        tech_articles.append(article)
    return tech_articles


# 相关问答,同PX页
def get_career_discuss(career_id):
    # 介绍页相关数据

    result = get_career_intro(career_id)
    if result.is_error():
        raise Exception('get_career_intro')
    if not result.result()['page_intro']:
        log.warn('career_course_intro have no mz_career_page data')
        raise Exception(u'没有相关介绍页数据')
    result = get_career_intro_discuss([str(result.result()['page_intro']['discuss_id1']),
                                       str(result.result()['page_intro']['discuss_id2']),
                                       str(result.result()['page_intro']['discuss_id3'])])
    if result.is_error():
        raise Exception('get_career_intro_discuss')
    discuss_list = result.result()
    views_count_list = get_discuss_views_count(career_id)
    if discuss_list:
        for index, discuss in enumerate(discuss_list):
            discuss["discuss_count"] = get_discuss_count(discuss["id"])
            if views_count_list:
                discuss["views_num"] = views_count_list[index]

    return discuss_list


# 学生作品,同PX页
def get_career_student_work(career_id):
    result = get_career_intro_student_article(career_id)
    if result.is_error():
        raise Exception('get_career_intro_student_article')
    student_articles = result.result()
    return student_articles


# 教师团队
def get_career_teachers(career_id):
    result = get_teachers_info_by_career_id(career_id)
    if result.is_error():
        raise Exception('get_teachers_info_by_career_id')
    teachers = list(result.result())
    if teachers:
        hot_index = None
        teacher_id_list = []
        for index, teacher in enumerate(teachers):
            # pop the duplicate teacher
            if teacher['teacher_id'] in teacher_id_list:
                teachers.pop(index)
            else:
                teacher_id = teacher["teacher_id"]
                intro_url = "%s%s" % (
                    settings.SITE_URL, reverse("common:teacher_introduce", kwargs={"teacher_id": teacher_id}))
                center_url = "%s%s" % (settings.SITE_URL, reverse("u:index", kwargs={"user_id": teacher_id}))
                url = intro_url if teacher['is_hot'] else center_url
                teacher["url"] = url
                if teacher['career_teacher_id']:
                    hot_index = index
                teacher_id_list.append(teacher['teacher_id'])
        if hot_index:
            teachers[hot_index], teachers[0] = teachers[0], teachers[hot_index]  # 列表调整顺序

    return teachers


# 获取评论数量
def get_discuss_count(problem_id):
    result = get_answer_count(problem_id)
    if result.is_error():
        raise Exception('get_discuss_count')
        log.warn('get discuss count failed.')
    count = result.result()
    return count


def get_discuss_views_count(career_id):
    """
    每个职业课程设置三个问题浏览数(100-300之间)
    :param career_id: 职业课程id
    :return:[num1,num2,num3]
    """
    views_count_dict = {128: [215, 104, 179], 1: [153, 186, 102], 2: [198, 199, 265], 3: [269, 257, 161],
                        4: [124, 171, 194], 5: [133, 251, 128], 6: [185, 293, 163], 7: [220, 189, 101],
                        8: [137, 179, 189], 9: [164, 218, 236], 10: [142, 114, 164], 11: [151, 296, 193],
                        12: [297, 281, 283], 13: [177, 241, 167], 14: [274, 285, 255], 15: [234, 243, 229],
                        16: [111, 175, 236], 131: [266, 172, 237], 132: [216, 288, 159], 133: [140, 212, 112],
                        134: [192, 118, 257], 129: [104, 219, 127], 135: [168, 103, 107], 136: [295, 135, 245],
                        137: [160, 168, 163], 130: [110, 157, 167], 114: [142, 160, 238], 115: [192, 144, 290],
                        125: [257, 298, 187], 126: [179, 278, 189], 127: [188, 227, 160]}
    return views_count_dict.get(career_id, None)
