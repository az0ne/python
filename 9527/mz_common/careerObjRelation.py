# coding: utf-8
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.core.urlresolvers import reverse

import utils.tool
import db.api.common.careerObjRelation
import db.api.apiutils
import utils.handle_exception
import utils.decorators
from utils.logger import logger as log

URL = ''


@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerObjRelation_list(request):
    """
    :param request
    :return
    """
    result_dict = {
        'message':'',
        'state':''
    }

    page_size = settings.PAGE_SIZE

    action = utils.tool.get_param_by_request(request.GET, 'action', 'search', str)
    page_index = utils.tool.get_param_by_request(request.GET, 'page_index', '1', int)
    key_word = utils.tool.get_param_by_request(request.GET, 'keyword', '', str)
    search_type = utils.tool.get_param_by_request(request.GET, 'type', 'COURSE', str)

    if action == 'delete':
        id = utils.tool.get_param_by_request(request.GET, 'id', 0, int)
        careerobjrelation = db.api.common.careerObjRelation.delete_careerobjrelation(id=id)

        if careerobjrelation.is_error():
            log.warn("delete careerObjRelation by id failed!"
                     "id:{0}".format(id))

            result_dict['state'] = u'false'
            result_dict['message'] = u'delete error'

            return render(request,'mz_common/careerObjRelation_list.html',result_dict)

        if not careerobjrelation.result():
            log.info("delete result back None"
                     "id:{0}".format(id)
                     )

            result_dict['state'] = u'false'
            result_dict['error'] = u'delete result error'

            return render(request, 'mz_common/careerObjRelation_list.html', result_dict)
        result_dict['state'] = u'success'

        return JsonResponse(result_dict)

    result_dict['state'] = ''
    result_dict['message'] = ''

    if action == 'search':
        global URL
        URL = request.get_full_path()
        if key_word == '%':
            key_word1 = '\\' + key_word
        else:
            key_word1 = key_word

        if search_type == 'ARTICLE':
            careerobjrelation = db.api.common.careerObjRelation.search_careerobjrelation_article(
                article_title='%' + key_word1 + '%',
                page_index=page_index,
                page_size=page_size)
        else:
            careerobjrelation = db.api.common.careerObjRelation.search_careerobjrelation_course(
                course_name='%' + key_word1 + '%',
                page_index=page_index,
                page_size=page_size)

        if careerobjrelation.is_error():
            log.warn(
                "careerobjrelation list error"
                "list type:{0}".format(search_type)
            )
            result_dict['state'] = u'false'
            result_dict['message'] = u'list error'
            return render(request, 'mz_common/careerObjRelation_list.html', result_dict)
        if not careerobjrelation.result():
            log.info(
                "careerobjrelation list none"
                "list type:{0}".format(search_type)
            )
            result_dict['state'] = u'false'
            result_dict['message'] = u'list result error'
            return render(request, 'mz_common/careerObjRelation_list.html',result_dict)

        result = {
            'careerobjrelation': careerobjrelation.result()['result'],
            'key_word': key_word,
            'page': dict(page_index=page_index, page_size=page_size,
                         rows_count=careerobjrelation.result()['rows_count'],
                         page_count=careerobjrelation.result()['page_count'])
        }

        return render(request, 'mz_common/careerObjRelation_list.html', result)



@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerObjRelation_edit(request):
    """
    detail, course
    """
    id = utils.tool.get_param_by_request(request.GET, 'id', 0, int)
    action = utils.tool.get_param_by_request(request.GET, 'action', '', str)
    career_course = db.api.common.careerObjRelation.get_career_course()
    course_list = db.api.common.careerObjRelation.get_obj_id_list()
    if action == 'update':
        careerobjrelation = db.api.common.careerObjRelation.careerobjrelation_detail(id=id)
        result_dict = {
            'career_course': career_course.result(),
            'careerobjrelation_detail': careerobjrelation.result()
        }
        return render(request,'mz_common/careerObjRelation_update.html',result_dict)
    else:
        result_dict = {
            'career_course': career_course.result(),
            'course_list': course_list.result()
        }
        return render(request,'mz_common/careerObjRelation_add.html',result_dict)


@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerObjRelation_add(request):
    """
    post param
    """
    error = {
        'error':''
    }

    obj_id = utils.tool.get_param_by_request(request.POST, 'obj_id', '', int)
    obj_type = utils.tool.get_param_by_request(request.POST, 'obj_type', '', str)
    career_id = utils.tool.get_param_by_request(request.POST, 'career_id', '', int)
    is_actived = utils.tool.get_param_by_request(request.POST, 'is_actived', '', int)
    action = utils.tool.get_param_by_request(request.POST, 'action', '', str)

    save_careerobjrelation = db.api.APIResult()

    if action == 'add':

        if obj_type == 'COURSE':
            save_careerobjrelation = db.api.common.careerObjRelation.insert_careerobjrelation(obj_id=obj_id,
                                                                                              obj_type=obj_type,
                                                                                              career_id=career_id,
                                                                                              is_actived=is_actived)
        elif obj_type == 'ARTICLE':
            save_careerobjrelation = db.api.common.careerObjRelation.insert_careerobjrelation(obj_id=obj_id,
                                                                                              obj_type=obj_type,
                                                                                              career_id=career_id,
                                                                                              is_actived=is_actived)
        if save_careerobjrelation.is_error():
            log.warn(
                "add mz_common_careerobjrelation is error"
                "obj_id:{0}".format(obj_id)
            )
            error['error'] = u'add error'
            return render(request,'mz_common/careerObjRelation_add.html',error)
        if not save_careerobjrelation.result():
            log.info(
                "add mz_common_careerobjrelation result back none"
                "obj_id:{0}".format(obj_id)
            )
            error['error'] = u'add result error'
            return render(request,'mz_common/careerObjRelation_add.html',error)

        return HttpResponseRedirect(utils.tool.get_correct_url(URL, reverse('mz_common:careerobjrelation_list')))



@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerobjrelation_update(request):
    """
    update careerobjrelation states by id
    """
    error = {
        'error':''
    }
    update_actived = db.api.APIResult()

    id = utils.tool.get_param_by_request(request.POST, 'id', 0, int)
    is_actived = utils.tool.get_param_by_request(request.POST, 'is_actived', '', int)
    action = utils.tool.get_param_by_request(request.POST, 'action', '', str)

    if action == 'update':
        update_actived = db.api.common.careerObjRelation.update_careerobjrelation(id=id, is_actived=is_actived)

    if update_actived.is_error():
        log.warn(
            "update mz_common_careerobjrelation is_actived is error"
            "id:{0}".format(id)
        )
        error['error'] = u'update error'
        return render(request,'mz_common/careerObjRelation_update.html',error)
    if not update_actived.result():
        log.info(
            "update mz_common_careerobjrelation result back none"
            "id:{0}".format(id)
        )
        error['error'] = u'update result error'
        return render(request,'mz_common/careerObjRelation_update.html',error)

    return HttpResponseRedirect(utils.tool.get_correct_url(URL,reverse('mz_common:careerobjrelation_list')))


@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerobjrelation_ajax_check(request):
    """
    check exits
    """
    error_dict = {
        "error":''
    }

    obj_id = utils.tool.get_param_by_request(request.GET, 'obj_id', 0, int)
    career_id = utils.tool.get_param_by_request(request.GET, 'career_id', 0, int)
    is_actived = utils.tool.get_param_by_request(request.GET, 'is_actived', '', int)
    obj_type = utils.tool.get_param_by_request(request.GET, 'obj_type', '', str)
    action = utils.tool.get_param_by_request(request.GET, 'action', '', str)

    if action == 'add':
        is_exist = db.api.common.careerObjRelation.check_exist(obj_id=obj_id, career_id=career_id, obj_type=obj_type)
        if is_exist.result():
            error_dict['error'] = u'该记录已存在'
            return JsonResponse(error_dict)

        check_obj_id = db.api.common.careerObjRelation.check_obj_id(obj_id=obj_id,obj_type=obj_type)
        if not check_obj_id.result():
            if obj_type == 'COURSE':
                error_dict['error'] = u'该课程不存在'
                return JsonResponse(error_dict)

            if obj_type == 'ARTICLE':
                error_dict['error'] = u'该文章不存在'
                return JsonResponse(error_dict)

        if (is_actived == 1) and (obj_type == 'COURSE'):
            check_actived = db.api.common.careerObjRelation.select_is_actived(obj_id=obj_id, obj_type=obj_type)
            if check_actived.result():
                error_dict['error'] = u'课程已存在激活专业'
                return JsonResponse(error_dict)

        return JsonResponse(error_dict)

    if action == 'update':
        if (obj_type == 'COURSE') and (is_actived == 1):
            get_actived = db.api.common.careerObjRelation.select_is_actived(obj_id=obj_id, obj_type=obj_type)
            for actived in get_actived.result():
                if int(actived['career_id']) != career_id:
                    error_dict['error'] = u'课程已存在激活专业'
                    return JsonResponse(error_dict)

        return JsonResponse(error_dict)
