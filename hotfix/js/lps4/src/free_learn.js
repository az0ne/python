define(function (require, exports, module) {
    var captchaPhone, PhoneValue;
    /*
     * @ 预约弹窗
     *
     */
    var captcha = require('./main').captcha;
    var isLogin = $('.header .topRight').attr('login') == 'True' ? true : false; // 是否登录
    $('.appointment-list li .order').each(function () {
        if (isLogin == true) {
            var isMobile = true ;// 是否绑定手机号
            if ($(this).attr('data-mobile') == ''){
                isMobile = false
            }
            if ($(this).attr('data-mobile') == 'None'){
                isMobile = false
            }
            if (isMobile == true) {
                $(this).click(function () {
                    //将所有popup的数据同步
                    syncAppointmentData($(this));
                    $('#appointment-study').modal({show: true, keyboard: false, backdrop: 'static'});
                });
            } else {
                $(this).click(function () {
                    $(".captchaMy").children().remove();
                    captcha(".captchaMy", "verifyMobile/", function (cap) {
                        captchaPhone = cap;
                    });

                    $('#newPhone').modal({show: true, keyboard: false, backdrop: 'static'});
                })
            }
        } else {
            $(this).click(function () {
                $('#loginModal').modal({show: true, keyboard: false, backdrop: 'static'});
            });
        }
    });
    $('#appointment-study .m-close').click(function () {
        $('#appointment-study').modal('hide');
    });

    $('#newPhone .zy_close').click(function () {
        $('#newPhone').modal('hide');
    });

    /*
     * @ 预约试学成功弹窗
     *
     */
    //var isSuccess = true; // 是否预约成功
    $('.enter-appo').click(function () {
        $.ajax({
            type: "POST",
            url: $(this).attr('hrf'),
            data: {'class_id': $(this).attr('data-class-id')},
            dataType: "json",
            success: function (data) {
                if (data['status']) {
                    $('#appointment-success').modal({show: true, keyboard: false, backdrop: 'static'});
                } else {
                    $('#appointment-fail .fail').text('预约失败，' + data['message'])
                    $('#appointment-fail').modal({show: true, keyboard: false, backdrop: 'static'});
                }
            },
        });
        //if(isSuccess == true){
        //    $('#appointment-success').modal({show:true, keyboard:false,backdrop: 'static'});
        //}else{
        //    $('#appointment-fail').modal({show:true, keyboard:false,backdrop: 'static'});
        //}
    })
    $('.know').click(function () {
        $('#appointment-success').modal('hide');
        window.location.reload();
    });
    $('.retry').click(function () {
        window.location.reload();
    });

    /*
     * @ 提交表单
     *
     */
    $("#newPhone .personalCbtn").click(function () {
        $.when(sendsms($(this))).then(function (a) {
            $("#newPhone2 .pm").slideUp();
            var npa = $("#newPhone2 .fg > a");
            npa.addClass("smsend").html("重发验证码(<span>5</span>s)");
            setInObj = setInterval(_foo($("#newPhone2 .fg > a>span"), 60, function () {
                npa.html("重发验证码").removeClass("smsend");
                npa.unbind().click(onceSend);
            }), 1000);
        });
    });

    $("#newPhone2 .personalCbtn").click(function () {
        $.ajax({
            type: "POST",
            url: "/home/settings/bind_mobile/",
            data: {"mobile": PhoneValue, "mobile_code": $("#newPhone2 .pcsBasicTableTxt").val()},
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
                $(this).css("pointer-events", "none");
            },
            success: function (data) {
                if (data.success) {
                    $("#newMeg").modal("show");
                    setInObj = setInterval(_foo($("#newMeg .p2>span"), 5, function () {
                        $("#newMeg").modal("hide");
                        location.reload();
                    }), 1000);
                } else {
                    $("#newPhone2 .pm").html(data.message).slideDown();
                }
            },
            complete: function (XMLHttpRequest) {
                $(this).css("pointer-events", "auto");
            }
        });
    });
    //同步弹窗：预约试学和预约试学成功弹窗的 文本数据
    function syncAppointmentData($this) {
        var name = $this.siblings('.first').html();
        $pThree = $this.parent().siblings(".three");
        var d_week = $pThree.find('.first').html();
        var d_date = $pThree.find('.second').html();
        var d_time = $pThree.find('.third').html();
        var mobile = $this.attr('data-mobile');
        var class_id = $this.attr('data-class-id');
        //赋值 预约试学
        $("#appointment-study .second .name").html(name);
        $("#appointment-study .second .name").siblings().html(d_week + ' ' + d_date + '' + d_time);
        $("#appointment-study .phone-num").html(function (i, oldtext) {
            return mobile + ' ' + oldtext.substring(oldtext.indexOf('<a'));
        });
        $("#appointment-study .enter-appo").attr('data-class-id',class_id);
        //预约试学成功
        $("#appointment-success .second .name").html(name);
        $("#appointment-success .second .name").siblings().html(d_week + ' ' + d_date + '' + d_time);
        $("#appointment-success .phone-num").html(mobile);
    }


    function sendsms($this) {
        return $.ajax({
            type: "POST",
            url: "/home/settings/bind_mobile/sendsms/",
            data: {
                "mobile": $("#newPhone .pcsBasicTableTxt").val(),
                "type": "verifyMobile",
                'geetest_challenge': $('#newPhone .geetest_challenge').attr('value'),
                'geetest_validate': $('#newPhone .geetest_validate').attr('value'),
                'geetest_seccode': $('#newPhone .geetest_seccode').attr('value')
            },
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
                $this.css("pointer-events", "none");
            },
            success: function (data) {
                if (data.success) {
                    $("#newPhone2").modal("show");
                    PhoneValue = $("#newPhone .pcsBasicTableTxt").val();
                } else {
                    $("#newPhone .megError").html(data.message).slideDown();
                    captchaPhone.refresh();
                }
            },
            complete: function (XMLHttpRequest) {
                $this.css("pointer-events", "auto");
            }
        });
    }

    var setInObj, setIn_num = 60;

    function setIn(dom, time, callback) {
        setIn_num--;
        dom.html(setIn_num);
        if (setIn_num <= 0) {
            setIn_num = time || setIn_num;
            callback.call(this);
            clearInterval(setInObj);
        }
    }

    function _foo(dom, time, callback) {
        setIn_num = time || setIn_num;
        clearInterval(setInObj);
        return function () {
            setIn(dom, time, callback);
        }
    }

    // 再次发送
    function onceSend() {
        var $this = $(this);
        $this.html("重发验证码(<span>60</span>s)").css("pointer-events", "none");
        $.ajax({
            type: "POST",
            url: "/home/settings/bind_mobile/sendsms/",
            data: {"mobile": PhoneValue, "retry": true},
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
            },
            success: function (data) {
                if (data.success) {
                    var npa = $("#newPhone2 .fg > a");
                    $("#newPhone2 .pm").html("手机短信验证码已发送，请查收！").slideDown();
                    $this.removeAttr("style").addClass("smsend");
                    setInObj = setInterval(_foo($("#newPhone2 .fg > a>span"), 60, function () {
                        npa.html("重发验证码").removeClass("smsend");
                        npa.unbind().click(onceSend);
                        $this.css("pointer-events", "auto");
                    }), 1000);
                }
                else {
                    $("#newPhone2 .pm").html(data.message).slideDown();
                }
            },
            complete: function (XMLHttpRequest) {
            }
        });
    }
    // 贴心小提示
    $('.free-step').on('click', function(){
        $('#free-tips').modal('show');
    });

    $('#free-tips .i-know').on('click', function(){
        $('#free-tips').modal('hide');
    })
})