function page_onFirst(url){
  window.location.href = "/career/item/";
}

function page_onPreview(url){
  pageSize = $('#slctPageSize').val();
  pageIndex = parseInt($('#spnPageIndex').html())-1;
  if (pageIndex>0){
    window.location.href = '/career/item/?pageSize='+pageSize+"&pageIndex="+pageIndex;
  }

}

function page_onNext(url){
  pageSize = $('#slctPageSize').val();
  pageIndex = parseInt($('#spnPageIndex').html())+1;
  window.location.href = '/career/item/?pageSize='+pageSize+"&pageIndex="+pageIndex;
  // console.log("check")
}

function page_onLast(url){}

function onQuery(){
  name = $("#txtitem").val();
  window.location.href = "/career/item/?name="+name;
}
