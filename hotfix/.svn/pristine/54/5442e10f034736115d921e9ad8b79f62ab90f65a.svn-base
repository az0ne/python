$(function() {
    /* 用户昵称截取 */
    var _Login = $('.topRight').attr('login');
    if(_Login == 'True'){
        var _nickName = $('.nick_name a:first-child');
        if(_nickName.attr('data-name').length >= 4){
            _nickName.text(_nickName.attr('data-name').substring(0,4)+'···');
        }else{
            _nickName.text(_nickName.attr('data-name'));
        }
    }


    /* 顶部搜索 */

    $('.hot-words a').attr('href', '/search/course/web前端-1/');
    $('.hot-words a:first-child').attr('href', '/search/course/产品经理-1/');
    $('.hot-words a:last-child').attr('href', '/search/course/ui-1/');

	$(".search-btn").click(function(){
		sreachBtn($("#data-search").val());
	});

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

    //zhouyi:7-30 发送验证邮件事件
	$(".sendE a").click(function(){
		$(".zy_success").removeClass("upmove");
		$(this).parent().hide();
		$(".sendE2").show().find("span").html("60s");

        $.ajax({
             type: "GET",
             url: "/user/send_again_email",
             data: {username:zyUname},
             dataType: "html",
             success: function(data){
                 zy_str="验证邮件发送成功";
                 //console.log(data)
                 if(data)
                    zy_Countdown();
             },
            error:function(){
                zy_str="验证邮件发送失败";
            }

         });


	});

    $(".toolbar-item-weibo>div").hover(function(){

	},function(){
		$(this).stop().hide("fast");
	});
    $(".toolbar-item-weibo").click(function(){
        $(".lixianB").show();
    });
    $(".toolbar-item-weixin").click(function(){
        $("#KFLOGO .Lelem").trigger("click");
    });
    var wttm=false;
	$(".wap_top_tou>a").unbind().bind({
		"touchend":function(){
			var mm=$(".wap_top_tou_menu");
			if(mm.css("display")=="none"){
				$(".wap_top_tou_menu").show();
			}
			else{
				$(".wap_top_tou_menu").hide();
			}
		}
	});
    $(".wap53").unbind().click(function(){
        location.href=$("#mobile_icon_div").attr("href");
    });
    $(".topSreachTxt").keydown(function(event){
        if(event.keyCode == 13)
            sreachBtn($(this).val());
    });
    $(".toolbar-item-gotop").click(function(){
        $('html,body').stop().animate({scrollTop: '0px'}, 800);
    });
    $("#data-search").keyup(function (event) {
            var e = event || window.event ;
            if (e && e.keyCode == 13) {
                sreachBtn($(this).val());
                return;
            }
        });

});
function checkTime(i){
   if (i < 10) {
       i = "0" + i;
    }
   return i;
}
function timeStr(nts){
    var dd = parseInt(nts / 60 / 60 / 24, 10);
    var hh = parseInt(nts / 60 / 60 % 24, 10);
    var mm = parseInt(nts / 60 % 60, 10);
    var ss = parseInt(nts / 1000 % 60, 10);
    $(".zy_activityDemo2 .p > span").html(dd);
    dd = checkTime(dd);
    hh = checkTime(hh);
    mm = checkTime(mm);
    ss = checkTime(ss);
    return dd+":"+hh+":"+mm+":"+ss;
}
function sreachBtn(str) {
    var str = str.replace('#', 'u0023').replace('?', 'u0022');
    window.open("/search/course/" + str + "-1/");
}
//zhouyi:7-30  验证邮件倒计时
var zy_c_num=60;
var zy_str="";
function zy_Countdown(){
    zy_c_num--;
    $(".sendE2 span").html(zy_c_num+"s");
    $(".zy_success span").html(zy_str);
    (zy_c_num<58)&&$(".zy_success").addClass("upmove");
    if(zy_c_num<=0){
        zy_c_num=60;
        $(".sendE2").hide();
        $(".sendE").show()
        return false;
    }
    setTimeout("zy_Countdown()",1000);
}

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

function synclogin(data){
    alert(data)
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
                    if(data.onepay_status == 'True'){
                        window.location.replace('/');
                    }
                    if(detect_ie() !== false) {
                        window.location.reload();
                    }
                    //window.location.href = "/user/center";
                    return;
                }else if(data.status == "failure"){
                    if(data.msg=='no_active'){
                        zyemail=$("#id_account_l").val();
                        zyUname=zyemail;
                        zy_validate_Email(false,zyemail,$("#id_password_l").val());

                    }
                    else
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

function login_form_ajax(uname,upwd){

    $.ajax({
        type: "POST",
        url:"/user/login/",
        data:{"account_l":uname,"password_l":upwd},
        success: function(data) {
            console.log(data)
        }
    });

}

//注册表单提交
var current_register_form = "email_register_form";
function change_form(to_form_id){
    $("#register-tips").hide()
    current_register_form = to_form_id;
}
//zhouyi
var zyemail="";
var zyUname="";
var hash={
    'qq.com': 'http://mail.qq.com',
    'gmail.com': 'http://mail.google.com',
    'sina.com': 'http://mail.sina.com.cn',
    '163.com': 'http://mail.163.com',
    '126.com': 'http://mail.126.com',
    'yeah.net': 'http://www.yeah.net/',
    'sohu.com': 'http://mail.sohu.com/',
    'tom.com': 'http://mail.tom.com/',
    'sogou.com': 'http://mail.sogou.com/',
    '139.com': 'http://mail.10086.cn/',
    'hotmail.com': 'http://www.hotmail.com',
    'live.com': 'http://login.live.com/',
    'live.cn': 'http://login.live.cn/',
    'live.com.cn': 'http://login.live.com.cn',
    '189.com': 'http://webmail16.189.cn/webmail/',
    'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
    'yahoo.cn': 'http://mail.cn.yahoo.com/',
    'eyou.com': 'http://www.eyou.com/',
    '21cn.com': 'http://mail.21cn.com/',
    '188.com': 'http://www.188.com/',
    'foxmail.coom': 'http://www.foxmail.com'
};
function zy_validate_Email(bo,zyem,upwd){
    var zybo1=true;
    if(!bo) {
        $("#emailValidate .close").unbind().click(function(){
            $('#emailValidate').modal('hide');
            login_form_ajax(zyem,upwd);
        })
        $('#registerModal').modal('hide');
        $('#addemailModal').modal('hide');
        $('#emailValidate').modal('show');
        var zya=$(".zy_email .a>a");
        var url = zyem.split('@')[1];
        zya.attr("href",hash[url]);
        $("#emailValidateEE span").html(zyem);
        if(undefined==hash[url] || hash[url]==null){
            zya.parent().hide();
        }
        zybo1=false;
    }
    else{
        zybo1=true;
    }
    return zybo1;
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
                //console.log(data)
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
                    $("#register_btn").html("登录中...");
                    $("#id_account_l").val($("#id_email").val());
                    $("#id_password_l").val($("#id_password").val());
                    zyemail=$("#id_email").val();
                    var ebo=zy_validate_Email(false,zyemail,$("#id_password").val());
                    zyUname=$("#id_email").val();
                    ebo&&login_form_submit("register-tips");
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
                    _trackData.push(['addaction','完成手机注册','来源'+location.pathname]);
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
        data:{
            'account':$('#id_account').val(),
            'geetest_challenge': $('.geetest_challenge').attr('value'),
            'geetest_validate': $('.geetest_validate').attr('value'),
            'geetest_seccode': $('.geetest_seccode').attr('value')
        },
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#findpassword_btn").html("提交中...")
            $("#findpassword_btn").attr("disabled","disabled")
        },
        success: function(data) {
            if(data.account){
                $("#findpassword-tips").html(data.account).show(500);
                $("#id_account").focus();
            }else if(data.mobile){
				$("#findpassword-tips").html(data.mobile).show(500);
            }else if(data.email_ue){
				$("#findpassword-tips").html(data.email_ue).show(500);
            }else if(data.captcha){
                $("#findpassword-tips").html(data.captcha).show(500);
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
                    $('#id_mobile_f').val($("#id_account").val());
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
var sendOFF = true;
function show_send_sms(time){
    $("#send-verify").html("重发验证码（" + time + "s）").css({'background':'#D6D6D6'}).attr("disabled","disabled");
    if(time<=0){
        clearTimeout(send_sms_time);
        $(".verify-tips.success").hide(500);
        $("#send-verify").html("重发验证码").css({'background':'#5ECFBA'}).removeAttr("disabled");
        sendOFF = true;
        return;
    }
    time--;
    send_sms_time = setTimeout("show_send_sms("+time+")", 1000);
}

//发送手机验证码
function send_sms_code(form_id,tips_id){
    //hash_key,code
    // if($("#id_captcha_m_1").val()==''){
    //     $("#"+tips_id).html("图片验证码不能为空").show(500); return;
    // }

    show_send_sms(60);
	var mobileVal = $('#id_mobile_code').val();
	var mobile_way = '';
	if(mobileVal == '' || mobileVal == undefined){
		mobileVal = $('#id_mobile_f').val();
		mobile_way = 'change';
	}
    if(sendOFF){
    	$.ajax({
    	    cache: false,
    	    type: "POST",
    	    url:"/user/register/mobile/sendsms_signup/",
    	    data:{
    	    	'mobile': mobileVal,
    	    	'geetest_challenge': $('.geetest_challenge').attr('value'),
    	    	'geetest_validate': $('.geetest_validate').attr('value'),
    	    	'geetest_seccode': $('.geetest_seccode').attr('value'),
				'way': mobile_way
    	    },
    	    async: true,
    	    success: function(data){
    	    	//console.log(data)

    	        if(data.mobile){
    	            $("#mobile_code_password_form_message").css({'background':'#f2dede'}).html(data.mobile).show(500);
    	            $("#id_mobile").focus();
    	        }else if(data.captcha){
    	            $("#mobile_code_password_form_message").css({'background':'#f2dede'}).html(data.captcha).show(500);
    	        }else if(data.status == 'success'){
    	            $("#mobile_code_password_form_message").css({'background':'#f2dede'}).html(data.info).show(500);
    	            show_send_sms(60);
    	        }else if(data.status == 'failure'){
    	            $("#mobile_code_password_form_message").css({'background':'#f2dede'}).html("短信验证码发送失败").show(500);
    	        }
    	    },
    	    complete: function(XMLHttpRequest){
    	        $("#send-verify").html("重发验证码");
    	        $("#send-verify").removeAttr("disabled");
    	    }
    	});

    	sendOFF = false;
    }

}

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
function login_popup(msg){
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
    // alert(msg);
    if(typeof(msg) != 'undefined'){
        $('#loginModal #login-form-tips').show().html(msg);
    }
}

document.write('<script type="text/javascript"  data-lxb-uid="7480776" data-lxb-gid="184162" src="http://lxbjs.baidu.com/api/asset/api.js?t=' + new Date().getTime() + '" charset="utf-8"></scr' + 'ipt>' );

document.getElementById("callBtn").onclick = function () {
    lxb.call(document.getElementById("telInput"));
}

// 鼠标经过用户头像，显示浮动层信息
/*
 * @parameter uBtn: Element Node // 用户头像元素
 * @parameter data: Object // 用户数据
 */
publicFunction = {};
var cache = [];
publicFunction.userInfoLayer = function (uBtn, data, showOrHide){

	function uInfoHtml(data){
		var s = '';
		s += '<div class="u-info-plane" style="display:none">';
		s += '<img class="u-info-picbg" src="'+ data.imgBg +'" onerror="this.src=/uploads/avatar/default_small.png" alt=""/>';
		s += '<div class="col-box">';
		s += '<div class="column-col column-col1">';
		s += '<div class="col-in" style="margin:0;">';
		s += '<span class="u-photo"><img src="'+ data.uImg +'" alt=""/></span>';
		s += '</div>';
		s += '</div>';
		s += '<div class="column-col column-full column-col2">';
		s += '<div class="col-in" style="margin-left:0;">';
		if( data.uStatusStyle == 2){
		s += '<span class="u-name" style="margin:0;">'+ data.uName +'</span><span class="u-status u-teacher-status"><span class="text">'+ data.uStatus +'</span></span>';
		}
		if( data.uStatusStyle == 1){
		s += '<span class="u-name" style="margin:0;">'+ data.uName +'</span><span class="u-status u-student-status"><span class="text">'+ data.uStatus +'</span></span>';
		}
		if( data.uStatusStyle == 0){
		s += '<span class="u-name" style="margin:0;">'+ data.uName +'</span>';
		}
		//s += '<span class="u-name">'+ data.uName +'</span><span class="u-status u-'+ (2 == data.uStatusStyle ? 'teacher' : 'student') +'-status"><span class="text">'+ data.uStatus +'</span></span>';
		s += '<span class="u-title">'+ data.uTitle +'</span>';
		s += '</div>';
		s += '</div>';
		s += '</div>';
		s += '<p class="u-introduction" style="margin:0;">'+ data.uIntr +'</p>';
		s += '<div class="row">';
		s += '<ul class="pull-left list-inline">';
		s += '<li><span class="i-num" style="width:auto;height:auto;">'+ data.wd +'</span><span class="i-type" style="width:auto;height:auto;">问答</span></li>';
		s += '<li><span class="i-num" style="width:auto;height:auto;">'+ data.wz +'</span><span class="i-type" style="width:auto;height:auto;">文章</span></li>';
		if(data.user_id!=data.xiaomai_id){
			s += '<li><span class="i-num" style="width:auto;height:auto;">'+ data.fs +'</span><span class="i-type" style="width:auto;height:auto;">粉丝</span></li>';
		}
		s += '</ul>';
		s += '<div class="pull-right">';
		s += '<div class="btn-box GZ" >';
		var hh1='',hh2='',ss1='',ss2='';
		if(data.is_self==false&&data.user_id!=data.xiaomai_id){
			if(data.is_bothgz == true){
				hh1='互相关注';
			}
			else{
				hh1='已关注';
			}
			if(data.is_login == false){
				hh2='onclick="login_popup()"'
			}
			else{
				hh2='onclick="guanzhu('+data.user_id+')"';
			}
			if(data.is_gz == true){

				ss1='';
				ss2='style="display:none"';
			}
			else{
				ss1='style="display:none"';
				ss2='';
			}
			s+='<div class="dropdown" '+ss1+'> <a data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" class="dropdown-toggle11">'+hh1+'<span class="caret"></span></a> <ul class="dropdown-menu" aria-labelledby=""> <li><a onclick="quxiaoguanzhu('+data.user_id+')">取消关注</a></li> </ul> </div>';
			s += '<span id="guan_zhu" class="btn" '+hh2+' '+ss2+'>+ 关注</span>';
		}
		s += '</div>';
		s += '</div>';
		s += '</div>';
		s += '</div>';
		return s;
	}

	function msOverFn(holder){
		//clearTimeout( uBtn[0]._uInfoLayer_timer );
		//uBtn[0]._uInfoLayer_timer = setTimeout(function(){
		//
		//}, 1);

		var uInfoLayer=$( uInfoHtml(data) );
		if( uInfoLayer[0].parentNode != document.body ){
			uInfoLayer.appendTo($(holder));
			uInfoLayer.hover(function(){
				//$(this).parent().parent().parent().parent().parent().unbind().click(function(){return false;})
			}, function(){
				//$(this).parent().parent().parent().parent().parent().unbind();
			});
		}
		if(holder){
			var other = $(holder);
			var offset = other.offset();
			var left = offset.left;
			var width = uInfoLayer.outerWidth(true);
			var bodyWidth = $('body').width();
			console.log(left + width+"==="+bodyWidth)
			if( left + width > bodyWidth ){
				left = -260;
			}
			else{
				left=0;
			}
			uInfoLayer.css({ left: left, top: other.height() });
		}
		uInfoLayer.show();
		$(".zyhideP").find(".u-info-plane").remove();
	}
	function msOutFn(holder){
		holder.children(".u-info-plane").remove();
	}

	var uInfoLayerIndex;
	uBtn = $(uBtn);
	uInforLayerIndex = uBtn.attr('info-layer-index');
	if( !uInforLayerIndex ){
		uInforLayerIndex = cache.length;
		uBtn.attr('info-layer-index', uInforLayerIndex);
	}
	//uInfoLayer = cache[ uInforLayerIndex ];
	//if( !uInfoLayer ){
	//	uInfoLayer = $( uInfoHtml(data) );
	//	cache[ uInforLayerIndex ] = uInfoLayer;
	//}
	if( null == showOrHide ){
		// 鼠标经过用户头像
		//uBtn.hover(function(){
		//	msOverFn( this );
		//}, function(){
		//	msOutFn();
		//});
	}else if( 'show' == showOrHide ){
		// 直接显示
		msOverFn( uBtn );

	}else if( 'hide' == showOrHide ){
		msOutFn(uBtn);
	}
}

function jsonpCallbackZZ2(data2){
    if (data2.status == 'success') {
        var eq=$(".GZ").children();
        eq.eq(1).hide();
        eq.eq(0).show();
    }
}
function guanzhu(id) {

	var a = '<div class="dropdown"> <a id=""  data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">已关注<span class="caret"></span></a> <ul class="dropdown-menu" aria-labelledby=""> <li><a onclick="quxiaoguanzhu(' + id + ')">取消关注</a></li> </ul> </div>';
	$.ajax({
        async: false,
        url:_fps_site_url+"common/ajax/usernetwork/" + id + "/?name=1",
        type: "GET",
        dataType: 'jsonp',
        jsonp: 'jsonpCallbackZZ2',
        data:{'callback':'jsonpCallbackZZ2'},
        timeout: 10000,
        beforeSend: function(){
        },
        success: function (json) {
        },
        complete: function(XMLHttpRequest, textStatus){
        },
        error: function(xhr){
        }
    });

}
function jsonpCallbackZZ3(data3){
    if(data3.status == 'success'){
        var eq=$(".GZ").children();
        eq.eq(0).hide();
        eq.eq(1).show();
    }
}
function quxiaoguanzhu(id) {
var b = '<span id="guan_zhu" class="btn" onclick="guanzhu('+ id +')">+ 关注</span>';
    $.ajax({
        async: false,
        url:_fps_site_url+"common/ajax/usernetwork0/" + id + "/?name=1",
        type: "GET",
        dataType: 'jsonp',
        jsonp: 'jsonpCallbackZZ3',
        data:{'callback':'jsonpCallbackZZ3'},
        timeout: 10000,
        beforeSend: function(){
        },
        success: function (json) {
        },
        complete: function(XMLHttpRequest, textStatus){
        },
        error: function(xhr){
        }
    });
}

var hovered_user;
function jsonpCallbackZZ(data){
    publicFunction.userInfoLayer(hovered_user, data.data, 'show');
    $('.dropdown-toggle11').unbind().dropdown()
}
function touxiangH(uid){
    //头像hover
    $('.u-photo-btn').parent().hover(function () {
        hovered_user = this;
        $(this).removeClass("zyhideP");
        $.ajax({
            async: false,
            url:_fps_site_url+'common/ajax/userinfo/' + $(hovered_user).children("a").attr("id"),
            type: "GET",
            dataType: 'jsonp',
            jsonp: 'jsonpCallbackZZ',
            data:{'callback':'jsonpCallbackZZ'},
            timeout: 10000,
            beforeSend: function(){
            },
            success: function (json) {
            },
            complete: function(XMLHttpRequest, textStatus){
            },
            error: function(xhr){
            }
        });

    },
    function () {
        $(this).addClass("zyhideP");
        publicFunction.userInfoLayer(this, null, 'hide');
    })
}

/* 顶部搜索 临时使用 web优化不在使用 */
// function onSearch(){
//     $("#data-search").textFiltered({
//         "boEnter":true,
//         "onkeyup":function(boolean){
//             var $th = this,bokey = false;
//             if(boolean){sreachBtn($th.val());return;}
//             $.ajax({
//                 type: "GET",
//                 url:"/homepage/get_course_category/",
//                 data:{"s":$th.val()},
//                 beforeSend:function(XMLHttpRequest){},
//                 success: function(data1) {
//                     $th.clear();
//                     for(var i=0;i<data1.length;i++){
//                         $th.addNode(data1[i],data1[i]);
//                         if(data1[i]==$th.val()){$th.data("vv",data1[i]);bokey=true;}
//                     }
//                 },
//                 complete: function(XMLHttpRequest){}
//             });
//             if(!bokey) $th.removeData("vv");
//         }
//         ,"height":180
//         ,"onarrowupdown":function(i){}
//         ,"onVclick":function(v){
//             this.data("vv",v);
//             if(v!="暂无数据") {
//                 $("#data-search").val(v);
//                 //sreachBtn(v);
//             }
//         }
//     });
// }