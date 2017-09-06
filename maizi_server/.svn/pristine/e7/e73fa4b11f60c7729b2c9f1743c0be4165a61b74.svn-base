function onAdd(){
  window.location.href = "/career/author/add/";
}

function onUpdate(author_id){
  window.location.href = "/career/author/update/?author_id="+author_id;
}

function onAddDo(){
  var name = $("#author_name").val();
  var info = $("#author_info").val();
  var fileName = $("#txtFileName").val();
  var fileExtension = $("#txtExtension").val();

  $.post("/career/author/add/do/",{
  "name":name,
  "info":info,
  "fileName":fileName,
  "fileExtension":fileExtension
  },
  function(res){
    if(res.code==200){
      window.location.href = "/career/author/";
    }else{
      alter("error");
  }
  });

}

function onUpdateDo(){
  var id = $("#author_id").val();
  var name = $("#author_name").val();
  var info = $("#author_info").val();
  var fileName = $("#txtFileName").val();

  if(fileName==''){
    var file = $("#author_head_url").val()
    var fileName = file.match("[0-9]+.png")[0]

  }

  $.post("/career/author/update/do/",{
  "author_id":id,
  "name":name,
  "info":info,
  "fileName":fileName,
  // "fileExtension":fileExtension
  },
  function(res){
    if(res.code==200){
      window.location.href = "/career/author/"
    }else{
      alter("error")
  }
  });

  }

function onReturn(){
  window.history.back();
}

function onQuery(){
  var name = $("#txtItem").val();

  window.location.href = "/career/author/?name="+name;
}
