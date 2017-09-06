# -*- coding: utf8 -*-
import json

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseServerError, HttpResponseRedirect, Http404, HttpResponse

import db.api.mz_wechat.message
import db.api.mz_wechat.reply

from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.conf import settings

from mz_wechat import functions, interface
from mz_wechat.constants import MessageType, ReplyType
from mz_wechat.functions import get_reply_data
from utils import tool
from utils.logger import logger as log
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@require_http_methods(['GET', 'POST'])
@handle_http_response_exception(501)
def message_edit(request):
    if request.method == 'GET':
        action = request.GET.get('action', 'add')
        data = dict(action=action)
        if action != 'add':
            m_id = tool.get_param_by_request(request.GET, 'id', _type=int)
            rules = functions.get_rules(m_id)
            data.update(rules=rules)

        return render(request, 'mz_wechat/message_edit.html', data)

    else:
        page_index = tool.safe_positive_int(request.POST.get('page_index'), 1)
        m_type = tool.get_param_by_request(
            request.POST, 'message_type', MessageType.KEY_WORDS, int)
        keywords = request.POST.get('keywords', '')
        match_type = tool.get_param_by_request(request.POST, 'match_type', _type=int)
        reply_type = tool.get_param_by_request(request.POST, 'reply_type', _type=int)

        try:
            reply_data = get_reply_data(request, request.POST, reply_type)
        except Exception, e:
            return HttpResponse(u'错误信息：{0}'.format(e.message))

        if m_type == MessageType.KEY_WORDS:
            m = db.api.mz_wechat.message.add_message(m_type, keywords, match_type)
        else:
            m = db.api.mz_wechat.message.add_message(m_type)

        if m.is_error():
            log.warn('add message failed. '
                     'keywords: {0}, match_type: {1}'.format(keywords, match_type))
            return HttpResponseServerError()
        else:
            m = m.result()

        r = db.api.mz_wechat.reply.add_reply(reply_type, reply_data)
        if r.is_error():
            log.warn('add reply failed. '
                     'content: {0}'.format(keywords, reply_data))
            return HttpResponseServerError()
        else:
            r = r.result()

        res = db.api.mz_wechat.reply.add_reply_message(m, r)
        if res.is_error():
            log.warn('add reply_message failed. '
                     'content: {0}'.format(keywords, reply_data))
            db.api.mz_wechat.message.del_message(m)
            return HttpResponseServerError()
        else:
            return HttpResponseRedirect(
                reverse('mz_wechat:message_list') +
                '?action=query&page_index={0}'.format(page_index))


@dec_login_required
@require_http_methods(['GET'])
@handle_http_response_exception(501)
def message_list(request):
    action = tool.get_param_by_request(request.GET, 'action', default_val='query')
    page_index = tool.safe_positive_int(request.GET.get('page_index'), 1)
    page_size = tool.safe_positive_int(request.GET.get('page_size'), settings.PAGE_SIZE)
    keyword = tool.get_param_by_request(request.GET, 'keyword', default_val='')

    if action == 'delete':
        m_id = tool.get_param_by_request(request.GET, 'id', _type=int)
        result = db.api.mz_wechat.message.del_rules(m_id)
        if result.is_error():
            log.warn('delete rules failed. message id: {0}'.format(m_id))
            return HttpResponse('删除失败，请返回重试')
        return HttpResponseRedirect(
            reverse('mz_wechat:message_list') +
            '?action=query&page_index={0}'.format(page_index))

    rules_data = db.api.mz_wechat.message.get_rules_list(
        page_index, page_size, keyword)
    if rules_data.is_error():
        log.warn('get rules list failed.')
        rules_data = {}
    else:
        rules_data = rules_data.result()

    return render(request, 'mz_wechat/message_list.html', rules_data)


@dec_login_required
@require_http_methods(['GET'])
@handle_http_response_exception(501)
def sync_rules(request):
    mapper = {
        'text': ReplyType.TEXT,
        'img': ReplyType.IMAGE,
        'video': ReplyType.VIDEO,
        'voice': ReplyType.VOICE,
        'news': ReplyType.NEWS,
    }

    rules = interface.get_rules()
    if not rules[0]:
        raise Exception(u'获取规则失败')
    rules = rules[1]

    # 关注
    follow = rules.get('add_friend_autoreply_info')
    if follow:
        msg = dict(type=MessageType.FOLLOW)
        reply = dict(type=mapper[follow['type']], content=follow['content'])
        db.api.mz_wechat.message.add_rules(msg, reply)
        log.info('follow done.')

    # 默认回复，普通消息
    default = rules.get('message_default_autoreply_info')
    if default:
        msg = dict(type=MessageType.BASIC)
        reply = dict(type=mapper[default['type']], content=default['content'])
        db.api.mz_wechat.message.add_rules(msg, reply)
        log.info('default done.')

    # 关键字
    keywords_list = rules.get('keyword_autoreply_info')
    if keywords_list:
        keywords_list = keywords_list.get('list')
        for keywords in keywords_list:
            key = '|'.join([k['content'] for k in keywords['keyword_list_info']])
            msg = dict(type=MessageType.KEY_WORDS, key=key)

            reply_list = keywords['reply_list_info']
            for rep in reply_list:
                if rep['type'] == 'news':
                    reply = dict(type=mapper[rep['type']], content=json.dumps(rep))
                else:
                    reply = dict(type=mapper[rep['type']], content=rep['content'])
                db.api.mz_wechat.message.add_rules(msg, reply)
    log.info('keywords done.')


@dec_login_required
@require_http_methods(['GET'])
@handle_http_response_exception(501)
def manual_update(request):
    return render(request, 'mz_wechat/manual_update.html')
