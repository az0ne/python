# -*- coding: utf-8 -*-
'''
支付宝接口
'''
import types
from urllib import urlencode, urlopen
from django.conf import settings
import hashlib, requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

# 网关地址
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'

# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
def params_filter(params):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key, sign_type = 'MD5'):
    if sign_type == 'MD5':
        return hashlib.md5(prestr + key).hexdigest()
    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee, extra_common_param):
    params = {}
    params['service']       = 'create_direct_pay_by_user'
    params['payment_type']  = '1'
    
    # 获取配置文件
    params['partner']           = settings.ALIPAY_PARTNER
    params['seller_email']      = settings.ALIPAY_SELLER_EMAIL
    params['return_url']        = settings.ALIPAY_RETURN_URL
    params['notify_url']        = settings.ALIPAY_NOTIFY_URL
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET
    params['show_url']          = settings.ALIPAY_SHOW_URL
    
    # 从订单数据中动态获取到的必填参数
    params['out_trade_no']  = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject']       = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body']          = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee']     = total_fee # 订单总金额，显示在支付宝收银台里的“应付总额”里
    
    # 扩展功能参数——网银提前
    params['paymethod'] = 'directPay'   # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    params['defaultbank'] = ''          # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379
    
    # 扩展功能参数——防钓鱼
    params['anti_phishing_key'] = ''
    params['exter_invoke_ip'] = ''
    
    # 扩展功能参数——自定义参数
    params['buyer_email'] = ''
    params['extra_common_param'] = extra_common_param

    # 扩展功能参数——分润
    params['royalty_type'] = ''
    params['royalty_parameters'] = ''
    
    params,prestr = params_filter(params)
    
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    
    return _GATEWAY + urlencode(params)


# app支付宝接口
def app_create_direct_pay_by_user(tn, subject, body, total_fee):
    data = dict(
        service='mobile.securitypay.pay',
        partner=settings.ALIPAY_PARTNER,
        _input_charset=settings.ALIPAY_INPUT_CHARSET,
        notify_url=settings.ALIPAY_APP_NOTIFY_URL,
        out_trade_no=tn,
        subject=subject,
        payment_type='1',
        seller_id=settings.ALIPAY_SELLER_EMAIL,
        total_fee=total_fee,
        body=body
    )
    _, prestr = params_filter(data)
    sign_string = rsa_sign(prestr)
    data['sign'] = sign_string
    data['sign_type'] = 'RSA'
    return urlencode(data)

# WAP 支付宝接口
def wap_create_direct_pay_by_user(tn, subject, body, total_fee, return_url):
    params = dict(
        service='alipay.wap.create.direct.pay.by.user',
        partner=settings.ALIPAY_PARTNER,
        _input_charset=settings.ALIPAY_INPUT_CHARSET,
        notify_url=settings.ALIPAY_NOTIFY_URL,
        return_url=return_url,

        out_trade_no=tn,
        subject=subject,
        total_fee=total_fee,
        seller_id=settings.ALIPAY_PARTNER,
        payment_type='1',
        show_url=settings.ALIPAY_SHOW_URL,
        body=body,
        app_pay='Y',
    )

    params, prestr = params_filter(params)
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)

def rsa_sign(data):
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/rsa_private_key.pem'
    with open(path, 'rb') as private_file:
        rsa_key = private_file.read()
    key = RSA.importKey(rsa_key)
    h = SHA.new(data)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature)


def notify_verify_rsa(post):
    _, data = params_filter(post)
    path = settings.PROJECT_ROOT + '/apps/mz_pay/pem/rsa_public_key.pem'
    with open(path, 'rb') as public_file:
        rsa_key = public_file.read()
    key = RSA.importKey(rsa_key)
    h = SHA.new(data)
    verifier = PKCS1_v1_5.new(key)
    if not verifier.verify(h, base64.b64decode(post.get('sign'))):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    partner = settings.ALIPAY_PARTNER
    notify_id = post.get('notify_id')
    veryfy_result = requests.get("https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s"
                                 % (partner, notify_id)).text
    if veryfy_result.lower().strip() == 'true':
        return True
    return False


def notify_verify(post):
    # 初级验证--签名
    _,prestr = params_filter(post)
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    if mysign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    partner = settings.ALIPAY_PARTNER
    notify_id = post.get('notify_id')
    veryfy_result = requests.get("https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s"
                                 % (partner, notify_id)).text
    if veryfy_result.lower().strip() == 'true':
        return True
    return False




