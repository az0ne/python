/**
 * Created by strii on 11/22/16.
 */

$(function () {
    $('.pay_btn').off('touchstart').on('touchstart', function () {
        $(this).css({'background-color': 'rgba(23, 156, 22,0.8)'});
    });
});
wx.config({
    debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: app_id, // 必填，公众号的唯一标识
    timestamp: time_stamp, // 必填，生成签名的时间戳
    nonceStr: noncestr, // 必填，生成签名的随机串
    signature: signature,// 必填，签名
    jsApiList: ['chooseWXPay'] // 必填，需要使用的JS接口列表
});
var touchend = true;
$(".pay_btn").bind("touchend", function () {
    if (touchend) {
        touchend = false;
        $.ajax({
            url: '/wike/order/',
            data: {
                'course_id': course_id
            },
            type: 'POST',
            success: function (data) {
                if (data.success) {
                    wx.chooseWXPay({
                        timestamp: data.data.timeStamp.toString(), // 支付签名时间戳
                        nonceStr: data.data.nonceStr, // 支付签名随机串
                        package: data.data.package, // 统一支付接口返回的prepay_id参数值
                        signType: data.data.signType, // 签名方式
                        paySign: data.data.paySign, // 支付签名
                        success: function (res) {
                            // 支付成功后的回调函数
                            window.location.href = '/wike/course/' + course_id + '/'
                        }
                    });
                    touchend = true;
                } else {
                    alert(data.message);
                    touchend = true;
                }
            }
        });
    }
});