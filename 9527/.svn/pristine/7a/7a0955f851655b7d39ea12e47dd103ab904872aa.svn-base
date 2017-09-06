/**
 * Created by Administrator on 2016/5/18.
 */
$(function () {
    /*------------------------------------------------弹出模态框--------------------------------------------------------*/
    //添加
    $(document).off('click', '#btn_addCareerAd').on('click', '#btn_addCareerAd', function () {
        $('#modal_addCareerAd').modal('show');
        modalInputFieldInit('#modal_addCareerAd');
        modalErrorLableInit('#modal_addCareerAd');
    });
    //删除
    $(document).off('click', '.btn_delCareerAd').on('click', '.btn_delCareerAd', function () {
        $('#delCareerAdMessage').text('确定要删除“' + $(this).parents().data('title') + '”个人中心广告吗？'); //删除提示信息
        selectDelRowId = $(this).parent().data('id');  //获取Id
        $('#modal_delCareerAd').modal('show');
    });
    //修改
    $(document).off('click', '.btn_editCareerAd').on('click', '.btn_editCareerAd', function () {
        modalErrorLableInit('#modal_editCareerAd');
        selectEditRowId = $(this).parent().data('id');
        var data=getData('/ajax/careerAd/get/',selectEditRowId).responseJSON.result;
        $('#file_edit_imgUrl').val('');
        $('.previewImg').attr('src',data.img_url);
        $('#txt_edit_careerName').val(data.career_name);
        $('#txt_edit_imgTitle').val(data.img_title);
        $('#slt_edit_type').val(data.type);
        $('#slt_edit_isActived').val((data.is_actived)?1:0);
        $('#modal_editCareerAd').modal('show');
    });
    //查看
    $(document).off('click', '.btn_showCareerAd').on('click', '.btn_showCareerAd', function () {
        $('#lbl_imgUrl').attr('src', $(this).parents('tr').children('.td_imgUrl').children().attr('src'));
        $('#lbl_imgTitle').text($(this).parents('tr').children('.td_imgTitle').text());
        $('#lbl_isActived').text($(this).parents('tr').children('.td_isActived').text());
        $('#lbl_careerName').text($(this).parents('tr').children('.td_careerName').text());
        $('#lbl_type').text($(this).parents('tr').children('.td_type').text());
        $('#modal_showCareerAd').modal('show');
    });
    //查看放大图片
    $(document).off('click', '.td_imgUrl>img').on('click', '.td_imgUrl>img', function () {
        $('#showOriginImg').attr('src', $(this).attr('src'));
        $('#modal_showOriginImg').modal('show');
    });
    /*-------------------------------------------------------END--------------------------------------------------------*/
    /*------------------------------------------------模态框按钮单击事件------------------------------------------------*/
    //添加/-保存按钮
    $(document).off('click', '#btn_saveAddCareerAd').on('click', '#btn_saveAddCareerAd', function () {
        var commitData = new FormData($('#form_addCareerAd')[0]);
        // commitData.append('img_url', $('#file_add_imgUrl')[0].files[0]);
        // commitData.append('img_title', $('#txt_add_imgTitle').val());
        // commitData.append('career_name',$('#txt_add_careerName').val());
        // commitData.append('is_actived', ($('#slt_add_isActived').val() == '激活') ? 1 : 0);
        // commitData.append('type',($('#slt_add_type').val() == '课程') ? 'COURSE' : 'ARTICLE');
        var result = formDataCommitValidate('modal_addCareerAd');
        if (result.code == 0) {
            addOrUpdateData('/ajax/careerAd/create/', '/ajax/careerAd/list/', commitData, '#modal_addCareerAd');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //修改-保存按钮
    $(document).off('click', '#btn_saveEditCareerAd').on('click', '#btn_saveEditCareerAd', function () {
        var commitData = new FormData($('#form_editCareerAd')[0]);
        var isUpdateImg = ($('#file_edit_imgUrl').val()) ? 1 : 0;
        commitData.append('id', selectEditRowId);
        commitData.append('career_id',$('#slt_add_careerName').val());
        commitData.append('type',$('#slt_edit_type').val());
        //commitData.append('isUpdateImg', isUpdateImg);
        //commitData.append('img_url', $('#file_edit_imgUrl')[0].files[0]);
        //commitData.append('img_title', $('#txt_edit_imgTitle').val());
        //commitData.append('is_actived', ($('#slt_edit_isActived').val() == '激活') ? 1 : 0);
        var result = formDataCommitValidate('modal_editCareerAd');
        if (result.code == 0) {
            addOrUpdateData('/ajax/careerAd/update/', '/ajax/careerAd/list/', commitData, '#modal_editCareerAd');
        }
        else {
            warningPrompt(result.errorInfo);
        }
    });
    //删除-确定按钮
    $(document).off('click', '#btn_ensureDelCareerAd').on('click', '#btn_ensureDelCareerAd', function () {
        deleteData('/ajax/careerAd/delete/', '/ajax/careerAd/list/', selectDelRowId, '#modal_delCareerAd');
    });
    /*-------------------------------------------------------END---------------------------------------------------------*/
    /*------------------------------------------------数据验证事件绑定---------------------------------------------------*/
    //图片标题验证
    $('.txt_imgTitle').off('blur').on('blur', function () {
        imgTitleValidate(this);
    });
    //图片上传验证
    $('.file_imgUrl').off('change').on('change', function () {
        $(this).parents('.modal-body').find('.previewImg').attr('src', window.URL.createObjectURL($(this)[0].files[0]));
        imgUploadValidate(this);
    });
    //职业名称验证
    $('.txt_careerName').off('blur').on('blur', function () {
        careerNameValidate(this);
    });
    addCareerNameOption();  // 职业广告下拉列表框填充数据
    $(document).off('dblclick','.td_careerName').on('dblclick','.td_careerName', function () {
        var id=$(this).data('id')
        var data=("/ajax/careerCourse/get/",id).responseJSON.result;
        
    });
});
/*------------------------------------------------把查询数据渲染到页面--------------------------------------------------*/
/*渲染表格数据*/
function showDataInTable(pageIndex, pageSize, data) {
    var dataList = [];
    var serialNumber = (pageIndex - 1) * pageSize;
    // alert(JSON.stringify(data));
    // var careerName = getData('/ajax/careerCourse/get/').responseJSON.result;
    // alert(JSON.stringify(careerName));
    if (data.result.totalCounts == 0) {
        dataList.push('<tr><td colspan="7">查询到0条数据！</td></tr>');
    } else {
        $.each(data.result.data, function (index, item) {
            serialNumber += 1;
            var status = (item.is_actived) ? '激活' : '未激活';
            var type = (item.type == 'ARTICLE') ? '文章' : '课程';
            dataList.push('<tr><td style="text-align: center">' + serialNumber + '</td>');
            dataList.push('<td class="td_careerName" data-id="' + item.career_id + '"> ' + item.career_name + '</td>');
            dataList.push('<td class="td_imgTitle">' + item.img_title + '</td>');
            dataList.push('<td class="td_imgUrl"><img src="' + item.img_url + '" height="80px;" width="80px;"/> </td>');
            dataList.push('<td class="td_isActived" style="text-align: center">' + status + '</td>');
            dataList.push('<td class="td_type" style="text-align: center">' + type + '</td>');
            dataList.push('<td data-id="' + item.id + '" data-title="' + item.img_title + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showCareerAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active btn_editCareerAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delCareerAd" style="margin-right:3px;" role="button"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
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
function addCareerNameOption() {
    var dataList = [];
    var data = getData('/ajax/careerCourse/get/');
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    $.each(data.responseJSON.result, function (index, item) {
        dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
    });
    $('.slt_careerName').children().remove();
    $('.slt_careerName').append(dataList.toString());
}
/*----------------------------------------------------------END-----------------------------------------------------------*/

/*-------------------------------------------------------模态框初始化-----------------------------------------------------*/
function modalInputFieldInit(modalId) {
    $(modalId).children().find('.inputArea').val('');
}
function modalErrorLableInit(modalId) {
    $(modalId).children().find('.inputAreaError').text('');
    $(modalId).children().find('.file_imgUrl').val('');
    $(modalId).children().find('.slt_isActived').val(0);
    $(modalId).children().find('.slt_careerName').val(1);
    $(modalId).children().find('.slt_type').val('COURSE');
    $('.lbl_imgUrlError').text('');
    $(modalId).children().find('.previewImg').attr('src','');
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
    if (modalId == 'modal_editCareerAd') {
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
/*-------------------------------------------------------模态框初始化-----------------------------------------------------*/
