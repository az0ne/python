/**
 * Created by zml on 2016/5/17.
 */
/*--------------------------------------------------事件绑定----------------------------------------------------------*/
$(function () {

});
/*--------------------------------------------------方法体--------------------------------------------------------------*/
var GOLBAL_ERROR = [];  // 全局错误变量，用于点击保存添加或修改，验证数据是否全部合法

/*--------------------------------------------------错误信息-------------------------------------------------------------*/
var IMGURL_ERROR = {};
IMGURL_ERROR.EMPTY = '上传图片不能为空！';
IMGURL_ERROR.FORMAT = '上传文件格式不合法！';
IMGURL_ERROR.SIZE = "上传图片尺寸不合法！";
IMGURL_ERROR.FILESIZE = "上传文件过大，请重新选择！";
var IMGTITLE_ERROR = {};
IMGTITLE_ERROR.EMPTY = '图片标题不能为空！';
IMGTITLE_ERROR.MAXLENGTH = '图片标题请小于255个字符！';
var BGCOLOR_ERROR = {};
BGCOLOR_ERROR.EMPTY = '背景颜色不能为空！';
BGCOLOR_ERROR.FORMAT = '格式不合法！请重新输入，如：#57af47';
var SE0TITLE_ERROR = {};
SE0TITLE_ERROR.EMPTY = '搜索标题不能为空！';
SE0TITLE_ERROR.MAXLENGTH = '搜索标题请小于255个字符！';
var CAREERCATEGORY_ERROR = {};
CAREERCATEGORY_ERROR.EMPTY = '职业方向名称不能为空！';
CAREERCATEGORY_ERROR.MAXLENGTH = '职业方向名称请小于255个字符！';
var ISACTIVED_ERROR = {};
ISACTIVED_ERROR.EMPTY = '状态不能为空！';
var SHOWCASE_ERROR = {};
SHOWCASE_ERROR.EMPTY = '展示位置不能为空！';
var OBJECTTYPE_ERROR = {};
OBJECTTYPE_ERROR.EMPTY = '对象类型不能为空！';
var OBJECTNAME_ERROR = {};
OBJECTNAME_ERROR.EMPTY = '对象名称不能为空！';
var CAREERCATEGORYNAME_ERROR = {};
CAREERCATEGORYNAME_ERROR.EMPTY = '专业方向名称不能为空！';
CAREERCATEGORYNAME_ERROR.MAXLENGTH = '专业方向名称请小于255个字符！';
var TAGNAME_ERROR = {};
TAGNAME_ERROR.EMPTY = '标签名称不能为空！';
var BANNERTITLE_ERROR = {};
BANNERTITLE_ERROR.EMPTY = '图片描述不能为空！';
BANNERTITLE_ERROR.MAXLENGTH = '图片描述请小于255个字符！';
var URL_ERROR = {};
URL_ERROR.FORMAT = '非网址格式，请重新输入！';
URL_ERROR.EMPTY = '链接不能为空！';
URL_ERROR.MAXLENGTH = '链接请小于255个字符！';
var INDEX_ERROR = {};
INDEX_ERROR.FORMAT = '非正整数格式，请重新输入！';
INDEX_ERROR.EMPTY = '序号不能为空！';
INDEX_ERROR.MAXLENGTH = '序号必须小于11！';
var CAREERNAME_ERROR = {};
CAREERNAME_ERROR.EMPTY = '职业名称不能为空！';
CAREERNAME_ERROR.MAXLENGTH = '职业名称必须小于255！';
var ENTERPRISE_ERROR = {};
ENTERPRISE_ERROR.EMPTY = '企业名称不能为空！';
ENTERPRISE_ERROR.MAXLENGTH = '企业名称必须小于50个字符！';
var DUTY_ERROR = {};
DUTY_ERROR.EMPTY = '职位名称不能为空！';
DUTY_ERROR.MAXLENGTH = '职位名称必须小于50个字符！';
var TEACHERNAME_ERROR = {};
TEACHERNAME_ERROR.EMPTY = '教师姓名不能为空！';
TEACHERNAME_ERROR.MAXLENGTH = '教师姓名不能超过50个字符！';
var TEACHERTITLE_ERROR = {};
TEACHERTITLE_ERROR.EMPTY = '教师头衔不能为空！';
TEACHERTITLE_ERROR.MAXLENGTH = '教师头衔不能超过50个字符！';
var TEACHERINFO_ERROR = {};
TEACHERINFO_ERROR.EMPTY = '教师介绍信息不能为空！';
TEACHERINFO_ERROR.MAXLENGTH = '教师介绍信息不能超过200个字符！';
var FILEUPLOAD_ERROR = {};
FILEUPLOAD_ERROR.EMPTY = '视频地址不能为空！';
FILEUPLOAD_ERROR.MAXLENGTH = '视频地址不能超过500个字符！';
FILEUPLOAD_ERROR.FORMAT = '视频地址格式不正确！';
var STORYNAME_ERROR = {};
STORYNAME_ERROR.EMPTY = '学员成功故事姓名不能为空！';
STORYNAME_ERROR.MAXLENGTH = '学员成功故事姓名不能超过50个字符！';
var STORYTITLE_ERROR = {};
STORYTITLE_ERROR.EMPTY = '学员成功故事职位不能为空！';
STORYTITLE_ERROR.MAXLENGTH = '学员成功故事职位不能超过50个字符';
var STORYINFO_ERROR = {};
STORYINFO_ERROR.EMPTY = '学员成功故事描述不能为空！';
STORYINFO_ERROR.MAXLENGTH = '学员成功故事描述不能超过200个字符！';
var STUDENTCOUNT_ERROR = {};
STUDENTCOUNT_ERROR.FORMAT = '非正整数格式，请重新输入！';
STUDENTCOUNT_ERROR.EMPTY = '毕业学员数不能为空！';
var SHORTINFO_ERROR = {};
SHORTINFO_ERROR.EMPTY = '一句话介绍不能为空！';
SHORTINFO_ERROR.MINLENGTH = '一句话介绍不能小于60个字符！';
SHORTINFO_ERROR.MAXLENGTH = '一句话介绍不能超过70个字符！';
var INFO_ERROR = {};
INFO_ERROR.EMPTY = '详细介绍不能为空！';
INFO_ERROR.MINLENGTH = '详细介绍不能超过90个字符！';
INFO_ERROR.MAXLENGTH = '详细介绍不能超过100个字符！';
var TEACHERID_ERROR = {};
TEACHERID_ERROR.EMPTY = '教师ID不能为空或0！';
TEACHERID_ERROR.FORMAT = '非正整数格式，请重新输入！';
TEACHERID_ERROR.MAXLENGTH = '教师ID不能超过11个字符！';
var COMMENT_ERROR = {};
COMMENT_ERROR.EMPTY = '评论不能为空！';
COMMENT_ERROR.MAXLENGTH = '评论不能超过100000个字符！';
var USERID_ERROR = {};
USERID_ERROR.EMPTY = '用户ID不能为空或0！';
USERID_ERROR.FORMAT = '非正整数格式，请重新输入！';
USERID_ERROR.MAXLENGTH = '用户ID不能超过11个字符！';
var NICKNAME_ERROR = {};
NICKNAME_ERROR.EMPTY = '用户昵称不能为空！';
NICKNAME_ERROR.MAXLENGTH = '用户昵称不能超过50个字符！';
var PARENTID_ERROR = {};
PARENTID_ERROR.EMPTY = '父级评论ID不能为空！';
PARENTID_ERROR.MAXLENGTH = '父级评论ID不能超过11个字符！';
var CAREEROUTLINE_ERROR = {};
CAREEROUTLINE_ERROR.EMPTY = '课程大纲不能为空！';
CAREEROUTLINE_ERROR.MINLENGTH = '课程大纲不能超过15个字符！';
CAREEROUTLINE_ERROR.MAXLENGTH = '课程大纲不能超过25个字符！';
var CAREERNAME_ERROR1 = {};
CAREERNAME_ERROR1.EMPTY = '课程名称不能为空！';
CAREERNAME_ERROR1.MAXLENGTH = '课程名称不能超过50个字符！';
var CAREERID_ERROR = {};
CAREERID_ERROR.EMPTY = '课程ID不能为空或0！';
CAREERID_ERROR.MAXLENGTH = '课程ID不能超过11个字符！';
var DISCUSSID_ERROR = {};
DISCUSSID_ERROR.EMPTY = '评论ID不能为空或0！';
DISCUSSID_ERROR.FORMAT = '非整数格式，请重新输入！';
DISCUSSID_ERROR.MAXLENGTH = '评论ID不能超过11个字符！';
var REASON_ERROR = {};
REASON_ERROR.EMPTY = '原因不能为空！';
REASON_ERROR.MINLENGTH = '原因不能超过30个字符！';
REASON_ERROR.MAXLENGTH = '原因不能超过40个字符！';
var POSITIONTYPE_ERROR = {};
POSITIONTYPE_ERROR.EMPTY = '出现位置不能为空！';
var CODEURL_ERROR = {};
CODEURL_ERROR.EMPTY = '下载链接不能为空！';
CODEURL_ERROR.FORMAT = 'URL地址不合法，请重新输入！';
CODEURL_ERROR.MAXLENGTH = '下载链接不能超过200个字符！';
var TITLE_ERROR = {};
TITLE_ERROR.EMPTY = '标题不能为空！';
TITLE_ERROR.MAXLENGTH = '标题不能超过50个字符！';
var ARTICLEURL_ERROR = {};
ARTICLEURL_ERROR.EMPTY = '文章链接不能为空！';
ARTICLEURL_ERROR.FORMAT = '文章链接地址不合法，请重新输入！';
ARTICLEURL_ERROR.MAXLENGTH = '文章链接地址不能超过200个字符！';
var ARTICLETITLE_ERROR = {};
ARTICLETITLE_ERROR.EMPTY = '文章标题不能为空！';
ARTICLETITLE_ERROR.MAXLENGTH = '文章标题不能超过50个字符！';
var TASKID_ERROR = {};
TASKID_ERROR.EMPTY = '任务ID不能为空或0！';
TASKID_ERROR.FORMAT = '非正整数格式，请重新输入！';
TASKID_ERROR.MAXLENGTH = '任务ID不能超过11个字符！';
var ARTICLETYPENAME_ERROR = {};
ARTICLETYPENAME_ERROR.EMPTY = '文章类型名称不能为空！';
ARTICLETYPENAME_ERROR.MAXLENGTH = '文章类型名称不能超过50个字符！';
var ARTICLETYPESHORTNAME_ERROR = {};
ARTICLETYPESHORTNAME_ERROR.EMPTY = '文章类型简称不能为空！';
ARTICLETYPESHORTNAME_ERROR.MAXLENGTH = '文章类型简称不能超过50个字符！';
var ARTICLETYPEID_ERROR = {};
ARTICLETYPEID_ERROR.EMPTY = '文章类型ID不能为空！';
ARTICLETYPEID_ERROR.FORMAT = '非正整数格式，请重新输入！';
ARTICLETYPEID_ERROR.MAXLENGTH = '文章类型ID不能超过11个字符！';
var HOMEPAGEINDEX_ERROR = {};
HOMEPAGEINDEX_ERROR.FORMAT = '非正整数格式，请重新输入！';
HOMEPAGEINDEX_ERROR.EMPTY = '首页文章序号不能为空！';
HOMEPAGEINDEX_ERROR.MAXLENGTH = '首页文章序号不能超过11个字符！';
var VNO_ERROR = {};
VNO_ERROR.EMPTY = '版本号不能为空！';
VNO_ERROR.MAXLENGTH = '版本号不能超过50个字符！';
var SIZE_ERROR = {};
SIZE_ERROR.EMPTY = '文件大小不能为空！'
SIZE_ERROR.MAXLENGTH = '文件大小不能超过11个字符！';
var VERSIONDESC_ERROR ={};
VERSIONDESC_ERROR.EMPTY = '版本介绍不能为空！';
VERSIONDESC_ERROR.MAXLENGTH = '文件大小不能超过200个字符！';

/*------------------------------------------绑定错误信息到验证框-------------------------------------------------------*/
var validate = {
    '#txt_addCareerCategoryName': CAREERCATEGORY_ERROR,
    '#txt_editCareerCategoryName': CAREERCATEGORY_ERROR,
    '#slt_add_obj_type': OBJECTTYPE_ERROR,
    '#slt_add_obj_name': OBJECTNAME_ERROR,
    '.txt_careerCatagoryName': CAREERCATEGORYNAME_ERROR,
    '#slt_add_careercatagory_name': CAREERCATEGORYNAME_ERROR,
    '#slt_add_tag_name': TAGNAME_ERROR,
    '.txt_imageTitle': BANNERTITLE_ERROR,
    '.file_imageUrl': IMGURL_ERROR,
    '#txt_add_url': URL_ERROR,
    '#txt_add_index': INDEX_ERROR,
    '.slt_isActived': ISACTIVED_ERROR,
    '#show_case': SHOWCASE_ERROR,
    '.txt_bgcolor': BGCOLOR_ERROR,
    '.slt_type': OBJECTTYPE_ERROR,
    '.slt_careerName': CAREERNAME_ERROR,
    '.txt_seoTitle': SE0TITLE_ERROR,
    '.slt_objectName': OBJECTNAME_ERROR,
    '.txt_enterpriseName': ENTERPRISE_ERROR,
    '.txt_dutyName': DUTY_ERROR,
    '.txt_teacherName': TEACHERNAME_ERROR,
    '.txt_teacherTitle': TEACHERTITLE_ERROR,
    '.txt_teacherInfo': TEACHERINFO_ERROR,
    '.file_videoUrl': FILEUPLOAD_ERROR,
    '.txt_storyName': STORYNAME_ERROR,
    '.txt_storyTitle': STORYTITLE_ERROR,
    '.txt_storyInfo': STORYINFO_ERROR,
    '.txt_studentCount': STUDENTCOUNT_ERROR,
    '.txt_shortInfo': SHORTINFO_ERROR,
    '.txt_info': INFO_ERROR,
    '.txt_teacherId': TEACHERID_ERROR,
    '.txt_comment': COMMENT_ERROR,
    '.txt_discussUserId': USERID_ERROR,
    '.txt_nickName': NICKNAME_ERROR,
    '.txt_parentId': PARENTID_ERROR,
    '.txt_careerOutline': CAREEROUTLINE_ERROR,
    '.txt_careerName': CAREERNAME_ERROR1,
    '.txt_careerId': CAREERID_ERROR,
    '.txt_discussId1': DISCUSSID_ERROR,
    '.txt_discussId2': DISCUSSID_ERROR,
    '.txt_discussId3': DISCUSSID_ERROR,
    '.txt_reason': REASON_ERROR,
    '.txt_index': INDEX_ERROR,
    '.slt_positionType': POSITIONTYPE_ERROR,
    '.txt_codeUrl': CODEURL_ERROR,
    '.txt_title': TITLE_ERROR,
    '.txt_articleUrl': ARTICLEURL_ERROR,
    '.txt_articleTitle': ARTICLETITLE_ERROR,
    '#file_imageUrl1': IMGURL_ERROR,
    '#file_imageUrl2': IMGURL_ERROR,
    '#file_imageUrl3': IMGURL_ERROR,
    '.txt_taskId': TASKID_ERROR,
    '.txt_articleTypeName': ARTICLETYPENAME_ERROR,
    '.txt_shortName': ARTICLETYPESHORTNAME_ERROR,
    '.txt_articleTypeId': ARTICLETYPEID_ERROR,
    '.txt_homepageIndex': HOMEPAGEINDEX_ERROR,
    '.txt_vno': VNO_ERROR,
    '.txt_size': SIZE_ERROR,
    '.txt_desc': VERSIONDESC_ERROR,
    '.txt_url': URL_ERROR,
};
/* ----------------------------------------------------验证背景颜色文本框---------------------------------------------- */
function colorValidate(validateField) {
    var RegUrl = new RegExp();
    RegUrl.compile("#[0-9a-fA-F]{6}$");
    var validateValue = $.trim($(validateField).val());
    var validateError = {};
    if (!RegUrl.test(validateValue) && validateValue.length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].FORMAT);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].FORMAT; // 暂存具体的错误信息
    }
    else if (validateValue.length == 0) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
}
/* ----------------------------------------------------------验证数字文本框-------------------------------------------- */
function numValidate(validateField, size) {
    var length = size ? size : 11;
    var regNum = /^\d+$/;  // 0+正整数正则表达式
    var validateValue = $.trim($(validateField).val());
    var validateError = {};

    if (!regNum.test(validateValue) && validateValue.length > 0) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].FORMAT);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].FORMAT; // 暂存具体的错误信息
    }
    else if (validateValue.length == 0) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息

    }
    else if (validateValue.length > length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MAXLENGTH);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].MAXLENGTH; // 暂存具体的错误信息
    }
    else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
    return validateError.status;
}
/* ----------------------------------------------------------验证非零数字文本框-------------------------------------------- */
function noZeroNumValidate(validateField, size) {
    var length = size ? size : 11;
    var regNoZeroNum = new RegExp();
    regNoZeroNum.compile("^[0-9]*[1-9][0-9]*$");  // 正整数正则表达式
    var validateValue = $.trim($(validateField).val());
    var validateError = {};
    if (!regNoZeroNum.test(validateValue) && validateValue.length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].FORMAT);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].FORMAT; // 暂存具体的错误信息
    }
    else if (validateValue == 0) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else if (validateValue.length > length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MAXLENGTH);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].MAXLENGTH; // 暂存具体的错误信息
    }
    else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
    return validateError.status;
}
/* ------------------------------------------------------验证url地址文本框--------------------------------------------- */
function urlValidate(validateField, size) {
    var length = size ? size : 500;
    var strRegex = "[a-zA-z]+://[^\s]*";
    var RegUrl = new RegExp(strRegex);
    var validateValue = $.trim($(validateField).val());
    var validateError = {};
    if (!RegUrl.test(validateValue) && validateValue.length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].FORMAT);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].FORMAT; // 暂存具体的错误信息
    }
    else if (validateValue.length < 1) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else if (validateValue.length > length) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MAXLENGTH);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].MAXLENGTH;  // 暂存具体的错误信息
    }
    else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
}
//搜索标题验证
function seoTitleValidate(validateField) {
    var seoTitle = $.trim($(validateField).val());
    var seoTitleError = {};
    if (seoTitle.length < 1) {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(SE0TITLE_ERROR.EMPTY);
        seoTitleError.status = -1;
        seoTitleError.errorInfo = SE0TITLE_ERROR.EMPTY;
    }
    else if (seoTitle.length > 255) {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(SE0TITLE_ERROR.MAXLENGTH);
        seoTitleError.status = -1;
        seoTitleError.errorInfo = SE0TITLE_ERROR.MAXLENGTH;
    } else {
        $(validateField).parent().find('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent().find('.inputAreaError').text('');
        $(validateField).parent().find('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
        seoTitleError.status = 0;
        seoTitleError.errorInfo = '';
    }
    GOLBAL_ERROR.push(seoTitleError);
}
/* ---------------------------------------------------------验证下拉列表框------------------------------------------------ */
function selectValidate(validateField) {
    var validateValue = $.trim($(validateField).val());
    var validateError = {};
    if (validateValue == '0_请选择' || validateValue == 0) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
    return validateError.status;
}

/* ------------------------------------------------------验证上传文件--------------------------------------------------- */
function imgUploadValidate(validateField, prefix, width, height, imgWidth, imgHeight, maxSize) {
    var max_size = maxSize ? maxSize : 1 * 1024 * 1024;  // 默认多大上传图片为1M
    var imgWidth = imgWidth ? imgWidth : width;
    var imgHeight = imgHeight ? imgHeight : height;
    var filePath = $.trim($(validateField).val());
    var extStart = filePath.lastIndexOf('.');
    var ext = filePath.substring(extStart, filePath.length).toUpperCase();
    var imgUrlError = {};
    // console.info(prefix);
    // console.info($(validateField).parents('.form-group').find('.previewImg').attr('src'));
    // console.info(filePath.length);
    if (filePath.length > 0) {
        var imgFile = $(validateField)[0].files[0];
        var imgSize = imgFile.size;
        if (imgSize > max_size) {
            $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
            $(validateField).parent().find('.inputAreaError').text(validate[validateField].FILESIZE);
            imgUrlError.status = -1;
            imgUrlError.errorInfo = validate[validateField].FILESIZE;
        }
        else if (imgHeight != height || imgWidth != width) {
            $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
            $(validateField).parent().find('.inputAreaError').text(validate[validateField].SIZE + '指定尺寸:' + width + 'x' + height);
            imgUrlError.status = -1;
            imgUrlError.errorInfo = validate[validateField].SIZE + '指定尺寸:' + width + 'x' + height;
        }
        else if (ext != ".BMP" && ext != ".PNG" && ext != ".GIF" && ext != ".JPG" && ext != ".JPEG") {
            $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
            $(validateField).parent().find('.inputAreaError').text(validate[validateField].FORMAT);
            imgUrlError.status = -1;
            imgUrlError.errorInfo = validate[validateField].FORMAT;
        }
        else {
            $(validateField).parent().find('.inputAreaError').css('color', '#4cae4c');
            $(validateField).parent().find('.inputAreaError').text("");
            $(validateField).parent().find('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
            imgUrlError.status = 0;
            imgUrlError.errorInfo = '';
        }
    }
    else {
        if ($(validateField).parents('.modal-body').find('.previewImg').attr('src') == prefix ||
            $(validateField).parents('.form-group').find('.previewImg').attr('src') == prefix ) {
            $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
            $(validateField).parent().find('.inputAreaError').text(validate[validateField].EMPTY);
            imgUrlError.status = -1;
            imgUrlError.errorInfo = validate[validateField].EMPTY;
        }
        else {
            $(validateField).parent().find('.inputAreaError').css('color', '#4cae4c');
            $(validateField).parent().find('.inputAreaError').text("");
            $(validateField).parent().find('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
            imgUrlError.status = 0;
            imgUrlError.errorInfo = '';
        }
    }
    GOLBAL_ERROR.push(imgUrlError);
}

function fileUploadValidate(validateField, prefix) {
    // var size = size? size:2M; #TODO 限制上传文件大小
    var filePath = $.trim($(validateField).val());
    var extStart = filePath.lastIndexOf('.');
    var ext = filePath.substring(extStart, filePath.length).toUpperCase();
    var fileUrlError = {};
    if (filePath.length < 1 && $(validateField).parents('.modal-body').find('.previewImg').attr('src') == prefix) {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(validate[validateField].EMPTY);
        fileUrlError.status = -1;
        fileUrlError.errorInfo = validate[validateField].EMPTY;
    }
    else if (filePath.length > 0 && ext != ".MP4" && ext != ".AVI" && ext != ".3GP" && ext != ".FLV" && ext != ".RMVB") {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(validate[validateField].FORMAT);
        fileUrlError.status = -1;
        fileUrlError.errorInfo = validate[validateField].FORMAT;
    }
    // else if (filePath.length > 0) {  #TODO 限制上传文件大小
    //     $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
    //     $(validateField).parent().find('.inputAreaError').text(validate[validateField].SIZE);
    //     fileUrlError.status = -1;
    //     fileUrlError.errorInfo = validate[validateField].SIZE;
    // }
    else {
        $(validateField).parent().find('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent().find('.inputAreaError').text("");
        $(validateField).parent().find('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
        fileUrlError.status = 0;
        fileUrlError.errorInfo = '';
    }
    GOLBAL_ERROR.push(fileUrlError);
}
//图片标题验证
function imgTitleValidate(validateField) {
    var imgTitle = $.trim($(validateField).val());
    var imgTitleError = {};

    if (imgTitle.length < 1) {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(IMGTITLE_ERROR.EMPTY);
        imgTitleError.status = -1;
        imgTitleError.errorInfo = IMGTITLE_ERROR.EMPTY;
    }
    else if (imgTitle.length > 255) {
        $(validateField).parent().find('.inputAreaError').css('color', 'crimson');
        $(validateField).parent().find('.inputAreaError').text(IMGTITLE_ERROR.MAXLENGTH);
        imgTitleError.status = -1;
        imgTitleError.errorInfo = IMGTITLE_ERROR.MAXLENGTH;
    } else {
        $(validateField).parent().find('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent().find('.inputAreaError').text('');
        $(validateField).parent().find('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
        imgTitleError.status = 0;
        imgTitleError.errorInfo = '';
    }
    GOLBAL_ERROR.push(imgTitleError);
}

/* ----------------------------------------------验证普通名称类文本框-------------------------------------------------- */
function textBoxValidate(validateField, maxLength, minLength) {
    var min_length = minLength ? minLength : 1;
    var max_length = maxLength ? maxLength : 1000000;
    var validateValue = $.trim($(validateField).val());  // 待验证区的文本值
    var validateError = {};  // 暂存验证区错误信息

    if (validateValue.length < 1) {  //验证区为空值
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else if (validateValue.length < min_length && validateValue.length > 0) { // 验证区文本值超出范围错误
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MINLENGTH);
        validateError.status = -1;
        validateError.errorInfo = validate[validateField].MINLENGTH;
    }
    else if (validateValue.length > max_length) { // 验证区文本值超出范围错误
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MAXLENGTH);
        validateError.status = -1;
        validateError.errorInfo = validate[validateField].MAXLENGTH;
    } else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
    return validateError.status;
}
/* ----------------------------------------------验证普通名称类文本域-------------------------------------------------- */
function textAreaValidate(validateField, maxLength, minLength) {
    var min_length = minLength ? minLength : 1;
    var max_length = maxLength ? maxLength : 1000000;
    var validateValue = $(validateField).val();  // 待验证区的文本值
    validateValue = validateValue.replace(/^\s*|\s*$/g, "");  // 去除文本值中开头和结尾中的空格和换行符
    var validateError = {};  // 暂存验证区错误信息

    if (validateValue.length < 1) {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].EMPTY);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].EMPTY; // 暂存具体的错误信息
    }
    else if (validateValue.length < min_length && validateValue.length > 0) {  //验证区为空值
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');  // 验证区和错误提醒标签是同级
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MINLENGTH);
        validateError.status = -1;  // 错误状态值为-1，
        validateError.errorInfo = validate[validateField].MINLENGTH; // 暂存具体的错误信息
    }
    else if (validateValue.length > max_length) { // 验证区文本值超出范围错误
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
        $(validateField).parent('.form-group').children('.inputAreaError').text(validate[validateField].MAXLENGTH);
        validateError.status = -1;
        validateError.errorInfo = validate[validateField].MAXLENGTH;
    } else {
        $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
        $(validateField).parent('.form-group').children('.inputAreaError').text('');
        $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');  // 没有错误，提醒信息处设置为绿色小勾
        validateError.status = 0;
        validateError.errorInfo = '';
    }
    GOLBAL_ERROR.push(validateError);  // 整个表单的错误信息集
    return validateError.status;
}

/* ----------------------------------------------验证数据的唯一性-------------------------------------------------- */
function validateUnique(URL, validateField, errorInfo) {
    var validateError = {};
    var errorInfo = errorInfo ? errorInfo : "该值已存在，请重新输入！";
    var validateValue = $.trim($(validateField).val());
    var isUniqueId = getData(URL, validateValue).responseJSON.result.length ? false : true;  // getData返回的是id=XX的所有字段,没有就返回空
    if (validateValue) {
        if (isUniqueId) {
            $(validateField).parent('.form-group').children('.inputAreaError').css('color', '#4cae4c');
            $(validateField).parent('.form-group').children('.inputAreaError').text('');
            $(validateField).parent('.form-group').children('.inputAreaError').append('<span class="glyphicon glyphicon-ok"></span>');
            validateError.status = 0;
            validateError.errorInfo = '';
        } else {
            $(validateField).parent('.form-group').children('.inputAreaError').css('color', 'crimson');
            $(validateField).parent('.form-group').children('.inputAreaError').text(errorInfo);
            validateError.status = -1;
            validateError.errorInfo = errorInfo;
        }
        GOLBAL_ERROR.push(validateError);
    }
}
/*---------------------------------------------------END---------------------------------------------------------------*/