$(function(){
    //lps3.1链接过来
    if(index=='1'){
        $('.money_val').text($('.selected .col-left .new').text());
        var pay_type = $('section.selected').attr('pay_type');
        $('#submit_order').attr('pay_type', pay_type);
    }
    // 选择支付银行
    $('.sub_pay_bank ul li').on('click', function () {
        $(this).addClass('bc-ff').siblings().removeClass('bc-ff');;
    });
    // 选择支付类型
    $('.select-type section').on('click', function () {
        $(this).addClass('selected').siblings().removeClass('selected');
        $('.money_val').text($('.selected .col-left .new').text());
        var pay_type = $(this).attr('pay_type');
        $('#submit_order').attr('pay_type', pay_type);
    });
    // 提交支付
    $('#submit_order').on('click', function (){
        var pay_way = $('.pay-bank ul').children(".bc-ff").attr("name");
        if (pay_way == 0){
            if($("#sub_repay ul").children(".bc-ff").attr("name") == 5){
                $('#module-confirm-stage').modal('show');
            }else if($("#sub_repay ul").children(".bc-ff").attr("name") == 9){
                if(userMobile != 'None'){
                    gopay();
                }else{
                    $("#bindPhoneNumber").modal('show');
                }
            }else{
                gopay();
            }
        }else{
            gopay();
        }
    });
    // 么分期输入电话
    $('#continue').click(function(){
        var userMobile = $('input[name=user_mobile]').val();
        var msg = '';
        var telReg = !userMobile.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/g);
        $('#mobile_code_telephone-tips').hide();
        if( userMobile == null || userMobile == ''){//空
            msg = '亲！请输入您的手机号码。';
            $('#mobile_code_telephone-tips').show().html(msg);
            return false;
        }else if(telReg){//不匹配
            msg = '亲！您输入的手机号码不正确。';
            $('#mobile_code_telephone-tips').show().html(msg);
            return false;
        }else{
            showAgreenment();
        }
    });

    function showAgreenment(){
        $('#module-confirm-stage').modal('hide');
        $('#module-agreement').modal('show');
        $('#check_check').attr('checked',false);
        $('#agree_pay').attr("disabled", "disabled");
    }

    $('#check_check').on('click', enable_submit_check);

    function enable_submit_check(){
        var check_contract = document.getElementById("check_check");
        var agree_contract = document.getElementById("agree_pay");

        if (check_contract.checked == true) {
            agree_contract.removeAttribute("disabled");
        }else{
            agree_contract.setAttribute("disabled", "disabled");
        }
    }

    function gopay(){
        var choose_pay_type = $('#submit_order').attr('pay_type');
        var pay_way = $('.pay-bank ul').children(".bc-ff").attr("name");
        if (pay_way == 0) {
            service_provider = $("#sub_repay ul").children(".bc-ff").attr("name");
        }else{
            service_provider = pay_way;
        }
        var oth = 0;
        if(cur_career_id == undefined || choose_pay_type == undefined || choose_class_coding == undefined || service_provider == undefined){
            alert('支付信息不完整，不能支付');
            return;
        }
        if(service_provider == 5){
            oth = $("#zy_user_mobile_tel").val();
            window.location.href = "/pay/go/"+cur_career_id+"/"+choose_pay_type+"/"+choose_class_coding+"/"+service_provider+"/"+ oth + '/' + has_discount + '/'
        }else if(service_provider==8){
            oth = $("#sub_bank ul .bc-ff").attr('name');
            window.open("/pay/go/"+cur_career_id+"/"+choose_pay_type+"/"+choose_class_coding+"/"+service_provider+"/" + oth + '/' + has_discount + '/', '_blank');
            $('#third-pay-tips').modal('show');
        }else{
            window.open("/pay/go/"+cur_career_id+"/"+choose_pay_type+"/"+choose_class_coding+"/"+service_provider+"/" + oth + '/' + has_discount + '/','_blank');
            $('#third-pay-tips').modal('show');
        }
    }

    $("#agree_pay").click(function(){
        gopay();
    });

    $('#pay-success').click(function(){
        window.location.href = href2;
    });

    $('#pay-fail').click(function(){
        window.location.reload();
    });

    $('.third-pay-close img').on('click',function(){
        $('#third-pay-tips').modal('hide');
    });
    // 选择支付方式
    var $payBank = $('.pay-bank ul li'),$subRepay = $('#sub_repay'),$subBank = $('#sub_bank');
    $payBank.on('click', function(){
        $(this).addClass('bc-ff').siblings().removeClass('bc-ff');
        if($(this).hasClass('repay')){            
            $subRepay.show();
            $subBank.hide();
        }else if($(this).hasClass('bank')){
            $subRepay.hide();
            $subBank.show();
        }else{
            $subRepay.hide();
            $subBank.hide();
        }
    });
});