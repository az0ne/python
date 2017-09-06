# -*- coding: utf-8 -*-
import base64

from django.http.response import JsonResponse, HttpResponse
from interface import upload_img, get_voice_or_video_from_wechat, get_news, save_wechat_news, update_wechat_menu
from utils.decorators import dec_login_required
from mz_wechat.interface import get_material_by_id


@dec_login_required
def get_news_list(request):
    """
    获取图文数据
    :param request:
    :return:
    """

    page = request.GET.get('page', 1)
    content = request.GET.get('content', None)
    data = get_news(int(page), content)
    data.update(status='success')
    return JsonResponse(data)


@dec_login_required
def get_voice_or_video(request):
    """
    获取语音或者视频数据;列表
    :param request:
    :return:
    """
    material_type = request.GET.get('type')
    if material_type not in ['voice', 'video']:
        return JsonResponse({'status': 'false', 'message': u'类型不正确'})
    data = get_voice_or_video_from_wechat(material_type)
    return JsonResponse({'status': 'success', 'data': data})


@dec_login_required
def upload_img_to_wechat(request):
    """
    上传图片到微信
    :param request:
    :return: 返回图片素材ID
    """
    img = request.FILES.get('img', None)
    if not img:
        return JsonResponse({'status': 'false', 'message': u'图片为空'})
    try:
        result = upload_img(img)
        if result[0]:
            return JsonResponse({'status': 'success', 'data': result[1]})
        return JsonResponse({'status': 'false', 'message': result[1]})
    except Exception as e:
        return JsonResponse({'status': 'false', 'message': str(e)})


@dec_login_required
def sync_wechat_news(request):
    """
    同步微信图文到数据库
    :param request:
    :return:
    """
    try:
        save_wechat_news()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'message': str(e)})


@dec_login_required
def set_menu(request):
    """
    更新自定义菜单
    :param request:
    :return:
    """
    result = update_wechat_menu()
    if result[0]:
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'false', 'message': result[1]})


# @dec_login_required
def get_material_data(request):
    """
    通过素材id获取素材数据
    :param request:
    :return:
    """

    m_id = request.GET.get('m_id')

    material = get_material_by_id(m_id)
    if material[0]:
        return HttpResponse(material[1])
        # return JsonResponse({'status': 'success', 'real_data': material[1]})

    return JsonResponse({'status': 'false', 'message': material[1]})
