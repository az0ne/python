# -*- coding: utf-8 -*-
import urllib2

url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
xml_string = """
	<xml>
	  <appid><![CDATA[wx2421b1c4370ec43b]]></appid>
	  <attach><![CDATA[支付测试]]></attach>
	  <bank_type><![CDATA[CFT]]></bank_type>
	  <fee_type><![CDATA[CNY]]></fee_type>
	  <is_subscribe><![CDATA[Y]]></is_subscribe>
	  <mch_id><![CDATA[10000100]]></mch_id>
	  <nonce_str><![CDATA[5d2b6c2a8db53831f7eda20af46e531c]]></nonce_str>
	  <openid><![CDATA[oUpF8uMEb4qRXf22hE3X68TekukE]]></openid>
	  <out_trade_no><![CDATA[1409811653]]></out_trade_no>
	  <result_code><![CDATA[SUCCESS]]></result_code>
	  <return_code><![CDATA[SUCCESS]]></return_code>
	  <sign><![CDATA[B552ED6B279343CB493C5DD0D78AB241]]></sign>
	  <sub_mch_id><![CDATA[10000100]]></sub_mch_id>
	  <time_end><![CDATA[20140903131540]]></time_end>
	  <total_fee>1</total_fee>
	  <trade_type><![CDATA[JSAPI]]></trade_type>
	  <transaction_id><![CDATA[1004400740201409030005092168]]></transaction_id>
	</xml>

"""
req = urllib2.Request(url="http://192.168.1.54:8000/pay/wechat/pay/return/",
                      data=xml_string,
                      headers={'Content-Type': 'application/xml'})
response = urllib2.urlopen(req)
json_read = response.read()
print json_read


# import qrcode
#
# img = qrcode.make('hweixin://wxpay/bizpayurl?pr=lkGrkBj')
# # img <qrcode.image.pil.PilImage object at 0x1044ed9d0>
#
# with open('test.png', 'wb') as f:
#     img.save(f)