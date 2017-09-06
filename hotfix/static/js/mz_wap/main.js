/**
 * Created by Administrator on 2016/3/23.
 */
$(function(){
	$(".ui-imglazyload").picLazyLoad();//图片延迟加载

	//底部上下滑动时显示隐藏
	var p=0,t=0;
    $(window).scroll(function(e){
        p = $(this).scrollTop();
        if(t<=p){
           $("#foot").animate({height:"0"},100);
        }else{
           $("#foot").animate({height:$(this).currentStyle},100)
        }
		t = p;
    });
	
	/*二级页面右边咨询浮动模块*/
	$(".seek-floats span").click(function(){
		$(this).parent().animate({right:"-2.25rem"});
	});
	var rights = $(".seek-floats").css("right");
	setTimeout(function showSeekFloats(){
		$(".seek-floats").animate({right:"0"});
	},1000);
	
	/*筛选*/
	var $el = $(".course-tabs-title span,.course-tabs-content");
	var clicknum=0;
	$el.bind("touchstart",function(e){
		e.stopPropagation();//阻止冒泡
	});
	$(".course-tabs-title span").bind("touchstart",function(e){
		$(".course-tabs-content").animate({bottom:"0"});
		$(this).addClass("active").siblings().removeClass("active");
		$(".course-tabs-content>div").eq($(this).index()).addClass("active").siblings().removeClass("active");
		if(clicknum==0){
			$(".bg").fadeIn();
		}
		clicknum++;
	});
	$(document).bind("touchstart",function(e){
		if(($(e.target) != $el) && ($el.hasClass('active'))){
			$el.removeClass('active');
			$(".course-tabs-content").animate({bottom:"-16.75rem"});
			$(".bg").fadeOut();
		}
		clicknum=0;
	});
	//选中状态--筛选
	$(".tab-lists-tile>li").click(function(){
		$(this).addClass("cur").siblings().removeClass("cur");
		$(".tab-lists>div").eq($(this).index()).addClass("cur").siblings().removeClass("cur");
		$(".lists ul li").removeClass("selecting");
	});
	$(".tab-lists li").click(function(){
		$(this).addClass("selecting").siblings().removeClass("selecting");
		$(".tab-lists span").removeClass("selecting");
	});
	$(".tab-lists span").click(function(){
		$(this).addClass("selecting")
		$(".tab-lists li").removeClass("selecting");
	});
	//热度搜索
	$(".course-tabs-hot li").click(function(){
		$(this).addClass("current").siblings().removeClass("current");
	});

	/***课程库***/
	/*课程章节展开全部*/
	function showList(id,bol){
		var charoLi = $("#"+ id +" li");
		if(charoLi.length>5){
			$("#"+ id +" li" + ":nth-child(n+6)").hide();
		}else{
			$("#"+ id).find(".course-expand").hide();
		}

		$("#"+ id).find(".course-expand").click(function(){
			$("#"+ id +" li" + ":nth-child(n+6)").show(200);
			if(bol === true){
				$("#"+ id +" li").eq(4).css("border-bottom","2px solid #e2e2e2");
			}			
			$(this).hide();
		});
	}
	showList("course-section", true);
	showList("wiki");
});