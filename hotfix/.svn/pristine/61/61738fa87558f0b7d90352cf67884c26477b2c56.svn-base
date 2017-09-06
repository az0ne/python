$(function(){
    //首页搜索模块
    $(".search-icon").click(function(){
        $('.searchwrap').animate({'opacity':1,'z-index':10,'transform':'translate(0,2.2rem) scale(1,1)'},500);
        setTimeout($(".search-icon").animate({'opacity':0},10),500);
    });
    $(".cancel").click(function(){
       $('.searchwrap').animate({'opacity':0,'z-index':-1,'transform':'translate(35%,-12%) scale(0.01,0.2)'},500); 
       setTimeout($(".search-icon").animate({'opacity':1},10),600);
    });
    // 清空搜索框文本值
    $('.empty').off('touchend').on('touchend',function(){
        $('.search_txt').val('');
        $('.searchwrap .suggest').hide();
    });

    // 搜索关键字改变时，重新请求suggest
    $('.search_txt').off('input propertychange').on('input propertychange',function(){
        var text_value=$('.search_txt').val();

        if(text_value==''){
            $('.suggest').css({opacity:"0"});
            $('.suggest').hide();
        }else{
            searchajax(text_value);
        }
    });

    // 输入搜索关键字，点击return事件
    $('.search_txt').off('keydown').on('keydown',function(event){
        var keywords = $('.search_txt').val();
        keywords = keywords? keywords: 'Android';
        if(event.which === 13){
            window.location.href='/search/course/'+keywords+'-1/';
        };
    });
    // 单击搜索建议中的小课程
    $('.course_course').off('tap').on({'tap':function(){
        $(this).css({'background': '#ffa800'});
        $(this).children().css({'color': '#fff'});
    }},'li a');

    // // 点击搜索取消按钮，隐藏suggest
    // $('.cancel').off('touchend').on('touchend',function(){
    //     $("#searchwrap").animate({top:"-100%"},600);
    //     $("body").css("position","relative").animate({top:0},300);
    //     $(".searchwrap .suggest").css({opacity: "0"}).hide();
    // });
    //搜索按钮
    $(".btn-search").click(function(){
        $("#page-id").html(0);
        //sreachBtn();
        searchBtn2();
    });
    //
    $('.hot_skill li').off('tap').on('tap',function(){
        $(this).addClass('selected');
    });
    $(".search-text input").keydown(function(event){
        if(event.keyCode == 13) {
            $("#page-id").html(0);
            //sreachBtn();
            searchBtn2();
        }
    });

});

// 搜索框响应函数
function searchBtn2() {
    window.location = '/course/list/?search=' + $(".search-text input").val();
};

function searchajax(keyword) {
    ret_val = false;
    return $.ajax({
        url: "http://suggest.maiziedu.com/suggest/?keyword=" + keyword,
        type: "GET",
        dataType: "jsonp",
        jsonp: "callback",
        success: function (data) {
            var courses = new Array(), careers = new Array(), teachers = new Array(), teachers_repeat = new Array(), careers_repeat = new Array();

            $.each(data, function(idx, obj) {
                $.each(obj["courses"], function(idx, course) {
                    courses.push({
                        id: course["id"],
                        name: obj["name"],
                        student_count:course["student_count"]
                    });

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
                $('.suggest').hide();
                return;
            }

            // coding
            var tmp = "";
            $(".course_course ul li").remove();
            $.each(courses, function(idx, course) {
                tmp = '<li><a href="/course/'+course["id"]+'/"><span>'+course["name"]+'</span><em>'+course["student_count"]+'人正在学习</em></a></li>';
                $(".course_course ul").append(tmp);
            });

            $(".career_course ul li").remove();
            $.each(careers, function(idx, career) {
                tmp = '<li><a href="/course/'+career["short_name"]+'-px/"><p class="img"><img src="/uploads/'+career["image"]+'" alt="'+career["name"]+'" data-src=""></p> <div class="txt"> <h3>'+career["name"]+'</h3><em>毕业学员'+career["student_count"]+'人</em> <p>'+career["description"]+'</p> </div> </a> </li>';

                $(".career_course ul").append(tmp);
            });

            $(".search_teacher ul li").remove();
            $.each(teachers, function(idx, teacher) {
                tmp = '<li><a href="'+"/u/"+teacher["teacher_id"]+'/"> <p class="img"><img src="/uploads/'+teacher["image"]+'" alt="'+teacher["name"]+'" data-src=""></p> <div class="txt"> <h3>'+teacher["name"]+'</h3><em>'+teacher["title"]+'</em> <p>'+teacher["info"]+'</p> </div> </a> </li>';
                $(".search_teacher ul").append(tmp);
            });

            $('.suggest').show();
            $('.suggest').css({opacity: "1"});
            $('.div').show();
        }
    });
}
