# -*- coding: utf-8 -*-

"""
@version: 2016/5/27
@author: Jackie
@contact: jackie@maiziedu.com
@file: seo.py
@time: 2016/5/27 10:02
@note:  ??
"""
import copy

keywords = u"麦子学院，IT职业培训，IT技能培训，IT在线教育，IT在线学习，编程学习，" \
           u"android,ios,php,java,python,html5,cocos2dx"
description = u"麦子学院IT技术文章专 注Android、python、iOS、物联网、产品经理、php、嵌入式、ui等IT技术分享，" \
              u"专门为互联网人才提供海量、优质的资源服务和信息分享，同时建立一个自由交流、学习探讨和共同" \
              u"提高的绝佳生态圈，让各类互联网爱好者和从业人员零距离交流。"
seo_dict = {'seo_title': '', 'seo_keyword': keywords, 'seo_description': description}


def get_seo_info(user):
    result = copy.deepcopy(seo_dict)
    if user.is_edu_admin():
        result.update(
            {'seo_title': u'%s老师-麦子学院' % user.staff_name})
    elif user.is_teacher():
        major = user.get_teacher_major()
        result.update(
            {'seo_title': u'%s-%s培训-麦子学院' % (user.staff_name, major)})
    elif user.is_student():
        result.update(
            {'seo_title': u'%s-麦子学院' % user.staff_name})
    return result
