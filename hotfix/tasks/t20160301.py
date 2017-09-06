# -*- coding: utf-8 -*-
"""
修复系统消息中的LPS链接
"""

__author__ = 'Jackie'

from tasks import djevn

djevn.load()

from mz_common.models import MyMessage

import re

_c = re.compile('<a href=[",\']/lps[2,3]/')


def main():
    objs = MyMessage.objects.filter(action_type__in=(1,))
    count = objs.count()

    for i, message in enumerate(objs):
        content = message.action_content
        tmp = _c.search(content)
        if not tmp:
            pass
        else:
            tmp = tmp.group()
            repl = tmp.replace('/lps2/', 'http://www.maiziedu.com/lps2/')
            repl = repl.replace('/lps3/', 'http://www.maiziedu.com/lps3/')
            message.action_content = content.replace(tmp, repl)
            message.save()
        print i + 1, '/', count


main()
