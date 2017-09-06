/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery()
{
    window.location.href = "/teacher/";
}

function onStop(id)
{
    _confirmDialog1("请确认","您是否确认禁用？",function(val){
        window.location.href = "/teacher/stop/?id=" + val;
    },id);
}

function onStart(id)
{
    _confirmDialog1("请确认","您是否确认启用？",function(val){
        window.location.href = "/teacher/start/?id=" + val;
    },id);
}

function onAdd()
{
    window.location.href = "/teacher/add/";
}

function onUpdate(id)
{
    window.location.href = "/teacher/update/?id=" + id;
}

function onAddDo()
{
    var name = $('#txtName').val();
    var phone = $('#txtPhone').val();
    var qq = $('#txtQQ').val();

        if (_checkStringLength(name,2,10) == false) {
            _alertDialog("提示","真实姓名在2~10个字符之间");
            return;
        }

        if (_checkPhone(phone) == false) {
            _alertDialog("提示","请输入正确的手机号");
            return;
        }

        if (_checkStringLength(qq,5,20) == false) {
            _alertDialog("提示","真实姓名在5~20个字符之间");
            return;
        }

        $.post("/teacher/add/do/",
            {
                name: name,
                phone: phone,
                qq: qq
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/add/success/?op_url=/teacher/add/&return_url=/teacher/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onUpdateDo()
{
    var teacher_id = $('#txtteacherID').val();
    var name = $('#txtName').val();
    var phone = $('#txtPhone').val();
    var qq = $('#txtQQ').val();

        if (_checkStringLength(name,2,10) == false) {
            _alertDialog("提示","真实姓名在2~10个字符之间");
            return;
        }

        if (_checkPhone(phone) == false) {
            _alertDialog("提示","请输入正确的手机号");
            return;
        }

        if (_checkStringLength(qq,5,20) == false) {
            _alertDialog("提示","真实姓名在5~20个字符之间");
            return;
        }

        $.post("/teacher/update/do/",
            {
                id: teacher_id,
                name: name,
                phone: phone,
                qq: qq
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/update/success/?return_url=/teacher/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn()
{
    window.location.href = "/teacher/";
}

