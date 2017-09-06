var Chart = (function(window){
    chart = function () {
        var _self = this;
        return _self;
    }

    var classList,
        classDate,
        _Width = 110,
        _StartDay,
        dataList = [classList,classDate];

    chart.prototype.init = function (option) {
        var dataLength;
        classList = option.classList;
        classDate = option.classDate;
        _interval = option.classDate.interval;
        dataLength = classList.length;
        chart.setTableWidth(dataLength);
        chart.creatTable(0,classList); // 初始化顶部课程列表
        chart.creatTable(1,classDate,classList); // 初始化底部日期列表
        chart.creatTable(2,classList); //初始化中间table
        chart.lineDrawing(dataLength, classList);
    }
    chart.prototype.setTableWidth = function (length) {
        var length = length,
            width = _Width * (length+1) + length + 1; // +length是因为每个框都有一个1PX的border
        $(".table-date").css("width",width);
        $(".table-content,.table-name,.table-line").css("width",width);

    }
    chart.prototype.creatTable = function(htmlIndex,data,list) {
        if(!data) data = dataList[htmlIndex];
        tableHtml(htmlIndex,data,list);
    }
    chart.prototype.lineDrawing = function(length, classList) {
        // 组装提示信息的html
        function produceMsg (msg){
            var tmpStr = '';
            for (var i = 0; i < msg.length; i++){
                tmpStr += '<li class="item-msg">' + msg[i].replace(/</g, "&lt;") + '</li>';
            }
            return tmpStr;
        }
        require.config( {
            baseUrl: '/static/js/chart',
            paths: {
                'zrender': 'zrender',
                'zrender/shape/Line': 'zrender',
                'zrender/shape/Circle': 'zrender',
                'zrender/tool/guid': 'zrender'
            }
        } );
        // 计算计划直线的长度
        var width = _Width * (length+1) + length;
        $("#charts-box-canvas").css("width", width + 40);
        require(['zrender',
            'zrender/shape/Line',
            'zrender/shape/Circle',
            'zrender/tool/guid'],
            function(zrender,
                LineShape,
                CircleShape,
                Guid){
            var zr = zrender.init(document.getElementById('charts-box-canvas'));
            var greenCircleGuid = [];
            var realCircleGuid = [];
            var yStart = 20;
            var xStart = 0;
            var realYStart = yStart;    //实际完成情况曲线每次的起点
            // 绿色的直线
            zr.addShape(new LineShape({
                style : {
                    xStart : xStart,
                    yStart : yStart,
                    xEnd : xStart + width,
                    yEnd : yStart,
                    color : '#1abc9c',   // == color
                    lineWidth : 2,
                    lineType : 'solid',
                },
                hoverable: false
            }));
            // 绿色的直线上绿色圆
            for (var i = 1; i <= length; i++){
                if (classList[i - 1].state == "rest"){
                    // 当时休息时，需要画灰色的线覆盖原来的绿色线,覆盖两块
                    color = '#c0c0c0';
                    zr.addShape(new LineShape({
                        style : {
                            xStart : xStart + 4 + ((i - 1) * (_Width + 1)), // 4是圆的半径
                            yStart : yStart,
                            xEnd : xStart + ((i + 1) * (_Width + 1)),
                            yEnd : yStart,
                            color : '#c0c0c0',   // == color
                            lineWidth : 2,
                            lineType : 'solid',
                        },
                        hoverable: false
                    }));
                }

                var realColor = '#e78964';
                var nextYStart = yStart + 157 - ((classList[i - 1].rank) / 100 * 157);
                // 画实际学习情况的曲线
                if ((classList[i - 1].state == "on" || classList[i - 1].state == "reset") &&
                    ((i == 1) || classList[i - 2].state == "on" || classList[i - 2].state == "reset") &&
                    (realYStart != nextYStart || nextYStart != yStart)){
                    // 得到本次画线的终点也是下一个起点的Y轴位置
                    var id = Guid();
                    zr.addShape(new LineShape({
                        id: id,
                        style : {
                            xStart : xStart + ((i - 1) * (_Width + 1)),
                            yStart : yStart,
                            xEnd : xStart + (i * (_Width + 1)),
                            yEnd : yStart,
                            color : realColor,   // == color
                            lineWidth : 2,
                            lineType : 'solid',
                        },
                        hoverable: false
                    }));
                    zr.animate(id, "style", false)
                        .when(1000, {
                            yStart: realYStart,
                            yEnd: nextYStart
                        }).start('QuarticOut');

                }
                realYStart = nextYStart;
            }
            // 重置realYStart
            realYStart = yStart;
            for (var i = 1; i <= length; i++){
                // var id = Guid();
                // var realId = Guid();
                // greenCircleGuid.push(id);
                // realCircleGuid.push(realId);
                var color = '#1abc9c';
                if (classList[i - 1].state == "off"){
                    color = '#e78964';
                }
                if (classList[i - 1].state == "rest"){
                    // 当时休息时，需要画灰色的线覆盖原来的绿色线,覆盖两块
                    color = '#c0c0c0';
                }

                var mouseOverFlag = false;
                var realColor = '#e78964';
                var nextYStart = yStart + 157 - ((classList[i - 1].rank) / 100 * 157);
                // 画实际学习情况的曲线
                if ((classList[i - 1].state == "on" || classList[i - 1].state == "reset" ||
                    classList[i - 1].state == "noline")){
                    // 得到本次画线的终点也是下一个起点的Y轴位置
                    mouseOverFlag = true;
                    var id = Guid();
                    zr.addShape(new CircleShape({
                        id: id,
                        style : {
                            x : xStart + (i * (_Width + 1)),
                            y : yStart,
                            r : 4,
                            color : realColor,          // rgba supported
                        }
                    }));
                    zr.addShape(new CircleShape({
                        style : {
                            x : xStart + (i * (_Width + 1)),
                            y : nextYStart,
                            r : 12,
                            color : "transparent",          // rgba supported
                        },
                        onmouseover : (function(msg){
                            return function(eventPacket) {
                                    var $tips = $(".learn-plan-tips");
                                    $tips.html(produceMsg(msg));
                                    if ($tips.is(":hidden")){
                                        $tips.css({"top":(eventPacket.event.clientY + 15) + "px", "left":(eventPacket.event.clientX - 57) + "px"});
                                        $tips.show();
                                    }
                                }
                        })(classList[i - 1].msg),
                        onmouseout : function(eventPacket) {
                            $(".learn-plan-tips").hide();
                        }
                    }));
                    zr.animate(id, "style", false)
                        .when(1000, {
                            y: nextYStart,
                        }).start('QuarticOut');
                }
                realYStart = nextYStart;
                zr.addShape(new CircleShape({
                    style : {
                        x : xStart + (i * (_Width + 1)),
                        y : yStart,
                        r : 4,
                        color : color,          // rgba supported
                    }
                }));
                zr.addShape(new CircleShape({
                    style : {
                        x : xStart + (i * (_Width + 1)),
                        y : yStart,
                        r : 12,
                        color : "transparent",          // rgba supported
                    },
                    onmouseover : (function(msg, mouseOverFlag){

                        return function(eventPacket) {
                            if (!mouseOverFlag){
                                var $tips = $(".learn-plan-tips");
                                $tips.html(produceMsg(msg));
                                if ($tips.is(":hidden")){
                                    $tips.css({"top":(eventPacket.event.clientY + 15) + "px", "left":(eventPacket.event.clientX - 57) + "px"});
                                    $tips.show();
                                }
                            }
                        }
                    })(classList[i - 1].msg, mouseOverFlag),
                    onmouseout : function(eventPacket) {
                        $(".learn-plan-tips").hide();
                    }
                }));
            }
            zr.render();
        });
    }
    function tableHtml (index,data,list) {
        switch(index) {
            /*
             * 0:顶部课程
             * 1:底部日期
             * 2:列表个数
            */
            case 0:
                var html = "";
                for(var i = 0; i < data.length; i++ ) {
                    var classProcess = data[i].process,
                        className = data[i].iclass,
                        classOn = data[i].state;
                     html += '<li style="width:'+_Width+'px;height:50px" class="transform '+classOn+'"><p class="font-color-ft">'+classProcess+'</p><p class="font-color-es f12">'+className+'</p></li>';
                }
                $(".table-name").append(html);
                $(".table-name").show();
                break;
            case 1:
                var html = '<li style="width:110px;height:25px"></li>',
                    length = classList.length,
                    _StartDay = new Date(data.startDay).getTime();
                for(var i = 0; i <= length + 1; i++ ) {
                    if( i < length) {
                        var date = forMatTime(list[i].interval,_StartDay);
                        html += '<li style="width:110px;height:25px">'+date+'</li>'
                    }
                }
                $(".table-date").append(html);
                $(".table-date li").eq(length+1).css("width","50");
                break;
            case 2:
                var length = classList.length,
                    html = "",
                    html2 = "";
                for ( var i = 0; i <= length; i++ ) {
                    html += '<li style="width:'+_Width+'px;height:78px"></td>'
                }
                for ( var i = 0; i <= length; i++ ) {
                    html2 += '<li style="width:'+_Width+'px;height:35px"></li>'
                }
                $(".table-content ul").append(html);
                $(".table-line").append(html2);
        }
    }
    var days = 0;
    function forMatTime (i,_StartDay) {
        var month,
            day,
            date,
            spDate,
            sendDate,
            newDate;
        date = _StartDay + (parseInt(days) + parseInt(i)) * 24 * 60 * 60 * 1000;
        days = parseInt(i) + parseInt(days);
        spDate = new Date(date);
        sendDate = spDate.getFullYear() + "-" + (spDate.getMonth()+1) + "-" + spDate.getDate();
        newDate = NewDate(sendDate);
        month = newDate.getMonth() + 1;
        if((newDate.getMonth() + 1) < 10 ) {
            month = "0"+ (newDate.getMonth() +1)
        }
        day = newDate.getDate();
        if((newDate.getDate() + 1) < 10) {
            day = "0" + (newDate.getDate());
        }
        date = month + "-" + day;
        return date;
    }


})(window)
//解决IE8 DateBUG
function NewDate(str) {
    str = str.split('-');
    var date = new Date();
    date.setUTCFullYear(str[0], str[1] - 1, str[2]);
    date.setUTCHours(0, 0, 0, 0);
    return date;
}