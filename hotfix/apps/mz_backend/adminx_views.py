# coding:utf8
from functools import partial

from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods, require_GET

from mz_backend.forms import OrderForm

__author__ = 'hidden'

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache

from django.template import loader, Context

from mz_common.decorators import superuser_required
from mz_lps2.calc_view import *

logger = logging.getLogger('mz_backend.views')

# 更新视频长度view
@superuser_required
def update_video_length_view(request):
    t = loader.get_template('mz_backend/update_video_length.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 加入班级界面
@superuser_required
def join_class_1_view(request):
    t = loader.get_template('mz_backend/join_class_1.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 学生退出班级第一步
@superuser_required
def quit_class_1_view(request):
    t = loader.get_template('mz_backend/quit_class_1.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 学生转换班级第一步
@superuser_required
def change_class_1_view(request):
    t = loader.get_template('mz_backend/change_class_1.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 订单查询
def order_list_view(request):
    if request.user.is_authenticated():
        if request.user.username != "919769614@qq.com" and \
                        request.user.username != "admin@maiziedu.com" and \
                        request.user.username != "hidden@maiziedu.com" and \
                        request.user.username != "editor@maiziedu.com":
            t = loader.get_template('mz_common/failure.html')
            result = t.render(Context({'reason': '权限不足，不能访问。'}))
            return HttpResponse(json.dumps({'html': result}))
    else:
        t = loader.get_template('mz_common/failure.html')
        result = t.render(Context({'reason': '权限不足，不能访问。'}))
        return HttpResponse(json.dumps({'reason': '还未登录，请登录后再刷新该页面。'}))

    keywords = request.REQUEST.get("keywords", "")
    pay_status = request.REQUEST.get("pay_status", "-1")
    if pay_status != '-1' and pay_status != '':
        order_list = UserPurchase.objects.filter(
            Q(user__username__icontains=keywords) |
            Q(order_no__icontains=keywords) |
            Q(trade_no__icontains=keywords),
            Q(pay_status=pay_status)
        ).order_by("-id")
    else:
        order_list = UserPurchase.objects.filter(
            Q(user__username__icontains=keywords) |
            Q(order_no__icontains=keywords) |
            Q(trade_no__icontains=keywords)
        ).order_by("-id")
    paginator = Paginator(order_list, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
        order_list = paginator.page(current_page)
    except(PageNotAnInteger, ValueError):
        order_list = paginator.page(1)
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)
    t = loader.get_template('mz_backend/order_list.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 生成优惠码
@superuser_required
def coupon_list_view(request):
    Money = request.REQUEST.get("Money", "")
    if Money != "":
        c = Coupon()
        c.surplus = 100
        c.coupon_price = str(Money)
        c.save()
        save_obj = Coupon.objects.order_by('-id')[0]
        for i in range(100):
            cd = Coupon_Details()
            code_sno = generate_random(16, 1)
            cd.code_sno = code_sno.upper()
            cd.coupon = save_obj
            cd.use_time = '0000-00-00 00:00:00'
            try:
                cd.save()
            except:
                i = i - 1
        status = '优惠码生成成功!'
        t = loader.get_template('mz_backend/coupon_list.html')
        result = t.render(Context(locals()))
        return HttpResponse(json.dumps({'html': result}))
    else:
        coupon_list = Coupon.objects.order_by("id")
        paginator = Paginator(coupon_list, 20)
        try:
            current_page = int(request.GET.get('page', '1'))
            coupon_list = paginator.page(current_page)
        except(PageNotAnInteger, ValueError):
            coupon_list = paginator.page(1)
        except EmptyPage:
            coupon_list = paginator.page(paginator.num_pages)
        t = loader.get_template('mz_backend/coupon_list.html')
        result = t.render(Context(locals()))
        return HttpResponse(json.dumps({'html': result}))


# 同步主站到论坛的头像
@superuser_required
def sync_avatar_view(request):
    t = loader.get_template('mz_backend/sync_avatar_view.html')
    result = t.render(Context())
    return HttpResponse(json.dumps({'html': result}))


# 显示当前的推荐阅读列表
@superuser_required
def recommend_reading_index(request):
    reading_type = request.REQUEST.get("reading_type", None)
    if reading_type and reading_type != '-1':
        readings = RecommendedReading.objects.filter(reading_type=reading_type)
    else:
        readings = RecommendedReading.objects.all()
    rearranged_readings = {RecommendedReading.ACTIVITY: [], RecommendedReading.NEWS: [], RecommendedReading.DISCUSS: []}
    for reading in readings:
        rearranged_readings[reading.reading_type] = reading
    t = loader.get_template('mz_backend/recommended_reading_index.html')
    result = t.render(Context({'readings': readings, 'rearranged_readings': rearranged_readings,
                               'choices': RecommendedReading.READING_TYPES}))
    return HttpResponse(json.dumps({'html': result}))


# 直播室列表
@superuser_required
def live_room_list(request):
    keywords = request.REQUEST.get("keywords", "")
    live_is_open = request.REQUEST.get("live_is_open", "-1")
    if live_is_open != '-1' and live_is_open != '':
        room_list = LiveRoom.objects.filter(
            Q(live_id__icontains=keywords) |
            Q(live_class__coding__icontains=keywords),
            Q(live_is_open=live_is_open)
        ).order_by("-id")
    else:
        room_list = LiveRoom.objects.filter(
            Q(live_id__icontains=keywords) |
            Q(live_class__coding__icontains=keywords)
        ).order_by("-id")
    paginator = Paginator(room_list, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
        room_list = paginator.page(current_page)
    except(PageNotAnInteger, ValueError):
        room_list = paginator.page(1)
    except EmptyPage:
        room_list = paginator.page(paginator.num_pages)
    t = loader.get_template('mz_backend/live_room_list.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 历史消息列表
@superuser_required
def msg_send_list(request):
    keywords = request.REQUEST.get("keywords", "")
    sendtarget = request.REQUEST.get("sendtarget", "")

    if sendtarget != '-2' and sendtarget != '':
        msg_list = MsgBox.objects.filter(
            Q(content__icontains=keywords),
            Q(sendtarget=sendtarget)
        ).order_by("-id")
    else:
        msg_list = MsgBox.objects.filter(
            Q(content__icontains=keywords)
        ).order_by("-id")

    paginator = Paginator(msg_list, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
        msg_list = paginator.page(current_page)
    except(PageNotAnInteger, ValueError):
        msg_list = paginator.page(1)
    except EmptyPage:
        msg_list = paginator.page(paginator.num_pages)
    t = loader.get_template('mz_backend/msg_send_list.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# 根据查询条件获取用户列表
def get_acauser_list(keywords, university):
    if university != '-1' and university != '':
        acausers = AcademicUser.objects.filter(
            Q(user__username__icontains=keywords) |
            Q(academic_course__name__icontains=keywords) |
            Q(owner_college__name__icontains=keywords, owner_college__level=2) |
            Q(stu_name__icontains=keywords) |
            Q(user_no__icontains=keywords),
            Q(owner_university__id=university, owner_university__level=1)
        ).order_by("-id")
    else:
        acausers = AcademicUser.objects.filter(
            Q(user__username__icontains=keywords) |
            Q(academic_course__name__icontains=keywords) |
            Q(owner_college__name__icontains=keywords, owner_college__level=2) |
            Q(stu_name__icontains=keywords) |
            Q(user_no__icontains=keywords)
        ).order_by("-id")

    return acausers


# 高校用户列表
def acauser_list(request):
    if request.user.is_authenticated():
        if request.user.username != "919769614@qq.com" and \
                        request.user.username != "admin@maiziedu.com" and \
                        request.user.username != "hidden@maiziedu.com" and \
                        request.user.username != "editor@maiziedu.com":
            t = loader.get_template('mz_common/failure.html')
            result = t.render(Context({'reason': '权限不足，不能访问。'}))
            return HttpResponse(json.dumps({'html': result}))
    else:
        t = loader.get_template('mz_common/failure.html')
        result = t.render(Context({'reason': '还未登录，请登录后再刷新该页面。'}))
        return HttpResponse(json.dumps({'html': result}))

    # 获取大学列表
    university_list = AcademicOrg.objects.filter(level=1)

    keywords = request.REQUEST.get("keywords", "")
    university = request.REQUEST.get("university", "-1")
    acausers = get_acauser_list(keywords, university)

    paginator = Paginator(acausers, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
        acausers = paginator.page(current_page)
    except(PageNotAnInteger, ValueError):
        acausers = paginator.page(1)
    except EmptyPage:
        acausers = paginator.page(paginator.num_pages)

    t = loader.get_template('mz_backend/acauser_list.html')
    result = t.render(Context(locals()))
    return HttpResponse(json.dumps({'html': result}))


# # 清除缓存
# def clear_cache(request):
#     cache.delete_many(['homepage_front','homepage_html'])
#     # cache._cache.flush_all()
#     t = loader.get_template('mz_common/success.html')
#     result = t.render(Context({'reason':'缓存清除成功。'}))
#     return HttpResponse(json.dumps({'html':result}))
#
# # 清除缓存
# def clear_courses_cache(request):
#     cache.delete_many(['career_course_list_new_html'])
#     # cache._cache.flush_all()
#     t = loader.get_template('mz_common/success.html')
#     result = t.render(Context({'reason':'缓存清除成功。'}))
#     return HttpResponse(json.dumps({'html':result}))

#lps2.0升级使用（暂时，升级首次执行,升级完后可删除）
# def lps2_pay_update(request):
#     try:
#         class_students = ClassStudents.objects.all()
#         for class_student in class_students:
#             unlock_stage_count = UserUnlockStage.objects.filter(user=class_student.user,
#                                               stage__career_course=class_student.student_class.career_course).count()
#             if unlock_stage_count == 1:
#                 if class_student.deadline is None:
#                     class_student.deadline = datetime.now() + timedelta(days=15)
#             elif unlock_stage_count > 1:
#                 class_student.deadline = None
#             else:
#                 continue
#             class_student.save()
#
#     except Exception as e:
#         print e
#         logger.error(e)
#         t = loader.get_template('mz_common/failure.html')
#         result = t.render(Context({'reason': '搞锤子，失败了的哇。'}))
#         return HttpResponse(json.dumps({'html':result}))
#     t = loader.get_template('mz_common/success.html')
#     result = t.render(Context({'reason': '支付信息升级成功。'}))
#     return HttpResponse(json.dumps({'html':result}))


# 手动录入订单
@superuser_required
@require_http_methods(["GET", "POST"])
def create_order(request):
    _render = partial(render, request, 'mz_backend/order_add.html')
    if request.method == "GET":
        pay_ways = OrderForm.PAY_WAYS.items()
        pay_ways.sort(key=lambda x: x[0])
        return _render({'pay_ways': pay_ways})
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except AssertionError as e:
                return JsonResponse(dict(success=False, error=str(e)))
            return JsonResponse(dict(success=True,
                                     url=reverse('backend:order_list_view')))
        else:
            errors = form.errors.as_data()
            # errors = [k+': '+';'.join([l.message for l in v])
            #           for k, v in errors.items()]
            errors = [u'\n'.join([l.code + ": " + l.message for l in v])
                      for v in errors.values()]
            return JsonResponse(dict(success=False, error=u'\n'.join(errors)))


# 用于手动录入订单时异步获取课程价格
@superuser_required
@require_GET
def get_course_price(request):
    try:
        student = request.GET['student']
        cls = request.GET['cls']
        pay_type = int(request.GET['pay_type'])
    except KeyError, e:
        data = {'success': False, 'error': u"缺少参数{0}".format(e)}
        return JsonResponse(data)

    if pay_type != 2:
        cls = OrderForm.get_cls(cls)
        if not cls:
            data = {'error': OrderForm.error_messages['cls_error']}
            return JsonResponse(data)
        c_course = cls.career_course
        data = {
            'success': True,
            'net_price': c_course.net_price,  # 全款价格
            'discounted_price': c_course.discounted_price,  # 优惠金额
            'contract_price': c_course.contract_price  # 合同价格
        }
        if pay_type == 0:  # 全款
            data.update({
                'final_payment_price':
                    data['net_price'] - data['discounted_price']
            })
        elif pay_type == 6:  # 无就业全款
            data['net_price'] = c_course.jobless_price
            data['discounted_price'] = 0   # 暂时没有优惠
            data['contract_price'] = c_course.jobless_price
            data.update({
                'final_payment_price':
                    data['net_price'] - data['discounted_price']
            })
        else:  # 试学
            data.update({'final_payment_price': c_course.try_price})
    else:
        order = UserPurchase.objects.filter(
            Q(user__email=student) | Q(user__mobile=student),
            Q(pay_class__coding=cls) | Q(pay_class__name=cls),
            pay_type=1, pay_status=1).first()
        if not order:
            data = {
                'success': False,
                'error': u"未找到试学订单，请检查支付类型，麦子账号，班级编号或名称"
            }
            return JsonResponse(data)
        data = {
            'success': True,
            'net_price': order.net_price,  # 全款价格
            'discounted_price': order.discounted_price,  # 优惠金额
            'contract_price': order.contract_price,  # 合同价格
            'final_payment_price': order.final_payment_price  # 应收款
        }
    return JsonResponse(data)
