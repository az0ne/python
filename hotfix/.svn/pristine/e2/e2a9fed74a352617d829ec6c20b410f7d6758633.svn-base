/* index 企业直通班课程 */
(function(){
  // width | height | top | left
  var layout = [
    [
      [0.1623,0.3333,0,0], [0.2564,0.3333,0,0.1623], [0.2564,0.6666,0,0.4187], [0.1623,0.3333,0,0.6751], [0.1623,0.3333,0,0.8374],
      [0.2564,0.6666,0.3333,0], [0.1623,0.3333,0.3333,0.2564], [0.1623,0.3333,0.3333,0.6751], [0.1623,0.3333,0.3333,0.8374],
      [0.1623,0.3333,0.6666,0.2564], [0.1623,0.3333,0.6666,0.4187], [0.2564,0.3333,0.6666,0.5810], [0.1623,0.3333,0.6666,0.8374]
    ],
    [
      [0.2564,0.6666,0,0], [0.1623,0.3333,0,0.2564], [0.2564,0.3333,0,0.4187], [0.1623,0.3333,0,0.6751], [0.1623,0.3333,0,0.8374],
      [0.1623,0.3333,0.3333,0.2564], [0.1623,0.3333,0.3333,0.4187], [0.2564,0.6666,0.3333,0.5810], [0.1623,0.3333,0.3333,0.8374],
      [0.1623,0.3333,0.6666,0], [0.2564,0.3333,0.6666,0.1623], [0.1623,0.3333,0.6666,0.4187], [0.1623,0.3333,0.6666,0.8374]
    ]
  ];
  layout.cur = null;
  window.indCourList = function (json) {
    var ul = $('.ind-cour-list');
    var html = '';
    if( layout.cur === 0 ){
      layout.cur = 1;
    }else{
      layout.cur = 0;
    }
    'array' == $.type(json) && $.each( json, function(i,o){
      var lay = layout[ layout.cur ];
      var lay_i = lay[ i ];
      html += '<li style="';
      html += 'width:' + (lay_i[ 0 ] || lay[ 0 ][ 0 ] ) * 100 + '%;';
      html += 'height:' + (lay_i[ 1 ] || lay[ 0 ][ 1] ) * 100 + '%;';
      html += 'top:' + (lay_i[ 2 ] || 0 ) * 100 + '%;';
      html += 'left:' + (lay_i[ 3 ] || 0 ) * 100 + '%;';
      html += '">';
      html += '<a href=/course/'+o.id+'><div class="ind-cour-i">';
      html += '<div class="ind-cour-i-m" style="background-color:';
      html += o.bgColor || '#1BBC9B';
      html += '">';
      html += '<i class="vh-i"></i>';
      html += '<div class="cnt-area">';
      html += '<span class="ico"><img class="lazy" src="/static/images/default2.png" data-original="/uploads/';
      html += o.imgUrl;
      html += '" alt="';
      html += o.text;
      html += '"></span>';
      html += '<span class="text">';
      html += o.text;
      html += '</span>';
      html += '</div>';
      html += '</div>';
      html += '<div class="ind-cour-i-d">';
      html += '<i class="mask-bg"></i>';
      html += '<i class="vh-i"></i>';
      html += '<div class="cnt-area">';
      html += o.count;
      html += '位学员正在学习</div>';
      html += '</div>';
      html += '</div></a>';
      html += '</li>';
        //console.log(html);
    });
    ul.html( html ).find( 'li' ).hide().fadeIn('slow').hover(function(){
      var that = this;
      if( !that.d ){
        that.d = $( '.ind-cour-i-d', that );
      }
      that.t = setTimeout(function(){
        that.d.stop(1).animate({ top : '0%' },'fast');
      },100);
    },function(){
      var that = this;
      that.t && clearTimeout( that.t );
      that.d.stop(1).animate({ top : '120%' },'fast');
    });
  }
  
}());