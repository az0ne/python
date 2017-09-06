$(document).ready(function () {
    //**增**
    //**点击功能区添加<专业方向信息>的按钮，弹出添加<专业方向信息>模态框
    $(document).off('click', '#btn_addNewCareerCategory').on('click', '#btn_addNewCareerCategory', function () {
        modalInputFieldInit('#modal_addCareerCategory');
        modalErrorLableInit('#modal_addCareerCategory');
        $('#txt_careerCategory').val("");
        $('#modal_addCareerCategory').modal('show');
    });
    //单击添加<专业方向信息模态框>中的确定按钮，调用ajax添加<专业方向信息>
    $(document).off('click', '#btn_saveAddCareerCategory').on('click', '#btn_saveAddCareerCategory', function () {
        var commitData = new FormData($('#form_addCareerCategory')[0]);
        var result = formDataCommitValidate('#modal_addCareerCategory');
        if (result.code == 0) {
            addOrUpdateData('/ajax/careerCatagory/create/', '/ajax/careerCatagory/list/', commitData, '#modal_addCareerCategory');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });

    //**删**
    //**点击<专业方向信息>中的删除按钮，弹出删除警告模态框
    $(document).off('click', '.btn_delCareerCategory').on('click', '.btn_delCareerCategory', function () {
        delCareerCategoryId = $(this).parents().data('id');
        $('#delCareerCategoryMessage').text('确定要删除“' + $(this).parents().data('name') + '”专业方向吗？');
        $('#modal_delCareerCategory').modal('show');
    });
    //单击<警告模态框>中的确定按钮，调用ajax删除<专业方向信息>
    $(document).off('click', '#btn_ensureDelCareerCategory').on('click', '#btn_ensureDelCareerCategory', function () {
        deleteData('/ajax/careerCatagory/delete/', '/ajax/careerCatagory/list/', delCareerCategoryId, '#modal_delCareerCategory');
    });
    //**改**
    //**点击<专业方向信息>中的编辑按钮，弹出修改专业方向信息模态框
    $(document).off('click', '.btn_editCareerCategory').on('click', '.btn_editCareerCategory', function updateCourse() {
        modalErrorLableInit('#modal_editCareerCategory');
        editCareerCategoryId = $(this).parents().data('id');
        $('#txt_editCareerCategoryName').val($(this).parents().data('name'));
        $('#modal_editCareerCategory').modal('show');
    });
    //单击修改<专业方向信息模态框>中的确定按钮，调用ajax更新<专业方向信息>
    $(document).off('click', '#btn_saveEditCareerCategory').on('click', '#btn_saveEditCareerCategory', function () {
        var commitData = new FormData($('#form_editCareerCategory')[0]);
        commitData.append('id', editCareerCategoryId);
        var result = formDataCommitValidate('#modal_editCareerCategory');
        if (result.code == 0) {
            addOrUpdateData('/ajax/careerCatagory/update/', '/ajax/careerCatagory/list/', commitData, '#modal_editCareerCategory');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });

    //**查**
    //**点击查看<专业方向信息>的按钮，弹出查看<专业方向信息>模态框
    $(document).off('click', '.btn_showCareerCategory').on('click', '.btn_showCareerCategory', function () {
        $('#modal_showCareerCategory').modal('show');
        $('#lbl_careerCategoryName').text($(this).parents().data('name'));
    });

    //搜索按钮单击事件
    $(document).off('click', '#btn_search').on('click', '#btn_search', function () {
        // var searchKeyWord=($('#txt_search').val().length)? $('#txt_search').val() :null;  //三目运算符
        var searchKeyWord = $('#txt_search').val();
        selectData('/ajax/careerCatagory/list/', 1, 8, searchKeyWord);
    });
    $(document).off('keydown', '#txt_search').on('keydown', '#txt_search', function () {
        if (event.keyCode == '13') {
            $('#btn_search').click();
        }
    });
});

/*------------------------------------------------把查询数据展示在表格中--------------------------------------------------*/
//获取专业方向信息列表
function showDataInTable(pageIndex, pageSize, data) {
    var dataList = [];
    var serialNumber = (pageIndex - 1) * pageSize;
    if (data.result.totalCounts == 0) {
        dataList.push('<label>查询到0条数据！</label>');
    } else {
        $.each(data.result.data, function (index, item) {
            serialNumber += 1;
            dataList.push('<tr><td style="text-align: center">' + serialNumber + '</td>');
            dataList.push('<td class="name">' + item.name + '</td>');
            dataList.push('<td data-id="' + item.id + '" data-name="' + item.name + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showCareerCategory" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active btn_editCareerCategory" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delCareerCategory" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
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
/*------------------------------------------------数据验证事件绑定---------------------------------------------------*/
//图片标题验证
$('.txt_careerCategoryName').off('blur').on('blur', function () {
    textBoxValidate('#' + $(this).attr('id'));
});
/*-------------------------------------------------------模态框初始化--------------------------------------------------------*/
function modalInputFieldInit(modalId) {
    $(modalId).children().find('.inputArea').val('');
}
function modalErrorLableInit(modalId) {
    $(modalId).children().find('.inputAreaError').text('');
    $(modalId).children().find('.inputAreaError').css('color', '#000')
    $(modalId).children().find('.inputAreaError').children().remove();
}
/*-------------------------------------------------------表单验证--------------------------------------------------------*/
// 提交form表单时，检查有无数据不合法的错误
function formDataCommitValidate(modalId) {
    var result = {};
    result.code = 0;
    result.errorInfo = '';
    GOLBAL_ERROR = [];  //  初始化验证数据合法性的全局变量
    console.info($(modalId).find('.txt_careerCategoryName').attr('id'));
    textBoxValidate('#' + $(modalId).find('.txt_careerCategoryName').attr('id'));  // 验证职业方向输入框

    $.each(GOLBAL_ERROR, function (index, items) {
        result.code = items.status + result.code;
        if (items.status == -1) {
            result.errorInfo = result.errorInfo + items.errorInfo + ' ';
        }
    });
    return result;
}




