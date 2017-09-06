/**
 * Created by feng on 2016/4/19.
 */

$(function(){
    // 首页搜索事件
    function track_search() {
        var search_text = $('#data-search').val();
        // console.log(search_text);
        zhuge.track("首页搜索事件", {
            // "事件ID": "home_search",
            "事件位置": "首页",
            // "事件描述": "获取用户搜索次数以及搜索的关键词",
            "搜索关键词": search_text
        });
    }
    $('.search-btn').click(function() {
        track_search();
    });
    $("#data-search").keyup(function() {
        if (event.keyCode == 13)
            track_search();
    });

    // 首页搜索框热点点击
    $('.hot-words>a').each(function () {
        $(this).click(function () {
            var text = this.text;
            // console.log(text);
            zhuge.track("首页搜索框热点点击", {
                // "事件ID": "home_search_hot",
                "事件位置": "首页",
                // "事件描述": "获取用户点击搜索框右方的推荐关键词次数以及关键词名称",
                "热点关键词": text
            });
        });
    });

    // 首页焦点图点击
    $('.top-banner .bx-wrapper a').each(function () {
        $(this).click(function () {
            var tag_a = this;
            var tag_img = this.firstChild;
            var url = tag_a.href;
            var img = tag_img.src;
            var alt = tag_img.alt;
            // console.log(url);
            zhuge.track("首页焦点图点击", {
                // "事件ID": "home_banner",
                "事件位置": "首页",
                // "事件描述": "获取用户点击焦点图的次数以及所点击的焦点图名称",
                "跳转url": url,
                "Banner": img,
                "Banner描述": alt
            });
        });
    });

    // 首页导航栏点击
    $('.nav-menu>ul>li>a').each(function () {
        $(this).click(function () {
            // console.log(this.href + '  ' + this.text);
            zhuge.track("首页导航栏点击", {
                // "事件ID": "home_navbar",
                "事件位置": "首页",
                // "事件描述": "获取用户点击导航栏次数以及所点击的导航栏名称",
                "跳转url": this.href,
                "url描述": this.text
            });
        });
    });

    // 首页左边侧栏点击
    function track_leftbar(url, career, course) {
        zhuge.track("首页左边侧栏点击", {
            // "事件ID": "home_leftbar",
            "事件位置": "首页",
            // "事件描述": "获取左边侧栏的点击数以及所点击的课程方向和课程关键字",
            "跳转url": url,
            "课程方向": career,
            "课程关键字": course
        });
    }
    $('.nav-group .menulihover>a').each(function () {
        $(this).click(function () {
            // console.log(this.href + '  ' + this.text);
            track_leftbar(this.href, this.text, '');
        });
    });
    $('.nav-group .MenuLCinList>p>a').each(function () {
        $(this).click(function () {
            var career = $(this).parent().siblings('h3').children().html();
            // console.log(this.href + '  ' + career + '  ' + this.text);
            track_leftbar(this.href, career, this.text);
        });
    });

    // 首页登录
    $('#login_btn').click(function () {
        var account = $('#id_account_l').val();
        // console.log('login: '+account);
        zhuge.track("首页登录", {
            // "事件ID": "home_login",
            "事件位置": "首页",
            // "事件描述": "获取用户在首页登录次数",
            "登录账号": account
        });
    });

    // 首页注册
    function track_regist(desc) {
        zhuge.track("首页注册", {
            // "事件ID": "home_regist",
            "事件位置": "首页",
            // "事件描述": "获取用户在首页注册次数",
            "注册入口": desc
        });
    }
    $('.register-button').click(function () {
        track_regist('首页注册按钮');
    });
    $('#btnRegister').click(function () {
        track_regist('登录弹框->立即注册');
    });

    // 首页最新资讯点击
    $('.latest-news-module>ul>li>a').each(function () {
        $(this).click(function () {
            // console.log(this.href + '  ' + this.text);
            zhuge.track("首页最新资讯点击", {
                // "事件ID": "home_news",
                "事件位置": "首页",
                // "事件描述": "获取用户点击最新资讯的次数",
                "跳转url": this.href,
                "标题": this.text
            });
        });
    });

    // 首页直通班点击
    $('div.points-recommended a').each(function () {
        $(this).click(function () {
            // console.log('首页直通班点击 ' + this.firstChild.alt + this.href);
            zhuge.track("首页直通班点击", {
                // "事件ID": "home_pushmajor",
                "事件位置": "首页",
                // "事件描述": "获取用户点击推荐的直通班的次数和所点击直通班的名称",
                "直通班名称": this.firstChild.alt,
                "直通班链接": this.href
            });
        });
    });

    // 首页诱导咨询点击
    $('ul.live-try-list a').each(function () {
        $(this).click(function () {
            // console.log('首页诱导咨询点击');
            zhuge.track("首页诱导咨询点击", {
                // "事件ID": "home_trick",
                "事件位置": "首页",
                // "事件描述": "获取用户点击咨询图片的的次数"
            });
        });
    });

    // 首页分类课程点击
    $('.contant-left-bottom ul').each(function (index, element) {
        $(element).find('a').each(function () {
            $(this).click(function () {
                var tab = $('.contant-center-top li').eq(index).text();
                var course_name = this.title;
                // console.log(tab + ' > ' + course_name);
                zhuge.track("首页分类课程点击", {
                    // "事件ID": "home_course",
                    "事件位置": "首页",
                    // "事件描述": "获取用户在首页点击课程卡片的次数以及该课程所属的tab和课程名",
                    "所属tab": tab,
                    "课程名": course_name
                });
            });
        });
    });

    // 首页课程大纲点击
    function track_career(career_name) {
        zhuge.track("首页课程大纲点击", {
            // "事件ID": "home_career",
            "事件位置": "首页",
            // "事件描述": "获取用户在首页点击课程大纲的次数和所点击的课程大纲名称",
            "课程大纲名称": career_name
        });
    }
    $('div.career-path-list a').each(function (index, element) {
        if (index%2 == 0) { // li下的第一个a标签
            $(element).click(function () {
                // console.log($(this).find('img').attr('alt'));
                track_career($(this).find('img').attr('alt'));
            });
        } else {    // li下的第二个a标签
            $(element).click(function () {
                // console.log($(this).prev().text());
                track_career($(this).prev().text());
            });
        }
    });

    // 首页金牌讲师点击
    $('.gmct .bx-viewport>ul>li>a.a2').each(function () {
        $(this).click(function () {
            // console.log($(this).children('p').text());
            zhuge.track("首页金牌讲师点击", {
                // "事件ID": "home_teacher",
                "事件位置": "首页",
                // "事件描述": "获取用户在首页点击老师的次数和所点击老师名字",
                "老师名字": $(this).children('p').text()
            });
        });
    });

    // 首页媒体报道点击
    $('.media-reports .bx-viewport a').each(function () {
        $(this).click(function () {
            // console.log($(this).children('img').attr('alt'));
            zhuge.track("首页媒体报道点击", {
                // "事件ID": "home_media",
                "事件位置": "首页",
                // "事件描述": "获取用户点击媒体报道的次数",
                "媒体": $(this).children('img').attr('alt'),
                "报道链接": this.href
            });
        });
    });

    // 首页合作企业点击
    $('.cooperative-enterprise .bx-viewport a').each(function () {
        $(this).click(function () {
            // console.log(this.href + ' ' + $(this).children('img').attr('alt'));
            zhuge.track("首页合作企业点击", {
                // "事件ID": "home_company",
                "事件位置": "首页",
                // "事件描述": "获取用户点击合作企业的次数",
                "企业": $(this).children('img').attr('alt'),
                "企业链接": this.href
            });
        });
    });

    // 首页合作院校点击
    $('.partner-schools .bx-viewport a').each(function () {
        $(this).click(function () {
            // console.log(this.href + ' ' + $(this).children('img').attr('alt'));
            zhuge.track("首页合作院校点击", {
                // "事件ID": "home_college",
                "事件位置": "首页",
                // "事件描述": "获取用户点击合作院校的次数",
                "院校": $(this).children('img').attr('alt'),
                "院校链接": this.href
            });
        });
    });

    // 继续学习点击
    $('.zyMainRight>.zyschedule>a').click(function () {
        // console.log('继续学习点击');
        zhuge.track("继续学习点击", {
            // "事件ID": "LPS_continueclick",
            "事件位置": "任务列表页",
            // "事件描述": "获取用户在任务列表页中点击继续学习的次数"
        });
    });

});
