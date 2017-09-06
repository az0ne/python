define(function(require, exports, module) {
var winWidth,winHeight;
function findDimensions() //函数：获取尺寸
{
	//获取窗口宽度	
	if(window.innerWidth)	
		winWidth = window.innerWidth;	
	else if ((document.body) && (document.body.clientWidth))
		winWidth = document.body.clientWidth;	
	//获取窗口高度	
	if (window.innerHeight)	
		winHeight = window.innerHeight;	
	else if ((document.body) && (document.body.clientHeight))	
		winHeight = document.body.clientHeight;	
	//通过深入Document内部对body进行检测，获取窗口大小	
	if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth)
	{
		winHeight = document.documentElement.clientHeight;	
	}
	var stObj=document.getElementById("section1");
	(stObj)&&(stObj.style.height=winHeight-64+"px");
	var vbg=document.getElementById("videobg");
	if(stObj&&vbg){
		if(winWidth/(winHeight-64)<1920/1080){vbg.style.height=winHeight+"px";
			var wwg=(winHeight-64)*(1920/1080);
			vbg.style.width=wwg+"px";
			vbg.style.left=-(wwg-winWidth)/2+"px";vbg.style.top="0px";
		}
		else{
			var hhg=winWidth*(1080/1920);
			vbg.style.height=hhg+"px";
			vbg.style.width="100%";
			vbg.style.left="0px";vbg.style.top=-(hhg-winHeight+64)/2+"px";
		}
	}
}
findDimensions();
/***
*banner切换
* Version:V1.0.0.0
* author：ZhouYi
* */
;(function($){
	var defaults = {
		model:"overlying"
		,"adaptiveHeightSpeed":500
		,"startSlide":0
		,onSliderLoad:function(){}
		,onSlideBefore:function(){}
		,onSlideAfter:function(){}
		,onSlideNext:function(){}
		,onSlidePrev:function(){}
	}
	$.fn.superposition=function(options){
		if(this.length == 0) return this;
		if(this.length > 1){
			this.each(function(){$(this).superposition(options)});
			return this;
		}

		var slider = {};
		var el = this;

		var windowWidth = $(window).width();
		var windowHeight = $(window).height();
		var childNum=el.children().length;

		var init=function(){
			slider.settings = $.extend({}, defaults, options);
			slider.viewport=$(el);
			slider.oldIndex=slider.settings.startSlide;
			el.css({"position":"relative","overflow":"hidden"})
			var childEle=el.children();
			childEle.each(function(ele,i){
				$(this).css({"position":"absolute","top":"0","left":"0","z-index":1});
			});
			childEle.eq(0).css("z-index","2");
			overlyingLoad();
			slider.settings.onSliderLoad(slider.oldIndex);
			$(window).bind('resize',resizeWindow);
		}
		el.goToSlideN=function(slideIndex){
			goToSlide(slideIndex,"next");
		}
		el.goToSlideNnext=function(){
			goToSlide(slider.oldIndex+1,"next");
		}
		el.goToSlideNprev=function(){
			goToSlide(slider.oldIndex-1,"prev");
		}
		//---------------FUNTION------------------
		var goToSlide=function(slideIndex, direction){
			if(slider.oldIndex==slideIndex){return;}
			if(slideIndex>=childNum){slideIndex=0}
			else if(slideIndex<0){slideIndex=childNum-1}
			var sObj=slider.viewport.children().eq(slideIndex);
			slider.settings.onSlideBefore(sObj,slider.oldIndex,slideIndex);
			if(direction=="next"){
				slider.settings.onSlideNext(sObj,slider.oldIndex,slideIndex);
			}else if(direction=="prev"){
				slider.settings.onSlidePrev(sObj,slider.oldIndex,slideIndex);
			}
			slider.viewport.children().css({"z-index":1}).eq(slider.oldIndex).css({"z-index":2});
			sObj.css({"top":el.height()+"px","z-index":3}).stop().animate({"top":"0"},slider.settings.adaptiveHeightSpeed,function(){
				slider.settings.onSlideAfter(sObj,slider.oldIndex,slideIndex);
			});
			slider.oldIndex=slideIndex;
		}
		var overlyingLoad=function(){
			var sObj=slider.viewport.children().eq(slider.settings.startSlide);
			sObj.css({"z-index":3});
			loadImage(sObj.children("img").attr("src"),function(){
				$(el).height($(el).width()*(this.height/this.width));
				slider.vImg=this;
			});
		}
		var resizeWindow=function(e){
			$(el).height($(el).width()*(slider.vImg.height/slider.vImg.width));
		}
		var loadImage=function(url, callb){
			var img = new Image();
			img.src = url;
			if(img.complete){
				callb.call(img);
				return;
			}
			img.onload=function(){
				callb.call(img);//将回调函数的this替换为Image对象
			};
		};
		init();
		//返回jQuery对象
		return this;
	}
})(jQuery)
	var th,player,player2,topbo=true;
	require('./videojs');require('./bxslider.js')($);
	var dd=require('dynamics');
	
	//-------------FUNTION-----------------.
	function newCouse(t){
		th=t;init();
	}
	var bxslider2;
	function section5_bottomAGO(){
		var n=parseInt($(this).attr("n"));
		$(".teacherVideoClose").attr("n",n);
		bxslider2.goToSlideN(n);
		$(this).addClass("aH").siblings().removeClass("aH");
		$(".section5_bottom").removeClass("lookVideo")
		$(".teacherVideo").fadeOut();
		player2.pause();
	};
	function slideDiv(obj){
		$(".section5 .div>p").eq(0).html(obj.attr("pt"));
		$(".section5 .div>p").eq(1).html(obj.attr("en"));
		$(".section5 .div>p").eq(2).html(obj.attr("pc"));
		$(".section5 .div>p").eq(3).attr("hp",obj.attr("hp"));
	};
	var SliderLoad=function(currentIndex){
		$(".bxslider>li").eq(currentIndex).children("div").removeClass("moveLeft")
	};
	var SlideAfter=function($slideElement, oldIndex, newIndex){
		$slideElement.children("div").removeClass("moveLeft");
		setTimeout(function(){$slideElement.parent().children().eq(oldIndex).children("div").addClass("moveLeft")},1000);			
	};
	function SlideAfter2($slideElement, oldIndex, newIndex){
		slideDiv($slideElement)			
	};
	function SliderLoad2(currentIndex){
		slideDiv($(".bxslider2>li").eq(0));
	};
	var player,player2;
	function closeEvent(){//关闭播放窗口
		player.pause();
		$('#VideoDemo').modal('hide');
	};
	function closeEventING(){//关闭播放窗口的事件
		player.pause();
	};
	function closeEvent(){//关闭播放窗口
		player.pause();
		$('#VideoDemo').modal('hide');
	}
	function closeEventING(){//关闭播放窗口的事件
		player.pause();
	}
	//菜单循环
	var setTime1;
	function newCousebox2_menuGO(){
		if(topbo){
			var li=$(".newCousebox2_menu li");
			if(li.hasClass("liH")){
				var lih=$(".newCousebox2_menu li.liH");			
				if($(".newCousebox2_menu li.liH").next().length>0){
					lih.removeClass("liH").next().addClass("liH");
				}
				else{
					li.removeClass("liH").eq(0).addClass("liH")
				}
			}
			else{
				li.eq(0).addClass("liH");
			}
		}
		setTime1=dynamics.setTimeout(newCousebox2_menuGO,3000);
	}
	//动画
	function animateGO(){
		$("#svg2 circle").attr("stroke-dasharray","848 848");
		var ciecleArr=$("#svg1 circle");
		ciecleArr.eq(0).attr("stroke-dasharray","5 5");
		ciecleArr.eq(1).attr("stroke-dasharray","1099 1099");		
		ciecleArr.eq(2).attr("stroke-dasharray","917 917");
		var gcircle=$("#svg1 .g circle");
		var gtext=$("#svg1 .g text");
		
		dynamics.setTimeout(function(){gcircle.eq(0).attr("r",5);},1000);
		dynamics.setTimeout(function(){gcircle.eq(1).attr("r",5);},1100);
		dynamics.setTimeout(function(){gcircle.eq(2).attr("r",5);},1200);
		dynamics.setTimeout(function(){gtext.eq(0).css("opacity",1);},1000);
		dynamics.setTimeout(function(){gtext.eq(1).css("opacity",1);},1000);
		dynamics.setTimeout(function(){gtext.eq(2).css("opacity",1);},1000);
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){

		//初始化videojs		
		videojs.options.flash.swf = "js/lib/v/video-js.swf";
		//走马灯
		var speed=30; //数字越大速度越慢
		var tab=document.getElementById("raffle_boxR_gun");
		var tab1=document.getElementById("ul1");
		var tab2=document.getElementById("ul2");
		tab2.innerHTML=tab1.innerHTML; //克隆demo1为demo2
		function Marquee(){
			if((tab2.offsetTop-tab.offsetTop)-tab.scrollTop<=0){//当滚动至demo1与demo2交界时
				tab.scrollTop-=tab1.offsetHeight; //demo跳到最顶端
			}
			else{
				tab.scrollTop++;
			}
		}
		var MyMar=setInterval(Marquee,speed);
		tab.onmouseover=function() {clearInterval(MyMar)};//鼠标移上时清除定时器达到滚动停止的目的
		tab.onmouseout=function() {MyMar=setInterval(Marquee,speed)};//鼠标移开时重设定时
		
		window.onresize=function(){findDimensions();}
		//video
		player = videojs("microohvideo", {
			controls: true,
			playbackRates: [1, 1.25, 1.5, 2]
		});
		player2 = videojs("microohvideo2", {
			controls: true,
			playbackRates: [1, 1.25, 1.5, 2]
		});
		$('.bxslider').bxSlider({
			"mode":"fade",
			"onSlideAfter":SlideAfter,
			"onSliderLoad":SliderLoad
		});
		$(window).keyup(function(e){
			if(e.keyCode==32) {
				if(player2.isFullScreen()) {
					player2.paused()?player2.play():player2.pause();
				}
				if(player.isFullScreen()) {
					$("#microohvideo").focus();
					player.paused()?player.play():player.pause();
				}
			}
		});
		player2.on("fullscreenchange",function(e){ //videojs事件
		});
		//头像切换
		bxslider2=$(".bxslider2").superposition({
			"mode":"overlying"
			,"onSlideAfter":SlideAfter2
			,"onSliderLoad":SliderLoad2
		});
		$(".section5_bottom a").click(section5_bottomAGO);
		//弹出视频播放
		$(".videoArrow").unbind().click(function(){
			th.openVideo2($(this).parent().attr("hp"));
			$(".section5_bottom").addClass("lookVideo");player2.play();
		});
		$(".jobs_list li > div .p2 a").unbind().click(function(){th.openVideo($(this).attr("pt"));player.play();});
		//关闭播放
		$(".zy_VideoDemo .close").unbind().click(closeEvent);
		$('#VideoDemo').on('hide.bs.modal', closeEventING);
		$(".teacherVideoClose").click(section5_bottomAGO);
		
		//菜单事件
		//newCousebox2_menuGO();
		$(".newCousebox2_menu").hover(function(e){
			dynamics.clearTimeout(setTime1);
		},function(e){		
			//setTime1=dynamics.setTimeout(newCousebox2_menuGO,1000);
			if(!topbo) return;
			$(this).children("li").removeClass("liold liC");
			
		});
		$(".newCousebox2_menu li").click(function(){			
			if(!topbo){
				$(this).addClass("click").siblings().removeClass("click");
			}	
			else{
				$(this).addClass("liC").siblings().removeClass("liC");
				$(this).parent().children(".liH").addClass("liold");
			}		
		});			
		$(".newCousebox2_con a").click(function(){
			$(".newCousebox2_con").hide();
			$(".newCousebox2_conTwo").show();
			dynamics.setTimeout(function(){$(".newCousebox2_conTwo .g1").removeClass("downGO");},200);
			dynamics.setTimeout(function(){$(".newCousebox2_conTwo .g2").removeClass("downGO");},600);
			dynamics.setTimeout(animateGO,1200);
		});		
		$(window).scroll(function(){
			if($(this).scrollTop()>=$(window).height()){
				$(".newCousebox2_menu").addClass("Ceiling");topbo=false;
				$(".newCousebox2_menu li").removeClass("click");
				if($(".newCousebox2_menu li.liH").length>0){
					$(".newCousebox2_menu li.liH").addClass("liold");
				}
				$(".newCousebox2_menu li>.div2").hide();
				dynamics.setTimeout(function(){$(".newCousebox2_menu li>.div2").show();},600);
			}
			else{
				$(".newCousebox2_menu").removeClass("Ceiling");topbo=true;
				$(".newCousebox2_menu li").removeClass("liold");
			}
		});
		
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
	}		
	
	module.exports = {
		"init":newCouse
	};
	
})