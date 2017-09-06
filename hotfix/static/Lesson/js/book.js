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
	document.getElementById("home").style.height=winHeight-90+"px";
}
findDimensions();
function getExplorer() {
	var explorer = window.navigator.userAgent ;
	if (explorer.indexOf("MSIE") >= 0) {
		var ienum=parseInt(explorer.split(";")[1].split(" ")[2],10);
		if(ienum<9){
			$(".Edition").addClass("scaleShow");
		}
	}
}
getExplorer();
var sbo=false;
$(function(){
	$(window).resize(function(){
		findDimensions();
		mTop=$(".section1").height();
	});
	window.requestAnimFrame = function(){
		return (
			window.requestAnimationFrame       || 
			window.webkitRequestAnimationFrame || 
			window.mozRequestAnimationFrame    || 
			window.oRequestAnimationFrame      || 
			window.msRequestAnimationFrame     || 
			function(/* function */ callback){
				window.setTimeout(callback, 1000 / 60);
			}
		);
	}();

	window.cancelAnimFrame = function(){
		return (
			window.cancelAnimationFrame       || 
			window.webkitCancelAnimationFrame || 
			window.mozCancelAnimationFrame    || 
			window.oCancelAnimationFrame      || 
			window.msCancelAnimationFrame     || 
			function(id){
				window.clearTimeout(id);
			}
		);
	}();
	
	
	var mTop=$(".section1").height();
	$(".mouseBottom").click(function(){
		$('html,body').animate({scrollTop: mTop+90+'px'}, 500);
	});
	var zyTop=$(window).scrollTop();
	var pyHeight=winHeight/2;
	var s1Top=$(".section1").offset().top,
		s1H=$(".section1").height();
	var s2Top=$(".section2").offset().top,
		s2H=$(".section2").height();
	var s3Top=$(".section3").offset().top,
		s3H=$(".section3").height();
	var s4Top=$(".section4").offset().top,
		s4H=$(".section4").height();
	var s5Top=$(".section5").offset().top,
		s5H=$(".section5").height();
	$(window).scroll(function(e){
		var newtop=$(this).scrollTop();
		if(newtop>=90){
			sbo=true;
		}
		else{
			$(".top2").slideUp();
			zyTop=newtop-1;
			sbo=false;
		}
		if(newtop>=s1Top&&newtop<s1Top+s1H-pyHeight){
			sbo=false;
			$(".top_menu a[href='#home']").addClass("aH").siblings().removeClass("aH");
		}
		if(newtop>=s2Top-pyHeight&&newtop<s2Top+s2H-pyHeight){
			$(".section2").addClass("background100");
			$(".top_menu a[href='#service']").addClass("aH").siblings().removeClass("aH");
		}
		if(newtop>=s3Top-pyHeight&&newtop<s3Top+s3H-pyHeight){
			$(".top_menu a[href='#products']").addClass("aH").siblings().removeClass("aH");
		}
		if(newtop>=s4Top-pyHeight&&newtop<s4Top+s4H-pyHeight){
			$(".top_menu a[href='#team']").addClass("aH").siblings().removeClass("aH");
		}
		if(newtop+winHeight>=s5Top&&newtop+winHeight<s5Top+s5H){
			$(".top_menu a[href='#contact']").addClass("aH").siblings().removeClass("aH");
		}
	});
	var mySwiper = new Swiper('.swiper-container1',{
		slidesPerView: 'auto',
		grabCursor: true,
		mousewheelControl:true,
		//Enable Scrollbar
		scrollbar: {
		  container: '.swiper-scrollbar',
		  hide: false,
		  draggable: true,
		  snapOnRelease: true
		}
	});
	 var mySwiper2,Swiperbo=true;
	$('.sreenArrenPrev').unbind().bind('click', function(e){
		e.preventDefault()
		mySwiper2.swipePrev()
	})
	$('.sreenArrenNext').unbind().bind('click', function(e){
		e.preventDefault()
		mySwiper2.swipeNext()
	})
	$(".goTop").click(function(){
		$('html,body').animate({scrollTop:'0px'}, 500);
	});
	$(".small_menu").click(function(){
		$(".small_menu_div").height($(window).height());
		if($(".small_menu_div").css("display")=="none")
			$(".small_menu_div").slideDown();
		else
			$(".small_menu_div").slideUp();
	});
	$(".swiper-container1 .swiper-slide").click(function(){
		$(".sreenDiv1").addClass("scaleShow");
		if(Swiperbo){
			Swiperbo=false;			
			 mySwiper2= new Swiper('.swiper-container2',{
				slidesPerView: 'auto',
				grabCursor: true,
				slidesPerView: 1
			});
		}
		var num=parseInt($(this).attr("num"),10);
		mySwiper2.swipeTo(num,1000,false);
	});
	$(".sreenDiv .close").click(function(){
		$(".sreenDiv1").removeClass("scaleShow");
	});
	$('.start_text').focus(function(){
		$(this).val($(this).val()==$(this).attr('title')?'':$(this).val());		
	}).blur(function(){	
		$(this).val($(this).val()==''?$(this).attr('title'):$(this).val());
	});
	$(".top_menu a").click(function(){
		var id=$(this).attr("href").replace("#","");
		var sc=$("#"+id).offset().top;
		$('html,body').animate({scrollTop: sc+'px'}, 800);
		return false;
	});
	function AnimFrame(){
		if(sbo){
			sbo=false;
			var newTop=$(window).scrollTop();
			if(zyTop==newTop){
			}
			else if(zyTop<newTop){				
				$(".top2").slideUp();
			}
			else{
				console.log("%d+%d",zyTop,newTop)
				$(".top2").slideDown();
			}
			zyTop=newTop;
		}
		window.requestAnimFrame(function(){AnimFrame();});
	}
	AnimFrame();
})