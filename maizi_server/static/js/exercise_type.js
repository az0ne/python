/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery()
{
    var exercise_type =  _getQueryValue($("#txtExerciseType").val());
    window.location.href = "/exercise_type/?exercise_type=" + exercise_type;
}


function onAdd()
{
    window.location.href = "/exercise_type/add/";
}

function onUpdate(id)
{
    window.location.href = "/exercise_type/update/?id=" + id;
}

function onViewExercise(exercise_type_id)
{
    window.location.href = "/exercise/?exercise_type_id=" + exercise_type_id;
}

function onAddDo()
{
    var exercise_type = $('#txtExerciseType').val();

        if (_checkStringLength(exercise_type,2,20) == false) {
            _alertDialog("提示","练习题分类在2~20个字符之间");
            return;
        }

        $.post("/exercise_type/add/do/",
            {
                exercise_type: exercise_type
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/add/success/?op_url=/exercise_type/add/&return_url=/exercise_type/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onUpdateDo()
{
    var exercise_type_id = $('#txtExerciseTypeID').val();
    var exercise_type = $('#txtExerciseType').val();

        if (_checkStringLength(exercise_type,2,20) == false) {
            _alertDialog("提示","练习题分类在2~20个字符之间");
            return;
        }

        $.post("/exercise_type/update/do/",
            {
                id: exercise_type_id,
                exercise_type: exercise_type
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/update/success/?return_url=/exercise_type/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn()
{
    window.location.href = "/exercise_type/";
}

