define(function(require, exports, module){
    var tab = require('./main.js').tab;
    var cutTimer = require('./main.js').cutTimer;   

    /*
     * @ 课程介绍、课程互动选项卡
     *
     */
    tab({
        tabNav: '.section_2 .tab_menu li',
        tabBox: '.section_2 .tab_box > div',
        select: 'active',
        type: 'show'
    })
    /* 
     * @ 倒计时
     * @ Day : 天数
     * @ intDiff : 倒计时总秒数量
     */
    var second = $('.time-item').attr('cutdown');
    var intDiff = parseInt(second);
    var timmer = 0;
    cutTimer(intDiff,'.time-item ');
    timmer = setInterval(function(){
        intDiff--;
        if(intDiff == 0){
            intDiff = 0;
            clearInterval(timmer);
            $('.section_1 .row_1').html('<p class="come">立刻进入试学吧</p>');
        }        
    },1000);

    /* 
     * @ 课程大纲
     * @
     */
    require('mousewheel');
    require('jscrollpane');
    if ($('.tab_nav .first i').length>0){
    var tabNav = $('.tab_nav li').not($(".line")); // 过滤直线
    var start = $('.tab_nav .first i').offset().left; // 第一个阶段位置
    var end = $('.tab_nav .last i').offset().left; // 最后一个阶段位置
    var color = ['#5ecfba','#5496d1','#76c583','#6951a1','#f48147','#5ecfba','#5496d1','#76c583','#6951a1','#f48147','#5ecfba','#5496d1','#76c583','#6951a1','#f48147','#5ecfba','#5496d1','#76c583','#6951a1','#f48147']; // 阶段位置颜色
    var oUl = $('.scroll_cards');
    var aLi = $('.cards > li');
    var oUlWidth = aLi.length * (aLi.outerWidth() + 20);
    oUl.css({'width': oUlWidth}); // 设置UL的宽度

    // 设置阶段直线
    $('.tab_nav .line').css({
        'width': (end - start) + 'px',
        'left': start + ($('.tab_nav .first i').width()/2)
    });

    tabNav.each(function(i){
        var index = tabNav.index(this);
        $(this).find('i').css({'background': color[i]});
        oUl.children('li').eq(index).find('ol > li').css({'background': color[index]});
         
    });

    $('.list_module .inner').jScrollPane({
        mouseWheelSpeed: 100
    });    
}
    /* 
     * @ 课程老师
     * 
     */
    tab({
        tabNav: '.user_nav li',
        tabBox: '.slider_lists > li',
        select: 'active',
        type: 'slide'
    });

    /*
     * @ 学员成功故事视频弹出层
     *
     */
    require('./videojs');
    videojs.options.flash.swf = "http://releases.flowplayer.org/swf/flowplayer-3.2.1.swf";
    var player = videojs("storyvideo", {
        "techOrder": ["html5","flash"],
        "children": {
            bigPlayButton : false,
            textTrackDisplay : false,
            posterImage: false,
            errorDisplay : false,
            controlBar : {
                captionsButton : false,
                chaptersButton: false,
                subtitlesButton:false,
                liveDisplay:false,
                playbackRateMenuButton:false
            }
        },
    });
    $('.video').click(function(){
        $('.video-warp').fadeIn();
        player.play();
    });
    $('.close-video').click(function(){
        player.pause();
        $('.video-warp').fadeOut();
    });
    player.on('ended',function(){
        $('.video-warp').fadeOut();
    });

    /* 
     * @ 学生作品展示
     *
     */
    require('./bxslider.js')($);
    $('.student_module .bxslider').bxSlider({
      mode: 'horizontal',
      auto: true,
      pagerType: 'short' //设置为数字显示
    });

    /* 
     * @ 学习该课程选项卡
     *
     */
    tab({
        tabNav: '.tab_module .tab_nav li',
        tabBox: '.tab_con > div',
        select: 'active',
        type: 'show'
    })

    /*
     * @ 底部免费试学
     *
     */
    
    $(window).scroll(function() {
        if ($(window).scrollTop() > 470) {
            $('.article_footer').css('marginBottom','70px');
            $(".section_4").slideDown(300);
        } else {
            $(".section_4").slideUp(300);
        }
    });

    /*
     * @ 免费试学弹窗
     *
     */
    
    var isFree = false // 是否免费
    if(isFree == true){
        $('#free-study').modal('show');
    }
    
    $('#free-study .close').click(function(){
        $('#free-study').modal('hide');
    });
    function verHeight() {
        var l = $(window).width();
        if((1600-l)>=0){
            var w = (80-(1600-l)/7.2) + 30;
            $(".course_introduce .section_1 .inner").css({"padding-top": w,"padding-bottom": w});
        }
        if(l<=1024){
            $(".course_introduce .section_1 .inner").css({"padding-top": 30,"padding-bottom": 30});
        }
    }
    verHeight();
    $(window).resize(function(){
        verHeight();
    })

    var isRegist = $('#user_center_course_record').val();// $('#');
		//模块弹出
		if(isRegist == 'true'){
			$("#interestCourse").modal('show');
		}

		var index = 0,oLis,oSpan;
			oLis = $("#interestCourse .modal-body li");
			oSpan = $("#interestCourse .modal-footer span");
		oSpan.click(function(){
			pages = parseInt((oLis.length-1)/6);//获取页数
			if(index < pages){
				index++;
			}else{
				index = 0;
			}
			//隐藏所以li,再显示需要显示的li
			oLis.hide().slice(6*index,6*(index+1)).fadeIn();
		});

		if(oLis.length<=6){
			oSpan.unbind("click");//当li个数小于等于6个时，取消点击事件
		};
});