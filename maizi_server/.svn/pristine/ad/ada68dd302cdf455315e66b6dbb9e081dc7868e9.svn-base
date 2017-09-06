function onAdd(){
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_id = $("#item_id").val();


  window.location.href = "/career/item/note/add/?course_id="+course_id+
  "&knowledge_id="+knowledge_id+"&item_id="+item_id

}

function onAddDo(){
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_id = $("#item_id").val();

  var content = $("#note_content").val();

  $.post("/career/item/note/add/do/",
    {
        "course_id":course_id,
        "knowledge_id":knowledge_id,
        "item_id":item_id,
        "content":content
    },
    function(res){
    if(res.code==200){
      window.history.back()
    }
  });
}

function onUpdate(note_id){
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_id = $("#item_id").val();

  window.location.href = "/career/item/note/update/?note_id="+note_id+"&item_id="+item_id+
  "&knowledge_id="+knowledge_id+"&course_id="+course_id
}

function onUpdateDo(){
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_id = $("#item_id").val();
  var content = $("#note_content").val();
  var note_id = $("#note_id").val();
  // alert(content)
  $.post("/career/item/note/update/do/",
    {
      "note_id":note_id,
      "content":content
    }
    ,function(res){
      if(res.code==200){
        window.location.href = "/career/item/note/?course_id="+course_id+
        "&knowledge_id="+knowledge_id+"&item_id="+item_id

      }
  });

}
