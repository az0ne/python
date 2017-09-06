// 拖拽验证
var captchaObjF,captchaObjF2,captchaObjF3;
function captcha(obj,ty,callback){
    callback = callback||function(){};
    var setting = {
        obj: obj,
        ty:ty
    };
    if(setting.ty == undefined){
      setting.ty = '';
    }
    var handler = function (captchaObj) {
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo(setting.obj);
        captchaObj.onSuccess(function(){
            $('.tab-pane.active .captcha').siblings('.v_sign_tips').removeClass('error').html('').show(500);
        });
        switch(setting.ty){
            case "mobile/":captchaObjF = captchaObj; break;
            case "verifyMobile/":callback.call(this,captchaObj); break;
            case "verifyEmail/":callback.call(this,captchaObj); break;
            case "":captchaObjF3 = captchaObj; break;
            default:captchaObjF2 = captchaObj;break;
        }
    };
    $.ajax({
        // 获取id，challenge，success（是否启用failback）
        url: "/geetest/getcaptcha/"+setting.ty,
        type: "get",
        dataType: "json", // 使用jsonp格式
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数，与创建Geetest实例时接受的参数一致
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "float", // 产品形式
                offline: !data.success,
            }, handler);
        }
    });
};