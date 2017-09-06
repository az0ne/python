

//底部全屏轮播

function footerBannerSlider() {
	$(".footer-banner-c-bd").find("li").eq(0).clone().appendTo($(".footer-banner-c-bd ul"))
	var Len = $(".footer-banner-c-bd").find("li").length;
	var oWidth = $(".footer-banner-c-bd").find("li").width();
	var iNow = 0;
	var Timer;
	var oDesUl = $(".footer-banner-c-bd ul");
	var tmp = ""
	oDesUl.width(Len * oWidth);

	for(var i = 0; i < Len - 1; i++) {
		tmp += "<li></li>";
	}
	$(".footer-banner-c-hd ul").html(tmp);
	$(".footer-banner-c-hd li").eq(0).addClass("active");

	function goNext() {
		if(!oDesUl.is(":animated")) {
			if(iNow < Len - 2) {
				iNow++
				oDesUl.animate({
					"left": -iNow * oWidth
				}, 600)
			} else {
				iNow = 0;
				oDesUl.animate({
					"left": -(Len - 1) * oWidth
				}, 600, function() {
					oDesUl.css("left", 0)
				})
			}
			$(".footer-banner-c-hd").find("li").eq(iNow).addClass("active").siblings().removeClass("active");
		}
	}
	Timer = setInterval(goNext, 2000)
	$(".footer-banner").hover(function() {
		clearInterval(Timer)
	}, function() {
		clearInterval(Timer)
		Timer = setInterval(goNext, 2000)
	})
	$(".footer-banner-c-hd").find("li").on("click", function() {
		iNow = $(this).index() - 1;
		goNext()
	})
}
function goTop() {
	$("html,body").animate({
		"scrollTop": 0
	}, 400)
}
$(function() {
	//点击课程介绍
	var TabTimer;
	var Obtn = true;
	var Timer;
	var oBtn = false;
	var iTop = $(".mzedu-tab").position().top;
	$(".mzedu-tab").find("li").on("click", function() {
		var index = $(this).index();
		$(this).addClass("active").siblings().removeClass("active");
		$(".big-wrap .container01").eq(index).addClass("cur").siblings(".container01").removeClass("cur");
		if(index == 2 && Obtn) {
			Obtn = false;
			clearInterval(TabTimer)
			TabTimer = setTimeout(function() {
				mzWaterfal();
			}, 60)
		}
		$("html,body").animate({
			"scrollTop": iTop
		}, 600)
	});

	//老师图片轮播
	$('#sliderPlay').sliderPlay();
	//	python是什么

	//python学完后能做什么
	var PicBox_left = parseInt($('.pic_box').css('left'));
	var UlLength = $('#pic_box ul').width();
	var SPEED=15;
	function pic_lunbo() {
		PicBox_left--;
		if(PicBox_left <= -UlLength) {
			PicBox_left = 0;
			$('.pic_box').css({ left: '0' });
		} else {
			$('.pic_box').css({ left: PicBox_left });
		}
	}
	var pic_slid = setInterval(pic_lunbo, SPEED);
	$('.main').hover(function(){
		clearInterval(pic_slid);
	},function(){
		clearInterval(pic_slid);
		pic_slid = setInterval(pic_lunbo, SPEED);
	});
	$('#left_btn').click(function(){
		PicBox_left+=140;
		if(PicBox_left >=0) {
			PicBox_left = -UlLength;
			$('.pic_box').animate({ left: PicBox_left });
		} else {
			$('.pic_box').animate({ left: PicBox_left });
		}
	});
	$('#right_btn').click(function(){
		PicBox_left-=140;
		if(PicBox_left <= -UlLength) {
			PicBox_left = 0;
			$('.pic_box').css({ left: '0' });
			$('.pic_box').animate({ left: PicBox_left });
		} else {
			$('.pic_box').animate({ left: PicBox_left });
		}
	});

	//学生轮播
	slider();

	function slider() {
		var oLeft = $("#left-slip");
		var oRight = $("#right-slip");
		var oStuShow = $("#stu-show");
		var sCrollLeft = $(".conbox").find("li").outerWidth(true);
		var oStuShow = $("#stu-show");
		var Html = oStuShow.html();
		oStuShow.append(Html);
		var disLen = oStuShow.find("li").length;
		oStuShow.width(sCrollLeft * disLen);
		var Timer;
		var iNow = 0;
		oRight.click(Next);
		Timer = setInterval(Next, 1000)

		function Next() {
			if(!oStuShow.is(":animated")) {
				if(iNow === 0) {
					iNow--;
					oStuShow.animate({
						left: iNow * sCrollLeft
					}, 1000);
				} else if(iNow === -(disLen / 2)) {
					iNow = 0;
					oStuShow.css({
						left: 0
					});
					iNow--;
					oStuShow.animate({
						left: iNow * sCrollLeft
					}, 1000);
				} else {
					iNow--;
					oStuShow.animate({
						left: iNow * sCrollLeft
					}, 1000);
				}
			}
		};
		oLeft.click(function() {
			if(!oStuShow.is(":animated")) {
				//console.log(iNow);
				if(iNow == 0) {
					iNow = -disLen / 2;
					oStuShow.css("left", iNow * sCrollLeft);
					iNow++;
					oStuShow.animate({
						left: iNow * sCrollLeft
					}, 1000);

				} else {
					iNow++;
					oStuShow.animate({
						left: iNow * sCrollLeft
					}, 1000);
				}
			}
		});
		$("#top").hover(function() {
			clearInterval(Timer)
		}, function() {
			clearInterval(Timer);
			Timer = setInterval(Next, 1000);
		})
	}
	$(window).scroll(function() {
		if($(this).scrollTop() >= iTop) {
			$("body").addClass("mzedu-tab-fiexd")
		} else {
			$("body").removeClass("mzedu-tab-fiexd")

		}
	});
})

//底部全屏轮播
$(function() {

	var n = 0;
	var $btn = $('.list-btn li');
	var $assbox = $('.assess-box');
	var $inner = $('.innerbox');
	var timer;

	function autoplay() {

		$inner.animate({
			"margin-left": (-800 * n) + 'px'
		}, 500);
		$btn.eq(n).addClass('active').siblings().removeClass('active');
		n++;
		if(n > 2) {
			n = 0;
		}
		timer = setTimeout(autoplay, 4000);
	}

	$assbox.hover(function() {
		clearTimeout(timer);
	}, function() {
		timer = setTimeout(autoplay, 4000);
	});

	$btn.click(function() {
		$(this).addClass('active').siblings().removeClass('active');
		n = $(this).index();
		$inner.animate({
			"margin-left": (-800 * n) + 'px'
		}, 500);
	})

	autoplay();

});