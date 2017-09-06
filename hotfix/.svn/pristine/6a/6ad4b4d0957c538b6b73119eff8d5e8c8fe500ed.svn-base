// 顶部登录事件
function topRightLogin(){
    login_popup();
}


function detect_ie() {
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE ');
    var trident = ua.indexOf('Trident/');

    if (msie > 0) {
        // IE 10 or older => return version number
        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
    }

    if (trident > 0) {
        // IE 11 (or newer) => return version number
        var rv = ua.indexOf('rv:');
        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
    }

    // other browser
    return false;
}

// 找回密码表单提交
function find_password_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/",
        data:{
            'account':$('#id_account').val(),
            'geetest_challenge': $('#find_password_form .geetest_challenge').attr('value'),
            'geetest_validate': $('#find_password_form .geetest_validate').attr('value'),
            'geetest_seccode': $('#find_password_form .geetest_seccode').attr('value')
        },
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#findpassword_btn").html("提交中...");
            $("#findpassword_btn").attr("disabled","disabled");
        },
        success: function(data) {
            if(data.account){
                $("#findpassword-tips").html(data.account).show(500);
                //$("#id_account").focus();
            }else if(data.captcha){
                $("#findpassword-tips").html(data.captcha).show(500);
            }else if(data.email_ue){
                $("#findpassword-tips").html(data.email_ue).show(500);
            }else if(data.mobile){
                $("#findpassword-tips").html(data.mobile).show(500);
            }else{
                if($("#id_account").val().indexOf("@") > 0 ){
                    $("#findpassword-tips").html("找回密码邮件已发送").show(500);
                }else{
                    if(data.status == 'failure') {
                        $('#mobile_code_password_form_message').html("手机短信验证码发送失败！");
                    }else{
                        $('#mobile_code_password_form_message').html("手机短信验证码已发送，请查收！");
                        show_send_sms(60);
                    }
                    $('#id_mobile' +
                        '_f').val($("#id_account").val());
                    $('#forgetpswModal').modal('hide');
                    $('#forgetpswMobileModal').modal('show');
                }
            }
        },
        complete: function(XMLHttpRequest){
            $("#findpassword_btn").html("提交");
            $("#findpassword_btn").removeAttr("disabled");
        }
    });
}

var init = function(){
    $(".zy_close").on({
        "click":function(){
            $(this).parent().parent().parent().parent().parent().modal("hide");
        }
    });
    //第三方登录弹框验证
    if(login_popupvar) {
        login_popup();
    }

    //登录表单键盘事件
    $("#login_form").keydown(function(event){
        if(event.keyCode == 13){
            login_form_submit("login-form-tips");
        }
    });

    //首页-忘记密码表单键盘事件
    //captcha(".newcaptcha");
    $("#find_password_form").keydown(function(event){
        if(event.keyCode == 13){
            find_password_form_submit();
        }
    });

    //找回密码提交
    $("#findpassword_btn").click(find_password_form_submit);

    /*
     *  关闭登录框trace事件.
     */
    $("#login_close").click(function(){
        var path = document.location.pathname;

        // pathname以lps-开头则trace事件
        if (path.search(/^\/lps-\w+?\/$/) == 0) {
            var career_name = path.substring(5, path.length-1);

            maizi_trace.trace({
                "suid": get_cookie("maiziuid"),
                "action_id": "trace_lps4_login_cancel",
                "trace_career_name": maizi_trace.career_name()
            });
            console.log("lps4 pathname traced. career_name: " + career_name);
            return true;
        }
    });

}
init();