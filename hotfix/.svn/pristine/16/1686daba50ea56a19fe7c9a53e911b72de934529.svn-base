
    var get_cookie = function(c_name) {
        if (document.cookie.length > 0) {
            var c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }

    var set_cookie = function (c_name,value,exdays) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + exdays);
        var c_value = escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
        document.cookie = c_name + "=" + c_value + "; path=/";
    }


    /*
     * set maiziuid
    */

    var uid_gen = function() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
        }
        return s4() + s4() + s4() + s4() + s4() + s4() + s4() + s4();
    }

    if (get_cookie("maiziuid") == "") {
        set_cookie("maiziuid", uid_gen(), 1024);
    }

    if (window.location.hostname.indexOf("maiziedu.com") >= 0) {
        (function () {
            var query_string = "url=" + escape(window.location.href) + "&";
            query_string = query_string + "maiziuid=" + get_cookie("maiziuid") + "&";
            query_string = query_string + "referrer=" + escape(document.referrer);

            var url = "http://hit.maiziedu.com/?" + query_string + "&callback=" + new Date().getTime();
            var script = document.createElement("script");
            script.setAttribute("src", url);
            document.getElementsByTagName("head")[0].appendChild(script);
        })();
    };


      //页面手机跳转
      //   if(/AppleWebKit.*Mobile/i.test(navigator.userAgent) || (/MIDP|android|SymbianOS|NOKIA|SAMSUNG|LG|NEC|TCL|Alcatel|BIRD|DBTEL|Dopod|PHILIPS|HAIER|LENOVO|MOT-|Nokia|SonyEricsson|SIE-|Amoi|ZTE/.test(navigator.userAgent))){if(window.location.href.indexOf("{{mobile_site}}")<0){
      //       // window.location.href="{{mobile_site}}" + window.location.pathname;
      //   }};




function HeaderFooterFn() {
    $(".hd-seach-btn").on("touchstart", function (ev) {
        ev.stopPropagation();
        $(this).parents(".mz-new-header").addClass("active");
    });
    $(".mz-new-header .cancel").on("touchstart", function (ev) {
        ev.stopPropagation();
        $(this).parents(".mz-new-header").removeClass("active");
    });
    $(".searchwrap").on("touchstart", function (ev) {
        ev.stopPropagation();

    });
    $(document).on("touchstart", function () {
        $(".mz-new-header").removeClass("active");
    });
    //清空val
    $(".search_div .empty").on("touchstart", function () {
        $(this).siblings("input").val("")
    });
    //搜索跳转
    $('.search_div input').off('keydown').on('keydown', function (event) {
        var keywords = $(this).val();
        keywords = keywords ? keywords : 'Android';
        if (event.which === 13) {
            window.location.href = '/search/course/' + keywords + '-1/';
        }
        ;
    });
    //底部导航是否显示
    var p = 0,
        t = 0;
    $(window).scroll(function (e) {
        p = $(this).scrollTop();
        if (t <= p) {
            $("body").removeClass("footer-show");
        } else {
            if(!$("body").hasClass("footer-show")&&!$("body").hasClass("MEIQIA-FULL-BODY")){
            $("body").addClass("footer-show");
            }
        }
        t = p;
    });
};
$(function () {
     //视频播放
    $(".video_introduce1").on("touchstart", function () {
        var viderSrc = $(this).find("a").attr("data-href");
        console.log(viderSrc)
        var $video = $('<div class="videocontainer"><div class="video-close mzub mzub-ac mzub-pc"><i class="mzicon mzicon-close"></i></div><div class="video-mask"></div><div class="videobox"><video src="' + viderSrc + '" webkit-playsinline="true"></video></div></div>');
        $("body").append($video);
        $video.find("video").get(0).play();
        $video.find(".video-close").off().on("touchstart", function () {
            $video.addClass("active");
            setTimeout(function () {
                $video.remove();
                return false;
            }, 900)
        })
    });

    $(".mzconsultation,.mz-consultation").on("touchstart", function () {
        mzConsultation()
    })
    //切换
    $(".mz-cuose-tab li").on("touchend", function () {
        $(this).addClass("active").siblings().removeClass("active");
        $(".mz-cuose-tabwrap .mz-cuose-tabcon").eq($(this).index()).addClass("active").siblings(".mz-cuose-tabcon").removeClass("active");
    });
    $(".see-curriculum").on("touchend", function () {
        $("body,html").scrollTop($(".banner").height())
        $(".mz-cuose-tab").find("li").eq(1).addClass("active").siblings("li").removeClass("active");
        $(".mz-cuose-tabwrap .mz-cuose-tabcon").eq(1).addClass("active").siblings(".mz-cuose-tabcon").removeClass("active");
        return false;
    });
    //显示本章节所有内容
    $(".ly-course-list-add").on("touchend", function () {
        $(this).hide().siblings().show();
    });
});

function tab3AdddMore() {
    var html = '<li>' +
        '											<div class="review-bcontainer-t-pic">' +
        '												<img src="images/st_headphoto.png" alt="st_headphoto">' +
        '											</div>' +
        '											<div class="clear review-bcontainer-t">' +
        '												<div class="fl review-bcontainer-t-l">' +
        '													<b>周安伟</b>' +
        '													<div class="mzedu-student-review-score dib">' +
        '														<i class="mzicon mzicon-star"></i>' +
        '														<i class="mzicon mzicon-star"></i>' +
        '														<i class="mzicon mzicon-star"></i>' +
        '														<i class="mzicon mzicon-star"></i>' +
        '														<i class="mzicon mzicon-star"></i>' +
        '													</div>' +
        '												</div>' +
        '												<span class="fr">' +
        '													45分钟前' +
        '												</span>' +
        '											</div>' +
        '											<div class="review-bcontainer-contxt">' +
        '												<div class="review-bcontainer-txt-sdu">' +
        '													作为一个刚入门的前端工程师，用这个视频教程作为学习 Vue 真是太好了，主要之前没怎么接触过模块化设计，网上对将这些方面的又不是很多。这个教程很 nice。1 天半看了 1/3 了，毫无难度，通俗易懂。唯一的一点不足就是这不是 Vue 2.0 的，有些不一样的地方我还得翻官方文档去改。但总的来说很好。点赞！' +
        '												</div>' +
        '												<div class="review-bcontainer-txt-tec">' +
        '													<b>老师回复：</b>感谢支持~ 能学会使用 Vue 开发实战项目就是本门课的宗旨~由于课程录制时间比较早选择的是 1.0 的。' +
        '												</div>' +
        '											</div>' +
        '										</li>'

    $(".review-bcontainer-contxt-add").on("touchend", function () {
        $(".review-bcontainer-contxt-add").parent().before(html);
    })

}

    //ZHUGE

    window.zhuge = window.zhuge || [];
    window.zhuge.methods = "_init debug identify track trackLink trackForm page".split(" ");
    window.zhuge.factory = function (b) {
        return function () {
            var a = Array.prototype.slice.call(arguments);
            a.unshift(b);
            window.zhuge.push(a);
            return window.zhuge;
        }
    };
    for (var i = 0; i < window.zhuge.methods.length; i++) {
        var key = window.zhuge.methods[i];
        window.zhuge[key] = window.zhuge.factory(key);
    }
    window.zhuge.load = function (b, x) {
        if (!document.getElementById("zhuge-js")) {
            var a = document.createElement("script");
            var verDate = new Date();
            var verStr = verDate.getFullYear().toString() + verDate.getMonth().toString() + verDate.getDate().toString();
            a.type = "text/javascript";
            a.id = "zhuge-js";
            a.async = !0;
            a.src = (location.protocol == 'http:' ? "http://sdk.zhugeio.com/zhuge-lastest.min.js?v=" : 'https://zgsdk.zhugeio.com/zhuge-lastest.min.js?v=') + verStr;
            var c = document.getElementsByTagName("script")[0];
            c.parentNode.insertBefore(a, c);
            window.zhuge._init(b, x)
        }
    };
    window.zhuge.load('7bdc65f630344e4fa3b5d23e5c096d35');


