function onQuery()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_interview/?student_id=" + student_id;
}

function onAdd()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_interview/add/?student_id=" + student_id;
}

function onUpdate(id)
{
    window.location.href = "/student_assistant_interview/update/?id=" + id;
}

function onAddDo()
{
        var student_id = $("#txtStudentID").val();
        var interviewer = $("#txtInterviewer").val();
        var interview_at = $("#txtInterviewAt").val();
        var state = $('#slctState').val();
        var remark = $("#txtRemark").val();

        if (_checkStringLength(interviewer,2,10) == false) {
            _alertDialog("提示","面试官姓名在2~10个字符之间");
            return;
        }

        if (_isDate(interview_at) == false) {
            _alertDialog("提示","面试日期请以2018-08-18的格式");
            return;
        }

        if (state == "-1") {
            _alertDialog("提示","请选择面试状态");
            return;
        }

        if (_checkStringLength(remark,10,500) == false) {
            _alertDialog("提示","面试评价在10~500个字符之间");
            return;
        }
        $.post("/student_assistant_interview/add/do/",
            {
                student_id : student_id,
                interviewer : interviewer,
                interview_at : interview_at,
                state : state,
                remark : remark
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

function onUpdateDo()
{
        var id = $("#txtID").val();
        var interviewer = $("#txtInterviewer").val();
        var interview_at = $("#txtInterviewAt").val();
        var state = $('#slctState').val();
        var remark = $("#txtRemark").val();

        if (_checkStringLength(interviewer,2,10) == false) {
            _alertDialog("提示","面试官姓名在2~10个字符之间");
            return;
        }

        if (_isDate(interview_at) == false) {
            _alertDialog("提示","面试日期请以2018-08-18的格式");
            return;
        }

        if (state == "-1") {
            _alertDialog("提示","请选择面试状态");
            return;
        }

        if (_checkStringLength(remark,10,500) == false) {
            _alertDialog("提示","面试评价在10~500个字符之间");
            return;
        }
        $.post("/student_assistant_interview/update/do/",
            {
                id : id,
                interviewer : interviewer,
                interview_at : interview_at,
                state : state,
                remark : remark
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
    window.location.href = "/student_assistant_interview/?student_id=" + student_id;
}