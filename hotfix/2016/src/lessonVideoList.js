/*! LPS4.0 2016-08-29
*/
function init(){var e=$(".footer-ad"),t=$(".tab_menu li span");t.on("click",function(){$(this).parent().addClass("active").siblings().removeClass("active");var e=t.index(this);$(".tab_box > div").eq(e).show().siblings().hide()}),e.find("i").on("click",function(){e.hide()})}init();