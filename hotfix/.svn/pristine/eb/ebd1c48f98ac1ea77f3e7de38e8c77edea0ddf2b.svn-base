/**
 * Created by Administrator on 2016/10/11.
 */
$(function() {
    // 是否登录
    var is_login = $thisUser == 'True',
        comment_input = $('.quiz_input'),
        QA_lists = $('.QA_lists');

    // 防止多次登录弹窗
    function safe_login_popup(text) {
        text = text ? text : '请先登录';
        if (!$('#loginModal').hasClass('in') && $('.modal-backdrop').length <= 0) {
            login_popup(text);
        }
    }

    // 导师介绍长度过长显示“显示全部”
    var tea_intro = $('.tea_intro>p').height();
    if (tea_intro>72){
        $('.tea_intro').siblings('.show_more').css({'display':'inline-block'});
    }

    function getLength(str){
       return String(str).replace(/[^\x00-\xff]/g,'aa').length;
    }

    function get_roll_height() {
        return window.innerHeight/4;
    }

    // 点击提问时间跳转
    $('.quiz_time').off().on('click',function(){

    })

    // tab切换
    $('.content_left .tab ul li').click(function(){
        $(this).addClass('selected').siblings().removeClass('selected');
        var index = $(this).index();
        $('.tab_content > div').eq(index).show().siblings().hide(); 
        if(index > 0){
            $('.my_join').hide();
        }else{
            $('.my_join').show();
        }          
    });

    // 查看和收起更多评论
    function on_more_discuss() {
        $('.more_discuss').off('click').on('click', function() {
            var text = $(this).text();
            var _this = $(this);
            if (text.split('收起↑').length > 1) {
                $(this).siblings('dd:gt(1)').slideUp(500);
                setTimeout(function() {
                    hide_bord_bot(_this);
                }, 500); // 延时500毫秒隐藏底边框
                $(this).text($(this).attr('value'));
            } else {
                $(this).siblings('dd:eq(1)').find('.children_text').removeClass('no_bd_btm');
                $(this).siblings('dd:gt(1)').slideDown(500);
                $(this).text('收起↑');
            }
        });
    }
    on_more_discuss();

    // 隐藏底边框
    function hide_bord_bot(current) {
        $(current).siblings('dd:eq(1)').find('.children_text').addClass('no_bd_btm');
    }

    function reBindEvent() {
        on_reply(); // 绑定回复按钮点击事件
        on_cancel();    // 绑定取消按钮点击事件
        on_praise();    // 绑定点赞事件
        child_button_click();   // 绑定回复子回复按钮事件
        showBigImgMain();   // 绑定查看大图事件
        on_more_discuss();  // 收起展开子评论
    }

    var lesson_id         = $('#lesson_id').val(),
        lesson_name       = $('#lesson_name').val(),
        discuss_location  = $('#discuss_location').val();

    // 向老师提问
    $('.submit_div .submit').on('click', function () {
        if (!is_login) {
            safe_login_popup();
            return false;
        }
        btn_disabled(this);

        var Img = $('#insert-img-list img');
        var arr = [];
        var smallArr = [];
        var self = this;
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
            'object_id': lesson_id,
            'object_name': lesson_name,
            'comment': $.trim(comment_input.val()),
            'object_content': $('.progressTime .current').text(),
            'material_arr': arr,
            'small_material_arr': smallArr
        };

        var str_num = Math.ceil(getLength(comment_input.val()));
        if ($.trim(comment_input.val()) == '' || null) {
            layer.tips('请输入您的问题。', comment_input, {
              tips: [1, '#5ECFBA'],
              time: 4000
            });
            btn_abled(this);
        } else if(str_num > 1000){
            layer.tips('输入超过1000字，请重新输入。', comment_input, {
              tips: [1, '#5ECFBA'],
              time: 4000
            });
            btn_abled(this);
        } else if($groupName == 'teacher'){
            layer.tips('对不起，老师不能提问。', comment_input, {
              tips: [1, '#5ECFBA'],
              time: 4000
            });
            btn_abled(this);
        } else {
            $.ajax({
                url: '/common/question_post_lps4/',
                data: dataJson,
                dataType: 'json',
                type: 'POST',
                success: function (data) {
                    var questionsWrap = $('.QA_lists');
                    if (data['status']=='success'){
                        clear_empty_qa();
                        var html = $(data.html);
                        html.hide();
                        questionsWrap.prepend(html);
                        html.fadeIn();
                        $('html, body').animate({scrollTop:html.offset().top-get_roll_height()}, 1000);

                        comment_input.val('');
                        clear_img_cache();
                        reBindEvent();
                        btn_abled(self);
                    }

                }
            });
            $('.upload_btn').removeClass('have_img');
        }

    });

    function clear_img_cache() {
        $('#insert-img-list li:not(.last)').remove();
        attachImg = [];
        tempImg = [];
    }

    // 点赞声明
    var on_praise = function () {
        $('.like').off('click').on('click', function (event) {
            if (is_login) {
                event.stopPropagation();
                var ths = $(this);
                var problem_id = ths.parent().attr('data-discuss-id');
                $.ajax({
                    url: '/home/s/ajax_praise/',
                    method: 'POST',
                    dataType: 'json',
                    data: {'problem_id': problem_id},
                    success: function (result) {
                        if (result['success']) {
                            var action = result['data']['action'];
                            var praise_count = result['data']['praise_count'];

                            if (action == 'mark') {
                                ths.addClass("selected");
                            } else if (action == 'cancel') {
                                ths.removeClass("selected");
                            }
                        } else {
                            if (result['code'] == 401) {
                                safe_login_popup('登录状态已过期！');
                                return false;
                            }
                        }
                    }
                });
            } else {
                safe_login_popup();
                return false;
            }
        });
    };
    // 点赞
    on_praise();

    // 给回复按钮绑定点击事件
    function on_reply() {
        $('.reply').off('click').on('click', function() {
            if (is_login) {
                var _dis = $(this).parent('.children_lower,.parent_lower').siblings('.children_reply,.parent_reply').css('display');
                if (_dis == 'none') {
                    $(this).parent('.children_lower,.parent_lower').siblings('.children_reply,.parent_reply').slideDown(300);
                } else {
                    $(this).parent('.children_lower,.parent_lower').siblings('.children_reply,.parent_reply').slideUp(300);
                }
                $(this).toggleClass('selected');
            } else {
                safe_login_popup();
            }
        });
    }
    on_reply();

    function btn_disabled(btn) {
        $(btn).attr("disabled", "disabled");
    }

    function btn_abled(btn) {
        $(btn).removeAttr('disabled');
    }

    function child_button_click() {
        // 提交回复评论
        var child_button = $('.button .submit');

        child_button.off('click').on('click', function () {
            btn_disabled(this);
            var parent_id = null,
                problem_id = null,
                answer_user_id = null,
                answer_nick_name = null,
                comment = $.trim($(this).parent().siblings('.input_area').children('textarea').val());
            // 回复问题
            if ($(this).parent().parent().hasClass('parent_reply')) {
                parent_id = $(this).parents('li').children('.last_id').val();
                problem_id = parent_id;
                //answer_user_id = $(this).parents('li').children('.answer_user_id').val();
                //answer_nick_name = $(this).parents('li').children('.answer_nick_name').val();
                answer_user_id = 0;
                answer_nick_name = '';
            } else {
                parent_id = $(this).parents('li').children('.last_id').val();
                problem_id = parent_id;
                answer_user_id = $(this).parents('._reply').siblings('.answer_user_id').val();
                answer_nick_name = $(this).parents('._reply').siblings('.answer_nick_name').val();
            }

            postAnswer(lesson_id, parent_id, problem_id, comment, answer_user_id, answer_nick_name, this);
        });
    }
    child_button_click();


    // 提交回答
    var postAnswer = function (object_id, _parent_id, _problem_id, _comment, _answer_user_id, _answer_nick_name, btn) {
        if(_comment == ''){
            layer.tips('请输入回复内容！', $(btn).parent().siblings('.input_area'), {
              tips: [1, '#5ECFBA'],
              time: 3000
            });
            btn_abled(btn);
        }else{
            $.ajax({
                url: '/common/answer_post_lps4/',
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
                        var cd = $(btn).parents('.parent_discuss').children('.children_discuss');
                        if (cd.css('display') == 'none') {
                            cd.show();
                        }
                        var html = $(data.html);
                        html.hide();
                        cd.append(html);
                        html.fadeIn();
                        $('html, body').animate({scrollTop:html.offset().top-get_roll_height()}, 1000);
                        $(btn).parent().siblings('.input_area').children('textarea').val('');
                        $(btn).parent().parent().prev().children('.reply').click();

                        reBindEvent();
                        btn_abled(btn);
                    }else{
                        layer.tips(data.msg, $(btn), {
                          tips: [1, '#5ECFBA'],
                          time: 3000
                        });
                    }
                    //answerBind();
                }
            });
        }
    };

    var more = $('.QA_more');
    // 加载更多
    function on_more() {
        more.text('加载更多↓');
        more.off('click').on('click', function () {
            var _ul = $('.QA_lists');
            var last_li = _ul.children('li').last();
            var last_id = $(last_li).find('.last_id').val();
            var object_id = lesson_id;

            var role = $('.my_join em').hasClass('actived') ? 'my' : 'all';
            loadMore(object_id, last_id, role, _ul);
        });
    }
    on_more();

    var loadMore = function (object_id, last_id, role, _ul) {
        if (is_login) {
            $.ajax({
                url: "/common/" + role + "_more_lps4/" + object_id + "/" + last_id + "/",
                dataType: "html",
                type: "GET",
                success: function (data) {
                    if ($.parseJSON(data)['status'] == 'failed') {
                        more.text('没有更多').off('click');
                    } else {
                        var html = $($.parseJSON(data)['html']);
                        html.hide();
                        _ul.append(html);
                        html.fadeIn();
                    }
                    $('.all-questions, .my-questions, .one-question-view').jScrollPane({
                        mouseWheelSpeed: 100
                    });
                    reBindEvent();
                }
            });
        } else {
            safe_login_popup();
            return false;
        }
    };

    // 取消回复评论
    function on_cancel() {
        $('.cancel').off('click').on('click', function() {
            $(this).parent('.button').parent('.children_reply,.parent_reply').slideUp(300);
            $(this).parent('.button').parent('.children_reply,.parent_reply').siblings('.children_lower,.parent_lower').children('.reply').removeClass('selected');
        });
    }
    on_cancel();

    // 切换最新问答，查看全部或只看自己参与的
    $('.my_join>em').off('click').on('click', function() {
        if (!is_login) {
            safe_login_popup();
            return false;
        }

        $(this).toggleClass('actived');

        var is_me = $(this).hasClass('actived');
        var _ul = $('.QA_lists');
        var object_id = lesson_id;

        if (is_me) {
            if ($(_ul).children().length == 0) {
                switch_empty_img('my');
            } else {
                switchRole(object_id, 'my', _ul);
            }
        } else {
            switchRole(object_id, 'all', _ul);
        }
        on_more();
    });

    var switchRole = function (object_id, role, _ul) {
        if (is_login) {
            $.ajax({
                url: "/common/" + role + "_more_lps4/" + object_id + "/0/",
                dataType: "html",
                type: "GET",
                success: function (data) {
                    if ($.parseJSON(data)['status'] == 'failed') {
                        empty_qa(role);
                    } else {
                        var html = $($.parseJSON(data)['html']);
                        if ($.trim($.parseJSON(data)['html']) == '') {
                            empty_qa(role);
                        } else {
                            clear_empty_qa();
                            html.hide();
                            _ul.html(html);
                            html.fadeIn();
                        }
                    }
                    $('.all-questions, .my-questions, .one-question-view').jScrollPane({
                        mouseWheelSpeed: 100
                    });
                    reBindEvent();
                }
            });
        } else {
            safe_login_popup();
            return false;
        }
    };

    function empty_qa(role) {
        $('.QA_lists, .QA_more').hide();
        if ($('.newest_QA .empty_qa').length > 0) {
            switch_empty_img(role);
        } else {
            if (role == 'all') {
                $('.newest_QA').append('<div class="empty empty_qa"><img src="/images/video_play/empty_QA.png"></div>');
            } else {
                $('.newest_QA').append('<div class="empty empty_qa"><img src="/images/video_play/empty_QA_me.png"></div>');
            }
        }
    }

    function clear_empty_qa() {
        $('.QA_lists').show();
        $('.QA_more').show();
        $('.newest_QA .empty_qa').remove();
    }

    function switch_empty_img(role) {
        if (role == 'all') {
            $('.newest_QA .empty_qa img').attr('src', '/images/video_play/empty_QA.png');
        } else {
            $('.newest_QA .empty_qa img').attr('src', '/images/video_play/empty_QA_me.png');
        }
    }

    // 获取img图片的高、宽
    $('.img_mc1>.ckdt').css({
        'width': function(index, value) {
            var img = new Image();
            img.src = $(this).siblings('img').attr('src');
            var img_width = img.width;
            var div_width = ($(this).parent().parent().parent('.txt_img').css('max-width')).split('px')[0];
            if (img_width > div_width) {
                return div_width;
            } else {
                return img.width;
            }

        },
        'height': function(index, value) {
            var img = new Image();
            img.src = $(this).siblings('img').attr('src');
            var img_height = img.height;
            var div_height = ($(this).parent().parent().parent('.txt_img').css('max-height')).split('px')[0];
            if (img_height > div_height) {
                return div_height;
            } else {
                return img_height;
            }
        },
        'padding-top': function(index, value) {
            var img = new Image();
            img.src = $(this).siblings('img').attr('src');
            var img_height = img.height;
            var div_height = ($(this).parent().parent().parent('.txt_img').css('max-height')).split('px')[0];
            if (img_height > div_height) {
                return (div_height - 24) / 2;
            } else {
                return (img_height - 24) / 2;
            }
        }
    });
    // 提问输入框获得焦点
    comment_input.off('focus').on('focus', function() {
        if(!is_login) {
            safe_login_popup();
            return false;
        }
        $(this).parent('.message_wrap').addClass('actived');
    });
    // 提问输入框失去焦点
    comment_input.off('blur').on('blur', function() {
        $(this).parent('.message_wrap').removeClass('actived');
    });
    // 显示更多的课程导师介绍
    $('.show_more').off('click').on('click', function() {
        var _text = $(this).text();
        var tea_info_txt = $('.tea_intro').children('p').height();
        if (_text == '收起↑') {
            $(this).siblings('.tea_intro').animate({
                'max-height': '72px'
            }, 500);
            setTimeout("$('.show_more').text('展示全部↓')",600);
        } else {
            $(this).siblings('.tea_intro').animate({
                'max-height': '216px'
            }, 500);
            $(this).text('收起↑');
        }
    });

    // 视频章节数和导师信息高度自适应
    // change_height();
    // function change_height(){
    //     $('.course_teacher').removeAttr('style');
    //     $('.catalog').removeAttr('style');
    //     $('.zyNewVideo_main').removeAttr('style');
    //     var video_height = $('.zyNewVideo_main').height();
    //     var tea_height = $('.course_teacher').height();
    //     if(tea_height > video_height){
    //         $('.catalog').height(tea_height);
    //         $('.video').css({'min-height': tea_height});
    //     }else{
    //         $('.catalog').height(video_height);
    //     }
    // }
    // // 改变窗体大小
    // $(window).resize(function(e){
    //     change_height();
    // });

    var next_btn = $('.next');
    var prev_btn = $('.prev');
    function next_click(roll_num) {
        var lesson_list = $('.lesson');
        var _move_height = $('.video').height() - next_btn.height() - prev_btn.height();
        var ul_margin_top = parseInt(lesson_list.children('ul').css('margin-top').split('px')[0]);
        var last_margin_top = lesson_list.children('ul').children('li').eq(-1).position().top;
        prev_btn.removeAttr('title');
        if (last_margin_top < _move_height) {
            next_btn.attr('title','这已是最后一页');
        } else {
        	next_btn.removeAttr('title');
            ul_margin_top -= _move_height;
            ul_margin_top = ul_margin_top * roll_num + 'px';
            lesson_list.children('ul').animate({
                'margin-top': ul_margin_top
            }, 500);
        }
    }
    // 单击视频列表下一页
    next_btn.off('click').on('click', function() {next_click(1)});
    // 单击视频列表上一页
    prev_btn.off('click').on('click', function() {
        var _move_height = $('.video').height() - next_btn.height() - prev_btn.height();
        var ul_margin_top = parseInt($(this).siblings('.lesson').children('ul').css('margin-top').split('px')[0]);
        var first_margin_top = $(this).siblings('.lesson').children('ul').children('li').eq(0).position().top;
        next_btn.removeAttr('title');
        if (40 <= first_margin_top) {
            $(this).attr('title','这已是第一页');
        }else if(-_move_height<=first_margin_top && first_margin_top<40){ 
             $(this).siblings('.lesson').children('ul').animate({
                'margin-top': 0
            }, 500);
        }else {
        	$(this).removeAttr('title');
            ul_margin_top += _move_height;
            ul_margin_top = ul_margin_top + 'px';
            $(this).siblings('.lesson').children('ul').animate({
                'margin-top': ul_margin_top
            }, 500);
        }
    });
    // 每个视频hover效果
    $('.catalog ul li a,.catalog ul li span').hover(function() {
        var tagName = $(this).prop('tagName');
        if (tagName == 'A') {
            var top = $(this).parent('li').position().top - 5;
        } else {
            var top = $(this).parent('li').position().top + 7;
        }
        var top = top + 'px';
        var text = $(this).attr('name');
        $(this).parent('li').parent('ul').siblings('.title').css({
            'top': top,'display':'table'
        }).children('span').text(text);
    }, function() {
        $(this).parent('li').parent('ul').siblings('.title').hide();
    });

    $('.kj a').on('click', function () {
       if (!is_login) {
           safe_login_popup();
       }
    });

    $('.lesson li').each(function (index) {
        if ($(this).children().hasClass('selected')) {
            var roll_num = Math.ceil(index/13.0-1);
            if (roll_num > 0) {
                next_click(roll_num);
            }
        }
    });

    //
    $('.tea_intro').jScrollPane({
        mouseWheelSpeed: 100
    });

    var p_ids = window.location.search.match(/p_id=([^&]+)/);
    if (p_ids) {
        var pid = p_ids[1];
        var cur = $('#'+pid);
        if (cur.length > 0) {
            setTimeout(function () {
                $('html, body').animate({scrollTop: cur.offset().top - get_roll_height()}, 1000);
            }, 500);
            cur.css({
                'background': '#FCFFC2',
                'transition': 'background-color 2s ease-in-out',
                '-moz-transition': 'background-color 2s ease-in-out',
                '-webkit-transition': 'background-color 2s ease-in-out',
                '-o-transition': 'background-color 2s ease-in-out'
            });
            setTimeout(function () {
                cur.css({background: '#FFFFFF'});
            }, 2000);
        }
    }

});