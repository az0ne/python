/**
 * Created by momax on 2017/6/26.
 */

window.onload = function() {
    $('#data-search').focus(function () {
        $('.hot-words').fadeOut(300);
    });
    $('.header-search, .search-btn').on('click', function (e) {
        var e = e || event;
        e.stopPropagation();
    })
    $(document).on('click', function (e) {
        $('.hot-words').fadeIn(300);
    });

};
    // 视频介绍
    var $videoIntroduce = $('.video_introduce1');

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


//动画效果
function AnimateFun(obj){
    obj.css('left' , ($(window).width() - obj.outerWidth())/2 );
    obj.stop().animate({'top' : ($(window).height() - obj.outerHeight())/2 + $(window).scrollTop()}, 300);
}



// 诸葛IO统计

//搜索栏 关键词
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

