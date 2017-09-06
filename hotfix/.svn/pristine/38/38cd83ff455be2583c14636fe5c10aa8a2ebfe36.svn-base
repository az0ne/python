# -*- coding: utf-8 -*-

"""
@version: 2016/4/25
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/4/25 17:32
@note:  学生端-支付信息
"""
import os
import datetime
from core.common.db.util import exec_sql

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()
from mz_lps.models import ClassStudents, Class
from mz_pay.models import UserPurchase
from core.common.db.util import exec_sql

def pretty_dt(dt):
    assert isinstance(dt, datetime.datetime)
    return dt.strftime(u"%Y年%m月%d日(%H:%M)")


def get_user_orders(user_id):
    """
    获取用户订单信息
    :param user_id:用户id
    :return:list of dict
    """
    sql = """
    SELECT
        _pay.order_no,
        _pay.trade_no,
        _pay.date_pay,
        _pay.pay_type,
        _pay.pay_way,
        _pay.pay_money,
        _pay.discounted_price,
        _course.id AS ccourse_id,
        _course.`name` AS ccourse_name,
        _cs.created AS join_class_time,
        _cs.deadline AS cstudent_deadline,
        _cs. STATUS AS cstudent_status,
        _class.coding AS class_coding,
        _class.meeting_enabled,
        _class.lps_version
    FROM
        mz_pay_userpurchase AS _pay
    INNER JOIN mz_course_careercourse AS _course ON _course.id = _pay.pay_careercourse_id
    LEFT JOIN mz_lps_classstudents AS _cs ON _cs.student_class_id = _pay.pay_class_id
    AND _cs.user_id = _pay.user_id
    LEFT JOIN mz_lps_class AS _class ON _class.id = _pay.pay_class_id
    WHERE
        _pay.pay_status = 1
    AND _pay.user_id = %s
    ORDER BY
        _pay.id DESC
    """ % user_id
    ret = list()
    now = datetime.datetime.now()
    for order_no, trade_no, date_pay, pay_type, pay_way, pay_money, \
        discounted_price, course_id, course_name, join_class_time, cstudent_deadline, \
        cstudent_status, class_coding, meeting_enable, lps_version in exec_sql(sql):
        need_pay = bool(lps_version == '3.0' and cstudent_deadline
                        and cstudent_status == ClassStudents.STATUS_NORMAL
                        )
        if cstudent_deadline:
            need_pay = need_pay & (now < (cstudent_deadline + datetime.timedelta(days=5)))

        deadline_pay = cstudent_deadline + datetime.timedelta(days=5) if cstudent_deadline else None

        ret.append(
            dict(
                order_no=order_no,  # 订单号
                course_id=course_id,
                course_name=course_name,  # 支付课程

                class_meeting_enable = meeting_enable,

                text_join_class_time=date_pay.date().isoformat(),  # 入学时间

                pay_money=pay_money or '',  # 支付金额
                text_pay_type=UserPurchase.PAY_TYPES.get(pay_type),  # 支付类型

                text_pay_way=UserPurchase.PAY_WAYS.get(pay_way),  # 支付方式
                trade_no=trade_no,  # 交易号

                discounted_price=discounted_price,
                need_pay=need_pay,
                deadline=cstudent_deadline,
                deadline_pay=deadline_pay,
                text_deadline=pretty_dt(cstudent_deadline) if cstudent_deadline else '',
                text_deadline_pay=pretty_dt(deadline_pay) if cstudent_deadline else '',
            )
        )
    return ret


def is_pay_user(user_id):
    """
    判断是否为付费用户
    :param user_id:用户id
    :return:True or False
    """
    return ClassStudents.objects.filter(
        user_id=user_id,
        student_class__class_type=Class.CLASS_TYPE_NORMAL
    ).exists()


def test():
    print get_user_orders(104231)


if __name__ == "__main__":
    test()
