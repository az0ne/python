
var aboutPhoto;
var old_user_photo;
$(function(){

           $('.personal_profile_btn').click(function(event){
               $.post('/user/get_photo_and_nickName/',{},function(datas) {

                   var $currentTarget = $(event.currentTarget);
                   aboutPhoto = $.commonTool.editUserInfo('#user_panel', null);
                   $("#real_name").val(datas.nick_name);
                   if (datas.people == "教师") {
                       $("#description").val(datas.description);
                   }
                   if (datas.people == "学生") {
                       $('.layui-layer-close').hide();
                   }
                   // 弹出框后，加载头像。如果没有头像，参数为null
                   aboutPhoto.fileChangeRunAjax = true;
                   // 检查是否已经上传国图片
                   if (!datas.avatar_middle_thumbnall) {
                       aboutPhoto.showPhoto("/uploads/" + $currentTarget.data('pic'));
                   } else {
                       aboutPhoto.showPhoto(datas.avatar_middle_thumbnall);
                       if (datas.avatar_middle_thumbnall) {
                           var temp_arr = datas.avatar_middle_thumbnall.split("/");
                           old_user_photo = temp_arr[temp_arr.length - 1];
                       } else {
                           old_user_photo = "";
                       }
                   }
                   //$('.layui-layer-close').hide();
               });

           });

           $('#update_photo').fileupload({
               url: '/user/student/avatar/upload/',
               dataType: 'json',
               autoUpload: true,
               done: function (e, data) {
                   if(data.result.status=="success"){
                       aboutPhoto.showPhoto("/uploads/temp/"+data.result.filename);
                       $('#update_photo_hidden').val(data.result.filename);
                   }else if(data.result.status=="failure"){
                       $(".avatar-error").html(data.result.message).show();
                   }else{
                       $(".avatar-error").html('未知错误').show();
                   }
               },
               progressall: function (e, data) {
                   var progress = parseInt(data.loaded / data.total * 100, 10);
                   $('#avatar-upload-progress').html(progress + '%').show();
               }
           }).prop('disabled', !$.support.fileInput)
                   .parent().addClass($.support.fileInput ? undefined : 'disabled');

       });

function user_profile_form_submit(){
                //提交前先设置图片裁切的参数
                $("#zoompicwidth").val(parseInt(aboutPhoto.imageInfo.imgWidth));
                $("#zoompicheight").val(parseInt(aboutPhoto.imageInfo.imgHeight));
                $("#marginTop").val(parseInt(Math.abs(aboutPhoto.imageInfo.marginTop)));
                $("#marginLeft").val(parseInt(Math.abs(aboutPhoto.imageInfo.marginLeft)));
                $("#boxwidth").val(parseInt(aboutPhoto.imageInfo.boxWidth));
                $("#boxheight").val(parseInt(aboutPhoto.imageInfo.boxHeight));

                var query = $('#user_profile').serializeArray();
                if (!query[0].value) {
                    query[0].value = old_user_photo;
                }
                $.ajax({
                    cache: false,
                    type: "POST",
                    url:$('#user_profile').attr('action'),
                    //data:$('#user_profile').serialize(),
                    data:query,
                    async: true,
                    beforeSend:function(XMLHttpRequest){
                        $("#user_profile_submit").html("提交中...");
                        $("#user_profile_submit").attr("disabled","disabled");
                    },
                    success: function(data) {
                        if(data.avatar){
                            $(".avatar-error").html(data.avatar).show(500).delay(1000).fadeOut(500);
                        }else if(data.real_name){
                            $(".name-error").html(data.real_name).show(500).delay(1000).fadeOut(500);
                            $("#real_name").focus();
                        }else if(data.study_goal){
                            $(".target-error").html(data.study_goal).show(500).delay(1000).fadeOut(500);
                            $("#study_goal").focus();
                        }else if(data.description){
                            $(".info-error").html(data.description).show(500).delay(1000).fadeOut(500);
                            $("#description").focus();
                        }else{
                            if(data.status == "success"){
                                $("#submit-tips").attr('class','tips-error bg-success').html("资料修改成功，2秒后自动跳转")
                                        .show(500).delay(1500).fadeOut(500, function(){
                                           window.location.replace(location.href);
                                            if(detect_ie() !== false) {
                                                window.location.reload();
                                            }
                                            return;
                                        });
                            }else if(data.status == "failure"){
                                $("#submit-tips").html("更新个人资料失败，请稍后重试！").show(500);
                            }
                        }
                    },
                    complete: function(XMLHttpRequest){
                        $("#user_profile_submit").html("提交");
                        $("#user_profile_submit").removeAttr("disabled");
                    }
                });
            }