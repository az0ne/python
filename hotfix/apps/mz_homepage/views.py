# -*- coding: utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import interface
import json
from utils.tool import JsonCommonEncoder
import db.api.common.homepage


def homepage(request):
    """首页Views"""

    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('homepage_html_0328')
        if html:
            return HttpResponse(html)

    template_vars = cache.get('homepage_front_0328')
    if not template_vars:
        template_vars = {}
        # banner
        banner_lst = db.api.common.homepage.get_banner(_enable_cache=True)
        if banner_lst.is_error():
            banner_lst = []
        else:
            banner_lst = banner_lst.result()
        template_vars['banner_lst'] = banner_lst

        # 精品课程
        hot_courses = db.api.common.homepage.get_hot_course_list(_enable_cache=True)
        if hot_courses.is_error():
            hot_course_data_list = []
        else:
            hot_course_data_list = hot_courses.result()
        template_vars['hot_course_data_list'] = hot_course_data_list

        # 首页课程广告
        career_newads = db.api.common.homepage.get_career_newad(_enable_cache=True)
        if career_newads.is_error():
            career_newad_list = []
        else:
            career_newad_list = career_newads.result()
        template_vars['career_newad_list'] = career_newad_list

        # 热门文章
        articles = db.api.common.homepage.get_home_page_articles(_enable_cache=True)
        if articles.is_error():
            article_data_list = []
        else:
            article_data_list = articles.result()

        # wiki
        wiki = db.api.common.homepage.get_home_page_wiki(_enable_cache=True)
        if wiki.is_error():
            wiki_list = []
        else:
            wiki_list = wiki.result()

        template_vars['article_data_list'] = article_data_list[:3]
        template_vars['wiki_list'] = wiki_list
        # 推广链接
        links = db.api.common.homepage.get_homepage_links(_enable_cache=True)
        if links.is_error():
            links = []
        else:
            links = links.result()
        template_vars['links'] = links

        template_vars = json.dumps(template_vars, cls=JsonCommonEncoder)

        cache.set('homepage_front_0328', template_vars, 5 * 60)
    template_vars = json.loads(template_vars)
    t = loader.get_template('index.html')

    html = t.render(RequestContext(request, template_vars))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('homepage_html_0328', html, 5 * 60)
    return HttpResponse(html)


def get_course_categorys(request):
    """获取专业列表"""
    keyword = request.GET.get('s', '').upper()
    courses_catagorys = interface.get_course_categorys()
    ret = list()
    for c in courses_catagorys:
        if keyword in c.upper():
            ret.append(c)
    if not ret:
        ret = [u'暂无数据']
    return JsonResponse(data=ret, safe=False)
