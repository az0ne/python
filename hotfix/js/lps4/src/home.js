define(function(require, exports, module) { 
	require("textFiltered")($);
	//-------------FUNTION-----------------.
	function sreachBtn(str){
        window.open("/course/list/?catagory="+str);
    }
    var init = {
        topSlider: function(){
            $(".banner-slider").css("backgroundImage","url("+$(".bxslider li").eq(0).children("a").attr("big")+")");

            $('.top-banner .bxslider').bxSlider({
                mode: 'horizontal',
                auto:true,
                hideControlOnEnd:true,
                onSlideBefore:function(slideElement, oldIndex, newIndex){
                    $(".banner-slider").css("backgroundImage","url("+slideElement.children("a").attr("big")+")");
                }
            });
        },

        goTop: function(){
            $(window).scroll(function() {
                if ($(window).scrollTop() > 100) {
                    $(".toolbar-item-gotop").fadeIn('fast');
                } else {
                    $(".toolbar-item-gotop").fadeOut('fast');
                }
            });
        },

        close: function(){
            $('.close-ad').on('click',function(){
                $('.float-ad').hide();
            });
        },

        nav: function(){
            var $liCur = $(".nav-menu>ul>li.active"),
                curP = $liCur.position().left,
                curW = $liCur.outerWidth(true),
                $slider = $(".nav-line"),
                $targetEle = $(".nav-menu>ul>li:not('.last')"),
                $navBox = $(".nav-menu");
            $slider.stop(true, true).animate({
                "left" : curP,
                "width" : curW
            });
            $targetEle.mouseenter(function () {
                var $_parent = $(this);//.parent(),
                _width = $_parent.outerWidth(true),
                posL = $_parent.position().left;
                $slider.stop(true, true).animate({
                    "left" : posL,
                    "width" : _width
                }, "fast");
            });
            $navBox.mouseleave(function (cur, wid) {
                cur = curP;
                wid = curW;
                $slider.stop(true, true).animate({
                    "left" : cur,
                    "width" : wid
                }, "fast");
            });
        },

        tabs: function(){
            $(".tab_item").eq(0).css({'color':'#5ecfba','font-weight':'blod'});
            $(".tab_item").mouseover(function() {

                var background = $(this).parent().find(".moving_bg");
                $(background).stop().animate({
                    left: $(this).position()['left']
                }, {
                    duration: 300
                });

                init.slideContent($(this));

            });
        },

        slideContent: function(obj) {
            var newobj;
            newobj = $(obj).parent().parent().parent();
            $(obj).css({'color':'#5ecfba','font-weight':'blod'});
            $(obj).prevAll().css({'color':'#333333','font-weight':'normal'});
            $(obj).nextAll().css({'color':'#333333','font-weight':'normal'});
            var margin = newobj.find(".slide_content").width();
            margin = margin * ($(obj).prevAll().size() - 1);
            margin = margin * -1;

            newobj.find(".tabslider").stop().animate({
                marginLeft: margin + "px"
            }, {
                duration: 300
            });
        },

        sliderControl: function(className){
            var LiWidth,LiNum;

            if($(className).attr('tag') == 1){
                LiWidth = 169;
                LiNum = 6;
            };

            if($(className).attr('tag') == 2){
                LiWidth = 264;
                LiNum = 4;
            };

            if($(className).attr('tag') == 3){
                LiWidth = 275;
                LiNum = 4;
            };

            $(className+' .bxslider').bxSlider({
                pager:false,
                slideWidth:LiWidth,
                auto:false,
                minSlides:1,
                maxSlides:LiNum,
                slideMargin:20
            });
        },

        kfServer: function(){
            var Txt = ['欢迎来到麦子学院','有什么疑问可以跟我聊聊','我是学习小助手，随时跟你在一起'];
            var num = 0;
			
            setInterval(function(){
                $('.kf-server').find('span').show().html(Txt[num]);
                setTimeout(function(){
                    $('.kf-server').find('span').hide();
                },5000);
                if(num < Txt.length){
                    num++;
                }else{
                    num = 0;
                };
            },10000);
        },

        verticalAlign: function(){
            var cacheModel = [];
            $(".modal").on("show.bs.modal", function(){
                for(var i = 0;i<cacheModel.length;i++){
                    if(cacheModel[i]){
                    cacheModel[i].modal('hide');
                    cacheModel[i] = null;
                    }
                }
                cacheModel.push($(this));
                var $this = $(this);
                if($this.find(".vam").length<=0) {
                    var $modal_dialog = $this.find(".modal-dialog");
                    var div = $('<div style="display:table; width:100%; height:100%;"></div>')
                    div.html('<div class="vam" style="vertical-align:middle; display:table-cell;"></div>');
                    div.children("div").html($modal_dialog);
                    $this.html(div);
                }
            });
        },

        indexSearch: function(){
            $("#data-search").textFiltered({
                "boEnter":true,
                "onkeyup":function(boolean){
                    var $th = this,bokey = false;
                    if(boolean){sreachBtn($th.val());return;}
                    $.ajax({
                        type: "GET",
                        url:"/homepage/get_course_category/",
                        data:{"s":$th.val()},
                        beforeSend:function(XMLHttpRequest){},
                        success: function(data1) {
                            $th.clear();
                            for(var i=0;i<data1.length;i++){
                                $th.addNode(data1[i],data1[i]);
                                if(data1[i]==$th.val()){$th.data("vv",data1[i]);bokey=true;}
                            }
                        },
                        complete: function(XMLHttpRequest){}
                    });
                    if(!bokey) $th.removeData("vv");
                }
                ,"height":180
                ,"onarrowupdown":function(i){}
                ,"onVclick":function(v){
                    this.data("vv",v);
                    if(v!="暂无数据") {
                        $("#data-search").val(v);
                        //sreachBtn(v);
                    }
                }
            });
        }
    }
	//------------FUNCTIONEND---------		
	require('./bxslider.js')($);
	init.topSlider();
	init.nav();
	init.tabs();
	init.goTop();
	init.close();
	init.kfServer();
	init.indexSearch();
	init.verticalAlign();
	init.sliderControl('.gmct');
	init.sliderControl('.media-reports');
	init.sliderControl('.cooperative-enterprise');
	init.sliderControl('.partner-schools');
	$(".search-btn").click(function(){
		sreachBtn($("#data-search").val());
	});
	//--------------------------诸葛io统计---------------------------------------------
	// 首页搜索事件
    function track_search() {
        var search_text = $('#data-search').val();
        zhuge.track("首页搜索事件", {
            "事件位置": "首页",
            "搜索关键词": search_text
        });
    }
    $('.search-btn').click(function() {
        track_search();
    });
    $("#data-search").keyup(function() {
        if (event.keyCode == 13){
            track_search();
        }
    });

    // 首页搜索框热点点击
    $('.hot-words>a').click(function () {
        var text = $(this).text();
        zhuge.track("首页搜索框热点点击", {
            "事件位置": "首页",
            "热点关键词": text
        });
    });

    // 首页焦点图点击
    $('.top-banner .bx-wrapper a').click(function () {
        var tag_a = this;
        var tag_img = this.firstChild;
        var url = tag_a.href;
        var img = tag_img.src;
        var alt = tag_img.alt;
        zhuge.track("首页焦点图点击", {
            "事件位置": "首页",
            "跳转url": url,
            "Banner": img,
            "Banner描述": alt
        });
    });

    // 首页导航栏点击
    $('.nav-menu>ul>li>a').click(function () {
        zhuge.track("首页导航栏点击", {
            "事件位置": "首页",
            "跳转url": $(this).attr('href'),
            "url描述": $(this).text()
        });
    });

    // 首页左边侧栏点击
    function track_leftbar(url, career, course) {
        zhuge.track("首页左边侧栏点击", {
            "事件位置": "首页",
            "跳转url": url,
            "课程方向": career,
            "课程关键字": course
        });
    }
    $('.nav-group .menulihover>a').click(function () {
        track_leftbar($(this).attr('href'), $(this).text(), '');
    });
    $('.nav-group .MenuLCinList>p>a').click(function () {
            var career = $(this).parent().siblings('h3').children().html();
            track_leftbar($(this).attr('href'), career, $(this).text());
    });

    // 首页登录
    $('#login_btn').click(function () {
        var account = $('#id_account_l').val();
        zhuge.track("首页登录", {
            "事件位置": "首页",
            "登录账号": account
        });
    });

    // 首页注册
    function track_regist(desc) {
        zhuge.track("首页注册", {
            "事件位置": "首页",
            "注册入口": desc
        });
    }
    $('.register-button').click(function () {
        track_regist('首页注册按钮');
    });
    $('#btnRegister').click(function () {
        track_regist('登录弹框->立即注册');
    });

    // 首页最新资讯点击
    $('.latest-news-module>ul>li>a').click(function () {
        zhuge.track("首页最新资讯点击", {
            "事件位置": "首页",
            "跳转url": $(this).attr('href'),
            "标题": $(this).text()
        });
    });

    // 首页直通班点击
    $('div.points-recommended a').click(function () {
        zhuge.track("首页直通班点击", {
            "事件位置": "首页",
            "直通班名称": $(this).eq($(this)).attr('alt'),
            "直通班链接": $(this).attr('href')
        });
    });

    // 首页诱导咨询点击
    $('ul.live-try-list a').click(function () {
        zhuge.track("首页诱导咨询点击", {
            "事件位置": "首页",
        });
    });

    // 首页分类课程点击
    $('.contant-left-bottom ul').each(function (index, element) {
        $(element).find('a').click(function () {
            var tab = $('.contant-center-top li').eq(index).text();
            var course_name = $(this).attr('title');
            zhuge.track("首页分类课程点击", {
                "事件位置": "首页",
                "所属tab": tab,
                "课程名": course_name
            });
        });
    });

    // 首页课程大纲点击
    function track_career(career_name) {
        zhuge.track("首页课程大纲点击", {
            "事件位置": "首页",
            "课程大纲名称": career_name
        });
    }
    $('div.career-path-list a').each(function (index, element) {
        if (index%2 == 0) { // li下的第一个a标签
            $(element).click(function () {
                track_career($(this).find('img').attr('alt'));
            });
        } else {    // li下的第二个a标签
            $(element).click(function () {
                track_career($(this).prev().text());
            });
        }
    });

    // 首页金牌讲师点击
    $('.gmct .bx-viewport>ul>li>a.a2').click(function () {
        zhuge.track("首页金牌讲师点击", {
            "事件位置": "首页",
            "老师名字": $(this).children('p').text()
        });
    });

    // 首页媒体报道点击
    $('.media-reports .bx-viewport a').click(function () {
        zhuge.track("首页媒体报道点击", {
            "事件位置": "首页",
            "媒体": $(this).children('img').attr('alt'),
            "报道链接": $(this).attr('href')
        });
    });

    // 首页合作企业点击
    $('.cooperative-enterprise .bx-viewport a').click(function () {
        zhuge.track("首页合作企业点击", {
            "事件位置": "首页",
            "企业": $(this).children('img').attr('alt'),
            "企业链接": $(this).attr('href')
        });
    });

    // 首页合作院校点击
    $('.partner-schools .bx-viewport a').click(function () {
        zhuge.track("首页合作院校点击", {
            "事件位置": "首页",
            "院校": $(this).children('img').attr('alt'),
            "院校链接": $(this).attr('href')
        });
    });
})