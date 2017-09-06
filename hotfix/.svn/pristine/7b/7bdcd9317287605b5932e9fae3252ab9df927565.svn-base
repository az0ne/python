# -*- coding: utf-8 -*-
__author__ = 'bobby'
from models import *
from datetime import datetime
from mz_user.models import UserProfile
from itertools import chain
from HTMLParser import HTMLParser



class FPSInfo(object):
    @classmethod
    def get_activity(self):
        actives = Activity.objects.using('fps').all().order_by("status", "-datetime_end")[:2]
        for activity in actives:
            activity_users = ActivityUser.objects.using('fps').filter(activity=activity).order_by("-id")[:5]
            user_list = []
            total_user = 0
            total_user = ActivityUser.objects.using('fps').filter(activity=activity).count()
            i = 0
            for activity_user in activity_users:
                if i > 3:
                    break
                user_id = activity_user.user.user
                user = UserProfile.objects.filter(id=user_id)
                if user:
                    user_list.append(user[0])
                    i += 1

            setattr(activity, 'activity_set', user_list)
            setattr(activity, 'total_user', total_user)
        return actives

    @classmethod
    def get_article(self):
        top_articles = Article.objects.using('fps').filter(is_head=True).order_by('-date_publish')[:6]
        top_num = top_articles.count()
        if top_num < 6:
            articles = Article.objects.using('fps').filter(privilege=3).order_by('-date_publish')[:6 - top_num]
            return chain(top_articles, articles)
        return top_articles

    @classmethod
    def get_ask(self):
        course_asks = CourseAsk.objects.using('fps').filter(is_head=True).order_by('-date_publish')[:1]
        asks = Ask.objects.using('fps').filter(is_head=True).order_by('-date_publish')[:1]
        if course_asks and asks:
            if course_asks[0].date_publish > asks[0].date_publish:
                ask = course_asks[0]
                setattr(ask, 'ask_url', '/group/course_ask/%s' % ask.id)
            else:
                ask = asks[0]
                setattr(ask, 'ask_url', '/group/ask/%s' % ask.id)
        elif course_asks:
            ask = course_asks[0]
            setattr(ask, 'ask_url', '/group/course_ask/%s' % ask.id)
        elif asks:
            ask = asks[0]
            setattr(ask, 'ask_url', '/group/ask/%s' % ask.id)
        else:
            ask = []
        if ask:
            user_id = ask.user
            user = UserProfile.objects.filter(id=user_id)
            if user:
                setattr(ask, 'ask_user', user[0])
            setattr(ask, 'ask_content', strip_tags(ask.content)[:100])
        return ask


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
