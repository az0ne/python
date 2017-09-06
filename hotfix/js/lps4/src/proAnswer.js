define(function(require, exports, module){
    /*
     * @ 点击展开详情
     *
     */
    $('.show-detail').click(function(){        
        if($(this).text() == '展开详情'){
            $('.pro-info').slideDown(500);
            $(this).text('收起详细');
        }else{
            $('.pro-info').slideUp(500);
            $(this).text('展开详情');
        }        
    });

    /*
     * @ 选项卡切换
     *
     */    
    var tab = require('./main.js').tab;
    var firstHash = window.location.hash.substring(1) || $('#show_current_stage').val();
    var tabNav = $('.tab-nav > li');
    var tabBox = $('.tab-box > li');
    window.bBtn = true;

    window.onhashchange = function(){
        if(window.bBtn){
            window.location.reload();
        }
    };
    if(!isNaN(firstHash) && firstHash < tabNav.length + 1){
        switch(firstHash){
            case firstHash:
                tabNav.eq(firstHash - 1).addClass('active').siblings().removeClass('active');
                tabBox.eq(firstHash - 1).show().siblings().hide();
                break;
        }
    }else{
        tabNav.eq(0).addClass('active').siblings().removeClass('active');
        tabBox.eq(0).show().siblings().hide();
    }

    tabNav.click(function(){
        var hash = $(this).attr('data-hash');
        window.location.hash = hash;
        window.bBtn = false;
        $(this).addClass('active').siblings().removeClass('active');
        var index = tabNav.index(this);
        tabBox.eq(index).show().siblings().hide();
        zhuge.track('点击选项卡', {'选项卡名称': $(this).text(),'按钮位置':'选项卡'});
    });

    /*
     * @ 班会答疑倒计时
     *
     */
    var cutTimer = require('./main.js').cutTimer;
    var Last = $('.answer .three').attr('countdown');
    var intTime1 = parseInt(Last);

    cutTimer(intTime1,'.answer ');    

    /*
     * @ 项目破冰倒计时
     *
     */    
    var First = $('.start .three').attr('countdown');
    var intTime2 = parseInt(First);
    cutTimer(intTime2);
    
    cutTimer(intTime2,'.start ');
    

    /*
     * @ 答疑提问
     *
     */
    var myFn0;
    $('.tiwen.out').bind('click', myFn0 = function(){
        var _this = $(this);

        $(this).unbind('click', myFn0);
        $('.quiz .hover-tips').stop(true).animate({
            'bottom': '-50px',
            'opacity': 1
        }, 300);
        (function(that){
            setTimeout(function(){
            $('.quiz .hover-tips').stop(true).animate({
                'bottom': '-55px',
                'opacity': 0
            }, 2000);
            $(that).bind('click', myFn0);
        }, 2000);
        })(_this);
    });

    /*
     * @ 满意度调查弹窗
     *
     */
    $('.show-remark').click(function () {
        $.ajax({
            type: "GET",
            url: $("#questionnaire_url").val(),
            dataType: 'json',
            success: function (data) {
                if (data.success == true) {
                    $('.show-remark').hide();
                    $('.teacher-remark').append('<p class="remark-con font14 color66">' + $('#user_task_info_remark').val() + '</p>');
                    $('.remark-con').css('display', 'block');
                } else {
                    var q_arr = {};
                    $("#satisfy-examen").html(data.data.html).modal({
                        show: true,
                        keyboard: false,
                        backdrop: 'static'
                    });
                    $('.satisfy-list li').each(function () {
                        $(this).find('.last label').click(function () {
                            $(this).parent().parent().addClass('now').siblings().removeClass('now');
                            $(this).addClass('select').siblings().removeClass('select');
                            var id = $(this).parent().attr('id');
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
                                        window.location.reload();
                                    } else if (data['msg'] == 'fail') {
                                        $('.modal-content .err_msg').text(data['data']).show().fadeOut(
                                            3000, window.location.reload()
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
    });
    $('#satisfy-examen').on({
        'click': function () {
            $('#satisfy-examen').modal('hide');
        }
    }, '.next-time');

    /*
     * @ 下载源码
     *
     */
    var myFn1;
    $('.down-source.not').bind('click', myFn1 = function(){
        var _this = $(this);

        $(this).unbind('click', myFn1);
        $('.student-data .hover-tips').stop(true).animate({
            'left': '15px',
            'opacity': 1
        }, 300);
        (function(that){
            setTimeout(function(){
                $('.student-data .hover-tips').stop(true).animate({
                    'left': '20px',
                    'opacity': 0
                }, 2000);
                $(that).bind('click', myFn1);
            }, 2000);
        })(_this);
    });
    /*
     * @ 项目进阶点击提示不跳转
     *
     */
    var myFn2;
    $('.lesson-list li .not').each(function(){        
        $(this).bind('click', myFn2 = function(){
            var _this = $(this);

            $(this).unbind('click', myFn2);
            $('.notice-content').stop(true).animate({
                'height': '40px',
                'margin-bottom': '10px'
            }, 300);
            (function(that){
                setTimeout(function(){
                    $('.notice-content').stop(true).animate({
                        'height': 0,
                        'margin-bottom': 0
                    }, 1000);
                    $(that).bind('click', myFn2);
                }, 1200);
            })(_this);
            
        });
    });
    /*
     * 学习资料点击提示不跳转
     *
     */
    $('.study-list li .not').each(function(){
        $(this).click(function(){
            $('.study-data .hover-tips').stop(true).animate({
                'left': '15px',
                'opacity': 1
            }, 300);
            setTimeout(function(){
                $('.study-data .hover-tips').stop(true).animate({
                    'left': '35px',
                    'opacity': 0
                }, 600);
            }, 1000);
        });
    });
});