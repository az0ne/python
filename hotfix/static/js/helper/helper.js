function helper(opt){
	var HTML = document.documentElement;
	var BODY = document.body;
	var oBODY = $(BODY);
	var helperBox = $('<div class="helper-box">');
	var mt=$('<div class="helper-m">'), ml = mt.clone(), mr = mt.clone(), mb = mt.clone();
	var area = $('<div class="helper-area">');
	var close = $('<i class="helper-close">').html('&nbsp;');
	var cnt = null;
	var cutSet = null;

	mt.addClass('helper-mt');
	ml.addClass('helper-ml');
	mr.addClass('helper-mr');
	mb.addClass('helper-mb');

	close.click(function(){
		run.close();		
	});

	function run(opt){
		cutSet = opt;
		var H = BODY.scrollHeight, W = BODY.scrollWidth, key = 'animate';

		if( mt[ 0 ].parentNode !== helperBox[ 0 ] ){
			$(HTML).css({ minWidth : W, minHeight : H });
			helperBox.append( mt,ml,mr,mb,area,close );
			oBODY.append( helperBox );
			key = 'css';
		}
		helperBox.css({ height : BODY.scrollHeight })

		cnt && cnt.remove();
		cnt = $( opt.cnt && opt.cnt );
		if( cnt.length && cnt[0].parentNode !== helperBox[ 0 ] ){
			helperBox.append( cnt );
		}		

		var top = testFn( opt.top );
		var left = testFn( opt.left );
		var width = testFn( opt.width );
		var height = testFn( opt.height );
		var scrollTop = testFn( opt.scrollTop );

		if( key === 'css' ){
			mt.css({ height : top });
			ml.css({ top : top, width : left, height : height });
			mr.css({ top : top, height : height, left : left + width});
			//mb.css({ height : H - top - height });
			mb.css({ top : top + height });
			area.css({ top : top, width : width, height: height, left: left });
		}else{
			area.animate({ top : top, width : width, height: height, left: left },{ step : function(a,b){
				a = Math.round(a);
				if( b.prop == 'top' ){
					mt.css( 'height' , a );
					ml.css( 'top' , a );
					mr.css( 'top' , a );
					mb.css( 'top' , a + ml[0].clientHeight );
					//mb.css( 'height' , H - a - area[0].clientHeight );
				}
				if( b.prop == 'left' ){
					ml.css( 'width' , a );
					mr.css( 'left' , a + area[0].clientWidth );
				}
				if( b.prop == 'height' ){
					ml.css( 'height' , a );
					mr.css( 'height' , a );
					mb.css( 'top' , a + parseInt( ml.css( 'top' ) ) );
					//mb.css( 'height' , H - parseInt( area.css( 'top' ) ) - a );
				}
				if( b.prop == 'width' ){
					mr.css( 'left' , parseInt( area.css( 'left' ) ) + a );
				}
				
			}, complete : function(){
				mt.css({ height : top });
				ml.css({ top : top, width : left, height : height });
				mr.css({ top : top, height : height, left : left + width});
				//mb.css({ height : H - top - height });
				mb.css({ top : top + height });
			}});
			/*mt.animate({ height : top }, { progress : function(a,b,c){
				console.log( a + ',' +b +',' + c );
			} });
			ml.animate({ top : top, width : left, height : height });
			mr.animate({ top : top, height : height, left : left + width});
			mb.animate({ height : H - top - height });
			area.animate({ top : top, width : width, height: height, left: left });*/
		}
			
		if( 'number' == $.type( scrollTop ) ){
			if( 'css' == key ){
				$('html,body').scrollTop( scrollTop );
			}else{
				$('html,body').animate( { scrollTop : scrollTop } );
			}
		}

		'function' == $.type( opt.callback ) && opt.callback( helperBox, cnt, area,{ W : W, H : H, top : top, left : left, width : width, height: height } );

		return run;
	}

	run.close = function(b){
		if( close[0].parentNode == helperBox[0] ){
			helperBox.remove();
		}
		if( b !== false ){
			$('.page-bottom-fix').slideDown();
		}
	};

	function testFn(fn,v){
		if( 'function' === $.type( fn ) ){
			return fn();
		}
		if( v !== undefined ){
			return v;
		}else{
			return fn;
		}
	}

	$( window ).resize(function(){
		cutSet && run( cutSet );
	});

	return run( opt );
}

$(window).load(function(){
	var chartContainer = $('#chart-container');
	var stp = null;
	stp1();
	function stp1(){
		stp = helper({
			top : function(){ return chartContainer.offset().top||0 },
			left : function(){ return chartContainer.offset().left||0 },
			width : function(){ return chartContainer[ 0 ].clientWidth||0 },
			height : function(){ return chartContainer[ 0 ].clientHeight||0 },
			scrollTop: 0,
			cnt : html( '我的学习计划能帮助你对整个学习计划进行全局概括，学习完成情况轻松掌握！', 'bc' ),
			callback:function(box,cnt,area,setting){
				cnt.css({ left : '50%', marginLeft : - cnt.outerWidth() / 2, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp2();
				});
			}
		});
	}
	function stp2(){
		stp({
			top : function(){ return chartContainer.offset().top + 58 ||0 },
			left : function(){ return chartContainer.offset().left + 128 ||0 },
			width : 45,
			height : 45,
			cnt : html( '绿点为您的学习计划点，也就是您奋斗的目标哦~' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - cnt.outerWidth()*0.25 + 15, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp3();
				});
			}
		});
	}
	function stp3(){
		stp({
			top : function(){ return chartContainer.offset().top + 213 ||0 },
			left : function(){ return chartContainer.offset().left + 128 ||0 },
			width : 45,
			height : 45,
			cnt : html( '黄点为您的学习实际点，随着您努力地学习，它也会逐渐向学习计划靠近哦~<br /><small>如果您最近实在太忙无法抽出时间学习课程，可以向老师申请请假的哦~</small>' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - cnt.outerWidth()*0.25 + 15, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp4();
				});
			}
		});
	}
	function stp4(){
		var ps_04 = $('.helper-ps-04');
		stp({
			top : function(){ return ps_04.offset().top - 60 ||0 },
			left : function(){ return ps_04.offset().left - 30 ||0 },
			width : ps_04.width() + 60,
			height : ps_04.height() + 100,
			scrollTop : 300,
			cnt : html( '通常一套职业课程是由四到五个阶段组成的，他们是您从菜鸟到大神的必经之道哦~' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp5();
				});
			}
		});
	}
	function stp5(){
		var ps_05 = $('.helper-ps-05');
		stp({
			top : function(){ return ps_05.offset().top - 20 ||0 },
			left : function(){ return ps_05.offset().left - 20 ||0 },
			width : ps_05.width() + 68,
			height : ps_05.height() + 92,
			scrollTop : 630,
			cnt : html( '您可以通过“课程学习”快速进入到课程的学习，也可以在这里快速查看到自己课程学习的完成情况哦~' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp6();
				});
			}
		});
	}
	function stp6(){
		var ps_06 = $('.helper-ps-06');
		stp({
			top : function(){ return ps_06.offset().top - 50 ||0 },
			left : function(){ return ps_06.offset().left - 20 ||0 },
			width : ps_06.width() + 68,
			height : ps_06.height() + 92,
			cnt : html( '看完课程后，对自己的学习结果进行检验是很重要的学习步骤哦！' ),
			scrollTop: 650,
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - 60, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp7();
				});
			}
		});
	}
	function stp7(){
		var ps_07 = $('.helper-ps-07');
		stp({
			top : function(){ return ps_07.offset().top - 20 ||0 },
			left : function(){ return ps_07.offset().left - 20 ||0 },
			width : ps_07.width() + 68,
			height : ps_07.height() + 92,
			scrollTop: 630,
			cnt : html( '除了基础的知识点，真实的实践能力也是至关重要的哦。赶快运用掌握的知识点自己写一个小小的Demo吧~', 'bc' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - 230 + setting.width / 2, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp8();
				});
			}
		});
	}
	function stp8(){
		var ps_08 = $('.helper-ps-08');
		stp({
			top : function(){ return ps_08.offset().top - 50 ||0 },
			left : function(){ return ps_08.offset().left - 20 ||0 },
			width : ps_08.width() + 68,
			height : ps_08.height() + 92,
			cnt : html( '学完一个课程后，需要对自己的理论知识做一次系统地检验和巩固哦~', 'bc' ),
			scrollTop: 650,
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - 230 + setting.width / 2, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp9();
				});
			}
		});
	}
	function stp9(){
		var ps_09 = $('.helper-ps-09');
		stp({
			top : function(){ return ps_09.offset().top - 20 ||0 },
			left : function(){ return ps_09.offset().left - 20 ||0 },
			width : ps_09.width() + 68,
			height : ps_09.height() + 92,
			scrollTop: 630,
			cnt : html( '老师会将这门课程的所有知识点综合起来给你出一个小小的项目需求，尽自己的最大努力去独立完成吧~', 'bc' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ left : setting.left - 230 + setting.width / 2, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp10();
				});
			}
		});
	}
	function stp10(){
		var ps_10 = $('#rank_ul li:first');
		stp({
			top : function(){ return ps_10.offset().top - 20 ||0 },
			left : function(){ return ps_10.offset().left - 30 ||0 },
			width : ps_10.width() + 60,
			height : ps_10.outerHeight() + 20,
			scrollTop: 450,
			cnt : html( '完成了上述的评测项后，您的学力值会嗖嗖地上涨哦，当然您肯定也会在班级里的同学中名列前茅啦~', 'br' ),
			callback:function(box,cnt,area,setting){
				cnt.width( 450 ).css({ right : setting.W - setting.left - setting.width, top : setting.top - cnt.outerHeight() - 20 }).hide().fadeIn();
				cnt.click(function(){
					stp11();
				});
			}
		});
	}
	function stp11(){
		var ps_10 = $('#rank_ul li:first');
		stp({
			top : function(){ return ps_10.offset().top - 20 ||0 },
			left : function(){ return ps_10.offset().left - 30 ||0 },
			width : 0,
			height : 0,
			cnt : html( '你现在已经对LPS系统有了初步的认识，现在就尽情体验一下这套会让你蜕变的学习管理系统吧！<div style="text-align:center;position:absolute;left:0;width:100%;top:100%"><span style="position:relative;top:20px"><span class="helper-tip-btn helper-agin" style="margin-right:20px">重新引导</span><span class="helper-tip-btn helper-leave">立即体验</span></span></div>'),
			callback:function(box,cnt,area,setting){
				var win = $(window);
				cnt.addClass( 'helper-tip-end' ).width( 450 ).css({ position : 'fixed', left : ( win.width() - cnt.outerWidth()) / 2, top : ( win.height() - cnt.outerHeight() ) / 2 - 40 }).hide().fadeIn();
				cnt.find('.helper-agin').click(function(){
					stp.close(false);
					stp1();
				});
				cnt.find('.helper-leave').click(function(){
					stp.close();
				});
			}
		});
	}


	function html(s,p){
		return '<div class="helper-tip-cnt"><div class="text">' + s +  '</div><i class="helper-tip-arrow helper-tip-arrow-'+ (p?p:'bl') +'"></i><i class="helper-tip-next"></i></div>'
	}
});