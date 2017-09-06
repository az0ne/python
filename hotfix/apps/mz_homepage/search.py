# -*- coding: utf-8 -*-

import json
import re
import requests
import time
import random
from django.shortcuts import render

from django.conf import settings
from mz_common.functions import paginater
from utils.logger import logger as log
from mz_platform.utils.view_tool import datetime_convert
import db.api.wiki.wiki
import db.api.course.lesson
import db.api.course.course
import db.api.course.career_course
import db.api.article.article
import db.api.search.fulltext_search


def get_search_course(request, keyword, page_index):
    """
        搜索职业技能
    """
    data = search_api(keyword, page_index, app='course')
    url_prefix = get_current_url(str(request.get_full_path()), "^(.*)-\d+$")
    data['url'] = url_prefix
    return render(request, 'mz_search_result/job_skill.html', data)


def get_search_article(request, keyword, page_index):
    """
        搜索文章干货
    """
    data = search_api(keyword, page_index, app='article')
    url_prefix = get_current_url(str(request.get_full_path()), "^(.*)-\d+$")
    data['url'] = url_prefix
    return render(request, 'mz_search_result/articles.html', data)


def get_search_wiki(request, keyword, page_index):
    """
        搜索技能WIKI
    """
    data = search_api(keyword, page_index, app='wiki')
    url_prefix = get_current_url(str(request.get_full_path()), "^(.*)-\d+$")
    data['url'] = url_prefix
    return render(request, 'mz_search_result/wiki_skill.html', data)


def search_api(keyword, page_index=1, app='course'):
    ori_keyword = keyword[:settings.SEARCH_KEYWORD_LENGTH].replace('u0023', '#').replace('u0022', '?')

    data = {'courses': random_get_threee_course(),
            'keyword': keyword, 'ori_keyword': ori_keyword,
            'app': app}

    try:
        page = int(page_index) - 1
        url = '{0}?app={1}&keyword={2}&page_size={3}&page={4}'.format(settings.SEARCH_API_URL,
                                                                      app, ori_keyword, settings.SEARCH_PAGESIZE, page)
        result = requests.get(url)
        search_result = json.loads(result.text)
    except Exception as e:
        log.error('request search api failed:{0}'
                  'request_url:{1}'.format(e, url))
        return data

    if result.status_code == 500:
        log.error('service error:{0}'.format(search_result['msg']))
        return data

    if result.status_code == 400:
        log.warn(search_result['msg'])
        return data

    if result.status_code == 200:

        if search_result['code'] != 200:
            log.warn('warn message:%s' % search_result.msg)
            return data

        if search_result['code'] == 200:
            # 分页
            page_count_list, page_index, start_index, end_index = paginater(page_index, settings.SEARCH_PAGESIZE,
                                                                            search_result['result']['total'], 2)
            if app == 'article':
                for ti in search_result['result']['items']:
                    if ti['publish_date']:
                        time_array = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ti['publish_date']) / 1000))
                        ti['html_publish_date'] = datetime_convert(time_array)
                    else:
                        ti['html_publish_date'] = 0
                article_id_list = get_search_result_id_list(search_result['result']['items'], 'id', 'article')
                article_tag = get_article_tag_name_and_tag_id(article_id_list)
                if article_tag:
                    for at in article_tag:
                        for a in search_result['result']['items']:
                            if at.get('key', '') == 'article_{0}'.format(str(a['id'])):
                                a['tags'] = at.get('tags', '')
                else:
                    log.info("get article tag from mongodb by article id list EMPTY!")

            if app == 'wiki':
                course_id_list = get_search_result_id_list(search_result['result']['items'], 'course_id', 'wiki')
                wiki_course = get_wiki_course_short_name_and_img_url(course_id_list)
                if wiki_course:
                    for wc in wiki_course:
                        for w in search_result['result']['items']:
                            if wc.get('key', '') == 'wiki_{0}'.format(str(w['course_id'])):
                                w['course_name'] = wc.get('name', '')
                                w['course_short_name'] = wc.get('short_name', '')
                                w['course_img_url'] = wc.get('img', '')
                else:
                    log.info("get wiki course from mongodb by article id list EMPTY!")

            if app == 'course':
                course_id_list = get_search_result_id_list(search_result['result']['items'], 'id', 'course')
                career_course = get_career_course_name(course_id_list)
                if career_course:
                    for cc in career_course:
                        for c in search_result['result']['items']:
                            if cc.get('key', '') == 'course_{0}'.format(str(c['id'])):
                                c['chapter_num'] = cc.get('chapter', '')
                                c['career_course_name'] = cc.get('names', '')[:1]
                                c['teacher_nick_name'] = cc.get('tea_ni_name', '')

                else:
                    log.info("get career course from mongodb by article id list EMPTY!")

            data.update({
                "searchResults": search_result,
                "page_count_list": page_count_list,
                "page_index": str(page_index),
                "page_count": page_count_list[-1] if page_count_list else '1'
            })

            return data


def get_search_result_id_list(search_result_list, field, splice_word):
    """
        把查询结果集中的每条id,合成一个id_list，并去重，用于sql语句where id in list中
    """
    id_list = []
    if not isinstance(splice_word, unicode):
        splice_word = splice_word.encode('utf-8')
    if not isinstance(splice_word, str):
        splice_word = str(splice_word)

    for srl in search_result_list:
        id_list.append('{0}_{1}'.format(splice_word, str(srl[field])))
    return list(set(id_list))


def for_search_result_add_new_value(new_value, old_value, compare_key, app, new_key):
    """
        给旧的结果集，添加新的key,value值，扩充数据
    """
    new_result_list = []
    for nv in new_value:
        for ov in reversed(range(len(old_value))):
            if nv[compare_key] == '{0}_{1}'.format(app, str(old_value[ov][compare_key])):
                for item in len(new_key):
                    old_value[ov][new_key[item]] = nv[new_key[item]]
                new_result_list.append(old_value[ov])
                # 把已添加新值的list删除，从而减少循环次数
                del old_value[ov]
    return new_result_list


def get_article_tag_name_and_tag_id(article_id_list):
    """
        根据文章ID，获取该文章有那些标签，默认最多只显示3个标签
    """
    article_tags = db.api.search.fulltext_search.get_article_tags(article_id_list)
    if article_tags.is_error():
        log.warn(
            'get article tag name from mongodb by article id list failed!'
            'article_id_list:{0}'.format(article_id_list)
        )
    else:
        return article_tags.result()


def get_wiki_course_short_name_and_img_url(course_id_list):
    """
       根据课程ID，获取课程的短名称，用于该wiki标题跳转页面
    """
    result = ''
    wiki_course = db.api.search.fulltext_search.get_wiki_course_meta(course_id_list)
    if wiki_course.is_error():
        log.warn(
            'get course name from mongodb by course id list failed!'
            'course_id_list: {0}'.format(course_id_list))
    if wiki_course.result():
        result = wiki_course.result()

    return result


def get_career_course_name(course_id_list):
    """
        根据小课程ID，获取职业课程的name,short_name和chapter_num
        short_name 职业课程的连接地址参数
        该小课程对于多个职业课程，只取一个
    """
    result = ''
    career_course = db.api.search.fulltext_search.get_course_career_names(course_id_list)
    if career_course.is_error():
        log.warn(
            'get career course name from mongodb by obj_id_list failed!'
            'obj_id_list:{0}'.format(course_id_list)
        )
    if career_course.result():
        result = career_course.result()
    return result


def get_career_course():
    """
        获取职业课程，默认获取前几条数据,如果不够就根据index排序
    """
    result = ''
    career_course = db.api.course.career_course.get_career_course_name_short_name_and_image()

    if career_course.is_error():
        log.warn('get career course name,short_name,image,course_color failed!')
    else:
        result = career_course.result()
    return result


def random_get_threee_course():
    """
        随机获取三个小课程
    """
    ran_course_id = ()
    result = ''

    all_course_id = db.api.course.course.get_all_course_course_id_list()
    if all_course_id.is_error():
        log.warn('get all course course id failed!')
        return ''
    if not all_course_id.result():
        log.info('course course table is empty!')

    if all_course_id.result():
        # 随机取三个course_id, type:tuple
        ran_course_id = tuple(random.sample(all_course_id.result(), 3))

        if ran_course_id:
            course = db.api.course.course.get_course_course(ran_course_id)

            if course.is_error():
                log.warn('get course the top three hits of data failed!')
            if course.result():
                result = course.result()

    return result


def get_current_url(url, regex_url):
    # 获取当前url的前缀用于分页，页数链接url地址拼接
    try:
        url_prefix = re.match(regex_url, url.rstrip("/")).groups()[0]

    except Exception as e:
        log.info(
            'invalid url: %s, details: %s' % (url, e)
        )

    return url_prefix
