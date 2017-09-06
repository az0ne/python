# -*- coding: utf8 -*-

import db.api
from utils.logger import logger as log


def get_u_home_recommend_career(user_id):
    """
    获取个人中心推荐课程
    :param user_id: 用户id
    :return:
    """

    count = db.api.get_count_usercareer(user_id)
    if count.is_error():
        log.warn('get count user career failed. '
                 'user_id: {0}'.format(user_id))
        count = 0
    else:
        count = count.result()

    if count == 0:
        careers = db.api.get_recommend_careers()
        if careers.is_error():
            log.warn('get recommend careers failed.')
            careers = None
        else:
            careers = careers.result()
    else:
        return None

    return careers


def first_signup_recommend(user):
    """
    首次注册，推荐课程弹窗
    :param user:
    :return:
    """
    recommend_careers = None

    if user.is_recommend:
        recommend_careers = get_u_home_recommend_career(user.id)
        user.is_recommend = False
        user.save()

    return recommend_careers
