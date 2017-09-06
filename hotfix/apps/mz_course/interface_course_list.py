# -*- coding: utf-8 -*-
from django.http.response import Http404
from mz_common.functions import paginater, safe_int
from mz_course.functions import get_keyword_course_list

import db.api.course.career
import db.api.course.catagory
import db.api.course.course
import db.api.course.tag
import db.api.course.keyword
import db.api.course.page_name_seo
import db.api.course.type_ad


def courses_list_interface(catagories='all', tag='all', sort_by='0', page_index=1, keyword=''):
    """
    课程列表页
    """
    # 取得参数并作必要的类型验证
    try:
        catagories = str(catagories)
        tag = str(tag)
        sort_by = str(sort_by)
        page_index = safe_int(page_index, 1)
        keyword = str(keyword)
    except ValueError:
        raise Http404

    ad_type = '1'
    page_name = '4'

    tag_name = db.api.course.tag.get_tag_name(tag).result()
    catagory_name = db.api.course.career.get_career_name(catagories).result()
    if tag_name:
        tag_name = tag_name[0]['name']
    if catagory_name:
        catagory_name = catagory_name[0]['name']

    # 取数据
    _catagories_list = db.api.course.career.get_career().result()  # 取分类
    career_tag_list = db.api.course.tag.get_tag_having_career_id().result()  # 取分类下的标签
    # 构造career_tag数据
    catagories_list = []
    for c in _catagories_list:
        c['tag_list'] = []
        for ct in career_tag_list:
            if ct['career_id'] == c['id']:
                c['tag_list'].append(ct)
        catagories_list.append(c)

    if tag != 'all' and catagories != 'all':
        course_list = db.api.course.course.get_tag_catagory_course(tag, catagories).result()
    elif tag != 'all':  # 如果有标签,根据标签取课程
        course_list = db.api.course.course.get_tag_course(tag).result()
    elif catagories != 'all':  # 此外,有分类,根据分类取标签和课程
        course_list = db.api.course.course.get_catagory_course(catagories).result()
    else:
        course_list = db.api.course.course.get_course().result()

    keyword_list = db.api.course.keyword.get_keyword().result()  # 取数据库里允许的关键词
    ad = db.api.course.type_ad.get_type_ad(ad_type).result()  # 根据ad_type取广告
    if ad:
        ad = ad[0]
    seo = db.api.course.page_name_seo.get_page_name_seo(page_name).result()  # 根据page_name取seo
    if seo:
        seo = seo[0]

    # 根据关键词取课程
    keyword_course_list = get_keyword_course_list(keyword, keyword_list)
    # 如果有keyword,返回根据关键词取的课程
    if keyword:
        course_list = keyword_course_list

    sort_by_dict = {'1': 'date_publish', '2': 'favorite_count', '3': 'click_count'}
    sort_by_dict_chinese = {'0': u'全部', '1': u'最新', '2': u'最热', '3': u'播放最多'}
    sort_by_list_chinese = sorted(sort_by_dict_chinese.iteritems(), key=lambda x: x[0])

    _sort_by = sort_by_dict.get(sort_by, '0')
    sort_by_chinese = sort_by_dict_chinese.get(sort_by, u'')

    # 排序
    if _sort_by != '0':
        course_list = sorted(course_list, key=lambda x: x[_sort_by], reverse=True)

    page_size = 15
    rows_count = len(course_list)
    page_aroud = 2  # 页数处于中间时,前后分别围绕的页数

    page_count_list, page_index, start_index, end_index = paginater(page_index, page_size, rows_count, page_aroud)
    course_list = course_list[start_index:end_index]

    return catagories_list, course_list, ad, seo, page_count_list, page_index, start_index, end_index, \
           catagories, tag, sort_by, keyword, tag_name, catagory_name, sort_by_chinese, sort_by_list_chinese, rows_count
