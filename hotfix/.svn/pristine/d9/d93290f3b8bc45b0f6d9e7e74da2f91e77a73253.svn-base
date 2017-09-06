# -*- coding: utf-8 -*-

"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/3/29 15:23
@note:  ??
"""
import os
import logging
from datetime import datetime, timedelta
from django.db.models import Q
from django.conf import settings
from PIL import Image
from utils.tool import upload_generation_dir
from utils.tool import generate_random
from utils.sms_manager import tpl_send_sms
from mz_common.models import MobileVerifyRecord
from mz_lps.models import ClassStudents, Class

logger = logging.getLogger('mz_user.views')


def get_user_type(user):
    if user.is_teacher():  # 用户类别（普通学员：0，直通班学员：1，老师：2）
        user_type = 2
    elif ClassStudents.objects.filter(status=ClassStudents.STATUS_NORMAL,
                                      user=user, student_class__class_type=Class.CLASS_TYPE_NORMAL).exists():
        user_type = 1
    else:
        user_type = 0
    return user_type


def get_student_class_type(user, class_id):
    if ClassStudents.objects.filter(status=ClassStudents.STATUS_NORMAL,
                                    user=user, student_class__class_type=Class.CLASS_TYPE_NORMAL,
                                    student_class_id=class_id).exists():
        return True
    return False


# 发送短信
def send_sms(mobile, ip, send_type=0):
    # 查询同IP是否超出最大短信数量发送限制
    start = datetime.now() - timedelta(hours=23, minutes=59, seconds=59)

    if MobileVerifyRecord.objects.filter(created__gt=start, mobile=mobile).count() >= settings.SMS_MAX_COUNT_MOBILE:
        return False, u"该手机号超过当日短信发送限制数量"

    if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=start)).count() >= settings.SMS_COUNT:
        return False, u"该IP超过当日短信发送限制数量"

    one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    if MobileVerifyRecord.objects.filter(Q(ip=ip), Q(created__gt=one_min_ago)).exists():
        return False, u"当前ip距离上一次发送验证码未超过60s"
    if MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(created__gt=one_min_ago)).exists():
        return False, u"当前手机号距离上一次发送验证码未超过60s"

    # 生成激活码
    random_str = generate_random(6, 0)
    # 邮件发送记录写入数据库
    mobile_record = MobileVerifyRecord()
    mobile_record.code = random_str
    mobile_record.mobile = mobile
    mobile_record.type = send_type
    mobile_record.ip = ip
    mobile_record.source = 2
    mobile_record.save()

    # 发送短信
    apikey = settings.SMS_APIKEY
    tpl_id = settings.SMS_TPL_ID  # 短信模板ID
    tpl_value = random_str

    try:
        tpl_send_sms.delay(apikey, tpl_id, tpl_value, mobile)
        return True, ''
    except Exception, e:
        logger.error(e)


# 个人资料 - 头像裁切
def avatar_crop(request, file_name, picwidth, picheight):
    marginTop, marginLeft, marginTo, marginLeft = (0, 0, 0, 0)
    width = picwidth
    height = picheight
    # 裁切
    try:
        # 获取头像临时图片名称
        # avatar_tmp = request.session.get("avatar_tmp", None)
        avatar_tmp = file_name
        source_path = os.path.join(settings.MEDIA_ROOT, 'temp', avatar_tmp)
        avatar_up_small = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_thumbnail.jpg"
        avatar_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_big.jpg"
        avatar_middle_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_middle.jpg"
        avatar_small_target_path = upload_generation_dir("avatar")+"/"+avatar_tmp.split(".")[0]+"_small.jpg"
        f = Image.open(source_path)
        f.resize((picwidth, picheight), Image.ANTIALIAS).save(avatar_up_small, 'jpeg', quality=100)
        ft = Image.open(avatar_up_small)
        box = (marginTop, marginLeft, marginTop+width, marginLeft+height)
        # box(0,0,100,100)
        ft.crop(box).resize((220, 220), Image.ANTIALIAS).save(avatar_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((104, 104), Image.ANTIALIAS).save(avatar_middle_target_path, 'jpeg', quality=100)
        ft.crop(box).resize((70, 70), Image.ANTIALIAS).save(avatar_small_target_path, 'jpeg', quality=100)

        # 读取原来的头像信息并删除(默认图片不能删除，by guotao 2015.9.23)
        if str(request.user.avatar_url).count('/') > 1 and avatar_tmp != str(request.user.avatar_url).split("/")[-1]:
            avatar_url_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_url)
            avatar_middle_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_middle_thumbnall)
            avatar_small_thumbnall_path = os.path.join(settings.MEDIA_ROOT)+"/"+str(request.user.avatar_small_thumbnall)
            if os.path.exists(avatar_url_path):
                os.remove(avatar_url_path)
            if os.path.exists(avatar_middle_thumbnall_path):
                os.remove(avatar_middle_thumbnall_path)
            if os.path.exists(avatar_small_thumbnall_path):
                os.remove(avatar_small_thumbnall_path)
    except Exception, e:
        logger.error(e)
        return False
    # 将裁切后的图片路径信息更新图片字段
    request.user.avatar_url = avatar_target_path.split("..")[-1].replace('/uploads', '').replace('\\', '/')[1:]
    request.user.avatar_middle_thumbnall = avatar_middle_target_path.split("..")[-1].replace('/uploads', '').\
        replace('\\', '/')[1:]
    request.user.avatar_small_thumbnall = avatar_small_target_path.split("..")[-1].replace('/uploads', '').\
        replace('\\', '/')[1:]
    request.user.save()

    # if request.user.uid:
    #     sync_avatar(request.user.uid, avatar_target_path)

    return True, settings.SITE_URL + settings.MEDIA_URL + str(request.user.avatar_url)


def sync_avatar(forum_uid, big):
    import shutil

    root_path = settings.PROJECT_ROOT
    filename, extension = os.path.splitext(big)
    filename = filename.split("../")[-1]
    pure_name = '_'.join(filename.split('_')[:-1])

    forum_uid = "%09d" % forum_uid
    dir1 = forum_uid[0:3]
    dir2 = forum_uid[3:5]
    dir3 = forum_uid[5:7]
    prefix = forum_uid[-2:]

    for size in ('big', 'middle', 'small'):
        main_avatar_path = root_path + "/" + pure_name + '_' + size + extension

        forum_avatar_dir_path = root_path + '/forum/uc_server/data/avatar/' + dir1 + '/' + dir2 + '/' + dir3

        if not os.path.exists(forum_avatar_dir_path):
            os.makedirs(forum_avatar_dir_path)

        avatar_name = prefix + '_avatar_' + size + extension
        forum_avatar_path = forum_avatar_dir_path + '/' + avatar_name
        if os.path.exists(forum_avatar_path):
            os.remove(forum_avatar_path)

        shutil.copyfile(main_avatar_path, forum_avatar_path)
