$(function(){
    load_provid(); //加载省份

    $("#id_prov").change(function(){
        var val = $("#id_prov").val();
        console.log(val)
        city_list(val);
    });

    $("#student_info_submit").click(function(){
        var valStr="不能为空"
        var real_name = $("#real_name").val().trim();
        if (!real_name) {
            layer.tips(valStr, $("#real_name"), {tips: [2, '#68c8b6']});
            $("#real_name").focus();
            return;
        }
        var mobile = $("#mobile").val().trim();
        console.log(mobile)
        if (!mobile||!checkPhone(mobile)) {
            if(!checkPhone(mobile)){valStr="手机格式错误"}
            layer.tips(valStr, $("#mobile"), {tips: [2, '#68c8b6']});
            $("#mobile").focus();
            return;
        }
        var qq = $("#qq").val().trim();
        if (!qq||!isnum(qq)||!(qq.length>4&&qq.length<13)) {
            if(!isnum(qq)){valStr="QQ格式不对"}
            if(!(qq.length>4&&qq.length<13)){valStr="QQ格式不对"}
            layer.tips(valStr, $("#qq"), {tips: [2, '#68c8b6']});
            $("#qq").focus();
            return;
        }
        var email = $("#email").val().trim();
        if (!email||!isEmail(email)) {
            if(!isEmail(email)){valStr="邮箱格式不正确"}
            layer.tips(valStr, $("#email"), {tips: [2, '#68c8b6']});
            $("#email").focus();
            return;
        }
        var address = $("#address").val().trim();
        if (!address) {
            layer.tips(valStr, $("#address"), {tips: [2, '#68c8b6']});
            $("#address").focus();
            return;
        }
        var data = {'real_name': real_name,
                'qq': qq,
                'email': email,
                'mobile': mobile,
                'address': address,
                'city': $('#id_city').val(),
                'study_goal_opt': $('#study_goal_opt').val(),
                'study_base_opt': $('#study_base_opt').val()
        };
        student_info_submit(data);
    });

    $("#myAgreement2_submit").click(function(){
        var flag = $("#myAgreement2_checkbox").context.checked;
        if (flag == false){
            layer.tips("请勾选同意后方可提交", $("#myAgreement2_checkbox").parent(), {tips: [2, '#68c8b6']});
            return ;
        }
        var data = {
            'checked': true,
            'class_id': class_id,
            'contract': '入学'
        };
        contract_submit(data);
    });
    $("#myAgreement2_checkbox").click(function(){
        if($(this).context.checked) {
            $("#myAgreement2_submit").removeClass("greyBG");
        }else{
            $("#myAgreement2_submit").addClass("greyBG");
        }
    });
    $("#myAgreement3_submit").click(function(){
        var flag = $("#myAgreement3_checkbox").context.checked;
        if (flag == false){
            layer.tips("请勾选后方可提交", $("#myAgreement3_checkbox").parent(), {tips: [2, '#68c8b6']});
            return ;
        }
        var data = {'checked': true,
                'class_id': class_id,
                'contract': '服务'
        };
        contract_submit(data);
    });
    
    $("#myAgreement3_checkbox").click(function(){
        if($(this).context.checked) {
            $("#myAgreement3_submit").removeClass("greyBG");
        }
        else{
            $("#myAgreement3_submit").addClass("greyBG");
        }
    })
    $("#myAgreement_submit").click(function(){
        var flag = $("#myAgreement_checkbox").context.checked;
        if (flag == false){
            layer.tips("请勾选同意后方可提交", $("#myAgreement_checkbox").parent(), {tips: [2, '#68c8b6']});
            return ;
        }
        var data = {'checked': true,
                'class_id': class_id,
                'contract': '就业'
        };
        contract_submit(data);
    });
    $("#myAgreement_checkbox").click(function(){
        if($(this).context.checked) {
            $("#myAgreement_submit").removeClass("greyBG");
        }
        else{
            $("#myAgreement_submit").addClass("greyBG");
        }
    })
});
var zzarr;
// 省份加载
function load_provid(){
    var str = $("#default_p_c").val();
    if(str == undefined){
        return;
    }
    zzarr = str.split("_");
    if(zzarr[0]==""){
        $('#id_prov').children().eq(0).attr("selected","selected");
        city_list($('#id_prov').val());
    }else{
        $("#id_prov").children('[value="'+zzarr[0]+'"]').attr("selected","selected");
        city_list(zzarr[0]);
    }
    $("#id_prov").next().remove();
    $("#id_prov").iSimulateSelect({width:194,height:200,selectBoxCls:"personal_info_selectD",optionCls:"personal_info_selectD_Op"});
}

// 城市加载
function city_list(provid){

    $.ajax({
        type: "GET",
        url: "/user/city/list/",
        data: {provid:provid},
        dataType: "json",
        success: function(data){
            var data = data["cityid"];
            var str = '';
            for(var i in data){
                str += '<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
            var ob=$('#id_city');
            ob.html(str);

            if(zzarr[0]=="") {
                ob.children().eq(0).attr("selected","selected");
            }
            else{
                ob.children('[value="'+zzarr[1]+'"]').attr("selected","selected");
            }
            ob.next().remove();
            ob.iSimulateSelect({width:194,height:200,selectBoxCls:"personal_info_selectD",optionCls:"personal_info_selectD_Op"});
        }
    });
}

//补全用户信息
function student_info_submit(data) {
    $.ajax({
        type: "POST",
        async: false,
        url: "/lps3/student/student_info_submit/",
        data: data,
        dataType: "json",
        success: function(data){
            var data = eval(data);
            if (data['status']) {
                window.location.reload();
            }
            else{
                layer.msg(data.error);
            }
        }
    });
}

//提交协议
function contract_submit(data) {
    $.ajax({
        type: "POST",
        url: "/lps3/student/contract_submit/",
        data: data,
        dataType: "json",
        success: function(data){
            var data = eval(data);
            if (data['status']) {
                window.location.reload();
            }
        }
    });
}

function checkPhone( strPhone ) {
    var phoneRegWithArea = /^1[358]\d{9}$|^147\d{8}$|^176\d{8}$/;
    var phoneRegNoArea = /^[1-9]{1}[0-9]{5,8}$/;
    if( true ) {
        if( phoneRegWithArea.test(strPhone) ){
            return true;
        }else{
            return false;
        }
    }else{
        if( phoneRegNoArea.test( strPhone ) ){
            return true;
        }else{
            return false;
        }
    }
}
function isEmail( str ){
    var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
    if(myReg.test(str)) return true;
    return false;
}
function isnum(str){
    if(!/^[0-9]*$/.test(str)){
        return false;
    }
    return true;
}