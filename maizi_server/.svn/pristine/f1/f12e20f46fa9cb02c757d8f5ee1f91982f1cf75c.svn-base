/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery()
{
    window.location.href = "/career/";
}

function onStop(id)
{
    _confirmDialog1("请确认","您是否确认禁用？",function(val){
        window.location.href = "/career/stop/?id=" + val;
    },id);
}

function onStart(id)
{
    _confirmDialog1("请确认","您是否确认启用？",function(val){
        window.location.href = "/career/start/?id=" + val;
    },id);
}

function onAdd()
{
    window.location.href = "/career/add/";
}

function onUpdate(id)
{
    window.location.href = "/career/update/?id=" + id;
}

function onAddDo()
{
    var name = $('#txtName').val();
    var type = $("input[name='rdoType']:checked").val();
    var remark = $('#txtRemark').val();

        if (_checkStringLength(name,2,20) == false) {
            _alertDialog("提示","课程名称在2~20个字符之间");
            return;
        }

        $.post("/career/add/do/",
            {
                name: name,
                type: type,
                remark: remark
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/add/success/?op_url=/career/add/&return_url=/career/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onUpdateDo()
{
    var career_id = $('#txtCareerID').val();
    var name = $('#txtName').val();
    var type = $("input[name='rdoType']:checked").val();
    var remark = $('#txtRemark').val();

        if (_checkStringLength(name,2,20) == false) {
            _alertDialog("提示","真实姓名在2~20个字符之间");
            return;
        }

        $.post("/career/update/do/",
            {
                id: career_id,
                name: name,
                type: type,
                remark: remark
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/update/success/?return_url=/career/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn()
{
    window.location.href = "/career/";
}

