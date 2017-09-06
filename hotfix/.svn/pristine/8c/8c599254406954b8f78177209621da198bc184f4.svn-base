# -*- coding: utf-8 -*-
from mz_platform.apis.common_sys_api import CommonSysApi


def set_tags4article_list(article_list):
    for article in article_list:
        article['tags'] = get_tags_by_article(article)


def get_tags_by_article(article):
    api = CommonSysApi.default_instance()
    tags = api.get_article_tags(article['id'])
    if tags:
        return tags.obj
    return []

