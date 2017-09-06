var selectedSpanArry = [],selectedIdArry = [];
$(function(){
    $(".teacherICO").on("mouseover",function(){
        layer.tips($(this).attr("title"), $(this), {
          tips: [1, '#333'] //还可配置颜色
        });
    });

    ScrollCalendar({
        // startTime:start_time,
        // endTime:end_time,
        dateLi:'.onlineBox .calenDar li',
        arrowLeft:'.onlineBox .arrL',
        arrowRight:'.onlineBox .arrR'
    });

    $('.onLineInfo .state').on({'click':function(){
        var spanId = $(this).parent().index();
        var liId = $(this).parents('li').index();
        if($(this).parent().hasClass('selected')){
            $(this).parent().removeClass('selected');
            delTimeArry(spanId,liId);
            console.log(selectedSpanArry)
        }else{
            $(this).parent().addClass('selected');
            addTimeArry(spanId,liId);
            console.log(selectedSpanArry)
        }
    }},'a');

    $('.onlineBox .refer .empty').on('click',function(){
        var selects = $('.onLineInfo .state span.selected');
        for(var i=0,len=selects.length;i<len;i++){
            var spanId = selects.eq(i).index();
            var liId = selects.eq(i).parents('li').index();
            delTimeArry(spanId,liId);
        }

        $('.onLineInfo .state span').removeClass('selected');
    });

    $('.onlineBox .refer .confirm.created').on('click',function(){
        var jsonSelectSpanArry =[],jsonSelectSpan =[],times =[],beginTime =[],endTime =[];
        if(selectedSpanArry.length == 0){
            return;
        }
        for(var i= 0,len=selectedSpanArry.length;i<len;i++){
            jsonSelectSpan[i] = selectedSpanArry[i].split(' ');
            times = jsonSelectSpan[i][1].split('-');
            beginTime[i] =  jsonSelectSpan[i][0] + ' '+times[0];
            endTime[i] =  jsonSelectSpan[i][0] + ' '+times[1];

            jsonSelectSpanArry.push(beginTime[i] + '--' +endTime[i])
        }
        $.ajax({
            type: "POST",
            url: "/home/t/ajax_create_onevone/",
            data: {'meeting_list': JSON.stringify(jsonSelectSpanArry)},
            dataType: "json",
            success: function (data) {
                if (data['success']) {
                    window.location.reload()
                }
            }
        });

        console.log(jsonSelectSpanArry)
    });

    $('.onlineBox .refer .confirm.cancel').on('click',function(){
        if(selectedIdArry.length == 0){
            return;
        }

        $.ajax({
            type: "POST",
            url: "/home/t/ajax_del_onevone/",
            data: {'meeting_list': JSON.stringify(selectedIdArry)},
            dataType: "json",
            success: function (data) {
                if (data['success']) {
                    window.location.reload()
                }
            }
        });

        console.log(selectedIdArry)
    });
});

function format_number(number) {
    return parseInt(number) < 10 ? '0' + number : number;
}

function ajaxContentFun($dateli, thisyear, isclick) {
    var oLi = $('.onLineInfo li');
    var cLi = $('.calenDar li');
    var spans, dates, starttime = [], endtime = [], timeArry = [], timelist = [], datelist = [], datesS, starttimeS = [], endtimeS = [];
    for (var i = 0, leni = oLi.length; i < leni; i++) {
        starttime[i] = $(oLi[i]).find('.time .start').text();
        endtime[i] = $(oLi[i]).find('.time .end').text();
        timelist[i] = starttime[i] + '-' + endtime[i];
        if (datelist.length < cLi.length) {
            for (var j = 0, lenj = cLi.length; j < lenj; j++) {
                var datetxt = $dateli.eq(j).find('span').text();
                dates = datetxt.replace(/[^0-9]/ig, "-");
                dates = dates.substring(0, dates.length - 1);
                if (dates.length <= 6) {
                    dates = thisyear + '-' + dates;
                }
                var _dates = [];
                $(dates.split('-')).each(function (index, ele) {
                    _dates.push(format_number(ele))
                });
                dates = _dates[0] + '-' + _dates[1] + '-' + _dates[2];
                datelist[j] = dates
            }
        }
    }

    var _date, _time, liId, spanId, lCreate = $('.lineCreate'), lRecall = $('.lineRecall');
    $.ajax({
            type: "POST",
            url: "/home/t/ajax_onevone_add_list/",
            data: {
                'timelist': timelist,
                'datelist': datelist
            },
            dataType: "json",
            success: function (data) {
                for (var i = 0, leni = oLi.length; i < leni; i++) {
                    spans = $(oLi[i]).find('.state span');
                    _time = timelist[i];
                    liId = spans.eq(i).attr("id");
                    for (var j = 0; j < 7; j++) {
                        _date = datelist[j];
                        spanId = spans.eq(j).attr("id");
                        if (!isclick) {
                            if (spans.eq(j).hasClass('selected')) {
                                selectedSpanArry.push(dates + ' ' + _time);
                                selectedIdArry.push(spanId);
                            }
                        }
                        var _data = data['data'][_time][_date];
                        switch (_data['status']) {
                            case 0:
                                lCreate.find(spans).eq(j).html('<a href="javascript:;"></a>');
                                lRecall.find(spans).eq(j).html('');
                                break;
                            case 1:
                                lCreate.find(spans).eq(j).html('已结束');
                                lRecall.find(spans).eq(j).html('');
                                break;
                            case 2:
                                lCreate.find(spans).eq(j).html('已创建');
                                lRecall.find(spans).eq(j).attr('id', _data['id']).html('<a href="javascript:;"></a>');
                                break;
                            case 3:
                                lCreate.find(spans).eq(j).html('已创建');
                                lRecall.find(spans).eq(j).html('');
                                break;
                        }
                        // var dl = conversionDate(j, i);
                        // var _a = _data['is_selected'] == 1,
                        //     _b = $.inArray((dl[0] + ' ' + dl[1] + '-' + dl[2]), selectedSpanArry) == -1;
                        // if (_a && lCreate.find(spans).eq(j).html() == '<a href="javascript:;"></a>' && _b) {
                        //     lCreate.find(spans).eq(j).addClass('selected');
                        //     addTimeArry(j, i);
                        // }
                        // if (_a && lRecall.find(spans).eq(j).html() == '<a href="javascript:;"></a>' && _b) {
                        //     lRecall.find(spans).eq(j).addClass('selected');
                        //     addTimeArry(j, i);
                        // }
                    }
                }
            }
        }
    );

    if (isclick) {
        oLi.find('.state .selected').removeClass('selected');

        for (var x = 0, lenx = selectedSpanArry.length; x < lenx; x++) {
            timeArry[x] = selectedSpanArry[x].split(' ');
            for (var i = 0, leni = oLi.length; i < leni; i++) {
                spans = $(oLi[i]).find('.state span');
                starttimeS[i] = $(oLi[i]).find('.time .start').text();
                endtimeS[i] = $(oLi[i]).find('.time .end').text();
                for (var j = 0; j < 7; j++) {
                    var datetxt = $dateli.eq(j).find('span').text();
                    datesS = datetxt.replace(/[^0-9]/ig, "-");
                    datesS = datesS.substring(0, datesS.length - 1);
                    if (datesS.length <= 6) {
                        datesS = thisyear + '-' + datesS;
                    }

                    if (datesS == timeArry[x][0] && (starttimeS[i] + '-' + endtimeS[i]) == timeArry[x][1]) {
                        $(oLi[i]).find('.state span').eq(j).addClass('selected');
                    }
                }
            }
        }
    }
}


function addTimeArry(spanId,liId){
    var dateTimes;
    dateTimes = conversionDate(spanId,liId);
    selectedSpanArry.push(dateTimes[0]+' '+dateTimes[1]+'-'+dateTimes[2]);
    selectedIdArry.push(dateTimes[3]);
}

function delTimeArry(spanId,liId){
    var indexs,dateTimes,indexid;
    dateTimes = conversionDate(spanId,liId);

    var deltimestamp = Date.parse(new Date(dateTimes[0]+' '+dateTimes[1]+'-'+dateTimes[2])) / 1000;
    var arrtimestamp =[];
    for(var i= 0,len = selectedSpanArry.length;i<len;i++){
        arrtimestamp[i] = Date.parse(new Date(selectedSpanArry[i])) / 1000;
    }
    if(arrtimestamp.indexOf(deltimestamp) || arrtimestamp.indexOf(deltimestamp) == 0){
        indexs = arrtimestamp.indexOf(deltimestamp);
        selectedSpanArry.splice(indexs,1);
    }
    if(selectedIdArry.indexOf(dateTimes[3]) || selectedIdArry.indexOf(dateTimes[3]) == 0){
        indexid = selectedIdArry.indexOf(dateTimes[3]);
        selectedIdArry.splice(indexid,1);
    }
}

function conversionDate(spanId,liId){
    var thisyear = new Date().getFullYear();
    var oLi = $('.onLineInfo li');
    var dateLi = $('.onlineBox .calenDar li');
    var starttime,endtime,dates,idVal;
    var datetxt = dateLi.eq(spanId).find('span').text();
        dates = datetxt.replace(/[^0-9]/ig,"-");
        dates=dates.substring(0,dates.length-1);
    if(dates.length<=6){
        dates = thisyear+'-'+dates;
    }
    starttime = oLi.eq(liId).find('.time .start').text();
    endtime = oLi.eq(liId).find('.time .end').text();

    if($('.lineRecall').length){
        idVal = oLi.eq(liId).find('.state span').eq(spanId).attr('id');
    }

    return [dates,starttime,endtime,idVal];
}
