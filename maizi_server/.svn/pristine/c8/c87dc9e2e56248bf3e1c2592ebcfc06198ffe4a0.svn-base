function onAdd(){
  window.location.href = "/career/book/add/";
}

function onAddDo(){
  var name = $("#book_name").val();
  var description = $("#book_description").val();
  var book_author = $("#book_author").val();
  var txtFileName = $("#txtFileName").val();
  var txtExtension = $("#txtExtension").val();
  var url = txtFileName;

  $.post(
    "/career/book/add/do/",
    {
      "name":name,
      "book_author":book_author,
      "description":description,
      "url":url,
    },
    function(res){
      if(res.code==200){
        window.location.href = "/career/book/"
      }
    }
  )
}

function onQuery(){
  var query_name = $("#txtItem").val();
  
}

function onReturn(){
  window.history.back();
}
