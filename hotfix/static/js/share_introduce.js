
function share_introduce_login(){
    var OFF = true;

    // 首页老带新弹窗交互
    $('.red-top').on('click',function(){
        if( OFF ){
            $.ajax({
                type:'GET',
                url:'/user/get_invitation_code/',
                dataType:'JSON',
                async:false,
                success: function(data){
                    $('.share-link').val(data.invitation_link);
                    $('.QR-code').html('<img src="' + data.qrcode + '"/>');
                }
            });

            OFF = false;
        }

        jiathis_config={
	        url:$('.share-link').val(),
	        summary: "老带新学费立减200！麦子学院为我助学加油",
	        pic: 'http://' + window.location.host + "/static/images/add_invited_160408/banner.png"
        };

        $('#Old-with-new-tips').modal('show');
        $('.Old-with-new-close img').on('click',function(){
        $('#Old-with-new-tips').modal('hide');
        });
        $('.Invitation-rules').on('click',function(){
        $(this).addClass('hide');
        $('.Invitation-rules-info,.Invitation-rules-up').removeClass('hide').addClass('show');
        $('.Invitation-rules-up').on('click',function(){
          $('.Invitation-rules').removeClass('hide');
          $('.Invitation-rules-info,.Invitation-rules-up').removeClass('show').addClass('hide');
        });
        });
    });
}

function share_introduce_not_login(){
    $('.red-top').on('click',function(){
        $('#registerModal').modal('hide');
        $('#loginModal').modal('show');
    });
}

function share_introduce_register(){
    // 首页老带新注册交互
    $('#own-register-tips').modal('show');
    $('.own-register-close').on('click',function(){
      $('#own-register-tips').modal('hide');
    });
    $('.own-just-register').on('click',function(){
        $('#own-register-tips').modal('hide');
        $('#registerModal').modal('show');
    });
}