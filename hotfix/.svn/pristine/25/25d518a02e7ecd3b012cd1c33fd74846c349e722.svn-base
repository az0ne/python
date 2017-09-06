# -*- coding: utf-8 -*-
import datetime
import json
from mz_platform.apis import course_sys_api, common_sys_api
from mz_platform.utils.view_shortcuts import ensure_apiresult_obj, ensure_obj

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor

def get_video(user_id, course_id, lesson_id):
    try:
        course_id = int(course_id)
        lesson_id = int(lesson_id)
    except ValueError:
        log.warn('course_id, lesson_id is not int')
    redis_key = 'get_video_%s_%s' % (course_id, lesson_id)

    @dec_timeit('get_video')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            api = course_sys_api.CourseSysApi.default_instance()
            common_api = common_sys_api.CommonSysApi.default_instance()

            lesson = ensure_apiresult_obj(api.get_one_lesson, id=lesson_id)
            course = ensure_obj(lesson.course)
            lesson_list = ensure_apiresult_obj(api.get_all_lesson, course_id=course.id)
            career_courses = api.get_careercourse_by_course(course_id=course.id).obj
            if career_courses:
                need_pay = api.is_registered_career_course(user_id,
                                                         list(item.id for item in career_courses))
                career_courses = api.get_careercourse_by_course(course_id=course.id, is_active=True).obj
                if career_courses:
                    career_courses = career_courses[0]
            else:
                need_pay = False
            has_pay = True if course.need_pay else False
            courseware = api.get_all_courseresource_by_course(course_id=course.id).obj
            discuss_list = api.get_discuss_by_lesson(lesson.id)
            seo = common_api.get_course_seo(course_id).obj

            data = dict(
                lesson=lesson, course=course, lesson_list=lesson_list,
                courseware=courseware, career_courses=career_courses,
                discuss_list=[], need_pay=need_pay, has_pay=has_pay,
                seo=seo)

        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # data = json.dumps(data)
        # set cache
        cache.set(redis_key, data, 60 * 60)

        return APIResult(result=data)

    return main(_enable_cache=True)

