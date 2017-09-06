define(function(require, exports, module){
    require('swiperjs');
    var $justAppoBtn,$appoSuccessModal,$appoSuccess,$appoSuccessClose,$phoneNum,$verification,telReg, tipsMsg, $sendVerif;

    $justAppoBtn = $('.just-appo-btn');
    $appoSuccessModal = $('.appo-success-modal');
    $appoSuccess = $('.appo-success');
    $appoSuccessClose = $('.appo-success-close');
    $phoneNum = $('#phone-num');
    $verification = $('#verification');
    $sendVerif = $('.send-verif');

    telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;

    $justAppoBtn.on('click',function(){
        if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if(!telReg.test($phoneNum.val())){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if($verification.val() == '' || null){
            tipsMsg = '手机验证码输入错误，请重试';
            Tips($verification, tipsMsg);
        }else{
            verifyCaptcha();
        }
    });

    $appoSuccessClose.on('click', function(){
        Animatehide();
    });

    $(window).scroll(function(){
        var $LeftHeight, $RightHeight, $appointmentForm;
        
        $LeftHeight = $('.course_appointment .main-container > .left').height();
        $RightHeight = $('.course_appointment .main-container > .right').css('height', $LeftHeight + 'px');
        $appointmentForm = $('.appointment-form');

        if ($appointmentForm.offset().top > 1045) {
            $appointmentForm.css({'top': 'auto','bottom': '86px', 'position': 'absolute'});
        }else if($appointmentForm.offset().top - $('.head-container').offset().top > 158) {
            $appointmentForm.removeAttr('style');
        }
    });

    function Animateshow(){
        $appoSuccessModal.css({
            'z-index': 100,
            'opacity': 1,
            'filter': 'Alpha(Opacity = 100)'
        });
        setTimeout(function(){
            $appoSuccess.css({
                'margin': '0 auto 0'
            });
            $(document.body).css({"position":"fixed","width":"100%"});
        }, 500);
    }

    function Animatehide(){
        $appoSuccess.css({
            'margin': '-500px auto 0'
        });

        setTimeout(function(){
            $appoSuccessModal.css({
                'z-index': -100,
                'opacity': 0,
                'filter': 'Alpha(Opacity = 0)'
            });
            $(document.body).removeAttr('style');
        }, 500);
    }

    function Tips(obj,tipsMsg){
        obj.wrap('<div class="tips-box"></div>').after('<span class="tips">' + tipsMsg + '</span>');
        setTimeout(function(){
           obj.unwrap().siblings().remove('.tips');
           obj.focus();
        }, 4000);
    }

    function backData(data) {
        if (!data.success) {
            tipsMsg = data.message;
            Tips($phoneNum, tipsMsg);
        } else {
            Cuttime($sendVerif, 60);
        }
    }

    function sendsms() {
        $.ajax({
            type: "POST",
            url: "/course/mobile/sendsms/",
            data: {
                "mobile": $("#phone-num").val(),
                "career_id":$("#meeting_career_id").val(),
                "class_time":$("#meeting_class_time").val(),
                "type": "verifyMobile",
            },
            dataType: "json",
            success: backData,
            error: function(data){
                console.log(data.success);
            }
        });
    }
        
    function Cuttime(obj, time){        
        var countdown = null;
        obj.addClass("send").val("重新发送(60s)").attr('disabled', 'disabled');
        countdown = setInterval(function(){
            time--;
            obj.val("重新发送("+time+"s)");
            if(time <= 0){
                clearInterval(countdown);
                obj.removeClass("send").val("重新发送").removeAttr('disabled');
            }
        },1000);        
    }

    $sendVerif.on('click', function(){
        if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else{
            if(telReg.test($phoneNum.val())){
                sendsms();                
            }else if(!telReg.test($phoneNum.val())){
                tipsMsg = '请输入正确的手机号';
                Tips($phoneNum, tipsMsg);
            }
        }        
    });

    Slider();

    function Slider(){
        var mySwiper = new Swiper ('.swiper-container', {
          loop: true,
          nextButton: '.swiper-button-next',
          prevButton: '.swiper-button-prev',
          preloadImages: false,
          lazyLoading: true
        });
    }

    function postAjax(){
        $.ajax({
            type: 'POST',
            url: '/course/publicmeeting/save/',
            data: {
                mobile:$phoneNum.val(),
                career_id:$("#meeting_career_id").val(),
                class_time:$("#meeting_class_time").val(),
                qq_group:$("#meeting_qq_group").val(),
                task_title:$("#task_title").val()
            },
            dataType: 'JSON',
            success: function(data){
                if (data.status == "success"){
                    Animateshow();
                    $("#verification").val("");
                }
            }
        });
    }

    function verifyCaptcha() {
        $.ajax({
            type: "POST",
            url: "/course/mobile/verify/",
            data: {
                "mobile": $("#phone-num").val(),
                "mobile_code": $("#verification").val(),
                "career_id":$("#meeting_career_id").val(),
                "class_time":$("#meeting_class_time").val()
            },
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    postAjax();
                } else {
                    tipsMsg = '手机验证码输入错误，请重试';
                    Tips($verification, tipsMsg);
                }
            },
        });
    }
});