# -*- coding: utf-8 -*-

from captcha.views import verify_code
import json

def verify_captcha_code(request, hash_key, code):
    """
    @brief 包装captcha的verify_code函数, 判断验证码是否验证通过
    :param hash_key:
    :param code:
    :return:
    """
    result = verify_code(request, hash_key, code)
    result = json.loads(result.content)
    if result.get('status') == 'success':
        return True
    return False

