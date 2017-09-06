//全局消息
function global_message(student_id, class_id){
    $.ajax({
        type:"POST",
        data: {
            'user_id': student_id,
            'class_id': class_id
        },
        url:"/lps3/student/ajax/global_message/",
        dataType:"JSON",
        success: function(data){
            if(data.status){
                ii=0;
                arrM = data.data;
                globalMessage();
            }
        }
    });
    var arrM = [],ii=0;
    var globalMessage = function(){
        if(arrM.length<=ii) return;
        $('.user-banner').append(arrM[ii]);
        ii++;
        var oClose = $('.header-user-msg-off');
        setTimeout(function(){
            oClose.parent().parent().addClass('fadein-move');
        },3000);

        oClose.live('click',function(){
            $(this).parent().parent().removeClass('fadein-move');
            setTimeout(globalMessage,1000);
        });
    };
}

// 任务成绩消息 task project message, which should be poped when user access the page
function task_score_message(student_id){
    $.ajax({
        url: "/lps3/student/ajax/task_score_message/",
        type: "GET",
        data: {'user_id':student_id},
        dataType: 'JSON',
        success : function(data){
            if(data.status){
                // 显示消息交互
                //console.log(data.data);
                ij=0;
                arrTaskScoreMessage = data.data;
                //$("#MyTaskScore").html(data.data[0]);
                //$("#MyTaskScore").modal('show');
                globalTaskScoreMessage();
            }
        }
    });
    var arrTaskScoreMessage = [], ij=0;
    var globalTaskScoreMessage = function(){
        if(arrTaskScoreMessage.length<=ij){
            $("#MyTaskScore").modal('hide');
            return;
        }
        $("#MyTaskScore").html(arrTaskScoreMessage[ij]);

        $("#MyTaskScore").modal('show');
        ij++;
        var oClose = $('.zy_newclose');
        oClose.live('click',function(){
            $(this).parent().remove();
            setTimeout(globalTaskScoreMessage,200);
        });
        var oClose2 = $('.scf_newclose');
        oClose2.live('click',function(){
            $(this).parent().remove();
            setTimeout(globalTaskScoreMessage,200);
        });
    };
}

// 班会计时消息
function class_meeting_message(student_id, class_id){
    $.ajax({
        url: "/lps3/student/ajax/class_meeting_schedule/",
        type: "GET",
        data: {'user_id':student_id, 'class_id': class_id},
        dataType: 'JSON',
        success : function(data){
            if(data.status){
                // 计时器交互代码
                //console.log(data.data);
                for(var i=0; i<data.data.length; i++){
                    class_meeting_schedule(data.data[i], i);
                }
            }
        }
    });
    // 计时器函数
    function class_meeting_schedule(data, _index){
        var index = _index;
        var left_time = data['left_time'];
        var html = data['html'];
        //郭涛 2016.4.12 修改过期班会还要提醒的BUG
        if (left_time >= 0) {
            setTimeout(function(){response_timer(index,html)}, left_time * 1000);
        }
    }
    // 计时器相应函数
    function response_timer(index,html){
        var local_index = index;
        $("#live-start-"+local_index).html(html);
        $("#live-start-"+local_index).modal('show');
        $("#zy_newclose_cm_"+local_index).live('click', function(){
            console.log('test2'+local_index);
            $("#live-start-"+local_index).modal('hide');
        });
    }
}

// 班会开始消息提醒
function class_meeting_open(student_id){
    $.ajax({
        url: "/lps3/student/ajax/class_meeting_open/",
        type: "GET",
        data: {'user_id':student_id},
        dataType: 'JSON',
        success : function(data){
            if(data.status){
                // 显示消息交互
                //console.log(data.data);
                ij=0;
                arrTaskScoreMessage = data.data;
                //$("#MyTaskScore").html(data.data[0]);
                //$("#MyTaskScore").modal('show');
                globalTaskScoreMessage();
            }
        }
    });
    var arrTaskScoreMessage = [], ij=0;
    var globalTaskScoreMessage = function(){
        if(arrTaskScoreMessage.length<=ij){
            $("#classmeetingSreen").modal('hide');
            return;
        }
        $("#classmeetingSreen").html(arrTaskScoreMessage[ij]);

        $("#classmeetingSreen").modal('show');
        ij++;
        var oClose = $('.zy_mypersonal2 .cl');
        oClose.live('click',function(){
            $(this).parent().remove();
            setTimeout(globalTaskScoreMessage,200);
        });
    };
}

// 缺席消息提醒
function class_meeting_absence(student_id,class_id){
    $.ajax({
        url: "/lps3/student/ajax/class_meeting_absence/",
        type: "GET",
        data: {'user_id':student_id,'class_id': class_id},
        dataType: 'JSON',
        success : function(data){
            if(data.status){
                // 显示消息交互
                //console.log(data.data);
                ij=0;
                arrTaskScoreMessage = data.data;
                //$("#MyTaskScore").html(data.data[0]);
                //$("#MyTaskScore").modal('show');
                globalTaskScoreMessage();
            }
        }
    });
    var arrTaskScoreMessage = [], ij=0;
    var globalTaskScoreMessage = function(){
        if(arrTaskScoreMessage.length<=ij){
            $("#classmeetingSreen").modal('hide');
            return;
        }
        $("#classmeetingSreen").html(arrTaskScoreMessage[ij]);

        $("#classmeetingSreen").modal('show');
        ij++;
        var oClose = $('.zy_mypersonal2 .cl');
        oClose.live('click',function(){
            $(this).parent().remove();
            setTimeout(globalTaskScoreMessage,200);
        });
    };
}