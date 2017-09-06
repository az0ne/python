/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery()
{
    var account =  _getQueryValue($("#txtAccount").val());
    var student_name =  _getQueryValue($("#txtStudentName").val());
    var career_id =  _getQueryValue($("#slctCareer").val());
    var career_job = $("#slctCareerJob").val();
    var assistant_id = $("#slctAssistant").val();
    var teacher_id = $("#slctTeacher").val();
    var reward = $("#slctReward").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();

    var pageSize = $("#slctPageSize").val();
    var params = "account="+account;
    params += "&student_name="+student_name;
    params += "&career_id="+career_id;
    params += "&career_job="+career_job;
    params += "&assistant_id="+assistant_id;
    params += "&teacher_id="+teacher_id;
    params += "&reward="+reward;
    params += "&page_size=" + pageSize;
    params += "&start_time=" + start_time;
    params += "&end_time=" + end_time;

    window.location.href = "/student_assistant/?" + params ;

}

function onUpdateAssistant(id)
{
    window.location.href = "/student_assistant/update/?id=" + id;
}

function onUpdateDo()
{
        var student_id = $('#txtStudentID').val();
        var start_at = $('#txtStartAt').val();
        var graduate_at = $('#txtGraduateAt').val();
        var stage = $('#slctStage').val();
        var state = $('#slctState').val();
        var company = $('#txtCompany').val();

        if (_isDate(start_at) == false) {
            _alertDialog("提示","开始学习日期请以2018-08-18的格式");
            return;
        }

        if (_isDate(graduate_at) == false) {
            _alertDialog("提示","毕业日期请以2018-08-18的格式");
            return;
        }

        if (stage == "-1") {
            _alertDialog("提示","请选择当前阶段");
            return;
        }

        if (state == "-1") {
            _alertDialog("提示","请选择当前状态");
            return;
        }

        $.post("/student_assistant/update/do/",
            {
                id : student_id,
                start_at : start_at,
                graduate_at : graduate_at,
                stage : stage,
                state : state,
                company : company
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

function onReturn()
{
    window.location.href = "/student_assistant/";
}

function onChangeTeacher(student_id)
{
    window.location.href = "/student_assistant_change_teacher/?student_id=" + student_id;
}

function onChangeAssistant(student_id)
{
    window.location.href = "/student_assistant_change_assistant/?student_id=" + student_id;
}

function onAddCommunication(student_id)
{
    window.location.href = "/student_assistant_communication/?student_id=" + student_id;
}

function onAddInterview(student_id)
{
    window.location.href = "/student_assistant_interview/?student_id=" + student_id;
}

function onAddSuspend(student_id)
{
    window.location.href = "/student_assistant_suspend/?student_id=" + student_id;
}

function excel_export() {
    var account =  _getQueryValue($("#txtAccount").val());
    var student_name =  _getQueryValue($("#txtStudentName").val());
    var career_id =  _getQueryValue($("#slctCareer").val());
    var career_job = $("#slctCareerJob").val();
    var assistant_id = $("#slctAssistant").val();
    var teacher_id = $("#slctTeacher").val();
    var reward = $("#slctReward").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    var is_all = "true"

    var pageSize = $("#slctPageSize").val();
    var params = "account="+account;
    params += "&student_name="+student_name;
    params += "&career_id="+career_id;
    params += "&career_job="+career_job;
    params += "&assistant_id="+assistant_id;
    params += "&teacher_id="+teacher_id;
    params += "&reward="+reward;
    params += "&page_size=" + pageSize;
    params += "&start_time=" + start_time;
    params += "&end_time=" + end_time;
    params += "&is_all=" + is_all;

    window.location.href = "/assistant/excel_export/?" + params ;

}