define(function(require, exports, module) {
    var $ = require('jquery');
    require('bootstrap');

    //-------------------FUNCTION------------------------
    var quizs = [], quizsSum = 0;
    var abc = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    function opHomework(obj) {
        var pop_href = obj;
        if (pop_href == undefined) {
            return;
        }
        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "json",
            success: function (data) {
                console.log(data)
                $("#tryTeacherLearnData .test .modal-title").html(data.papertitle);
                quizs = data.quizs;
                bindst();
                $("#tryTeacherLearnData .data").hide();
                $("#tryTeacherLearnData .test").fadeIn();
                $("#tryTeacherLearnData .modal-dialog").addClass("modal-test").removeClass("modal-data");
            },
            error: function (data) {
                alert("service data error");
            }
        });
    }
    //处理答题
    function bindanswer(n) {
        var data = quizs[n - 1];
        $("#tryTeacherLearnData .test h5").html(n + ".&nbsp;" + data.question);
        var html = '';
        var an = data.answer;
        var i = 0;
        for (var aa in an) {
            var classt = '';
            if (data.user_choose == abc[i] && data.user_choose != data.correct) {
                classt = "error"
            }
            if (data.correct == abc[i]) {
                classt = "active"
            }
            html += '<li class="' + classt + '"><span>' + abc[i] + '</span>' + an[abc[i]] + '</li>';
            i++;
        }
        $("#tryTeacherLearnData .test ol").html(html);
    }
    function bindst() {
        quizsSum = quizs.length;
        var html = '';
        for (var i = 0; i < quizsSum; i++) {
            var data = quizs[i];
            var classt = "right";
            if (data.user_choose != data.correct) classt = "error";
            html += '<li class="' + classt + '" num="' + (i + 1) + '"></li>';
        }
        $("#tryTeacherLearnData .infos ul").html(html);
        $("#tryTeacherLearnData .infos li").unbind().click(function () {
            bindanswer($(this).attr("num"));
            $(this).addClass("active").siblings().removeClass("active");
        }).eq(0).trigger("click");
    }
    var getLength = function(str){
       return String(str).replace(/[^\x00-\xff]/g,'aa').length;
    };
    //-------------处理答题END-------------
    function opItemProject(obj) {
        var pop_href = obj;
        if (pop_href == undefined) {
            return;
        }

        $.ajax({
            type: 'GET',
            url: pop_href,
            dataType: "html",
            success: function (data) {

                $('#tryTeacherLearnData').modal('hide');
                $('#tryTeacherCorrWork').html(data);
                $('#tryTeacherCorrWork').modal('show');
            },
            error: function (data) {
                alert("service data error");
            }
        });
    };
    function requestTask(url){
        $.ajax({
            type: 'GET',
            url: url,
            dataType: "html",
            success: function (data){
                $("#tryTeacherLearnData").html(data);
                $('#tryTeacherLearnData').modal({show:true, keyboard:false,backdrop: 'static'});
            }
        });
    }

    var imgPopup = function(img_src){
        var html = '';

        html += '<div id="imgzoom"><i class="imgzoom-close"></i><div id="imgzoom-image-ctn">';
        html += '<img class="img" src="'+ img_src +'" alt="">';
        html += '</div></div>';

        $('body').append(html);

        var oImg = $('#imgzoom-image-ctn');

        oImg.find('.img').load(function(){
            oImg.css({'left': '50%','top': '50%','marginLeft': -oImg.outerWidth()/2,'marginTop':-oImg.outerHeight()/2});
        });

        $('#imgzoom').fadeIn('fast','linear').css({'z-index':'1100','top':'0px'});

        $('.imgzoom-close').on('click',function(event){$('#imgzoom').remove();});
    };
//-------------------FUNCTION_END------------------------
    $(function () {
        //-------------show事件-------
        $('#tryTeacherCorrWork').on('show.bs.modal', function () {
            //评分
            $("#tryTeacherCorrWork .score span").unbind().hover(function () {
                layer.tips($(this).attr("v"), $(this), {tips: [1, '#626262'], time: 2000});
            }, function () {

            }).click(function () {
                $(this).addClass("active").siblings().removeClass("active");
            });

        });
        //学习数据
        $(".tryTeacherManage .tableBox .LearnData").on("click", function() {
            var pop_href = $(this).attr("pop_href");
            if (pop_href == undefined) {
                return;
            }
            requestTask(pop_href);
        });

        //批改作业/查看作业
        $(".tryTeacherManage .tableBox .CorrWork").on('click', function () {
            var pop_href = $(this).attr("pop_href");
            if (pop_href == undefined) {
                return;
            }
            $.ajax({
                type: 'GET',
                url: pop_href,
                dataType: "html",
                success: function (data) {
                    $('#tryTeacherLearnData').modal('hide');
                    $('#tryTeacherCorrWork').html(data);
                    $('#tryTeacherCorrWork').modal('show');
                },
                error: function (data) {
                    alert("service data error");
                }
            });
        });

        $('#tryTeacherLearnData').on('show.bs.modal', function () {
            //获取当前列表内容
            $("#tryTeacherLearnData .data li").each(function(){
                $(this).click(function(){
                    $(this).addClass("active").siblings().removeClass("active");
                    if($(this).attr("data-type") == "LESSON"){
                        opItemProject($(this).children("a").attr('pop_href'));
                    }else{
                        opHomework($(this).children("a").attr('pop_href'));
                    }
                });
            });
            //答题翻页
            $("#tryTeacherLearnData .infos .lastQuest").unbind().click(function () {
                $("#tryTeacherLearnData .infos li.active").prev().trigger("click");
            });
            $("#tryTeacherLearnData .infos .nextQuest").unbind().click(function () {
                $("#tryTeacherLearnData .infos li.active").next().trigger("click");
            });
            //返回
            $("#tryTeacherLearnData .test .backBtn").on("click",function () {
                $("#tryTeacherLearnData .test").hide();
                $("#tryTeacherLearnData .modal-dialog").addClass("modal-data").removeClass("modal-test");
                $("#tryTeacherLearnData .data").fadeIn();
            });
        });
    });
    $('#tryTeacherLearnData').on('shown.bs.modal', function () {
        $('.tryTeacherLearnData .data').jScrollPane({
            mouseWheelSpeed:100
        });
    });
    require('mousewheel');
    require('jscrollpane');
    $('#tryTeacherCorrWork').on('shown.bs.modal', function () {
        $('#tryTeacherCorrWork .submitBtn').click(function () {
            var desc = $('#tryTeacherCorrWork textarea').val();
            var num = Math.ceil(getLength(desc) / 2);
            if ($('#tryTeacherCorrWork .score span.active').length == 0 || desc == '') {
                layer.msg('请评分，写评语！');
            } else if (num > 200) {
                layer.msg('已超出200字！');
            } else {
                $.ajax({
                    type: 'POST',
                    url: $("#project_marking").val(),
                    data: {'score': $('.active').text(), 'desc': desc},
                    dataType: 'json',
                    success: function (data) {
                        if (data.status == 'success' || data.message == "'LocMemCache' object has no attribute 'client'") {
                            $('#tryTeacherCorrWork').modal('hide');
                            layer.msg('评分成功！');
                        } else {
                            layer.msg(data.message);
                        }
                    }
                });
            }
        });

        //-----------------批改----------------
        var score = $('#tryTeacherCorrWork .score span');
        var oImgList = $('#tryTeacherCorrWork li a');
        score.each(function(){
            $(this).on('click',function(){
                $(this).addClass("active").siblings("span").removeClass("active");
            });
        });
        oImgList.on('click',function(event){
            event.stopPropagation();
            event.preventDefault();
            imgPopup($(this).find('img').attr('src'));
        });
        $('.tryTeacherCorrWork').jScrollPane({
            mouseWheelSpeed:100
        });
    });
});