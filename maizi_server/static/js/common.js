/**
 * Created by Administrator on 2017/3/6.
 */
function _checkPhone(phone) {
    if (!(/^1[34578]\d{9}$/.test(phone))) {
        return false;
    }
    return true;
}

function _checkPassword(password) {
    if (!(/^[a-zA-Z]\w{5,17}$/.test(password))) {
        return false;
    }
    return true;
}

function _checkStringLength(str,minLength,maxLength) {
    if(str.length>= minLength && str.length <= maxLength)
    {
        return true;
    }
    return false;
}

function _isDate(date) {

if (!(/((^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(10|12|0?[13578])([-\/\._])(3[01]|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(11|0?[469])([-\/\._])(30|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(0?2)([-\/\._])(2[0-8]|1[0-9]|0?[1-9])$)|(^([2468][048]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([3579][26]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][13579][26])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][13579][26])([-\/\._])(0?2)([-\/\._])(29)$))/.test(date))) {
        return false;
    }
    return true;
}

function _alertDialog(title,content)
{
    $("#alertTitle").html(title);
    $("#alertContent").html(content);
    $("#alertDialog").modal();
}

function _confirmDialog(title,content)
{
    $("#confirmTitle").html(title);
    $("#confirmContent").html(content);
    $("#confirmDialog").modal();
}

function _confirmDialog1(title,content,func,param)
{
    _confirmDialog(title,content);
    $("#confirm_btnOK").click(function() {
        func(param);
    });
}

function _confirmDialog2(title,content,func,param1,param2)
{
    _confirmDialog(title,content);
    $("#confirm_btnOK").click(function() {
        func(param1,param2);
    });
}

function _isInteger(val) {

    var re = /^[0-9]*[1-9][0-9]*$/ ;
    return re.test(val)

}

function _getQueryValue(val) {
    return _trim(val);
}

function _trim(str){ //删除左右两端的空格　　
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function _ltrim(str){ //删除左边的空格
    return str.replace(/(^\s*)/g,"");
}

function _rtrim(str){ //删除右边的空格
　　return str.replace(/(\s*$)/g,"");
}

function _doLoginOut() {

    $.post("/user/login_out/",
        {},
        function (data, status) {
            if (data.code == 200) {
                if (data.success) {
                    window.location.href = "/";
                }
            }
        });
}
