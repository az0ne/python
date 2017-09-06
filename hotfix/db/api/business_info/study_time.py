# -*- coding: utf-8 -*-

from datetime import datetime
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mongodbconn import get_mongo_db
from db.api.apiutils import APIResult, dec_make_conn_cursor


"""
    记录用户观看视频的数据到mongodb.
"""
@dec_timeit("append_study_info")
def append_study_info(create_time, user_id, course_id, lesson_id):

    mongodb = get_mongo_db("businessinfo")

    today = create_time.replace(hour=0, minute=0, second=0, microsecond=0)
    current_minute = create_time.hour * 60 + create_time.minute

    try:
        mongodb.business_study_info.update({
            "user_id": user_id,
            "course_id": course_id,
            "lesson_id": lesson_id,
            "day": today,
        }, {
            "$addToSet": {"minutes": current_minute},
        }, upsert=True)
    except Exception as e:
        log.warn(
            "update business_info failed. "
            "detaii: %s, user_id: %s, "
            "course_id: %s, lesson_id: %s, minute :%s, day: %s"
            % (e, user_id, course_id, lesson_id, current_minute, today))
        
        return APIResult(code=False)
    else:
        log.info(
            "update business_info succeed. "
            "user_id: %s, course_id: %s, lesson_id: %s, "
            "minute :%s, day: %s"
            % (user_id, course_id, lesson_id, current_minute, today))
        
    return APIResult(
        result={
            "day": today,
            "minute": current_minute,
        })


"""
    把已经统计了的用户视频观看时长批量写入mz_businessinfo_study_time表
"""    
@dec_timeit("set_study_time_info")
@dec_make_conn_cursor
def set_study_time_info_batch(conn, cursor, _study_time_info_list):

    now = datetime.now().isoformat()

    qsql = """
        INSERT IGNORE INTO mz_businessinfo_study_time(
           user_id, course_id, lesson_id, total_minutes,
           day, create_time, update_time)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        study_time_info_list = map(
            lambda x: (
                x["user_id"],
                x["course_id"],
                x["lesson_id"],
                x["total_minutes"],
                x["day"],
                now,
                now), _study_time_info_list)
    except KeyError as e:
        log.warn("study_time_info_list key error. detail: %s" % e)
        raise e

    try:
        cursor.executemany(qsql, study_time_info_list)
        conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:" % (e, cursor._last_executed))
        raise e
        
    return APIResult(result=True)
