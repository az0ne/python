function onAdd(){
  window.location.href = '/career/course/add';
}

function onAddDo(){

  var course_name = $("#course_name").val();
  var course_order_index = $('#course_order_index').val();
  var courseAuthor = $("#courseAuthor").val()
  var career_id = $("#slcLand").val();

  function success(res){
    if(res.code == 200){
      window.location.href = '/career/course/';
    }
  }

  url = '/career/course/add/do/';

  data = {
  'course_name':course_name,
  'course_order_index':course_order_index,
  "career_id":career_id,
  "courseAuthor":courseAuthor
  }

  $.post(url,data,success);

}

function onReturn(){
  window.location.href = '/career/course/';
}

function onUpdate(course_id){
  // alert(course_id)
  window.location.href = '/career/course/update/?course_id='+course_id;
}

function onUpdateDo(){
  var course_id = $('#course_id').val();
  var course_name = $('#course_name').val();
  var course_order_index = $('#course_index').val();
  var teacher_id = $("#courseAuthor").val();

  $.post("/career/course/update/do/",{
    'course_id':course_id,
    'course_name':course_name,
    'course_order_index':course_order_index,
    "teacher_id":teacher_id
  },function(res){
    if(res.code==200){
      window.location.href = '/career/course/';
    }
  });

}

// page infos

function page_onFirst(url){
  window.location.href = "/career/course/";
}

function page_onPreview(url){
  pageSize = $('#slctPageSize').val();
  pageIndex = parseInt($('#spnPageIndex').html())-1;
  console.log(pageIndex)
  if (pageIndex>0){
    window.location.href = '/career/course/?pageSize='+pageSize+"&pageIndex="+pageIndex;
  }

}

function page_onNext(url){
  pageSize = $('#slctPageSize').val();
  pageIndex = parseInt($('#spnPageIndex').html())+1; //jquery获取span标签的值为html，js原生的是innerText
  window.location.href = '/career/course/?pageSize='+pageSize+"&pageIndex="+pageIndex;
}

function page_onLast(url){}

function onStart(course_id){
  _confirmDialog1("请确认","是否启用该小课程",function(val){
    $.get('/career/course/set/',{
      'state':1,
      'course_id':course_id
    },function(res){
      if(res.code==200){
        // window.location.href = '/career/course/'
        window.location.href = window.location.href;
      }
    });
  },course_id)

}

function onStop(course_id){
  _confirmDialog1("请确认","是否禁用该小课程",function(val){
    $.get('/career/course/set/',{
      'state':0,
      'course_id':course_id
    },function(res){
      if(res.code==200){
        // window.location.href = '/career/course/'
        window.location.href = window.location.href;
      }
    });
  },course_id)

}

function onQuery(){
  var name = $("#txtitem").val()
  window.location.href = "/career/course/?name="+name;
}

function onManager(course_id){
  window.location.href = '/career/course/knowledge/?course_id='+course_id;
}

// function onAuthor(course_id){}
