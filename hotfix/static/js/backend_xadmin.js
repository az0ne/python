var content = $('#content-block');
var backend  = $('#nav-panel-9 a');

//var url_list = [
//    '/backend/update_video_length_view/',
//    '/backend/join_class_step1/',
//    '/backend/quit_class_step1/',
//    '/backend/change_class_step1/',
//    '/backend/order_list/',
//    '/backend/coupon_list/',
//    '/backend/sync_avatar_view/',
//    '/backend/recommend_reading_index/',
//    '/backend/liveroom_list/',
//    '/backend/msgbox_list/',
//    '/backend/acauser_list/',
//    '/backend/clear_cache/',
//    '/backend/lps2_pay_update/'
//];

var url_list = [
    '/backend/update/video/length/view/',
    '/backend/join/class/step1/',
    '/backend/quit/class/step1/',
    '/backend/change/class/step1/',
    '/backend/order/list/',
    '/backend/coupon/list/',
    '/backend/sync/avatar/view/',
    '/backend/recommend/reading/index/',
    '/backend/liveroom/list/',
    '/backend/msgbox/list/',
    '/backend/acauser/list/',
    '/backend/clear/cache/',
    '/backend/clear/courses_cache/',
    '/backend/lps2/pay/update/'
];

//backend.each(function(index) {
//    //alert(index);
//    $(this).on('click',function(){
//        date = $.ajax({
//            type: "GET",
//            url: url_list[index],
//            dataType: "json",
//            async: false,
//            success: function(data) {
//              content.html(data['html']);
//        }
//      });
//    });
//});
backend.each(function(index) {
    //alert(index);
    $(this).on('click',function(){
        var html = '<iframe height="800px" width="100%" src=" '+url_list[index]+' "></iframe>';
        content.html(html);
    });
});