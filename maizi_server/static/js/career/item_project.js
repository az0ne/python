function onAdd(){
  var item_id = $("#item_id").val();
  window.location.href = "/career/item/project/add/?item_id="+item_id;
}

function onAddDo(){
  var item_id = $("#item_id").val();
  var name = $("#project_name").val();
  var url = $("#project_url").val();

  $.post("/career/item/project/add/do/",
    {
      "item_id":item_id,
      "name":name,
      "url":url
    },
    function(res){
    if(res.code==200){
      window.history.back();
    }
  });
}

function onUpdate(project_id){
  // console.log(project_id);
  window.location.href = "/career/item/project/update/?project_id="+project_id
}

function onUpdateDo(){
  var project_id = $("#project_id").val();
  var project_url = $("#project_url").val();
  var project_name = $("#project_name").val();

  $.post("/career/item/project/update/do/",
    {
      "project_id":project_id,
      "url":project_url,
      "name":project_name
    },
    function(res){
      if(res.code=200){
        window.history.back();
      }
    });
}

function onReturn(){
  window.history.back()
}
