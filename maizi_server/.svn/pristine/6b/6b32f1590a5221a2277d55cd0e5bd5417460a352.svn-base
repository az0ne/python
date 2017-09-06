function onAdd(){
  // var id = $('#course_id').val()
  var id = window.location.href.split("=")[1];
  window.location.href = "/career/course/knowledge/add/?course_id="+id;
}

function onUpdate(id){
  window.location.href = "/career/course/knowledge/update/?knowledge_id="+id;
}

function onAddDo(){
  var course_id = $('#course_id').val();
  var knowledge_name = $('#knowledge_name').val();
  var knowledge_order_index = $('#knowledge_order_index').val();
  // var knowledge_url = $('#knowledge_url').val()


  $.post("/career/course/knowledge/add/do/",{
    "course_id":course_id,
    "knowledge_name":knowledge_name,
    "knowledge_order_index":knowledge_order_index,
    // "knowledge_url":knowledge_url
  },function(res){
    if(res.code==200){
      window.location.href = "/career/course/knowledge/?course_id="+course_id;
    }
  })

}

function onUpdateDo(){
  var course_id = $("#course_id").val();
  var knowledge_id = $("#knowledge_id").val();
  var knowledge_name = $("#knowledge_name").val();
  var knowledge_order_index = $("#knowledge_order_index").val();
  // var knowledge_url = $("#knowledge_url").val()

  $.post("/career/course/knowledge/update/do/",{
    "course_id":course_id,
    "knowledge_id":knowledge_id,
    "knowledge_name":knowledge_name,
    "knowledge_order_index":knowledge_order_index,
    // "knowledge_url":knowledge_url,
  },function(res){
    if(res.code==200){
      window.location.href = "/career/course/knowledge/?course_id="+course_id;
    }
  })

}

function onStart(knowledge_id){
  course_id = $("#course_id").val();
  $.get('/career/course/knowledge/set/',{
    'state':1,
    'knowledge_id':knowledge_id
  },function(res){
    if(res.code==200){
      // window.location.href = '/course/knowledge/?course_id='+course_id
      window.location.href = window.location.href;
    }
  });
}

function onStop(knowledge_id){
  course_id = $("#course_id").val();
  $.get('/career/course/knowledge/set/',{
    'state':0,
    'knowledge_id':knowledge_id
  },function(res){
    if(res.code==200){
      // window.location.href = '/course/knowledge/?course_id='+course_id
      window.location.href = window.location.href;
    }
  });
}

function onManager(knowledge_id){
  // var course_id = $('#course_id').val()
  var course_id = window.location.href.split("=")[1]
  window.location.href = "/career/course/knowledge/item/?course_id="+course_id+"&knowledge_id="+knowledge_id
}

function onReturn(){
  window.history.back()
}
