function onAdd(vedio_id){
  var item_id = $("#item_id").val();
  window.location.href = "/career/item/vedio/add/?vedio_id="+vedio_id+"&item_id="+item_id;
}

function onAddDo(){
  var item_id = $("#item_id").val();
  var url = $("#vedio_url").val();
  var name = $("#vedio_name").val()

  $.post("/career/item/vedio/add/do/",{
    "url":url,
    "name":name,
    "item_id":item_id
  },function(res){
    if(res.code==200){
      window.history.back();
    }
  });
}

function onReturn(){
  window.history.back();
}

function onUpdate(item_id){
  var item_id = item_id;
  var vedio_id = $("#vedio_id").val();

  window.location.href = "/career/item/vedio/update/?item_id="+item_id+"&vedio_id="+vedio_id;
}

function onUpdateDo(){
  var item_id = $("#item_id").val();
  var vedio_id = $("#vedio_id").val();
  var url = $("#vedio_url").val();
  var name = $("#vedio_name").val();

  $.post("/career/item/vedio/update/do/",{
      "item_id":item_id,
      "vedio_id":vedio_id,
      "url":url,
      "name":name
  },
  function(res){
    if(res.code==200){
      window.history.back();
    }
  })

}
