#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    计算用户观看视频时长的脚本
"""
import time

import os
import sys
from datetime import datetime, timedelta

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django
django.setup()

import db.api
from db.cores.mongodbconn import get_mongo_db
from utils.logger import logger as log


# 当学习时间间隔5分钟以上,则不计入当天的累计学习时间
SEPARATION = 5

"""
    计算用户观看视频时长,
    minutes是一个这样的list:
    [0,1,2,7,9...], 最小为0, 最大为1439
　　0代表当天第一分钟, 1439代表当天最后一分钟
"""
def cal_study_total_minutes(minutes):
    total_minutes = 0
    last_minutes = 0
    
    for m in minutes:
        if (m - last_minutes) < SEPARATION:
            total_minutes += m - last_minutes

        last_minutes = m

    return total_minutes


def do_task():
    # make mongo instance
    try:
        mongo_db = get_mongo_db("businessinfo")
    except Exception as e:
        log.warn("get mongo_db failed.")
        return False
        
    collection = mongo_db.business_study_info

    lastday = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0) - timedelta(days=1)

    # mongo query limit
    LIMIT = 100
    # result count
    RES_COUNT = collection.find({"day": lastday}).count()
    # mongo skip count
    div = 1 if RES_COUNT % LIMIT != 0 else 0
    SKIP_COUNT = RES_COUNT / LIMIT + div

    failed_list = []
    
    # batch get data from mongodb
    for n in xrange(SKIP_COUNT):
        study_time_info_list = []

        log.info("starting cal study_time_info_list. "
                     "skip: %d, limit: %d" % (n*LIMIT, LIMIT))

        
        for item in collection.find({"day": lastday}).skip(n*LIMIT).limit(LIMIT):
            total_minutes = cal_study_total_minutes(item["minutes"])
            
            study_time_info_list.append({
                "user_id": item["user_id"],
                "course_id": item["course_id"],
                "lesson_id": item["lesson_id"],
                "day": lastday,
                "total_minutes": total_minutes,
            })

        if not study_time_info_list:
            log.warn("got no study_time_info_list. "
                     "skip: %d, limit: %d" % (n*LIMIT, LIMIT))
            continue
        
        api_result = db.api.set_study_time_info_batch(study_time_info_list)

        if api_result.is_error() == True:
            for study_time_info in study_time_info_list:
                log.warn("set study time info failed. "
                         "user_id:%s, course_id:%s, lesson_id:%s, "
                         "day:%s, total_minutes:%s"
                         % (study_time_info["user_id"],
                            study_time_info["course_id"],
                            study_time_info["lesson_id"],
                            study_time_info["day"].isoformat(),
                            study_time_info["total_minutes"]))
                
            log.warn("set_study_time_info failed. "
                      "count: %s" % len(study_time_info_list))

            failed_list.extend(study_time_info_list)
        else:
            for study_time_info in study_time_info_list:
                log.info("set study time info succeed. "
                         "user_id:%s, course_id:%s, lesson_id:%s, "
                         "day:%s, total_minutes:%s"
                         % (study_time_info["user_id"],
                            study_time_info["course_id"],
                            study_time_info["lesson_id"],
                            study_time_info["day"].isoformat(),
                            study_time_info["total_minutes"]))
                
            log.info("set_study_time_info succeed. "
                      "count: %s" % len(study_time_info_list))
            
    if failed_list:
        return False
    else:
        return True

if __name__ == '__main__':
    retry = 32
    delay_seconds = 60

    while retry > 0:
        ret = do_task()
    
        if ret == True:
            log.info("set study time done.")
            break
        else:
            log.warn("retry set study time after 60s.")
            time.sleep(delay_seconds)
            retry = retry - 1
    else:
        log.info("set study time failed.")