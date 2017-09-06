#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, django

if django.VERSION[1] > 5:
    pwd = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(pwd+"/..")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

from tornado_per_lps4_teacher_briefing import send_briefing_base

briefing_dict = dict(briefing9=['app_teacher_briefing', '【工作简报-待办任务】新的一天开始了，你目前还有%s条待办需要处理，加油吧~'],
                     briefing16=['app_teacher_briefing', '【工作简报-待办任务】温馨提示，老师截止目前您还有%s条待办信息需要处理~'],)


if __name__ == '__main__':
    briefing_num = None
    args = sys.argv
    print args
    if len(args) > 0:
        briefing_num = briefing_dict.get(args[1])
    print briefing_num
    if briefing_num:
        send_briefing_base(*briefing_num)
        print 'success'
    else:
        print u'没有这个简报模板'