# -*- coding: UTF-8 -*-
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils import tool
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from db.api.feed_back import feed_back as api_feed_back
from django.conf import settings
from django.core.urlresolvers import reverse
from utils.logger import logger as log
from mz_common.feedback import export_excle_feed_back

FEED_TYPE_NAME = (u"bug", u"功能建议", u"交互体验", u"吐个槽", u"表个扬", u"课程建议")
@dec_login_required
@handle_http_response_exception(501)
def feed_back_list(request):

    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    get_keyword = ''
    if "delete" not in action:
        request.session["url_back_feedback"] = request.get_full_path()

    if 'delete' in action:
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        ret_delete = api_feed_back.delete_feed_back_by_id(_id)
        if ret_delete.is_error():
            log.warn('failed to delete the feed back! ')
            return render(request, '404.html', {})
        else:
            return HttpResponseRedirect(reverse('mz_common:feed_back_list'))

    elif 'search' in action:
        keyword = tool.get_param_by_request(request.GET, 'keyword', '', str)
        if keyword in FEED_TYPE_NAME:
            type = str(FEED_TYPE_NAME.index(keyword))
            get_feed_back = api_feed_back.get_feed_back_by_type(page_index, settings.PAGE_SIZE, '%' + type + '%', )
        else:
            get_feed_back = api_feed_back.get_feed_back_by_keyword(page_index, settings.PAGE_SIZE, '%' + keyword + '%', )
        if get_feed_back.is_error():
            log.warn('failed to get the result of search feed back! ')
            return render(request, "404.html", {})

    else:
        get_feed_back = api_feed_back.list_feed_back_by_page(page_index, settings.PAGE_SIZE)
        if get_feed_back.is_error():
            log.warn('failed to get the result of search feed back! ')
            return render(request, "404.html", {})
    feedbacks = get_feed_back.result()["result"]
    if feedbacks:
        for feedback in feedbacks:
            if feedback["feed_type"]:
                feedback["feed_type"] = FEED_TYPE_NAME[int(feedback["feed_type"])]
    c = {"feed_back": feedbacks, 'keyword': get_keyword,
         "page": {"page_index": page_index, "rows_count": get_feed_back.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_feed_back.result()["page_count"]}}
    return render(request, "mz_feedback/feedback.html", c)


@dec_login_required
@handle_http_response_exception(501)
def feedback_edit(request):
    id = tool.get_param_by_request(request.GET, "id", 0, int)
    get_backfeed = api_feed_back.get_feed_back_by_id(id)
    if get_backfeed.is_error():
        log.warn("get feedback by id failed .id=%s" % id)
        return render(request, "404.html", {})
    feedback = get_backfeed.result()
    if feedback:
        feedback["feed_type"] = FEED_TYPE_NAME[int(feedback["feed_type"])]
    return render(request, "mz_feedback/feedback_record.html", dict(feedback=feedback))


def feedback_save(request):
    id = tool.get_param_by_request(request.POST, "id", 0, int)
    record = tool.get_param_by_request(request.POST, "record", "", str)
    update_feedback = api_feed_back.update_feed_back_by_id(_id=id,record=record)
    if update_feedback.is_error():
        log.warn("update feedback failed.id=%s,record=%s" % (id, record))
        return render(request, "404.html", {})
    return HttpResponseRedirect(request.session.get("url_back_feedback", reverse("mz_common:feed_back_list")))


def export_excle(request):
    feed_back_data = api_feed_back.list_feed_back().result()
    bio = export_excle_feed_back.excle_export(feed_back_data)
    response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=feed_back.xls'
    response['Content-Length'] = len(bio.getvalue())
    return response

