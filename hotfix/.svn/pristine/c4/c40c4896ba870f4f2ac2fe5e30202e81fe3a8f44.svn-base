$(function(){

    var mySwiper = new Swiper('.swiper-container',{
      pagination: '.swiper-pagination',
      autoplay: 3000,
      loop:true,
      grabCursor: true,
      calculateHeight: true,
      resizeReInit:true
    });
    
    $(window).resize(function(){
      mySwiper.resizeFix();
    });
    //首页-大图切换
    var carousel = $("#carousel").featureCarousel({
        topPadding: 0,
        sidePadding: 0,
        smallFeatureOffset: 100,
        trackerSummation: false
    });

    //首页-名师切换
    $('#foo').carouFredSel({
        auto: false,
        prev: '#prev',
        next: '#next',
        mousewheel: false,
        items:{
            visible:4,
            minimum:1
        },
        scroll:{
            items:1,
            duration:1000
        }
    });

    $(".tc-list #prev").click(function(){
        $('html,body').animate({scrollTop: ($(window).scrollTop()+1)+'px'}, 800);
    });
    $(".tc-list #next").click(function(){
        $('html,body').animate({scrollTop: ($(window).scrollTop()-1)+'px'}, 800);
    });

    $('.v5-course-item').each(function(index, el) {
        var _ul = $(this).find('.course-list').length;
        var _id = $(this).attr('id');
        var _holder = $(this).attr('data-holder');
        $("#"+_holder).jPaginator({
            nbPages:_ul,
            marginPx:12,
            length:5,
            widthPx:20,
            overBtnLeft:'#'+_id+'_backward',
            overBtnRight:'#'+_id+'_forward',
            onPageClicked: function(a,num) {
                $('#'+_id).find('.course-list').eq(num-1).show().find('li').addClass('animated bounceIn');
                $('#'+_id).find('.course-list').eq(num-1).siblings().hide().find('li').removeClass('animated bounceIn');
            }
        });
    });


})

