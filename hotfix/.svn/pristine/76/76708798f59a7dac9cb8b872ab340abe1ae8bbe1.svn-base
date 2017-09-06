$(function(){
    // ScrollCalendar({
    //     startTime:start_time,
    //     endTime:end_time,
    //     dateLi:'.onlineBox .calenDar li',
    //     arrowLeft:'.arrL',
    //     arrowRight:'.arrR'
    // });

    /*
     ****动态计算日历中元素的宽度
     * defaultW最小宽度（默认的）
     * defaultEle外面div的最小值
     * defaultUl内容区ul的最小值
     * defaultLi日历区li的最小值
     * defaultTime左边时刻表的最小值
     * defaultSpan内容区格子span的最小值
     * defaultCalP日历区外层div的padding的最小值
     */
    // var defaultW = 1280,
    //     defaultEle = 783,
    //     defaultUl = 741,
    //     defaultLi = 93,
    //     defaultTime = 81,
    //     defaultSpan = 94,
    //     defaultMargin = 3,
    //     defaultCalP = 40;
    // calculativeCellWidth(defaultW,defaultEle,defaultUl,defaultLi,defaultTime,defaultSpan,defaultMargin,defaultCalP);
    // $(window).resize(function(){
    //     calculativeCellWidth(defaultW,defaultEle,defaultUl,defaultLi,defaultTime,defaultSpan,defaultMargin,defaultCalP);
    // });

    if (is_employment_contract == 'True' && is_pop_complete_resume == 'True') {
        //完善我的简历
        perfectMyResume();
    }

    //textAreaBox();



    // $('.oto-tab-box .onLineInfo .state').on({'click':function(){
    //     popupMsg($('#oto-order'));

    //     var spanIndex,liIndex,getDateText,getDateTime,getTime,getDay,startTime,endTime,thisYear,str,this_id = $(this).parent().attr('id');
    //         thisYear = (new Date()).getFullYear();

    //         spanIndex = $(this).parent().index();
    //         liIndex = $(this).parents('li').index();


    //         getDateText = $('.oto-tab-box .calenDar li').eq(spanIndex).find('span').text();
    //         getDateTime = (getDateText.replace(/[^0-9]/ig,"-")).substring(0,getDateText.length-1);
    //         getDay = $('.oto-tab-box .calenDar li').eq(spanIndex).find('strong').text();
    //         getTime = $('.oto-tab-box .onLineInfo li').eq(liIndex).find('.time');
    //         startTime = getTime.children('.start').text();
    //         endTime = getTime.children('.end').text();

    //     if(getDateTime.length<=6){
    //         getDate = thisYear+'-'+getDateTime;
    //     }

    //     $.ajax({
    //         type: "GET",
    //         url: "/lps4/ajax_onevone_datelist/" + career_id + "/",
    //         success: function (data) {
    //             var _data = data['data']['data'], t_data, is_select;
    //             str = '';
    //             for (var i=0; i<_data.length; i++) {
    //                 t_data = _data[i];
    //                 if (this_id == t_data["m_id"]) {
    //                     is_select = ' selected=true'
    //                 } else {
    //                     is_select = ''
    //                 }
    //                 str += '<option value="'+ t_data["m_id"] + '"' + is_select + '>' + t_data["m_time"] +'(周'+ t_data["m_day"] +' '+ t_data["m_date"] +')</option>';

    //             }
    //             $('#orderTime').empty().append(str);
    //         }
    //     });



    // }},".appoin a");



    //1v1直播约课
    //yueKeNextStep();

    //确认预约
    //confirmYuye();

});

// function calculativeCellWidth(defaultW,defaultEle,defaultUl,defaultLi,defaultTime,defaultSpan,defaultMargin,defaultCalP){
//     var baseNum = parseInt(($(window).width() - defaultW)/8);
//     if(baseNum<=0){
//         baseNum = 0;
//     }
//     otoDiv = $('.ono-to-one .oto-line');
//     otoDiv.find('.onlineBox,.calenDar').css('width',defaultEle + 8 * baseNum);
//     otoDiv.find('.calenDar').css('padding-left',defaultCalP + baseNum);
//     otoDiv.find('.calenDar li').css('width',defaultLi + baseNum);
//     otoDiv.find('.onLineInfo').css('width',defaultUl + 8 * baseNum);
//     otoDiv.find('.time').css('width',defaultTime + baseNum);
//     otoDiv.find('.state>span').css('width',defaultSpan + baseNum);
//     otoDiv.find('.time>span').css('margin','0 '+(defaultMargin + parseInt(baseNum/8))+'px');
// }


// function ajaxContentFun($dateli,thisyear){
//     var backvalue = 0;
//     var oLi = $('.onLineInfo li');
//     var spans,starttime=[],endtime=[];
//     for(var i=0;i<oLi.length;i++){
//         spans = $(oLi[i]).find('.state span');
//         starttime[i] = $(oLi[i]).find('.time .start').text();
//         endtime[i] = $(oLi[i]).find('.time .end').text();
//         for(var j=0;j<7;j++){
//             var datetxt = $dateli.eq(j).find('span').text();
//                 dates = datetxt.replace(/[^0-9]/ig,"-");
//                 dates=dates.substring(0,dates.length-1);
//             if(dates.length<=6){
//                 dates = thisyear+'-'+dates;
//             }
//
//             //spans.eq(j).html(dates+' '+starttime[i]+'-'+endtime[i]);
//         }
//     }
// }


// function format_number(number) {
//     return parseInt(number) < 10 ? '0' + number : number;
// }

// function ajaxContentFun($dateli, thisyear) {
//     var oLi = $('.onLineInfo li');
//     var cLi = $('.calenDar li');
//     var spans, dates, starttime = [], endtime = [], timelist = [], datelist = [];
//     for (var i = 0, leni = oLi.length; i < leni; i++) {
//         starttime[i] = $(oLi[i]).find('.time .start').text();
//         endtime[i] = $(oLi[i]).find('.time .end').text();
//         timelist[i] = starttime[i] + '-' + endtime[i];
//         if (datelist.length < cLi.length) {
//             for (var j = 0, lenj = cLi.length; j < lenj; j++) {
//                 var datetxt = $dateli.eq(j).find('span').text();
//                 dates = datetxt.replace(/[^0-9]/ig, "-");
//                 dates = dates.substring(0, dates.length - 1);
//                 if (dates.length <= 6) {
//                     dates = thisyear + '-' + dates;
//                 }
//                 var _dates = [];
//                 $(dates.split('-')).each(function (index, ele) {
//                     _dates.push(format_number(ele))
//                 });
//                 dates = _dates[0] + '-' + _dates[1] + '-' + _dates[2];
//                 datelist[j] = dates
//             }
//         }
//     }

//     var _date, _time, spanId, lInfo = $('.onLineInfo');
//     $.ajax({
//             type: "POST",
//             url: "/lps4/ajax_onevone_list/" + career_id + "/",
//             data: {
//                 'timelist': timelist,
//                 'datelist': datelist
//             },
//             dataType: "json",
//             success: function (data) {
//                 for (var i = 0, leni = oLi.length; i < leni; i++) {
//                     spans = $(oLi[i]).find('.state span');
//                     _time = timelist[i];
//                     for (var j = 0; j < 7; j++) {
//                         _date = datelist[j];
//                         spanId = spans.eq(j).attr("id");

//                         var _data = data['data'][_time][_date];
//                         var url = '/lps4/student_service/' + career_id + '/?detail=' + _data['id'];
//                         switch (_data['status']) {
//                             case 0:
//                                 lInfo.find(spans).eq(j).attr('class', '').html('');
//                                 break;
//                             case 1:
//                                 lInfo.find(spans).eq(j).attr('class', '').html('');
//                                 break;
//                             case 2:
//                                 lInfo.find(spans).eq(j).attr('class', 'appoin').attr('id', _data['id']).html('<a href="javascript:;">预约</a>');
//                                 break;
//                             case 3:
//                                 lInfo.find(spans).eq(j).attr('class', '').html('已被预约');
//                                 break;
//                             case 4:
//                                 lInfo.find(spans).eq(j).attr('class', 'enter').html('<a href="' + url + '&status=enter">进入</a>');
//                                 break;
//                             case 5:
//                                 lInfo.find(spans).eq(j).attr('class', 'review').html('<a href="' + url + '&status=review">回看</a>');
//                                 break;
//                         }
//                     }
//                 }
//             }
//         }
//     );
// }

/*
 * @ 提示弹窗
 */
function popupMsg(obj){
    obj.modal({show:true, keyboard:false,backdrop: 'static'});
    $('.close').on('click', function(){
        obj.modal('hide');
    });
};

/*
 * @ 1v1直播约课
 */
// function yueKeNextStep(){
//     var $phoneNum = $('#ops-phone-num'),
//         $verification = $('#ops-verification'),
//         $sendVerif = $('#ops-send-verify');
//         telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;

//     $('#oto-order .next').off().on('click',function(){
//         if($phoneNum.val() == '' || null){
//             tipsMsg = '请输入正确的手机号';
//             Tips($phoneNum, tipsMsg);
//         }else if(!telReg.test($phoneNum.val())){sg = '请输入正确的手机号';
//             Tips($phoneNum, tipsMsg);
//         }else if($verification.val() == '' || null){
//             tipsMsg = '手机验证码输入错误，请重试';
//             Tips($verification, tipsMsg);
//         }else{
//             ops_verify();
//         }
//     });
//     $('#ops-send-verify').on('click',function(){
//         if($phoneNum.val() == '' || null){
//             tipsMsg = '请输入正确的手机号';
//             Tips($phoneNum, tipsMsg);
//         }else{
//             if(telReg.test($phoneNum.val())){
//                 sendsms();
//             }else if(!telReg.test($phoneNum.val())){
//                 tipsMsg = '请输入正确的手机号';
//                 Tips($phoneNum, tipsMsg);
//             }
//         }
//     });
//     function sendsms() {
//         $.ajax({
//             type: "POST",
//             url: "/lps4/mobile/sendsms/",
//             data: {
//                 "mobile": $phoneNum.val()
//             },
//             dataType: "json",
//             success: backData,
//             error: function(data){
//                 console.log(data);
//             }
//         });
//     }
//     function backData(data) {
//         if (!data.success) {
//             if (data.data.type){
//                 appointmentFail();
//             }
//             else {
//                 tipsMsg = data.message;
//                 Tips($phoneNum, tipsMsg);
//             }
//         }
//         else {
//             Cuttime($sendVerif, 60);
//         }
//     }
//     function Cuttime(obj, time){
//         var countdown = null;
//         obj.addClass("send").val("重新发送(60s)").attr('disabled', 'disabled');
//         countdown = setInterval(function(){
//             time--;
//             obj.val("重新发送("+time+"s)");
//             if(time <= 0){
//                 clearInterval(countdown);
//                 obj.removeClass("send").val("重新发送").removeAttr('disabled');
//             }
//         },1000);
//     }

//     // $confirmUse.on('click', function(){
//     //     if($phoneNum.val() == '' || null){
//     //         tipsMsg = '请输入正确的手机号';
//     //         Tips($phoneNum, tipsMsg);
//     //     }else if(!telReg.test($phoneNum.val())){
//     //         tipsMsg = '请输入正确的手机号';
//     //         Tips($phoneNum, tipsMsg);
//     //     }else if($verification.val() == '' || null){
//     //         tipsMsg = '手机验证码输入错误，请重试';
//     //         Tips($verification, tipsMsg);
//     //     }else{
//     //         verifyCaptcha();
//     //     }
//     // });
//     // $sendVerif.on('click', function(){
//     //     if($phoneNum.val() == '' || null){
//     //         tipsMsg = '请输入正确的手机号';
//     //         Tips($phoneNum, tipsMsg);
//     //     }else{
//     //         if(telReg.test($phoneNum.val())){
//     //             sendsms();
//     //         }else if(!telReg.test($phoneNum.val())){
//     //             tipsMsg = '请输入正确的手机号';
//     //             Tips($phoneNum, tipsMsg);
//     //         }
//     //     }
//     // });
//     // function verifyCaptcha() {
//     //     $.ajax({
//     //         type: "POST",
//     //         url: "/lps4/order_onevone_meeting/",
//     //         data: {
//     //             "mobile": $("#phone-num").val(),
//     //             "mobile_code": $("#verification").val(),
//     //             "career_id":career_id,
//     //             "meeting_id":$meeting_id
//     //
//     //         },
//     //         dataType: "json",
//     //         success: function (data) {
//     //             if (data.success) {
//     //                 appointmentStep();
//     //             } else {
//     //                 if (data.data.type){
//     //                     appointmentFail();
//     //                 }
//     //                 else {
//     //                     tipsMsg = data.message;
//     //                     Tips($verification, tipsMsg);
//     //                 }
//     //             }
//     //         },
//     //     });
//     // };


// }

// function ops_verify() {
//     var $verification = $('#ops-verification'),tipsMsg;
//     $.ajax({
//         type: "POST",
//         url: "/lps4/order_onevone_meeting/",
//         data: {
//             "time" : $("#orderTime").val(),
//             "mobile": $("#ops-phone-num").val(),
//             "mobile_code": $("#oto-order .verification").val(),
//             "career_id":career_id
//         },
//         dataType: "json",
//         success: function (data) {
//             if (data.success) {
//                 $('.oto-order-form').css({'visibility':'hidden','z-index':'0'});
//                 $('.tabBox').css('height','370px');
//                 $('.oto-order-content').addClass('show');
//             } else {

//                 tipsMsg = data.message;
//                 Tips($verification, tipsMsg);
//             }
//         }
//     });
// };


// function confirmYuye(){
//     var $ordercontent = $('#oto-order .oto-order-content');
//     var uediter = UE.getEditor('onevone_ueditor');
//     uediter.addListener('keyup focus',function(){
//         var strContentadd = uediter.getContent();
//          if(uediter.getContentTxt().length > 14 || uediter.getContentTxt().length < 1001){
//              $ordercontent.find('.textErr').text('');
//          }
//     });
//     $ordercontent.find('.submitBtn').on('click',function() {
//         var strContentadd = uediter.getContent();
//         if(strContentadd == "" || uediter.getContentTxt().length < 15 || uediter.getContentTxt() == '请输入你的疑问，已便于老师为你更好的解答（不少于15字）'){
//             $ordercontent.find('.textErr').text('输入的问题不能为空/输入问题不能低于15字');
//         }else if(uediter.getContentTxt().length >1000){
//             $ordercontent.find('.textErr').text('输入问题不能大于1000字');
//         }else{
//             $ordercontent.find('.textErr').text('');
//             $('#oto-order .select-title').removeClass('Error');
//             $('#oto-order .selectErr').text('');
//             $.ajax({
//                 url: "/lps4/ajax_date_onovone_meeting/"+$('#orderTime').val()+"/",
//                 type: 'POST',
//                 data: {
//                     "mobile": $("#ops-phone-num").val(),
//                     "career_id": career_id,
//                     'content': strContentadd
//                 },
//                 success: function(data){
//                     if(data.success){
//                         $ordercontent.find('.tip2').removeClass('err').addClass('suc').text('预约成功');
//                         window.location.href = '/lps4/student_service/' + career_id + '/?m=true';
//                     }else{
//                         $('#oto-order .select-title').addClass('Error');
//                         $('#oto-order .selectErr').text(data['message']);

//                         $ordercontent.find('.tip2').removeClass('suc').addClass('err').text('预约失败，请重新点击确认');
//                     }
//                 }
//             });
//         }
//     });
// }


/*
 * @ 提示完善我的简历
 */
function perfectMyResume() {
    $('#perfectMyResume').modal('show');
    if (is_force_pop_complete_resume == 'True') {
        $('#perfectMyResume .close').remove();
    }
    else {
        $('#perfectMyResume .close').on('click', function () {
            $('#perfectMyResume').modal('hide');
        });
    }
}

/*
 * @ 文本框--副文本
 */
// function textAreaBox(){
//     var ue = createUE("onevone_ueditor");
//     ue.ready(function() {
//         ue.setContent('<p style="color: #7a7a7a;font-size: 14px;font-family: "Microsoft Yahei";">请输入你的疑问，已便于老师为你更好的解答（不少于15字）</p>');
//     });
//     (ue).addListener('focus',function(){
//         if(ue.getContentTxt() == '请输入你的疑问，已便于老师为你更好的解答（不少于15字）'){
//             ue.setContent('');
//         }
//     });
//     function createUE(name){
//         return UE.getEditor(name,{
//             toolbars:[['simpleupload']],
//             autoClearinitialContent: true,
//             autoFloatEnabled: false,
//             wordCount: false,
//             elementPathEnabled: false,
//             initialFrameHeight: 170,
//             initialFrameWidth:720,
//             imagePopup:false,
//             maximumWords:1000,
//             autoHeightEnabled:false,
//             initialStyle:'p{color: #7a7a7a;font-size: 14px;line-height:1.2em;font-family: Microsoft Yahei;}img{max-width:100%;}'
//         });
//     };
// }