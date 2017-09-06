$(function() {
	var login_popup, eleArr, teaStates, handler;

    //最小高度
    minHeight();
    function minHeight(){
        $(".main-center").css('min-height',$(window).height()-252);
    }

    function is_login() {
        return $('.topRight').attr('login') == 'True';
    }

    //点赞
    function interlocutionParised(){
        var spans = $('.lps4_stu_ques_ans .interact .like');
        spans.unbind();
        spans.each(function () {
            $(this).click(function (event) {
                //$(this).addClass("parised");
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
                    topRightLogin();
                    return false;
                }
            });
        })
    }
    function addonclick(){
         $('#main>div.cur .list>ul>li').click(function(){
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

    //初始化
    interlocutionParised();
    addonclick();
    stopthebubble();

    //定义TAB位置
    var teaState = $(".personalInterlocutionTeaState>span.aH").index();
    teaStates = new Array();
    $(".personalInterlocutionTeaState>span").each(function(){
        teaStates.push(teaState);
    });

    //筛选
    $(".personalInterlocutionTeaState span").click(function(){
        $(this).addClass("aH").siblings().removeClass("aH");
        teaStates[$(".tab-nav li.select").index()] = $(this).index();//记录当前子页签位
        $('.lps4_stu_ques_ans .content>div.cur').empty();
        ajax_html(true);//重新加载
    });
    $(".tab-nav li").on('click',function(){
        $(this).addClass('select').siblings().removeClass('select');
        $(".lps4_stu_ques_ans .content>div").eq($(this).index()).addClass("cur").siblings().removeClass("cur");
        //改变当前子页签位置
        $(".personalInterlocutionTeaState>span").eq(teaStates[$(this).index()]).addClass("aH").siblings().removeClass("aH");
        //当鼠标点击TAB标签切换时布局
        oUlLayout();
        addonclick();
    });

    //绑定scroll事件
    function docScroll(){
        //是否到底部（这里是判断离底部还有100px开始载入数据）.
        var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
        if(closeToBottom) {
            ajax_html(false);//追加数据
        }
    }
    $(document).scroll(docScroll);

    //页面加载时第一次布局
    $(window).resize(function() {
        oUlLayout();
        minHeight();
    });
    oUlLayout();
    //定义基本属性--瀑布流
    function oUlLayout(){
        var listLenth = $("#main div.cur .list").length;
        for(var i=0;i<listLenth;i++){
           handler = $('#main>div.cur .list').eq(i).children("ul").children("li");
           handler.wookmark({
                align:'left',
                autoResize: true,
                container: $('#main div.cur .list'),
                offset: 20,
                itemWidth: 420
           },i);
        }
    }

    function ajax_html(flagsEmpty){
        //这里就是AJAX载入的数据
        var ajaxUrl = $(".tab-nav li.select a").attr("url");
        var end_id = $('#main>div.cur .list>ul>li:last').attr("discuss_id");
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
                    $('#main>div.cur').html('');
                    $('#main>div.cur .list>ul').html(html);
                }else{
                    //把新数据追加到对象中
                    $('#main>div.cur .list>ul').append(html);
                }
                //创建新的wookmark对象
                oUlLayout();
                //点赞
                interlocutionParised();
                addonclick();
                stopthebubble();
                //点赞
                interlocutionParised();
            },
            complete:function(XMLHttpRequest, textStatus){
                $(document).on('scroll',docScroll);
            }
       });
    }
});