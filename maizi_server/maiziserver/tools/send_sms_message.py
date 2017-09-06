# -*- coding: utf-8 -*-
import json
import sys

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

reload(sys)
sys.setdefaultencoding('utf8')

REGION = "cn-hangzhou"
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAI0BF1174TTfTR"
ACCESS_KEY_SECRET = "42XcU3ShfR8MfpBKQ51rsx5HmtXT45"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


def _encode_json_string(params):
    """
    返回json字符串
    :param params: python字典
    :return: json字符串
    """

    param_url = "{"

    for key in params:
        param_url += "\"" + key + "\"" + ":" + "\"" + str(params[key]) + "\"" + ","

    param_url = param_url[:-1] + "}"

    return param_url


def _decode_json_string(str):
    """

    :param str: json字符串
    :return: 返回一个字典
    """
    return json.loads(str)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    """
    发送短信的方法
    :param business_id:
    :param phone_numbers: 接受短信的手机号码
    :param sign_name: 短信签名
    :param template_code: 短信模板ID
    :param template_param: 短信模板变量替换JSON串
    :return: 发送成功返回True， 失败返回False
    """
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name);

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    return _decode_json_string(smsResponse)


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    """
    查询短信发送的结果
    :param biz_id:
    :param phone_number:
    :param page_size:
    :param current_page:
    :param send_date:
    :return:
    """

    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # 查询的手机号码
    queryRequest.set_PhoneNumber(phone_number)
    # 可选 - 流水号
    queryRequest.set_BizId(biz_id)
    # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # 必填-当前页码从1开始计数
    queryRequest.set_CurrentPage(current_page)
    # 必填-页大小
    queryRequest.set_PageSize(page_size)

    # 调用短信记录查询接口，返回json
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    # TODO 业务处理

    return queryResponse


def send_sms_daily(phone, total_score, params):
    """
    发送每日通知
    :param phone 手机号码
    :param total_score 每日的活跃学分
    :param params 短信模板接受的参数
    :return: 发送是否成功
    """
    __business_id = uuid.uuid1()
    sign_name = '麦子学院'

    param_url = _encode_json_string(params)

    if total_score > 0:
        # 活跃学分大于0 , 短信模板不一样
        template_code = "SMS_76475099"
    else:
        # 活跃学分等于0
        template_code = "SMS_76535092"

    api_result = send_sms(__business_id, phone, sign_name, template_code, param_url)

    return api_result

#
# __name__ = 'send'
if __name__ == 'send':

    # params = {
    #     'name': '邓麒文'
    # }

    params = {
        'name': '邓麒文',
        'vedio': 3,
        'test': 3,
        'task': 5,
        'order': 1,
        'coach': 2
    }

    # param_url = _encode_json_string(params)
    #
    # print param_url

    print send_sms_daily('15390496865', 10, params)

    # params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
    # api_result = send_sms(__business_id, "18782685754", "阿里云短信测试专用", "SMS_76035455", param_url)
    #
    # print api_result['Code']

if __name__ == 'query':
    print query_send_detail("1234567^8901234", "13000000000", 10, 1, "20170612")
