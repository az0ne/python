/**
 * Created by Administrator on 2017/3/6.
 */

function onQuery() {
    var account = _getQueryValue($("#txtAccount").val());
    var student_name = _getQueryValue($("#txtStudentName").val());
    var sailer = _getQueryValue($("#txtSailer").val());
    var phone = _getQueryValue($("#txtPhone").val());
    var qq = _getQueryValue($("#txtQQ").val());
    var pageSize = $("#slctPageSize").val();
    var remark = $("#getremark").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    var params = "&account=" + account;
    params += "&student_name=" + student_name;
    params += "&sailer=" + sailer;
    params += "&phone=" + phone;
    params += "&qq=" + qq;
    params += "&page_size=" + pageSize;
    params += "&start_time=" + start_time;
    params += "&end_time=" + end_time;
    window.location.href = "/student_sailer/?remark=" + remark + params;
}

function onAddSail() {
    var remark = $("#getremark").val();
    window.location.href = "/student_sailer/add/?remark=" + remark;
}

function onUpdateSail(id) {
    var remark = $("#getremark").val();
    window.location.href = "/student_sailer/update/?id=" + id + "&remark=" + remark;
}

function onAddDo() {
    var account = $("#txtAccount").val();
    var student_name = $("#txtStudentName").val();
    var phone = $("#txtPhone").val();
    var qq = $("#txtQQ").val();
    var address = $("#txtAddress").val();
    var pay_money = $("#txtPayMoney").val();
    var pay_real = $("#txtPayReal").val();
    var pay_type = $("#txtPayType").val();
    var pay_order_num = $("#txtPayOrderNum").val();
    var filename = $('#txtFileName').val();
    var extension = $('#txtExtension').val();

    var sailer = $("#txtSailer").val();
    var sail_at = $("#txtSailAt").val();
    var sail_remark = $("#txtSailRemark").val();
    var student_remark = $("#txtStudentRemark").val();

    var career_id = $("#slctCareer").val();
    var career_job = $("input[name='rdoCareerJob']:checked").val();
    var assistant_id = $("#slctAssistant").val();
    var teacher_id = $("#slctTeacher").val();

    var reward = $("input[name='rdoReward']:checked").val();
    var reward_month = $("#slctRewardMonth").val();
    var bank = $("#txtBank").val();
    var bank_account = $("#txtBankAccount").val();
    var idcard = $("#txtIDCard").val();

    var loan = $("input[name='rdoLoan']:checked").val();
    var loan_company = $("#txtLoanCompany").val();
    var loan_type = $("#txtLoanType").val();
    var loan_interest = $("#txtLoanInterest").val();
    var loan_person = $("#txtLoanPerson").val();
    var loan_money = $("#txtLoanMoney").val();
    var subsidy = $("#txtSubsidy").val();
    var reduction = $("#txtReduction").val();

    if( idcard == ""){
        _alertDialog("提示", "身份证号必填");
        return;
    }
    if (_checkStringLength(account, 2, 20) == false) {
        _alertDialog("提示", "麦子账号在2~50个字符之间");
        return;
    }

    if (_checkStringLength(student_name, 2, 10) == false) {
        _alertDialog("提示", "学员姓名在2~10个字符之间");
        return;
    }

    if (_checkPhone(phone) == false) {
        _alertDialog("提示", "请输入正确的手机号");
        return;
    }

    if (_checkStringLength(qq, 2, 20) == false) {
        _alertDialog("提示", "qq在2~20个字符之间");
        return;
    }

    if (_checkStringLength(address, 2, 20) == false) {
        _alertDialog("提示", "所在地在2~20个字符之间");
        return;
    }
    if (career_id == "") {
        _alertDialog("提示", "请选择所学专业");
        return;
    }

    if (career_job == "") {
        _alertDialog("提示", "请选择就业类型");
        return;
    }

    if (_isInteger(pay_money) == false) {
        _alertDialog("提示", "支付金额请输入正整数");
        return;
    }

    if (_checkStringLength(pay_type, 2, 20) == false) {
        _alertDialog("提示", "支付方式在2~10个字符之间");
        return;
    }

    if (_isDate(sail_at) == false) {
        _alertDialog("提示", "成单日期请以2018-08-18的格式");
        return;
    }

    if (teacher_id == "") {
        _alertDialog("提示", "请选择技术老师");
        return;
    }

    if (assistant_id == "") {
        _alertDialog("提示", "请选择教务老师");
        return;
    }

    if (_checkStringLength(sail_remark, 10, 500) == false) {
        _alertDialog("提示", "销售备注在10~500个字符之间");
        return;
    }

    if (_checkStringLength(student_remark, 10, 500) == false) {
        _alertDialog("提示", "学员概况在10~500个字符之间");
        return;
    }
    $.post("/student_sailer/add/do/",
        {
            account: account,
            student_name: student_name,
            phone: phone,
            qq: qq,
            address: address,
            pay_money: pay_money,
            pay_type: pay_type,
            sailer: sailer,
            sail_at: sail_at,
            sail_remark: sail_remark,
            student_remark: student_remark,
            career_id: career_id,
            career_job: career_job,
            assistant_id: assistant_id,
            teacher_id: teacher_id,
            reward: reward,
            reward_month: reward_month,
            bank: bank,
            bank_account: bank_account,
            idcard: idcard,
            loan: loan,
            loan_company: loan_company,
            loan_type: loan_type,
            loan_interest: loan_interest,
            loan_person: loan_person,
            loan_money: loan_money,
            subsidy: subsidy,
            reduction: reduction,
            pay_order_num: pay_order_num,
            pay_real: pay_real,
            filename1: arryImgUP[0],
            filename2: arryImgUP[1],
            filename3: arryImgUP[2],
            extension: extension

        },
        function (data, status) {
            if (data.code == 200) {
                if (data.success) {
                    window.location.href = "/add/success/?op_url=/student_sailer/add/&return_url=/student_sailer/";
                }
                else {
                    _alertDialog("提示", data.message);
                }
            }
        });
}

function onUpdateDo() {
    var student_id = $('#txtStudentID').val();

    var account = $("#txtAccount").val();
    var student_name = $("#txtStudentName").val();
    var phone = $("#txtPhone").val();
    var qq = $("#txtQQ").val();
    var address = $("#txtAddress").val();
    var pay_money = $("#txtPayMoney").val();
    var pay_real = $("#txtPayReal").val();
    var pay_type = $("#txtPayType").val();
    var pay_order_num = $("#txtPayOrderNum").val();
    var file_name = $('#txtFileName').val();
    var extension = $('#txtExtension').val();

    var sailer = $("#txtSailer").val();
    var sail_at = $("#txtSailAt").val();
    var sail_remark = $("#txtSailRemark").val();
    var student_remark = $("#txtStudentRemark").val();

    var career_id = $("#slctCareer").val();
    var career_job = $("input[name='rdoCareerJob']:checked").val();
    var assistant_id = $("#slctAssistant").val();
    var teacher_id = $("#slctTeacher").val();

    var reward = $("input[name='rdoReward']:checked").val();
    var reward_month = $("#slctRewardMonth").val();
    var bank = $("#txtBank").val();
    var bank_account = $("#txtBankAccount").val();
    var idcard = $("#txtIDCard").val();

    var loan = $("input[name='rdoLoan']:checked").val();
    var loan_company = $("#txtLoanCompany").val();
    var loan_type = $("#txtLoanType").val();
    var loan_interest = $("#txtLoanInterest").val();
    var loan_person = $("#txtLoanPerson").val();
    var loan_money = $("#txtLoanMoney").val();
    var subsidy = $("#txtSubsidy").val();
    var reduction = $("#txtReduction").val();

    if (_checkStringLength(account, 2, 20) == false) {
        _alertDialog("提示", "麦子账号在2~50个字符之间");
        return;
    }

    if (_checkStringLength(student_name, 2, 10) == false) {
        _alertDialog("提示", "学员姓名在2~10个字符之间");
        return;
    }

    if (_checkPhone(phone) == false) {
        _alertDialog("提示", "请输入正确的手机号");
        return;
    }

    if (_checkStringLength(qq, 2, 20) == false) {
        _alertDialog("提示", "qq在2~20个字符之间");
        return;
    }

    if (_checkStringLength(address, 2, 20) == false) {
        _alertDialog("提示", "所在地在2~20个字符之间");
        return;
    }
    if (career_id == "") {
        _alertDialog("提示", "请选择所学专业");
        return;
    }

    if (career_job == "") {
        _alertDialog("提示", "请选择就业类型");
        return;
    }

    if (_isInteger(pay_money) == false) {
        _alertDialog("提示", "支付金额请输入正整数");
        return;
    }

    if (_checkStringLength(pay_type, 2, 20) == false) {
        _alertDialog("提示", "支付方式在2~10个字符之间");
        return;
    }

    if (_isDate(sail_at) == false) {
        _alertDialog("提示", "成单日期请以2018-08-18的格式");
        return;
    }

    if (teacher_id == "") {
        _alertDialog("提示", "请选择技术老师");
        return;
    }

    if (assistant_id == "") {
        _alertDialog("提示", "请选择教务老师");
        return;
    }

    if (_checkStringLength(sail_remark, 10, 500) == false) {
        _alertDialog("提示", "销售备注在10~500个字符之间");
        return;
    }

    if (_checkStringLength(student_remark, 10, 500) == false) {
        _alertDialog("提示", "学员概况在10~500个字符之间");
        return;
    }

    $.post("/student_sailer/update/do/",
        {
            id: student_id,
            account: account,
            student_name: student_name,
            phone: phone,
            qq: qq,
            address: address,
            pay_money: pay_money,
            pay_type: pay_type,
            sailer: sailer,
            sail_at: sail_at,
            sail_remark: sail_remark,
            student_remark: student_remark,
            career_id: career_id,
            career_job: career_job,
            assistant_id: assistant_id,
            teacher_id: teacher_id,
            reward: reward,
            reward_month: reward_month,
            bank: bank,
            bank_account: bank_account,
            idcard: idcard,
            loan: loan,
            loan_company: loan_company,
            loan_type: loan_type,
            loan_interest: loan_interest,
            loan_person: loan_person,
            loan_money: loan_money,
            subsidy: subsidy,
            reduction: reduction,
            pay_order_num: pay_order_num,
            pay_real: pay_real,
            filename1: arryImgUP[0],
            filename2: arryImgUP[1],
            filename3: arryImgUP[2],
            extension: extension
        },
        function (data, status) {
            if (data.code == 200) {
                if (data.success) {
                    window.location.href = "/update/success/?return_url=/student_sailer/";
                }
                else {
                    _alertDialog("提示", data.message);
                }
            }
        });
}

function onReturn() {
    var remark = $("#getremark").val();
    window.location.href = "/student_sailer/?" + "remark=" + remark;
}

$(document).ready(function () {
    arryImgUP = [];
    $("#file").pekeUpload({
        "btnText": "请选择文件",
        "url": "/upload/",
        "allowedExtensions": "png|jpg|doc|docx|pdf|xls|xlsx|ppt|pptx",
        "invalidExtError": "文件格式不正确",
        "bootstrap": true,
        "delfiletext": "移除",
        "showPreview": false,
        "limit": 3,
        "limitError": "只能上传3个文件",
        "onFileError": function (file, error) {
            console.log(error);
        },
        "onFileSuccess": function (file, data) {
            console.log(data);
            if (data.code == true) {
                arryImgUP.push(data.file_name);
                console.log(arryImgUP);
                $("#txtExtension").val(data.extension);

                $("#upimgtd div").attr("margin-bottom",10);
            }
        }
    });

    $("#txtPayReal").blur(function () {

        var pay_money = $("#txtPayMoney").val();
        var pay_real = $("#txtPayReal").val();
        var txtReduction = $("#txtReduction").val();
        // $("#txtPayReal").val(pay_money-txtReduction);
       $("#txtReduction").val(pay_money-pay_real);
    });
    $("#txtPayMoney").blur(function () {

        var pay_money = $("#txtPayMoney").val();
        var pay_real = $("#txtPayReal").val();
        var txtReduction = $("#txtReduction").val();
         // $("#txtReduction").val(pay_money-pay_real);
        $("#txtPayReal").val(pay_money-txtReduction);

    });
    $("#txtReduction").blur(function () {

       var pay_money = $("#txtPayMoney").val();
        var pay_real = $("#txtPayReal").val();
        var txtReduction = $("#txtReduction").val();
        $("#txtPayReal").val(pay_money-txtReduction);
        // $("#txtReduction").val(pay_money-pay_real);
    });
    var get_remark = $("#getremark").val();
    console.log(get_remark);
    if (get_remark == "财务") {
        $(".tag").hide();
        $(".item").hide();
        $(".tag").eq(1).show();
        $(".item").eq(0).show();
        $(".tag").removeAttr("href");
        $(".item").removeAttr("href");
        $("#add-sailer-btn").hide();
    }
    console.log($("#getUPImgInfo3").val());
});

function excel_export() {
    var account = _getQueryValue($("#txtAccount").val());
    var student_name = _getQueryValue($("#txtStudentName").val());
    var sailer = _getQueryValue($("#txtSailer").val());
    var phone = _getQueryValue($("#txtPhone").val());
    var qq = _getQueryValue($("#txtQQ").val());
    var pageSize = $("#slctPageSize").val();
    var remark = $("#getremark").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    var is_all = "true"

    var params = "&account=" + account;
    params += "&student_name=" + student_name;
    params += "&sailer=" + sailer;
    params += "&phone=" + phone;
    params += "&qq=" + qq;
    params += "&page_size=" + pageSize;
    params += "&start_time=" + start_time;
    params += "&end_time=" + end_time;
    params += "&is_all=" + is_all;
    window.location.href = "/excel_export/?" + remark + params;

}