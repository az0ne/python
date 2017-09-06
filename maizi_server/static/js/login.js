
$(document).ready(function () {
    $('#spnUserName').hide();
    $('#spnPassword').hide();

    $('#btnLogin').click(function() {

        $('#spnUserName').hide();
        $('#spnPassword').hide();

		var user_name = $('#txtUserName').val();
        var password = $('#txtPassword').val();

        if (_checkPhone(user_name) == false) {
            $('#spnUserName').show();
            $("#spnUserName").html("请输入正确的手机号");
            return;
        }

        if (_checkPassword(password) == false) {
            $('#spnPassword').show();
            $("#spnPassword").html("密码以字母开头，长度在6~18之间，只能包含字符、数字和下划线");
            return;
        }

        $.post("/user/login/",
            {
                user_name: user_name,
                password: password
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        var remark = data.message;

                        window.location.href = "/home/?"+"remark="+remark;
                    }
                    else {
                        $('#spnPassword').show();
                        $("#spnPassword").html(data.message);
                    }
                }
            });
    });
});
