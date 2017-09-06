// JavaScript Document


$(function(){
	$('.more').unbind().click(function(){
            $('#KFLOGO .Lelem').eq(0).trigger('click');
        });
	$(".lixianB").hover(function(){
		$(this).children("div").stop().show("fast");
	},function(){
		$(this).children("div").stop().hide("fast");
	})	
	// var secondm=40;
	// $(".zy_srean_close").unbind().click(function(){
	// 	$(".zy_srean").hide();
	// 	if(secondm>60) return;
	// 	setTimeout(function(){$(".zy_srean").show();},secondm*1000);
	// 	secondm+=20;
	// });
	// setTimeout(function(){
	// 	$(".zy_srean").show();
	// },10000)
	// var bbb=true;
	// $(".zy_srean").unbind().click(function(){
	// 	(bbb)&&$(".zy_srean_close").trigger("click");
	// });
	// $(".zy_srean_div").hover(function(){
	// 	bbb=false;
	// },function(){
	// 	bbb=true;
	// })
	
	$(".play-b1").click(function(){
		$(".video-f1").show();
		$("#video-f1").html('<video autoplay id="example_video_1" class="video-js vjs-default-skin" controls preload="none" width="1000" height="600" poster="" data-setup="{http://www.maizitime.com/pages/loading-pic.jpg}"><source src="http://www.maizitime.com/pages/video/ksrsnew.mp4" type="video/mp4" /><track kind="captions" src="demo.captions.vtt" srclang="en" label="English"></track><track kind="subtitles" src="demo.captions.vtt" srclang="en" label="English"></track></video>')
	})
	$(".c1-btn").click(function(){
		$(".video-f1").hide();
		$("#example_video_1").remove();
	})
	
	$(".play-b2").click(function(){
		$(".video-f2").show();
		$("#video-f2").html('<video autoplay id="example_video_2" class="video-js vjs-default-skin" controls preload="none" width="1000" height="600" poster="" data-setup="{http://www.maizitime.com/pages/loading-pic.jpg}"><source src="http://www.maizitime.com/pages/video/jyhznew.mp4" /><track kind="captions" src="demo.captions.vtt" srclang="en" label="English"></track><track kind="subtitles" src="demo.captions.vtt" srclang="en" label="English"></track></video>')
	})
	$(".c2-btn").click(function(){
		$(".video-f2").hide();
		$("#example_video_2").remove();
	})
	
	$(".play-b3").click(function(){
		$(".video-f3").show();
		$("#video-f3").html('<video autoplay id="example_video_3" class="video-js vjs-default-skin" controls preload="none" width="1000" height="600" poster="" data-setup="{http://www.maizitime.com/pages/loading-pic.jpg}"><source src="http://www.maizitime.com/pages/video/wanghaining.mp4" /><track kind="captions" src="demo.captions.vtt" srclang="en" label="English"></track><track kind="subtitles" src="demo.captions.vtt" srclang="en" label="English"></track></video>')
	})
	$(".c3-btn").click(function(){
		$(".video-f3").hide();
		$("#example_video_3").remove();
	}) 
	
	$(".page-js-list li a.more-btn").click(function(){
		var sdiv = $(this).parent().next();
		var nshow = $(this).parent().next();
		if (nshow.is(":hidden")) {
			$(this).html("收起");
			$(sdiv).show();
			$(sdiv).addClass('zoomInLeft hinge1s');	
			setTimeout(function () {
            $(sdiv).removeClass('zoomInLeft hinge1s');
        }, 1000);
		}
		else {
			$(this).html("查看详情");
			$(sdiv).addClass('rollOut hinge1s');
			setTimeout(function () {
			$(sdiv).removeClass('rollOut hinge1s');
			$(sdiv).hide();
        }, 1000);					
		}
	})
	
})


$(function() {
	/*轮播*/
	var json0 = {
		"width": 57,
		"height": 57,
		"top": 112,
		"left": -300
	};
	var json1 = {
		"width": 154,
		"height": 154,
		"top": 63,
		"left": -198
	}
	var json2 = {
		"width": 205,
		"height": 205,
		"top": 38,
		"left": 0
	}
	var json3 = {
		"width": 278,
		"height": 278,
		"top": 0,
		"left": 246
	}
	var json4 = {
		"width": 205,
		"height": 205,
		"top": 38,
		"left": 573
	}
	var json5 = {
		"width": 154,
		"height": 154,
		"top": 63,
		"left": 824
	}
	var json6 = {
		"width": 57,
		"height": 57,
		"top": 112,
		"left": 1020
	}

	$(".youanniu").click(function() {
		if (!$("#yixing li").is(":animated")) {
			//先交换位置
			$(".no1").stop(true, false).animate(json0, 400);
			$(".no2").stop(true, false).animate(json1, 400);
			$(".no3").stop(true, false).animate(json2, 400);
			$(".no4").stop(true, false).animate(json3, 400);
			$(".no5").stop(true, false).animate(json4, 400);
			$(".no6").stop(true, false).animate(json5, 400);
			$(".no0").css(json6);

			//再交换身份
			$(".no0").attr("class", "denghou");
			$(".no1").attr("class", "no0");
			$(".no2").attr("class", "no1");
			$(".no3").attr("class", "no2");
			$(".no4").attr("class", "no3");
			$(".no5").attr("class", "no4");
			$(".no6").attr("class", "no5");
			//上面的交换身份，把no0搞没了！所以，我们让no1前面那个人改名为no0
			if ($(".no5").next().length != 0) {
				//如果no5后面有人，那么改变这个人的姓名为no6
				$(".no5").next().attr("class", "no6");
			} else {
				//no5前面没人，那么改变此时队列最开头的那个人的名字为no0
				$("#yixing li:first").attr("class", "no6");
			}
			//发现写完上面的程序之后，no6的行内样式还是json0的位置，所以强制：
			$(".no6").css(json6);
		}

	});

	setTime = setInterval(function() {
		$(".youanniu").trigger("click");
	}, 3000)
	$(".slidebox").hover(function() {
		clearInterval(setTime);
	}, function() {
		setTime = setInterval(function() {
			$(".youanniu").trigger("click");
		}, 3000)
	});

	$(".zuoanniu").click(
		function() {
			if (!$("#yixing li").is(":animated")) {
				$(".no0").stop(true, false).animate(json1, 400);
				$(".no1").stop(true, false).animate(json2, 400);
				$(".no2").stop(true, false).animate(json3, 400);
				$(".no3").stop(true, false).animate(json4, 400);
				$(".no4").stop(true, false).animate(json5, 400);
				$(".no5").stop(true, false).animate(json6, 400);
				$(".no6").css(json0);

				$(".no6").attr("class", "denghou");
				$(".no5").attr("class", "no6");
				$(".no4").attr("class", "no5");
				$(".no3").attr("class", "no4");
				$(".no2").attr("class", "no3");
				$(".no1").attr("class", "no2");
				$(".no0").attr("class", "no1");

				//上面的交换身份，把no0搞没了！所以，我们让no1前面那个人改名为no0
				if ($(".no1").prev().length != 0) {
					//如果no1前面有人，那么改变这个人的姓名为no0
					$(".no1").prev().attr("class", "no0");
				} else {
					//no1前面没人，那么改变此时队列最后的那个人的名字为no0
					$("#yixing li:last").attr("class", "no0");
				}

				$(".no0").css(json0);
			}
		}
	);

});

