# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from mz_course.interface_course_list import courses_list_interface


def courses_list_all(request):
    """
    课程列表页无参数
    """
    keyword = str(request.GET.get('catagory', ''))
    catagories_list, course_list, ad, seo, page_count_list, page_index, start_index, end_index, catagories, \
        tag, sort_by, keyword, tag_name, catagory_name, sort_by_chinese, sort_by_list_chinese, rows_count = \
        courses_list_interface(keyword=keyword)
    return render(request, "mz_course/course_list.html", locals())


def courses_list(request, catagories, tag, sort_by, page_index):
    """
    课程列表页
    """
    keyword = str(request.GET.get('catagory', ''))
    catagories_list, course_list, ad, seo, page_count_list, page_index, start_index, end_index, catagories, \
        tag, sort_by, keyword, tag_name, catagory_name, sort_by_chinese, sort_by_list_chinese, rows_count = \
        courses_list_interface(catagories, tag, sort_by, page_index, keyword)
    if catagories == 'all' and tag == 'all' and sort_by == '0' and page_index == '1' and keyword == '':
        return redirect('course:stage_course_list_all')
    return render(request, "mz_course/course_list.html", locals())
