# -*- coding: utf-8 -*-

import json
import re
import string
from random import *
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.conf import settings
import os, time, uuid, logging, random
from HTMLParser import HTMLParser
from utils.logger import logger as log

logger = logging.getLogger('utils.tool')

# 全局变量，用于get_param_by_request函数的不同类型数据的默认空值
DEFAULT_VAL = {'None': '', 'str': '', 'float': 0.00, 'int': 0, 'dict': {},
               'tuple': (), 'list': [], 'bool': False}


def generate_random(random_length, type):
    '''
    随机字符串生成函数
    :param random_length:字符串长度
    :param type:字符串类型（0：纯数字 or 1：数字+字符 or 2：数字+字符+特殊字符）
    :return:生成的随机字符串
    '''
    # 随机字符串种子
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
    if second / 3600 <= 1:
        if second / 60 <= 1:
            result = str(second) + "秒钟"
        else:
            result = str(int(second / 60)) + "分钟"
    else:
        result = str(int(second / 3600)) + "小时"
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
    return time.strftime("%Y%m%d%H%M%S") + str(random.randint(10, 99))


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


def get_page_info(page_index, page_size):
    if page_index < 1:
        page_index = 1
    if page_size < 5:
        page_size = 5
    start_index = (page_index - 1) * page_size
    # end_index = page_index * page_size;
    return start_index


def get_page_count(rows_count, page_size):
    page_count = 0
    if rows_count % page_size == 0:
        page_count = rows_count / page_size
    else:
        page_count = rows_count / page_size + 1
    return page_count


def dec_timeit(func):
    def _func(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)

        log.info(
            "func:%s prosessed, "
            "takes %f s" % (func.func_name, time.time() - now))

        return res

    return _func


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


def get_param_by_request(request, param_name, default_val='', _type=None):
    """
    从request中取值，无就赋默认值，并可以强制转换类型
    :param request: request对象
    :param param_name: request中的键
    :param default_val: 默认值
    :param _type: 需要强制转换的类型
    :return: 结果值
    """
    _val = ''
    try:
        if param_name in request:
            _val = request[param_name].strip()
        if not _val:
            if (not default_val) and _type:
                global DEFAULT_VAL
                # 根据需要转换的类型，赋该类型的空值给_val
                _val = DEFAULT_VAL[str(_type).split('\'')[1]]
                return _val

            else:
                _val = default_val
        # 把unicode编码为utf-8的string对象
        if isinstance(_val, unicode):
            _val = _val.encode("utf-8")
        # 类型强制转换
        if _type:
            _val = _type(_val)

        return _val
    except Exception as e:
        log.info("get param failed, %s" % e)


def upload(files, upload_path1):
    """
    upload image
    :param files: 上传的文件
    :param upload_path1: 文件存储路径
    :return: 返回上传的路径，去除uplaods/层
    """

    upload_path = upload_path1.decode('utf-8')  # 处理中文路径
    try:
        ext = os.path.splitext(files.name)[1]
        d = os.path.dirname(files.name)
        fn = time.strftime("%Y%m%d%H%M%S")
        fn = fn + "_" + str(random.randint(9999, 100000))
        image_name = os.path.join(d, fn + ext)

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        upload_image_path = upload_path + image_name

        upload_image_files = open(upload_image_path, 'wb+')
        for chunk in files.chunks():
            upload_image_files.write(chunk)
        upload_image_files.close()

        image_path = upload_path.split('/', 1)[1] + image_name  # 去除uploads/这层文件路径
        return image_path
    except Exception as e:
        log.warn("get param failed, %s" % e)
        return None


def safe_int(n, default=None):
    if n:
        try:
            n = int(n)
        except TypeError:
            n = default
    else:
        n = default
    return n


# 判断是否为正整数
def safe_positive_int(n, default=1):
    if safe_int(default, -1) < 1:
        raise ValueError('default must be positive integer')
    n = safe_int(n, default)
    return default if n < 1 else n


# 获取上一页
def get_back_url(request, check_url):
    referer = request.META.get('HTTP_REFERER', [])
    if check_url in referer:
        return referer
    else:
        return check_url


def convert_01(val):
    """
    转换01为是否
    :param val:
    :return:
    """
    return u'是' if val else u'否'


# 如果首选url不存在就使用备选url
def get_correct_url(preferred_url, backup_url):
    if not preferred_url:
        preferred_url = str(backup_url)
    return preferred_url


def sql_unicode_encoding(content):
    """
    转换unicode字符为mysql可识别的编码，
    针对mysql中存json串的情况，
    如 黑客 -> '_u9ed1_u5ba2'
    :param content:
    :return:
    """
    return repr(content) \
        .replace('\\', '_') \
        .replace('u\'', '') \
        .replace('\'', '')


def other_day(n):
    """
    获取n天前的时间
    :param n:
    :return:
    """
    return datetime.now() - timedelta(days=n)


def get_week_1():
    """
    获取本周一对应的日期
    :return:
    """

    weekday = date.today().weekday()

    start = datetime.now() - timedelta(days=weekday)

    return start


def get_month_1():
    """
    获取本月一号对应的日期
    :return:
    """

    today = date.today()
    year = today.year
    month = today.month

    start = datetime(year, month, 1)

    return start


def is_phone(text):
    """
    是否是电话号码
    """
    return re.match('(13|14|15|18|17)[0-9]{9}$', text) is not None


def is_telephone(text):
    """
    是否是座机号码（包括小灵通）
    """
    ln = len(text)
    if ln == 6 or ln == 7 or ln == 8:
        return re.match('(\d{6})|(\d{7})|(\d{8})$', text) is not None
    else:
        return re.match('0(([1-9]\d)|([3-9]\d{2}))(\d{7}|\d{8})$', text) is not None


def is_phone_or_telephone(text):
    """
    是否是电话号码或小灵通
    """
    phone = is_phone(text)
    if not phone:
        return is_telephone(text)
    return True


def ip_check(ip):
    q = ip.split('.')
    return len(q) == 4 and len(
        filter(lambda x: 0 <= x <= 255,
               map(int, filter(lambda x: x.isdigit(), q)))) == 4


def fill_datetime(d):
    return datetime(d.year, d.month, d.day, 23, 59, 59)
