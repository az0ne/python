// $(".toolbar-item-weibo").hover(function () {
//         $(".lixianB_B").show();
//         $('.lixianB_B').animate({right: '0'});
//     }, function () {
//         $('.lixianB_B').animate({right: '-160px'});
//         $(".lixianB_B").hide();
//     }
// )


// $('.msg').hover(function () {
//     $('.hidemsg').css("display","block");
// },function () {
//      $('.hidemsg').css("display","none");
// })


$('.mobel').hover(function () {
    $('.mobel img').attr("src", "/static/images/toolbarbox/mobelHover.png");
    $('.hidemobelBox').css("display","block");
}, function () {
    $('.mobel img').attr("src", "/static/images/toolbarbox/mobel.jpg");
    $('.hidemobelBox').css("display","none");
})
$('.Rtop').hover(function () {
    $('.Rtop img').attr("src", "/static/images/toolbarbox/RtopHover.png");
    $('.hideRtop').css("display","block");
}, function () {
    $('.Rtop img').attr("src", "/static/images/toolbarbox/Rtop.jpg");
    $('.hideRtop').css("display","none");
})

