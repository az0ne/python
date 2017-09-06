# -*- coding:utf-8 -*-
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
django.setup()


def sync_message():
    from mz_common.models import MyMessage
    MyMessage.objects.filter(action_type=1, action_content__icontains='您已成功报名课程').update(action_type=50)
    MyMessage.objects.filter(action_type=1, action_content__icontains='已上传了').update(action_type=51)
    print 'success'
    
if __name__ == '__main__':
    sync_message()