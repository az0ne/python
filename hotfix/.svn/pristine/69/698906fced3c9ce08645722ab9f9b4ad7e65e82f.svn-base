$(function () {
    //首页搜索模块
    $(".input-btn").click(function () {
        var scrollHeight = $(".topwrap").height() + $(".index-banner").height() - document.body.scrollTop - 220;
        $("body").css("position", "fixed").animate({top: -scrollHeight}, 300);
        $("#searchwrap").animate({top: "0"}, 600);
        $(".search_txt").val('').focus();
    });
    // 精品课程推荐
    goodLesson();

    TouchSlide({
        slideCell: "#top-banner",
        titCell: ".hd ol",
        mainCell: ".bd ul",
        effect: "left",
        autoPlay: true,
        autoPage: true
    });

    TouchSlide({
        slideCell: '#careers',
        mainCell: "#careers .menu",
        titCell: "#careers .hd ol",
        effect: "leftLoop",
        autoPage: true
    });
    TouchSlide({
        slideCell: '#focus5',
        mainCell: "#focus5 .menu",
        titCell: "#focus5 .hd ol",
        effect: "leftLoop",
        autoPage: true
    });
});

function goodLesson() {
    var $div_li = $('.tab dl dd');
    $div_li.click(function () {
        $(this).addClass('active').siblings().removeClass('active');
        var index = $div_li.index(this);
        $('#good-course > ul').eq(index).show().siblings().hide();
    });
};