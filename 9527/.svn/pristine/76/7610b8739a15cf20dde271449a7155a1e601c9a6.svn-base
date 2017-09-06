# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required
from django.conf import settings
from db.api.homepage import homepage_article as api_homepageArticle
from utils import tool
from utils import logger as log
from utils.handle_exception import handle_http_response_exception

# 全局变量
CURRENT_URL = ''  # 记录查看或修改某一条数据前的url地址


@dec_login_required
@handle_http_response_exception(501)
def homepage_article_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    article_type = tool.get_param_by_request(request.GET, 'articleType', '0_全部', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    homepage_article = None
    if action == 'query' or action == 'search':
        global CURRENT_URL
        CURRENT_URL = request.get_full_path()
    if 'query' in action:
        homepage_article = api_homepageArticle.list_article_for_homepage_by_page(6, page_index)

    if "search" in action:
        article_type_id = int(article_type.split('_')[0])
        if article_type_id == 0:
            return HttpResponseRedirect(reverse('mz_homepage:homepageArticle_list'))
        homepage_article = api_homepageArticle.search_article_by_article_type_id(article_type_id, 6)

    if homepage_article.is_error():
        return render(request, '404.html', {})

    c = {"homepageArticles": homepage_article.result()["result"],
         "page": {"page_index": page_index, "rows_count": homepage_article.result()["rows_count"],
                  "page_size": 6,
                  "page_count": homepage_article.result()["page_count"],
                  }, "keyword": key_word, "articleType": article_type}
    return render_to_response("mz_homepage/homepage_article_list.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def homepage_article_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', 'edit', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 0, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', '', str)
    article_type = tool.get_param_by_request(request.GET, 'articleType', '', str)
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)

    homepage_article = api_homepageArticle.get_article_homepage_index(_id)

    if homepage_article.is_error():
        log.warn('get newarticle of homepage_index field by newarticle id failed!'
                 'newarticle_id:{0}'.format(_id))
        return render(request, '404.html', {})

    c = {"homepageArticle": homepage_article.result(), "page_index": page_index, "action": action, 'keyword': key_word,
         'articleType': article_type}
    return render(request, 'mz_homepage/homepage_article_edit.html', c)


@dec_login_required
@handle_http_response_exception(501)
def homepage_article_save(request):
    action = tool.get_param_by_request(request.POST, 'action', 'edit', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    article_type = tool.get_param_by_request(request.POST, 'articleType', '', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    homepage_index = tool.get_param_by_request(request.POST, 'homepage_index', 0, int)

    homepage_article = api_homepageArticle.update_homepage_article_of_homepage_index(_id, homepage_index)

    if homepage_article.is_error():
        log.warn('update newarticle table of homepage_index field by newarticle id failed!'
                 'newarticle_id: {0}'.format(_id))
        return render(request, '404.html', {})

    return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_homepage:homepageArticle_list')))