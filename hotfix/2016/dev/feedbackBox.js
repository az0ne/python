$(function(){
    //阻止键盘事件
    $('#feedback_content,#telphone').keyup(function (event) {
        event.stopPropagation();
    });

    //弹窗隐藏时的操作
    $("#feedbakBox").on("hidden.bs.modal", function() {
        removeDate();
    });
    //模块弹出
    $("#feedbackfade").click(function(){
        $("#feedbakBox").modal('show');
    });
    //隐藏模块
    $("#feedbakBox .zy_close").click(function(){
        $(this).parents("#feedbakBox").modal('hide');
    });

    //提交按钮不可用
    function addDisable(){
        $("#feedbakBox .subminBtn").addClass("disable").attr("disabled","disabled");
    }
    //提交按钮可用
    function removeDisable(){
        $("#feedbakBox .subminBtn").removeClass("disable").removeAttr("disabled");
    }
    //“文本框”及手机号码框获取焦点时，提交可用且隐藏错误提示
    $("#feedbakBox input[type=tel],#feedbakBox textarea").keyup(function(){
        removeDisable();
        $(this).siblings("em").hide();
    });
    //input框、组合框及文本框失去焦点时，判断值是否全为空，是则让提交按钮不可用，否则可用
    $("#feedbakBox input[type=file],#feedbackBox #telphone,#feedbakBox textarea").blur(function(){
        if($("#feedbakBox input[type=file]").val() =="" && $("#feedbakBox #telphone").val() =="" && $("#feedbakBox textarea").val() ==""){
            addDisable();
        };
    });
    $("#feedback_type").blur(function(){
        if(!$("#feedback_type").val()==""){
            removeDisable();
            $(this).siblings("em").hide();
         }
    });

    //鼠标按下时，隐藏错误提示，提交按钮可用
    $(".feedbackcaptcha").on('mousedown',$('.gt_slider_knob'),function(){
        $(".feedbackcaptcha").parent().siblings("em").hide();
        removeDisable();
    });
    //提交按钮的点击事件
    var textareaVal,telVal,reg,textareaValLength;
    $("#feedbakBox .subminBtn").click(function(){
        textareaVal = $("#feedbakBox textarea").val();
        telVal = $("#feedbakBox #telphone").val();
        var reg = /^0?1[3|4|5|7|8][0-9]\d{8}$/;//手机号码验证
        //组合框为空则提交按钮不可用且显示提示信息
        if($("#feedback_type").val() == ""){
            $("#selectError").show();
            addDisable();
            return;
        }
        //文本框为空则提交按钮不可用且显示提示信息
        else if(textareaVal == ""){
            $("#feedbakBox #textareaError").show();
            addDisable();
            return;
        }
        //手机号码不合法或者为空则提交按钮不可用且显示提示信息
        else if(reg.test(telVal) === false || telVal==""){
            $("#feedbakBox #telError").show();
            addDisable();
            return;
        }
        //显示错误提示，提交按钮不可用
       else if(!$(".feedbackcaptcha .gt_ajax_tip").hasClass("gt_success")) {
            $(".feedbackcaptcha").parent().siblings("em").show();
            addDisable();
            return;
        }
       else{
            feedback_submit();
       }
        console.log($("#feedback_type").val())
    });

    //显示文本框可以输入的字数，大于200字时，提交按钮不可用，且错误提示信息隐藏
    $("#feedbakBox textarea").keyup(function(){
        textareaValLength = $("#feedbakBox textarea").val().length;
        $("#feedbakBox .textareaBox span em").html(200-textareaValLength);
        $(this).parent().siblings("em").hide();
    });

    //图片上传
    var errorMsg = $(".fileerrorTip"),
        msgTips = errorMsg.html();
    $('#feedbackupload').fileupload({
        url:"/common/feedback/image_upload/",
        dataType: 'json',
        autoUpload: true,
        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /^(png|jpg|jpeg)$/i;
            var filesize = data.originalFiles[0]['size'] / (1024);
            Ntype = data.originalFiles[0]['name'].split('.');
            Ntype = Ntype[Ntype.length - 1];

            if (acceptFileTypes.test(Ntype)) {
                errorMsg.html("").hide();
                $("#feedbakBox .showFileName").html(data.originalFiles[0]['name']);
                $(".file>span").html('重新上传');
                removeDisable();
            }else{
                $("#feedbakBox .showFileName").html("");
                errorMsg.html('支持图片格式：png、jpg、jpeg').show();
                uploadErrors.push('Not an accepted file type');
                addDisable();
                setTimeout(function () {
                    errorMsg.html(msgTips);
                }, 2000);
            }
            if (parseInt(filesize) > 500) {
                errorMsg.html('文件超过500KB大小！').show();
                uploadErrors.push('Filesize is too big');
                addDisable();
                setTimeout(function () {
                    errorMsg.html(msgTips);
                }, 2000);
            }

             if(uploadErrors.length==0){
                data.submit();
              }

        },
        done: function (e, data) {
              var img_url = data.result.image_url;
              $("#hideen_image_url").val(img_url)
        }
    });
    captcha(".feedbackcaptcha","");
});

function removeDate(){
    $("input[type=reset]").trigger("click");
    $('.feedbackcaptcha').empty();
    captcha(".feedbackcaptcha","");
    $("#hideen_image_url").val("");
    $("#feedbakBox .showFileName").html("");
    $(".file>span").html('上传图片');
}

function feedback_submit(){
    var data = {feedback_type:$("#feedback_type option:selected").val(),
                feedback_content:$("#feedback_content").val(),
                contact:$('#telphone').val(),
                image_url:$("#hideen_image_url").val(),
                current_url:window.location.href
                };
    $.ajax({
        type:"post",
        url:"/common/feedback/save/",
        dataType:"json",
        data:data,
        success:function(data){

           $("#feedbakBox").modal('hide')
           $("#feedbakBoxSuccess").modal('show');
           setTimeout(
           function(){$("#feedbakBoxSuccess").modal('hide')},2000);
        }
    });
}