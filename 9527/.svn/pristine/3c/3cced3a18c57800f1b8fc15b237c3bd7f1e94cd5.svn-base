/**
 * Created by Administrator on 2016/5/20.
 */
/**
 * Created by Administrator on 2016/5/18.
 */
$(function () {
    /*------------------------------------------------弹出模态框--------------------------------------------------------*/
    //添加
    $(document).off('click', '#btn_addObjSEO').on('click', '#btn_addObjSEO', function () {
        $('#modal_addObjSEO').modal('show');
        modalInputFieldInit('#modal_addObjSEO');
        modalErrorLableInit('#modal_addObjSEO');
    });
    //删除
    $(document).off('click', '.btn_delObjSEO').on('click', '.btn_delObjSEO', function () {
        $('#delObjSEOMessage').text('确定要删除“' + $(this).parents().data('title') + '”个人中心广告吗？'); //删除提示信息
        selectDelRowId = $(this).parent().data('id');  //获取Id
        $('#modal_delObjSEO').modal('show');
    });
    //修改
    $(document).off('click', '.btn_editObjSEO').on('click', '.btn_editObjSEO', function () {
        modalErrorLableInit('#modal_editObjSEO');
        selectEditRowId = $(this).parent().data('id');
        var data=getData('/ajax/objSEO/get/',selectEditRowId).responseJSON.result;
        alert(JSON.stringify(data));
        $('#slt_edit_objectName').val(data.obj_name);
        $('#txt_edit_seoTitle').val(data.seo_title);
        $('#txt_edit_seoKeyword').val(data.seo_keywords);
        $('#txtA_edit_seoDescription').val(data.seo_description);
        $('#slt_edit_objectType').val(data.obj_type);
        $('#modal_editObjSEO').modal('show');
    });
    //查看
    $(document).off('click', '.btn_showObjSEO').on('click', '.btn_showObjSEO', function () {
        $('#lbl_objectName').text($(this).parents('tr').children('.td_objectName').text());
        $('#lbl_seoTitle').text($(this).parents('tr').children('.td_seoTitle').text());
        $('#lbl_seoKeyword').text($(this).parents('tr').children('.td_seoKeyword').text());
        $('#lbl_seoDescription').text($(this).parents('tr').children('.td_seoDescription').text());
        $('#lbl_objectType').text($(this).parents('tr').children('.td_objectType').text());
        $('#modal_showObjSEO').modal('show');
    });
    /*-------------------------------------------------------END--------------------------------------------------------*/
    /*------------------------------------------------模态框按钮单击事件------------------------------------------------*/
    //添加/-保存按钮
    $(document).off('click', '#btn_saveAddObjSEO').on('click', '#btn_saveAddObjSEO', function () {
        var commitData = new FormData($('#form_addObjSEO')[0]);
        // commitData.append('img_url', $('#file_add_imgUrl')[0].files[0]);
        // commitData.append('img_title', $('#txt_add_imgTitle').val());
        // commitData.append('career_name',$('#txt_add_careerName').val());
        // commitData.append('is_actived', ($('#slt_add_isActived').val() == '激活') ? 1 : 0);
        // commitData.append('type',($('#slt_add_type').val() == '课程') ? 'COURSE' : 'ARTICLE')
        var result = formDataCommitValidate('modal_addObjSEO');
        if (result.code == 0) {
            addOrUpdateData('/ajax/objSEO/create/', '/ajax/objSEO/list/', commitData, '#modal_addObjSEO');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //修改-保存按钮
    $(document).off('click', '#btn_saveEditObjSEO').on('click', '#btn_saveEditObjSEO', function () {
        var commitData = new FormData($('#form_editObjSEO')[0]);
        var isUpdateImg = ($('#file_edit_imgUrl').val()) ? 1 : 0;
        commitData.append('id', selectEditRowId);
        commitData.append('obj_type', $('#slt_edit_objectType').val());
        commitData.append('obj_id',$('#slt_edit_objectName').val());
        var result = formDataCommitValidate('modal_editObjSEO');
        if (result.code == 0) {
            addOrUpdateData('/ajax/objSEO/update/', '/ajax/objSEO/list/', commitData, '#modal_editObjSEO');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //删除-确定按钮
    $(document).off('click', '#btn_ensureDelObjSEO').on('click', '#btn_ensureDelObjSEO', function () {
        deleteData('/ajax/objSEO/delete/', '/ajax/objSEO/list/', selectDelRowId, '#modal_delObjSEO');
    });
    /*-------------------------------------------------------END---------------------------------------------------------*/
    /*------------------------------------------------数据验证事件绑定---------------------------------------------------*/
    //搜索标题验证
    $('.txt_seoTitle').off('blur').on('blur', function () {
        seoTitleValidate(this);
    });
    //当obj_type改变时，重新填充obj_name中的值
    $('#slt_add_objectType').off('change').on('change',function(){
        var obj_type=$(this).val();
        var typeTableRelation={'ARTICLE':'/ajax/articleType/get/','COURSE':'/ajax/careerCourse/get/'}
        if(obj_type==0){
            $('#slt_add_objectName').val(0);
        }else {
            addObjectNameOption(typeTableRelation[obj_type]);
        }
    });
    // addobjectNameOption();  // 对象名称下拉列表框填充数据
});
/*------------------------------------------------把查询数据渲染到页面--------------------------------------------------*/
/*渲染表格数据*/
function showDataInTable(pageIndex, pageSize, data) {
    var dataList = [];
    var serialNumber = (pageIndex - 1) * pageSize;
    var objectType = {'ARTICLE': '文章', 'TEACHER': '老师', 'COURSE': '课程', 'LESSON': '视频'};
    if (data.result.totalCounts == 0) {
        dataList.push('<label>查询到0条数据！</label>');
    } else {
        $.each(data.result.data, function (index, item) {
            var objectTypeKey = item.obj_type;
            serialNumber += 1;
            dataList.push('<tr><td style="text-align: center">' + serialNumber + '</td>');
            dataList.push('<td class="td_objectType" data-name="' + item.obj_type + '">' + objectType[objectTypeKey] + '</td>');
            dataList.push('<td class="td_objectName" data-id="' + item.object_id + '"> ' + item.objName + '</td>');
            dataList.push('<td class="td_seoTitle">' + item.seo_title + '</td>');
            dataList.push('<td class="td_seoKeyword">' + item.seo_keywords + '</td>');
            dataList.push('<td class="td_seoDescription">' + item.seo_description + '</td>');
            dataList.push('<td data-id="' + item.id + '" data-title="' + item.img_title + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showObjSEO" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active btn_editObjSEO" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delObjSEO" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
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
/*渲染职业名称下拉框*/
function addObjectNameOption(url) {
    var dataList = [];
    var data = getData(url);
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    $.each(data.responseJSON.result, function (index, item) {
        dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
    });
    $('#slt_add_objectName').children().remove();
    $('#slt_add_objectName').append(dataList.toString());
}
/*----------------------------------------------------------END-----------------------------------------------------------*/

/*-------------------------------------------------------模态框初始化--------------------------------------------------------*/
function modalInputFieldInit(modalId) {
    $(modalId).children().find('.inputArea').val('');
}
function modalErrorLableInit(modalId) {
    $(modalId).children().find('.inputAreaError').text('');
    $(modalId).children().find('.slt_objectName').val(0);
    $(modalId).children().find('.slt_objectType').val(0);
    $(modalId).children().find('.inputAreaError').css('color', '#000')
    $(modalId).children().find('.inputAreaError').children().remove();
}
/*-------------------------------------------------------END--------------------------------------------------------*/
// 提交form表单时，检查有无数据不合法的错误
function formDataCommitValidate(modalId) {
    var result = {};
    result.code = 0;
    result.errorInfo = '';
    GOLBAL_ERROR = [];  //  初始化验证数据合法性的全局变量
    if (modalId == 'modal_editObjSEO') {
        seoTitleValidate('#txt_edit_seoTitle');  // 验证搜索标题控件
    } else {
        seoTitleValidate('#txt_add_seoTitle');  // 验证搜索标题控件
    }
    selectValidate('#slt_add_objectType');  // 验证对象类型输入框
    selectValidate('#slt_add_objectName');  // 验证对象名称输入框

    $.each(GOLBAL_ERROR, function (index, items) {
        result.code = items.status + result.code;
        if (items.status == -1) {
            result.errorInfo = result.errorInfo + items.errorInfo + ' ';
        }
    });
    return result;
}