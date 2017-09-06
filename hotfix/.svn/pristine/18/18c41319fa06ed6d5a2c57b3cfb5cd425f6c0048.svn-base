$(function(){

    //获取职业课程和阶段信息
    var curcareercourseId = $('#j-curcareercourseId').val();
    var curstageId = $('#j-curstageId').val();
    var studentId = $('#j-studentid').val();


    loadStageCourse(curcareercourseId, curstageId, studentId);

    //绑定阶段切换事件
    $(document).delegate('.j_tostage', 'click', function(){

        var toStage = $(this).attr("data-stage");


        $.ajax({
            url:'/lps2/stage/'+curcareercourseId+'/'+toStage+'/'+studentId+'/',
            dataType: 'json',
            success: function(data){
                    console.log("yes");
                if(data.status == 'success'){

                    var html = template('jtpl-stage', data);

                    $('#desc_box').html(html);
                    $('#j-curstageId').val(data.cur_stage.id);
                    $('.j-course-group').html('<div style="text-align:center;margin-top:10px;"><img src="/static/images/loading.gif"></div>');

                    loadStageCourse(curcareercourseId, data.cur_stage.id, studentId);
                }
            }
        });
    })

});
function addSctipt(src){
	var script=document.createElement("script");
	script.setAttribute("type", "text/javascript");
	script.setAttribute("src", src);
	var heads = document.getElementsByTagName("head");
	if(heads.length)
		heads[0].appendChild(script);
	else
		document.documentElement.appendChild(script);
}

function loadStageCourse(curcareercourseId, curstageId, studentId){
    //获取数据
    $.ajax({
        url: '/lps2/course/stage/'+curcareercourseId+'/'+curstageId+'/'+studentId+'/',
        dataType: 'json',
        success: function(data){
            var isunlock = $('#j-curisunlock').val();

            if(isunlock == 'True'){
                data.cur_careercourse.is_unlock = true
            }else{
                data.cur_careercourse.is_unlock = false
            }

            /*
            //加载数据前的准备
            for(var i=0;i<data.cur_stage_course_list.length;i++){

                var str = data.cur_stage_course_list[i].project.description;
                str = str.replace(/</g,'&#60;');
                str = str.replace(/>/g,'&#62;');
                str = str.replace(/&/g,'&#38;');
                data.cur_stage_course_list[i].project.description = str;
            }
            */
            template.config("escape", false);

            //加载模版
            var html = template('jtpl-course-gourp', data);

            $('.j-course-group').html(html);

            var dialogHtml = template('jtpl-dialog', data);

            $('body').append(dialogHtml);

            //加载页面后处理
            $('.course_result_text_button2').unbind('click').click(function(){
                var _course_id = $(this).parent().parent().attr("course_id");
                close_onlinetest('#course_'+_course_id+'_testModal');
            })

             $('.course_result_text_button1').each(function(index, button){
                 check_error(this, index, button);
             });

            // 是否弹出项目框
            var courseId = $('#j-courseId').val();
            if(courseId){
                var obj = new Object();
                obj.id = 'xmzz_'+courseId;
                open_popup(obj);
            }
            addSctipt('http://v3.jiathis.com/code/jia.js?uid=1680508');
        }
    });
}
//zhouyi 8-12
function zy_jia_config(tit,con){
    jiathis_config={
        data_track_clickback:true,
        url:"http://www.maiziedu.com/course/",
        summary:con,
        title:tit,
        shortUrl:false,
        hideMore:true,
        pic:""
    }
}