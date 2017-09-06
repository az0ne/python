var img_top_margin,img_left_margin,img_width,img_height,is_upload=false;
$(function(){
    // 注册验证码刷新事件
    $('#new_mobile_form .captcha-refresh').click({'form_id':'new_mobile_form'},refresh_captcha);
    $('#new_mobile_form .captcha').click({'form_id':'new_mobile_form'},refresh_captcha);
    $('#new_email_form .captcha-refresh').click({'form_id':'new_email_form'},refresh_captcha);
    $('#new_email_form .captcha').click({'form_id':'new_email_form'},refresh_captcha);

    save_click();//个人资料保存
    load_provid(); //加载省份

    $("#id_prov").change(function(){
        val = $("#id_prov  option:selected").val();
        city_list(val);
    });

    save_click();//个人资料保存
    $("#id_prov").change(function(){
        val = $("#id_prov  option:selected").val();
        city_list(val);
    })
    // Create variables (in this scope) to hold the API and image size
    $('#change-pass').click(function(){
        change_pass();
    });

    var selection = null;
    var width = 0;
    var height = 0;
    $('#file_upload').fileupload({
        url: '/user/student/avatar/upload/',
        dataType: 'json',
        autoUpload: true,
        done: function (e, data) {
            // console.log(data.result);
            if(data.result.status=="success"){
                $('#photo').attr({"src":"/uploads/temp/"+data.result.filename});
                $('#photo').css({maxWidth:'100%',maxHeight:'100%'});
                $('#cut-photo').attr({"src":"/uploads/temp/"+data.result.filename});
                $('#photo').load(function(){
                    width = $('#photo').width();
                    height = $('#photo').height();
                    preview({width:width,height:height}, {x1:(width-100)/2, y1:(height-100)/2, width:100, height:100}); 
                    
                })
                //console.log(width, height);
                //console.log(width/2-50, (height-100)/2, width/2+50, height/2+50)
                if(selection === null) {
                     selection = $('#photo').imgAreaSelect({
                        fadeSpeed : 400,
                        aspectRatio : '1:1',
                        handles : true,
                        //x1:0, y1:0, x2:100 ,y2:100,
                        onSelectChange : preview, 
                        maxWidth: 200, 
                        maxHeight: 200,
                        minWidth:100,
                        minHeight:100,
                        instance: true,
                        persistent:true,

                });

                }   
                    selection.cancelSelection();
                    $('#photo').load(function(){
                        selection.setSelection((width-100)/2, (height-100)/2, (width+100)/2, (height+100)/2, true);
                        selection.update();
                        selection.setOptions({show:true})
                    })

                
                
            }else if(data.result.status=="failure"){
                $("#tips-avatar-upload").html(data.result.message).show().delay(8000).fadeOut();
            }else{
                $("#tips-avatar-upload").html('未知错误').show().delay(8000).fadeOut()
            }
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

    $('.close').click(function(event) {
        selection.setOptions({hide:true});
        // $('#photo').attr({"src":""});    
        // $('#cut-photo').attr({"src":""});
    });
    $('#change-photo').click(function(event) {
       selection.setOptions({show:true});
    });
});

function preview(img, selection) {
        if (!selection.width || !selection.height)
            return;
        var scaleX = 150 / selection.width;
        var scaleY = 150 / selection.height;
        width = img.width;
        height = img.height;
        // console.log(scaleY * selection.y1);
        $('#cut-photo').css({
            width : Math.round(scaleX * width),
            height : Math.round(scaleY * height),
            marginLeft : -Math.round(scaleX * selection.x1),
            marginTop : -Math.round(scaleY * selection.y1),
            maxWidth:'none',
            display: 'block'
        });
        
        $("#startX").val(selection.x1);
        $("#startY").val(selection.y1);
        $("#width").val(selection.width);
        $("#height").val(selection.height);
}
//裁剪头像
function avatar_crop() {
    if($('#photo').attr("src") =='/static/images/avata-bg.png'){
        return;
    }
    picwidth = $('#photo').width();
    picheight = $('#photo').height();
    var params="&marginTop="+parseInt($("#startX").val())+"&marginLeft="+parseInt($("#startY").val())+"&width="+parseInt($("#width").val())+"&height="+ parseInt($("#height").val())+"&picwidth="+parseInt(picwidth)+"&picheight="+parseInt(picheight);
    $.ajax({
        type: "get",
        url: "/user/student/avatar/crop/",
        data: params,
        dataType: "json",
        success: function (data) {
            location.reload();
            if(data.status == "success"){
                location.reload();
                // $("#tips-avatar-upload").attr("class","tips-error bg-success").html("头像已经成功保存").show(500).delay(2000).fadeOut(1000,function(){ location.reload(); });
            }
        }
    })
}

// 省份加载
function load_provid(){
    str = $("#default_p_c").val();
    arr = str.split("_");
    if(arr==','){
        $('#id_prov').selectedIndex = 1;
        pid = $('#id_prov').val();
        city_list(pid);
        $('#id_city').selectedIndex = 1;
    }else{
        $("#id_prov").val(arr[0]);
        city_list(arr[0]);
        $("#id_city").val(arr[1]);
    }

}

// 城市加载
function city_list(provid){
    $.ajax({
        type: "GET",
        async: false,
        url: "/user/city/list/",
        data: {provid:provid},
        dataType: "json",
        success: function(data){
            var data = eval(data);
            var str = '';
            $(data).each(function(i,val) {
                var a = val['cityid'];
                $(a).each(function(j,v){
                    str += '<option value="'+v[0]+'">'+v[1]+'</option>';
                });
            });
            $('#id_city').html(str);


        }
    });

}

//个人资料保存
function save_click(){
    $("#user_save").click(function(){
        user_info_save();
    });
}

//用户个人资料保存
function user_info_save(){
    $.ajax({
        type: "POST",
        url:"/user/info/save/",
        data:$('#user_info_save').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#msg").html("保存中...").show(500);
        },
        success: function(data) {
            var msg="";
            for (i in data)
            {
                msg = data[i];
                $("#id_"+i).focus();

                $("#msg").removeClass("bg-warning").addClass("bg-danger").html(msg).show(500);
                if(msg){
                    return false;
                }else{
                    return true;
                }
            }
            $("#msg").html("保存成功").removeClass('bg-warning').removeClass('bg-danger').addClass("bg-success").show().delay(3000).fadeOut();
        }
    });
}

// 发送激活邮件
function user_info_email(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/info/email/",
        data:$('#user_info_save').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#msg").html("验证邮件发送中...").show(500);
        },
        success: function(data) {
            if(data.email){
                $("#msg").html(data.mobile).show(500);
                $("#id_email").focus();
            }else if(data.status == 'success'){
                $("#msg").html("激活验证邮件已发送").show(500);
                $("#vaild_email").attr("disabled","disabled");
            }else if(data.status == 'failure'){
                $("#msg").html("激活验证邮件发送失败").show(500);
            }
        }
    });
}

//新增邮箱
function addemail(){
    $("#id_email_ue").val("");
    $("#id_captcha_ue_1").val("");
    $("#new_email_tips").hide();
    refresh_captcha({"data":{"form_id":"new_email_form"}});
    $('#addemailModal').modal('show');
}
//设置新手机号
function newMobilnumber(){
    $("#id_mobile_um").val("");
    $("#id_captcha_um_1").val("");
    $("#new_mobile_tips").hide();
    refresh_captcha({"data":{"form_id":"new_mobile_form"}});
    $('#newMobilnumberModal').modal('show');
}
//设置修改新手机号下一步操作
function newMobilnumberNext(){
    $("#id_mobile_code_f").val("");
    $('#newMobilnumberNextModal').modal('show');
}

function change_pass(){
    $.ajax({
        type: "POST",
        url:"/user/change/password/",
        data:$('#change_pass').serialize(),
        beforeSend:function(XMLHttpRequest){
            $("#resetpswModal .tips-error").html("保存中...").show(500);
        },
        success: function(data) {
            var msg="";
            for (i in data)
            {
                msg = data[i];
                $("#id_"+i).focus();

                $("#resetpswModal .tips-error").removeClass("bg-warning").addClass("bg-danger").html(msg).show(500);
                if(msg){
                    return false;
                }else{
                    return true;
                }
            }
            $("#resetpswModal .tips-error").html("保存成功").removeClass('bg-warning').removeClass('bg-danger').addClass("bg-success").show().delay(2000).fadeOut(1000,function(){ location.reload(); });
        }
    });
}

// 修改手机号表单提交
function new_mobile_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/mobile/update/sendsms/",
        data:$('#new_mobile_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#new_mobile_tips").html("验证中...").show(500);
        },
        success: function(data) {
            if(data.mobile_um){
                $("#new_mobile_tips").html(data.mobile_um).show(500);
                $("#id_mobile_um").focus();
            }else if(data.captcha_um){
                $("#new_mobile_tips").html(data.captcha_um).show(500);
                $("#id_captcha_um_1").focus();
            }else if(data.status == "failure"){
                $("#new_mobile_tips").html("验证短信发送失败，请重试").show(500);
                $("#id_mobile_um").focus();
            }else if(data.status == "success"){
                $("#id_mobile_f").val($("#id_mobile_um").val());
                $('#newMobilnumberModal').modal('hide');
                newMobilnumberNext();
            }
            refresh_captcha({"data":{"form_id":"new_mobile_form"}});
        }
    });
}

//个人资料手机新增和修改手机验证码表单验证
function mobile_code_update_mobile_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/mobile/update/",
        data:$('#mobile_code_update_mobile_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#update_mobile_tips").html("验证中...").show(500);
        },
        success: function(data) {
            if(data.mobile_code_f){
                $("#update_mobile_tips").html(data.mobile_code_f).show(500);
                $("#id_mobile_code_f").focus();
            }else if(data.status == "success"){
                //验证成功，回到个人资料修改界面
                $("#update_mobile_tips").html("手机信息更新成功").show(500).delay(2000).fadeOut(1000,function(){ location.reload(); });
            }else{
                $("#update_mobile_tips").html("手机信息更新失败").show(500)
            }
        }
    });
}

// 修改邮箱表单提交
function new_email_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/email/update/",
        data:$('#new_email_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#new_email_tips").html("验证中...").show(500);
        },
        success: function(data) {
            if(data.email_ue){
                $("#new_email_tips").html(data.email_ue).show(500);
                $("#id_email_ue").focus();
            }else if(data.captcha_ue){
                $("#new_email_tips").html(data.captcha_ue).show(500);
                $("#id_captcha_ue_1").focus();
            }else if(data.status == "failure"){
                $("#new_email_tips").html("验证邮件发送失败，请重试").show(500);
                $("#id_email_ue").focus();
            }else if(data.status == "success"){
                $("#new_email_tips").attr("class","tips-error bg-success").html("验证邮件已发送，请查收邮件完成后续操作").show(500).delay(2000).fadeOut(1000,function(){ location.href = '/user/info?'+Math.random(); });
            }
            refresh_captcha({"data":{"form_id":"new_email_form"}});
        }
    });
}
