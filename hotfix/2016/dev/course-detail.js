$(function(){
     url = $("article h3").find("a").first().attr("href");
     if(typeof(url) == "undefined"){
        $('.btn-xlg').attr("disabled",true).css({"background":"#b5b5b5","border-color":"#b5b5b5"});
        $('.course-btn li:eq(1)').hide();
     }
    $(".zy_rightBox li").click(function(){
        var g=$(this).attr("go");
        $('html,body').animate({scrollTop: $("#"+g).offset().top-70+'px'}, 800);
    });
    $(window).scroll(function(){
        var th=$(this);
        var pyHeight=th.height();
        var newtop=$(this).scrollTop();
        $(".zygogo").each(function(){
            var s2Top=$(this).offset().top;
            if(newtop>(s2Top-pyHeight)&&newtop<s2Top+$(this).parent().height()-100) {
                //console.log($(this).attr("id"))
                $(".zy_rightBox li[go='"+$(this).attr("id")+"']").addClass("liH");
                $(".zy_rightBox li[go='"+$(this).attr("id")+"']").siblings().removeClass("liH");
                return false;
            }
        })
    });
    $(".zy_tab li").click(function(){
        $('html,body').stop().animate({scrollTop: '0px'}, 800);
        $(".zy_tabBB").hide();
        $(".zy_tab"+$(this).attr("num")).show();
        $(this).addClass("liH").siblings().removeClass("liH");
        if($(this).attr("num")==1){
            $(".zy_rightBoxDD").hide();
        }
        else{
            $(".zy_rightBoxDD").show();
        }
    });
    //友链切换
    $(".friendLinks span").mouseover(function(){
        $(this).addClass("active").siblings().removeClass("active");
        $(".friendLinks .nav").eq($(this).index()).fadeIn().siblings().hide();
    });

    $('.course-stage-item .lists').stop().hover(function(){
        $(this).find('.description').show();
    },function(){
        $(this).find('.description').hide();
    });
});