function share_introduce_login(){
    var OFF = true;

    // 首页老带新弹窗交互
    if( OFF ){
        $.ajax({
            type:'GET',
            url:'/user/get_invitation_code/',
            dataType:'JSON',
            async:false,
            success: function(data){
                $('#share-link').val(data.invitation_link);
                $('.QR-code').html('<img src="' + data.qrcode + '"/>');
            }
        });

        OFF = false;
    }

    jiathis_config={
        url:$('#share-link').val(),
        summary: ":快来领取200元现金红包,和我一起加入企业直通班！傲娇带你飞，一起挺进BAT！",
        pic: 'http://' + window.location.host + "/static/mz_lps4/images/wx-red-packets2.png"
    };
};


function share_introduce_not_login(){
	$(".bg-box").show();
    $(".login-box").show(200);
}