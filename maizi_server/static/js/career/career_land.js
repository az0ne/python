
function onAdd(){
  window.location.href = '/career/land/add/';
}

function onAddDo(){
  name = $('#land_name').val();
  remark = $("#land_remark").val();
  // state = $("#land_state").val()

  $.post(
    '/career/land/add/do/',
    {
    'name':name,
    'remark':remark
    // 'state':state
    },
    function(res){
      if(res.code == 200){
        window.location.href = '/career/land/';
      }

    });

}

function onUpdate(land_id){
  window.location.href = "/career/land/update/?land_id="+land_id;
}

function onUpdateDo(){
  var land_name = $('#land_name').val();
  var land_remark = $('#land_remark').val();
  var land_id = $('#land_id').val();

  $.post(
    '/career/land/update/do/',
    {
    'name':land_name,
    'remark':land_remark,
    'land_id':land_id
    },
    function(res){
      if(res.code == 200){
        window.location.href = '/career/land/';
      }

    });
}

function onStart(land_id){

  _confirmDialog1("请确认","是否启用该课程",function(val){

    $.get('/career/land/state/',{'land_id':land_id,'state':1},function(res){if(res.code == 200){
      window.location.href = window.location.href;
    }})

  },land_id);

}

function onStop(land_id){
  _confirmDialog1("请确认","是否禁用该课程",function(val){

    $.get('/career/land/state/',{'land_id':land_id,'state':0},function(res){if(res.code == 200){
      // window.location.href = '/career_land/'
      window.location.href = window.location.href;
    }})

  },land_id);

}

function onReturn(){
  window.location.href = '/career/land/'
}

// page infos

function page_onFirst(url){
  window.location.href = "/career/land/"
}

function page_onPreview(url){
  pageSize = $('#slctPageSize').val()
  pageIndex = parseInt($('#spnPageIndex').html())-1
  console.log(pageIndex)
  if (pageIndex>0){
    window.location.href = '/career/land/?pageSize='+pageSize+"&pageIndex="+pageIndex
  }

}

function page_onNext(url){
  pageSize = $('#slctPageSize').val()
  pageIndex = parseInt($('#spnPageIndex').html())+1 //jquery获取span标签的值为html，js原生的是innerText
  // console.log('/career_land/?pageSize='+pageSize+"&pageIndex="+pageIndex)
  window.location.href = '/career/land/?pageSize='+pageSize+"&pageIndex="+pageIndex
}

function page_onLast(url){}

function onManager(land_id){
  window.location.href = "/career/land/course/?land_id="+land_id;
}
