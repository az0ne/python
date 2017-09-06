function onQueryAll()
{
    var career_id =  _getQueryValue($("#slctCareer").val());
    var assistant_id = $("#slctAssistant").val();

    var pageSize = $("#slctPageSize").val();
    var params = "career_id="+career_id;
    params += "&assistant_id="+assistant_id;
    params += "&page_size=" + pageSize
    window.location.href = "/student_assistant_communication_all/?" + params ;
}

function onQuery()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_communication/?student_id=" + student_id;
}

function onAdd()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_communication/add/?student_id=" + student_id;
}

function onAddDo()
{
        var student_id = $("#txtStudentID").val();
        var assistant_id = $("#slctAssistant").val();
        var communicate_at = $("#txtCommunicateAt").val();
        var stage = $('#slctStage').val();
        var content = $("#txtContent").val();

        if (assistant_id == "") {
            _alertDialog("提示","请选择教务老师");
            return;
        }

        if (stage == "-1") {
            _alertDialog("提示","请选择沟通阶段");
            return;
        }

        if (_isDate(communicate_at) == false) {
            _alertDialog("提示","沟通日期请以2018-08-18的格式");
            return;
        }

        if (_checkStringLength(content,10,500) == false) {
            _alertDialog("提示","沟通内容在10~500个字符之间");
            return;
        }
        $.post("/student_assistant_communication/add/do/",
            {
                student_id : student_id,
                communicate_at : communicate_at,
                stage : stage,
                content : content,
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
    window.location.href = "/student_assistant_communication/?student_id=" + student_id;
}

function goBack()
{
    history.go(-1);
}

function onDetail(id)
{
    window.location.href = "/student_assistant_communication/detail/?id=" + id;
}