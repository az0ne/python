# -*- coding: utf-8 -*-

import os

env = os.environ.get("ENV", "local")

if env == "prod":
    SITE_URL = "http://www.maiziedu.com"
elif env == "staging":
    SITE_URL = "http://dev.microoh.com:99"
elif env == "local":
    from .local import SITE_URL
else:
    raise Exception("error environ: ENV=%s" % env)


"""
    weibo api
"""
WEIBO_KEY = '2530430363'
WEIBO_SECRET = 'f10567b9434dd893fb4c5db527d79c2d'
WEIBO_AUTH_CALLBACK = '/webo/callback'
WEIBO_CANCEL_AUTH_CALLBACK = '/webo/cancelcallback'


"""
    QQ第三方登陆
"""
QQ_ID = '101268310'
QQ_KEY = '726795013a96586ce218350829156d77'
QQ_AUTH_URL = 'https://graph.qq.com/oauth2.0/authorize'
QQ_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
QQ_OPENID_URL = 'https://graph.qq.com/oauth2.0/me'
QQ_AUTH_CANCELCALLBACK = 'http://www.maiziedu.com/qq/cancelcallback'
QQ_USERINFO_URL = 'https://graph.qq.com/user/get_user_info'



"""
    微信第三方登陆
"""
WEIXIN_ID = 'wx5262498657c1ba69'
WEIXIN_KEY = 'd4624c36b6795d1d99dcf0547af5443d'
WEIXIN_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
WEIXIN_AUTH_TOKEN_URL = 'https://api.weixin.qq.com/sns/auth'
WEIXIN_AUTH_URL = 'https://open.weixin.qq.com/connect/qrconnect'
WEIXIN_CALLBACK_URL = ''
WEIXIN_USERINFO_URL = 'https://api.weixin.qq.com/sns/userinfo'


"""
    展示互动直播室信息配置 开始
"""
LIVE_ROOM_USERNAME = "admin@maiziedu.com"
LIVE_ROOM_PASSWORD = "ef5a7fa94f8efbe14dae8760ff279162"
LIVE_ROOM_CREATE_API = "http://maiziedu.gensee.com/integration/site/training/room/created"
LIVE_ROOM_UPDATE_API = "http://maiziedu.gensee.com/integration/site/training/room/modify"
LIVE_ROOM_JOININFO_API = "http://maiziedu.gensee.com/integration/site/training/export/history"
LIVE_ROOM_EXPORTQA_API = "http://maiziedu.gensee.com/integration/site/training/export/qa"
LIVE_ROOM_GET_API = "http://maiziedu.gensee.com/integration/site/training/courseware/syn"
LIVE_ROOM_GET_API510 = "http://maiziedu.gensee.com/integration/site/training/record/syn"
LIVE_ROOM_DELETE_API = "http://maiziedu.gensee.com/integration/site/training/room/deleted"


"""
    UCENTER配置
"""
UC_KEY = 'a05a64BgUzzhmx9B8jOM+645p75plJTmYASlF6Y'
UC_API = 'http://localhost:8081/maiziedubbs/uc_server'
UC_CHARSET = 'utf-8'
UC_IP = '127.0.0.1'
UC_APPID = '2'
UC_PPP = '20'
UC_CLIENT_VERSION = '1.6.0'
UC_CLIENT_RELEASE = '20110501'


"""
    拉勾网接口
"""
LAGOU_PRODUCT_MANAGER_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduPM_words"
LAGOU_IOS_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduIos_words"
LAGOU_ANDROID_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduAndroid_words"
LAGOU_JOINT_PAI = "http://api.lagou.com/cooperation/data/api/AD__maizieduWlw_words"
LAGOU_EMBEDDED_PAI = "http://api.lagou.com/cooperation/data/api/AD__maizieduQrs_words"
LAGOU_WINPHONE_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduWinPhone_words"
LAGOU_COCOS2D_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduCocos2d_words"
LAGOU_WEB_API = "http://api.lagou.com/cooperation/data/api/AD__maizieduWeb_words"


"""
    信鸽推送
"""
XG_ACCESS_ID = "2100080798"
XG_SECRET_KEY = "854bdfc82d3eaa5add966ced34208cbd"


"""
    么分期相关参数设置
"""
MIME_PAY_URL = "https://yxtest.memedai.cn/merchantApp/merchant/open/submitOrder/maizi"
MIME_PAY_APPID = 'cbee4f49784e708addcc7c44'
MIME_PAY_KEY = '0326cce8f00d69ca35a21bd8295f77b2f5b087a0f3d4b70b76c6f70dcf2175e7'



# 短信发送配置
SMS_HOST = "yunpian.com"  # 短信服务器地址
SMS_PORT = 80  # 端口号
SMS_VERSION = "v1"  # 短信版本
SMS_APIKEY = "fe05905d4428388010950428571baee7"  # 短信的apikey
SMS_TPL_ID = 1  # 短信使用的短信模版ID
SMS_COMPANY = "麦子学院"
SMS_COUNT = 50  # 同IP一天内最大短信发送条数
SMS_MAX_COUNT_MOBILE = 3
SMS_MOBILE = 18280021954


######### 支付宝相关参数设置 开始 #############
# 合作身份者ID，以2088开头的16位纯数字
ALIPAY_PARTNER = '2088901464726023'
# 安全检验码，以数字和字母组成的32位字符
ALIPAY_KEY = 'ovh9hof0jv9ubbix196dbj2p3mrlb4re'
# 签约支付宝账号或卖家支付宝帐户
ALIPAY_SELLER_EMAIL = 'sundy@microoh.com'
# 交易过程中服务器通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
ALIPAY_NOTIFY_URL = SITE_URL + "/pay/alipay/notify/"
# 付完款后跳转的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
# return_url的域名不能写成http://localhost/js_php_utf8/return_url.php ，否则会导致return_url执行无效
ALIPAY_RETURN_URL = SITE_URL + "/pay/alipay/return/"
# 网站商品的展示地址，不允许加?id=123这类自定义参数
ALIPAY_SHOW_URL = ''
# 签名方式 不需修改
ALIPAY_SIGN_TYPE = 'MD5'
# 字符编码格式 目前支持 GBK 或 utf-8
ALIPAY_INPUT_CHARSET = 'utf-8'
# 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
ALIPAY_TRANSPORT = 'http'
# 移动端支付接口公钥
ALIPAY_PUBLIC_KEY = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRAFljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQEB/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5KsiNG9zpgmLCUYuLkxpLQIDAQAB'
# 移动端支付接口私钥
ALIPAY_PRIVATE_KEY = 'MIICdAIBADANBgkqhkiG9w0BAQEFAASCAl4wggJaAgEAAoGBALi5yfl041mwcwFE1yK2zhX35/lri2P4OPV1/UZ7OnUnWekQ47wCUrgFkfEVhZNfu10JmPTuiROi/0F8BGc2YkR0bDR4byDdLoZH5pvpngVsUTZ60B7sjQGdcFQmXU0ylExud1bsxh25BJTCffpD8o7qYSVZw9SuGx2zK9DRRmZRAgMBAAECgYASPJVKAVYolpjj+S3cCXwTAyRtpUZfmjPVV86nVKcSxc3EipxRBVGxRSuBR4SmZf8TUk09cQcrXx4gEuREZEQTHwWrsqNPehsdHFNCpBIrAITy0An/ZjtfZ9QcMJuWookqsSP5J9X4FnvnFsW1M1vx6gRy7WpY2whJc4s6I6CZgQJBAOSK4DXKYUVz1Cc1SaFyF2GkHQouJgbN5u+UOcFtb5eG0okml1B2wwHjeVNLKrKPBunFQZuLpt7r30tHA30MaekCQQDO60WHc10sKYPbMqsEo00iVt6GXNS5Uk8ExMH5AZ8p5fCBlGWQKGxYKxhSSGpkUOJgHCET3yRWdZM+o0qQp/ApAj9aKnBKyI2X2RraXSuvhlOzMgxC9/IIvTNfUht3NLXSEl79vTv1guVs2VIEiqNNzx/rGufHdlFfoa93A41cyIkCQGY7n/K4cQRszpTyh8SW2nlo6jEAlKmrnRcCD8RzpKwSy616IGQFVOKLCE0/MjG2NOK/gyhKS63cEZAVJbYrA2ECQFnbvqj7mZMvYgcYftuQek3AZ6hVWChhmJe7Fb3DDAeXIZcJX88nnpcNOgLZEaDimWwmtRTb9zNpaQL4JFRtXDs='
# 移动端异步回调地址
ALIPAY_APP_NOTIFY_URL = SITE_URL + "/pay/alipay/appnotify/"

######### 支付宝相关参数设置 结束 #############


"""
    weixin pay
"""
WEIXIN_PAY_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
WEIXIN_NOTIFY_URL = SITE_URL+"/pay/wechat/pay/return/"

WEIXIN_PAY_MCH_ID = "1261534001"
WEIXIN_PAY_APPID = "wxcaa4d9c16ae244f9"
WEIXIN_PAY_TRADE_TYPE = "NATIVE"
WEIXIN_PAY_KEY = "K1PIMnNjwJvB6qbu02vID5dNRuFEAigr"


WEIXIN_APP_PAY_MCH_ID = '1360697802'
WEIXIN_APP_PAY_APPID = 'wx5c3115efd5611f08'
WEIXIN_APP_PAY_TRADE_TYPE = 'APP'
WEIXIN_APP_PAY_KEY = 'OfdKd8dsDkl1Dkjfd738s299mz2GzHtz'

"""
    银联支付
"""
UNION_PAY_MER_ID = '898510157321001'
UNION_PAY_RETURN = SITE_URL + '/pay/union/return/'
UNION_PAY_NOTIFY =SITE_URL + '/pay/union/notify/'

# 微课
# 微信鉴权需要的http
WEIXIN_PAGE_URL_GET_CODE = 'https://open.weixin.qq.com/connect/oauth2/authorize'
WEIXIN_PAGE_URL_GET_TOKEN = WEIXIN_TOKEN_URL
WEIXIN_PAGE_URL_GET_USERINFO = WEIXIN_USERINFO_URL
APPID = 'wxcaa4d9c16ae244f9'
SECRET = '4a4bbf7cece290d20189af4c5b70ddb0'
WEIXIN_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
WEIXIN_JSAPI_TICKET = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'

"""
    分期乐支付
"""
FQL_PAY_MER_ID = 'MPA201607010000033'
FQL_PAY_KEY = '51c7aee94544656210245ff9c1355f58'
FQL_PAY_RETURN = SITE_URL + '/pay/fql/return/'
FQL_PAY_NOTIFY = SITE_URL + '/pay/fql/notify/'


"""
    易宝支付
"""
YEE_PAY_MER_ID = '10013650886'
YEE_PAY_MER_KEY = 'i6vht16gg1u25yk74uozky69k16lbyygq73div6fs28wzgqmqedp8oj8xcp6'
YEE_PAY_RETURN = SITE_URL + '/pay/yee/return/'


"""
    有贝分期
"""
UUBEE_PAY_MER_ID = '201607290000081003'
UUBEE_PAY_RETURN = SITE_URL + '/pay/uubee/return/'
UUBEE_PAY_NOTIFY = SITE_URL + '/pay/uubee/notify/'
