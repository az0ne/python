# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from django import template

from mz_platform.utils.view_tool import html_content_brief

register = template.Library()


@register.filter(name='content_brief')
def content_brief(content, length=120):
    length = int(length)
    return html_content_brief(content, length)
