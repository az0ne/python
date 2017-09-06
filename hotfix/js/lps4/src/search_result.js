define(function (require, exports, module) {
    var $ = require('jquery');

    $(".search_result .ad span").click(function(){
        $(this).parent().stop().slideUp(300);
    });

    $(".search_result_right .course a").hover(function(){
        $(this).parent("li").addClass("active").siblings("li").removeClass("active");
    },function(){
    });
});
