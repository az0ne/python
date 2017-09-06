/*!
 * 注册, 找回密码 相关的JS
 */

$(function(){
    var $sendphoneyzm = $("#sendphoneyzm");
    var $captcha = $("#captcha");
    var $captcha_img = $("#captcha_img");

    // 渲染验证码的函数, 作为回调函数调用, 在主线程内防止阻塞
    function render_captcha_img(image_url){
        $captcha_img.attr("src", image_url);
    }

    // 渲染验证码
    get_captcha_image(render_captcha_img);

    // 更换验证码
    $captcha_img.bind("touchend", function(){
        get_captcha_image(render_captcha_img);
    });

    // 确定"发送手机验证码"和是否可用的函数
    var if_sms_bind = false;
    function make_sure_sms_disabled(){
        // 禁用"发送手机验证码"按钮
        if($captcha.val()==""){
            $sendphoneyzm.addClass("send").attr("disabled","disabled");
            if_sms_bind = false;
        } else {
            $sendphoneyzm.removeClass("send").removeAttr("disabled");
            if_sms_bind = true;
        }
    };

    // 确定"注册按钮"是否可用的函数
    var if_register_bind = false;
    function make_sure_register_disabled(){
        // 禁用"注册"按钮
        if($("#registerForm #telphone").val()=="" && $("#registerForm #captcha").val()=="" && $("#registerForm #phoneyzm").val()=="" && $("#registerForm #password").val()==""){
            $("#registerForm .btn").addClass("send").attr("disabled","disabled");
            if_register_bind = false;
        } else {
            $("#registerForm li>em").html("");
            //$(this).parent("span").removeClass("field-invalid");
            $("#registerForm .btn").removeClass("send").removeAttr("disabled");
            if_register_bind = true;
        }
    };

    // 确定"发送手机验证码"和"注册按钮"是否可用
    make_sure_sms_disabled();
    make_sure_register_disabled();

    // keyup, 重新检测"发送手机验证码"是否可用
    $captcha.keyup(make_sure_sms_disabled);

    // keyup, 重新检测"注册按钮"是否可用
    $("#registerForm input").keyup(make_sure_register_disabled);

    // 获取手机验证码执行之前, 检测是否符合执行条件
    function make_sure_send_sms_code(){
        if(if_sms_bind == true){
            get_sms_code();
        };
    };

    // 绑定"发送手机验证码"的响应函数
    $sendphoneyzm.bind("touchend", make_sure_send_sms_code);

    // 注册函数执行之前, 检测是否符合执行条件
    function make_sure_register(){
        if(if_register_bind == true){
            register();
        };
    };

    // 绑定"注册按钮"的响应函数
    $("#registerForm .btn").bind("touchend", make_sure_register);

    // 前端验证手机号是否合法
    function verify_phone_number(){
        var phone = $.trim($("#telphone").val());
        if (!phone || !/^0?1[3|4|5|8]\d{9}$/.test(phone)) {
            //$("#telphonetips").html("请输入正确手机号码").siblings("span").addClass("field-invalid");
            $("#telphonetips").html("请输入正确的手机号码");
            return false;
        }else{
            $("#telphonetips").html("");
            return true;
        };
    };

    // 前端验证验证码是否合法
    function verify_random_code(){
        var random_code = $.trim(captchaVal=$captcha.val());
        if(!random_code || !/^\w{6}$/.test(random_code)){  // 验证码为6位
            //$("#yzmtips").html("请输入正确的验证码").siblings("span").addClass("field-invalid");
            $("#yzmtips").html("请输入正确的验证码");
            return false;
        } else {
            $("#yzmtips").html("");
            return true;
        }
    };

    // 前端验短信验证码是否正确
    function verify_sms_code(){
        var sms_code = $.trim($("#phoneyzm").val());
        if (!sms_code || !/^\d{6}$/.test(sms_code)) {  // 短信验证码为6位, 纯数字
            $("#phoneyzmtips").html("请输入正确的手机验证码");
            return false;
        }else{
            $("#phoneyzmtips").html("");
            return true;
        };
    };

    // 前端验证密码是否合法
    function verify_password(){
        var password = $.trim($("#password").val());
        if (password.length < 8 || password.length > 20) {  // 密码为8到20位字符串
            $("#passwordtips").html("请输入正确的密码");
            return false;
        }else{
            $("#passwordtips").html("");
            return true;
        };
    };

    // 发送手机验证码之前, 短暂时间内,不可点击,
    function before_send_random_code(){
        $sendphoneyzm.addClass("send").attr("disabled","disabled");  //样式不可点击
        $sendphoneyzm.unbind("touchend");  //取消点击事件绑定
    };

    // 发送手机验证码之后, 恢复点击事件
    function after_send_random_code(){
        $sendphoneyzm.removeClass("send").val("重新发送验证码");  //样式可点击
        $sendphoneyzm.bind("touchend", make_sure_send_sms_code);  //绑定点击事件绑定
    };

    // 发送注册信息之前, 禁用注册按钮
    function before_register(){
        // 解除点击事件
        $("#registerForm .btn").unbind("touchend", make_sure_register);
        // 禁用4个输入框
        $("#registerForm #telphone,#registerForm #captcha,#registerForm #phoneyzm,#registerForm #password").attr("disabled","disabled").css("color","#000");
        // 修改"找回密码"按钮的样式
        $("#registerForm .btn").addClass("send").attr("disabled","disabled");
    }

    // 发送注册信息之后, 恢复注册按钮
    function after_register(){
        // 修改"找回密码"按钮的样式
        $("#registerForm .btn").removeClass("send").removeAttr("disabled");
        // 解除禁用4个输入框
        $("#registerForm #telphone,#registerForm #captcha,#registerForm #phoneyzm,#registerForm #password").removeAttr('disabled').css("color","#999");
        // 绑定点击事件
        $("#registerForm .btn").bind("touchend", make_sure_register);
    }

    // 随机验证码验证失败
    function show_error_info(data){
        if(data.mobile){  //手机号错误
            $("#telphonetips").html(data.mobile);
        } else if(data.captcha){  //验证码错误
            $("#yzmtips").html(data.captcha);
        } else if(data.mobile_code){  //手机验证码错误
            $("#phoneyzmtips").html(data.mobile_code);
        } else if(data.password_m){  //密码错误
            $("#passwordtips").html(data.password_m);
        };
    }

	// 重发送短信验证码计时
	// var sendOFF = true;
	function show_send_sms(times){
	    $sendphoneyzm.unbind("touchend");  //取消事件绑定
        $sendphoneyzm.addClass("send").val("发送中（" + times + "s）");
        var countdown = setInterval(function(){
            times--;
            $sendphoneyzm.val("发送中（"+times+"s）");
            if(times<=0){
                clearInterval(countdown);
                after_send_random_code();
                $captcha.removeAttr("disabled").css("color","#999"); //打开验证码输入框
            }
        },1000);
	}

    // 发送随机验证码
    function send_random_code(){
        $.ajax({
            type: "POST",
            url: "/user/register/wap_mobile_verify/",
            data: {
                mobile: $('#telphone').val(),
                mobile_code: '-11111',
                password_m: '-1111111',
                code: $('#captcha').val(),
                hash_key: captcha_key,
            },
            beforeSend:function(XMLHttpRequest){
                $captcha.blur().attr("disabled","disabled").css("color","#000");//禁用验证码输入框
                before_send_random_code();
            },
            success:function(data){
                if(data.status=="success"){
                    send_sms_code();
                } else {
                    show_error_info(data);
                    after_send_random_code();
                    $captcha.removeAttr("disabled").css("color","#999");
                }
            },
        });
    };

    // 发送手机短信随机码
    function send_sms_code(){
        $.ajax({
            type: "POST",
            url:"/user/register/mobile/sendsms_signup/",
            data:{
                'mobile': $("#telphone").val(),
            },
            success: function(data){
                //console.log(data)
                if(data.status == 'success'){
                    show_send_sms(60);
                } else {
                    show_error_info(data);
                    after_send_random_code();
                    $captcha.removeAttr("disabled").css("color","#999");
                }
            }
        });
    };

    // 发送注册信息
    function send_register_info(){
        $.ajax({
            type: "POST",
            url:"/user/register/wap_mobile/",
            data:{
                mobile: $('#telphone').val(),
                mobile_code: $('#phoneyzm').val(),
                password_m: $('#password').val(),
                code: $('#captcha').val(),
                hash_key: captcha_key,
            },
            beforeSend:function(XMLHttpRequest){
                before_register();
            },
            success: function(data){
                if(data.status == 'success'){
                    window.location = data.source_url;
                } else {
                    show_error_info(data);
                    after_register();
                }
            }
        });
    }



    // 发送手机验证码按钮 对应的函数
    function get_sms_code() {

        // var flag;

        // 前端验证手机号码是否合法
        if(verify_phone_number() == false){
            return;
        }

        // 前端验证验证码
        if(verify_random_code() == false){
            return;
        };

        // 验证随机验证码
        send_random_code();
    };

    // 注册按钮相应函数
    function register(){

        // 前端验证手机号码是否合法
        if(verify_phone_number() == false){
            return;
        }

        // 前端验证验证码
        if(verify_random_code() == false){
            return;
        };

        // 前端验证短信验证码是否合法
        if(verify_sms_code() == false){
            return;
        }

        // 前端验证密码是否合法
        if(verify_password() == false){
            return;
        }

        send_register_info();
    };

});