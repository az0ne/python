# -*- coding: utf-8 -*-

import string
from random import *
from datetime import datetime, date
from django.conf import settings
import os, time, uuid, logging
from HTMLParser import HTMLParser
import json
from decimal import Decimal
from utils.logger import logger as log

logger = logging.getLogger('utils.tool')

def generate_random(random_length, type):
    '''
    随机字符串生成函数
    :param random_length:字符串长度
    :param type:字符串类型（0：纯数字 or 1：数字+字符 or 2：数字+字符+特殊字符）
    :return:生成的随机字符串
    '''
    #随机字符串种子
    if type == 0:
        random_seed = string.digits
    elif type == 1:
        random_seed = string.digits + string.ascii_letters
    elif type == 2:
        random_seed = string.digits + string.ascii_letters + string.punctuation
    random_str = []
    while (len(random_str) < random_length):
        random_str.append(choice(random_seed))
    return ''.join(random_str)

def second_to_time(second):
    '''
    秒数化整
    :param second:
    :return:
    '''
    if second/3600 <= 1 :
        if second/60 <= 1 :
            result = str(second) + "秒钟"
        else:
            result = str(int(second/60)) + "分钟"
    else:
        result = str(int(second/3600)) + "小时"
    return result

def upload_generation_dir(target_dir):
    '''
    生成并获取上传文件的目标目录
    :param target_dir:
    :return:
    '''
    # 获取当前年份
    year_path = datetime.now().strftime("%Y")
    # 获取当前月份
    month_path = datetime.now().strftime("%m")
    # 目标路径
    target_path = os.path.join(settings.MEDIA_ROOT, target_dir, year_path, month_path)
    # 检查目录结构是否存在
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    return target_path

def generation_order_no():
    random = Random()
    random.seed(uuid.uuid1())
    return time.strftime("%Y%m%d%H%M%S")+str(random.randint(10,99))


# 去除html标签
class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def dec_timeit(func_name):
    def _wrap(func):
        def _func(*args, **kwargs):
            now = time.time()
            res = func(*args, **kwargs)
            
            log.debug(
                "func:%s prosessed, "
                "takes %f s" % (func_name, time.time() - now))
        
            return res
            
        return _func
        
    return _wrap

class JsonCommonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return "%.2f" % obj
        else:
            return json.JSONEncoder.default(self, obj)



def get_page_info(page_index, page_size):
    if page_index < 1:
        page_index = 1
    if page_size < 5:
        page_size = 5
    start_index = (page_index - 1) * page_size;
    end_index = page_index * page_size;
    return start_index, end_index


def get_page_count(rows_count, page_size):
    page_count = 0
    if rows_count % page_size == 0:
        page_count = rows_count / page_size
    else:
        page_count = rows_count / page_size + 1
    return page_count


def get_param_by_request(request, param_name, default_val=None, _type=None):
    try:
        if param_name in request:
            _val = request[param_name]
        else:
            _val = default_val
        if _type:
            _val = _type(_val)
        return _val
    except Exception as e:
        log.warn("get param failed, %s" % e)
        return default_val