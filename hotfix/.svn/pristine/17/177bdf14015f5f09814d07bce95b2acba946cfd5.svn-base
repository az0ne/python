#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()

import db.api.search.fulltext_search
import db.api.course.course
import db.api.course.career_course_intro
from db.cores.mongodbconn import get_mongo_db
from utils.logger import logger as log


def write_data_to_mongodb():
    """
    将数据写入到mongodb数据库
    :return: {'key':'article_<id>','tags':[[<tag_id>,'<tag_name>']..]}.., # tags one to many
                {'key':'course_<id>','chapter':<chapter_num>,'names'[['<career_course_name>','<career_course_short_name>']..]}.., #career_course one to many
                {'key':'wiki_<id>','img':'<course_img_url>','short_name':'<course_short_name>','name':'<course_name>'}..
    """
    meta_list = []

    """
     获取article tags
    """

    result = db.api.search.fulltext_search.make_article_tags()
    if result.is_error():
        log.warn("get article tags failed!")
        return False
    else:
        article_tags = result.result()

        for _art_id, tag_set in article_tags.items():
            meta_list.append({"key": "article_%d" % _art_id, "tags": list(tag_set)})

        log.info('career course write into mongodb!')

    """
        获取career course name
    """
    result = db.api.search.fulltext_search.make_course_career_names()

    if result.is_error():
        log.warn('get career course name failed!')
        return False
    else:
        career_course_names = result.result()

    """
        获取 small course teacher
    """

    result = db.api.search.fulltext_search.make_course_teacher()
    if result.is_error():
        log.warn("get small course teacher failed!")
        return False
    else:
        teacher = result.result()

    """
        获取course chapter num
    """

    result = db.api.search.fulltext_search.make_course_chapter()

    if result.is_error():
        log.warn('get course chapter num failed!')
        return False
    else:
        course_chapter_num = result.result()

        for _course_id, chapter in course_chapter_num.items():
            m = {"key": "course_%d" % _course_id, "chapter": chapter}
            m["names"] = list(career_course_names.get(_course_id, set()))
            m["tea_ni_name"] = teacher.get(_course_id, "")
            meta_list.append(m)

        log.info('career course write into mongodb!')

    """
        获取wiki course
    """
    result = db.api.search.fulltext_search.make_wiki_course_meta()
    if result.is_error():
        log.warn('get wiki course failed!')
        return False
    else:
        wiki_course = result.result()

        for _wiki_id, course_set in wiki_course.items():
            meta_list.append(
                {'key': "wiki_%d" % _wiki_id, 'name': course_set[0], 'short_name': course_set[1], 'img': course_set[2]})

        log.info('wiki course write into mongodb!')

    try:
        mongo_db = get_mongo_db("search_meta")
    except Exception as e:
        log.warn("get mongo_db failed.")
        return False

    coll = mongo_db.search_meta
    coll.remove({})
    for meta in meta_list:
        coll.ensure_index("key", unique=True)
        coll.update_one({"key": meta["key"]}, {"$set": meta}, upsert=True)

    return True


def write_suggest_data_to_mongodb():
    courses_result = db.api.course.course.get_courses()
    if courses_result.is_error() == True:
        log.warn("get_courses failed.")
        return False

    career_infos_result = db.api.search.fulltext_search.get_course_career_infos()
    if career_infos_result.is_error() == True:
        log.warn("get_courses_career_infos failed.")
        return False

    career_teachers_result = db.api.course.career_course_intro.get_career_teachers()
    if career_teachers_result.is_error() == True:
        log.warn("get_career_teachers failed.")
        return False

    courses = {}
    course_career_infos = {}
    career_teachers = {}

    for ct in career_teachers_result.result():
        career_teachers[ct["career_id"]] = career_teachers.get(
            ct["career_id"], [])

        career_teachers[ct["career_id"]].append({
            "teacher_id": ct["teacher_id"],
            "name": ct["name"],
            "title": ct["title"],
            "info": ct["info"],
            "image": ct["avatar_url"],
        })

    for c in career_infos_result.result():
        course_career_infos[c["course_id"]] = course_career_infos.get(
            c["course_id"], [])

        if not (c["name"] and c["image"] and c["short_info"]):
            continue

        course_career_infos[c["course_id"]].append({
            "name": c["name"],
            "image": c["image"],
            "short_name": c["short_name"],
            "description": c["short_info"],
            "student_count": c["student_count"],
            "teachers": career_teachers.get(c["id"], [])
        })

    for c in courses_result.result()["result"]:
        courses[c["name"]] = courses.get(c["name"], [])
        courses[c["name"]].append({
            "id": c["id"],
            "image": c["image"],
            "student_count": c["student_count"],
            "course_status": c["course_status"],
            "careers": course_career_infos.get(c["id"], [])
        })

    try:
        mongo_db = get_mongo_db("search_meta")
    except Exception as e:
        log.warn("get mongo_db failed.")
        return False

    coll = mongo_db.suggest_meta
    coll.remove({})

    for cname, course in courses.items():
        coll.ensure_index("name", unique=True)
        coll.update_one(
            {"name": cname}, {"$set": {"courses": course}}, upsert=True)

    return True


if __name__ == '__main__':

    delay_seconds = 60

    retry = 8
    while retry > 0:
        ret = write_data_to_mongodb()

        if ret == True:
            log.info("full text search data write into mongodb  done.")
            break
        else:
            log.warn("full text search data write into mongodb time after 60s.")
            time.sleep(delay_seconds)
            retry = retry - 1
    else:
        log.info("full text search data write into mongodb failed.")

    retry = 8
    while retry > 0:
        try:
            ret = write_suggest_data_to_mongodb()
        except Exception as e:
            log.warn("write_suggest_data_to_mongodb failed.")
            ret = False

        if ret == True:
            log.info("full text suggest data write into mongodb  done.")
            break
        else:
            log.warn("full text suggest data write into mongodb time after 60s.")
            time.sleep(delay_seconds)
            retry = retry - 1
    else:
        log.info("full text suggest data write into mongodb failed.")
