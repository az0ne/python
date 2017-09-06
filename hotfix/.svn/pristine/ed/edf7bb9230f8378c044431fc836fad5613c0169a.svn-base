# -*- coding: utf-8 -*-

from datetime import datetime
from django import template

from mz_platform.utils.view_tool import datetime_convert

register = template.Library()


@register.tag(name='date_convert')
def date_convert(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except:
        raise template.TemplateSyntaxError(" tag  error!")
    return DateConvert(format_string)


class DateConvert(template.Node):
    def __init__(self, format_string):
        self.format_string = template.Variable(format_string)

    def render(self, context):
        times = self.format_string.resolve(context)
        return datetime_convert(times)
