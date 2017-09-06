$(function(){
    if($(window).height()<700) {
        var d2 = $(".course > ul > li > div.d2");
        d2.each(function(){
            $(this).html($("<div></div>").html($(this).html()));
        });
        var px,moveN;
        function touchstartBind(e){
            var touch = event.targetTouches[0];
            px=touch.pageX;
            moveN=parseInt($(this).children().css("left"),10);
        }
        function touchmoveBind(e){
            e.preventDefault();
            var touch = event.targetTouches[0];
            $(this).children().css("left",(moveN+touch.pageX-px)+"px");
        }
        function touchendBind(e){
            moveN=parseInt($(this).children().css("left"),10);
            var huh=$(this).children().width()-$(this).width()
            if(moveN>0){
                $(this).children().animate({"left":0},300);
            }
            if(huh>0&&-moveN>huh){
                $(this).children().animate({"left":-huh},300);
            }
            if(huh<=0){
                $(this).children().animate({"left":0},300);
            }
        }
        $(".course > ul > li > div.d2").unbind().bind({
            "touchstart":touchstartBind,
            "touchmove":touchmoveBind,
            "touchend":touchendBind
        });
    }
    $('.course-lists li').stop().hover(function(){
        $(this).find('.description').show();
    },function(){
        $(this).find('.description').hide();
    });
    (function(){
        var slideMore = $('.slide-more'),
            parentLevel = $('.parent-level'),
            childLevel = $('.child-level'),
            len = parentLevel.find('li').length;

        parentLevel.find('li').hover(function(){
            var index = $(this).index();
            if(index >= len -4){
                parentLevel.find('li').css({
                    'position': 'static'
                });
                childLevel.css({
                    'top':'auto',
                    'bottom':'0px'
                });
            }
            
        },function(){
            parentLevel.find('li').css({
                'position': 'relative'
            });
            childLevel.removeAttr('style');
        });

        slideMore.on('click', function(){
            $(this).toggleClass('slide-up');  
            if(!$(this).hasClass('slide-up')){
                parentLevel.find('.None').hide();
            }else{            
                parentLevel.find('.None').show();
            }
        });
    })();
});