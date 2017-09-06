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
	var secondm=40;
	$(".zy_srean_close").unbind().click(function(){
		$(".zy_srean").hide();
		if(secondm>60) return;
		setTimeout(function(){$(".zy_srean").show();},secondm*1000);
		secondm+=20;
	});
	setTimeout(function(){
		$(".zy_srean").show();
	},10000)
	var bbb=true;
	$(".zy_srean").unbind().click(function(){
		(bbb)&&$(".zy_srean_close").trigger("click");
	});
	$(".zy_srean_div").hover(function(){
		bbb=false;
	},function(){
		bbb=true;
	})

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
		$(this).parent().next().toggle()
		var nshow = $(this).parent().next();
		if (nshow.is(":hidden")) {
			$(this).html("查看详情");
			$(this).css("text-align","left");
			$(this).css("text-indent","0");
			$(this).css("background-position","0 0");
		}
		else {
			$(this).html("收起");
			$(this).css("text-indent","16px");
			$(this).css("background-position","0 -30px");
		}
	})
	
})

