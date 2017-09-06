/**
 * Created by Administrator on 2016/5/24.
 */
function getPage() {
    var page = "&page_index=" + $("#hidPageIndex").val();
    return page;
}

function getPage2(prefix) {
    var page = prefix + "page_index=" + $("#hidPageIndex").val();
    return page;
}

function checkPage(pageIndex) {
    if (isNaN(pageIndex)) {
        pageIndex = 1;
    }
    pageIndex = parseInt(pageIndex);
    var pageCount = parseInt($("#hidPageCount").val());
    if (pageIndex > pageCount) {
        pageIndex = pageCount;
    }
    if (pageIndex < 1) {
        pageIndex = 1;
    }
    $("#hidPageIndex").val(pageIndex);
    return pageIndex;
}

function onFirst() {
    pageIndex = checkPage(1);
    var cururl = window.location.href;
    search();
}

function onLast() {
    pageIndex = checkPage(parseInt($("#hidPageCount").val()));
    search();
}

function onNext() {
    pageIndex = checkPage(parseInt($("#hidPageIndex").val()) + 1);
    search();
}

function onPre() {
    pageIndex = checkPage(parseInt($("#hidPageIndex").val()) - 1);
    search();
}

function onDiretct() {
    if (isNaN($("#txtPageIndex").val())) {
        $("#txtPageIndex").val("1");
    }
    pageIndex = checkPage(parseInt($("#txtPageIndex").val()));
    search();
}
function search() {
    var cururl = window.location.href;
    var staurl = cururl.split("&page_index=")[0];
    var inurl = cururl.indexOf("action=search");
    if (inurl < 0) {
        onQuery();
    } else {
        window.location.href = staurl + "&page_index=" + $("#hidPageIndex").val();
    }
}
