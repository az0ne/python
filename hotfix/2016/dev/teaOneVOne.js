$(function(){
    $(".teacherICO").on("mouseover",function(){
        layer.tips($(this).attr("title"), $(this), {
          tips: [1, '#333'] //还可配置颜色
        });
    });

    //tab切换
    $('.tabTitle>span').on('click',function(){
        $(this).addClass('cur').siblings().removeClass('cur');
        $('.tabCon>div').eq($(this).index()).addClass('cur').siblings().removeClass('cur');
    });

    //-------------------FUNCTION------------------------
    var quizs = [], quizsSum = 0;
    var abc = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    $("#yourHomework").on({"click":function(){
        opItemProject(this);
    }},".zy_yourHomework .liH .yourHomeworkProject");
    $("#yourHomework").on({"click":function(){
        opHomework(this);
    }},".zy_yourHomework .liH .yourHomeworkTest");

    function opHomework(obj) {
        var pop_href = $(obj).attr("pop_href");
        if (pop_href == undefined) {
            return;
        }
        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "json",
            success: function (data) {
                console.log(data)
                $(".zy_yourHomework3 .pt>span").html(data.papertitle);
                quizs = data.quizs;
                bindst();
                $('#yourHomework').modal('hide');
                $('#yourHomework3').modal('show');
            },
            error: function (data) {
                alert("service data error");
            }
        });
    }
    //处理答题
    function bindanswer(n) {
        var data = quizs[n - 1];
        $(".zy_yourHomework3 .ptt").html(n + ".&nbsp;" + data.question);
        var html = '';
        var an = data.answer;
        var i = 0;
        for (var aa in an) {
            var classt = '';
            if (data.user_choose == abc[i] && data.user_choose != data.correct) {
                classt = "error"
            }
            if (data.correct == abc[i]) {
                classt = "right"
            }
            html += '<li class="' + classt + '"><span>' + abc[i] + '</span>' + an[abc[i]] + '</li>';
            i++;
        }
        $(".zy_yourHomework3_div ul").html(html);
    }
    function bindst() {
        quizsSum = quizs.length;
        var html = '';
        for (var i = 0; i < quizsSum; i++) {
            var data = quizs[i];
            var classt = "aH";
            if (data.user_choose != data.correct) classt = "error";
            html += '<a class="an ' + classt + '" num="' + (i + 1) + '"></a>';
        }
        $(".zy_yourHomework3 .examinationBottom>.znum").html(html);
        $(".zy_yourHomework3 .examinationBottom a").unbind().click(function () {
            bindanswer($(this).attr("num"));
            $(this).addClass("active").siblings().removeClass("active");
        }).eq(0).trigger("click");
    }
    //-------------处理答题END-------------
    function opItemProject(obj) {
        var pop_href = $(obj).attr("pop_href");
        if (pop_href == undefined) {
            return;
        }
        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "html",
            success: function (data) {
                $('#yourHomework').modal('hide');
                $('#yourHomework2').html(data);
                $('#yourHomework2').modal('show');
            },
            error: function (data) {
                alert("service data error");
            }
        });
    }

    function startClass() {
        window.location.href = "{% url 'lps3:teacher_class_start' class_id %}";
    }

    var getLength = function(str){
       return String(str).replace(/[^\x00-\xff]/g,'aa').length;
    };

    var imgPopup = function(img_src){
        var html = '';

        html += '<div id="imgzoom"><i class="imgzoom-close"></i><div id="imgzoom-image-ctn">';
        html += '<img class="img" src="'+ img_src +'" alt="">';
        html += '</div></div>';

        $('body').append(html);
        console.log(html)

        var oImg = $('#imgzoom-image-ctn');

        oImg.find('.img').load(function(){
            oImg.css({'left': '50%','top': '50%','marginLeft': -oImg.outerWidth()/2,'marginTop':-oImg.outerHeight()/2});
        });

        $('#imgzoom').fadeIn('fast','linear').css({'z-index':'1100','top':'0px'});

        $('.imgzoom-close').on('click',function(event){$('#imgzoom').remove();});
    };
    var golbal_href='',golbal_tSturight;
    //请求任务列表
    function requestTask(url) {
        $.ajax({
            type: 'GET',
            url: url,
            dataType: "html",
            success: function (data) {
                $("#yourHomework").html(data);
                $('#yourHomework').modal({show:true, keyboard:false,backdrop: 'static'});

            }
        });
    }
//-------------------FUNCTION_END------------------------
    //-------------show事件-------
    $('#yourHomework2').on('show.bs.modal', function () {
        //评分
        $(".yourHomeworkD a").unbind().hover(function () {
            layer.tips($(this).attr("v"), $(this), {tips: [1, '#68c8b6'], time: 2000});
        }, function () {

        }).click(function () {
            $(this).addClass("aH").siblings().removeClass("aH");
        });
    });

    $(".personal_select").iSimulateSelect({
        width: 132,
        height: 0,
        selectBoxCls: "personal_info_selectD",
        optionCls: "personal_info_selectD_Op"
    });
    $(".personal_select").change(function () {
        _order = $(this).val();
        _url = window.location.pathname + "?s_order=" + _order;
        window.location.href = _url;
    });

    $(".teacherStulist li").unbind().hover(function () {
        $(this).children(".s_details").addClass("HH");
    }, function () {
        $(this).children(".s_details").removeClass("HH");
    });

    //顶部开关
    $(".zy_onoffBtn").unbind().click(function () {
        $(this).toggleClass("on");
        setTimeout("startClass()", 600);
        //点击刷新
    });
    //展开任务
    $("#yourHomework").on({'click':function () {
        $(this).parent().parent().toggleClass("liH");
        $(this).parents("li").find("dd").removeAttr("onclick");
        SPwork.jScrollPane({
            mouseWheelSpeed:10
        });
    }},".zy_yourHomework_divUL li>.a .s1");

    //总体关闭
    $(".modal").on({"click": function(){
        $('#yourHomework').modal('hide');
        $('#yourHomework2').modal('hide');
    }},'.zy_newclose');
    $(".zy_newclose").on("click",function(){
        $('#yourHomework3').modal('hide');
    });
    //阶段点击
    $(".teacherTasklist li span").on("click", function () {
        var pop_href = $(this).attr("pop_href");
        if (pop_href == undefined) {
            return;
        }
        golbal_href=pop_href;
        golbal_tSturight=$(this);
        requestTask(pop_href);
    });
    var SPwork;
    $('#yourHomework').on('shown.bs.modal', function () {
        SPwork=$('.zy_yourHomework').jScrollPane({
            mouseWheelSpeed:80
        });
    });
    //查看
    $("#yourHomework").on({'click':function () {
        var pop_href = $(this).attr("pop_href");
        if (pop_href == undefined) {
            return;
        }
        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "html",
            success: function (data) {
                $('#yourHomework').modal('hide');
                $('#yourHomework2').html(data);
                $('#yourHomework2').modal('show');
            },
            error: function (data) {
                alert("service data error");
            }
        });
    }},".zy_yourHomework_divUL li > .a > .s2");
    //批改按钮
    $("#yourHomework").on({'click':function () {
        var pop_href = $(this).attr("pop_href");
        if (pop_href == undefined) {
            return;
        }
        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "html",
            success: function (data) {
                $('#yourHomework').modal('hide');
                $('#yourHomework2').html(data);
                $('#yourHomework2').modal('show');

            },
            error: function (data) {
                alert("service data error");
            }
        });
    }},".zy_yourHomework_divUL li > .a > .yhbtn")
    //返回
    $("#yourHomework2").on({"click":function () {
        $('#yourHomework2').modal('hide');
        $('#yourHomework').modal('show');
    }},".modal-dialog .pt a");
    $(".zy_yourHomework3 .pt a").on("click",function(){
        $('#yourHomework3').modal('hide');
        $('#yourHomework').modal('show');
    });

    //答题翻页
    $(".zy_yourHomework3 .examinationBottom .ebtn.prev").unbind().click(function () {
        $(".zy_yourHomework3 .examinationBottom a.active").prev().trigger("click");
    })
    $(".zy_yourHomework3 .examinationBottom .ebtn.next").unbind().click(function () {
        $(".zy_yourHomework3 .examinationBottom a.active").next().trigger("click");
    });

    //点击图片放大
    $("#yourHomework2").on({'click':function(event){
        event.stopPropagation();
        event.preventDefault();
        imgPopup($(this).find('img').attr('src'));
    }},".zy_yourHomework2_divImg > a");
    //事件
    $('#yourHomework2').on('shown.bs.modal', function () {
        $('.zy_yourHomework2').jScrollPane({
            mouseWheelSpeed:100
        });
    })
    //-----------------批改----------------
    var score = $('.yourHomeworkD a');
    score.each(function(){
        $(this).on('click',function(){
            $(this).addClass('aH').siblings().removeClass('aH');
        });
    });
    $("#yourHomework2").on({'click':function(){
        var desc = $('#desc-remark').val();
        var num = Math.ceil(getLength(desc)/2);
        if($('.yourHomeworkD a.aH').length == 0 || desc == ''){
            layer.msg('请评分，写评语！');
        }else if(num >200){
            layer.msg('已超出200字！');
        }else{
            $.ajax({
                type:'POST',
                url:$("#project_marking").val(),
                data:{'score':$('.Arial').filter('.aH').text(),'desc':desc},
                dataType: 'json',
                success: function(data){
                    if (data.status == 'success' || data.message == "'LocMemCache' object has no attribute 'client'") {
                        $('#yourHomework2').modal('hide');
                        layer.msg('评分成功！');
                        //golbal_tSturight
                        if(data.number==0){
                            golbal_tSturight.children("i").remove();
                        }
                        else{
                            golbal_tSturight.children("i").html(data.number);
                        }
                        requestTask(golbal_href);
                    }else{
                        layer.msg(data.message);
                    }


                }
            });
        }
    }},'#remark-submit');
    //--------------批改END-------------

})