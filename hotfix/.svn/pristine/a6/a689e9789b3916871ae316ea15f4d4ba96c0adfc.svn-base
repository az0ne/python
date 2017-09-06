# -*- coding: utf-8 -*-
__author__ = 'admin'

from django import template
from django.template import Context, Template, loader, resolve_variable
import string
from  datetime import *
import  time
from mz_course.views import *

register=template.Library()

@register.tag(name='first_lesson')
def first_lesson(parser,token):
    try:
        tag_name,course_id=token.split_contents()
    except :
        raise template.TemplateSyntaxError(" tag  error!")
    return find_first_lesson(course_id)

class find_first_lesson(template.Node):
    def __init__(self,course_id):
        self.course_id=template.Variable(course_id)
    def render(self, context):
        courseid = self.course_id.resolve(context)
        lesson_list = Lesson.objects.filter(course=courseid).order_by("index")
        if len(lesson_list) > 0:
            return str(lesson_list[0].id)
        else:
        	return '0'


@register.tag(name='first_careercourse')
def first_career(parser,token):
    try:
        tag_name,course_id=token.split_contents()
    except :
        raise template.TemplateSyntaxError(" tag  error!")
    return find_first_career(course_id)

class find_first_career(template.Node):
    def __init__(self,course_id):
        self.course_id = template.Variable(course_id)
    def render(self, context):
        courseid = self.course_id.resolve(context)
        course = Course.objects.get(pk=courseid)
        stage_set = course.stages_m.all()
        lesson_list = Lesson.objects.filter(course=courseid).order_by("index")
        if stage_set:
            re_str = "%s/%d-%d/"%(stage_set[0].career_course.short_name.lower(),courseid,lesson_list[0].id)
            return re_str
        else:
            re_str = "other/%d-%d"%(courseid,lesson_list[0].id)
            return re_str

@register.tag(name='remove_black_tag')
def first_career(parser,token):
    try:
        tag_name,input_str=token.split_contents()
    except :
        raise template.TemplateSyntaxError(" tag  error!")
    re_str = RemoveBlank(input_str)
    print re_str

class RemoveBlank(template.Node):
    def __init__(self,input_str):
        self.input_str = template.Variable(input_str)

    def render(self,context):
        input_str = self.input_str.resolve(context)
        return input_str.replace(' ','')

