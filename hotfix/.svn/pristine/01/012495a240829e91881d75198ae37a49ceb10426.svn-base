$(function(){
    var imgpop = $('#project-module-image-list li');

    imgpop.live('click',function(event){
        event.stopPropagation();
        event.preventDefault();
        
        imgPopup();
    });

    $('#project-submit').on('click',function(){
        var oModule1 = $('.project-module');
        var oModule2 = $('.project-submit-module');
        var oContainer = $('.project-container');
        oContainer.stop().animate({'left':-oModule1.outerWidth() + 'px'},function(){
            var oStep = $('#return-step');
            oStep.on('click',function(){
                oContainer.stop().animate({
                    'left':'0px'
                }).children('.project-module').stop().animate({'opacity':'1','filter':'alpha(opacity=0)'});
            })
        }).children('.project-module').stop().animate({'opacity':'0','filter':'alpha(opacity=0)'});
    });






    // $('#project-reset-file').fileupload({
    //     dropZone:null,
    //     url: '',
    //     //formData:{'course_id':{{ course.id }}},
    //     add:function(e,data){
    //       var uploadErrors = [];
    //       var acceptFileTypes = /^(zip|rar)$/i;
    //       var filesize = data.originalFiles[0]['size']/(1024)/(1024);
    //       Ntype = data.originalFiles[0]['name'];
    //       Ntype = Ntype.substring(Ntype.length-3,Ntype.length);
    //       if(!acceptFileTypes.test(Ntype)){
    //           layer.msg('文件格式不正确（zip，rar）');
    //           uploadErrors.push('Not an accepted file type');
    //       }
    //       if(parseInt(filesize)>10) {
    //          layer.msg('文件超过10M大小');
    //           uploadErrors.push('Filesize is too big');
    //       }
    //       if(uploadErrors.length==0){
    //         data.submit();
    //       }
    //     },
    //     dataType: 'json',
    //     autoUpload: true,
    //     done: function (e, data) {
    //         $('.project-reset-file >span').html('重新上传');
    //     }
    // });

    //项目截图上传
    // $('#uploadPreview').fileupload({
    //     dropZone:null,
    //     url: '',
    //     //formData:{'course_id':{{ course.id }}},
    //     add:function(e,data){
    //       var uploadErrors = [];
    //       var acceptFileTypes = /^(jpe?g|png)$/i;
    //       var filesize = data.originalFiles[0]['size']/(500)/(500);
    //       Ntype = data.originalFiles[0]['name'];
    //       Ntype = Ntype.substring(Ntype.length-3,Ntype.length);
    //       if(!acceptFileTypes.test(Ntype)){
    //           layer.msg('文件格式不正确（jpg，png）');
    //           uploadErrors.push('Not an accepted file type');
    //       }
    //       if(parseInt(filesize)>10) {
    //          layer.msg('文件超过500k大小');
    //           uploadErrors.push('Filesize is too big');
    //       }
    //       if(uploadErrors.length==0){
    //         data.submit();
    //       }
    //     },
    //     dataType: 'json',
    //     autoUpload: true,
    //     done: function (e, data) {
    //         //alert($('#project-reset-file').val().replace(/.*(\/|\\)/, ""));
    //     }
    // });


    $('#project-reset-file').change(function(){
        if($(this).val().length>0){
            var fileExt = (/[.]/.exec($(this).val())) ? /[^.]+$/.exec($(this).val().toLowerCase()) : '';
            if(fileExt != 'zip' && fileExt != 'rar'){
                layer.msg('文件格式不正确（例如：zip，rar）');
                return false;
            }else{
                $('.project-submit-attachment').html($(this).val().replace(/.*(\/|\\)/, ""));
                $('.project-reset-file').find('span').text('重新上传');
                ajaxFileUpload('project-reset-file');
            }
        }
    });

    $('#uploadPreview').change(function(){
        if($(this).val().length>0){
            var fileExt = (/[.]/.exec($(this).val())) ? /[^.]+$/.exec($(this).val().toLowerCase()) : '';
            if(fileExt != 'jpg' && fileExt != 'png'){
                layer.msg('文件格式不正确（例如：.jpg，.png）');
                return false;
            }else{
                ajaxFileUpload('uploadPreview');
            }
        }
    });

    function ajaxFileUpload(id) {
        $.ajaxFileUpload
        (
            {
                url: 'data.html', //用于文件上传的服务器端请求地址
                secureuri: false, //是否需要安全协议，一般设置为false
                fileElementId: id, //文件上传域的ID
                dataType: 'JSON', //返回值类型 一般设置为json
                success: function (data, status)  //服务器成功响应处理函数
                {

                },
                error: function (data, status, e)//服务器响应失败处理函数
                {
                    alert(e);
                }
            }
        )
        //return false;
    }

});

var getLength = function(str){
   return String(str).replace(/[^\x00-\xff]/g,'aa').length; 
}

var imgPopup = function(){
    var html = '';

    html += '<div id="imgzoom"><i class="imgzoom-close"></i><div id="imgzoom-image-ctn">';
    html += '<img src="'+ $(this).find('img').attr('src') +'">';
    html += '</div></div>';

    $(document.body).append(html);

    $('#imgzoom').fadeIn('fast','linear');

    $('.imgzoom-close').on('click',function(event){
        $('#imgzoom').remove();
    });
};