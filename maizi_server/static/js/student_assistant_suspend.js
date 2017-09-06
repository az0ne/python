function onQueryAll()
{
    var career_id =  _getQueryValue($("#slctCareer").val());
    var assistant_id = $("#slctAssistant").val();

    var pageSize = $("#slctPageSize").val();
    var params = "career_id=" + career_id;
    params += "&assistant_id=" + assistant_id;
    params += "&page_size=" + pageSize
    window.location.href = "/student_assistant_suspend_all/?" + params ;
}

function onQuery()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_suspend/?student_id=" + student_id;
}

function onAdd()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_suspend/add/?student_id=" + student_id;
}

function onAddDo()
{
        var student_id = $("#txtStudentID").val();
        var assistant_id = $("#slctAssistant").val();
        var start_at = $("#txtStartAt").val();
        var end_at = $("#txtEndAt").val();
        var reason = $("#txtReason").val();

        if (assistant_id == "") {
            _alertDialog("提示","请选择教务老师");
            return;
        }

        if (_isDate(start_at) == false) {
            _alertDialog("提示","开始日期请以2018-08-18的格式");
            return;
        }

        if (_isDate(end_at) == false) {
            _alertDialog("提示","结束日期请以2018-08-18的格式");
            return;
        }

        if (_checkStringLength(reason,10,500) == false) {
            _alertDialog("提示","休学理由在10~500个字符之间");
            return;
        }
        $.post("/student_assistant_suspend/add/do/",
            {
                student_id : student_id,
                start_at : start_at,
                end_at : end_at,
                reason : reason,
                assistant_id : assistant_id
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/update/success/?return_url=/student_assistant/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn(student_id)
{
    window.location.href = "/student_assistant_suspend/?student_id=" + student_id;
}

function goBack()
{
    history.go(-1);
}

function onDetail(id)
{
    window.location.href = "/student_assistant_suspend/detail/?id=" + id;
}