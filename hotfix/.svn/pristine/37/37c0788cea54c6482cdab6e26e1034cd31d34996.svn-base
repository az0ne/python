/**
 * Created by Administrator on 2016/12/10.
 */

// <给项目评分按钮>单击事件
$('.grade_btn').off('click').on('click', function () {
    $(this).addClass('on');
    $('.grade_float').removeClass('_hide').addClass('_show');
});
// <修改评分按钮>单击事件
$('.change_btn').off('click').on('click', function () {
    $(this).addClass('xg_on');
    $('.grade_float').removeClass('_hide').addClass('_show');
});
// 选取评分类型
$('.grade_level>li').off('click').on('click', function () {
    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
    } else {
        $(this).addClass('selected').siblings().removeClass('selected');
    }
});
// 关闭评分弹窗
$('._close').off('click').on('click', function () {
    $('.grade_float').removeClass('_show').addClass('_hide');
});
// <确定评分按钮>单击事件
$('.sure_grade_btn').off('click').on('click', function (event) {
    var img_src = $('.grade_level>.selected>img').attr('src');
    var img_src = img_src ? img_src : "";
    var grade_level = $('.grade_level>.selected>img').attr('name');
    $('.grade_float').removeClass('_show').addClass('_hide');
    $.ajax({
        url: '/lps4/grade_coach_project/',
        type: 'POST',
        data: { 'class_id': classId,
                'score': grade_level,
                'stage_task_id': stageTaskId,
                'student_id': studentId
        },
        success: function(data){
            if(data.success){
                if (img_src != "") {
                    $('.grade>img').attr('src', img_src);
                    $('.grade>.grade_btn').hide();
                    $('.grade>.change_btn').hide();
                    $('.grade>.comment').show();
                    switch (grade_level) {
                        case 'S':
                            $('.grade>.comment').html('超出预期的完成了作业');
                            break;
                        case 'A':
                            $('.grade>.comment').html('出色的完成了作业');
                            break;
                        case 'B':
                            $('.grade>.comment').html('完成了作业主要考核点，但仍有些许瑕疵');
                            break;
                        case 'C':
                            $('.grade>.comment').html('完成了作业但并无出彩之处');
                            break;
                        case 'D':
                            $('.grade>.comment').html('学生的作业没有达到要求');
                            $('.grade>.change_btn').css('display', 'inline-block');
                            break;
                    }
                } else {
                    $('.grade>img').attr('src', '/images/lps4/project_making/waiting.png');
                    $('.grade>.change_btn').hide();
                    $('.grade>.grade_btn').show();
                }
                $('.grade_btn').removeClass('on');
            }else{
                layer.alert(data.message, {
                    skin: 'layui-layer-molv',
                    closeBtn: 0
                });
            }
        }
    });
    event.stopPropagation();
});