$(function () {
    // 清空搜索框文本值
    $('.empty').off('click').on('click', function () {
        $('.search_txt').val('');
    });

    // 搜索关键字改变时，重新请求suggest
    $('.search_txt').off('input propertychange').on('input propertychange', function () {
        var text_value = $('.search_txt').val();
        if (text_value == '') {
            $('.suggest').hide();
            $('.div').hide();
        } else {
            searchajax(text_value);
        }
    });

    // 输入搜索关键字，点击return事件
    $('.search_txt').off('keydown').on('keydown', function (event) {
        var keywords = $('.search_txt').val();
        if (event.which === 13) {
            window.location.href = '/search/course/' + keywords + '-1/';
        }
    });
    // 搜索文本框获得焦点,显示取消按钮
    $('.search_txt').off('focus').on('focus', function () {
        var keywords = $('.search_txt').val();
        $('.cancel').show();
        searchajax(keywords);
    });

    // 点击搜索取消按钮，隐藏suggest
    $('.cancel').off('touchend').on('touchend', function () {
        $('.suggest').hide();
        $('.div').hide();
        setTimeout("$('.cancel').hide()", 500);
    });
    // 
    $('.div').off('touchend').on('touchend',function(){
        $('.suggest').hide();
        setTimeout("$('.div').hide()",100);
    });
    // 
    $('.course_course').off('tap').on({'tap':function(){
        $(this).css({'background': '#ffa800'});
        $(this).children().css({'color': '#fff'});
    }},'li a');

});

