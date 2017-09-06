/**
 * Created by Administrator on 2017/3/8.
 */
$(document).ready(function() {
    var pageSize = $("#hdnPageSize").val();
    if (pageSize == "")
    {
        pageSize = 10;
    }
    $("#slctPageSize").val(pageSize);
});

function page_getQuery()
{
    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    var pageIndex = parseInt($("#hdnPageIndex").val());
    return "page_index=" + pageIndex + "&page_size=" + pageSize + "&" + queryString;
}

function page_onFirst(url) {
    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    window.location.href = url + "?page_index=1&page_size=" + pageSize + "&" + queryString;
}

function page_onPreview(url) {
    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    var pageIndex = parseInt($("#hdnPageIndex").val());
    if (pageIndex > 1) {
        pageIndex = pageIndex - 1;
        window.location.href = url + "?page_index=" + pageIndex + "&page_size=" + pageSize + "&" + queryString;
    }
}

function page_onNext(url) {
    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    var pageIndex = parseInt($("#hdnPageIndex").val()) ;
    var pageCount = parseInt($("#hdnPageCount").val());
    if(pageIndex < pageCount)
    {
        pageIndex = pageIndex + 1;
        window.location.href = url + "?page_index=" + pageIndex + "&page_size=" + pageSize + "&" + queryString;
    }
}

function page_onLast(url) {
    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    var pageIndex = parseInt($("#hdnPageIndex").val());
    var pageCount = parseInt($("#hdnPageCount").val());
    pageIndex = pageCount;
    window.location.href = url + "?page_index=" + pageIndex + "&page_size=" + pageSize + "&" + queryString;
}

function page_onRedirect(url) {


    if(!_isInteger($("#txtPageIndex").val()))
    {
        return;
    }

    var pageSize = $("#slctPageSize").val();
    var queryString = $("#hdnQuery").val();
    var pageIndex = parseInt($("#txtPageIndex").val());
    var pageCount = parseInt($("#hdnPageCount").val());

    if(pageIndex > pageCount)
    {
        pageIndex = pageCount;
    }

    if(pageIndex < 1)
    {
        pageIndex = 1;
    }

    window.location.href = url + "?page_index=" + pageIndex + "&page_size=" + pageSize + "&" + queryString;
}