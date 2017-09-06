/**
 * Created by zml on 2016/5/15.
 */
<!--添加/更新数据-->
function addOrUpdateData(addOrUpdateUrl, selectUrl, jsonSet, currentModal) {   //jsonSet为检查过后的数据
    /*addOrUpdateUrl:更新或添加的url地址;selectUrl:查询的URL地址;jsonSet:添加或更新的数据集;currentModal:当前模态框;pageIndex:查询后的跳转页码;*/
    $.ajax({
        url: addOrUpdateUrl,
        type: 'POST',
        data: jsonSet,
        cache: false,
        contentType: false,  // 必须false才会自动加上正确的Content-Type
        processData: false,  // 必须false才会避开jQuery对 formdata 的默认处理
        success: function (data) {
            resultHandle(selectUrl, data, currentModal);
        }
    });
}
<!--分页查询数据-->
function selectData(selectUrl, pageIndex, pageSize, searchKeyWord) {
    /*selectUrl:查询的URL地址;pageSize:每页显示的数据条数;searchKeyWord:搜索关键字;pageIndex:查询后的跳转页码;*/
    pagesize = pageSize;  //  全局变量，用于63行重新list请求
    var searchKeyword = (searchKeyWord) ? searchKeyWord : '';
    $.get(selectUrl, {"currentPage": pageIndex, "pageSize": pageSize, "searchKeyWord": searchKeyword}, function (data) {
        if (data.code < 0) {
            warningPrompt(data.error);
        } else {
            showDataInTable(pageIndex, pageSize, data, selectUrl);
        }
    });
}
<!--同步查询数据-->
function getData(getUrl, id) {
    return $.ajax({
        url: getUrl,
        type: 'GET',
        data: {'id': id},
        async: false,  // 必须使用同步，不然数据还没有查询出来就return了
        dataType: 'json',
        success: function (data) {
            if (data.code < 0) {
                warningPrompt(data.error);
                return null;
            } else {
                return data;  // ajax中的return是返回给.ajax方法的
            }
        }
    });
}

<!--删除数据-->
function deleteData(delUrl, selectUrl, dataRowId, currentModal) {
    /*delUrl:删除的url地址;selectUrl:查询的URL地址;dataRowId:删除ID;currentModal:当前模态框;pageIndex:查询后的跳转页码;*/
    $.post(delUrl, {"id": dataRowId}, function (data) {
        resultHandle(selectUrl, data, currentModal);
    });
}
<!--对后台返回的数据进行处理-->
function resultHandle(selectUrl, resultData, currentModal) {
    if (resultData.code < 0) {
        warningPrompt(resultData.error);
    } else {
        $(currentModal).modal('hide');
        selectData(selectUrl, parseInt($('#pagination1 .active').text()), pagesize, $('#txt_search').text());
    }
}

/*渲染职业名称下拉框 <option value="id">name</option>*/
function addObjectNameOption(url, fillYield, firstSltName) {
    var firstSltName = firstSltName ? firstSltName : '请选择';
    var dataList = [];
    var data = getData(url);
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    dataList.push('<option value="0">' + firstSltName + '</option>');
    $.each(data.responseJSON.result, function (index, item) {
        if ("name" in item) {
            dataList.push('<option value="' + item.id + '">' + item.name + '</option>');
        } else {
            dataList.push('<option value="' + item.id + '">' + item.title + '</option>');
        }
    });
    $(fillYield).children().remove();
    $(fillYield).append(dataList.toString());
}

/*渲染下拉框 --- 格式:<option value="id_name">name</option>*/
function addNameOption(url, fillYield, firstSltName) {
    var firstSltName = firstSltName ? firstSltName : '请选择';
    var dataList = [];
    var data = getData(url);
    //alert(JSON.stringify(data));  //json对象转换为json字符串
    dataList.push('<option value="0_'+firstSltName+'">' + firstSltName + '</option>');
    $.each(data.responseJSON.result, function (index, item) {
        if ("name" in item) {
            dataList.push('<option value="' + item.id + '_' + item.name + '">' + item.name + '</option>');
        } else {
            dataList.push('<option value="' + item.id + '_' + item.title + '">' + item.title + '</option>');
        }
    });
    $(fillYield).children().remove();
    $(fillYield).append(dataList.toString());
}
