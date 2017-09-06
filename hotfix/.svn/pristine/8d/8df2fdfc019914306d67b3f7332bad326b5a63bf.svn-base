window.onload = function(){
    $('#data-search').focus(function(){
        $('.hot-words').fadeOut(300);
    });
    $('.header-search, .search-btn').on('click', function(e){
        var e = e || event;
        e.stopPropagation();
    })
    $(document).on('click', function(e){
        $('.hot-words').fadeIn(300);
    });
    $('.switch>dd').click(function(){
        var name = $(this).attr('name');
        if(!$(this).hasClass('on')){
            $(this).addClass('on').siblings().removeClass('on');
        }
        switch(name){
            case '0':
                $('.coop-etpr-lists>ul').animate({'margin-left':'0'},500);
                break;
            case '1':
                $('.coop-etpr-lists>ul').animate({'margin-left':'-200px'},500);
                break;
        }
    });

    // 按需加载
    //var aImg = $('.main-con-inner img');
    //showImage();
    
    window.onscroll = function(){
        //showImage();
        Ceiling();
    };
    
    // function showImage() {        
    //     var scrollTop  = document.documentElement.scrollTop || document.body.scrollTop;
        
    //     for (var i=0; i<aImg.length; i++) {
            
    //         if ( !aImg[i].isLoad && getTop(aImg[i]) < scrollTop + document.documentElement.clientHeight ) {
    //             aImg[i].src = aImg[i].getAttribute('_src');
    //             aImg[i].isLoad = true;
    //         }
            
    //     }        
    // }
    
    // function getTop(obj) {
    //     var iTop = 0;
    //     while(obj) {
    //         iTop += obj.offsetTop;
    //         obj = obj.offsetParent;
    //     }
    //     return iTop;
    // }

    // 精品课程推荐
    goodLesson();
    // 左侧菜单
    navHover();
    $(window).on('resize',function(){
        navHover();
        setWidth();
    });
    var headH = $('.head-container').outerHeight();
    Ceiling();
    window.onresize = Ceiling;
    function Ceiling(){
        var scrtop = $(document.documentElement).scrollTop() || $(document.body).scrollTop();

        if(scrtop + 70 > headH){
            $('.hidden-box').stop().animate({
                'height':'0px'
            }, 300);
        }else{
            $('.hidden-box').stop().animate({
                'height':'70px'
            }, 300);
        }
    }
    // 视频介绍
    var $videoIntroduce = $('.video_introduce');

    $videoIntroduce.find('a').on('click', function(){
        var mask = $('<div class="modal-mask"></div>');
        var dialog = $('<div class="dialog"><video id="video_introduce" autoplay preload="none" width="100%" height="100%" src="'+ $(this).attr('data-href') +'"></video><a class="off" href="javascript: void(null);"></a></div>');
        
        $('body').append(mask);
        $('body').append(dialog);        
        AnimateFun(dialog);        
        
        $('.off').on('click', function(){   
            $(mask).remove();
            $(dialog).remove();            
        });        
        
        $(window).on('resize scroll',function(){
            AnimateFun(dialog);    
        });        
    });
    // 轮播图
    $(".slide").slide({
        titCell:".slide-tab",
        mainCell:".slide-box ul",
        autoPage:true,
        effect:"fold",
        autoPlay:true,
        trigger:"click",
        interTime: 5000
    });
    // 金牌讲师
    $(".gold-teacher").slide({
        titCell:".gold-tab",
        mainCell:".gold-slide ul",
        autoPage:true,
        effect:"leftLoop",
        scroll:4,
        vis:4,
        trigger:"click"
    });
    var $ul = $('#gold-list');
    var Time = 500;
    $ul.find('.inner-box').hover(function(){
        $(this).find('.hover-mask, .hover-card').stop().fadeIn(Time);
        $(this).next('h5').animate({
            'opacity': '0'
        },Time);
        $(this).find('.teach-icon').stop().animate({
            'bottom': '-32px',
            'opacity': '1'
        },Time);
    },function(){
        $(this).find('.hover-mask, .hover-card').stop().fadeOut(Time);
        $(this).next('h5').animate({
            'opacity': '1'
        },Time);
        $(this).find('.teach-icon').stop().animate({
            'bottom': '60px',
            'opacity': '0'
        },Time);
    });
    // 获得奖项
    $(".cooperate").slide({
        titCell:".slide-tab",
        mainCell:".cooperate-slide ul",
        autoPage:true,
        effect:"leftLoop",
        trigger:"click"
    });
    jobPath();
}

function navHover(){
    var doc = ($(document.documentElement) || $(document.body)).width();        
    if(doc < 1349){
        $('.side-bar').hover(function(){
            $(this).stop().animate({
                'width':'168px'
            },300);
            $('.w1920').stop().animate({
                'left':'0'
            },300);        
        },function(){
            $(this).stop().animate({
                'width':'33px'
            },300);
            $('.w1920').stop().animate({
                'left':'-168px'
            },300);        
        });
    }else{
        $('.side-menu').removeAttr('style');
        $('.side-bar').unbind();
    }
}
//设置slider宽度
function setWidth(){
    var $parentWidth=$('.slide-box').width();
    $('.slide-box>ul').css("width",$parentWidth);
    $('.slide-box>ul>li').css("width",$parentWidth);
}

function AnimateFun(obj){
    obj.css('left' , ($(window).width() - obj.outerWidth())/2 );
    obj.stop().animate({'top' : ($(window).height() - obj.outerHeight())/2 + $(window).scrollTop()}, 300); 
}

function goodLesson(){
    var $div_li = $('.tab_menu li');
    $div_li.click(function(){
        $(this).addClass('selected').siblings().removeClass('selected');
        var index = $div_li.index(this);
        $('div.tab_box > div').eq(index).show().siblings().hide();
    });
};

function jobPath(){
    var $jobPath = $('.job-path'), $jobTab = $('.job-tab span'), $jobList = $('.job-list');
    $jobTab.eq(0).on('click', function(){
        $jobList.stop().animate({
            'margin-left': '0px'
        }, 500);
        $(this).addClass('select').siblings().removeClass('select');
    });
    $jobTab.eq(1).on('click', function(){
        $jobList.stop().animate({
            'margin-left': '-762px'
        }, 500);
        $(this).addClass('select').siblings().removeClass('select');
    });
};

// 诸葛IO统计
$('.hot-words a').click(function(){
    zhuge.track('热词推荐');
    setTimeout(function(){}, 500);
});

$('.tab_menu li').click(function(){
    zhuge.track('首页精品课程tab的点击次数', {'事件位置': '精品课程','名称': $(this).text()});
});
$('div.tab_box ul li > a').click(function(){
    zhuge.track('首页精品课程的点击数', {'事件位置': '精品课程','课程名称': $(this).find('.title').text()});
});
