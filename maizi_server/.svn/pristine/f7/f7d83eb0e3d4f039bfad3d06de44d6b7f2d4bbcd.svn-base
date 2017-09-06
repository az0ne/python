function onAdd(land_id){
  window.location.href = "/career/land/course/add/?land_id="+land_id;
}

function onUpdate(course_id){
  land_id = land_id = window.location.href.match("[0-9]+$")[0];
  window.location.href = "/career/land/course/update/?land_id="+land_id+"&course_id="+course_id
}

function onAddDo(){
  land_id = window.location.href.match("[0-9]+$")[0];
  course_id = $("#course_id").val();

  $.post("/career/land/course/add/do/",{
    "land_id":land_id,
    "course_id":course_id
  }, function(res){
    if(res.code==200){
      window.history.back()
    }
  });
}

function onUpdateDo(){}

function onReturn(){}
