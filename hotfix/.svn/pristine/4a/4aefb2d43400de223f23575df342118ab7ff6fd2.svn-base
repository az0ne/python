$(function() {

    //$("#selectdate").dateSelector();
    //get_careercourse();
    //class_number();
    //create_class_save();
    page_click();
    for_back();
    load_more_index();
    //兼容IE9下placeholder不显示问题
    $('input, textarea').placeholder();

    //注册刷新验证码点击事件
    $('#email_register_form .captcha-refresh').click({'form_id':'email_register_form'},refresh_captcha);
    $('#email_register_form .captcha').click({'form_id':'email_register_form'},refresh_captcha);
    $('#mobile_register_form .captcha-refresh').click({'form_id':'mobile_register_form'},refresh_captcha);
    $('#mobile_register_form .captcha').click({'form_id':'mobile_register_form'},refresh_captcha);
    $('#find_password_form .captcha-refresh').click({'form_id':'find_password_form'},refresh_captcha);
    $('#find_password_form .captcha').click({'form_id':'find_password_form'},refresh_captcha);

    //登录表单键盘事件
    $("#login_form").keydown(function(event){
        if(event.keyCode == 13)
            login_form_submit("login-form-tips");
    });
    //注册表单键盘事件
    $("#email_register_form").keydown(function(event){
        if(event.keyCode == 13)
            register_form_submit();
    });
    $("#email_register_form").keydown(function(event){
        if(event.keyCode == 13)
            register_form_submit();
    });
    //首页-忘记密码表单键盘事件
    $("#find_password_form").keydown(function(event){
        if(event.keyCode == 13)
            find_password_form_submit();
    });

    //首页 - 课程搜索推荐
    "use strict";

    window.mz = window.mz || {};
    window.mz.config = {
        media_url: "{{ MEDIA_URL }}"
    };

    //var $hotkeyword = $("#hotkeyword"),
    //    $cf = $hotkeyword.find(".cf");
    //
    //$.get("/common/recommend_keyword/")
    //    .done(function(res) {
    //        var html = "";
    //        try {
    //            res.forEach(function(item) {
    //                html += "<li><a href='javascript:void(0);'>" + item.name + "</a></li>";
    //            });
    //        } catch(e) {
    //            html = "还没有推荐的关键词";
    //        }
    //
    //        $cf.html(html);
    //    })
    //    .error(function(xhr) {
    //        console.dir(xhr);
    //        $cf.html("还没有推荐的关键词");
    //    });
});

//刷新验证码
function refresh_captcha(event){
    $.get("/captcha/refresh/?"+Math.random(), function(result){
        $('#'+event.data.form_id+' .captcha').attr("src",result.image_url);
        $('#'+event.data.form_id+' .form-control-captcha[type="hidden"]').attr("value",result.key);
    });
    return false;
}

//登录成功跳转计时函数
function login_jump(tips_id,time, url){
    $("#"+tips_id).css("class","tips-error bg-success");
    $("#"+tips_id).html("正在登录,"+time+"秒后跳转...").show(500);
    time--;
    if (time == 0) {
        window.opener = null;
        window.location.href = url;
    }else {
        setTimeout("login_jump('"+tips_id+"',"+time+",'"+url+"')", 1000);
    }
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

//登录表单提交
function login_form_submit(tips_id){

    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/login/",
        data:$('#login_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#login_btn").html("登录中...");
            $("#login_btn").attr("disabled","disabled");
        },
        success: function(data) {
            if(data.account_l){
                $("#login-form-tips").html(data.account_l).show(500);
                $("#id_account_l").focus();
            }else if(data.password_l){
                $("#login-form-tips").html(data.password_l).show(500);
                $("#id_password_l").focus();
            }else{
                if(data.status == "success"){
		            window.location.replace(data.url);
                    if(detect_ie() !== false) {
                        window.location.reload();
                    }
                    return;
                }else if(data.status == "failure"){
                    $("#login-form-tips").html("账号或者密码错误，请重新输入").show(500);
                }
            }
        },
        complete: function(XMLHttpRequest){
            $("#login_btn").html("登录");
            $("#login_btn").removeAttr("disabled");
        }
    });
}

//注册表单提交
var current_register_form = "email_register_form";
function change_form(to_form_id){
    $("#register-tips").hide()
    current_register_form = to_form_id;
}
function register_form_submit(){
    if(current_register_form == "email_register_form"){
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/register/email/",
            data:$('#email_register_form').serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                $("#register_btn").html("注册中...");
                $("#register_btn").attr("disabled","disabled");
            },
            success: function(data) {
                if(data.email){
                    $("#register-tips").html(data.email).show(500);
                    $("#id_email").focus();
                }else if(data.password){
                    $("#register-tips").html(data.password).show(500);
                    $("#id_password").focus();
                }else if(data.captcha){
                    $("#register-tips").html(data.captcha).show(500);
                    $("#id_captcha_1").focus();
                    if(data.captcha == "验证码错误")
                        refresh_captcha({"data":{"form_id":"email_register_form"}});
                }else{
                    $("#register_btn").html("登录中...")
                    $("#id_account_l").val($("#id_email").val());
                    $("#id_password_l").val($("#id_password").val());
                    login_form_submit("register-tips");
                    return;
                }
            },
            complete: function(XMLHttpRequest){
                $("#register_btn").html("注册并登录");
                $("#register_btn").removeAttr("disabled");
            }
        });
    }else if(current_register_form == "mobile_register_form"){
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/register/mobile/",
            data:$('#mobile_register_form').serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                $("#register_btn").html("注册中...");
                $("#register_btn").attr("disabled","disabled");
            },
            success: function(data) {
                if(data.mobile){
                    $("#register-tips").html(data.mobile).show(500);
                    $("#id_mobile").focus();
                }else if(data.mobile_code){
                    $("#register-tips").html(data.mobile_code).show(500);
                    $("#id_mobile_code").focus();
                }else if(data.password_m){
                    $("#register-tips").html(data.password_m).show(500);
                    $("#id_password_m").focus();
                }else if(data.captcha_m){
                    $("#register-tips").html(data.captcha_m).show(500);
                    $("#id_captcha_m_1").focus();
                    if(data.captcha_m == "验证码错误")
                        refresh_captcha({"data":{"form_id":"mobile_register_form"}});
                }else{
                    $("#register_btn").html("登录中...")
                    $("#id_account_l").val($("#id_mobile").val());
                    $("#id_password_l").val($("#id_password_m").val());
                    login_form_submit("register-tips");
                    return;
                }
            },
            complete: function(XMLHttpRequest){
                $("#register_btn").html("注册并登录");
                $("#register_btn").removeAttr("disabled");
            }
        });
    }
}

//找回密码表单提交
function find_password_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/",
        data:$('#find_password_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#findpassword_btn").html("提交中...")
            $("#findpassword_btn").attr("disabled","disabled")
        },
        success: function(data) {
            if(data.account){
                $("#findpassword-tips").html(data.account).show(500);
                $("#id_account").focus();
            }else if(data.captcha_f){
                $("#findpassword-tips").html(data.captcha_f).show(500);
                $("#id_captcha_f_1").focus();
                if(data.captcha_f == "验证码错误")
                    refresh_captcha({"data":{"form_id":"find_password_form"}});
            }else{
                if($("#id_account").val().indexOf("@") > 0 ){
                    $("#findpassword-tips").html("找回密码邮件已发送").show(500);
                }else{
                    if(data.status == 'success'){
                        $('#mobile_code_password_form_message').html("手机短信验证码已发送，请查收！");
                    }else if(data.status == 'failure'){
                        $('#mobile_code_password_form_message').html("手机短信验证码发送失败！");
                    }
                    $('#id_mobile_f').val($("#id_account").val());
                    $('#forgetpswModal').modal('hide');
                    $('#forgetpswMobileModal').modal('show');
                }
                refresh_captcha({"data":{"form_id":"find_password_form"}});
            }
        },
        complete: function(XMLHttpRequest){
            $("#findpassword_btn").html("提交");
            $("#findpassword_btn").removeAttr("disabled");
        }
    });
}

//手机验证码表单验证
function mobile_code_password_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/mobile/",
        data:$('#mobile_code_password_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#mobile_code_password_btn").html("提交中...")
            $("#mobile_code_password_btn").attr("disabled","disabled")
        },
        success: function(data) {
            if(data.mobile_code_f){
                $("#mobile_code_password-tips").html(data.mobile_code_f).show(500);
                $("#id_mobile_code_f").focus();
            }else if(data.status == "success"){
                //忘记密码跳转到修改密码的界面前的合法性验证
                account = $("#id_account").val();
                code = $("#id_mobile_code_f").val();
                location.href="/user/password/reset/"+account+"/"+code;
            }
        },
        complete: function(XMLHttpRequest){
            $("#mobile_code_password_btn").html("提交");
            $("#mobile_code_password_btn").removeAttr("disabled");
        }
    });
}
//重发送短信验证码计时
function show_send_sms(time){
    $("#send_sms_btn").html(time+"秒后重发");
    if(time<=0){
        clearTimeout(send_sms_time);
        $("#register-tips").hide(500);
        $("#send_sms_btn").html("发送验证码").removeAttr("disabled");
        return;
    }
    time--;
    send_sms_time = setTimeout("show_send_sms("+time+")", 1000);
}

////发送手机验证码
//function send_sms_code(form_id,tips_id){
//    $.ajax({
//        cache: false,
//        type: "POST",
//        url:"/user/register/mobile/sendsms/",
//        data:$('#'+form_id).serialize(),
//        async: true,
//        beforeSend:function(XMLHttpRequest){
//            $("#register_btn").html("发送中...");
//            $("#register_btn").attr("disabled","disabled");
//        },
//        success: function(data) {
//            if(data.mobile){
//                $("#"+tips_id).html(data.mobile).show(500);
//                $("#id_mobile").focus();
//            }else if(data.captcha){
//                $("#"+tips_id).html(data.captcha).show(500);
//                $("#id_captcha_m_1").focus();
//                if(data.captcha_m == "验证码错误，请重新输入")
//                    refresh_captcha({"data":{"form_id":"mobile_register_form"}});
//            }else if(data.status == 'success'){
//                $("#"+tips_id).html("短信验证码已发送").show(500);
//                $("#send_sms_btn").attr("disabled","disabled");
//                show_send_sms(60);
//                refresh_captcha({"data":{"form_id":form_id}});
//            }else if(data.status == 'failure'){
//                $("#"+tips_id).html("短信验证码发送失败").show(500);
//                refresh_captcha({"data":{"form_id":form_id}});
//            }
//        },
//        complete: function(XMLHttpRequest){
//            $("#register_btn").html("注册并登录");
//            $("#register_btn").removeAttr("disabled");
//        }
//    });
//}

function get_careercourse(){
    $.ajax({
        type: "GET",
        async: false,
        url: "/user/get/careercourse/",
        dataType: "json",
        success: function(data){
            var data = eval(data);
            var str = '<option value="0" selected = "selected" >选择课程</option>';
            $(data).each(function(i,val) {
                // console.log(val);
                str += '<option id = "op-'+val.id+'" name="'+val.short+'" value="'+val.id+'">'+val.name+'</option>';

            });
            $('#select_course').html(str);
        }
    });
}

function class_number(){

   $('#select_course').change(function(){
        var na = $(this).find("option:selected").attr("name");
        var inx = $(this).find("option:selected").index();
        if(inx==0){
            $("#class-no").html("请选择课程生成班级号");
        }else{
            $("#class-no").html(na + get_se_date());
        }
   });

   $(".se-op").change(function(){
        if($('#select_course').val()==0){
            $("#class-no").html("请选择课程生成班级号");
        }else{
            var na = $("#select_course").find("option:selected").attr("name");
            $("#class-no").html(na + get_se_date());
        }

   });


}

function get_se_date(){
    var year = $("#selectdate_selectYear").find("option:selected").val();
    var month = $("#selectdate_selectMonth").find("option:selected").val();
    var date = $("#selectdate_selectDay").find("option:selected").val();
    month = month <= 9 ? "0"+month : month;
    date = date <= 9 ? "0"+date : date;
    return year  + month + date ;
}


function create_class_save(){

    $("#create-class").live("click",function(){
        if($('#select_course').val()==0){
            $("#class-no").html("请选择课程生成班级号");
        }else{
            classno = $("#class-no").html();
            $.ajax({
                type: "POST",
                url:"/user/create/class/save/",
                data:$('#form-create-save').serialize()+"&classno="+classno,
                async: true,
                beforeSend:function(XMLHttpRequest){
                    $("#create-class").html("保存中...");
                },
                success: function(data) {

                    if(data.message =="success"){
                            location.reload();
                    }else{
                        // alert(data.message);
                        $("#class_msg").html(data.message).addClass('bg-warning').addClass('bg-danger').show().delay(1500).fadeOut(500,function(){
                            $("#create-class").html("保存");
                        });

                    }
                    // for (i in data)
                    // {
                    //     msg = data[i];
                    //     alert(msg);


                    // }
                    // $("#class_msg").html("保存成功").removeClass('bg-warning').removeClass('bg-danger').addClass("bg-success").show().delay(3000).fadeOut();
                }
            });
        }

    });

}


function page_click(){
    $(".paginator_p").live('click',function(){
        var page = $(this).html();
        var type = $(this).parent().parent().parent().parent().parent().attr('id');
        page_li_click(type,page,false);
        $('#'+type+' .paginator_p_bloc').find(".selected").removeClass("selected");
        $(this).addClass("selected");
    })
}

function page_li_click(type,page,bools){
    $.ajax({
        type: "GET",
        url: "/common/course/list",
        data: {type:type, page:page},
        dataType: "json",
        beforeSend:function(){
        	if(bools){
        		$('.load-more').html('加载中...');
        	}
        },
        complete: function(msg) {
        	if(bools){
        		$('.load-more').html('加载更多');
        	}
    }
        ,
        success: function(data){
            var data = eval(data);
            var str = '';
            $(data).each(function(i,val) {
                    str +='<li class="col-xs-12 col-sm-6 col-md-6 col-lg-3">';
                    str +='<a href="/course/'+val.course_id+'/recent/play/"><dl><dt><div style="width:275px;height:174px;">'
                    str +='<img width="275px" height="174px" src="'+val.image+'"></div>';
                    str +='</dt><dd><span>'+val.name+'</span><p>'+val.student_count+'位同学正在学习</p></dd></dl></a></li>';
                });

                if(bools){
                	$("#"+type+" .page-item >ul").append(str);
                }else{
                	$("#"+type+" .page-item >ul").html($(str).hide().fadeIn(500));
                }
        }
    });
}

function for_back(){
    $('.backward').live('click',function(){
        var type = $(this).parent().parent().parent().attr('id');
        var p = $('#'+type+' .paginator_p_bloc').find(".selected").prev();
        if(p.length>0){
            $('#'+type+' .paginator_p_bloc').find(".selected").removeClass("selected");
            p.addClass("selected");
            p.prev().css("display","block");
            p.prev().prev().css("display","block");
            var index_val = $('#'+type+' .paginator_p_bloc').find(".selected").index();//当前index值
            if(index_val<4){
                var p_index = index_val-4;
                $('#'+type+' .paginator_p_bloc .paginator_p:lt('+p_index+')').css("display","block");
            }
            var pe = $('#'+type+' .paginator_p_bloc').find(".selected").html();
            page_li_click(type,pe,false);
        }

    });
    $('.forward').live('click',function(){
        var type = $(this).parent().parent().parent().attr('id');
        var p = $('#'+type+' .paginator_p_bloc').find(".selected").next();
        if(p.length>0){
            $('#'+type+' .paginator_p_bloc').find(".selected").removeClass("selected");
            p.addClass("selected");
            var index_val = $('#'+type+' .paginator_p_bloc').find(".selected").index();//当前index值
            if(index_val>4){
                var p_index = index_val-2;
                $('#'+type+' .paginator_p_bloc .paginator_p:lt('+p_index+')').css("display","none");
            }
            var pe = $('#'+type+' .paginator_p_bloc').find(".selected").html();
            page_li_click(type,pe,false);
        }

    });
}

function load_more_index(){
	$('.load-more').click(function(){
		type = $('.tabs-container div:visible').attr('id');
		p = $('#'+type+' .paginator_p_bloc').find(".selected").next();
        if(p.length>0){
            $('#'+type+' .paginator_p_bloc').find(".selected").removeClass("selected");
            p.addClass("selected");
            var index_val = $('#'+type+' .paginator_p_bloc').find(".selected").index();//当前index值
            if(index_val>4){
                var p = index_val-4;
                $('#'+type+' .paginator_p_bloc .paginator_p:lt('+p+')').css("display","none");
            }
            var pe = $('#'+type+' .paginator_p_bloc').find(".selected").html();
           	page_li_click(type,pe,true);
           	// $('.load-more').html('加载更多');
        }else{
        	$('.load-more').html('没有更多了');
        }
		// page_li_click(type,page,true);
	});
}


//职业课程详细列表，体验学习跳转函数
function learn_experience(obj){
     url = $("article h3").find("a").first().attr("href");
     if(typeof(url) != "undefined"){
        location.href = url;
     }
}

// 弹出登陆框
function login_popup(){
    $('#id_account_l').val("");
    $('#id_password_l').val("");
    $('#id_email').val("");
    $('#id_password').val("");
    $('#id_captcha_1').val("");
    $('#id_mobile').val("");
    $('#id_mobile_code').val("");
    $('#id_password_m').val("");
    $('#id_captcha_m_1').val("");
    $('#id_captcha_1').val("");
    $('#login-form-tips').hide();
    $('#findpassword-tips').hide();
    $('#mobile_code_password-tips').hide();
    $('#register-tips').hide();
    refresh_captcha({"data":{"form_id":"email_register_form"}});
    refresh_captcha({"data":{"form_id":"mobile_register_form"}});
    refresh_captcha({"data":{"form_id":"find_password_form"}});
    $('#loginModal').modal('show');
}