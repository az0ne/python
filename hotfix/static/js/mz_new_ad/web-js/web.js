/**
 * Created by Administrator on 2017/3/29.
 */
$(function(){

    // $('.ser_btn').click(function () {
    //     $('.ser_btn').fadeOut();
    //     $('.header-search').animate({'right': 0}, 800);
    //     return false;
    // });
    //
    // $('html').click(function(){
    //     $('.header-search').animate({'right': -500}, 800,function(){
    //         $('.ser_btn').fadeIn();
    //     });
    // });

    // function evaluationNum() {
    //     var num = $('.evaluation-box').length;
    //     $('.nav_tag b').html(num);
    // }

    $(".work-tag li").click(function(){
        var i=$(this).index();
        $(this).addClass('active').siblings().removeClass('active');
        $('.tab1-work').css({'background':'url(/static/images/mz_new_ad/web-images/work-bg'+(i+1)+'.png) no-repeat',
            'background-size':'100% 100%'
        })
    });

    $('.course-content li').click(function(){
       $(this).find('a').trigger('click');
    });

    //文字轮播
    var n=0;
    var $btn=$('.list-btn li');
    var $assbox=$('.assess-box');
    var $inner=$('.innerbox');
    var timer;

    function autoplay(){

        $inner.animate({"margin-left":(-800*n)+'px'},500);
        $btn.eq(n).addClass('active').siblings().removeClass('active');
        n++;
        if(n>2){
            n=0;
        }
        timer=setTimeout(autoplay,4000);
    }

    $assbox.hover(function(){
        clearTimeout(timer);
    },function(){
        timer=setTimeout(autoplay,4000);
    });

    $btn.click(function(){
        $(this).addClass('active').siblings().removeClass('active');
        n=$(this).index();
        $inner.animate({"margin-left":(-800*n)+'px'},500);
    })

    autoplay();

    // evaluationNum();

    //加载更多评论 ajax
    $('.show-eval').click(function(){
        $(this).hide();

        $('.tab3-evaluation ul').append("<li> <div class='eval-title'> <h4>周安伟 <img src='/static/images/mz_new_ad/web-images/evaluation-star.png' alt='学生全员好评'></h4> <span>45分钟前</span> </div> <div class='" +
            "eval-content'> 这是评论</div> <img src='/static/images/mz_new_ad/web-images/big-img.png' alt='学生全员好评'> </li>");

        //有老师回复的的代码
    //     $('.tab3-evaluation ul').append("<li> <div class='eval-title'> <h4>周安伟 <img src='/static/images/mz_new_ad/web-images/evaluation-star.png' alt='学生全员好评'></h4> <span>45分钟前</span> </div> <div class='" +
    //         "eval-content'>这是评论 <div class='eval-reply'>
    //     <p><span>老师回复：</span>感谢支持~能学会使用Vue开发实战项目就是本门课的宗旨~由于课程录制时间比较早选择的是1.0的。</p>
    //     </div></div> <img src='/static/images/mz_new_ad/web-images/big-img.png' alt='学生全员好评'> </li>");
    //
    });

});