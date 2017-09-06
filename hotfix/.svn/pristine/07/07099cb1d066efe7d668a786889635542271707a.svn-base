// 绑定53客服
$(".class53").click(function(){
    $("#KFLOGO .Lelem").eq(0).trigger("click");
});
// 侧边悬浮框
$(".toolbar-item-weibo>div").hover(function(){
},function(){
    $(this).stop().hide("fast");
});
$(".toolbar-item-weibo").click(function(){
    $(".lixianB").show();
});
$(".toolbar-item-weixin, .toolbar-kf").unbind().click(function(){
    $("#KFLOGO .Lelem").eq(0).trigger("click");
    $(".toolbar-kf").hide();
});

// 返回顶部
function checkPosition(pos){
    var scrtop = $(document.documentElement).scrollTop() || $(document.body).scrollTop();
    if(scrtop > pos){
        $(".toolbar-item-gotop").fadeIn();
    }else {
        $(".toolbar-item-gotop").fadeOut();
    }
}
$(window).on('scroll',function(){
    checkPosition($(window).height())
});
checkPosition($(window).height());
$(".toolbar-item-gotop").click(function(){
    $('html,body').stop().animate({scrollTop: '0px'}, 800);
});

// Tips提示
function Tips(obj,tipsMsg){
    obj.wrap('<div class="tips-box"></div>').after('<span class="tips">' + tipsMsg + '</span>');
    setTimeout(function(){
       obj.unwrap().siblings().remove('.tips');
       obj.focus();
    }, 4000);
};

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
    $('#loginModal').modal('show');
    // if(typeof(msg) != 'undefined'){
    //     $('#loginModal #login-form-tips').show().html(msg);
    // }
}
// 弹出登录框
$(".globalLoginBtn").on("click",login_popup);
//登录事件
$(".globalLogin").on("click",function(){
    login_form_submit("login-form-tips");
});

// 弹窗上下左右居中
(function(){
    var cacheModel = [];
    $(".modal").on("show.bs.modal", function(){
        for(var i = 0;i<cacheModel.length;i++){
            if(cacheModel[i]){
                cacheModel[i].modal('hide');
                cacheModel[i] = null;
            }
        }
        cacheModel.push($(this));
        var $this = $(this);
        var $modal_dialog = $this.find(".modal-dialog");
        var div = $('<div style="display:table; width:100%; height:100%;"></div>')
        div.html('<div style="vertical-align:middle; display:table-cell;"></div>');
        div.children("div").html($modal_dialog);
        $this.html(div);
    });
})();

// 验证邮件倒计时
var zy_c_num = 60,zy_str = "",sendECount;
function zy_Countdown(){
    zy_c_num--;
    $(".sendE2 span").html(zy_c_num + "s");
    $(".zy_success span").html(zy_str);
    (zy_c_num < 58) && $(".zy_success").addClass("upmove");
    if(zy_c_num <= 0){
        zy_c_num = 60;
        $(".sendE2").hide();
        $(".sendE").show();
        clearInterval(sendECount);
    }
}

// 发送验证邮件事件
$(".sendE a").click(function(){
    sendECount = setInterval(zy_Countdown,1000);
    $(".zy_success").removeClass("upmove");
    $(this).parent().hide();
    $(".sendE2").show().find("span").html("60s");   
    $.ajax({
         type: "GET",
         url: "/user/send_again_email",
         data: {username:$('#id_account_l').val()},
         dataType: "html",
         success: function(data){
             zy_str = "验证邮件发送成功";
             if(data)
                zy_Countdown();
         },
        error:function(){
            zy_str = "验证邮件发送失败";
        }
     });
});

// 登录表单提交
function login_form_submit(){    
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/login/",
        data:$('#login_form').serialize(),
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
                    if(data.onepay_status == 'True'){
                        window.location.replace('/');
                    }else {
                        window.location.replace(data.url);
                    }
                    if(detect_ie() !== false) {
                        window.location.reload();
                    }
                    return;
                }else if(data.status == "failure"){
                    if(data.msg == 'no_active'){
                        zyemail = $("#id_account_l").val();
                        zyUname = zyemail;
                        zy_validate_Email(false,zyemail,$("#id_password_l").val());
                    }else{
                        $("#login-form-tips").html("账号或者密码错误，请重新输入").show(500);
                    }
                }
            }
        },
        complete: function(XMLHttpRequest){
            $("#login_btn").html("登录");
            $("#login_btn").removeAttr("disabled");
        }
    });
}

// 重发送短信验证码计时
var sendOFF = true;
function show_send_sms(time){
    $("#forgetpswMobileModal .send-verify,#verify_form .send-verify").html("重发验证码（" + time + "s）").css({'background':'#D6D6D6'}).attr("disabled","disabled");
    if(time <= 0){
        $(".verify-tips.success").hide(500);
        $("#forgetpswMobileModal .send-verify,#verify_form .send-verify").html("重发验证码").css({'background':'#5ECFBA'}).removeAttr("disabled");
        sendOFF = true;
        return;
    }
    time--;
    setTimeout("show_send_sms("+ time +")", 1000);
}

// 发送手机验证码
function send_sms_code(form_id){
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
            success: function(data){
                if(data.mobile){
                    if(mobile_way != ''){
                        $('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.mobile);
                    }else{
                        $(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
                    }
                }else if(data.captcha){
                    if(mobile_way != ''){
                        $('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.captcha);
                    }else{
                        $(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
                    }
                }else if(data.status == 'success'){
                    if(mobile_way != ''){
                        $('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('');
                    }else{
                        $(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
                        show_send_sms(60);
                    }
                }else if(data.status == 'failure'){
                    if(mobile_way != ''){
                        $('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('请稍后再试');
                    }else{
                        $(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
                    }
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

// 忘记密码
var OFF = true;
$('#btnForgetpsw').on('click', function () {
    if(captchaObjF3) captchaObjF3.refresh();
        if(OFF){
            captcha(".newcaptcha");
            OFF = false;
        }
    $('#forgetpswModal').modal('show');
    $('#loginModal').modal('hide');
});
$("#forgetpswMobileModal .send-verify").click(function(){
    send_sms_code('verify_form','verify-tips');
});
//忘记密码下一步
$("#mobile_code_password_btn").click(mobile_code_password_form_submit);

// 验证邮件
var zyemail = "";
var zyUname = "";
var hash = {
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
    var zybo1 = true;
    if(!bo) {
        $("#emailValidate .close").unbind().click(function(){
            $('#emailValidate').modal('hide');
        })
        $('#registerModal').modal('hide');
        $('#addemailModal').modal('hide');
        $('#emailValidate').modal('show');
        var zya = $(".zy_email .a>a");
        var url = zyem.split('@')[1];
        zya.attr("href",hash[url]);
        $("#emailValidateEE span").html(zyem);
        if(undefined == hash[url] || hash[url] == null){
            zya.parent().hide();
        }
        zybo1 = false;
    }else{
        zybo1 = true;
    }
    return zybo1;
}

// 手机验证码表单验证
function mobile_code_password_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/mobile/",
        data:$('#mobile_code_password_form').serialize(),
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

// 顶部搜索
function flayer_show() {
    $("#fLayerdl").show();
    $("#dd_listbox").hide();
}

function flayer_hide(delay) {
    if (delay) {
        setTimeout("$('#fLayerdl').hide();", delay);
    } else {
        $('#fLayerdl').hide();
    }
}

function listbox_show() {
    $("#dd_listbox").show();
    $("#fLayerdl").hide();
}

function listbox_hide(delay) {
    if (delay) {
        setTimeout("$('#dd_listbox').hide();", delay);
    } else {
        $("#dd_listbox").hide();
    }
}

function searchajax(keyword) {
    $.ajax({
        url: "http://suggest.maiziedu.com/suggest/?keyword=" + keyword,
        type: "GET",
        dataType: "jsonp",
        jsonp: "callback",
        success: function (data) {
            var courses = new Array(), careers = new Array(), teachers = new Array(), teachers_repeat = new Array(), careers_repeat = new Array();

            $.each(data, function(idx, obj) {
                $.each(obj["courses"], function(idx, course) {
                    courses.push({
                        id: course["id"],
                        name: obj["name"],
                        student_count:course["student_count"]
                    });

                    $.each(course["careers"], function(idx, career) {
                        if (!career["student_count"]) {
                            return;
                        }
                        if (careers_repeat.indexOf(career["name"]) == -1) {
                            careers.push({
                                name: career["name"],
                                short_name: career["short_name"],
                                image: career["image"],
                                description: career["description"],
                                student_count: career["student_count"]
                            });
                            careers_repeat.push(career["name"]);
                        }

                        $.each(career["teachers"], function(idx, teacher) {
                            if (teachers_repeat.indexOf(teacher["name"]) == -1) {
                                teachers.push({
                                    "teacher_id": teacher["teacher_id"],
                                    name: teacher["name"],
                                    title: teacher["title"],
                                    image: teacher["image"],
                                    info: teacher["info"]

                                })
                                teachers_repeat.push(teacher["name"]);
                            }
                        })
                    })
                })
            })

            if (courses.length == 0) {
                $('.dd_listbox').hide();
                return;
            }

            // coding
            var tmp = "";
            $(".careercraft").remove();
            $.each(courses, function(idx, course) {
                tmp = '<div class="careercraft"><a target="_blank" href="/course/'+course["id"]+'/"><p class="pull-left course_info">'+course["name"]+'</p><p class="pull-right study_count">'+course["student_count"]+'人正在学习</p></a></div>';
                $("#course_name_ledg").append(tmp);
            });

            $(".chcourse").remove();
            $.each(careers, function(idx, career) {
                tmp = '<div class="chcourse"><img src="/uploads/'+career["image"]+'" class="dd_courseimg img-circle"><a target="_blank" href="/course/'+career["short_name"]+'-px/" style="outline:none;"><p class="dd_coursedescriname">'+career["name"]+'</p><p class="radius"><span class="f_radius">毕业学员： <span class="finished_count">'+career["student_count"]+'</span>人</span></p><p class="dd_coursedescri">'+career["description"]+'</p>';
                $("#incld_careers").append(tmp);
            });

            $(".careerteacher").remove();
            $.each(teachers, function(idx, teacher) {
                tmp = '<div class="careerteacher"><a target="_blank" href="'+"/u/"+teacher["teacher_id"]+'/" style="outline:none;"><img src="/uploads/'+teacher["image"]+'" class="dd_courseimg img-circle"><p class="courseteacher">'+teacher["name"]+'</p><p class="ls">|</p><p class="teachertt">'+teacher["title"]+'</p><p class="teacherdes">'+teacher["info"]+'</p></a></div>'
                $("#incld_teachers").append(tmp);
            });
            if ($("#data-search").val()) {
                if (careers.length == 0) {
                    $("#dd_csitem").hide();
                    $("#incld_careers").hide();
                } else {
                    $("#dd_csitem").show();
                    $("#incld_careers").show();
                }
                if (teachers.length == 0) {
                    $("#dd_tutor").hide();
                    $("#incld_teachers").hide();
                } else {
                    $("#dd_tutor").show();
                    $("#incld_teachers").show();
                }
                if (courses.length == 0) {
                    $("#dd_craft").hide();
                    $("#course_name_ledg").hide();
                } else {
                    $("#dd_craft").show();
                    $("#course_name_ledg").show();
                }
                listbox_show();
            }
        }
    });
}
Search();
function Search() {
    $(".search-btn").click(function () {
        sreachBtn($("#data-search").val());
        zhuge.track('搜索次数', {'搜索关键词': $("#data-search").val()});
    });

    function sreachBtn(str) {
        var str = str.replace('#', 'u0023').replace('?', 'u0022');
        if ($('.search_result_bg').length > 0) {
            var app = $('.search_app').val() ? $('.search_app').val() : 'course';
            window.location.href = "/search/" + app + "/" + str + "-1/";
        } else {
            window.open("/search/course/" + str + "-1/");
        }
    }

    $("#data-search").keyup(function (event) {
        var e = event || window.event || arguments.callee.caller.arguments[0];
        if (e && e.keyCode == 13) {
            sreachBtn($(this).val());
            return;
        }
    });
}

$(document).ready(function () {
    $("#data-search").focus(function () {
        keywd = $("#data-search").val();
        if (keywd == "") {
            flayer_show();
        } else {
            searchajax(keywd);
        }
    }).blur(function() {
        flayer_hide(500);
    })

    $("#data-search").keyup(function () {
        keywd = $("#data-search").val();
        if (keywd == "") {
            listbox_hide();
            flayer_show();
            return;
        }
        searchajax(keywd);
    }).blur(function() {
        keywd = $("#data-search").val();
        if (keywd == "") {
            listbox_hide();
            return;
        }
        listbox_hide(500);
    })
});

/* 
 * @ 倒计时
 * @ Day : 天数
 * @ intDiff : 倒计时总秒数量
 */

function cutTimer(intDiff,obj){
    window.setInterval(function(){
        var day = 0,
            hour = 0,
            minute = 0,
            second = 0;//时间默认值      
        if(intDiff > 0){
            day = Math.floor(intDiff / (60 * 60 * 24));
            hour = Math.floor(intDiff / (60 * 60)) - (day * 24);
            minute = Math.floor(intDiff / 60) - (day * 24 * 60) - (hour * 60);
            second = Math.floor(intDiff) - (day * 24 * 60 * 60) - (hour * 60 * 60) - (minute * 60);
        }
        if (minute <= 9) {minute = '0' + minute};
        if (second <= 9) {second = '0' + second};
        $(obj + '#day_show').html(day+"天");
        $(obj + '#hour_show').html( hour +'时');
        $(obj + '#minute_show').html(minute +'分');
        $(obj + '#second_show').html(second +'秒');
        intDiff--;
    }, 1000);
}

/*
 * @ 选项卡
 * @ tab_menu: 选项卡按钮class
 * @ tab_box: 选项卡内容class
 * @ active: 选项卡按钮添加选中样式 
 * @ type: 动画类型
 */
function tab(options){
    var define = {
        'tabNav': '.tab_menu > li',
        'tabBox': '.tab_box > div',
        'select': 'active',
        'type': 'show'
    };
    var option = options;
    $.extend(define, options);
    var oUl = $(define.tabNav || option.tabNav);
    oUl.click(function(){
        $(this).addClass(define.select || option.select).siblings().removeClass(define.select || option.select);
        var index = oUl.index(this);
        switch(define.type){
            case 'show': $(define.tabBox || option.tabBox).eq(index).show().siblings().hide();
            break;
            case 'slide': $(define.tabBox || option.tabBox).eq(index).slideDown(300).siblings().slideUp(300);
            break;
            case 'fade': $(define.tabBox || option.tabBox).eq(index).fadeIn(300).siblings().fadeOut(300);
            break;
        }           
    });
};

/*
 * @ 图片查看弹窗
 * @ img_src是/uploads/图片相对的路径
 */
function imgPopup(img_src){
    var html = '';
    var  newImg = new Image();
    newImg.src = img_src;
    newImg.className = 'img';

    html += '<div id="imgzoom"><div id="imgzoom-image-ctn"><i class="imgzoom-close"></i>';
    html += '<img class="img" src="'+ newImg.src +'" alt=""/>';
    html += '</div></div>';

    $('body').append(html);

    var oImg    = $('#imgzoom-image-ctn'), oZoom = $('#imgzoom');
    // oImg.find('.img').load(function(){
    //     var ddh = oImg.outerHeight(),
    //         ddw = oImg.outerWidth(),
    //         whF = oImg.outerWidth()/oImg.outerHeight();

    //     if(oImg.outerWidth()>ddh){
    //         if(Dheight<oImg.outerHeight()){
    //             ddh = Dheight - 20;
    //             ddw = ddh * whF;
    //         }
    //     }else{
    //         if(ddw > 1160){ ddw = 1160;ddh = 1160/whF;}
    //     }

    //     oImg.css({'left': '50%','top': '50%','marginLeft': -ddw/2,'marginTop':-ddh/2});
    // });
    newImg.onload = function(){
        var oImgH = 0, oImgW = 0;
        oImgW = newImg.width;
        oImgH = newImg.height;

        // if(oImgH > oImg.height()){
        //     $('.img').css({'width': $('#imgzoom-image-ctn').width() + 'px' });
        // }

        //oImg.css({'max-width': $('.img').width() + 'px','max-height': $('.img').height() + 'px'});
        if((oImg.width() / oImg.height()) >= (oImgW / oImgH)){
            if(oImgH > oImg.height()){
                oImg.find('.img').width(parseInt((oImg.height() * oImgW) / oImgH));
                oImg.find('.img').height(parseInt(oImg.height()));
                oImg.width(parseInt((oImg.height() * oImgW) / oImgH));
                oImg.height(parseInt(oImg.height()));
            }else{
                oImg.width(oImgW);
                oImg.height(oImgH);
            }
        }
        oImg.css({'left': '50%','top': '50%','marginLeft': -oImg.width()/2,'marginTop':-oImg.height()/2});
        oImg.fadeIn();
    }    
    

    oZoom.fadeIn('fast','linear');
    oZoom.find('.img').on('click', function(e){
        var e = e || event;
        e.stopPropagation();
    }); 
    $('.imgzoom-close, body').on('click',function(){$('#imgzoom').remove();});
};
// 用户昵称截取 
var _Login = $('.topRight').attr('login');
if(_Login == 'True'){
    var _nickName = $('.nick_name a:first-child');
    if(_nickName.attr('data-name').length >= 4){
        _nickName.text(_nickName.attr('data-name').substring(0,4)+'...');
    }else{
        _nickName.text(_nickName.attr('data-name'));
    }
}

/**
 * ops约课成功
 */
function yueKeSuccess(){
    var yuekeSucces = $('#yueke-success');
    yuekeSucces.modal({show:true, keyboard:false,backdrop: 'static'});
    $('#yueke-success .close, #yueke-success .know').off().on('click' ,function(){
        yuekeSucces.modal('hide');
    });
}
/**
 * ops已经预约过了
 */
function yueKeOver(){
    var yuekeOver = $('#yueke-over');
    yuekeOver.modal({show:true, keyboard:false,backdrop: 'static'});
    $('#yueke-over .close, #yueke-over .know').on('click', function(){
        yuekeOver.modal('hide');
    });
}
/**
 * ops预约最后一步
 */
function yueKeLastStep(source){
    var yuekeLastStep = $('#yueke-last-step'),
        $username = $('#ops-user-name'),
        $phoneNum = $('#ops-phone-num'),
        $advisor = $('#ops-advisor'),
        $verification = $('#ops-verification'),
        telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
    $verification.val();
    yuekeLastStep.modal({show:true, keyboard:false,backdrop: 'static'});
    $('#yueke-last-step .close').on('click', function(){
        yuekeLastStep.modal('hide');
    });

    $('#yueke-last-step .know').off().on('click',function(){
        if($username.val() == '' || null){
            tipsMsg = '请输入你的姓名';
            Tips($username, tipsMsg);
        }else if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if(!telReg.test($phoneNum.val())){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if($advisor.selected = ($advisor.val() == 0)){
            tipsMsg = '未选择';
            Tips($advisor, tipsMsg);
        }else if($verification.val() == '' || null){
            tipsMsg = '手机验证码输入错误，请重试';
            Tips($verification, tipsMsg);
        }else{
            ops_verify(source);
        }
    });
    $('#ops-send-verify').on('click',function(){
        if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else{
            if(telReg.test($phoneNum.val())){
                ops_send_sms();
            }else if(!telReg.test($phoneNum.val())){
                tipsMsg = '请输入正确的手机号';
                Tips($phoneNum, tipsMsg);
            }
        }
    });
}
/**
 * ops预约1v1服务
 */
function ovoService(){
    var ovoService = $('#ovo-service');
    ops_is_exist('1',oveOrderService);

    function oveOrderService() {
        ovoService.modal({show: true, keyboard: false, backdrop: 'static'});
        $('#ovo-service .know').off().on('click', function () {
            ovoService.modal('hide');
            yueKeLastStep('1');
        });
        $('#ovo-service .close').on('click', function(){
            ovoService.modal('hide');
        });
    };
};
/**
 * ops预约1v1直播
 */
function openService(){
    var openService = $('#open-service');
    ops_is_exist('2',oveOrderMetting);

    function oveOrderMetting() {
        openService.modal({show: true, keyboard: false, backdrop: 'static'});
        $('#open-service .know').off().on('click', function () {
            openService.modal('hide');
            yueKeLastStep('2');
        });
        $('#open-service .close').on('click', function(){
            openService.modal('hide');
        });
    };

}

function ops_verify(source) {
    var $verification = $('#ops-verification'),tipsMsg;
    $.ajax({
        type: "POST",
        url: "/lps4/ajax_ops_verify/",
        data: {
            "mobile": $("#ops-phone-num").val(),
            "mobile_code": $("#yueke-last-step .verification").val(),
            "career_id":career_id,
            "source":source,
            "username": $('#ops-user-name').val(),
            "advisor": $('#ops-advisor').val(),
            'status': $('#ops-status').val()
        },
        dataType: "json",
        success: function (data) {
            if (data.success) {
                $('#yueke-last-step').modal('hide');
                yueKeSuccess();
            } else {
                tipsMsg = data.message;
                Tips($verification, tipsMsg);
            }
        }
    });
};



function ops_is_exist(source, callbackOrder) {
    $.ajax({
        type: "POST",
        url: "/lps4/ajax_ops_is_exist/",
        data: {
            "career_id":career_id,
            "source":source
        },
        dataType: "json",
        success: function (data) {
            if (data.success) {
                if (data.data.is_exist){
                    //已经预约
                    yueKeOver();
                }else {
                    //预约回调
                    callbackOrder();
                }
            } else {
                layer.alert(data.message, {
                    skin: 'layui-layer-molv',
                    closeBtn: 0
                });
            }
        }
    });
};

function ops_send_sms(){
    var mobile = $('#ops-phone-num').val(),
        $verification = $('#ops-verification'),
        tipsMsg,
        $sendVerif = $('#ops-send-verify');
    $.ajax({
        type: "POST",
        url: "/lps4/mobile/sendsms/",
        data: {
            "mobile": mobile,
            "retry": 1
        },
        dataType: "json",
        success: function (data) {
            if (data.success) {
                Cuttime($sendVerif, 60);
            } else {
                tipsMsg = data.message;
                Tips($verification, tipsMsg);
            }
        }
    });
}
/**
 * 倒计时
 */
 function Cuttime(obj, time){
     var countdown = null;
     obj.addClass("send").val("60s").attr('disabled', 'disabled');
     countdown = setInterval(function(){
         time--;
         obj.val(time+"s");
         if(time <= 0){
             clearInterval(countdown);
             obj.removeClass("send").val("重新发送").removeAttr('disabled');
         }
     },1000);
 }
/**
 * 点击加入直播室，需要先更新点击记录
 */
$(".finished").parent().on('click',function() {
    var meeting_id = $(this).attr('meeting_id');
    var href_url = $(this).attr('href_url');
    $.ajax({
        type: "POST",
        url: "/home/t/ajax_insert_onevone_attendance/",
        data: {
            "meeting_id": meeting_id
        },
        dataType: "json",
        success: function (data) {
        }
    });
    window.open(href_url);
});

/**
 * 20161220老师点击加入直播室，需要先更新点击记录
 */
$(".live-btn.living").on('click', function () {
    var meeting_id = $(this).attr('meeting_id');
    var href_url = $(this).attr('href_url');
    $.ajax({
        type: "POST",
        url: "/home/t/ajax_insert_onevone_attendance/",
        data: {
            "meeting_id": meeting_id
        },
        dataType: "json",
        success: function (data) {
        }
    });
    window.open(href_url);
});
