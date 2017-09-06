# -*- coding:utf-8 -*-
'''
  关于ADMIN的相关操作
'''
import urlparse
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
from utils.decorators import dec_login_required
from db.api.upload.uploader import Uploader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from utils.handle_exception import handle_http_response_exception,handle_ajax_response_exception
from django.template import RequestContext
from db.api.admin import AdminUsr as api_AdminUsr
from db.api.admin import role as api_role
from utils import tool
from utils.tool import get_correct_url
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from utils.logger import logger as log

url_back = ""


def admin_home(request):
    session_name = request.session.get('username')
    if session_name is None:
        return HttpResponseRedirect(reverse('admin_login'))
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


@require_http_methods(["GET", "POST"])
def admin_login(request):
    if request.method == 'GET':
        return render_to_response('loginindex.html', {}, context_instance=RequestContext(request))
    else:
        name = request.POST.get("name")
        password = request.POST.get("password")
        login_url = reverse('admin_login')

        if 'name' and 'password' in request.POST:
            user = api_AdminUsr.get_AdminUsr_by_name(name).result()
            if not user:
                return render_to_response('loginindex.html', {'error': '用户名或密码错误！'},
                                          context_instance=RequestContext(request))
            if not check_password(password, user["pwd"]):
                return render_to_response('loginindex.html', {'error': '用户名或密码错误！'},
                                          context_instance=RequestContext(request))
            menus = api_AdminUsr.get_menus_by_urser_id(user['id']).result()
            role = api_AdminUsr.get_role_by_user_id(user['id']).result()

            request.session['role'] = role
            request.session['role_menus'] = menus
            request.session['username'] = user["name"]
            request.session['userid'] = user['id']

            back_url = reverse('admin_home')
            try:
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    result = urlparse.urlsplit(referer)
                    host = request.META.get('HTTP_HOST', '')
                    if result.netloc == host and result.path not in [login_url, '/', '/login/']:
                        back_url = result.path + '?' + result.query
            except:
                pass
            return HttpResponseRedirect(back_url)
        return HttpResponseRedirect(login_url)


@handle_http_response_exception(501)
def admin_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(reverse('admin_login'))


@dec_login_required
@handle_http_response_exception(501)
def admin_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    name = tool.get_param_by_request(request.POST, 'name', "", str)
    remark = tool.get_param_by_request(request.POST, 'remark', '', str)
    _password = tool.get_param_by_request(request.POST, 'password', "123456", str)
    password = make_password(_password, None, settings.PWD_HASH_TYPE)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    if action == 'add':
        user = api_AdminUsr.get_AdminUsr_by_name_or_id(name, _id).result()
        if user:
            return render_to_response("mz_back/AdminUsr_add.html", {'error': '添加失败，用户名或id已存在！', 'action': 'add'},
                                      context_instance=RequestContext(request))
        adminUsr = api_AdminUsr.insert_AdminUsr(_id, name, remark, password)
        if adminUsr.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        adminUsr = api_AdminUsr.update_remark_AdminUsr(_id, remark)
        if adminUsr.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_back:admin_list")))


@dec_login_required
@handle_http_response_exception(501)
def admin_edit(request):
    '''
    :param request:
    :return:
    '''
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    adminUsr = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        adminUsr = api_AdminUsr.get_AdminUsr_by_id(_id)
        if adminUsr.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        adminUsr = adminUsr.result()[0]
    c = {"AdminUsrs": adminUsr, "action": action, "page_index": page_index}
    return render_to_response("mz_back/AdminUsr_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def admin_list(request):
    '''
    :param request:
    :return:
    '''
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    keyword = ''
    adminRoles = api_role.list_role_and_admin().result()
    roles = api_role.list_roles().result()
    if 'delete' not in action:
        request.session["url_back"] = request.get_full_path()

    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        adminUsr = api_AdminUsr.delete_AdminUsr(_id)
        if adminUsr.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(request.session.get("url_back", reverse("mz_back:admin_list")))
    elif action == 'search':
        keyword = tool.get_param_by_request(request.GET, 'keyword', "", str)
        adminUsr = api_AdminUsr.get_AdminUsr_by_keyword(page_index, settings.PAGE_SIZE, '%' + keyword + '%', )
        if adminUsr.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    else:
        adminUsr = api_AdminUsr.list_AdminUsr_by_page(page_index, settings.PAGE_SIZE)
        if adminUsr.is_error():
            # 处理错误
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"AdminUsrs": adminUsr.result()["result"], 'adminRoles': adminRoles, 'roles': roles, 'keyword': keyword,
         "page": {"page_index": page_index, "rows_count": adminUsr.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": adminUsr.result()["page_count"]}}
    return render_to_response("mz_back/AdminUsrs_list.html", c, context_instance=RequestContext(request))


@csrf_exempt
def upload_controller(request):
    result = ""
    action = request.GET.get("action", "")
    if action == "config":
        result = Uploader.get_config()

    elif action == "uploadimage" or action == "uploadfile" or action == "uploadvideo":
        file = request.FILES.get("upfile", None)
        uploadresult = Uploader.upload(file, action)
        result = uploadresult.info

    return HttpResponse(result)


@dec_login_required
@handle_http_response_exception(501)
def admin_role_save(request):
    user_id = tool.get_param_by_request(request.POST, 'user_id', 0, int)
    role_id = tool.get_param_by_request(request.POST, 'role', 0, int)
    update_ret = api_role.update_admin_role_by_user(role_id, user_id)
    if update_ret.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_back:admin_list")))


# @dec_login_required
# @handle_ajax_response_exception
# def is_had_the_user(request):
#     _id = tool.get_param_by_request(request.GET, 'id', 0, int)
#     name = tool.get_param_by_request(request.GET, 'name', '', str)
#     get_is_had_user = api_AdminUsr.get_AdminUsr_by_name_or_id(name, _id)
#     status = "success"
#     is_get = False
#     if get_is_had_user.is_error():
#         log.warn("get user by id or name failed.id=%s,name=%s" % (_id, name))
#         status = "fail"
#     result = get_is_had_user.result()
#     if result:
#         is_get = True
#     return dict(status=status, is_get=is_get)
