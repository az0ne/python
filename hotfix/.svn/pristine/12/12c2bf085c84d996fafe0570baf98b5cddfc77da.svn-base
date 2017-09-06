
$(function(){

    $(".wapLogin .formBox li input").focus(function(){
        $(this).parent().parent().css("border-color","#5ECFBA").siblings("li").css("border-color","#e2e2e2");
    });

    function usernameFocus(){
        $(".wapLogin .username input").focus().parent().parent().css("border-color","#5ECFBA");
    };

    function passwordFocus(){
        $(".wapLogin .userpassword input").focus().parent().parent().css("border-color","#5ECFBA");
    }

    // 错误信息提示
    function show_error_msg(data){
        if(data.account_l){
            $errorTip.html(data.account_l[0]);
            errorFun();
            //usernameFocus();
        } else if(data.password_l){
            $errorTip.html(data.password_l[0]);
            errorFun();
            //passwordFocus();
        } else if(data.status == "failure"){  // wap 端不需要考虑账号是否激活
            //usernameFocus();
            if(data.msg){
                $errorTip.html(data.msg);
            } else {
                $errorTip.html('账号或者密码错误，请重新输入');
            };
            errorFun();
        };
    };

    // 登陆表单提交函数
    function submit_login(){
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/wap_login/",
            data:$('#login_form').serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                $(".wapLogin .btn").val("登录中...");
                $(".wapLogin .btn").attr("disabled","disabled");
            },
            success: function(data) {
                if(data.status == 'success'){
                    window.location.replace(data.url);
                } else {
                    show_error_msg(data);
                    $(".wapLogin .btn").val("登录");
                    $(".wapLogin .btn").removeAttr("disabled");
                };
            }
        });
    }

    // 定义登陆输入格式错误的函数
    function errorFun(){
        $errorTip.addClass("show");
        $box.animate({"height":"13rem"},150);
    }

    // 检查登陆输出是否合法, 如果合法, 则提交登陆信息
    function check_login_input(){
        var nameVal, passwordVal;
        nameVal = $(".username input").val();
        passwordVal = $(".userpassword input").val();

        if(nameVal == ""){
            $errorTip.html('账号不能为空');
            //usernameFocus();
            errorFun();
            return;
        }else if(!$.trim(nameVal) || !/^0?1[3|4|5|8]\d{9}$/.test($.trim(nameVal))){
            $errorTip.html('该账号格式不正确');
            //usernameFocus();
            errorFun();
            return;
        }else if(passwordVal == ""){
            $errorTip.html('密码不能为空');
            //passwordFocus();
            errorFun();
            return;
        };

        // 前端验证正确, 登陆
        submit_login();

    };

    //////  登陆相关

    var $errorTip,$box,$indexBg;
    $errorTip = $(".wapLogin .errorTip");
    $box = $('.wapLogin .box');
    $indexBg = $(".indexBg");

    /**
     * [browser 判断平台]
     * @param test: 判断是否为Iphone
     */
    var browser = {
      versions: function () {
      var u = navigator.userAgent, app = navigator.appVersion;
          return {//移动终端浏览器版本信息
           trident: u.indexOf('Trident') > -1, //IE内核
           presto: u.indexOf('Presto') > -1, //opera内核
           webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
           gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
           mobile: !!u.match(/AppleWebKit.*Mobile/i) || !!u.match(/MIDP|SymbianOS|NOKIA|SAMSUNG|LG|NEC|TCL|Alcatel|BIRD|DBTEL|Dopod|PHILIPS|HAIER|LENOVO|MOT-|Nokia|SonyEricsson|SIE-|Amoi|ZTE/), //是否为移动终端
           ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
           android: u.indexOf('Android') > -1,  //android终端
           uc: u.indexOf('UCBrowser') > -1,  //uc浏览器
           iPhone: u.indexOf('iPhone') > -1 || u.indexOf('Mac') > -1, //是否为iPhone或者QQHD浏览器
           iPad: u.indexOf('iPad') > -1, //是否iPad
           webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
          };
      } (),
      language: (navigator.browserLanguage || navigator.language).toLowerCase()
    };
    //点击登陆按钮, 弹出登陆窗口
    $("#login").bind("touchend",function(e){
        //判断是否是IOS系统或者UC浏览器
        if (browser.versions.iPhone || browser.versions.iPad || browser.versions.ios || browser.versions.uc) {
            // $(".index .wapLogin div.box").css({"position":"absolute","top":"inherit"});
            $(".index .wapLogin div.box").css({"position":"absolute"});
            $(".career_course_detail .wapLogin div.box").css({"position":"absolute","bottom":"inherit"});
            $(".wapLogin div.bg").css({"position":"absolute"});
            var windowHeight = $(window).height(),
                marginBottomHeight = $(document).height() - $(window).scrollTop() - windowHeight;
            // $(".index .wapLogin .box").css("bottom",(windowHeight-480)/2 + marginBottomHeight);
            $(".index .wapLogin .box").css("top",'10'+'px');
            $(".career_course_detail .wapLogin .box").css("top",(windowHeight-480)/2);
        };
        $box.addClass("show");
        $indexBg.addClass("show");
    });

    //弹窗显示后，不允许滑动页面
    $(".wapLogin .box,.wapLogin .bg").bind("touchmove",function(e){
        e.preventDefault();
    });

    //当职业课程页面的登录界面input框获得焦点时，重置其背景高度，以确保UC浏览器中出现兼容性问题（页面滚动后，底下的背景覆盖不全）
    $(".career_course_detail .wapLogin .formBox input").focus(function(){
        if (browser.versions.uc) {
            $(".wapLogin .bg").css("height",$(window).height()*2);
        };
    });
    //当职业课程页登录界面input框失去焦点时，IOS及UC页面回到顶部（实现登录框居中显示）
    $(".career_course_detail .wapLogin .formBox input").blur(function(){
        if (browser.versions.iPhone || browser.versions.iPad || browser.versions.ios || browser.versions.uc) {
            window.scrollTo(0,0);
        };
    });

    // 绑定登陆按钮
    $(".wapLogin .btn").bind("click", check_login_input);

    // 绑定取消登陆按钮
    $(".wapLogin .cancleBtn").bind("click", function(e){
        $box.removeClass("show");
        $indexBg.removeClass("show");
    });

    //////  退出登陆相关

    // 绑定退出登陆按钮, 弹出 退出登陆窗口
    $(".quit input").bind("touchend",function(e){
        if (browser.versions.uc){
            $(".indexQuitBox").css({"position":"absolute","top":"inherit"});
            $(".index").css({"position":"fixed","top":"inherit","bottom":"0"});
            var windowHeight = $(window).height(),
                    marginBottomHeight = $(document).height() - $(window).scrollTop() - windowHeight;
                $(".indexQuitBox").css("bottom",(windowHeight-276)/2);
        };
        $(".indexQuitBox").addClass("show");
        $indexBg.addClass("show");

    });

    // 弹出退出窗口之后，不允许滑动页面
    $(".indexBg,.indexQuitBox").bind("touchmove",function(e){
        e.preventDefault();
    });

    // 绑定 取消退出登陆按钮
    $(".indexQuitBox .cancel").bind("touchend",function(e){
        var e = e || event;
        $(".index").removeAttr("style");
        $(this).parents(".indexQuitBox").removeClass("show");
        $indexBg.removeClass("show");
        e.stopPropagation();
    });

    //绑定　确定退出登陆按钮
    $(".indexQuitBox .ok").bind("touchend",function(e){
        var e = e || event;
        e.stopPropagation();
    });

});