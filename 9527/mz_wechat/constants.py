# -*- coding: utf8 -*-


class MenuType(object):
    """
    菜单事件类型
    """
    TARGET = 1      # 菜单跳转
    CLICK = 2       # 菜单click事件
    MENU = 3        #主菜单

    map = {TARGET: u'菜单跳转',
           CLICK: u'菜单click事件',
           MENU: u'主菜单'}


class MessageType(object):
    """
    用户消息类型
    """
    BASIC = 1       # 普通消息
    KEY_WORDS = 2   # 关键字消息
    FOLLOW = 3      # 关注
    IMAGE = 4       # 图片消息

    map = {BASIC: u'普通消息',
           KEY_WORDS: u'关键字消息',
           FOLLOW: u'关注',
           IMAGE: u'图片消息'}


class ReplyType(object):
    """
    回复类型
    """
    TEXT = 1        # 回复文本
    IMAGE = 2       # 回复图片
    VIDEO = 3       # 回复视频
    VOICE = 4       # 回复语音
    NEWS = 5        # 回复图文

    map = {TEXT: u'文本',
           IMAGE: u'图片',
           VIDEO: u'视频',
           VOICE: u'语音',
           NEWS: u'图文'}


class MatchType(object):
    """
    匹配类型
    """
    CONTAIN = 0     # 包含
    EQUAL = 1       # 全匹配

    map = {CONTAIN: u'包含',
           EQUAL: u'全匹配'}
