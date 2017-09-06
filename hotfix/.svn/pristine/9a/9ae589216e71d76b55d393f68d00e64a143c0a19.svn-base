//仅用于测试图片验证码功能

// 获取验证码, 并回调给定的函数处理验证码
function get_captcha_image(func_obj){
    $.ajax({
        type:"GET",
        url:"/captcha/refresh/",
        success:function(data){
            window.captcha_key=data.key;
            //console.log(captcha_key);
            func_obj(data.image_url);
        }
    });
}

// 验证验证码
var verify_code = function(code, befor_func, fail_func, succes_func){
    if(code!=""){
        $.ajax({
            type:"GET",
            url:"/captcha/verify/"+captcha_key+"/"+code+"/",

            beforeSend:function(XMLHttpRequest){
                if(befor_func){
                    befor_func();
                }
            },
            success:function(data){
                if(data.status=="success"){
                    console.log("验证成功！");
                    if(succes_func){
                        succes_func();
                    }
                } else {
                    if(fail_func){
                        fail_func();
                    }
                }
            }
        });
    }
}