# -*- coding: utf-8 -*-
from CCPRestSDK import REST

#主帐号
accountSid= '8a48b551522ff9310152351ff2010f47'

#主帐号Token
accountToken= 'b17b0cdd2e4e4184a5737724cc1e989d'

#应用Id
appId='8a48b551522ff9310152390a830c18bb'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

def sendTemplateSMS(to,datas,tempId):

    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    print datas
    r = rest.sendTemplateSMS(to,datas,tempId)
    result = {}
    result['code'] = -1
    result['detal'] = ''
    if r['statusCode'] == '000000':
        result['code'] = 0

    return result
