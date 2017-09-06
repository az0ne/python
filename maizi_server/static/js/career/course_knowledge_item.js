function onUpdateDo(){
  // var knowledge_id = $("#knowledge_id").val()
  // var course_id = $("#course_id").val()
  var knowledge_name = $("#knowledge_name").val();
  var knowledge_order_index = $("#knowledge_order_index").val();
  var knowledge_type = $("#knowledge_type").val();
  var item_id = $("#item_id").val();

  $.post("/career/course/knowledge/item/update/",{
    "item_id":item_id,
    // "knowledge_id":knowledge_id,
    // "course_id":course_id,
    "knowledge_name":knowledge_name,
    "knowledge_order_index":knowledge_order_index,
    "knowledge_type":knowledge_type

  },function(res){
    if(res.code==200){
      window.history.back();
    }
  })
}

function onReturn(){
  window.history.back();
}

function onUpdate(item_id){
  var knowledge_id = $("#knowledge_id").val();
  var course_id = $("#course_id").val();

  // console.log(knowledge_id,course_id)
  window.location.href = "/career/course/knowledge/item/update/?item_id="+item_id+"&course_id="+course_id+"&knowledge_id="+knowledge_id;

}

function onUpdateDo(){
  var item_id = $("#item_id").val();
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_name = $("#item_name").val();
  var item_order_index = $("#item_order_index").val();

  // var item_type = $("#item_type input[name='type']:checked").val();

  $.post("/career/course/knowledge/item/update/do/",{
    "item_id":item_id,
    "knowledge_id":knowledge_id,
    "course_id":course_id,
    "item_name":item_name,
    "item_order_index":item_order_index
    // "item_type":item_type
  },function(res){
    if(res.code==200){
      window.location.href = "/career/course/knowledge/item/?course_id="+course_id+"&knowledge_id="+knowledge_id;
    }
  })

}

function onAdd(){
  // var course_id = $("#course_id").val()
  // var knowledge_id = $("#knowledge_id").val()

  var course_id = window.location.href.split('=')[1].split("&")[0];
  var knowledge_id = window.location.href.split('=')[2];

  window.location.href = "/career/course/knowledge/item/add/?course_id="+course_id+"&knowledge_id="+knowledge_id;
}

function onAddDo(){

  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var item_name = $("#item_name").val();
  // item_type = $("#item_type").val()
  var item_type = $("#item_type input[name='type']:checked").val();
  var order_index = $("#item_order_index").val();


  $.post("/career/course/knowledge/item/add/do/",{
    "course_id":course_id,
    "knowledge_id":knowledge_id,
    "item_name":item_name,
    "item_type":item_type,
    "order_index":order_index
  },function(res){
    if(res.code==200){
      window.location.href = "/career/course/knowledge/item/?course_id="+course_id+"&knowledge_id="+knowledge_id;
    }
  });

}

function onQuery(){}

function onStart(item_id){

  _confirmDialog1("请确认","是否启用该章节",function(val){
    var course_id = $("#course_id").val();
    var knowledge_id = $("#knowledge_id").val();
    $.get("/career/course/knowledge/item/set/",{
          "course_id":course_id,
          "knowledge_id":knowledge_id,
          "item_id":item_id,
          "state":1
      },
    function(res){
        if(res.code==200){
          window.location.href = window.location.href;
        }
      });
  },item_id);


}

function onStop(item_id){

  _confirmDialog1("请确认","是否禁用该章节",function(val){
    var course_id = $("#course_id").val();
    var knowledge_id = $("#knowledge_id").val();
    $.get("/career/course/knowledge/item/set/",{
        "course_id":course_id,
        "knowledge_id":knowledge_id,
        "item_id":item_id,
        "state":0
    },
    function(res){
      if(res.code==200){
          window.location.href = window.location.href;
      }
    });
  },item_id);



}

function onManager(item_id){
  var item_type = $("#item_type").val();
  var resource_id = $("#item_resource_id").val();

  window.location.href = "/career/item/vedio/?item_id="+item_id+"&item_type="+item_type+"&resource_id="+resource_id;
}

function onNote(item_id){
  item_id = $("#item_id").val();
  course_id = $("#course_id").val();
  knowledge_id = $("#knowledge_id").val();

  window.location.href = "/career/item/note/?course_id="+course_id+"&knowledge_id="+
  knowledge_id+"&item_id="+item_id

}
