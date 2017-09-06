/**
 * Created by Administrator on 2016/6/3.
 */
define(function(require, exports, module) {
    var $ = require('jquery');
    require('./bxslider.js')($);
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

        teacher();
    });
    /*
     * 金牌讲师
     * @
     * @
     */
    function teacher(){
        var LiLength = $('.gold_teacher .bxslider li').not(".bx-clone").length > 4;
        $('.gold_teacher .bxslider').bxSlider({
            mode: 'horizontal',
            auto: false,
            slideWidth: 288,
            maxSlides: 4,
            slideMargin: 15,
            hideControlOnEnd: true,
            pager: LiLength ? true : false
        });
    }
    function teacherRecruitFlowAnimate(){
        var teacherRecruitFlowLeftNum,teacherRecruitFlowOli = $(".teacherRecruitFlow .detail li");
        for(var i=1;i<=teacherRecruitFlowOli.length;i++){
            teacherRecruitFlowLeftNum = 42+(i-1)*294;
            teacherRecruitFlowOli.eq(i-1).animate({"left":teacherRecruitFlowLeftNum},i*50);
        }
    }
});
