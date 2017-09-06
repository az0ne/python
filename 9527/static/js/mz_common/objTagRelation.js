/**
 * Created by zml on 2016/5/20.
 */

$(function () {
    /*------------------------------------------------弹出模态框--------------------------------------------------------*/
    //添加
    $(document).off('click', '#btn_addObjTagRelation').on('click', '#btn_addObjTagRelation', function () {
        $('#modal_addObjTagRelation').modal('show');
        modalInputFieldInit('#modal_addObjTagRelation');
        modalErrorLableInit('#modal_addObjTagRelation');
    });
    //删除
    $(document).off('click', '.btn_delObjTagRelation').on('click', '.btn_delObjTagRelation', function () {
        $('#delObjTagRelationMessage').text('确定要删除“' + $(this).parents().data('title') + '”个人中心广告吗？'); //删除提示信息
        selectDelRowId = $(this).parent().data('id');  //获取Id
        $('#modal_delObjTagRelation').modal('show');
    });
    //修改
    $(document).off('click', '.btn_editObjTagRelation').on('click', '.btn_editObjTagRelation', function () {
        modalErrorLableInit('#modal_editObjTagRelation');
        selectEditRowId = $(this).parent().data('id');
        var data = getData('/ajax/objTagRelation/get/', selectEditRowId).responseJSON.result;
        $('#slt_edit_obj_name').val(data.obj_id);
        $('#slt_edit_careercatagory_name').val(data.careercatagory_id);
        $('#slt_edit_tag_name').val(data.tag_id);
        $('#slt_edit_obj_type').val(data.obj_type);
        $('#modal_editObjTagRelation').modal('show');
    });
    //查看
    $(document).off('click', '.btn_showObjTagRelation').on('click', '.btn_showObjTagRelation', function () {
        $('#lbl_obj_name').text($(this).parents('tr').children('.td_obj_name').text());
        $('#lbl_careercatagory_name').text($(this).parents('tr').children('.td_careercatagory_name').text());
        $('#lbl_tag_name').text($(this).parents('tr').children('.td_tag_name').text());
        $('#lbl_obj_type').text($(this).parents('tr').children('.td_obj_type').text());
        $('#modal_showObjTagRelation').modal('show');
    });
    /*-------------------------------------------------------END--------------------------------------------------------*/
    /*------------------------------------------------模态框按钮单击事件------------------------------------------------*/
    //添加/-保存按钮
    $(document).off('click', '#btn_saveAddObjTagRelation').on('click', '#btn_saveAddObjTagRelation', function () {
        var commitData = new FormData($('#form_addObjTagRelation')[0]);
        // var result = formDataCommitValidate('modal_addObjTagRelation');
        var result = formDataCommitValidate();
        if (result.code == 0) {
            addOrUpdateData('/ajax/objTagRelation/create/', '/ajax/objTagRelation/list/', commitData, '#modal_addObjTagRelation');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //修改-保存按钮
    $(document).off('click', '#btn_saveEditObjTagRelation').on('click', '#btn_saveEditObjTagRelation', function () {
        var commitData = new FormData($('#form_editObjTagRelation')[0]);
        commitData.append('id', selectEditRowId);
        // var result = formDataCommitValidate('modal_editObjTagRelation');
        if (result.code == 0) {
            addOrUpdateData('/ajax/objTagRelation/update/', '/ajax/objTagRelation/list/', commitData, '#modal_editObjTagRelation');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //删除-确定按钮
    $(document).off('click', '#btn_ensureDelObjTagRelation').on('click', '#btn_ensureDelObjTagRelation', function () {
        deleteData('/ajax/objTagRelation/delete/', '/ajax/objTagRelation/list/', selectDelRowId, '#modal_delObjTagRelation');
    });
    /*-------------------------------------------------------END---------------------------------------------------------*/
    /*------------------------------------------------填充下拉列表框---------------------------------------------------*/
    //当obj_type改变时，重新填充obj_name中的值
    $('#slt_add_obj_type').off('change').on('change', function () {
        var obj_type = $(this).val();
        var typeTableRelation = {'ARTICLE': '/ajax/articleType/get/', 'COURSE': '/ajax/careerCourse/get/'}
        if (obj_type == 0) {
            $('#slt_add_obj_name').val(0);
        } else {
            addObjectNameOption(typeTableRelation[obj_type]);
        }

    });
    /*------------------------------------------------下拉列表框填充---------------------------------------------------*/
    // addObjectNameOption();  // 对象名称
    addTagNameOption();   //  标签名称
    addCareerCategoryOption();  //专业方向
});
/*------------------------------------------------把查询数据渲染到页面--------------------------------------------------*/
/*渲染表格数据*/
function showDataInTable(pageIndex, pageSize, data, selectUrl) {
    var dataList = [];
    var serialNumber = (pageIndex - 1) * pageSize;
    var objectType = {'ARTICLE': '文章', 'TEACHER': '老师', 'COURSE': '课程'};
    if (data.result.totalCounts == 0) {
        dataList.push('<label>查询到0条数据！</label>');
    } else if (data.result.data.length == 0) { // 删除之前当前页只有一条数据，删除后跳到前一页
        selectData(selectUrl, pageIndex - 1, 15);
    }
    else {
        $.each(data.result.data, function (index, item) {
            var objectTypeKey = item.obj_type;
            serialNumber += 1;
            dataList.push('<tr><td style="text-align: center">' + serialNumber + '</td>');
            dataList.push('<td class="td_tag_name" data-id="' + item.tag_id + '"> ' + item.tag_name + '</td>');
            dataList.push('<td class="td_careercatagory_name" data-id="' + item.careercatagory_id + '">' + item.careercatagory_name + '</td>');
            dataList.push('<td class="td_obj_type" data-id="' + item.obj_type + '">' + item.obj_type + '</td>');
            dataList.push('<td class="td_obj_name" data-id="' + item.obj_id + '">' + item.obj_name + '</td>');
            dataList.push('<td data-id="' + item.id + '" data-title="">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showObjTagRelation" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delObjTagRelation" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
        });
    }
    $('#dataTable').children().remove();
    $('#dataTable').append(dataList.toString());
    $("#pagerDataInfo").text("共" + data.result.totalPages + "页" + data.result.totalCounts + "条数据");
    $('#pagination1').jqPaginator('option', {
        totalPages: data.result.totalPages,
        currentPage: pageIndex,
    });
}
/*渲染对象名称下拉框*/
function addObjectNameOption(url) {
    var dataList = [];
    var data = getData(url);
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    $.each(data.responseJSON.result, function (index, item) {
        dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
    });
    $('.slt_obj_name').children().remove();
    $('.slt_obj_name').append(dataList.toString());
}
/*渲染标签下拉框*/
function addTagNameOption() {
    var dataList = [];
    var data = getData('/ajax/tag/get/');
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    $.each(data.responseJSON.result, function (index, item) {
        dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
    });
    $('.slt_tag_name').append(dataList.toString());
}
/*渲染专业方向下拉框*/
function addCareerCategoryOption() {
    var dataList = [];
    var data = getData('/ajax/careerCatagory/get/');
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    $.each(data.responseJSON.result, function (index, item) {
        dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
    });
    $('.slt_careercatagory_name').append(dataList.toString());
}
/*----------------------------------------------------------END-----------------------------------------------------------*/

/*-------------------------------------------------------模态框初始化--------------------------------------------------------*/
function modalInputFieldInit(modalId) {
    $(modalId).children().find('.slt_careercatagory_name').val(0);
    $(modalId).children().find('.slt_tag_name').val(0);
    $(modalId).children().find('.slt_obj_type').val(0);
    $(modalId).children().find('.slt_obj_name').val(0);
}
function modalErrorLableInit(modalId) {
    $(modalId).children().find('.inputAreaError').css('color', '#000')
    $(modalId).children().find('.inputAreaError').children().remove();
}
/*-------------------------------------------------------END--------------------------------------------------------*/

/*-------------------------------------------------------表单验证--------------------------------------------------------*/
// 提交form表单时，检查有无数据不合法的错误
function formDataCommitValidate() {
    var result = {};
    result.code = 0;
    result.errorInfo = '';
    GOLBAL_ERROR = [];  //  初始化验证数据合法性的全局变量
    selectValidate('#slt_add_obj_type');  // 验证对象类型输入框
    selectValidate('#slt_add_obj_name');  // 验证对象名称输入框
    selectValidate('#slt_add_careercatagory_name');  // 验证专业方向名称输入框
    selectValidate('#slt_add_tag_name');  // 验证标签名称输入框

    $.each(GOLBAL_ERROR, function (index, items) {
        result.code = items.status + result.code;
        if (items.status == -1) {
            result.errorInfo = result.errorInfo + items.errorInfo + ' ';
        }
    });
    return result;
}
