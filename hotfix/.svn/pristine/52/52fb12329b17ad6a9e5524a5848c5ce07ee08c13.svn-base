define(function(require, exports, module) { 
	require('PicCarousel')($);require('./bxslider.js')($);
	var bxslider2,scrollBO=true;
	//-------------FUNTION-----------------.
	function newCouseD(t){
		init();
	}
	function section5_bottomAGO(){
		var n=parseInt($(this).attr("n"))
		bxslider2.goToSlide(n);
		$(this).addClass("aH").siblings().removeClass("aH")
	}
	function slideDiv(obj){
		$(".section5 .div>p").eq(0).html(obj.attr("pt"));
		$(".section5 .div>p").eq(1).html(obj.attr("en"));
		$(".section5 .div>p").eq(2).html(obj.attr("pc"));
		$(".section5 .div>p").eq(3).attr("hp",obj.attr("hp"));
	}
	function SlideAfter2($slideElement, oldIndex, newIndex){
		slideDiv($slideElement)			
	}
	function SliderLoad2(currentIndex){
		slideDiv($(".bxslider2>li").eq(0));
	}
	var windowscroll=function(event){
		//窗口的高度+看不见的顶部的高度=屏幕低部距离最顶部的高度  
		var thisButtomTop = parseInt($(this).height()) + parseInt($(this).scrollTop());  
		var thisTop = parseInt($(this).scrollTop()); //屏幕顶部距离最顶部的高度  
		var PictureTop = parseInt($(".aboutlessonBox4").offset().top)+500;  
		if (PictureTop >= thisTop && PictureTop <= thisButtomTop &&scrollBO) {
			scrollBO=false;
			if(!$(".aboutlessonBox4").hasClass("original")) {
				if ($(".aboutlessonBox4 .poster-list").attr("ppt")) {
					$(".aboutlessonBox4Div").PicCarousel({
						"width": 1000,
						"height": 560,
						"posterWidth": 304,
						"posterHeight": 540,
						"scale": 0.8,
						"speed": 500,
						"autoPlay": false,
						"delay": 1000,
						"verticalAlign": "middle"
					});
				}
				else {
					$(".aboutlessonBox4Div").PicCarousel({
						"width": 1200,
						"height": 450,
						"posterWidth": 680,
						"posterHeight": 430,
						"scale": 0.9,
						"speed": 500,
						"autoPlay": false,
						"delay": 1000,
						"verticalAlign": "bottom"
					});
				}
			}
			else{
				$(".aBox4Div").addClass("HH");
			}
		}
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){	
		//头像切换
		bxslider2=$('.bxslider2').bxSlider({
			"mode":"horizontal",
			"pager":false,
			"controls":false,
			"onSlideAfter":SlideAfter2,
			"onSliderLoad":SliderLoad2,
			"infiniteLoop":false
		}); 
		$(".section5_bottom a").hover(section5_bottomAGO,function(){});
		$(window).bind("scroll", windowscroll);
		if(!$(".aboutlessonBox4 .poster-list").attr("ppt")) {
			$(".aboutlessonBox4 .poster-item").css({"marginLeft":"-329px","width":"658px"});
		}
		$(".section5 .div .videoArrow").unbind().click(function(){th.openVideo($(this).parent().attr("hp"));});
		$(".aboutlessonFoot > div > a").click(function(){
			var goID=$(this).attr("href");
			$('html,body').stop().animate({scrollTop: $(goID).offset().top+'px'}, 800);
			return false;
		});
		$(".footNewBox2").css("marginBottom","80px");
		/*
		 * @ 项目弹窗引导
		 *
		 */
		if($('#pm').val() == 'True'){
			$('#pop_pm2npm_window').modal({show:true, keyboard:false,backdrop: 'static'});
		}
	}		
	
	module.exports = {
		"init":newCouseD
	};
	//----------------诸葛io统计----------------------------------
	if(is_authenticated){
        $(".topRight .a").eq(1).click(function(){
            zhuge.track("登录", {
                "事件位置": "课程介绍页"
            });
        });
    }
    // 课程介绍页_搜索事件
    $('.topSreachTxt').keyup(function(){
        if (event.keyCode == 13){
            zhuge.track("搜索", {
                "事件位置": "课程介绍页",
                "搜索关键词": $(this).val()
            });
        }
    });

    //企业直通班点击事件
    $('.top_menu li').click(function(){
        zhuge.track("导航栏", {
            "事件位置": "课程介绍页",
            "导航栏名称": $(this).find('span').text()
        });
    });

    $('.top_menu_div a').click(function(event){
        event.stopPropagation();
        zhuge.track("企业直通班", {
            "事件位置": "课程介绍页",
            "课程": $(this).text()
        });
    });



    // 注册事件
    $(".topRight .a").eq(0).click(function(){
        zhuge.track("注册", {
            "事件位置": "课程介绍页"
        });
    });

    // 免费体验学习
    $('.aboutlessonBox1Btn a').click(function(){
        zhuge.track($(this).text(), {
            "事件位置": "课程介绍页"
        });
    });

    //查看免费视频教学
    $('.aLessonBtn').click(function(){
        zhuge.track($(this).text(), {
            "事件位置": "课程介绍页"
        });
    });

    //在线客服
    $('.toolbar a').eq(0).click(function(){
        zhuge.track("在线客服", {
            "事件位置": '课程介绍页'
        });
    });

    //在线通话
    $('.toolbar a').eq(1).click(function(){
        zhuge.track("课程介绍页_免费通话", {
            "事件位置": '课程介绍页'
        });
    });

    // 意见反馈
    $('.toolbar-item-fankui').click(function(){
        zhuge.track("意见反馈", {
            "事件位置": '课程介绍页'
        });
    });

    // 底部导航点击
    $('.aboutlessonFoot a,.aboutlessonFoot_a1,.aboutlessonFoot_a2').click(function(){
        zhuge.track($(this).text(), {
            "事件位置": "课程介绍页"
        });
    });
})