/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery()
{
    var user_name =  _getQueryValue($("#txtUserName").val());
    var real_name =  _getQueryValue($("#txtRealName").val());
    var pageSize = $("#slctPageSize").val();
    var params = "user_name="+user_name;
    params += "&real_name="+real_name;
    params += "&page_size=" + pageSize
    window.location.href = "/user/?" + params ;
}

function onStop(id)
{
    _confirmDialog1("请确认","您是否确认禁用？",function(val){
        window.location.href = "/user/stop/?id=" + val + "&" + page_getQuery();
    },id);
}

function onStart(id)
{
    _confirmDialog1("请确认","您是否确认启用？",function(val){
        window.location.href = "/user/start/?id=" + val + "&" + page_getQuery();
    },id);
}

function onAdd()
{
    window.location.href = "/user/add/";
}

function onUpdate(id)
{
    window.location.href = "/user/update/?id=" + id;
}

function onAddDo()
{
    var user_name = $('#txtUserName').val();
    var real_name = $('#txtRealName').val();
    var password = $('#txtPassword').val();
    var password2 = $('#txtPassword2').val();
    var remark = $('#txtRemark').val();

        if (_checkPhone(user_name) == false) {
            _alertDialog("提示","请输入正确的手机号");
            return;
        }

        if (_checkStringLength(real_name,2,10) == false) {
            _alertDialog("提示","真实姓名在2~10个字符之间");
            return;
        }

        if (_checkPassword(password) == false) {
            _alertDialog("提示","密码以字母开头，长度在6~18之间，只能包含字符、数字和下划线");
            return;
        }

        if (password != password2) {
            _alertDialog("提示","两次密码输入不一致");
            return;
        }

        $.post("/user/add/do/",
            {
                user_name: user_name,
                real_name: real_name,
                password: password,
                remark: remark
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/add/success/?op_url=/user/add/&return_url=/user/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onUpdateDo()
{
    var user_id = $('#txtUserID').val();
    var user_name = $('#txtUserName').val();
    var real_name = $('#txtRealName').val();
    var password = $('#txtPassword').val();
    var password2 = $('#txtPassword2').val();
    var remark = $('#txtRemark').val();

        if (_checkStringLength(real_name,2,10) == false) {
            _alertDialog("提示","真实姓名在2~10个字符之间");
            return;
        }

        if (_checkPassword(password) == false) {
            _alertDialog("提示","密码以字母开头，长度在6~18之间，只能包含字符、数字和下划线");
            return;
        }

        if (password != password2) {
            _alertDialog("提示","两次密码输入不一致");
            return;
        }

        $.post("/user/update/do/",
            {
                id: user_id,
                user_name: user_name,
                real_name: real_name,
                password: password,
                remark: remark
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/update/success/?return_url=/user/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn()
{
    window.location.href = "/user/";
}

