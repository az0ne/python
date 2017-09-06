define(function(require, exports, module) {
	var login_popup, eleArr, teaStates, handler;
    login_popup = require('./main').login_popup;
    require('/js/common/wookmark.js');

	function studentmyanswer(t){
		init();
	}

    function is_login() {
        return $('.topRight').attr('login') == 'True';
    }

    //点赞
    function interlocutionParised(){
        var spans = $('.personalInterlocutionQues .time .like');
        spans.unbind();
        spans.each(function () {
            $(this).click(function (event) {
                if (is_login()) {
                    event.stopPropagation();
                    var span = $(this);
                    var problem_id = span.attr('data-discuss-id');
                    $.ajax({
                        url: '/home/s/ajax_praise/',
                        method: 'POST',
                        dataType: 'json',
                        data: {'problem_id': problem_id},
                        success:function(result){
                            if (result['success']) {
                                var action = result['data']['action'];
                                var praise_count = result['data']['praise_count'];
                                if (action == 'mark') {
                                    span.html(praise_count);
                                    span.addClass("parised");
                                } else if (action == 'cancel') {
                                    span.html(praise_count);
                                    span.removeClass("parised");
                                }
                            } else {
                                if (result['code'] == 401) {
                                    login_popup('登录状态已过期！');
                                    return false;
                                }
                            }
                        }
                    });
                } else {
                    login_popup();
                    return false;
                }

            });
        })
    }
    //function personalCicoHover(){
    //    $(".personalInterlocutionQues .personalCico").hover(function() {
    //        layer.tips($(this).attr("title"), $(this), {
    //            tips: [1, "#333" ],
    //            time: 1000
    //        });
    //    }, function() {});
    //}
    function addonclick(){
         $('#main>div.cur>ul>li').click(function(){
             var p_id = $(this).attr("discuss_id");
             window.location.href = window.location+'?p_id='+p_id;
        });
    }
    // 阻止冒泡
    function stopthebubble(){
        eleArr = [$('.toUserCenter'),$('.interact'),$('.objectHref'),$('.answer .img'),$('.answerToUserCenter')];
        for(var i = 0;i<eleArr.length;i++){
            eleArr[i].on('click',function(event){
                event.stopPropagation();
            });
        }
    }

    //打开缓存
    $.ajaxSetup({
        cache: true
    });
    //定义子TAB（已读，未读，的最后位置）
    teaStates = null;
    handler = null;
    
    //定义基本属性--瀑布流
    var options = {
      autoResize: true,
      container: $('#main'),
      offset: 2,
      itemWidth: 420
    };

    function contentEmpty(status){
        var emptyHtml='';
        if (status==0 | status==-1){
            if ($(".teacherCenterMenu>a.aH").text()=='我的提问'){
                emptyHtml = '<div class="textC nulldata">'+
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>'+
                                '<p class="font22 color33 marginB10">我的提问记录空空</p>'+
                                '<p class="font14 color66">暂时还没有提出过疑问</p>'+
                                '<p class="font14 color66 marginB10">赶快去课程视频下提问吧</p>'+
                            '</div>'
            } else if ($(".teacherCenterMenu>a.aH").text()=='我的回答') {
                emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">我的回答记录空空</p>' +
                                '<p class="font14 color66">暂时还没有回答过问题</p>' +
                                '<p class="font14 color66 marginB10">赶快去课程视频下回答吧</p>' +
                            '</div>'
            } else if ($(".teacherCenterMenu>a.aH").text()=='TA的提问') {
                emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">TA的提问记录空空</p>' +
                                '<p class="font14 color66">TA暂时还没有提出过疑问</p>' +
                            '</div>'
            } else if ($(".teacherCenterMenu>a.aH").text()=='TA的问答') {
                emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">TA的回答记录空空</p>' +
                                '<p class="font14 color66">TA暂时还没有回答过问题</p>' +
                            '</div>'
            }else if ($(".teacherCenterMenu>a.aH").text()=='优质解答') {
                emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">优质解答记录空空</p>' +
                                '<p class="font14 color66">暂时还没有人向老师提问</p>' +
                                '<p class="font14 color66 marginB10">赶快去老师的课程下提问吧</p>' +
                            '</div>'
            }else{
                emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">记录空空</p>' +
                                '<p class="font14 color66">暂时还没有问答记录</p>' +
                            '</div>'
            }
        }else{
             emptyHtml = '<div class="textC nulldata">' +
                                '<p class="marginB29"><img src="/images/no_answer2.png"></p>' +
                                '<p class="font22 color33 marginB10">记录空空</p>' +
                                '<p class="font14 color66">暂时还没有问答记录</p>' +
                            '</div>'
        }
        return emptyHtml
    }

    //初始化
    var init = function(){
        interlocutionParised();
        //personalCicoHover();
        addonclick();
        stopthebubble();
        //定义子TAB位置
        var teaState = $(".personalInterlocutionTeaState>span.aH").index();
        teaStates = new Array();
        $(".personalInterlocutionTeaState>span").each(function(){
            teaStates.push(teaState);
        });

        //筛选
        $(".personalInterlocutionTeaState span").click(function(){
            $(this).addClass("aH").siblings().removeClass("aH");
            teaStates[$(".teacherCenterMenu>a.aH").index()] = $(this).index();//记录当前子页签位
            $('#main>div.cur>ul').empty();
            ajax_html(true);//重新加载
        });
        $(".teacherCenterMenu>a").click(function(){
            $(this).addClass("aH").siblings().removeClass("aH");
            $(".teacherCenterTabContent>div").eq($(this).index()).addClass("cur").siblings().removeClass("cur");
            //改变当前子页签位置
            $(".personalInterlocutionTeaState>span").eq(teaStates[$(this).index()]).addClass("aH").siblings().removeClass("aH");
            //当鼠标点击TAB标签切换时布局
            oUlLayout();
            //当鼠标点击TAB标签切换时获取ID值为1的日期/时间并显示在浮标上
            oDivTimeDisplay();
            addonclick();
        });

        //hover时显示“点赞”“分享”“回复”
        oLiHover();
        function oLiHover(){
            $(".personalInterlocutionQues>div>ul>li").hover(function(){
                $(this).find(".interact").show();
            },function(){
                $(this).find(".interact").hide();
            });
        }


        //绑定scroll事件
        function docScroll(){
            //随着滚动条的滚动，获取最右侧卡片的时间，并填充至右侧浮标上
            var interlocutionTeaState = $(".personalInterlocutionTeaState").height()+15;
            if(interlocutionTeaState == 15) interlocutionTeaState=-20;
            var oDivCurLis = $(".personalInterlocutionQues>div.cur>ul>li");
            oDivCurLis.each(function(){
                var oDivCurLisLeft = parseInt($(this).css("left"));
                if(oDivCurLisLeft == 440){
                    var oLisid = $(this).attr("data-wookmark-id"),//获取li的ID值
                        oDivCurLisTop = parseInt(oDivCurLis.eq(oLisid).css("top"))+interlocutionTeaState;
                    console.log($(window).scrollTop())
                    if($(window).scrollTop()>oDivCurLisTop){//当滚动条大于li的top值时
                        $(".personalInterlocutionCardTime strong").html(oDivCurLis.eq(oLisid).find(".time span").html());//日期
                        $(".personalInterlocutionCardTime em").html(oDivCurLis.eq(oLisid).find(".time em").html());//时间
                    }
                }
            });
            //是否到底部（这里是判断离底部还有100px开始载入数据）.
            var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
            if(closeToBottom) {
                ajax_html(false);//追加数据
            }
        }
        $(document).scroll(docScroll);

        //页面加载时第一次布局
        oUlLayout();
        function oUlLayout(){
            handler = $('#main>div.cur>ul');
            handler.wookmark(options);
        }

        //获取ID值为1的日期/时间并显示在浮标上
        oDivTimeDisplay();
        function oDivTimeDisplay(){
            var oDivCurLis = $(".personalInterlocutionQues>div.cur>ul>li");
            if (oDivCurLis.length>0){
                $(".personalInterlocutionCardTime").show();
            }else{
                $(".personalInterlocutionCardTime").hide();
            }
            var oDivCurLisTime = oDivCurLis.eq(1);
            $(".personalInterlocutionCardTime strong").html(oDivCurLisTime.find(".time span").html());
            $(".personalInterlocutionCardTime em").html(oDivCurLisTime.find(".time em").html());
        }

        function ajax_html(flagsEmpty){
            //这里就是AJAX载入的数据

            var ajaxUrl = $(".teacherCenterMenu>a.aH").attr("url");
            var end_id = $('#main>div.cur>ul>li:last').attr("discuss_id");
            var status = $(".personalInterlocutionTeaState>span.aH").index();
            var param = new Array();
            if (end_id){
                param.push('end_id='+end_id);
            }
            if (status){
                param.push('status='+status);
            }
            var str_param = param.join('&');

            $.ajax({
                url:ajaxUrl+'?'+str_param,
                dataType:"html",
                beforeSend:function(XMLHttpRequest){
                    $(document).off('scroll');
                },
                success:function(html){
                    //清空所有数据
                    if (flagsEmpty==true){
                        if (html.indexOf('div')<0){
                            $('#main>div.cur').html(contentEmpty(status));
                        }else{
                            $('#main>div.cur').html('<ul></ul>');
                            $('#main>div.cur>ul').html(html);
                        }
                    }else{
                        //把新数据追加到对象中
                        $('#main>div.cur>ul').append(html);
                    }
                    //创建新的wookmark对象
                    oUlLayout();
                    //点赞
                    interlocutionParised();
                    //personalCicoHover();
                    oDivTimeDisplay();
                    addonclick();
                    //hover时显示"点赞"/"分享"/"回复"
                    oLiHover();
                    stopthebubble();
                    //加载jiathis.js分享代码
                    //$.getScript("http://v3.jiathis.com/code/jia.js?uid=2055164");
                    interlocutionParised();
                },
                complete:function(XMLHttpRequest, textStatus){
                    $(document).on('scroll',docScroll);
                }
           });
        }
    };
	module.exports = {
		"init":studentmyanswer
	};
});