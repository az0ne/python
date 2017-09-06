# -*- coding: utf-8 -*-

import djevn
djevn.load()

from mz_user.mz_oauth import WeiXinAuth2
from db.cores.cache import cache

def get_weixin_jsapi_ticket():
    """
    @brief　获取微信token，并缓存
    :return:
    """
    access_token = WeiXinAuth2.get_weixin_token()
    if not access_token:  # 获取token失败，不会影响主要业务，但需要发邮件报警，在外层实现发邮件
        return False, 'get token fail'
    try:
        cache.set('get_weixin_token', access_token, 5400)
    except Exception as e:  # 设置缓存失败，　不会影响主要业务，　但需要套发邮件报警，在外层实现发邮件
        return False, 'cache token fail: %s' % str(e)

    jsapi_ticket = WeiXinAuth2.get_weixin_jsapi_ticket(access_token)
    if not jsapi_ticket:  # 获取jsapi_ticket失败，不会影响主要业务，但需要发邮件报警, 在外层实现发邮件
        return False, 'get jaspi_ticket fail'
    try:
        cache.set('get_weixin_jsapi_ticket', jsapi_ticket, 5400)
    except Exception as e:
        return False, 'cache jsapi_ticket fail: %s' % str(e)
    return True, None

def call_weixin_token():
    result, msg = get_weixin_jsapi_ticket()
    if not result:
        print msg
        pass  # send mail here

def main():
    call_weixin_token()

if __name__ == '__main__':
    main()
