// $(window).load(function(){
//     $('.preloader').delay(500) .fadeOut("slow", function (){
//         createItems();
//         //新手引导
//         if (user_is_already_guided == 'False') {
//             setTimeout(function(){
//                 guidebox();
//             }, 300)
//         }
//     });
// });
$(function(){
    createItems();
    //新手引导
    if (user_is_already_guided == 'False') {        
        if(get_cookie("access") == ""){
            guidebox();
            set_cookie("access", uid_gen(), 1024);
        }        
    }

    $('.need-sign-in').on('click', function ( ) {
        login_popup();
        return false
    });
    if (student_info == 'False') {
        // 完善学习信息
        perfectInfo();
    } else if (is_view_contract == 'False') {
        // 入学须知
        agreement($('#myAgreement2'));
    } else if (is_job_intention_info == 'True') {
        // 完善就业信息
        jobIntentionInfo();
    } else if (is_view_employment_contract == 'True') {
        // 就业协议
        agreement($('#myAgreement'));
    } else if (is_view_not_employment_contract == 'True') {
        // 服务承诺
        agreement($('#myAgreement3'));
    } else if (is_employment_contract == 'True' && is_pop_complete_resume == 'True') {
        //完善我的简历
        perfectMyResume();
    }

    // 任务成绩消息
    if(student_info == 'True' && class_type != '2'){
        task_score_message(student_id);
    };

    // 视频介绍
    videoIntroduce();
    // 讲师切换
    majorTeacher();
    // 1v1直播预约
    appointment();

    // 立即购买
    goBuy();

    showStageLists();

    // 往期录课
    livePrev();

    //约课--立即进入
    immediately_enter();

    window.onresize = function(){
        createItems();
    }

    $('.sign-in, .default-user-icon').on('click', function(){
        login_popup();
    });

    $('#left-nav li').not(".LPS").find('a').on('click', function(){
        if(isLogin == 'False'){
            login_popup();
            return false;
        }
    });
    $('.one-to-one a').on('click', function(){
        if(isLogin != 'False'){
            if(isStudent == 'True'){
                if(class_type == '2'){
                    ovoService();
                    return false;
                }
            }else{
                return false;
            }
        }
    });
    $('.answers a').on('click', function(){
        if(isLogin != 'False'){
            if(isStudent == 'True'){
                if(class_type == '2'){
                    ovoService();
                    return false;
                }
            }else{
                return false;
            }
        }
    });

    // 学生作品展示
    $(".student-work").slide({
        titCell:".slide-tab",
        mainCell:".slide-box ul",
        autoPage:true,
        effect:"leftLoop",
        autoPlay:true,
        trigger:"click"
    });

    // 相关文章展示
    $(".relate-article").slide({
        titCell:".slide-tab",
        mainCell:".slide-box ul",
        autoPage:true,
        effect:"leftLoop",
        autoPlay:true,
        trigger:"click"
    });

    $('.adviser').unbind().click(function(){
        $("#KFLOGO .Lelem").eq(0).trigger("click");
    });

    //模块弹出
    $(".feedbackfade").click(function(){
        $("#feedbakBox").modal('show');
    });
    //隐藏模块
    $("#feedbakBox .zy_close").click(function(){
        $(this).parents("#feedbakBox").modal('hide');
    });
    //如果url里有stagetask_id,则trigger出任务详情
    var _s = window.location.search.split(/\W/, 3);
    if(_s[1] == 'stagetask_id' && _s[2]){
        $('#' + _s[2]).trigger('click');
    }
});
function uploadFile(options,callback){
    var big_image_url='';
    var option = options;

    if($(option.picUpload).length > 0){
        $(option.picUpload).fileupload({
            url:"/lps4/onevone/avatar/upload/",
            dataType: 'json',
            autoUpload: true,
            add: function (e, data) {
                var uploadErrors = [];
                var acceptFileTypes = /^(png|jpg|jpeg)$/i;
                var filesize = data.originalFiles[0]['size']/(1024);

                Ntype = data.originalFiles[0]['name'].split('.');
                Ntype = Ntype[Ntype.length - 1];

                if (!acceptFileTypes.test(Ntype)) {
                    files.removeClass('pic');
                    uploadErrors.push('Not an accepted file type');
                }
                if(uploadErrors.length==0){
                    data.submit();
                }
            },
            done: function (e, data) {
                data = data.result;
                if(data.success){
                    var img_url = data.data.small_result.img_url;
                    big_image_url = data.data.result.img_url;
                    $(option.qrurl).val(img_url);
                    $(option.file).addClass('pic');
                    $(option.file).find('img').attr("src",img_url);
                }
            }
        });
    }
    $(option.textarea).keyup(function(){
        if($(this).val().length > 14){
            $(option.btns).removeClass('disabled').removeAttr('disabled');
        }else{
            $(option.btns).addClass('disabled').attr('disabled','disabled');
        }
    });
    $(option.btns).on('click',function(){
        $.ajax({
            type: "POST",
            url: "/lps4/update_onevone_meeting/"+$(option.meeting_id).attr('meeting_id')+"/",
            data: {
                "small_image_url": $(option.qrurl).val(),
                "image_url": big_image_url,
                "question": $(option.textarea).val()
            },
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    callback();
                } else {
                  console.error(data.message)
                }
            }
        });
    });
}
function videoIntroduce(){
    //视频介绍
    $seeVideo = $('.see-video');
    $seeVideo.on('click', function(){
        var mask = $('<div class="modal-mask"></div>');
        var dialog = $('<div class="dialog"><video id="video_introduce" autoplay preload="none" width="100%" height="100%" src="'+ $(this).attr('data-href') +'"></video><a class="off" href="javascript: void(null);"></a></div>');

        $('body').append(mask);
        $('body').append(dialog);
        AnimateFun(dialog);

        $('.off').on('click', function(){
            $(mask).remove();
            $(dialog).remove();
        });

        $(window).on('resize scroll',function(){
            AnimateFun(dialog);
        });
    });
};

function AnimateFun(obj){
    obj.css('left' , ($(window).width() - obj.outerWidth())/2 );
    obj.stop().animate({'top' : ($(window).height() - obj.outerHeight())/2 + $(window).scrollTop()}, 300);
};

function majorTeacher(){
    var $majorNav = $('.major-nav li');
    $majorNav.click(function(){
        $(this).addClass('active').siblings().removeClass('active');
        var index = $majorNav.index(this);
        $('.major-box > div').eq(index).show().siblings().hide();
    });
};

var _taskIndex = 1;
var _taskArray = [];
var _arrayPostion = [];
var _taskPostion = [];

var _windowWidth = 0;
var _taskWidth = 174;
var _taskHeight = 175;
var _colCount = 0;
var _stageCount = 0;
var _stageIndex = 0;
var _speed = 40;
function createItems(){
    _taskPostion = [];
    _windowWidth = $(window).width() - 110 - 283 - 60 - 43;
    _colCount = parseInt(_windowWidth / _taskWidth);
    _stageCount = $('.lists').length;
    _stageIndex = 0;
    for(var i = 0;i <_stageCount; i++){
         setDivSize($('.lists')[i]);
    }
    countProcess();
    createStage(_taskWidth,_taskHeight,_colCount,$('.lists')[_stageIndex]);
};

function getTaskPosition(id){
    for(var i = 0; i < _taskPostion.length; ++i){
        if(_taskPostion[i].id == id){
            return _taskPostion[i];
        }
    }
    return null;
};

// function paddingLeft(num,length)
// {
//     var tmp = num.toString();
//     if(tmp.length >= length)
//     {
//         return tmp;
//     }

//     for(var i = 0; i < length - tmp.length; ++i)
//     {
//         tmp = "0" + tmp;
//     }
//     return tmp;
// }

function countLeftDay(seconds){
    // var leftDays = "";
    // if (seconds < (3600 * 24))
    // {
    //     leftDays = 1;
    // }
    // else if()
    // {
    //     leftDays = seconds / (3600 * 24)  + 1;
    // }

    return parseInt(seconds / (3600 * 24))  + 1;
}

function countProcess(){
    var nextStart = [0];
    for(var i = 0; i < _stageCount; ++i){
        var count = 0;
        var stage = $('.lists')[i]
        var taskArray = getTaskArray(stage);
        for(var j = 0; j < taskArray.length; ++j){
            if( $(taskArray[j]).attr("class") == "finish"){
                count = count + 1;
            }
        }

        var rowCount = countRowCount(stage);
        var div = $(stage).parent();
        var height = rowCount * _taskHeight + 60;
        var point = $(div).parent().parent().find(".study-stage-progress");


        var process = $(div).parent().parent().find(".progress-on");
        if(count == taskArray.length){
            process.css({"height": height + "px"});
            nextStart.push(i + 1);
        }else{
            process.css({"height": height * (count / taskArray.length) + "px"});
        }

        for(var k = 0; k < nextStart.length; ++k){
            if (i == nextStart[k]){
                point.addClass("complete");
            }
        }
    }
}

function taskHoveIn(){

    var id = $(this).attr("id");
    var position = getTaskPosition(id);
    var tipPostion = {"left":0, "top": position.top};

    var tips = $(this).find('p');

    var leftTime = 0;
    var msg = "";
    if (tips.attr('left-time') != null && tips.attr('left-time') != ""){
        leftTime = parseInt(tips.attr('left-time'));
        leftTime = countLeftDay(leftTime);
        msg = "倒计时:" + leftTime + "天";
    }else{
        msg = "";
    }

    var _divHoverTips = $('<div class="hover-tips"><h4>' + tips.text() + '</h4><p>'+ ((tips.attr('attr-b') == '') ? '' : '<span class="first">' + tips.attr('attr-b') + '</span>') +'<span class="two">'+ msg +'</span></p>' + '</div>');
    $(this).parent().parent().append(_divHoverTips);

    switch(tips.attr('color-a')){
        case 'orange':
        $(".hover-tips").addClass('orange');
        break;
        case 'green':
        $(".hover-tips").addClass('green');
        break;
        case 'red':
        $(".hover-tips").addClass('green');
        break;
    };
    if(position.tipDirect == "left"){
        tipPostion.left = position.left - _taskWidth;
        $(".hover-tips").removeClass('left-arrow');
    }else{
        tipPostion.left = position.left + _taskWidth;
        $(".hover-tips").addClass('left-arrow');
    }

    $(".hover-tips").css({"left": tipPostion.left + "px", "top": tipPostion.top + "px"});
    $(".hover-tips").show();
};

function taskHoveOut(){
    $(".hover-tips").remove();
};

function getTaskArray(stage){
    var taskArray = [];
    taskArray = $(stage).find('li');
    return taskArray;
};

function countRowCount(stage){
    _taskArray = getTaskArray(stage);
    var taskCount = _taskArray.length;
    var rowCount = 0;

    if(taskCount % _colCount == 0){
        rowCount = parseInt(taskCount/_colCount);
    }else{
        rowCount = parseInt(taskCount / _colCount) + 1;
    }
    return rowCount;
};

function setDivSize(stage){
    var rowCount = countRowCount(stage);
    var div = $(stage).parent();
    var height = rowCount * _taskHeight;
    var width = _colCount * _taskWidth;
    $(div).css({"height": height + "px" , "width": width + "px"});
    $(div).parent().css({"height": height + 60 + "px" , "width": width + "px"});
    $(div).parent().parent().find(".study-stage-progress").css({"height": (height + 60) + "px"});
};

function createStage(_taskWidth,_taskHeight,_colCount,stage){
    var rowCount = countRowCount(stage);
    var taskCount = _taskArray.length;
    _arrayPostion = [];
    for (var i = 0; i < rowCount; i++){
        for (var j = 0; j < _colCount; j++){

            if((i * _colCount) + j == taskCount){
                break;
            }

            task = _taskArray[(i * _colCount) + j];
            var top = i * _taskHeight;
            var left = 0;

            var tipDirect = "left";
            if(i % 2 == 0){
                //left
                left = j * _taskWidth;
                if(j == _colCount - 1){
                    $(task).children('div').removeClass().addClass('add-arrow-b');
                }else{
                    $(task).children('div').removeClass().addClass('add-arrow-r');
                }

                if(j == 0){
                    //判断是不是每列的第一个
                    tipDirect = "right";
                }else{
                    tipDirect = "left";
                }

            }else{
                //right
                left = (_colCount - 1 - j) * _taskWidth;
                if(j == _colCount - 1){
                    $(task).children('div').removeClass().addClass('add-arrow-b');
                }else{
                    $(task).children('div').removeClass().addClass('add-arrow-l');
                }

                if(j == _colCount - 1){
                    //判断是不是每列的第一个
                    tipDirect = "right";
                }else{
                    tipDirect = "left";
                }
            }

            if((i * _colCount) + j == taskCount - 1){
                $(task).children('div').removeClass();
            }
            _arrayPostion.push({"top":top + 'px',"left":left + 'px'});
            _taskPostion.push({"id": $(task).attr("id") ,"top":top,"left":left, "tipDirect" : tipDirect});
        }
    }

    for(var i = 0 ; i < taskCount; ++i){
         $(_taskArray[i]).unbind("mouseover").unbind("mouseout");
         $(_taskArray[i]).bind({mouseover:taskHoveIn,mouseout:taskHoveOut});
    }

    $(_taskArray[0]).css(_arrayPostion[0]);
    for(var i = 1; i < _taskArray.length;++i){
        $(_taskArray[i]).hide();
        $(_taskArray[i]).css(_arrayPostion[i]);
    }

    if(taskCount == 1)
    {
        _stageIndex = _stageIndex + 1;
        if(_stageIndex  < _stageCount){
            createStage(_taskWidth,_taskHeight,_colCount,$('.lists')[_stageIndex]);
        }
    }
    else
    {
        _taskIndex = 1;
        $(_taskArray[_taskIndex]).show();
        $(_taskArray[_taskIndex]).animate(_arrayPostion[_taskIndex],_speed,move);
    }
};

function move(){
    _taskIndex = _taskIndex + 1;
    if (_taskIndex < _taskArray.length){
        $(_taskArray[_taskIndex]).css(_arrayPostion[_taskIndex-1]);
        $(_taskArray[_taskIndex]).show();
        $(_taskArray[_taskIndex]).animate(_arrayPostion[_taskIndex],_speed,move);

    }else{
        _stageIndex = _stageIndex + 1;
        if(_stageIndex  < _stageCount){
            createStage(_taskWidth,_taskHeight,_colCount,$('.lists')[_stageIndex]);
        }
    }
};
/*
 * @ 预约成功函数
 */
function appointmentSuccess(){
    var meeting_id = $('.live-appointment').attr('meeting_id');
    $.ajax({
    type: "GET",
    url: "/lps4/onevone_meeting_success/"+meeting_id+"/",
    dataType: "json",
    success: function(data){
        if (data.success) {
            $('#appointment-success .modal-content').html(data.data.html)
            pop_div();
        } else {
            alert('直播预约的成功信息获取失败')
        }
    },
    error: function(data){
        console.log(data);
    }
    });

    function pop_div(){
        $('#appointment-success .close, #appointment-success #know').on('click',function(){
            $('#appointment-success').modal('hide');
            window.location.reload();
        });
        $('#appointment-success #join').on('click',function(){
            $('#appointment-success').modal('hide');
            joinMeeting(meeting_id);
        });
        $('#appointment-success').modal({show:true, keyboard:false,backdrop: 'static'});
    }

}
/*
 * @ 预约失败函数
 */
function appointmentFail(){
    $('#appointment-fail .close').on('click',function(){
         $('#appointment-fail').modal('hide');
    });
    $('#appointment-fail').modal({show:true, keyboard:false,backdrop: 'static'});
}
/*
 * @ 预约最后一步
 */
function appointmentStep(){
    $('#appointment-step').modal({show:true, keyboard:false,backdrop: 'static'});
    $('.close').on('click', function(){
        $('#appointment-step').modal('hide');
    })
    // 预约最后一步 图片上传
    uploadFile({
        'file' : "#appointment-step .file",
        'picUpload' : '#picUpload2',
        'btns' : "#appointment-step .submitBtn",
        'textarea' : "#appointment-step textarea",
        'qrurl' : "#appointment-step .QRurl",
        'meeting_id' : ".live-appointment"
    },appointmentSuccess);
}
/*
 * @ 预约函数
 */
function appointment(){
    var appointmentBtn1 = $('.fake_ovo_meeting'),
        $meeting_id = $('.live-appointment').attr('meeting_id'),
        $appointment = $('#appointment'),
        $confirmUse = $('.confirm-use'),
        $phoneNum = $('#phone-num'),
        $verification = $('#verification'),
        $sendVerif = $('.send-verif'),
        $close = $appointment.find('.close'),
        telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/,
        tipsMsg,
        myFn1;

    appointmentBtn1.on('click', myFn1 = function() {
        $(this).unbind('click', myFn1);
        if (isLogin == 'False') {
            login_popup();
        } else if ($(this).attr("need_pay")) {
            openService();

        } else {
            $appointment.modal({show: true, keyboard: false, backdrop: 'static'});
        }
        (function(that){
            setTimeout(function(){
                $(that).bind('click', myFn1);
            }, 2000);
        })($(this));
    });
    $close.on('click', function(){
        $appointment.modal('hide');
    });
    $confirmUse.on('click', function(){
        if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if(!telReg.test($phoneNum.val())){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else if($verification.val() == '' || null){
            tipsMsg = '手机验证码输入错误，请重试';
            Tips($verification, tipsMsg);
        }else{
            verifyCaptcha();
        }
    });
    $sendVerif.on('click', function(){
        if($phoneNum.val() == '' || null){
            tipsMsg = '请输入正确的手机号';
            Tips($phoneNum, tipsMsg);
        }else{
            if(telReg.test($phoneNum.val())){
                sendsms();
            }else if(!telReg.test($phoneNum.val())){
                tipsMsg = '请输入正确的手机号';
                Tips($phoneNum, tipsMsg);
            }
        }
    });

    function sendsms() {
        $.ajax({
            type: "POST",
            url: "/lps4/mobile/sendsms/",
            data: {
                "mobile": $("#phone-num").val(),
                "meeting_id":$meeting_id
            },
            dataType: "json",
            success: backData,
            error: function(data){
                console.log(data);
            }
        });
    };

    function backData(data) {
        if (!data.success) {
            if (data.data.type){
                appointmentFail();
            }
            else {
                tipsMsg = data.message;
                Tips($phoneNum, tipsMsg);
            }
        } else {
            Cuttime($sendVerif, 60);
        }
    };

    function Cuttime(obj, time){
        var countdown = null;
        obj.addClass("send").val("重新发送(60s)").attr('disabled', 'disabled');
        countdown = setInterval(function(){
            time--;
            obj.val("重新发送("+time+"s)");
            if(time <= 0){
                clearInterval(countdown);
                obj.removeClass("send").val("重新发送").removeAttr('disabled');
            }
        },1000);
    };
    function verifyCaptcha() {
        $.ajax({
            type: "POST",
            url: "/lps4/order_onevone_meeting/",
            data: {
                "mobile": $("#phone-num").val(),
                "mobile_code": $("#verification").val(),
                "career_id":career_id,
                "meeting_id":$meeting_id

            },
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    appointmentStep();
                } else {
                    if (data.data.type){
                        appointmentFail();
                    }
                    else {
                        tipsMsg = data.message;
                        Tips($verification, tipsMsg);
                    }
                }
            },
        });
    };
};
//加入1v1 直播函数
function joinMeeting(meeting_id){
    $.ajax({
    type: "GET",
    url: "/lps4/onevone_meeting_join_info/"+meeting_id+"/",
    dataType: "json",
    success: function(data){
        if (data.success) {
            $('#live-ready .web a').attr('href',data.data.web_join_url);
            $('#live-ready .client a').attr('href',data.data.join_url);
            popupMsg($('#live-ready'));

        } else {
            alert('直播预约的成功信息获取失败')
        }
    },
    error: function(data){
        console.log(data);
    }
    });
}
/**
 * 立即进入
 * @ clicktag判断是否1秒内多次点击
 */
function immediately_enter(){
    var clicktag = 0;
    $('.appointment-btn-3').on('click', function () {
        if (clicktag == 0) {
            clicktag = 1;
            joinMeeting($(this).attr('id'));
            setTimeout(function () { clicktag = 0 }, 1000);
        }
    });
}

/*
 * @ 报名函数
 */
function enroll(){
    var $close = $('.close');
    $('#enroll').modal({show:true, keyboard:false,backdrop: 'static'});
    tab({
        tabNav: '#enroll .tab-nav li',
        tabBox: '#enroll .tab-box li',
        select: 'select'
    });
    // 根据点标签的不同，把index加到跳转链接里
    var goBuy = $('#enroll .go-buy').attr('href');
    var $enroll = $('#enroll .tab-nav li');
    $enroll.click(function(){
        $(this).addClass('select').siblings().removeClass('select');
        var index = $enroll.index(this);
        $('#enroll .tab-box li').eq(index).show().siblings().hide();
        $('#enroll .go-buy').attr('href', goBuy + '&index=' + index)
    });

    $close.on('click', function(){
        $('#enroll').modal('hide');
    });
}
/*
 * @ 立即购买
 */
function goBuy(){
    var goBuy = $('.ad .go-buy');
    goBuy.on('click', function(){
        if(isLogin == 'False'){
            login_popup();
        }else{
            enroll();
        }
        return false;
    })
}
/*
 * @ 显示任务列表函数
 */
function showStageLists(){
    var stageLi = $('.study-stage-ball .lists li'),
        studyStageBox = $('.right-fixed-box'),
        stageTitle = $('.stage-title'),
        goBack = $('.stage-top'),
        mask = $('<div class="modal-mask"></div>');

    stageLi.each(function(i){
        $(stageLi[i]).on('click',function(){
            var class_attr = $(this).attr('class');
            var h4_text = $(this).find('p').text();
            var p_text = $(this).find('p').attr('desc');
            var right_text = $(this).find('p').attr('attr-b');
            var task_type = $(this).find('p').attr('task_type');
            var stagetask_id = $(this).attr('id');
            var stage_box = studyStageBox.find('.stage-box');

            $.ajax({
                url: '/lps4/' + class_id + '_' + stagetask_id + '/',
                type: 'POST',
                data: {'status': class_attr.split(' ')[0], 'class_type': class_type, 'task_type': task_type},
                success: function (data) {
                    if ($.parseJSON(data)['status']=='success') {

                        stageTitle.find('.left').attr('class', 'left ' + class_attr);
                        stageTitle.find('h4').text(h4_text);
                        stageTitle.find('p').text(p_text);
                        stageTitle.find('.right').text(right_text);
                        studyStageBox.find('.stage-box').remove();
                        stageTitle.after(stage_box);
                        $('.stage-box').height($(window).height() - 246);
                        $('.stage-box').html($.parseJSON(data)['html']);

                        $('body').append(mask);
                        $('.modal-mask').fadeIn(250, function(){
                            studyStageBox.stop().animate({
                                'right': '0px'
                            },250);
                            $('html,body').css({'height':'100%','overflow':'hidden'});
                        });

                        showTaskLists();
                        $('.stage-box').jScrollPane({
                            mouseWheelSpeed: 100
                        });
                        $('.need-sign-in').on('click', function ( ) {
                            login_popup();
                            return false

                        });
                        $('.need_pay').on('click', function ( ) {
                            enroll();
                            return false
                        });
                        $('.lock_pop').on('click', function () {
                            popupMsg($('#popup-1'));
                            return false
                        });
                        $('.try_lock_pop').on('click', function () {
                            popupMsg($('#popup-4'));
                            return false
                        });
                        $('.current_pop ').on('click', function () {
                            popupMsg($('#popup-3'));
                            $('.know2').on('click', function () {
                                $.ajax({
                                    url: '/lps4/unlock/' + class_id + '_' + stagetask_id + '/',
                                    type: 'POST',
                                    data: {'class_type': class_type, 'career_id': career_id},
                                    success: function () {
                                        if ($.parseJSON(data)['status']=='success') {
                                            // 改变任务地图任务球的状态
                                            $('#' + stagetask_id).attr({'class': 'ongoing'}).find('p').attr({'attr-b': '正在学习（0%）'});
                                            // 改变任务详情任务球的状态
                                            stageTitle.find('.left').attr('class', 'left ongoing');
                                            stageTitle.find('.right').text('正在学习（0%）');
                                            // 去掉item的current_pop属性
                                            $('.current_pop').each(function(){
                                                var current_pop_attr = $(this).attr('class').replace('current_pop', '');
                                                $(this).attr('class', current_pop_attr).off('click');
                                            });
                                            // var current_pop_attr = $('.current_pop').attr('class').replace('current_pop', '');
                                            // // 取消current_pop事件
                                            // $('.current_pop').attr('class', current_pop_attr).off('click');
                                            $('.can_be_unlock_pop').on('click', function () {
                                                popupMsg($('#popup-2'));
                                                return false
                                            });
                                        } else {
                                            layer.alert('解锁失败', {
                                                skin: 'layui-layer-molv',
                                                closeBtn: 0
                                            });
                                        }
                                    },
                                    error: function () {
                                        layer.alert('网络出错', {
                                            skin: 'layui-layer-molv',
                                            closeBtn: 0
                                        });
                                    },
                                    complete: function () {
                                        $('#popup-3').modal('hide');
                                    }
                                })
                            });
                            return false
                        });
                        $('.can_be_unlock_pop').on('click', function () {
                            popupMsg($('#popup-2'));
                            return false
                        });

                    } else {
                        layer.alert('获取任务详情失败', {
                            skin: 'layui-layer-molv',
                            closeBtn: 0
                        });
                    }
                },
                error: function () {
                    layer.alert('网络出错', {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                }
            });

            maizi_trace.trace({
                "suid": maizi_trace.suid(),
                "action_id": "trace_lps4_trigger_taskball",
                "trace_pay_type": maizi_trace.pay_type(),
                "trace_user_type": maizi_trace.user_type(),
                "trace_career_name": maizi_trace.career_name(),
                "trace_taskball_name": $(this).attr("trace_task_name")
            });

        })
    });


    goBack.on({'click':function(){
        colseRightBox();
    }},'.go-back');

    /*
     * 点击空白处关闭抽屉
     */
    var $ele = $('.right-fixed-box, .modal, .guide');
    $ele.on("click",function(e){
        e.stopPropagation();//阻止冒泡
    });
    $(document).on('click',function(){
        colseRightBox();
    });

    /*
     * 关闭抽屉
     */
    function colseRightBox(){
        studyStageBox.stop().animate({
            'right': '-500px'
        },250);
        $('.modal-mask').remove();
        $('html,body').removeAttr('style');
    }
}

$('.continue').on('click', function () {
    var i = $(this).attr('rid');
    $('#' + i).trigger('click');
});

function showTaskLists(){
    var stageLists = $('.stage-lists > li'),
        subLists = $('.sub-lists'),
        index;
    stageLists.each(function(i){
        index = i;
        $(stageLists[index]).on({'click': function(e){
            $(this).parent().parent().toggleClass('open').children('.sub-lists').slideToggle(250);
            setTimeout(function(){
                $('.stage-box').jScrollPane({
                    mouseWheelSpeed: 100
                });
            },250)
        }}, 'i');
    });
}

//新手引导
function guidebox(){
    var ballTop,ballLeft,firstLi, w, h;
        if($('.guide').length > 0){
            $('html,body').animate({scrollTop:0},0).css("cssText","overflow:hidden!important");
            $('.guide').fadeIn();
            firstLi = $('.main-content .study-stage').eq(0).find('.study-stage-ball>ul>li:first-child');

            ballTop = firstLi.offset().top-$("body").scrollTop() + 15;
            ballLeft = firstLi.offset().left + 38;
            w = window.screen.width;
            h = $(window).height();

        $(".guide i").css({
            'left':0,
            'top':0,
            'borderWidth':(ballTop+12) + 'px' + ' '+ w + 'px' + ' '+ h + 'px' + ' '+ (ballLeft+11) + 'px'
        });
        $(".guide .step1").stop().animate({
            left:ballLeft,
            top:ballTop
        },200);

        $(".guide .step2").hide().css({
            left:ballLeft,
            top:ballTop
        });

         $(".guide .step1").on('click',function(){
             $(this).fadeOut(50);
             $('.guide i').css({
                 'borderWidth':(h-100) + 'px' + ' '+ w + 'px' + ' '+ h + 'px' + ' '+ 16 + 'px'
             });
             $(".guide .step2").fadeIn(80).animate({
                left:0,
                top:h-120,
            },80);
         });

        $(".guide .Ikonw").on('click',function(){
            $('html,body').removeAttr('style');
            $('.guide').fadeOut();
            $.ajax({
                url: '/lps4/update_is_already_guided/',
                type: 'GET'
            });

            maizi_trace.trace({
                "suid": maizi_trace.suid(),
                "action_id": "trace_lps4_finish_guide",
                "trace_career_name": maizi_trace.career_name()
           });

        });
    }
}

/*
 * @ 提示弹窗一
 */
function popupMsg(obj){
    obj.modal({show:true, keyboard:false,backdrop: 'static'});
    $('.close, .know').on('click', function(){
        obj.modal('hide');
    });
};

/*
 * @ 1v1 展示弹窗
 */
function livePrev(){
    var lessonPast = $('.lesson-past'),
        livePrev = $('.live-prev'),
        // liveBtn2 = $('.appointment-btn-2'),
        // liveBtn3 = $('.appointment-btn-3'),
        goBack = $('.stage-top'),
        context = $('.context-box'),
        mask = $('<div class="modal-mask"></div>');
        livePrev.on('click', function(){
            $('.context').html('');
            getOldMeetingList();
        });
        // liveBtn2.on('click', function(){
        //     var meeting_id = $('.live-appointment').attr('meeting_id');
        //     getOldMeeting(meeting_id);
        // });
        // liveBtn3.on('click', function(){
        //     var meeting_id = $('.live-appointment').attr('meeting_id');
        //     getOldMeeting(meeting_id);
        // });
    goBack.on({'click':function(){
       backMask();
    }},'.go-back');
    $(document).on('click', function(){
        backMask();
    });
    //获取往期直播列表
    function getOldMeetingList() {
        $.ajax({
            type: "GET",
            url: "/lps4/old_onevone_meeting_list/"+career_id+"/",
            dataType: "json",
            success: function(data){
                if (data.success) {
                    $('.context').html(data.data.html);
                    modalMask();
                } else {
                    layer.alert('往期直播列表获取失败', {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                }
            },
            error: function(data){
                console.log(data);
            },
            complete:function(){
                $('.context-box').height($(window).height() - 70);
                setTimeout(function(){
                    $('.context-box').jScrollPane({
                        mouseWheelSpeed: 100
                    });
                }, 250);
                lessonPast.find('.1v1info').each(function(i,v){
                    $(v).on('click',function(){
                        $('.context').html('');
                        backMask();
                        getOldMeeting($(this).attr('meeting_id'));
                    });
                });
            }
        });
    };
    //打开抽屉后续处理
    function modalMask(){
        $('body').append(mask);
        $('.modal-mask').fadeIn(250, function(){
            lessonPast.stop().animate({
                'right': '0px'
            }, 250);
            $('html,body').css({'height':'100%','overflow':'hidden'});
        });
    }
    //关闭抽屉后续处理
    function backMask(){
        lessonPast.stop().animate({
            'right': '-500px'
        },250).on('click', function(event){
            event.stopPropagation();
        });
        $('.modal-mask').remove();
        $('html,body').removeAttr('style');
    }
    //获取往期直播详情
    function getOldMeeting(meeting_id) {
        $.ajax({
            type: "GET",
            url: "/lps4/get_onevone_meeting/"+meeting_id+"/",
            dataType: "json",
            success: function(data){
                if (data.success) {
                    $('.context').html(data.data.html);
                    $('.card .join_meeting').on('click',function(){
                        joinMeeting(meeting_id)
                    });
                    modalMask();
                } else {
                    layer.alert('直播详情获取失败', {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                }
            },
            error: function(data){
                console.log(data);
            },
            complete:function(){
                $('.context-box').height($(window).height() - 70);
                setTimeout(function(){
                    $('.context-box').jScrollPane({
                        mouseWheelSpeed: 100
                    });
                }, 250);
                if ($(".lesson-past .write"))
                {
                    uploadFile({
                        'file' : ".lesson-past .stage_detail .file",
                        'picUpload' : '#picUpload1',
                        'btns' : ".lesson-past .submitBtn",
                        'textarea' : ".lesson-past textarea",
                        'qrurl' : ".lesson-past .QRurl",
                        'meeting_id' : ".lesson-past .con"
                    },uploadCallBack);
                }
            }
        });
        //上传完成，并且确认提交后的回调函数
        function uploadCallBack(){
            backMask();
            getOldMeeting(meeting_id);
        }
    };
};

/*
 * @ 入学须知
 * @ 服务承诺
 * @ 就业协议
 */
function agreement(obj){
    obj.modal({show:true, keyboard:false,backdrop: 'static'});
    obj.on('shown.bs.modal', function () {
        $('#' + obj.attr('id') + ' .zy_myAgreement_div').jScrollPane({
            mouseWheelSpeed:100
        });
    });
};

/*
 * @ 完善学习信息
 */
function perfectInfo(){
    $('#perfectinfo').modal({show:true, keyboard:false,backdrop: 'static'});
}

/*
 * @ 就业信息
 */
 ;(function($){
     $.fn.statisticsRadio=function(){
         if(this.length == 0) return this;
         if(this.length > 1){
             this.each(function(){$(this).statisticsRadio()});
             return this;
         }
         var th=this;
         th.children("input").click(function(){
             $("input[name='"+this.name+"']").each(function(index, element) {
                 if(element.checked){
                     $(this).parent().addClass("rH");
                 }else{
                     $(this).parent().removeClass("rH");
                 }
             });
         });
     }
 })(jQuery);

var _city = ['北京','上海','广州','深圳','天津','南京','武汉','沈阳','西安','成都','重庆','杭州','青岛','大连','宁波','济南','哈尔滨','长春','厦门','郑州','长沙','福州','苏州','无锡','乌鲁木齐','昆明','兰州','南昌','贵阳','南宁','合肥','太原','石家庄','呼和浩特','佛山','东莞','唐山','烟台','泉州','包头','温州','珠海','大庆','西宁','海口','徐州','淄博','潍坊','洛阳','南通','常州','绍兴','台州','鞍山','中山','汕头','吉林','柳州','拉萨','邯郸','银川','秦皇岛','沧州','威海','济宁','临沂','德州','滨州','泰安','湖州','嘉兴','金华','秦州','镇江','盐城','扬州','桂林','惠州','湛江','江门','茂名','株洲','岳阳','衡阳','宝鸡','宜昌','襄樊','开封','许昌','平顶山','赣州','九江','芜湖','绵阳','齐齐哈尔','牡丹江','抚顺','本溪','丹东','辽阳','锦州','营口','承德','廊坊','邢台','大同','榆林','延安','天水','南阳','濮阳','连云港','常德'];
function jobIntentionInfo(){
    $("#jobIntentionInfo input[type=reset]").trigger("click");
    $('#jobIntentionInfo').modal({show:true, keyboard:false,backdrop: 'static'});
    $(".statisticsRadio").statisticsRadio();
    $("#jobIntentionInfo .jobIntentionInfoBtn").on("click",function(){

        var selectCity = $("#goCity").val();
        var isHave = false;
        for (var i = 0; i < _city.length; ++i){
            if(selectCity == _city[i]){
                isHave = true;
                break;
            }
        }

        if(isHave == false){
            $(".errorInfo").html("请选择我们提供的城市作为意向城市").slideDown();
            return;
        }

        var jobIntentionInfoForm1=$("#jobIntentionInfoForm").serialize();
        var jobIntentionInfoForm=jobIntentionInfoForm1.split("&");

        for(var i=0;i<jobIntentionInfoForm.length;i++){
            var arr=jobIntentionInfoForm[i].split("=");
            if(arr[0]!="position"&&arr[0]!="industry"&&arr[1]==""){
                $(".errorInfo").html("不能为空").slideDown();
                $("#jobIntentionInfoForm input[name="+arr[0]+"]").focus();
                return false;
            }
        }
        if(jobIntentionInfoForm1.indexOf("onthejob")<0){
            $(".errorInfo").html("请选择在职与否").slideDown();
            return false;
        }
        $("#jobIntentionInfoForm").submit();
    });
};
// 意向城市切换功能
(function(){
    tab({
        tabNav: '.city-tab li',
        tabBox: '.city-wrap .city-cont',
        select: 'select'
    });
    var goCity = $('#goCity'),
        cityContainer = $('.city-container'),
        cityCont = $('.city-cont span');
    goCity.on('click', function(event){
        event.stopPropagation();
        cityContainer.show();
    });
    cityContainer.on('click', function(event){
        event.stopPropagation();
    });
    goCity.keyup(function(){
        if(goCity.val() == ''||null){
            $('.city-cont').children('span').removeAttr('style');
        }
        var index;
        for(var i=0; i<cityCont.length;++i){
            if(goCity.val() == $(cityCont[i]).text()){
                $(cityCont[i]).parent().siblings().children('span').removeAttr('style');
                index = $(cityCont[i]).parent().index();
                $(cityCont[i]).css({
                    'color': '#68d5c3',
                    'font-weight': 'bold'
                }).siblings().removeAttr('style');
            }
        }
        $('.city-tab li').eq(index).addClass('select').siblings().removeClass('select');
        $('.city-wrap .city-cont').eq(index).show().siblings().hide();
    });
    cityCont.on('click', function(){
        $(this).parent().siblings().children('span').removeAttr('style');
        goCity.val($(this).text());
        $(this).css({
            'color': '#68d5c3',
            'font-weight': 'bold'
        }).siblings().removeAttr('style');
    });
    $('#jobIntentionInfo').off().on('click', function(event){
        event.stopPropagation();
        cityContainer.hide();
    });
})();

// 任务成绩消息
function task_score_message(student_id){
    var arrTaskScoreMessage = [], ij = 0;
    $.ajax({
        url: "/lps4/student/ajax/task_score_message/",
        type: "GET",
        data: {'user_id':student_id},
        dataType: 'JSON',
        success : function(data){
            if(data.status){
                ij = 0;
                arrTaskScoreMessage = data.data;
                stage_task_id = data.stage_task_id;
                globalTaskScoreMessage();
            }
        }
    });

    var globalTaskScoreMessage = function(){
        if(arrTaskScoreMessage.length <= ij){
            $("#MyTaskScore").modal('hide');
            return;
        }
        $("#MyTaskScore .zy_mysuccess").html(arrTaskScoreMessage[ij]);
        if(ij == 0){
            $("#MyTaskScore").modal('show');
        }

        ij++;
        var oClose = $('.zy_newclose');
        oClose.on('click',function(){
            setTimeout(globalTaskScoreMessage,200);
        });
        var oClose2 = $('.scf_newclose');
        oClose2.on('click',function(){
            var rescore = $(this).attr('rescore');

            $('.right-fixed-box').stop().animate({
                'right': '0px'
            },250);
            $('#' + rescore).trigger('click');
            setTimeout(globalTaskScoreMessage,200);
        });
        $('.go-on-study').on('click',function(){
            setTimeout(globalTaskScoreMessage,200);
        });
    };

};

/*
 * @ 提示完善我的简历
 */
function perfectMyResume() {
    $('#perfectMyResume').modal('show');
    if (is_force_pop_complete_resume == 'True') {
        $('#perfectMyResume .close').remove();
    }
    else {
        $('#perfectMyResume .close').on('click', function () {
            $('#perfectMyResume').modal('hide');
        });
    }
}