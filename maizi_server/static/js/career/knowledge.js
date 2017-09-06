function onAdd(){
  window.location.href = '/career/knowledge/add/';
}

function onAddDo(){
  var name = $("#knowledge_name").val();
  var course_id = $("#slctAssistant").val();
  var order_index = $("#knowledge_order_index").val();
  var url = $("#knowledge_url").val();

  $.post('/career/knowledge/add/do/',{
    'name':name,
    'course_id':course_id,
    'order_index':order_index,
    'url':url
  },function(res){
    if(res.code==200){
      window.location.href = '/career/knowledge/';
    }
  });

}

function onReturn(){
  window.location.href = '/career/knowledge/';
}

function onUpdate(knowledge_id){
  window.location.href = '/career/knowledge/update/?knowledge_id='+knowledge_id;
}

function onUpdateDo(){
  var name = $("#knowledge_name").val();
  var order_index = $("#knowledge_order_index").val();
  var url = $("#knowledge_url").val();
  var course_id = $("#course_id").val();

}

function onQuery(){
  var name = $("#txtitem").val();
  window.location.href = "/career/knowledge/?name="+name
}

function page_onFirst(url){
  window.location.href = "/career/knowledge/"
}

function page_onPreview(url){
  pageSize = $('#slctPageSize').val()
  pageIndex = parseInt($('#spnPageIndex').html())-1
  if (pageIndex>0){
    window.location.href = '/career/knowledge/?pageSize='+pageSize+"&pageIndex="+pageIndex
  }

}

function page_onNext(url){
  pageSize = $('#slctPageSize').val()
  pageIndex = parseInt($('#spnPageIndex').html())+1 //jquery获取span标签的值为html，js原生的是innerText
  // console.log('/land/?pageSize='+pageSize+"&pageIndex="+pageIndex)
  window.location.href = '/career/knowledge/?pageSize='+pageSize+"&pageIndex="+pageIndex
}

function page_onLast(url){}
