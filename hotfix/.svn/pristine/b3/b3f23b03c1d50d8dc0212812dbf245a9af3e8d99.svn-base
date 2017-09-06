$(function(){
    $(".wapPay .expand").bind("touchend",function() {
        $(this).hide();
        $(".wapPay .resume").addClass("show");
    });

    var career_course_id = $("#career_course_id").text();
    var class_coding = $("#class_name").text();
    //var mobile_number = $("#phone").text();
    var mobile_number = 0; // 沿用PC端的做法，默认为0.
    var pay_category = 0;  // 默认全款
    var pay_service_provider = 10;  // 默认为支付宝

    // 学习类型响应函数
    function study_type(){
        $(event.target).parents("li").addClass("checked").siblings().removeClass("checked");
        var reg_type = $(event.target).parents("li").find("input")
        $(".payInfo em").html(reg_type.attr("price"));
        if(reg_type.val() == 'employment'){  // 全款付款
            pay_category = 0;
        } else if(reg_type.val() == 'interest'){  // 无就业付款
            pay_category = 6;
        }
    }

    // 绑定学习类型按钮
    $(".wapPay .payAims span").each(function(){
        $(this).bind("touchend", study_type)
    });

    // 支付类型的函数
    function pay_type(){
        $(event.target).parents("li").addClass("checked").siblings().removeClass("checked");
        var way = $(event.target).parents("label").find("input").val();
        if(way == 'mfq'){ //么么贷
            pay_service_provider = 5;
        } else if(way == 'fql'){ //分期乐
            pay_service_provider = 7;
        } else if(way == 'weixin'){  //微信
            pay_service_provider = 4;
        } else if(way == 'zfb'){  //支付宝
            pay_service_provider = 10;
        }
        console.log(pay_service_provider);
    }

    // 绑定支付类型按钮
    $(".wapPay .payWay span").each(function(){
        $(this).bind("touchend", pay_type);
    });

    // 确定支付按钮
    $(".payOffBtn").bind("touchend", function(){
        common_gopay(career_course_id, class_coding, pay_category, pay_service_provider, mobile_number);
    });

    // 通用的gopay函数
    // 由templates/mz_pay/pay_step.html中的函数gopay改良而来
    // @note:
    // cur_career_id: 报名的职业课程id
    // choose_class_coding: 班级名字
    // choose_pay_type: 付款类型, 现在有两种类型: 一般付款和无就业保证付款. 之前还有488预付款, 现已取消
    // service_provider: 支付渠道. 支付渠道可以决定付款方式: 支付宝和微信支付为全款支付, 么么贷和分期乐为分期付款

    function common_gopay(cur_career_id, choose_class_coding, choose_pay_type, service_provider, phone){
        if(cur_career_id == undefined || choose_pay_type == undefined || choose_class_coding == undefined || service_provider ==undefined){
            alert('支付信息不完整，不能支付');
            return;
        }
        if(service_provider==5){
            window.location.href = "/pay/go/"+cur_career_id+"/"+choose_pay_type+"/"+choose_class_coding+"/"+service_provider+"/"+phone + '/0/'
        }else{
            window.open("/pay/go/"+cur_career_id+"/"+choose_pay_type+"/"+choose_class_coding+"/"+service_provider+"/"+phone + '/0/','_blank');
            //$('#third-pay-tips').modal('show');
        }
    }
});