/**
 * Created by zml on 2016/5/16.
 */
$(function () {
    /*------------------------------------------------弹出模态框--------------------------------------------------------*/
    //添加
    $(document).off('click', '#btn_addUserCenterAd').on('click', '#btn_addUserCenterAd', function () {
        modalInputFieldInit('#modal_addUserCenterAd');
        modalErrorLableInit('#modal_addUserCenterAd');
        $('#modal_addUserCenterAd').modal('show');
    });
    //删除
    $(document).off('click', '.btn_delUserCenterAd').on('click', '.btn_delUserCenterAd', function () {
        $('#delUserCenterAdMessage').text('确定要删除“' + $(this).parents().data('title') + '”个人中心广告吗？'); //删除提示信息
        selectDelRowId = $(this).parent().data('id');  //获取Id
        $('#modal_delUserCenterAd').modal('show');
    });
    //修改
    $(document).off('click', '.btn_editUserCenterAd').on('click', '.btn_editUserCenterAd', function () {
        modalErrorLableInit('#modal_editUserCenterAd');
        selectEditRowId = $(this).parent().data('id');
        var status = ($(this).parents('tr').children('.td_isActived').text() == '激活') ? 1 : 0;
        $('#file_edit_imgUrl').val('');
        $('.previewImg').attr('src', $(this).parents('tr').children('.td_imgUrl').children().attr('src'));
        $('#txt_edit_imgTitle').val($(this).parents('tr').children('.td_imgTitle').text());
        $('#slt_edit_isActived').val((status == 1) ? 1 : 0);
        $('#modal_editUserCenterAd').modal('show');
    });
    //查看
    $(document).off('click', '.btn_showUserCenterAd').on('click', '.btn_showUserCenterAd', function () {
        $('#lbl_imgUrl').attr('src', $(this).parents('tr').children('.td_imgUrl').children().attr('src'));
        $('#lbl_imgTitle').text($(this).parents('tr').children('.td_imgTitle').text());
        $('#lbl_isActived').text($(this).parents('tr').children('.td_isActived').text());
        $('#modal_showUserCenterAd').modal('show');
    });
    //查看放大图片
    $(document).off('click', '.td_imgUrl>img').on('click', '.td_imgUrl>img', function () {
        $('#showOriginImg').attr('src', $(this).attr('src'));
        $('#modal_showOriginImg').modal('show');
    });
    /*-------------------------------------------------------END--------------------------------------------------------*/
    /*------------------------------------------------模态框按钮单击事件------------------------------------------------*/
    //添加/-保存按钮
    $(document).off('click', '#btn_saveAddUserCenterAd').on('click', '#btn_saveAddUserCenterAd', function () {
        var commitData = new FormData($('#form_addUserCenterAd')[0]);
        commitData.append('img_url', $('#file_add_imgUrl')[0].files[0]);
        commitData.append('img_title', $('#txt_add_imgTitle').val());
        commitData.append('is_actived', $('#slt_add_isActived').val());
        var result = formDataCommitValidate('modal_addUserCenterAd');
        if (result.code == 0) {
            addOrUpdateData('/ajax/userCenterAd/create/', '/ajax/userCenterAd/list/', commitData, '#modal_addUserCenterAd');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //修改-保存按钮
    $(document).off('click', '#btn_saveEditUserCenterAd').on('click', '#btn_saveEditUserCenterAd', function () {
        var commitData = new FormData();
        var isUpdateImg = ($('.td_imgUrl').children().attr('src') == $('.previewImg').attr('src')) ? 1 : 0;
        // console.info('tableIMG:' + $('.td_imgUrl').children().attr('src') + ',previewImg:' + $('.previewImg').attr('src') + isUpdateImg)
        commitData.append('id', selectEditRowId);
        commitData.append('isUpdateImg', isUpdateImg);
        commitData.append('img_url', $('#file_edit_imgUrl')[0].files[0]);
        commitData.append('img_title', $('#txt_edit_imgTitle').val());
        commitData.append('is_actived', $('#slt_edit_isActived').val());
        var result = formDataCommitValidate('modal_editUserCenterAd');
        if (result.code == 0) {
            addOrUpdateData('/ajax/userCenterAd/update/', '/ajax/userCenterAd/list/', commitData, '#modal_editUserCenterAd');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //删除-确定按钮
    $(document).off('click', '#btn_ensureDelUserCenterAd').on('click', '#btn_ensureDelUserCenterAd', function () {
        deleteData('/ajax/userCenterAd/delete/', '/ajax/userCenterAd/list/', selectDelRowId, '#modal_delUserCenterAd');
    });
    /*-------------------------------------------------------END---------------------------------------------------------*/
    /*------------------------------------------------数据验证事件绑定---------------------------------------------------*/
    //图片标题验证
    $('.txt_imgTitle').off('blur').on('blur', function () {
        imgTitleValidate(this);
    });
    //图片上传验证
    $('.file_imgUrl').off('change').on('change', function () {
        console.info(JSON.stringify($('.file_imgUrl')[0].files[0]));
        $(this).parents('.modal-body').find('.previewImg').attr('src', window.URL.createObjectURL(
            $(this)[0].files[0]));  // 本地图片预览
        imgUploadValidate(this);
    });
});
/*------------------------------------------------把查询数据展示在表格中--------------------------------------------------*/
function showDataInTable(pageIndex, pageSize, data) {
    var dataList = [];
    var serialNumber = (pageIndex - 1) * pageSize;
    if (data.result.totalCounts == 0) {
        dataList.push('<tr><td colspan="5">查询到0条数据！</td></tr>');
    } else {
        $.each(data.result.data, function (index, item) {
            serialNumber += 1;
            var status = (item.img_isactived) ? '激活' : '未激活';
            dataList.push('<tr><td style="text-align: center">' + serialNumber + '</td>');
            dataList.push('<td class="td_imgUrl"><img src="' + item.img_url + '" height="80px;" width="80px;"/> </td>');
            dataList.push('<td class="td_imgTitle">' + item.img_title + '</td>');
            dataList.push('<td class="td_isActived" style="text-align: center">' + status + '</td>');
            dataList.push('<td data-id="' + item.id + '" data-title="' + item.img_title + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showUserCenterAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active btn_editUserCenterAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delUserCenterAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
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
/*----------------------------------------------------------END-----------------------------------------------------------*/

/*-------------------------------------------------------模态框初始化--------------------------------------------------------*/
function modalInputFieldInit(modalId) {
    $(modalId).children().find('.inputArea').val('');
    $(modalId).children().find('.previewImg').attr('src', '');
}
function modalErrorLableInit(modalId) {
    $(modalId).children().find('.inputAreaError').text('');
    $(modalId).children().find('.file_imgUrl').val('');
    $(modalId).children().find('.slt_isActived').val(0);
    $('.lbl_imgUrlError').text('');
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
    if (modalId == 'modal_editUserCenterAd') {
        imgUploadValidate('#file_edit_imgUrl');  // 验证上传图片控件
        imgTitleValidate('#txt_edit_imgTitle');  // 验证图片标题输入框
    } else {
        imgUploadValidate('#file_add_imgUrl');  // 验证上传图片控件
        imgTitleValidate('#txt_add_imgTitle');  // 验证图片标题输入框
    }

    $.each(GOLBAL_ERROR, function (index, items) {
        result.code = items.status + result.code;
        if (items.status == -1) {
            result.errorInfo = result.errorInfo + items.errorInfo + ' ';
        }
    });
    return result;
}