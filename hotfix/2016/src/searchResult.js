/*! LPS4.0 2016-08-29
*/
$(".search_result .ad span").click(function(){$(this).parent().stop().slideUp(300)}),$(".search_result_right .course a").hover(function(){$(this).parent("li").addClass("active").siblings("li").removeClass("active")},function(){});