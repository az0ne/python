# -*- coding: utf-8 -*-
# lewis
__author__ = 'Lewis'
from collections import OrderedDict
from mz_course.models import CareerCatagory,CourseCatagory
from utils.decorators_cache import cache_data

def get_courselist():
    """获取课程库的数据结构"""
    course_catagorys_dict = OrderedDict()
    career_catagory_lst = CareerCatagory.objects.all().order_by('id')
    for career_catagory in career_catagory_lst:
        course_catagory_lst = CourseCatagory.objects.filter(career_catagory=career_catagory)
        course_catagorys_dict[career_catagory.name] = course_catagory_lst
    return course_catagorys_dict

@cache_data(60 * 1)
def get_course_categorys():
    course_category_lst = CourseCatagory.objects.all().values_list('name',flat=True)
    return course_category_lst