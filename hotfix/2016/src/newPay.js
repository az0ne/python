/*! LPS4.0 2016-10-10
 */
$(function () {
    function e() {
        $("#module-confirm-stage").modal("hide"), $("#module-agreement").modal("show"), $("#check_check").attr("checked", !1), $("#agree_pay").attr("disabled", "disabled")
    }

    function i() {
        var e = document.getElementById("check_check"), i = document.getElementById("agree_pay");
        1 == e.checked ? i.removeAttribute("disabled") : i.setAttribute("disabled", "disabled")
    }

    function c() {
        var e = $("#submit_order").attr("pay_type"), i = $(".pay-bank ul").children(".bc-ff").attr("name");
        service_provider = 0 == i ? $("#sub_repay ul").children(".bc-ff").attr("name") : i;
        var c = 0;
        return void 0 == cur_career_id || void 0 == e || void 0 == choose_class_coding || void 0 == service_provider ? (alert("支付信息不完整，不能支付"), void 0) : (5 == service_provider ? (c = $("#zy_user_mobile_tel").val(), window.location.href = "/pay/go/" + cur_career_id + "/" + e + "/" + choose_class_coding + "/" + service_provider + "/" + c + "/" + has_discount + "/") : 8 == service_provider ? (c = $("#sub_bank ul .bc-ff").attr("name"), window.open("/pay/go/" + cur_career_id + "/" + e + "/" + choose_class_coding + "/" + service_provider + "/" + c + "/" + has_discount + "/", "_blank"), $("#third-pay-tips").modal("show")) : (window.open("/pay/go/" + cur_career_id + "/" + e + "/" + choose_class_coding + "/" + service_provider + "/" + c + "/" + has_discount + "/", "_blank"), $("#third-pay-tips").modal("show")), void 0)
    }

    if ("1" == index) {
        $(".money_val").text($(".selected .col-left .new").text());
        var o = $("section.selected").attr("pay_type");
        $("#submit_order").attr("pay_type", o)
    }
    $(".sub_pay_bank ul li").on("click", function () {
        $(this).addClass("bc-ff").siblings().removeClass("bc-ff")
    }), $(".select-type section").on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected"), $(".money_val").text($(".selected .col-left .new").text());
        var e = $(this).attr("pay_type");
        $("#submit_order").attr("pay_type", e)
    }), $("#submit_order").on("click", function () {
        var e = $(".pay-bank ul").children(".bc-ff").attr("name");
        0 == e ? 5 == $("#sub_repay ul").children(".bc-ff").attr("name") ? $("#module-confirm-stage").modal("show") : 9 == $("#sub_repay ul").children(".bc-ff").attr("name") ? "None" != userMobile ? c() : $("#bindPhoneNumber").modal("show") : c() : c()
    }), $("#continue").click(function () {
        var i = $("input[name=user_mobile]").val(), c = "", o = !i.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/g);
        return $("#mobile_code_telephone-tips").hide(), null == i || "" == i ? (c = "亲！请输入您的手机号码。", $("#mobile_code_telephone-tips").show().html(c), !1) : o ? (c = "亲！您输入的手机号码不正确。", $("#mobile_code_telephone-tips").show().html(c), !1) : (e(), void 0)
    }), $("#check_check").on("click", i), $("#agree_pay").click(function () {
        c()
    }), $("#pay-success").click(function () {
        window.location.href = href2
    }), $("#pay-fail").click(function () {
        window.location.reload()
    }), $(".third-pay-close img").on("click", function () {
        $("#third-pay-tips").modal("hide")
    });
    var t = $(".pay-bank ul li"), a = $("#sub_repay"), s = $("#sub_bank");
    t.on("click", function () {
        $(this).addClass("bc-ff").siblings().removeClass("bc-ff"), $(this).hasClass("repay") ? (a.show(), s.hide()) : $(this).hasClass("bank") ? (a.hide(), s.show()) : (a.hide(), s.hide())
    })

});
$(document).ready(function () {
    $('.nine-pay-bg').css("display", "none");
    $('.nine-pay-bg').css({"width": "100%", "height": "100%"});

    function stopPropagation(e) {//把事件对象传入
        if (e.stopPropagation) //支持W3C标准
            e.stopPropagation();
        else //IE8及以下浏览器
            e.cancelBubble = true;
    }

    $('.nine_repay').click(function (e) {
        $('.nine-pay-bg').css("display", "block");
         $('.hong-pay-bg').css("display", "none");
        $(".pay_submit").hide();
        stopPropagation(e);
    })
    var codediv = $('.nine-pay-bg');
    var nine_hide_div = codediv.css("display");
    console.log(nine_hide_div);
    if (nine_hide_div = "block") {
        $(document).bind('click', function () {
            codediv.css('display', 'none');
            $(".pay_submit").show();
        });

        codediv.bind('click', function (e) {
            $('.nine-pay-bg').css("display", "block");
            stopPropagation(e);
        });
        $('.nine-otherPay').click(function (e) {
            $('.nine-pay-bg').css("display", "none");
            $('#sub_repay li').removeClass("bc-ff");
            stopPropagation(e);
        })
        $('.nine-paied').click(function (e) {
            $('.nine-pay-bg').css("display", "none");
            stopPropagation(e);
        })
    }


     $('.hong-pay-bg').css("display", "none");
    $('.hong-pay-bg').css({"width": "100%", "height": "100%"});
    $('.hong_repay').click(function (e) {
        $('.hong-pay-bg').css("display", "block");
        $('.nine-pay-bg').css("display", "none");
        $(".pay_submit").hide();
         console.log("hong_hide_div="+$('.hong-pay-bg').css("display"))
        stopPropagation(e);
    })

    var hongDiv = $('.hong-pay-bg');
    var hong_hide_div = hongDiv.css("display");

    console.log("hong_hide_div333==="+hong_hide_div);
    if (hong_hide_div = "block") {
        $(document).bind('click', function () {
            hongDiv.css('display', 'none');
            $(".pay_submit").show();
        });

        hongDiv.bind('click', function (e) {
            $('.hong-pay-bg').css("display", "block");
            stopPropagation(e);
        });
        $('.hong-otherPay').click(function (e) {
            $('.hong-pay-bg').css("display", "none");
            $('#sub_repay li').removeClass("bc-ff");
            stopPropagation(e);
        })
        $('.hong-paied').click(function (e) {
            $('.hong-pay-bg').css("display", "none");
            stopPropagation(e);
        })
    }


})
