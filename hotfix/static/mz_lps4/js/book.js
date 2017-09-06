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
Date.prototype.diff = function(date){
  return Math.floor(this.getTime() - date.getTime())/(24 * 60 * 60 * 1000);
}
Date.prototype.dimm = function(date){
	var bMonth=date.getFullYear()*12+date.getMonth();
	var eMonth=this.getFullYear()*12+this.getMonth();
  return Math.abs(eMonth-bMonth);
}


var Load = function(){
	var cacheModel=[];
	this.init = function(){
		$(".modal").on("show.bs.modal", function(){
			//$(".modal").modal('hide');
//			if($(".modal-backdrop").length>0){
//				$(".modal-backdrop").remove();
//			}
			for(var i=0;i<cacheModel.length;i++){
				if(cacheModel[i]){
				cacheModel[i].modal('hide');
				cacheModel[i]=null;
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
		if(login_popupvar) login_popup();
		//兼容IE9下placeholder不显示问题
		$('input, textarea').placeholder();
		//登录全局
		$('.top_user .sp').on('click', function (event) {
			event.preventDefault();
			event.stopPropagation();
			$('.show-card-wrap').toggleClass('in');
		});	
		$(document).on('click', function() {
			$('.show-card-wrap').removeClass('in');
		});		
		show_card();	
		$(window).resize(function(){
			show_card();
		});
		$(".top_meg").hover(function(){
			$(this).children(".bubble").show()
		},function(){
			$(this).children(".bubble").hide()
		});
		$(".topRight .a").eq(0).click(topRightRegister);
		$(".topRight .a").eq(1).click(topRightLogin);
		//中部搜索
		$(".sreachBBoxBtn").click(function(){sreachBtn($(".sreachBBoxTxt").val());});
		//顶部搜索
		$(".topSreach").click(function(){
			$(this).parent().parent().toggleClass("sH")
		});
		$(".topSreachTxt,.sreachBBoxTxt").keydown(function(event){
			if(event.keyCode == 13)
				sreachBtn($(this).val());
		});
		$(".sreachBBoxBtn").click(function(){sreachBtn($(".sreachBBoxTxt").val());});
		$(".section1_sreach_txt").keydown(function(event){
			if(event.keyCode == 13)
				sreachBtn($(this).val());
		});
		$(".section1_sreach_btn").click(function(){sreachBtn($(".section1_sreach_txt").val());});
		$(".class53").click(function(){
			$("#KFLOGO .Lelem").eq(0).trigger("click");
		});
		//学生基数计算
		//var nowdate=new Date();
		//nowdate.setHours(0);
		//nowdate.setMinutes(0);
		//nowdate.setSeconds(0);
		//var startdate=new Date("2016/03/04 0:0:0");
		//$(".section1_font>.pa .stc1").html(82000+parseInt(nowdate.diff(startdate))*5);
		//$(".section1_font>.pa .stc2").html(200+parseInt(nowdate.dimm(startdate))*10);
		//$(".section1_font>.pa .stc3").html(70+parseInt(nowdate.dimm(startdate))*5);
		//返回顶部
		$(".toolbar-item-gotop").click(function(){
			$('html,body').stop().animate({scrollTop: '0px'}, 800);
		});
		//------------OLD-----------------------------
		$(".toolbar-item-weibo>div").hover(function(){
		},function(){
			$(this).stop().hide("fast");
		});
		$(".toolbar-item-weibo").click(function(){
			$(".lixianB").show();
		});
		$(".toolbar-item-weixin").unbind().click(function(){
			$("#KFLOGO .Lelem").eq(0).trigger("click");
		});

		//忘记密码
		var OFF = true;
		$('#btnForgetpsw').on('click', function () {
		  if(captchaObjF3) captchaObjF3.refresh();
		  if(OFF){
		    captcha(".newcaptcha");
		    OFF = false;
		  }
		  $('#forgetpswModal').modal('show');
		  $('#loginModal').modal('hide');
		  
		})

		//注册
		$('#btnRegister').on('click', function () {
		  $('#loginModal').modal('hide');
		})
	
		//登录表单键盘事件
		$("#login_form").keydown(function(event){
			if(event.keyCode == 13)
				login_form_submit("login-form-tips");
		});
		//注册表单键盘事件
		$("#email_register_form").keydown(function(event){
			if(event.keyCode == 13)
				register_form_submit();
		});
		$("#email_register_form").keydown(function(event){
			if(event.keyCode == 13)
				register_form_submit();
		});
		//首页-忘记密码表单键盘事件
		//captcha(".newcaptcha");
		$("#find_password_form").keydown(function(event){
			if(event.keyCode == 13)
				find_password_form_submit();
		});
		//zhouyi:7-30 发送验证邮件事件
		$(".sendE a").click(function(){
			$(".zy_success").removeClass("upmove");
			$(this).parent().hide();
			$(".sendE2").show().find("span").html("60s");	
			$.ajax({
				 type: "GET",
				 url: "/user/send_again_email",
				 data: {username:zyemail},
				 dataType: "html",
				 success: function(data){
					 zy_str="验证邮件发送成功";
					 if(data)
						zy_Countdown();
				 },
				error:function(){
					zy_str="验证邮件发送失败";
				}
	
			 });
		});
		notice_message();
		//------------OLDEND-----------------------------
	}
	function checkTime(i){
	   if (i < 10) {
		   i = "0" + i;
		}
	   return i;
	}
	function timeStr(nts){
		var dd = parseInt(nts / 60 / 60 / 24, 10);
		var hh = parseInt(nts / 60 / 60 % 24, 10);
		var mm = parseInt(nts / 60 % 60, 10);
		var ss = parseInt(nts / 1000 % 60, 10);
		$(".zy_activityDemo2 .p > span").html(dd);
		dd = checkTime(dd);
		hh = checkTime(hh);
		mm = checkTime(mm);
		ss = checkTime(ss);

		return dd+":"+hh+":"+mm+":"+ss;
	}
	function sreachBtn(str){
		location.href="/course/list/?catagory="+str;
	}
	function topRightLogin(){
		login_popup();
	}
	function topRightRegister(){
		window.open('/user/signup/');
	}	
	function show_card(){
		if($('.top_user').length>0){
		var _parent_left = $('.top_user').offset().left;
		var _parent_outw = $('.top_user').outerWidth();
		var _this_outw = $('.show-card').outerWidth();
		var _this_left = Math.abs(_parent_left - (_this_outw - _parent_outw));
		$('.show-card').css({
			'left': _this_left
		});
		}
	}
	this.openVideo = function(url){
		url||(url="http://ocsource.maiziedu.com/lps_intro.mp4");
		$("#microohvideo").children().attr("src",url);
		$('#VideoDemo').modal('show');
	}
	this.openVideo2 = function(url){
		url||(url="http://ocsource.maiziedu.com/lps_intro.mp4");
		$("#microohvideo2").children().attr("src",url);
		$('.teacherVideo').fadeIn();
	}
	//Damon: 喇叭气泡
	function notice_message(){
	  function notice_info(data){
		var Txt = '';
		Txt += '<li><a href="'+_fps_site_url+'chat/?type=system">系统消息&nbsp;<span>'+ (data.sys_msg_count == 0 ? '' : data.sys_msg_count) + '</sapn></a></li>';
		var uu= _fps_site_url+"common/dynmsg/";
        if(data.dyn_msg_count > 0){uu=_fps_site_url+"common/dynmsg/?unread=1&page=1";}
		Txt += '<li><a href="'+uu+'">动态&nbsp;<span>'+ (data.dyn_msg_count == 0 ? '' : data.dyn_msg_count) + '</sapn></a></li>';
		Txt += '<li><a href="'+_fps_site_url+'common/social/?list_type=fans">粉丝&nbsp;'+ (data.fan_msg_count == 0 ? '' : data.fan_msg_count) + '</sapn></a></li>';
		Txt += '<li><a href="'+_fps_site_url+'chat/?type=praise">赞&nbsp;'+ (data.praise_msg_count == 0 ? '' : data.praise_msg_count) + '</sapn></a></li>';
		//Txt += '<li><a href="'+_fps_site_url+'chat/?type=at">@我&nbsp;'+ (data.at_msg_count == 0 ? '' : data.at_msg_count) + '</sapn></a></li>';
		return Txt;

	  }

	  var oUl = $('.bubble');
	  $.ajax({
		 url: _fps_site_url+'chat/',
		 type: 'POST',
		 dataType: 'json',
		 xhrFields: {
              withCredentials: true
           },
		 success: function (data) {
			if(data.status == 'success') {
				var num = data.sys_msg_count + data.dyn_msg_count + data.fan_msg_count + data.praise_msg_count + data.at_msg_count;
				var html = notice_info(data);
				if(num){
				  $('.top_meg').addClass('top_megH');
				  $('.top_megH i.Arial').css('display','block').html(num);
				}
				oUl.html(html).removeClass('loading');
			}
		 }
	  });

		$.ajax({
		 url: _fps_site_url+'common/user_fans_zan/',
		 type: 'POST',
		 dataType: 'json',
		 xhrFields: {
              withCredentials: true
           },
		 success: function (data) {
			if(data.status == 'success') {
				$(".zy_userDiv .d2 .s1").html(data.fans);
				$(".zy_userDiv .d2 .s2").html(data.praise);
			}
		 }
	  });

	  console.log("\u0026\u006c\u0074\u003b\u0021\u002d\u002d\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u003b\u004a\u0037\u002c\u0020\u003a\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u003a\u003b\u0037\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0069\u0076\u0059\u0069\u002c\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003b\u004c\u004c\u004c\u0046\u0053\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0069\u0076\u0037\u0059\u0069\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0037\u0072\u0069\u003b\u006a\u0035\u0050\u004c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u003a\u0069\u0076\u0059\u004c\u0076\u0072\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0069\u0076\u0072\u0072\u0069\u0072\u0072\u0059\u0032\u0058\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u003b\u0072\u0040\u0057\u0077\u007a\u002e\u0037\u0072\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0069\u0076\u0075\u0040\u006b\u0065\u0078\u0069\u0061\u006e\u006c\u0069\u002e\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0069\u004c\u0037\u003a\u003a\u002c\u003a\u003a\u003a\u0069\u0069\u0069\u0072\u0069\u0069\u003a\u0069\u0069\u003b\u003a\u003a\u003a\u003a\u002c\u002c\u0069\u0072\u0076\u0046\u0037\u0072\u0076\u0076\u004c\u0075\u006a\u004c\u0037\u0075\u0072\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0072\u0069\u003a\u003a\u002c\u003a\u002c\u003a\u003a\u0069\u003a\u0069\u0069\u0069\u0069\u0069\u0069\u0069\u003a\u0069\u003a\u0069\u0072\u0072\u0076\u0031\u0037\u0037\u004a\u0058\u0037\u0072\u0059\u0058\u0071\u005a\u0045\u006b\u0076\u0076\u0031\u0037\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003b\u0069\u003a\u002c\u0020\u002c\u0020\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u0072\u0072\u0069\u0072\u0069\u0069\u003a\u0069\u003a\u003a\u003a\u0069\u0069\u0069\u0072\u0032\u0058\u0058\u0076\u0069\u0069\u003b\u004c\u0038\u004f\u0047\u004a\u0072\u0037\u0031\u0069\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u002c\u002c\u0020\u002c\u002c\u003a\u0020\u0020\u0020\u002c\u003a\u003a\u0069\u0072\u0040\u006d\u0069\u006e\u0067\u0079\u0069\u002e\u0069\u0072\u0069\u0069\u003a\u0069\u003a\u003a\u003a\u006a\u0031\u006a\u0072\u0069\u0037\u005a\u0042\u004f\u0053\u0037\u0069\u0076\u0076\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u003a\u003a\u002c\u0020\u0020\u0020\u0020\u003a\u003a\u0072\u0076\u0037\u0037\u0069\u0069\u0069\u0072\u0069\u0069\u0069\u003a\u0069\u0069\u0069\u003a\u0069\u003a\u003a\u002c\u0072\u0076\u004c\u0071\u0040\u0068\u0075\u0068\u0061\u006f\u002e\u004c\u0069\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u0020\u002c\u003a\u0069\u0072\u0037\u0069\u0072\u003a\u003a\u002c\u003a\u003a\u003a\u0069\u003b\u0069\u0072\u003a\u003a\u003a\u0069\u003a\u0069\u003a\u003a\u0072\u0053\u0047\u0047\u0059\u0072\u0069\u0037\u0031\u0032\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u003a\u003a\u0020\u0020\u002c\u0076\u0037\u0072\u003a\u003a\u0020\u003a\u003a\u0072\u0072\u0076\u0037\u0037\u003a\u002c\u0020\u002c\u002c\u0020\u002c\u003a\u0069\u0037\u0072\u0072\u0069\u0069\u003a\u003a\u003a\u003a\u003a\u002c\u0020\u0069\u0072\u0037\u0072\u0069\u0037\u004c\u0072\u0069\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u0032\u004f\u0042\u0042\u004f\u0069\u002c\u0069\u0069\u0069\u0072\u003b\u0072\u003a\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0069\u0072\u0072\u0069\u0069\u0069\u0069\u003a\u003a\u002c\u002c\u0020\u002c\u0069\u0076\u0037\u004c\u0075\u0075\u0072\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u0020\u0020\u0020\u0020\u0020\u0069\u0037\u0038\u004d\u0042\u0042\u0069\u002c\u003a\u002c\u003a\u003a\u003a\u002c\u003a\u002c\u0020\u0020\u003a\u0037\u0046\u0053\u004c\u003a\u0020\u002c\u0069\u0072\u0069\u0069\u0069\u003a\u003a\u003a\u0069\u003a\u003a\u002c\u002c\u003a\u0072\u004c\u0071\u0058\u0076\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0069\u0075\u004d\u004d\u0050\u003a\u0020\u003a\u002c\u003a\u003a\u003a\u002c\u003a\u0069\u0069\u003b\u0032\u0047\u0059\u0037\u004f\u0042\u0042\u0030\u0076\u0069\u0069\u0069\u0069\u003a\u0069\u003a\u0069\u0069\u0069\u003a\u0069\u003a\u003a\u003a\u0069\u004a\u0071\u004c\u003b\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u003a\u003a\u003a\u003a\u0069\u0020\u0020\u0020\u002c\u002c\u002c\u002c\u002c\u0020\u003a\u003a\u004c\u0075\u0042\u0042\u0075\u0020\u0042\u0042\u0042\u0042\u0042\u0045\u0072\u0069\u0069\u003a\u0069\u003a\u0069\u003a\u0069\u003a\u0069\u003a\u0069\u003a\u0069\u003a\u0072\u0037\u0037\u0069\u0069\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u002c\u002c\u003a\u003a\u003a\u0072\u0072\u0075\u0042\u005a\u0031\u004d\u0042\u0042\u0071\u0069\u002c\u0020\u003a\u002c\u002c\u002c\u003a\u003a\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u0069\u0072\u0069\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u002c\u002c\u003a\u003a\u003a\u003a\u0069\u003a\u0020\u0020\u0040\u0061\u0072\u0071\u0069\u0061\u006f\u002e\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u003a\u002c\u002c\u0020\u002c\u003a\u003a\u003a\u0069\u0069\u003b\u0069\u0037\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u003a\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0072\u006a\u0075\u006a\u004c\u0059\u004c\u0069\u0020\u0020\u0020\u002c\u002c\u003a\u003a\u003a\u003a\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u002c\u002c\u0020\u0020\u0020\u002c\u003a\u0069\u002c\u003a\u002c\u002c\u002c\u002c\u002c\u003a\u003a\u0069\u003a\u0069\u0069\u0069\u000d\u000a\u0020\u0020\u0020\u0020\u003a\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0042\u0042\u0042\u0042\u0042\u0042\u0042\u0042\u0042\u0030\u002c\u0020\u0020\u0020\u0020\u002c\u002c\u003a\u003a\u003a\u0020\u002c\u0020\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u0020\u002c\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u002c\u002c\u0020\u002c\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0069\u002c\u0020\u0020\u002c\u0020\u0020\u002c\u0038\u0042\u004d\u004d\u0042\u0042\u0042\u0042\u0042\u0042\u0069\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u003a\u002c\u002c\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u002c\u0020\u002c\u0020\u002c\u0020\u0020\u0020\u002c\u0020\u002c\u0020\u002c\u0020\u003a\u002c\u003a\u003a\u0069\u0069\u003a\u003a\u0069\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0069\u005a\u004d\u004f\u004d\u004f\u004d\u0042\u0042\u004d\u0032\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u002c\u002c\u002c\u002c\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u002c\u002c\u002c\u002c\u003a\u002c\u002c\u002c\u003a\u003a\u003a\u003a\u0069\u003a\u0069\u0072\u0072\u003a\u0069\u003a\u003a\u003a\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0069\u0020\u0020\u0020\u002c\u002c\u003a\u003b\u0075\u0030\u004d\u0042\u004d\u004f\u0047\u0031\u004c\u003a\u003a\u003a\u0069\u003a\u003a\u003a\u003a\u003a\u003a\u0020\u0020\u002c\u002c\u002c\u003a\u003a\u002c\u0020\u0020\u0020\u002c\u002c\u002c\u0020\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u0069\u003a\u0069\u0069\u0072\u0069\u0069\u003a\u0069\u003a\u0069\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u002c\u0069\u0075\u0055\u0075\u0075\u0058\u0055\u006b\u0046\u0075\u0037\u0069\u003a\u0069\u0069\u0069\u003a\u0069\u003a\u003a\u003a\u002c\u0020\u003a\u002c\u003a\u002c\u003a\u0020\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u0069\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u0072\u0037\u0069\u0069\u0072\u0069\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u0020\u003a\u0072\u006b\u0040\u0059\u0069\u007a\u0065\u0072\u006f\u002e\u0069\u003a\u003a\u003a\u003a\u003a\u002c\u0020\u002c\u003a\u0069\u0069\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u003a\u002c\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u0072\u0072\u0069\u0069\u0069\u0072\u0069\u003a\u003a\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u003a\u0020\u0020\u0020\u0020\u0020\u0020\u0035\u0042\u004d\u0042\u0042\u0042\u0042\u0042\u0042\u0053\u0072\u003a\u002c\u003a\u003a\u0072\u0076\u0032\u006b\u0075\u0069\u0069\u003a\u003a\u003a\u0069\u0069\u0069\u003a\u003a\u002c\u003a\u0069\u003a\u002c\u002c\u0020\u002c\u0020\u002c\u002c\u003a\u002c\u003a\u0069\u0040\u0070\u0065\u0074\u0065\u0072\u006d\u0075\u002e\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u003a\u0072\u0035\u0030\u0045\u005a\u0038\u004d\u0042\u0042\u0042\u0042\u0047\u004f\u0042\u0042\u0042\u005a\u0050\u0037\u003a\u003a\u003a\u003a\u0069\u003a\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u002c\u003a\u0020\u003a\u002c\u003a\u002c\u003a\u003a\u0069\u003b\u0072\u0072\u0072\u0069\u0072\u0069\u0069\u0069\u0069\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u006a\u0075\u006a\u0059\u0059\u0037\u004c\u0053\u0030\u0075\u006a\u004a\u004c\u0037\u0072\u003a\u003a\u002c\u003a\u003a\u0069\u003a\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u0069\u0072\u0072\u0072\u0072\u0072\u0072\u0072\u003a\u0069\u0069\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u003a\u0020\u0020\u003a\u0040\u006b\u0065\u0076\u0065\u006e\u0073\u0075\u006e\u002e\u003a\u002c\u003a\u002c\u002c\u002c\u003a\u003a\u003a\u003a\u0069\u003a\u0069\u003a\u003a\u003a\u003a\u003a\u002c\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0072\u003b\u0069\u0069\u003b\u0037\u0076\u0037\u0037\u003b\u0069\u0069\u003b\u0069\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u002c\u0020\u0020\u0020\u0020\u0020\u002c\u002c\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u0069\u0069\u0069\u0069\u0069\u003a\u0069\u003a\u003a\u003a\u003a\u002c\u002c\u0020\u003a\u003a\u003a\u003a\u0069\u0069\u0069\u0069\u0072\u0040\u0078\u0069\u006e\u0067\u006a\u0069\u0065\u0066\u002e\u0072\u003b\u0037\u003a\u0069\u002c\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u002c\u0020\u002c\u0020\u002c\u002c\u002c\u003a\u002c\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0069\u0069\u0069\u0069\u0069\u0069\u0069\u0069\u003a\u002c\u003a\u002c\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u0069\u0069\u0072\u003b\u0072\u0069\u0037\u0076\u004c\u0037\u0037\u0072\u0072\u0069\u0072\u0072\u0069\u003a\u003a\u000d\u000a\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u0020\u003a\u002c\u002c\u0020\u002c\u0020\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u003a\u0069\u003a\u003a\u003a\u0069\u003a\u003a\u003a\u0069\u003a\u0069\u003a\u003a\u002c\u002c\u002c\u002c\u002c\u003a\u002c\u003a\u003a\u0069\u003a\u0069\u003a\u003a\u003a\u0069\u0069\u0072\u003b\u0040\u0053\u0065\u0063\u0062\u006f\u006e\u0065\u002e\u0069\u0069\u003a\u003a\u003a\u000d\u000a\u000d\u000a\u002d\u002d\u0026\u0067\u0074\u003b")
	}
}
//首页JS
var myIndex=function(){
	Load.call(this);
	var th;
	this.userV;
	this.indexInit=function(){
		window.onresize=function(){findDimensions();}
		th=this;
		th.init();
		$(".section1_menu li").hover(menu2HoverGO,menu2HoverTO);
		$('.bxslider').bxSlider({
			"mode":"fade",
			"onSlideAfter":SlideAfter,
			"onSliderLoad":SliderLoad
		});		
		$(window).bind("scroll", windowscroll);		
				
		//video
		player = videojs("microohvideo", {
			controls: true,
			playbackRates: [1, 1.25, 1.5, 2]
		});
		player2 = videojs("microohvideo2", {
			controls: true,
			playbackRates: [1, 1.25, 1.5, 2]
		});

		$(".zy_VideoDemo .close").unbind().click(closeEvent);
		$('#VideoDemo').on('hide.bs.modal', closeEventING);				
		//头像切换
		bxslider2=$(".bxslider2").superposition({
			"mode":"overlying"
			,"onSlideAfter":SlideAfter2
			,"onSliderLoad":SliderLoad2
		});
		$(".section5_bottom a").click(section5_bottomAGO);
		$(".topHead").hover(function(){
			//$(this).parent().addClass("poTop");
		},function(){
			if(srocllTop==0){
				$(this).parent().removeClass("poTop");
			}
		});		
		onload();
		$(window).scroll(function(){
			onload();
		});
		$(".videoArrow").unbind().click(function(){th.openVideo2($(this).parent().attr("hp"));
			$(".section5_bottom").addClass("lookVideo");player2.play();
		});
		//$(".section5 .div .videoArrow").unbind().click(function(){th.openVideo($(this).parent().attr("hp"));});
		$(".jobs_list li > div .p2 a").unbind().click(function(){th.openVideo($(this).attr("pt"));player.play();});
		var zzyypic= 0,zzyyStr='';
		$(".zy_pingce_con").css({scrollLeft:0});
		$(".zy_pingce_btn").click(function(){
			zzyypic++;
			if(zzyypic==5){
				if(!$(".zy_pingce_con ul li").eq(zzyypic-1).find(".cl").length){
					$(".zyred").show();zzyypic--;return false;
				}
				$(".zy_pingce_con ul li").each(function(){
					if($(this).find(".cl").length)
						zzyyStr+=$(this).find(".cl").children("input").val();
					else
						zzyyStr+=0;
				});
				var ss=askArr[zzyyStr.substr(2,5)]
				var hh='';
				for(var s in ss){
					hh+='<dd><a href="'+ss[s]+'" target="_blank">'+s+'</a></dd>';
				}
				$(".zy_pingce_dl").html(hh);
				$('#pingce').modal('hide');
				$('#pingceSuccess').modal('show');
				zzyypic=0;zzyyStr='';
			}
			else{
				if(!$(".zy_pingce_con ul li").eq(zzyypic-1).find(".cl").length){
					$(".zyred").show();zzyypic--;return false;
				}
				$(".zyred").hide();
			}
			if(zzyypic>4){
				zzyypic=4;
			}
			$(".zy_pingce_con ul").stop().animate({'left': -(zzyypic*453)+'px'}, 300);

		});
		$('#pingce').on('hide.bs.modal', function () {
        	zzyypic=0;$(".zyred").hide();
		});
		$(".zy_radioNew input").click(function(){
			if($(this).parent().hasClass("cl")){
				$(this).parent().removeClass("cl");
			}
			else{
				$(this).parent().parent().parent().find(".zy_radioNew").removeClass("cl");
				$(this).parent().addClass("cl");
			}
		});
		$(".zy_pingce .close").click(function(){
			$('#pingce').modal('hide');
			$('#pingceSuccess').modal('hide');
		});
		$(".teacherVideoClose").click(section5_bottomAGO);
	};
	var srocllTop=0;
	function onload(){
		srocllTop=$(window).scrollTop();
		if(srocllTop>0){
			$(".section1").addClass("poTop");
		}
		else{
			$(".section1").removeClass("poTop");
		}
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
	var player,player2;
	function closeEvent(){//关闭播放窗口
		player.pause();
		$('#VideoDemo').modal('hide');
	}
	function closeEventING(){//关闭播放窗口的事件
		player.pause();
	}
	
	var scrollBO=true,scrollBO2=true;
	var funFall = function(ball,b,c) {			
		var start = 0, during = 60;
		var _run = function() {
			start++;
			var top = Tween.Quad.easeOut(start, b, c, during);
			ball.css("bottom", top);
			if (start < during) requestAnimationFrame(_run);
		};
		_run();
	};
	var windowscroll=function(event){
		//窗口的高度+看不见的顶部的高度=屏幕低部距离最顶部的高度  
		var thisButtomTop = parseInt($(this).height()) + parseInt($(this).scrollTop());  
		var thisTop = parseInt($(this).scrollTop()); //屏幕顶部距离最顶部的高度  
		var PictureTop = parseInt($(".section3").offset().top)+500;
		var PictureTop2 = parseInt($(".section7").offset().top)+500;
		if (PictureTop >= thisTop && PictureTop <= thisButtomTop &&scrollBO) {
			scrollBO=false;
			new funFall($(".section3>img").eq(2),-686,476);
			setTimeout(function(){new funFall($(".section3>img").eq(1),-676,466);},500)	
			setTimeout(function(){new funFall($(".section3>img").eq(0),-666,500);},1000)	
		}
		if (PictureTop2 >= thisTop && PictureTop2 <= thisButtomTop &&scrollBO2) {
			scrollBO2=false;
			$(".section7 .img1").removeClass("moveL");
			$(".section7 .img2").removeClass("moveL");
		}
	}
	var menu2HoverGO=function(){
		$(this).children(".menu2").stop().css("height","auto").slideDown();
	};
	var menu2HoverTO=function(){
		$(this).children(".menu2").stop().css("height","auto").slideUp();
	};
	var SliderLoad=function(currentIndex){
		$(".bxslider>li").eq(currentIndex).children("div").removeClass("moveLeft")
	};
	var SlideAfter=function($slideElement, oldIndex, newIndex){
		$slideElement.children("div").removeClass("moveLeft");
		setTimeout(function(){$slideElement.parent().children().eq(oldIndex).children("div").addClass("moveLeft")},1000);			
	};
	
}
//介绍页
var myaLesson=function(){
	Load.call(this);
	var th;
	this.indexInit=function(){
		th=this;
		th.init();
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
	}
	var bxslider2,scrollBO=true;
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


}
//注册页
var signUp = function(){
	Load.call(this);
	var th;
	this.indexInit=function(){
		th=this;
		th.init();



		$('#id_mobile_code').blur(function(){
			var userMobile = $(this).val();
			var telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/g;
			if(userMobile == null || userMobile == ''){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('success').addClass('error').html('请输入你的手机号').show(500);
			}else if(telReg.test(userMobile)){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!telReg.test(userMobile)){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('success').addClass('error').html('手机号码格式不正确').show(500);
			}
		}).keyup(function(){
			var userMobile = $(this).val();
			var telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/g;
			if(userMobile == null || userMobile == ''){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('success').addClass('error').html('请输入你的手机号').show(500);
			}else if(telReg.test(userMobile)){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!telReg.test(userMobile)){
				$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('success').addClass('error').html('手机号码格式不正确').show(500);
			}
		});

		$('#id_password_m').blur(function(){
			
			if($(this).val() == null || $(this).val() == ''){
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		}).keyup(function(){
			if($(this).val() == null || $(this).val() == ''){
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				$("label[for=password_m]").siblings('.p_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});

		$('#id_email').blur(function(){
			var userEmail = $(this).val();
			var emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			if(userEmail == null || userEmail == ''){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入你的邮箱').show(500);
			}else if(emailReg.test(userEmail)){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!emailReg.test(userEmail)){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('注册账号需为邮箱格式').show(500);
			}else{
				$("label[for=email]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		}).keyup(function(){
			var userEmail = $(this).val();
			var emailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/g;
			if(userEmail == null || userEmail == ''){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入你的邮箱').show(500);
			}else if(emailReg.test(userEmail)){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!emailReg.test(userEmail)){
				$("label[for=email]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('注册账号需为邮箱格式').show(500);
			}else{
				$("label[for=email]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});

		$('#id_password').blur(function(){
			if($(this).val() == null || $(this).val() == ''){
				$("label[for=password]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				$("label[for=password]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				$("label[for=password]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		}).keyup(function(){
			if($(this).val() == null || $(this).val() == ''){
				$("label[for=password]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				$("label[for=password]").siblings('.e_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				$("label[for=password]").siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});
	}
	$('.just-sign').on('click',function(){
		$('#loginModal').modal('show');
	})

}

var newIndex = function(){
	Load.call(this);
	var th;
	this.indexInit = function(){
		th=this;
		th.init();
	}
}

//教务--学生
var mystudentManage=function(){
	Load.call(this);
	var th;
	var zmap=new Map(),timeArray=new Array(),mysort=true,mypaystate=[],mylearningstate=[];
	var deanUrl={"ct":"/change/","ls":"/quit/","ds":"/pause/"};
	this.indexInit=function(op){
		th=this;
		th.init();
		op=op||{};
		th.userV = new UserVail("vail");
		$("#leaveschool").on({"click":function(){
				$(".modal").modal("hide");
			}
		},".zy_newclose");
		var sid;
		//退学等处理
		$(".sManage_table").on({
			"click":function(){
				sid=$(this).attr("sid").split("_");
				var th=$(this);
				$.ajax({
					 type: "GET",
					 url: "/lps3/ea/students/"+sid[1]+"_"+sid[2]+deanUrl[sid[0]]+"",
					 dataType: "html",
					 success: function(data){
						$("#leaveschool").html(data);
						$("#leaveschool").modal("show");
					 },
					error:function(){

					},
					beforeSend:function(XMLHttpRequest){
						th.css({"pointerEvents":"none"});
					},
					complete: function(XMLHttpRequest){
						th.css({"pointerEvents":"auto"});
					}
				 });
			}
		},".operation>a[data-target]");
		$("#leaveschool").on({"click":function(){
			var $th=$(this);
			var thNext=$th.next();
			if((!(th.userV.get("toclass"))||/^[ ]+$/.test(th.userV.get("toclass")))
				&&(!(th.userV.get("remark"))||/^[ ]+$/.test(th.userV.get("remark")))
			){
				thNext.removeClass("megRight").addClass("megError").html("不能为空");
				thNext.width(134);
				return ;
			}
			if(th.userV.get("remark").length>100){
				thNext.removeClass("megRight").addClass("megError").html("不能多余100字");
				thNext.width(134);
				return;
			}
			$.ajax({
				 type: "POST",
				 url: "/lps3/ea/students/"+sid[1]+"_"+sid[2]+deanUrl[sid[0]]+"",
				 data:$("#leaveschoolForm").serialize(),
				 dataType: "json",
				 success: function(data){
					if(data.status){
						thNext.removeClass("megError").addClass("megRight").html(data.message);
						setTimeout(function(){location.reload()},1000);
					}
					else{
						thNext.removeClass("megRight").addClass("megError").html(data.message);
					}
					thNext.width(134);
					setTimeout(function(){thNext.width(0);},4000);
				 },
					error:function(){
						thNext.removeClass("megError").addClass("megRight").html("系统错误");
						setTimeout(function(){location.reload()},1000);
					},
					beforeSend:function(XMLHttpRequest){
						$th.attr("disabled","disabled");
					},
					complete: function(XMLHttpRequest){
						$th.removeAttr("disabled");
					}
			});

			}
		},".deanframebtn");
		//教务班级事件
		$(".sm_select").change(function(){
			//var text=$(this).children("[selected]").html();
			$("#deanClassTxt").val("");
		})

		$(".sm_select").iSimulateSelect({width:148,height:0,selectBoxCls:"sm_info_selectD",optionCls:"sm_info_selectD_Op"});
		$(".sManage_table").on({
			"mouseenter":function(){
				$(this).parent().css("zIndex",3);
				$(this).children(".tstage_child").show();
			},"mouseleave":function(){
				$(this).parent().css("zIndex",2);
				$(this).children(".tstage_child").hide();
			}
		},".tstage>div");

		$(".sManage_table .people").each(function(index, element) {
			zmap.put($(this).children('[ttime]').attr("ttime"),$(element));
			timeArray.push(parseInt($(this).children('[ttime]').attr("ttime"),10));
		});
		//多选
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":["全款","试学"]
			,"arrayvalue":["全款","试学"]
			,"selectvalue":"全部"
			,onSelect:filterval
		});
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":["落后","正常","休学","已毕业","已退学"]
			,"arrayvalue":["落后","正常","休学","已毕业","已退学"]
			,"selectvalue":"全部"
			,onSelect:filterval2
		});
		//排序
		$(".multiselect1").multiselect({
			onSelect:function(e,value){
				if(value==1)
					ascending();
				else
					descending();
			}
		});
		//查询筛选框
		$(".sManage_Seltxt").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_classes/",
					data:{"e":$("#lps4dean").val(),"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if(data1[i][1]==$th.val()){$th.data("vv",data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $th.removeData("vv");
			}
			,"height":360
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
			}
			,onload:function(){
				(op.newid)&&(this.data("vv",op.newid))
			}
		});
		//第一个搜索
		var errornum=0
		$("#deanClassBtn").click(function(){
			var vv=$("#deanClassTxt").data("vv");
			if(vv&&vv!="-1"){
				location.href=changeURLPar(location.href.split("?")[0],"c",vv);
			}
			else{
				var thN=$(this).next();
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++;
			}
		})
		$("#deanClassBtn2").click(function(){
			var val=$("#deanClassTxt2").val().replaceAll(" ","");
			if(val!="") {
				var url = changeURLPar(location.href.split("?")[0], "q", val);
				url = changeURLPar(url, "e", $("#lps4dean").val());
				location.href = url;
			}
		})
	};
	//升序
	function ascending (){
		mysort=true;	var j=1;
		$(".sManage_table .people").remove();
		timeArray=timeArray.quickSort();
		for(var i=0;i<timeArray.length;i++){
			var tr=zmap.get(timeArray[i].toString());
			if((mypaystate.length==0||mypaystate.indexOf(tr.find("[pay-state]").attr("pay-state"))>-1)
				&&(mylearningstate.length==0||mylearningstate.indexOf(tr.find("[learning-state]").attr("learning-state"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}

		}
	}
	//降序
	function descending (){
		mysort=false;	var j=1;
		$(".sManage_table .people").remove();
		timeArray=timeArray.quickSort();
		for(var i=timeArray.length-1;i>-1;i--){
			var tr=zmap.get(timeArray[i].toString());
			if((mypaystate.length==0||mypaystate.indexOf(tr.find("[pay-state]").attr("pay-state"))>-1)
				&&(mylearningstate.length==0||mylearningstate.indexOf(tr.find("[learning-state]").attr("learning-state"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}
		}
	}
	//筛选
	function filterval(e,value){
		mypaystate=value;
		mysort?ascending():descending();
	}
	function filterval2(e,value){
		mylearningstate=value;
		mysort?ascending():descending();
	}

}
//教务--班级
var myclassManage=function(){
	Load.call(this);
	var th;
	var nowdate=new Date();
	var zmap=new Map();
	var classMegStr={"ce":"确认关闭报名?","oe":"确认开启报名?","graduation":"确认毕业？"}
	this.indexInit=function(op){
		th=this;
		th.init();
		$(".zy_newclose,.zy_classMeg_btn>.a2").click(function(){
			$(".modal").modal("hide");
		});
		$(".zy_classMeg_btn>.a1").click(function(){
			var classid=$(this).attr("classid").split("_");
			$.ajax({
				type: "GET",
				url:"/lps3/ea/classes/update_state/",
				data:{"e":classid[1],"i":classid[2]},
				beforeSend:function(XMLHttpRequest){

				},
				success: function(data1) {
					location.reload();
				},
				complete: function(XMLHttpRequest){
				}
			});
		});
		//时间限制
		new GySetDate({"targets":'#year1,#month2,#day3',"range":nowdate.getFullYear()+"-"+(nowdate.getMonth()+1)+"-"+nowdate.getDate()+",2030-09-21","value":""})

		$(".sManage_table .people").each(function(index, element) {
			zmap.put(index,$(element));
		});

		$(".modal").on("show.bs.modal", function(e){
			var datameg=e.relatedTarget.getAttribute("data-meg");
			if(datameg){
				var datamegA=datameg.split("_"),zcM=$(".zy_classMeg>p");
				zcM.eq(0).html("班级编号 "+datamegA[0]);
				zcM.eq(1).html(classMegStr[datamegA[1]]);
				zcM.eq(2).children().eq(0).attr("classid",datameg);
			}
		});
		$(".deanframebtn").click(function(){
			var $th=$(this);
			var career_courseV=$("#createClassForm input[name=career_course]").val();
			var qq_groupV=$("#createClassForm input[name=qq_group]").val();
			var teacherV=$("#createClassForm input[name=teacher]").val();
			var edu_adminV=$("#createClassForm input[name=edu_admin]").val();
			if(career_courseV.replaceAll(" ","")==""||career_courseV.replaceAll(" ","")=="-1"){
				$th.next().height(30).html("*请选择专业"); return;
			}
			else if(qq_groupV.replaceAll(" ","")==""){
				$th.next().height(30).html("*请输入QQ"); return;
			}
			else if(teacherV.replaceAll(" ","")==""||teacherV.replaceAll(" ","")=="-1"){
				$th.next().height(30).html("*请选择教师"); return;
			}
			else if(edu_adminV.replaceAll(" ","")==""||edu_adminV.replaceAll(" ","")=="-1"){
				$th.next().height(30).html("*请选择教务"); return;
			}

			$.ajax({
				type: "POST",
				url:"/lps3/ea/classes/create_class/",
				data:$("#createClassForm").serialize(),
				dataType: "json",
				beforeSend:function(XMLHttpRequest){
					$th.attr("disabled","disabled");
				},
				success: function(data1) {
					if(data1.status){
						location.reload();
					}
					else{
						$th.next().height(30).html(data1.message);
					}
				},
				complete: function(XMLHttpRequest){
					$th.removeAttr("disabled");
				}
			});

		});
		var cStatename=op.cStatename || [],cStatevalue=op.cStatevalue || []
			,specialtyname=op.specialtyname || [],specialtyvalue=op.specialtyvalue || []
			,tearchername=op.tearchername || [],tearchervalue=op.tearchervalue || [];
		//班级状态
		$(".multiselect1").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":cStatename
			,"arrayvalue":cStatevalue
			,"selectvalue":"全部"
			,onSelect:filterval1
		});
		//专业
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":specialtyname
			,"arrayvalue":specialtyvalue
			,"selectvalue":"全部"
			,onSelect:filterval2
		});
		//教师
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":tearchername
			,"arrayvalue":tearchervalue
			,"selectvalue":"全部"
			,onSelect:filterval3
		});
		//查询筛选框
		$(".sManage_Seltxt").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_eduadmins/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1],data1[i][2]);
							if(data1[i][1]==$th.val()){$th.data("vv",data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $th.removeData("vv");
			}
			,"height":360
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
			}
			,onload:function(){
				(op.newid)&&(this.data("vv",op.newid))
			}
		});
		//----添加班级下拉框---
		$(".csSreach").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				var career_courseObj=$("#createClassForm input[name=career_course]");
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_career_courses/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1],data1[i][2]);
							if(data1[i][1]==$th.val()){career_courseObj.val(data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) career_courseObj.val("");
			}
			,"height":180
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v,v2){
				this.data("vv",v);
				//var d=new Date();
				var no=v2.toUpperCase()+ $("#createClassForm #year1").val()+ $("#createClassForm #month2").val()+ $("#createClassForm #day3").val();
				$("#numberS").html(no);
				$("#createClassForm input[name=class_no]").val(no).data("v2",v2);
				$("#createClassForm input[name=career_course]").val(v);
			}
		});
		$(".selectTime select").change(function(){
			var v2=$("#createClassForm input[name=class_no]").data("v2");
			var no=v2.toUpperCase()+ $("#createClassForm #year1").val()+ $("#createClassForm #month2").val()+ $("#createClassForm #day3").val();
			$("#createClassForm input[name=class_no]").val(no);
			$("#numberS").html(no);
		});
		$(".tearcherSreach").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_teachers/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if(data1[i][1]==$th.val()){$("#createClassForm input[name=teacher]").val(data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $("#createClassForm input[name=teacher]").val("");
			}
			,"height":180
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
				$("#createClassForm input[name=teacher]").val(v);
			}
		});
		$(".deanSreach").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_eduadmins/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if(data1[i][1]==$th.val()){$("#createClassForm input[name=edu_admin]").val(data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $("#createClassForm input[name=edu_admin]").val("");
			}
			,"height":180
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
				$("#createClassForm input[name=edu_admin]").val(v);
			}
		});
		var errornum=0
		//教务查询
		$(".sManage_Sel_sreach_btn").click(function(){
			var vv=$("#deanClassTxt").data("vv");
			if(vv&&vv!="-1"){
				location.href=changeURLPar(location.href.split("?")[0],"b",vv);
			}
			else{
				var thN=$(this).next();
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++
			}
		});
	};
	var myclassstate=[],myspecialty=[],mytearcher=[];
	function checkTime(i){
	   if (i < 10) {
		   i = "0" + i;
		}
	   return i;
	}
	function filterval1(e,value){
		myclassstate=value;
		filtered();
	}
	function filterval2(e,value){
		myspecialty=value;
		filtered();
	}
	function filterval3(e,value){
		mytearcher=value;
		filtered();
	}
	function filtered (){
		var j=1;
		$(".sManage_table .people").remove();
		zmap.each(function(k,d,i){
			var tr=d;
			if((myclassstate.length==0||myclassstate.indexOf(tr.find("[class-state]").attr("class-state"))>-1) &&
				(myspecialty.length==0||myspecialty.indexOf(tr.find("[class-specialty]").attr("class-specialty"))>-1)&&
				(mytearcher.length==0||mytearcher.indexOf(tr.find("[class-tearcher]").attr("class-tearcher"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}
		});
	}
}
//教务--统计
var mystatisticsManage=function(){
	Load.call(this);
	var th;
	var zmap=new Map();
	this.indexInit=function(op){
		th=this;
		th.init();
		op=op ||{};
		$(".sManage_table .people").each(function(index, element) {
			zmap.put(index,$(element));
		});
		$(".ssMore").hover(function(){
			var ssMorediv=$(this);
			if(ssMorediv.children(".ssMorediv").length<=0){
				var html='';
				html+='<div class="ssMorediv"><i></i>';
				html+='<p><span>1.授课语言准确，清晰流畅，通俗易懂</span> 5分</p>';
				html+='<p><span>2.授课思路敏捷、逻辑性强、条理清晰</span> 4分</p>';
				html+='<p><span>3.语速控制适当，声音洪亮、富有激情</span> 5分</p>';
				html+='</div>';
				ssMorediv.append(html);
			}
			ssMorediv.children(".ssMorediv").show();
		},function(){
			$(this).children(".ssMorediv").hide();
		});

		//查询筛选框
		$(".sManage_Seltxt").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_eduadmins/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if($th.val()==data1[i][1]){$th.data("vv",data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $th.removeData("vv");
			}
			,"height":360
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
			}
			,onload:function(){
				(op.newid)&&(this.data("vv",op.newid))
			}
		});
		var specialtyname=op.specialtyname || [],specialtyvalue=op.specialtyvalue || []
			,tearchername=op.tearchername || [],tearchervalue=op.tearchervalue || [];
		//专业
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":specialtyname
			,"arrayvalue":specialtyvalue
			,"selectvalue":["全部","全部"]
			,onSelect:filterval2
		});
		//教师
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":tearchername
			,"arrayvalue":tearchervalue
			,"selectvalue":["全部","全部"]
			,onSelect:filterval3
		});
		//搜索
		var errornum=0;
		$("#eduadmin_det").click(function () {
			var vv = $("#deanClassTxt").data("vv");
			var url = changeURLPar(location.href.split("?")[0], "year", $("#year_value").val());
			url = changeURLPar(url, "month", $("#month_value").val());
			url = changeURLPar(url, "eu_id", vv);
			var thN=$(this).next();
			if(vv&&vv!="-1") {
				location.href = url;
			}
			else{
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++;
			}

		});

	};
	var myspecialty=[],mytearcher=[];
	function filterval2(e,value){
		myspecialty=value;
		filtered();
	}
	function filterval3(e,value){
		mytearcher=value;
		filtered();
	}
	function filtered (){
		var j=1;
		$(".sManage_table .people").remove();
		zmap.each(function(k,d,i){
			var tr=d;
			if((myspecialty.length==0||myspecialty.indexOf(tr.find("[class-specialty]").attr("class-specialty"))>-1)&&
				(mytearcher.length==0||mytearcher.indexOf(tr.find("[class-tearcher]").attr("class-tearcher"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}
		});
	}
}
//教务--直播排期
var mybroadcastManage=function(){
	Load.call(this);
	var th;
	this.indexInit=function(){
		th=this;
		th.init();

		$(".cs_select").iSimulateSelect({width:178,height:0,selectBoxCls:"cs_info_selectD",optionCls:"cs_info_selectD_Op"});
		$(".cs_select").change(function(e){
		var text=$(this).children("[selected]").html();
			$(".selectEND span").html(text);
		});

	};
}
//教务--问卷
var myquestionnaire =function(){
	Load.call(this);
	var th;
	this.indexInit=function(){
		th=this;
		th.init();

		//表单--单选
		$(".statisticsRadio").statisticsRadio();
		$("#ques_info_save").valid();

		$("#id_save_post").click(function () {
			var len1=$("#ques_info_save textarea[name=subjective_item_2]").val().length;
			var len2=$("#ques_info_save textarea[name=subjective_item_1]").val().length;
			if(len1>100||len2>100){
				$("#get_data").text("提交失败").addClass("bg-danger").addClass("tips-error").fadeIn().delay(3000).fadeOut();
				return false;
			}
			var $th=$(this);
			$.ajax({
				type: 'POST',
				url: $("#ques_info_save").attr("action"),
				data: $("#ques_info_save").serialize(),
				success: function (data) {
					if (data.status == "failure") {
						$("#get_data").text(data.msg).addClass("bg-danger").addClass("tips-error").fadeIn().delay(3000).fadeOut();
					} else {
						$("#get_data").text(data.msg).addClass("bg-success").addClass("tips-error").fadeIn().delay(3000).fadeOut(function () {
							window.location.href = $("#ques_info_save").attr("tourl");
						});
					}
				},
				beforeSend:function(XMLHttpRequest){
                    $th.attr("disabled","disabled");
                },
                complete: function(XMLHttpRequest){
                    $th.removeAttr("disabled");
                }
			});

		})
	};
}

//企业直通班
var myCourse =function(){
	Load.call(this);
	var th,player,player2;
	var topbo=true;
	this.indexInit=function(){
		th=this;
		th.init();

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
				$(".newCousebox2_menu li").removeClass("click liC");
				if($(".newCousebox2_menu li.liH").length>0){
					$(".newCousebox2_menu li.liH").addClass("liold")
				}
				$(".newCousebox2_menu li>.div2").hide();
				dynamics.setTimeout(function(){$(".newCousebox2_menu li>.div2").show();},600);
			}
			else{
				$(".newCousebox2_menu").removeClass("Ceiling");topbo=true;
				$(".newCousebox2_menu li").removeClass("liold");
			}
		});
		//
		var oGun = $('.zy_course_Nbox4_gun #ul1');
		$.ajax({
			url: '/course/get_student_dynamic/',
			type: 'GET',
			dataType:'html',
			success: function(data){
				oGun.html(data);
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
			}
		});

	};
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
}

//----------------------OLD---------------------
//刷新验证码
// function refresh_captcha(event){
//     $.get("/captcha/refresh/?"+Math.random(), function(result){
//         $('#'+event.data.form_id+' .captcha').attr("src",result.image_url);
//         $('#'+event.data.form_id+' .form-control-captcha[type="hidden"]').attr("value",result.key);
//     });
//     return false;
// }
// 弹出登陆框
function login_popup(msg){
    $('#id_account_l').val("");
    $('#id_password_l').val("");
    $('#id_email').val("");
    $('#id_password').val("");
    $('#id_captcha_1').val("");
    $('#id_mobile').val("");
    $('#id_mobile_code').val("");
    $('#id_password_m').val("");
    $('#id_captcha_m_1').val("");
    $('#id_captcha_1').val("");
    $('#login-form-tips').hide();
    $('#findpassword-tips').hide();
    $('#mobile_code_password-tips').hide();
    $('#register-tips').hide();
    // refresh_captcha({"data":{"form_id":"email_register_form"}});
    // refresh_captcha({"data":{"form_id":"mobile_register_form"}});
    // refresh_captcha({"data":{"form_id":"find_password_form"}});
    $('#loginModal').modal('show');
    // alert(msg);
    if(typeof(msg) != 'undefined'){
        $('#loginModal #login-form-tips').show().html(msg);
    }
}
//注册提交
function register_form_submit(){
    if(current_register_form == "mobile_register_form"){
    	if($('.active .form-control').val().length > 0){
    		$('.active .form-control').next('label').css({'transform': 'translateY(-18px)'});
    	}   	
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/register/mobile_verify/",
            data:{
				'type': 'mobile',
            	'mobile': $('#id_mobile_code').val(),
            	'password_m': $('#id_password_m').val(),
            	'geetest_challenge': $('.geetest_challenge').attr('value'),
            	'geetest_validate': $('.geetest_validate').attr('value'),
            	'geetest_seccode': $('.geetest_seccode').attr('value'),
            	"mobile_code": '-11111'
            },
            async: true,
            beforeSend:function(XMLHttpRequest){
                $(".sign_btn").html("注册中...");
                $("sign_btn").attr("disabled","disabled");
            },
            success: function(data) {
            	//console.log(data);
            	if(data.status == 'success'){

			    $.ajax({
			        cache: false,
			        type: "POST",
			        url:"/user/register/mobile/sendsms_signup/",
			        data:{
			        	'mobile': $('#id_mobile_code').val(),
			        	'geetest_challenge': $('.geetest_challenge').attr('value'),
			        	'geetest_validate': $('.geetest_validate').attr('value'),
			        	'geetest_seccode': $('.geetest_seccode').attr('value'),
			        },
			        async: true,
			        success: function(data){
			        	//console.log(data)
			        	       	
			            if(data.mobile){
			                $(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
			                //$("#id_mobile").focus();
			                $('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.mobile).show(500);
			            }else if(data.captcha){
			                $(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
			                
			            }else if(data.status == 'failure'){
			                $(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
			            }else{
			                $(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
			                $('#mobile_register_form').hide().siblings('#verify_form').show('fast',function(){
			                	$('.sign-tabs li').unbind('click');
			                });
			                show_send_sms(60);
			            }
			        }
			    });
            		
            		
            		$('.user_mobile').html($("#id_mobile_code").val().substring(0,3)+"****"+$("#id_mobile_code").val().substring(8,11));
            		
            		$('#verify-ok').on('click',function(){
        				$.ajax({
        				    cache: false,
        				    type: "POST",
        				    url:"/user/register/mobile/",
        				    data:{
								'type': 'mobile',
        				    	'mobile': $('#id_mobile_code').val(),
        				    	'password_m': $('#id_password_m').val(),
        				    	'geetest_challenge': $('.geetest_challenge').attr('value'),
        				    	'geetest_validate': $('.geetest_validate').attr('value'),
        				    	'geetest_seccode': $('.geetest_seccode').attr('value'),
        				    	'mobile_code': $('#Verify').val(),
								"partner": $('#reg_partner').val(),
								"openid": $('#reg_openid').val(),
								"invitation_code": $('#invitation_code').val()
        				    },
        				    async: true,
        				    beforeSend:function(XMLHttpRequest){},
        				    success: function(data) {

        				    	if(data.mobile_code){
        				    	    $(".verify-tips").removeClass('success').addClass('error').html(data.mobile_code).show(500);
        				    	    //$("#Verify").focus();
        				    	}else{
        				    	    window.location = '/user/sign_success/';
        				    	}
        				    }
        				});
            		})
            	}else{
            		if(data.mobile){
						$(".m_sign_tips").addClass('error').html(data.mobile).show(500);
						//$("#id_mobile").focus();
            		}else if(data.password_m){
            			$(".p_sign_tips").addClass('error').html(data.password_m).show(500);
            			//$("#id_password_m").focus();
            		}else if(data.captcha){
            			$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
            		}
            	}
                
            },
            complete: function(XMLHttpRequest){
                $(".sign_btn").html("注册");
                $(".sign_btn").removeAttr("disabled");
            }
        });
    }else if(current_register_form == "email_register_form"){
    	
        $.ajax({
            cache: false,
            type: "POST",
            url:"/user/register/email/",
            data:{
				'type': 'email',
            	'email': $('#id_email').val(),
            	'password': $('#id_password').val(),
            	'geetest_challenge': $('#email_register_form .geetest_challenge').attr('value'),
            	'geetest_validate': $('#email_register_form .geetest_validate').attr('value'),
            	'geetest_seccode': $('#email_register_form .geetest_seccode').attr('value'),
				"partner": $('#reg_partner').val(),
				"openid": $('#reg_openid').val(),
				"invitation_code": $('#invitation_code').val()
            },
            async: true,
            beforeSend:function(XMLHttpRequest){
                $(".sign_btn").html("注册中...");
                $(".sign_btn").attr("disabled","disabled");
            },
            success: function(data) {
            	
                //console.log(data)
                if(data.email){
                	$("label[for=email]").siblings('.e_sign_tips').addClass('error').html(data.email).show(500);
                	//$("#id_email").focus();
                }else if(data.password){
                	$("label[for=password]").siblings('.e_sign_tips').addClass('error').html(data.password).show(500);
                	//$("#id_password").focus();
				}else if(data.email_ue){
                	$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.email_ue).show(500);
                	//$("#id_password").focus();
                }else if(data.captcha){
                	$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
                }else{
                	$('#email_register_form').hide().siblings('#email_form').show();
                	$('.email-tips').addClass('success');
                	$('.user_email').html($('#id_email').val());
                }
                // if(data.email){
                //     $("#register-tips").html(data.email).show(500);
                //     $("#id_email").focus();
                // }else if(data.password){
                //     $("#register-tips").html(data.password).show(500);
                //     $("#id_password").focus();
                // }else if(data.captcha){
                //     $("#register-tips").html(data.captcha).show(500);
                //     $("#id_captcha_1").focus();
                //     if(data.captcha == "验证码错误")
                //         refresh_captcha({"data":{"form_id":"email_register_form"}});
                // }else{
                // 	$('#email_register_form').hide().siblings('#email_form').show();
                // 	$('.user_email').html($('#id_email').val());
                //     $("#register_btn").html("登录中...");
                //     $("#id_account_l").val($("#id_email").val());
                //     $("#id_password_l").val($("#id_password").val());
                //     zyemail=$("#id_email").val();
                //     var ebo=zy_validate_Email(false,zyemail,$("#id_password").val());
                //     zyUname=$("#id_email").val();
                //     ebo&&login_form_submit("register-tips");
                //     _trackData.push(['addaction','完成邮件注册','来源'+location.pathname]);
                //     return;
                // }
            },
            complete: function(XMLHttpRequest){
                $(".sign_btn").html("注册");
                $(".sign_btn").removeAttr("disabled");
            }
        });
    }
}
//找回密码表单提交
function find_password_form_submit(){

    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/",
        data:{
        	'account':$('#id_account').val(),
        	'geetest_challenge': $('#find_password_form .geetest_challenge').attr('value'),
        	'geetest_validate': $('#find_password_form .geetest_validate').attr('value'),
        	'geetest_seccode': $('#find_password_form .geetest_seccode').attr('value')
        },
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#findpassword_btn").html("提交中...")
            $("#findpassword_btn").attr("disabled","disabled")
        },
        success: function(data) {
        	if(data.account){
        		$("#findpassword-tips").html(data.account).show(500);
        		//$("#id_account").focus();
        	}else if(data.captcha){
        		$("#findpassword-tips").html(data.captcha).show(500);
			}else if(data.email_ue){
        		$("#findpassword-tips").html(data.email_ue).show(500);
        	}else if(data.mobile){
				$("#findpassword-tips").html(data.mobile).show(500);
			}else{
        		if($("#id_account").val().indexOf("@") > 0 ){
                    $("#findpassword-tips").html("找回密码邮件已发送").show(500);
                }else{
                    if(data.status == 'failure') {
						$('#mobile_code_password_form_message').html("手机短信验证码发送失败！");
					}else{
						$('#mobile_code_password_form_message').html("手机短信验证码已发送，请查收！");
						show_send_sms(60);
                    }
                    $('#id_mobile' +
						'_f').val($("#id_account").val());
                    $('#forgetpswModal').modal('hide');
                    $('#forgetpswMobileModal').modal('show');
                }
        	}
        	
            // if(data.account){
            //     $("#findpassword-tips").html(data.account).show(500);
            //     $("#id_account").focus();
            // }else if(data.captcha){
            //     $("#findpassword-tips").html(data.captcha_f).show(500);
            //     $("#id_captcha_f_1").focus();
            //     if(data.captcha_f == "验证码错误")
            //         refresh_captcha({"data":{"form_id":"find_password_form"}});
            // }else{
            //     if($("#id_account").val().indexOf("@") > 0 ){
            //         $("#findpassword-tips").html("找回密码邮件已发送").show(500);
            //     }else{
            //         if(data.status == 'success'){
            //             $('#mobile_code_password_form_message').html("手机短信验证码已发送，请查收！");
            //         }else if(data.status == 'failure'){
            //             $('#mobile_code_password_form_message').html("手机短信验证码发送失败！");
            //         }
            //         $('#id_mobile_f').val($("#id_account").val());
            //         $('#forgetpswModal').modal('hide');
            //         $('#forgetpswMobileModal').modal('show');
            //     }
            //     refresh_captcha({"data":{"form_id":"find_password_form"}});
            // }
        },
        complete: function(XMLHttpRequest){
            $("#findpassword_btn").html("提交");
            $("#findpassword_btn").removeAttr("disabled");
        }
    });
}

//手机验证码表单验证
function mobile_code_password_form_submit(){
    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/password/find/mobile/",
        data:$('#mobile_code_password_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#mobile_code_password_btn").html("提交中...")
            $("#mobile_code_password_btn").attr("disabled","disabled")
        },
        success: function(data) {
            if(data.mobile_code_f){
                $("#mobile_code_password-tips").html(data.mobile_code_f).show(500);
                $("#id_mobile_code_f").focus();
            }else if(data.status == "success"){
                //忘记密码跳转到修改密码的界面前的合法性验证
                account = $("#id_account").val();
                code = $("#id_mobile_code_f").val();
                location.href="/user/password/reset/"+account+"/"+code;
            }
        },
        complete: function(XMLHttpRequest){
            $("#mobile_code_password_btn").html("提交");
            $("#mobile_code_password_btn").removeAttr("disabled");
        }
    });
}
//重发送短信验证码计时
var sendOFF = true;
function show_send_sms(time){
    $("#send-verify").html("重发验证码（" + time + "s）").css({'background':'#D6D6D6'}).attr("disabled","disabled");
    if(time<=0){
        clearTimeout(send_sms_time);
        $(".verify-tips.success").hide(500);
        $("#send-verify").html("重发验证码").css({'background':'#5ECFBA'}).removeAttr("disabled");
        sendOFF = true;
        return;
    }
    time--;
    send_sms_time = setTimeout("show_send_sms("+time+")", 1000);
}

//发送手机验证码

function send_sms_code(form_id,tips_id){
    //hash_key,code
    // if($("#id_captcha_m_1").val()==''){
    //     $("#"+tips_id).html("图片验证码不能为空").show(500); return;
    // }

    show_send_sms(60);
	var mobileVal = $('#id_mobile_code').val();
	var mobile_way = '';
	if(mobileVal == '' || mobileVal == undefined){
		mobileVal = $('#id_mobile_f').val();
		mobile_way = 'change';
	}
    if(sendOFF){
    	$.ajax({
    	    cache: false,
    	    type: "POST",
    	    url:"/user/register/mobile/sendsms_signup/",
    	    data:{
    	    	'mobile': mobileVal,
    	    	'geetest_challenge': $('.geetest_challenge').attr('value'),
    	    	'geetest_validate': $('.geetest_validate').attr('value'),
    	    	'geetest_seccode': $('.geetest_seccode').attr('value'),
				'way': mobile_way
    	    },
    	    async: true,
    	    success: function(data){
    	    	//console.log(data)
    	    	       	
    	        if(data.mobile){
					if(mobile_way != ''){
						$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.mobile);
					}else{
						$(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
					}
    	        }else if(data.captcha){

					if(mobile_way != ''){
						$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.captcha);
					}else{
						$(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
					}
    	        }else if(data.status == 'success'){
					if(mobile_way != ''){
						$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('');
					}else{
						$(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
    	            	show_send_sms(60);
					}

    	        }else if(data.status == 'failure'){

					if(mobile_way != ''){
						$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('请稍后再试');
					}else{
						$(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
					}
    	        }
    	    },
    	    complete: function(XMLHttpRequest){
    	        $("#send-verify").html("重发验证码");
    	        $("#send-verify").removeAttr("disabled");
    	    }
    	});

    	sendOFF = false;
    }
    
}
//登录表单提交
function login_form_submit(tips_id){

    $.ajax({
        cache: false,
        type: "POST",
        url:"/user/login/",
        data:$('#login_form').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $("#login_btn").html("登录中...");
            $("#login_btn").attr("disabled","disabled");
        },
        success: function(data) {
            if(data.account_l){
                $("#login-form-tips").html(data.account_l).show(500);
                $("#id_account_l").focus();
            }else if(data.password_l){
                $("#login-form-tips").html(data.password_l).show(500);
                $("#id_password_l").focus();
            }else{
                if(data.status == "success"){
					if(data.onepay_status == 'True'){
						window.location.replace('/');
					}else {
						window.location.replace(data.url);
					}
                    if(detect_ie() !== false) {
                        window.location.reload();
                    }
                    //window.location.href = "/user/center";
                    return;
                }else if(data.status == "failure"){
                    if(data.msg=='no_active'){
                        zyemail=$("#id_account_l").val();
                        zyUname=zyemail;
                        zy_validate_Email(false,zyemail,$("#id_password_l").val());

                    }
                    else
                        $("#login-form-tips").html("账号或者密码错误，请重新输入").show(500);
                }
            }
        },
        complete: function(XMLHttpRequest){
            $("#login_btn").html("登录");
            $("#login_btn").removeAttr("disabled");
        }
    });

}
//注册表单提交
var current_register_form = "mobile_register_form";
function change_form(to_form_id){
    $("#register-tips").hide()
    current_register_form = to_form_id;
}
//zhouyi
var zyemail="";
var zyUname="";
var hash={
    'qq.com': 'http://mail.qq.com',
    'gmail.com': 'http://mail.google.com',
    'sina.com': 'http://mail.sina.com.cn',
    '163.com': 'http://mail.163.com',
    '126.com': 'http://mail.126.com',
    'yeah.net': 'http://www.yeah.net/',
    'sohu.com': 'http://mail.sohu.com/',
    'tom.com': 'http://mail.tom.com/',
    'sogou.com': 'http://mail.sogou.com/',
    '139.com': 'http://mail.10086.cn/',
    'hotmail.com': 'http://www.hotmail.com',
    'live.com': 'http://login.live.com/',
    'live.cn': 'http://login.live.cn/',
    'live.com.cn': 'http://login.live.com.cn',
    '189.com': 'http://webmail16.189.cn/webmail/',
    'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
    'yahoo.cn': 'http://mail.cn.yahoo.com/',
    'eyou.com': 'http://www.eyou.com/',
    '21cn.com': 'http://mail.21cn.com/',
    '188.com': 'http://www.188.com/',
    'foxmail.coom': 'http://www.foxmail.com'
};
function zy_validate_Email(bo,zyem,upwd){
    var zybo1=true;
    if(!bo) {
        $("#emailValidate .close").unbind().click(function(){
            $('#emailValidate').modal('hide');
            login_form_ajax(zyem,upwd);
        })
        $('#registerModal').modal('hide');
        $('#addemailModal').modal('hide');
        $('#emailValidate').modal('show');
        var zya=$(".zy_email .a>a");
        var url = zyem.split('@')[1];
        zya.attr("href",hash[url]);
        $("#emailValidateEE span").html(zyem);
        if(undefined==hash[url] || hash[url]==null){
            zya.parent().hide();
        }
        zybo1=false;
    }
    else{
        zybo1=true;
    }
    return zybo1;
}
//zhouyi:7-30  验证邮件倒计时
var zy_c_num=60;
var zy_str="";
function zy_Countdown(){
    zy_c_num--;
    $(".sendE2 span").html(zy_c_num+"s");
    $(".zy_success span").html(zy_str);
    (zy_c_num<58)&&$(".zy_success").addClass("upmove");
    if(zy_c_num<=0){
        zy_c_num=60;
        $(".sendE2").hide();
        $(".sendE").show()
        return false;
    }
    setTimeout("zy_Countdown()",1000);
}
var askArr={"aaa":{"嵌入式驱动开发":"/course/qrsqd-px/","物联网开发":"/course/iot-px/"},
    "aab":{"产品经理":"/course/pm-px/"},
    "aba":{"Python Web开发":"/course/python-px/","PHP Web开发":"/course/php-px/","Java Web开发":"/course/java-px/"},
    "aab":{"产品经理":"/course/pm-px/"},
    "abb":{"软件测试":"/course/te-px/"},
    "baa":{"Cocos2d-x手游开发":"/course/cocos2d-x-px/"},
    "bab":{"Android应用开发":"/course/android-px/","iOS应用开发":"/course/ios-px/"},
    "bba":{"游戏原画设计":"/course/yuanhua-px/"},
    "bbb":{"Web前端开发":"/course/web-px/"}
}
function openpingce(){
    $('#pingce').modal('show');
    $(".zy_pingce_con ul").css("left","0px");
    $(".zy_pingce_con ul .cl").removeClass("cl");
}
function scrollGO(){
    $('#pingceSuccess').modal('hide');
    $('html,body').stop().animate({scrollTop: '10000px'}, 800);
}

//拖拽验证
var captchaObjF,captchaObjF2,captchaObjF3;
var captcha = function(obj,ty){
    var setting = {
        obj: obj,
        ty:ty
    };
    if(setting.ty == undefined){
      setting.ty = '';
    }
    var handler = function (captchaObj) {
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo(setting.obj);
        captchaObj.onSuccess(function(){
            $('.tab-pane.active .captcha').siblings('.v_sign_tips').removeClass('error').html('').show(500);
        });
        if(setting.ty=="mobile/"){
        	captchaObjF=captchaObj;
        }else if(setting.ty==""){
        	captchaObjF3=captchaObj;
        }else{
    		captchaObjF2=captchaObj;
    	}
    };
    $.ajax({
        // 获取id，challenge，success（是否启用failback）
        url: "/geetest/getcaptcha/"+setting.ty,
        type: "get",
        dataType: "json", // 使用jsonp格式
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数，与创建Geetest实例时接受的参数一致
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "float", // 产品形式
                offline: !data.success,
            }, handler);
        }
    });
};
function detect_ie() {
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE ');
    var trident = ua.indexOf('Trident/');

    if (msie > 0) {
        // IE 10 or older => return version number
        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
    }

    if (trident > 0) {
        // IE 11 (or newer) => return version number
        var rv = ua.indexOf('rv:');
        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
    }

    // other browser
    return false;
}