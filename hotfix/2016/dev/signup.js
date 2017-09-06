//初始化
var signInit = function(){
    //注册表单键盘事件
    $("#email_register_form").keydown(function(event){
        if(event.keyCode == 13){
            register_form_submit();
        }            
    });
    $('.sign-left .form-control').focus(function(){
        $(this).next('label').css({'transform': 'translateY(-18px)'});
    });
    $('.sign-left .form-control').blur(function(){
        if($(this).val() == ''){
            $(this).next('label').css({'transform': 'translateY(0px)'});
        }else{
            $(this).next('label').css({'color':'#5ECFBA'});
        }
    });

    var $div_li = $('.sign-tabs li'), OFF1 = true, OFF2 = true, refresh_count = 0;
    if(OFF1){
        captcha(".tab-pane.active .captcha1", 'mobile/');
        OFF1 = false;
    }
    
    $div_li.on('click',function(){
        var index = $div_li.index(this);
        if($(this).hasClass('active')){

        }else{
            $(this).addClass('active').siblings().removeClass('active');
            if(captchaObjF && $('#mobile_register_form .gt_input input').val().length > 0 ) {
                if(refresh_count > 10){
                    window.location.reload();
                }
                refresh_count++;
                captchaObjF.refresh();
            }
            if(captchaObjF2 && $('#email_register_form .gt_input input').val().length > 0) {
                if(refresh_count > 10){
                    window.location.reload();
                }
                refresh_count++;
                captchaObjF2.refresh();
            }   
        }
        
        $('.tab-pane.active .captcha').siblings('.v_sign_tips').removeClass('error').html('').show(500);
        $("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('error success').html('').show(500);
        $("label[for=password_m]").siblings('.p_sign_tips').removeClass('error success').html('8-20位，区分大小写，不支持空格').show(500);
        $("label[for=email]").siblings('.e_sign_tips').removeClass('error success').html('').show(500);
        $("label[for=password]").siblings('.e_sign_tips').removeClass('error success').html('8-20位，区分大小写，不支持空格').show(500);
        
        $('.tab-content .tab-pane').eq(index).addClass('active').siblings().removeClass('active');

        if(OFF1 && index == 0 ){
            captcha(".tab-pane.active .captcha1", 'mobile/');
            OFF1 = false;
        }
        
        if(OFF2 && index == 1){
            captcha(".tab-pane.active .captcha2", 'email/');
            OFF2 = false;
        }
        
        $('#verify_form').hide().siblings('#mobile_register_form').show();
        $('#email_form').hide().siblings('#email_register_form').show();

        if($('.active .form-control').val() != ''){
            $('.form-control').val('').next('label').css({'transform': 'translateY(0px)','color':'#999999'});
        }        
    });
    
    $('#id_mobile_code').on('blur keyup', function(){
        var userMobile = $(this).val(),mobile_code=$("label[for=mobile_code]");
        var telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[0-9]|18[0-9]|14[0-9])[0-9]{8}$/g;
        if(userMobile == null || userMobile == ''){
            mobile_code.siblings('.m_sign_tips').removeClass('success').addClass('error').html('请输入你的手机号').show(500);
        }else if(telReg.test(userMobile)){
            mobile_code.siblings('.m_sign_tips').removeClass('error').addClass('success').html('').show(500);
        }else if(!telReg.test(userMobile)){
            mobile_code.siblings('.m_sign_tips').removeClass('success').addClass('error').html('手机号码格式不正确').show(500);
        }
    });
    $('#id_password_m').on('blur keyup',function(){
        var password_m=$("label[for=password_m]");
        if($(this).val() == null || $(this).val() == ''){
            password_m.siblings('.p_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
        }else if($(this).val().length < 8){
            password_m.siblings('.p_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
        }else{
            password_m.siblings('.p_sign_tips').removeClass('error').addClass('success').html('').show(500);
        }
    });
    $('#id_email').on('blur keyup', function(){
        var userEmail = $(this).val(),email=$("label[for=email]");
        var emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(userEmail == null || userEmail == ''){
            email.siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入你的邮箱').show(500);
        }else if(emailReg.test(userEmail)){
            email.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
        }else if(!emailReg.test(userEmail)){
            email.siblings('.e_sign_tips').removeClass('success').addClass('error').html('注册账号需为邮箱格式').show(500);
        }else{
            email.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
        }
    });
    $('#id_password').on('blur keyup',function(){
        var password=$("label[for=password]");
        if($(this).val() == null || $(this).val() == ''){
            password.siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
        }else if($(this).val().length < 8){
            password.siblings('.e_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
        }else{
            password.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
        }
    });
    //注册
    $(".sign-left .btn-micv5").click(function(){
        register_form_submit($(this).attr("typeF"));
    });
    //再次发送
    $("#send-verify").click(function(){
        send_sms_code('verify_form','verify-tips');
    });
    
    $("#email_form .sendE a").unbind().click(function(){
        sendECount = setInterval(zy_Countdown,1000);
        $(".zy_success").removeClass("upmove");
        $(this).parent().hide();
        $(".sendE2").show().find("span").html("60s");   
        $.ajax({
            type: "GET",
            url: "/user/send_again_email",
            data: {username:$('#id_email').val()},
            dataType: "html",
            success: function(data){
                zy_str = "验证邮件发送成功";
                if(data){
                    zy_Countdown();
                }
            },
            error:function(){
                zy_str = "验证邮件发送失败";
            }
        });
    });
}
signInit();
// 注册提交
function register_form_submit(type){
    var current_register_form = type || "mobile_register_form";
    if(current_register_form == "mobile_register_form"){
        if($('.active .form-control').val().length > 0){
            $('.active .form-control').next('label').css({'transform': 'translateY(-18px)'});
        }       
        $.ajax({
            type: "POST",
            url:"/user/register/mobile_verify/",
            data:{
                'type': 'mobile',
                'mobile': $('#id_mobile_code').val(),
                'password_m': $('#id_password_m').val(),
                'geetest_challenge': $('.geetest_challenge').attr('value'),
                'geetest_validate': $('.geetest_validate').attr('value'),
                'geetest_seccode': $('.geetest_seccode').attr('value'),
                "mobile_code": '-11111'
            },
            beforeSend:function(XMLHttpRequest){
                $(".sign_btn").html("注册中...");
                $("sign_btn").attr("disabled","disabled");
            },
            success: function(data) {
                if(data.status == 'success'){
                    $.ajax({
                        type: "POST",
                        url:"/user/register/mobile/sendsms_signup/",
                        data:{
                            'mobile': $('#id_mobile_code').val(),
                            'geetest_challenge': $('.geetest_challenge').attr('value'),
                            'geetest_validate': $('.geetest_validate').attr('value'),
                            'geetest_seccode': $('.geetest_seccode').attr('value'),
                        },
                        success: function(data){                                    
                            if(data.mobile){
                                $(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
                                $('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.mobile).show(500);
                            }else if(data.captcha){
                                $(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
                            }else if(data.status == 'failure'){
                                $(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
                            }else{
                                $(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
                                $('#mobile_register_form').hide().siblings('#verify_form').show('fast',function(){
                                    $('.sign-tabs li').unbind('click');
                                });
                                show_send_sms(60);
                            }
                        }
                    });                    
                    
                    $('.user_mobile').html($("#id_mobile_code").val().substring(0,3)+"****"+$("#id_mobile_code").val().substring(8,11));
                    $('#verify-ok').on('click',function(){
                        $.ajax({
                            type: "POST",
                            url:"/user/register/mobile/",
                            data:{
                                'type': 'mobile',
                                'mobile': $('#id_mobile_code').val(),
                                'password_m': $('#id_password_m').val(),
                                'geetest_challenge': $('.geetest_challenge').attr('value'),
                                'geetest_validate': $('.geetest_validate').attr('value'),
                                'geetest_seccode': $('.geetest_seccode').attr('value'),
                                'mobile_code': $('#Verify').val(),
                                "partner": $('#reg_partner').val(),
                                "openid": $('#reg_openid').val(),
                                "invitation_code": $('#invitation_code').val()
                            },                              
                            success: function(data) {
                                if(data.mobile_code){
                                    $(".verify-tips").removeClass('success').addClass('error').html(data.mobile_code).show(500);
                                }else{
                                    window.location = '/user/sign_success/';
                                }
                            }
                        });
                    })
                }else{
                    if(data.mobile){
                        $(".m_sign_tips").addClass('error').html(data.mobile).show(500);
                    }else if(data.password_m){
                        $(".p_sign_tips").addClass('error').html(data.password_m).show(500);
                    }else if(data.captcha){
                        $('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
                    }
                }
                
            },
            complete: function(XMLHttpRequest){
                $(".sign_btn").html("注册");
                $(".sign_btn").removeAttr("disabled");
            }
        });
    }else if(current_register_form == "email_register_form"){
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/register/email/",
            data:{
                'type': 'email',
                'email': $('#id_email').val(),
                'password': $('#id_password').val(),
                'geetest_challenge': $('#email_register_form .geetest_challenge').attr('value'),
                'geetest_validate': $('#email_register_form .geetest_validate').attr('value'),
                'geetest_seccode': $('#email_register_form .geetest_seccode').attr('value'),
                "partner": $('#reg_partner').val(),
                "openid": $('#reg_openid').val(),
                "invitation_code": $('#invitation_code').val()
            },
            beforeSend:function(XMLHttpRequest){
                $(".sign_btn").html("注册中...");
                $(".sign_btn").attr("disabled","disabled");
            },
            success: function(data) {
                if(data.email){
                    $("label[for=email]").siblings('.e_sign_tips').addClass('error').html(data.email).show(500);
                }else if(data.password){
                    $("label[for=password]").siblings('.e_sign_tips').addClass('error').html(data.password).show(500);
                }else if(data.email_ue){
                    $('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.email_ue).show(500);
                }else if(data.captcha){
                    $('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
                }else{
                    $('#email_register_form').hide().siblings('#email_form').show();
                    $('.email-tips').addClass('success');
                    $('.user_email').html($('#id_email').val());
                }
            },
            complete: function(XMLHttpRequest){
                $(".sign_btn").html("注册");
                $(".sign_btn").removeAttr("disabled");
            }
        });
    }
}