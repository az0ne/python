/**
 * Created by Administrator on 2016/6/3.
 */
    $(function(){
        var teacherRecruitFlowTop,teacherRecruitFlow = $(".teacherRecruitFlow");
        teacherRecruitFlowTop = teacherRecruitFlow.position().top-(teacherRecruitFlow.height()+360);
        if($(window).scrollTop()>teacherRecruitFlowTop){
            teacherRecruitFlowAnimate();
        };
        $(window).scroll(function(){
            if($(window).scrollTop()>teacherRecruitFlowTop){
                teacherRecruitFlowAnimate();
            };
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
    });
    function teacherRecruitFlowAnimate(){
        var teacherRecruitFlowLeftNum,teacherRecruitFlowOli = $(".teacherRecruitFlow .detail li");
        for(var i=1;i<=teacherRecruitFlowOli.length;i++){
            teacherRecruitFlowLeftNum = 42+(i-1)*294;
            teacherRecruitFlowOli.eq(i-1).animate({"left":teacherRecruitFlowLeftNum},i*50);
        }
    }
