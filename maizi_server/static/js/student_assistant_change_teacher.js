function onQuery()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_change_teacher/?student_id=" + student_id;
}

function onAdd()
{
    var student_id = $("#txtStudentID").val();
    window.location.href = "/student_assistant_change_teacher/add/?student_id=" + student_id;
}

function onAddDo()
{
        var student_id = $("#txtStudentID").val();
        var old_teacher_id = $("#txtOldTeacherID").val();
        var new_teacher_id = $("#slctNewTeacher").val();
        var change_at = $("#txtChangeAt").val();
        var reason = $("#txtReason").val();

        if (new_teacher_id == "") {
            _alertDialog("提示","请选择所要更换的老师");
            return;
        }

        if (_isDate(change_at) == false) {
            _alertDialog("提示","更换日期请以2018-08-18的格式");
            return;
        }

        if (_checkStringLength(reason,10,500) == false) {
            _alertDialog("提示","更换原因在10~500个字符之间");
            return;
        }
        $.post("/student_assistant_change_teacher/add/do/",
            {
                student_id : student_id,
                old_teacher_id : old_teacher_id,
                new_teacher_id : new_teacher_id,
                change_at : change_at,
                reason : reason
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
    window.location.href = "/student_assistant_change_teacher/?student_id=" + student_id;
}