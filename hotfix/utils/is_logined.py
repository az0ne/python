# -*- coding: utf-8 -*-
import db.api.lps.student
import db.api.onevone.meeting
from mz_lps4.class_dict import LPS4_DICT
from utils.logger import logger as log
from utils.tool import get_param_by_request


def is_logined(request):
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        return False
    else:
        return True


def student_in_career_required(request):
    """
    判断是否是lps4付费用户
    :return:
    """
    if not request.user.is_authenticated():
        raise Exception(u'unauthorized')
    user_id = request.user.id
    career_id = get_param_by_request(request.POST, "ccourse_id", 0, int)
    class_id = get_param_by_request(request.POST, "class_id", 0, int)
    meeting_id = get_param_by_request(request.POST, "meeting_id", 0, int)

    if not career_id and not class_id:
        # 通过meeting_id验证用户是否是lps4付费用户
        result = db.api.onevone.meeting.check_meeting_is_belong_to_user(meeting_id, user_id)
        if result.is_error():
            log.warn(u'check_meeting_is_belong_to_user error. career_id %s, user_id %s.' % (career_id, user_id))
            raise Exception(u'服务器开小差了，请稍后再试')
        if not result.result():
            raise Exception(u'请先报名')
        return

    if not career_id:
        # 通过class_id取career_id
        career_id = LPS4_DICT.get(class_id, 0)
    # 通过career_id验证用户是否是lps4付费用户
    career_student = db.api.lps.student.check_is_lps4_paid_user(career_id, user_id)
    if career_student.is_error():
        log.warn(u'check_is_lps4_paid_user error. career_id %s, user_id %s.' % (career_id, user_id))
        raise Exception(u'服务器开小差了，请稍后再试')
    if not career_student.result():
        raise Exception(u'请先报名')
