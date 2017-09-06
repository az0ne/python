define(function(require, exports, module) {
    require('superSlide');
    require('textFiltered')($);
    //require('./feedbackBox.js');
    
    // 搜索
    function flayer_show() {
        $("#fLayerdl").show();
        $("#dd_listbox").hide();
    }

    function flayer_hide(delay) {
        if (delay) {
            setTimeout("$('#fLayerdl').hide();", delay);
        } else {
            $('#fLayerdl').hide();
        }
    }

    function listbox_show() {
        $("#dd_listbox").show();
        $("#fLayerdl").hide();
    }

    function listbox_hide(delay) {
        if (delay) {
            setTimeout("$('#dd_listbox').hide();", delay);
        } else {
            $("#dd_listbox").hide();
        }
    }

    function searchajax(keyword) {
        $.ajax({
            url: "http://suggest.maiziedu.com/suggest/?keyword=" + keyword,
            type: "GET",
            dataType: "jsonp",
            jsonp: "callback",
            success: function (data) {
                var courses = new Array();
                var careers = new Array();
                var teachers = new Array();

                var teachers_repeat = new Array();
                var careers_repeat = new Array();

                $.each(data, function(idx, obj) {
                    $.each(obj["courses"], function(idx, course) {
                        courses.push({
                            id: course["id"],
                            name: obj["name"],
                            student_count:course["student_count"]
                        })

                        $.each(course["careers"], function(idx, career) {
                            if (!career["student_count"]) {
                                return;
                            }
                            if (careers_repeat.indexOf(career["name"]) == -1) {
                                careers.push({
                                    name: career["name"],
                                    short_name: career["short_name"],
                                    image: career["image"],
                                    description: career["description"],
                                    student_count: career["student_count"]
                                });
                                careers_repeat.push(career["name"]);
                            }

                            $.each(career["teachers"], function(idx, teacher) {
                                if (teachers_repeat.indexOf(teacher["name"]) == -1) {
                                    teachers.push({
                                        "teacher_id": teacher["teacher_id"],
                                        name: teacher["name"],
                                        title: teacher["title"],
                                        image: teacher["image"],
                                        info: teacher["info"]
                                    })
                                    teachers_repeat.push(teacher["name"]);
                                }
                            })
                        })
                    })
                })

                if (courses.length == 0) {
                    $('.dd_listbox').hide();
                    return;
                }

                // coding
                var tmp = "";
                $(".careercraft").remove();
                $.each(courses, function(idx, course) {
                    tmp = '<div class="careercraft"><a target="_blank" href="/course/'+course["id"]+'/"><p class="pull-left course_info">'+course["name"]+'</p><p class="pull-right study_count">'+course["student_count"]+'人正在学习</p></a></div>';
                    $("#course_name_ledg").append(tmp);
                })

                $(".chcourse").remove();
                $.each(careers, function(idx, career) {
                    tmp = '<div class="chcourse"><img src="/uploads/'+career["image"]+'" class="dd_courseimg img-circle"><a target="_blank" href="/course/'+career["short_name"]+'-px/" style="outline:none;"><p class="dd_coursedescriname">'+career["name"]+'</p><p class="radius"><span class="f_radius">毕业学员： <span class="finished_count">'+career["student_count"]+'</span>人</span></p><p class="dd_coursedescri">'+career["description"]+'</p>';
                    $("#incld_careers").append(tmp);
                })

                $(".careerteacher").remove();
                $.each(teachers, function(idx, teacher) {
                    tmp = '<div class="careerteacher"><a target="_blank" href="'+"/u/"+teacher["teacher_id"]+'/" style="outline:none;"><img src="/uploads/'+teacher["image"]+'" class="dd_courseimg img-circle"><p class="courseteacher">'+teacher["name"]+'</p><p class="ls">|</p><p class="teachertt">'+teacher["title"]+'</p><p class="teacherdes">'+teacher["info"]+'</p></a></div>'
                    $("#incld_teachers").append(tmp);
                })
                if ($("#data-search").val()) {
                    if (careers.length == 0) {
                        $("#dd_csitem").hide();
                        $("#incld_careers").hide();
                    } else {
                        $("#dd_csitem").show();
                        $("#incld_careers").show();
                    }
                    if (teachers.length == 0) {
                        $("#dd_tutor").hide();
                        $("#incld_teachers").hide();
                    } else {
                        $("#dd_tutor").show();
                        $("#incld_teachers").show();
                    }
                    if (courses.length == 0) {
                        $("#dd_craft").hide();
                        $("#course_name_ledg").hide();
                    } else {
                        $("#dd_craft").show();
                        $("#course_name_ledg").show();
                    }

                    listbox_show();
                }
            }
        })
    }

    $(document).ready(function () {
        $("#data-search").focus(function () {
            keywd = $("#data-search").val();
            if (keywd == "") {
                flayer_show();
            } else {
                searchajax(keywd);
            }
        }).blur(function() {
            flayer_hide(500);
        })

        $("#data-search").keyup(function () {
            keywd = $("#data-search").val();
            if (keywd == "") {
                listbox_hide();
                flayer_show();
                return;
            }
            searchajax(keywd);
        }).blur(function() {
            keywd = $("#data-search").val();
            if (keywd == "") {
                listbox_hide();
                return;
            }
            listbox_hide(500);
        })
    });

    Search();
    $('#data-search').focus(function(){
        $('.hot-words').fadeOut(300);
    });
    $('.header-search, .search-btn').on('click', function(e){
        var e = e || event;
        e.stopPropagation();
    })
    $(document).on('click', function(e){
        $('.hot-words').fadeIn(300);
    });    

    function Search() {
        $(".search-btn").click(function () {
            sreachBtn($("#data-search").val());
            zhuge.track('搜索次数', {'搜索关键词': $("#data-search").val()});
        });

        function sreachBtn(str) {
            var str = str.replace('#', 'u0023').replace('?', 'u0022');
            if ($('.search_result_bg').length > 0) {
                var app = $('.search_app').val() ? $('.search_app').val() : 'course';
                window.location.href = "/search/" + app + "/" + str + "-1/";
            } else {
                window.open("/search/course/" + str + "-1/");
            }

        }

        $("#data-search").keyup(function (event) {
            var e = event || window.event || arguments.callee.caller.arguments[0];
            if (e && e.keyCode == 13) {
                sreachBtn($(this).val());
                return;
            }
        });
    }

    // 精品课程推荐
    goodLesson();
    
    navHover();
    function navHover(){
        var doc = ($(document.documentElement) || $(document.body)).width();        
        if(doc < 1349){
            $('.side-bar').hover(function(){
                $(this).stop().animate({
                    'width':'168px'
                },300);
                $('.w1920').stop().animate({
                    'left':'0'
                },300);        
            },function(){
                $(this).stop().animate({
                    'width':'33px'
                },300);
                $('.w1920').stop().animate({
                    'left':'-168px'
                },300);        
            });
        }else{
            $('.side-menu').removeAttr('style');
            $('.side-bar').unbind();
        }
    }
    
    $(window).on('resize',function(){
        navHover();                
    });

    // 视频介绍
    var $videoIntroduce = $('.video_introduce');

    $videoIntroduce.find('a').on('click', function(){
        var mask = $('<div class="modal-mask"></div>');
        var dialog = $('<div class="dialog"><video id="video_introduce" autoplay preload="none" width="100%" height="100%" src="'+ $(this).attr('data-href') +'"></video><a class="off" href="javascript: void(null);"></a></div>');
        
        $('body').append(mask);
        $('body').append(dialog);        
        AnimateFun(dialog);        
        
        $('.off').on('click', function(){   
            $(mask).remove();
            $(dialog).remove();            
        });        
        
        $(window).on('resize scroll',function(){
            AnimateFun(dialog);    
        });        
    });

    function AnimateFun(obj){
        obj.css('left' , ($(window).width() - obj.outerWidth())/2 );
        obj.stop().animate({'top' : ($(window).height() - obj.outerHeight())/2 + $(window).scrollTop()}, 300); 
    }

    $(".slide").slide({
        titCell:".slide-tab",
        mainCell:".slide-box ul",
        autoPage:true,
        effect:"fade",
        autoPlay:true,
        trigger:"click"
    });

    $(".gold-teacher").slide({
        titCell:".gold-tab",
        mainCell:".gold-slide ul",
        autoPage:true,
        effect:"leftLoop",
        scroll:4,
        vis:4,
        trigger:"click"
    });

    $(".cooperate").slide({
        titCell:".slide-tab",
        mainCell:".cooperate-slide ul",
        autoPage:true,
        effect:"leftLoop",
        trigger:"click"
    });

    /*
     * @ 金牌讲师
     * 
     */
    var $ul = $('#gold-list');
    var Time = 500;
    $ul.find('.inner-box').hover(function(){
        $(this).find('.hover-mask, .hover-card').stop().fadeIn(Time);
        $(this).next('h5').animate({
            'opacity': '0'
        },Time);
        $(this).find('.teach-icon').stop().animate({
            'bottom': '-32px',
            'opacity': '1'
        },Time);
    },function(){
        $(this).find('.hover-mask, .hover-card').stop().fadeOut(Time);
        $(this).next('h5').animate({
            'opacity': '1'
        },Time);
        $(this).find('.teach-icon').stop().animate({
            'bottom': '60px',
            'opacity': '0'
        },Time);
    });


    var headH = $('.head-container').outerHeight();

    window.onload = window.onscroll = window.onresize = function(){
        var scrtop = $(document.documentElement).scrollTop() || $(document.body).scrollTop();

        if(scrtop + 70 > headH){
            $('.hidden-box').stop().animate({
                'height':'0px'
            }, 300);
        }else{
            $('.hidden-box').stop().animate({
                'height':'70px'
            }, 300);
        }
    }

    function goodLesson(){
        var $div_li = $('.tab_menu li');
        $div_li.click(function(){
            $(this).addClass('selected').siblings().removeClass('selected');
            var index = $div_li.index(this);
            $('div.tab_box > div').eq(index).show().siblings().hide();
        });
    };

    jobPath();
    function jobPath(){
        var $jobPath = $('.job-path'), $jobTab = $('.job-tab span'), $jobList = $('.job-list');
        $jobTab.eq(0).on('click', function(){
            $jobList.stop().animate({
                'margin-left': '0px'
            }, 500);
            $(this).addClass('select').siblings().removeClass('select');
        });
        $jobTab.eq(1).on('click', function(){
            $jobList.stop().animate({
                'margin-left': '-508px'
            }, 500);
            $(this).addClass('select').siblings().removeClass('select');
        });
    };

    // 诸葛IO统计
    $('.hot-words a').click(function(){
        zhuge.track('热词推荐');
        setTimeout(function(){}, 500);
    });

    $('.tab_menu li').click(function(){
        zhuge.track('首页精品课程tab的点击次数', {'事件位置': '精品课程','名称': $(this).text()});
    });
    $('div.tab_box ul li > a').click(function(){
        zhuge.track('首页精品课程的点击数', {'事件位置': '精品课程','课程名称': $(this).find('.title').text()});
    });
    $('.job-list li').click(function(){
        zhuge.track('首页职业学习路线', {'事件位置': '职业学习路线','课程名称': $(this).find('h4').text()});
    });
});