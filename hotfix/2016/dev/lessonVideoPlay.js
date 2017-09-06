//初始化
var tempImg         = [],
    attachImg       = [];
var init = function () {
    var playerWrap = $('video'), player = playerWrap[0], headTitle1, headTitle2;
    // 意见反馈显示/关闭提示
    $(".ldFeedback a").mouseover(function(){
    $(this).siblings(".feedboxTip").stop().slideDown(150).animate({"opacity":"1"},400);
    });
    $(".feedboxTip .closed").click(function(){
        $(this).parent().stop().animate({"opacity":"0"},250).slideUp(500);
    });    

    // 获取当前播放的是第几章
    function get_current_lesson_index() {
        return parseInt($('.lesson li .selected').text());
    }


    // 设置不再提醒
    function set_no_longer_remind_flag(flag) {
        $.cookie('pop_career_no_longer_remind_flag', flag, {expires: 365, path: '/course/'});
    }

    function get_no_longer_remind_flag() {
        return $.cookie('pop_career_no_longer_remind_flag');
    }

    if ($thisUser == 'False') {
        if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
            login_popup('请先登录');
        }
    }

    // 查看职业课程大纲弹窗
    var oCheckBox = $('.check_box'), // 不在提醒checkbox
        oVideoPartLists = $('.lesson li'), // 课程列表
        oCheckLessonLists = $('#check_lesson_lists'), // 查看课程大纲弹窗
        oJustPay = $('#just_pay'), // 立即付费弹窗
        zy_nnn = 0,
        zy_nbo = $needPay,
        zy_nbo2 = $isPaid,
        no_longer_remind_flag = get_no_longer_remind_flag() || false,
        to_be_update = true; // 待更新进度,在更新进度后变成false

    oVideoPartLists.each(function () {
        zy_nnn++;
        if ($(this).children().hasClass("need_pay")) {
            return false;
        }
    });

    oCheckLessonLists.on('click', '.close', function () {
        oCheckLessonLists.modal('hide');
    });

    oJustPay.on('click', '.close', function () {
        oJustPay.modal('hide');
    });

    oCheckBox.on('click', function () {
        if ($(this).hasClass('in')) {
            set_no_longer_remind_flag(false);
            $(this).removeClass('in');
        } else {
            set_no_longer_remind_flag(true);
            $(this).addClass('in');
        }
    });

    //测试用,不要开
    //Videojs();

    // 定期判断: 当视频处于播放状态, 向后端发送用户和课程信息 for business log
    setInterval(function () {
        if (!player.paused) {
            //var course_id = $("#course_id").val();
            //var lesson_id = $("#lesson_id").val();
            $.get("/v4/append_study_info?course_id=" + $courseId + "&lesson_id=" + $lessonId);
        }
    }, 1000 * 60);

    $(".vjs-error-display").html('<div><img src="/images/refresh.png">&nbsp;&nbsp;视频加载失败，请<a onclick="location.reload();" style="cursor: pointer;">刷新重试</a></div>');
    $("#microohvideo").append($(".videoStopMeg"));

    function isIE(){
        if (!!window.ActiveXObject || "ActiveXObject" in window){
            return true;
        }else{
            return false;
        }
    };
    
    // 获取视频开始播放的时间并从该时间播放, copied and modified from LPS2.0
    //var video_current_time = $.cookie('lesson_{{ lesson_id }}');
    var video_current_time = $.cookie('lesson_' + $lessonId) ? $.cookie('lesson_' + $lessonId) : 0;
   
    var playerBO = true;
    playerWrap.ready(function () {
        if(!isIE()){
            player.currentTime = video_current_time;
        }

        // 记录当前章节播放时间。用于断点播放
        setInterval(function () {
            getPlayPostion();
        }, 1000);

        playerWrap.on("play", function () {
            zy_nbo2 = true;
            if ($thisUser == 'False') {
                //测试用,不要开
                //player.pause();
                startPause();
                if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                    login_popup('请先登录');
                }
            } else if (get_current_lesson_index() == 3 && $needPay && !$isPaid && $ifHaveCareerCourse) { // 判断当前播放的是第几章
                if (player.currentTime > 60 && zy_nbo && zy_nbo2) {
                    zy_nbo2 = false;
                    //测试用,不要开
                    //player.pause();
                    startPause();
                    pop_pay();
                }
                setInterval(function () {
                    if (player.currentTime > 60 && zy_nbo && zy_nbo2) {
                        zy_nbo2 = false;
                        //测试用,不要开
                        //player.pause();
                        startPause();
                        pop_pay();
                    }
                }, 1000);
                return false;
            } else if (get_current_lesson_index() > 3 && $needPay && !$isPaid && $ifHaveCareerCourse) {
                if (zy_nbo && zy_nbo2) {
                    zy_nbo2 = false;
                    //测试用,不要开
                    //player.pause();
                    startPause();
                    pop_pay();
                }
                return false;
            }
        });

        playerWrap.on("ended", function () {

            // 广告弹出框条件,!不再显示 && 职业课程广告配图没有值 && 对此课程相关职业课程未付费
            if (!no_longer_remind_flag && !$ad && !$isPaid) {
                if (!oCheckLessonLists.hasClass('in') && $('.modal-backdrop').length <= 0) {
                    oCheckLessonLists.modal('show');
                }
            }
            $.cookie('lesson_' + $lessonId, null);
        });

        //$(player.tag || player.L).on('dblclick', function () {
        //  if (player.isFullscreen()) {
        //      player.exitFullscreen();
        //  } else {
        //      player.requestFullscreen();
        //  }
        //});
    });


    // 重新播放
    $(".VSMbtn1").on("click", function () {
        if ($thisUser == 'True') {
            player.pause();
            if (player.paused) {
                startPause();
                to_be_update = true; // 初始化待更新进度的值为true
            }
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
        }
    });

    // 获取视频的播放进度， copied and modified from LPS2.0
    function getPlayPostion() {
        //将当前播放实际进度保存到cookie
        var current_position = Math.ceil(player.currentTime);
        $.cookie('lesson_' + $lessonId, current_position);
        if (current_position) {
            if ($thisUser == "True") {
                //判断视频是否播放到整体进度的95%
                var video_total_time = $videoLength;
                // 如果是在lps3里学习,并且视频播放时间到了规定的百分比,记录学习记录
                if (to_be_update == true && $classId.length > 0 && (current_position / video_total_time) > $videoExamComplete) {
                    // 更新是否完成该章节的学习
                    to_be_update = false;
                    $.get("/lps3/student/ajax/item_lesson/update/" + $userItem);
                }
            }
        }
    }

    function has_next() {
        var next = $('.video_part_lists li.liH').next();
        return Boolean(next.length)
    }

    function jump_next_course() {
        var next = $('.video_part_lists li.liH').next();
        window.location = next.children().get(0).href;
    }

    // 事件
    $(".VSMbtn").on("click", '.VSMbtn2', function () {
        if (has_next()) {
            jump_next_course();
        } else {
            if (player) player.cancelFullScreen();
            var zvA = $(".zvright a").eq(0);
            if (!zvA.hasClass("aH")) zvA.trigger("click");
        }
    });
    // 下载课件
    if ($thisUser == 'False') {
        $(".zvrightSreen3 a").each(function () {
            $(this).on("click", function () {
                if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                    login_popup('请先登录');
                }
            })
        });
    }

    //初始化标题
    headTitle1 = $(".video_part_lists li.liH a").find(".col_l").text();
    headTitle2 = $(".zyleve1 li.liH a").attr("title");
    $(".zyNewVideo_top .s").html(headTitle1 || headTitle2);

    // 分页
    var zyright = true,
        zvideoW = $(".zvideo_index").width();

    function mouseWheel(obj, speed) {
        $(obj).jScrollPane({
            mouseWheelSpeed: speed
        });
    }


    /*
     * @ 提问
     *
     */
    var insertLi = "<li class='last'><span class='font14 color66 uploadPreview'><i class='add-screenshot-img'></i><input type='file' name='image' accept='image/*' multiple id='uploadPreview'><span class='add-img-msg font14 color66'>添加图片</span></span></li>",

        bottomModule    = $('.bottom-module'),
        tiwenCon        = $('.tiwen-con'),
        user            = $('.user'),
        share           = $('.share'),
        downLoad        = $('.down-load'),
        messageWarp     = $('.message-wrap'),
        altTa           = $('.alt-ta'),
        btnBox          = $('.btn-box'),
        tiwenBtn        = $('.tiwen-btn'),
        cancelBtn       = $('.cancel-btn'),
        current         = $('.current'),
        curTime         = $('.current-time'),
        uploadCon       = $('.upload-con'),
        uploadImg       = $('.upload-img'),
        insertImg       = $('#insert-img'),
        insertImgList   = $('#insert-img-list'),
        cancelInsertBtn = $('.cancel-insert-btn'),
        insertImgBtn    = $('.insert-img-btn'),
        uploadCon       = $('.upload-con'),
        errorMsg        = $('.msg'),
        stopPro         = [tiwenCon, insertImg, $('.questions-top a'), $('.questions-bottom .share'), $('.question-current span')],
        msgTips         = errorMsg.html(),
        isTrue          = true,
        //tempImg         = [],
        //attachImg       = [],
        real_img_url    = '';


    function templateHtml(_url, url, i) {
        var html = '';
        html += '<li>';
        html += '<i id="' + i + '" class="remove-img"></i>';
        html += '<img _src="' + _url + '" src="' + url + '" height="120" width="120"/>';
        html += '</li>';
        return html;
    }

    function createItems(imgArray) {
        var html = '';
        for (var i = 0; i < imgArray.length; i++) {
            html += templateHtml(imgArray[i][1], imgArray[i][0], i);
        }
        insertImgList.html("");
        insertImgList.append(html);
        insertImgList.append(insertLi);

        if (insertImgList.find('li').length > 4) {
            insertImgList.find('li.last').hide().prev().css('margin-right', 0);
        }

        $('.remove-img').on('click', function () {
            $(this).parent().remove();
            var _index = $(this).attr("id");
            if (insertImgList.find('li').length <= 4) {
                insertImgList.find('li.last').show().prev().css('margin-right', '20px');
            }

            tempImg.splice(_index, 1);
        });

        $('#uploadPreview').fileupload({
            url: '/common/img/upload/',
            dataType: 'json',
            autoUpload: true,
            add:function(e,data){
                var uploadErrors = [];
                var acceptFileTypes = /^(png|jpg|jpeg)$/i;
                var filesize = data.originalFiles[0]['size']/(1024);

                Ntype = data.originalFiles[0]['name'].split('.');
                Ntype = Ntype[Ntype.length - 1];

                if(!acceptFileTypes.test(Ntype)){
                    errorMsg.text('图片格式不正确！').css({'color': '#F01400'});
                    uploadErrors.push('Not an accepted file type');
                    setTimeout(function(){
                        errorMsg.html(msgTips).css({'color': '#666'});
                    }, 2000);
                }
                if(parseInt(filesize)>500) {
                    errorMsg.text('文件超过500KB大小！').css({'color': '#F01400'});
                    uploadErrors.push('Filesize is too big');
                    setTimeout(function(){
                        errorMsg.html(msgTips).css({'color': '#666'});
                    }, 2000);
                }
                if(uploadErrors.length == 0){
                    data.submit();
                }
            },
            done: function (e, data) {
                if (data.result.data.result.img_url != undefined && data.result.data.small_result.img_url != undefined) {
                    tempImg.push([data.result.data.small_result.img_url, data.result.data.result.img_url]);
                }
                createItems(tempImg);
            }
        });

    }

    function getLength(str){
       return String(str).replace(/[^\x00-\xff]/g,'aa').length;
    }

    // 提交问题事件
    tiwenBtn.on('click', function (event) {
        if($thisUser == 'False'){
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
        }else{
            var Img = $('#insert-img-list img');
            var arr = [];
            var smallArr = [];
            for (var i = 0; i < Img.length; i++) {
                var imgSrc = Img.eq(i).attr('_src');
                var smallImgSrc = Img.eq(i).attr('src');
                if (imgSrc && smallImgSrc) {
                    imgSrc = imgSrc.split('/uploads/')[1];
                    smallImgSrc = smallImgSrc.split('/uploads/')[1];
                    arr.push(imgSrc);
                    smallArr.push(smallImgSrc);
                }
            }
            var dataJson = {
                'discuss_location': discuss_location,
                'object_id': object_id,
                'object_name': object_name,
                'comment': textMsg.val(),
                'object_content': $('.message-wrap .current-time').text(),
                'material_arr': arr,
                'small_material_arr': smallArr
            };
            var Strnum = Math.ceil(getLength($('.text-msg').val()));
            if (textMsg.val() == '' || null) {
                layer.tips('请输入您的问题。', textMsg, {
                  tips: [1, '#5ECFBA'],
                  time: 4000
                });
            } else if(Strnum > 1000){
                layer.tips('输入超过1000字，请重新输入。', textMsg, {
                  tips: [1, '#5ECFBA'],
                  time: 4000
                });
            } else if($groupName == 'teacher'){
                layer.tips('对不起，老师不能提问。', textMsg, {
                  tips: [1, '#5ECFBA'],
                  time: 4000
                });
            } else {
                flyAnimate(event);
                $.ajax({
                    url: '/common/question_post/',
                    data: dataJson,
                    dataType: 'json',
                    type: 'POST',
                    success: function (data) {
                        var questionsWrap = $('.all-questions, .my-questions');
                        if (data['status']=='success'){
                            questionsWrap.each(function (index, ele) {
                                if ($(ele).find('ul').length == 0) {
                                    $(ele).find('.no-answer').remove();
                                    $(ele).children().children().html('<ul></ul><a class="load-more">加载更多</a>')
                                }
                            });
                            questionsWrap.find('ul').prepend(data.html);
                            insertImgList.html("");
                            insertImgList.append(insertLi);
                            praise();
                            replyQuestion();
                        }

                        textMsgTxt = '';
                    }
                });
                initTextMsg();
                attachImg = [];
                tempImg = [];
                uploadCon.children('.pin').remove();
            }
        }
    });

    function flyAnimate(event) {
        var offset = $("#target").offset();
        var flyer = $('<div id="boll" class="boll"></div>');

        flyer.fly({
            start: {
                left: event.pageX,
                top: event.pageY
            },
            end: {
                left: offset.left + 10,
                top: offset.top + 10
            },
            onEnd: function () {
                this.destory();
            }
        });
    }

    // 插入图片弹窗
    uploadImg.on('click', function () {
        if ($thisUser == 'False') {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
        } else {
            $(this).parent('.message_wrap').addClass('actived');
            errorMsg.html(msgTips).css({'color': '#666'});
            insertImgList.html("");
            tempImg = attachImg;
            createItems(tempImg);
            insertImg.modal('show');
        }
    });

    // 插入图片别针
    insertImgBtn.on('click', function () {
        insertImg.modal('hide');
        attachImg = tempImg;
        tempImg = [];
        if (attachImg.length > 0) {
           $('.upload_btn').addClass('have_img');
        }else{
            $('.upload_btn').removeClass('have_img');
        }
        $('.message_wrap').removeClass('actived');
    });

    // 插入图片弹窗取消
    cancelInsertBtn.on('click', function () {
        errorMsg.html(msgTips).css({'color': '#666'});
        insertImg.modal('hide');
        tempImg = [];
        if (attachImg.length == 0) {
            uploadCon.children('.pin').remove();
            $('.upload_btn').removeClass('have_img');
        }
        $('.message_wrap').removeClass('actived');
    });

    /*
     * @ 侧边栏交互
     *
     */
    var tabNav            = $('.tab-nav li'),
        tabBox            = $('.tab-box > div'),
        allQuestions      = $('.all-questions'),
        myQuestions       = $('.my-questions'),
        allQuestionsLists = $('.all-questions-lists'),
        questionsBox      = $('.questions-box'),
        backQuestions     = $('#back-questions'),
        replyTotal        = $('.reply-total'),
        object_id         = $('.object_id').val(),
        class_id          = $('.class_id').val(),
        object_name       = $('.object_name').val(),
        discuss_location  = $('.discuss_location').val(),
        from_user_center  = false;

    tabNav.on('click', function () {
        if ($thisUser == 'True') {
            var i = $(this).index();
            $(this).addClass('active').siblings().removeClass('active');
            tabBox.eq(i).show().siblings().hide();
            mouseWheel('.all-questions, .my-questions', 100);
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
            return false;
        }
    });


    var intoOneQuestion = function (discuss_id) {
        if ($thisUser == 'True') {
            mouseWheel('.one-question-view', 100);
            questionsBox.css('margin-left', '-360px');
            allQuestions.css('opacity', 0);
            myQuestions.css('opacity', 0);

            // 此时的last_id是问题的本身的last_id,即为问答详情的discuss_id和problem_id
            discuss_id = isNaN(discuss_id) ? $(this).find('.last_id').val() : discuss_id;
            loadOne(discuss_id)
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
            return false;
        }
    };

    // 如果进来的时候后面有问号则,加载一个问题详情,打开右边栏,定位视频播放位置
    $(function () {
            if (window.location.search.length > 0) {
                var _str_list = window.location.search.split('=');
                var discuss_id = _str_list[_str_list.length - 1];
                $('.zvright a').eq(1).trigger("click");
                from_user_center = true;
                intoOneQuestion(discuss_id);
            }
        }
    );

    // 点击问题列表到问题详情
    $('.all-questions, .my-questions').on({click: intoOneQuestion}, 'li');

    // 返回问题列表
    backQuestions.on('click', function () {
        questionsBox.css('margin-left', '0');
        allQuestions.css('opacity', 1);
        myQuestions.css('opacity', 1);
    });

    // 原图查看弹窗
    var _src = null;
    $('.one-question-view').on({'click':function(e){
        e.stopPropagation();
        _src = $(this).attr('_src');
        imgPopup(_src);
    }}, '.questions-img img');

    // 回复
    var replyBtn, submitReplyBtn, replyMsg, tipsMsg,
        replyTextarea, _parent_id, _problem_id, _answer_user_id, _answer_nick_name,
        _placehodler;

        replyBtn          = $('.reply-btn');
        submitReplyBtn    = $('.submit-reply-btn');
        replyMsg          = $('.reply-msg');
        replyTextarea     = $('.reply-textarea');
        _parent_id        = null;
        _problem_id       = null;
        _answer_user_id   = null;
        _answer_nick_name = null;
        _placehodler      = null;

    replyTextarea.find('textarea').keyup(function (event) {
        event.stopPropagation();
    });

    // 在问答详情点击回复
    //replyBtn.on('click', function(){
    $(document).on('click', '.reply-btn', function () {
        $('.reply-textarea').css('bottom', 0);

        // 如果是回复'回复',parent_id为回复本身,problem_id为问题
        if ($(this).parent().hasClass('reply-date')) {
            _parent_id = $(this).parents('.right').siblings('.left').find('.last_id').val();
            _problem_id = $(this).parents('.right').siblings('.left').find('.problem_id').val();
            _answer_user_id = $(this).parent().parent().parent().siblings('.left').find('.answer_user_id').val();
            _answer_nick_name = $(this).parent().parent().parent().siblings('.left').find('.answer_nick_name').val();
            _placehodler = '回复' + $.trim(_answer_nick_name) + ':';
            // 否则是回复'问题',则parent_id和problem_id为同一个
        } else {
            _parent_id = $(this).parent().siblings('.last_id').val();
            _problem_id = _parent_id;
            _answer_user_id = $(this).parent().siblings('.answer_user_id').val();
            _answer_nick_name = $(this).parent().siblings('.answer_nick_name').val();
            _placehodler = '回复' + $.trim(_answer_nick_name) + ':';
        }
        replyTextarea.find('textarea').attr({placeholder: _placehodler});
    });

    // 在问答列表点击回复声明
    function replyQuestion() {
        if ($thisUser == 'True') {
            var replyTotal = $('.reply-total');
            replyTotal.unbind();
            replyTotal.on({'click': function () {
                questionsBox.css('margin-left', '-360px');
                replyTextarea.css('bottom', 0);
                // parent_id和problem_id为同一个
                _parent_id = $(this).parents('li').find('.last_id').val();
                _problem_id = _parent_id;
                _answer_user_id = $(this).parents('li').find('.answer_user_id').val();
                _answer_nick_name = $(this).parents('li').find('.answer_nick_name').val();
                _placehodler = '回复' + $.trim(_answer_nick_name) + ':';
                replyTextarea.find('textarea').attr({placeholder: _placehodler});
            }});
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
            return false;
        }
    }

    // 在问答列表点击回复事件
    replyQuestion();

    // 回复按钮绑定回复事件声明
    function answerBind () {
        submitReplyBtn.on('click', function () {
            var _comment = $('textarea').val();
            $(this).off();
            postAnswer(object_id, _parent_id, _problem_id, _comment, _answer_user_id, _answer_nick_name);
        });
    }

    answerBind ();

    // 提交回答
    var postAnswer = function (object_id, _parent_id, _problem_id, _comment, _answer_user_id, _answer_nick_name) {
        var tipsMsg = '';
        if(_comment == ''){
            tipsMsg = $('<span>请输入回复内容！</span>');
            $('.submit-reply-btn').before(tipsMsg);
            setTimeout(function(){
                tipsMsg.remove();
            }, 2000);
        }else{
            $.ajax({
                url: '/common/answer_post/',
                data: {
                    'object_id': object_id,
                    'parent_id': _parent_id,
                    'problem_id': _problem_id,
                    'comment': _comment,
                    'answer_user_id': _answer_user_id,
                    'answer_nick_name': _answer_nick_name
                },
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    if (data['status']=='success'){
                        // 如果回复的是问题
                        if (data.parent_id == data.problem_id) {
                            $('.question-lists').prepend(data.html)
                        } else {
                            $('#answer_' + data.parent_id).after(data.html)
                        }
                        $('.reply-textarea').css('bottom', '-180px').find('textarea').val('');
                        $('.one-question-view .load-more').text('没有更多');
                        $('.one-question-view').jScrollPane({mouseWheelSpeed: 100});
                    }else{
                        tipsMsg = $('<span>'+data['msg']+'</span>');
                        $('.submit-reply-btn').before(tipsMsg);
                        setTimeout(function(){
                            tipsMsg.remove();
                        }, 2000);
                    }
                    answerBind ();
                }
            });
        }
    };

    // 点赞声明
    var praise = function () {
        var good = $('.good');
        good.unbind();
        good.on({
            'click': function (event) {
                if ($thisUser == 'True') {
                    event.stopPropagation();
                    var ths = $(this);
                    var problem_id = ths.parent().siblings('.last_id').val();
                    var small = ths.children('small');
                    $.ajax({
                        url: '/home/s/ajax_praise/',
                        method: 'POST',
                        dataType: 'json',
                        data: {'problem_id': problem_id},
                        success: function (result) {
                            if (result['success']) {
                                var action = result['data']['action'];
                                var praise_count = result['data']['praise_count'];

                                // 对在其他位置的这个问题同步点赞次数
                                $('.last_id').each(function () {
                                    var last = $(this);
                                    var good_a = last.parent().find('.good');

                                    if (last.val() == problem_id) {
                                        var last_small = $(good_a).children('small');

                                        if (action == 'mark') {
                                            last_small.html(praise_count);
                                            good_a.addClass("jia-good");
                                        } else if (action == 'cancel') {
                                            last_small.html(praise_count);
                                            good_a.removeClass("jia-good");
                                        }
                                    }
                                });
                            } else {
                                if (result['code'] == 401) {
                                    if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                                        login_popup('登录状态已过期！');
                                    }
                                    return false;
                                }
                            }
                        }
                    });
                } else {
                    if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                        login_popup('请先登录');
                    }
                    return false;
                }
            }
        });
    };
    // 点赞
    praise();

    $('.reply-cancel').on('click', function () {
        $('.reply-textarea').css('bottom', '-180px');
    });

    // 加载更多
    $('.load-more').on('click', function () {
        var last_id = null,
            _ul = null,
            object_id = null;
        // 如果是在问答详情里
        if ($(this).parents('.scroll-pane').hasClass('one-question-view')) {
            last_id = $(this).siblings().find('.questions-reply').last().find('.last_id').val();
            // 此时object_id实际上是指problem_id,即loadOne的discuss_id
            object_id = $(this).siblings().find('.questions-reply').last().find('.problem_id').val();
            _ul = $(this).siblings().find('.question-lists');
        } else {
            last_id = $(this).siblings().children().last().find('.last_id').val();
            object_id = $(this).siblings().children().last().find('.object_id').val();
            _ul = $(this).siblings();
        }
        var _role = $(this).parents('.scroll-pane').attr('class').split(' ')[0];
        var role = _role.split('-')[0];
        loadMore(object_id, last_id, _role, role, _ul);
    });

    var loadMore = function (object_id, last_id, _role, role, _ul) {
        if ($thisUser == 'True') {
            $.ajax({
                url: "/common/" + role + "_more/" + object_id + "/" + last_id + "/",
                dataType: "html",
                type: "GET",
                success: function (data) {
                    if ($.parseJSON(data)['status'] == 'failed') {
                        $('.' + _role + ' .load-more').text('没有更多').off('click')
                    } else {
                        _ul.append($.parseJSON(data)['html']);
                    }
                    $('.all-questions, .my-questions, .one-question-view').jScrollPane({
                        mouseWheelSpeed: 100
                    });
                    praise();
                }
            });
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
            return false;
        }
    };


    // 显示一个问题的详情
    var loadOne = function (discuss_id) {
        $.ajax({
            url: "/common/one_more/" + discuss_id + "/0/",
            dataType: "html",
            type: "GET",
            success: function (data) {
                $('.one-question-view li').empty().append($.parseJSON(data)['html']);
                if ($.parseJSON(data)['has_answer'] == false) {
                    $('.one-question-view .load-more').text('暂无回答')
                } else {
                    $('.one-question-view .load-more').text('加载更多')
                }
                $('.one-question-view').jScrollPane({
                    mouseWheelSpeed: 100
                });
                praise();
                //jumpTime($('.one-question-view .question-current span').text());
                if (from_user_center == true) {
                    $('.question-current span').trigger('click');
                    from_user_center = false
                }
                $.getScript('http://v3.jiathis.com/code/jia.js?uid=1680508');
                jiathis_config = {
                    data_track_clickback: true,
                    shortUrl: false,
                    hideMore: false,
                    url: window.location.origin + '/u/'+ $('.answer_user_id').val() + '/discuss/?p_id=' + discuss_id,
                    summary: "我正在麦子学院学习"+ $(document).attr("title") +",赶快和我一起来感受神奇的在线学习方式吧！——麦子学院，在线学习好工作。",
                    title: $('.one-question-view .question-title').text()
                }
            }
        })
    };

    // 问题时间点击跳转
    $('.content_left').on({'click': jumpTime}, '.question-current span');
    $('.question-current span').on({'click': jumpTime});

    function jumpTime(){
        if ($thisUser == 'True') {
            var t = $(this).text();
            t = t.split(":");
            var _t = 0;
            for (var i = 0; i < t.length; i++) {
                _t += parseInt(t[i]) * Math.pow(60, t.length - 1 - i);
            }
            player.currentTime = _t;
        } else {
            if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
                login_popup('请先登录');
            }
            return false;
        }
    }

    // 下一节
    $('.play-next-control,.VSMbtn2').on('click', function () {
        // 呼出右侧边栏
        //var zvA = $(".zvright a").eq(0);
        //if (!zvA.hasClass("aH")) zvA.trigger("click");
        if ($classId.length > 0) {
            nextcourseLps3();
        } else { //小课程播放页下一节
            var next_href = null;
            $('.lesson li').each(function () {
                if ($(this).children().hasClass('selected')) {
                    next_href = $(this).next().children().attr('href');
                    return true;
                }
            });
            if (next_href) {
                window.location.href = next_href;
            } else {
                layer.alert('没有下一节！', {
                    skin: 'layui-layer-molv',
                    closeBtn: 0
                });
            }
        }
    });

    // lps3视频播放页下一节
    function nextcourseLps3() {
        var goA = $(".zyleve1>li,.zvrightSreen .d-task-list li.last");
        goA.each(function (index, ele) {
            if ($(ele).hasClass("liH")) {
                var goAindex = goA.eq(index + 1);
                if (goAindex.find("a").attr("href")) {
                    var zyleve1_href = goAindex.find("a").attr("hid_href");
                    if (zyleve1_href) location.href = zyleve1_href;
                }
                else {
                    goAindex.find("a").trigger("click");
                }
            }
            //if (goA.length - 1 == index) {
            //    location.href == $(ele).find("a").attr("hid_href")
            //}
        })
    }

    // 试学班返回按钮
    var q_arr = {};
    $('.show-remark').on({
        'click': function () {
            $.ajax({
                type: "GET",
                url: $("#questionnaire_url").val(),
                dataType: 'json',
                success: function (data) {
                    if (data.success == true) {
                        window.location.href = $("#next_url").val();
                    } else {
                        $("#satisfy-examen").html(data.data.html).modal({
                            show: true,
                            keyboard: false,
                            backdrop: 'static'
                        });
                        $('.satisfy-list li').each(function () {
                            $(this).find('label').click(function () {
                                $(this).parent().addClass('now').siblings().removeClass('now');
                                $(this).addClass('select').parent().siblings().children().removeClass('select');
                                var id = $(this).parent().parent().siblings().attr('id');
                                var key = $(this).attr('value');
                                var val = $(this).text();
                                q_arr[id] = '{"' + key + '":"' + val + '"}';
                            });
                        });
                        $('.button-group').on({
                            'click': function () {
                                $.ajax({
                                    type: "POST",
                                    url: $("#submit_url").val(),
                                    data: q_arr,
                                    dataType: 'json',
                                    success: function (data) {
                                        if (data['msg'] == 'success') {
                                            window.location.href = $("#next_url").val();
                                        } else if (data['msg'] == 'fail') {
                                            $('.modal-content .err_msg').text(data['data']).show().fadeOut(
                                                8000, $('#satisfy-examen').modal('hide')
                                            );
                                        } else {
                                            $('.modal-content .err_msg').text(data['data']).show().fadeOut(3000);
                                        }
                                    }
                                });
                            }
                        }, '.submit');
                    }
                }
            });
        }
    });
    $('#satisfy-examen').on({
        'click': function () {
            window.location.href = $("#next_url").val();
        }
    }, '.next-time');

};

!function (a) {
    a.fly = function (b, c) {
        var d = {
                version: "1.0.0",
                autoPlay: !0,
                vertex_Rtop: 20,
                speed: 1.2,
                start: {},
                end: {},
                onEnd: a.noop
            },
            e = this,
            f = a(b);
        e.init = function (a) {
            this.setOptions(a),
            !!this.settings.autoPlay && this.play()
        },
            e.setOptions = function (b) {
                this.settings = a.extend(!0, {},
                    d, b);
                var c = this.settings,
                    e = c.start,
                    g = c.end;
                f.css({
                    marginTop: "0px",
                    marginLeft: "0px",
                    position: "fixed"
                }).appendTo("body"),
                null != g.width && null != g.height && a.extend(!0, e, {
                    width: f.width(),
                    height: f.height()
                });
                var h = Math.min(e.top, g.top) - Math.abs(e.left - g.left) / 3;
                h < c.vertex_Rtop && (h = Math.min(c.vertex_Rtop, Math.min(e.top, g.top)));
                var i = Math.sqrt(Math.pow(e.top - g.top, 2) + Math.pow(e.left - g.left, 2)),
                    j = Math.ceil(Math.min(Math.max(Math.log(i) / .05 - 75, 30), 100) / c.speed),
                    k = e.top == h ? 0 : -Math.sqrt((g.top - h) / (e.top - h)),
                    l = (k * e.left - g.left) / (k - 1),
                    m = g.left == l ? 0 : (g.top - h) / Math.pow(g.left - l, 2);
                a.extend(!0, c, {
                    count: -1,
                    steps: j,
                    vertex_left: l,
                    vertex_top: h,
                    curvature: m
                })
            },
            e.play = function () {
                this.move()
            },
            e.move = function () {
                var b = this.settings,
                    c = b.start,
                    d = b.count,
                    e = b.steps,
                    g = b.end,
                    h = c.left + (g.left - c.left) * d / e,
                    i = 0 == b.curvature ? c.top + (g.top - c.top) * d / e : b.curvature * Math.pow(h - b.vertex_left, 2) + b.vertex_top;
                if (null != g.width && null != g.height) {
                    var j = e / 2,
                        k = g.width - (g.width - c.width) * Math.cos(j > d ? 0 : (d - j) / (e - j) * Math.PI / 2),
                        l = g.height - (g.height - c.height) * Math.cos(j > d ? 0 : (d - j) / (e - j) * Math.PI / 2);
                    f.css({
                        width: k + "px",
                        height: l + "px",
                        "font-size": Math.min(k, l) + "px"
                    })
                }
                f.css({
                    left: h + "px",
                    top: i + "px"
                }),
                    b.count++;
                var m = window.requestAnimationFrame(a.proxy(this.move, this));
                d == e && (window.cancelAnimationFrame(m), b.onEnd.apply(this))
            },
            e.destory = function () {
                f.remove()
            },
            e.init(c)
    },
        a.fn.fly = function (b) {
            return this.each(function () {
                void 0 == a(this).data("fly") && a(this).data("fly", new a.fly(this, b))
            })
        }
}(jQuery);

init();