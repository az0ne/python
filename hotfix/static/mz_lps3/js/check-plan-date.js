$(function(){
    var mydate = new Date();
    var thisyear = mydate.getFullYear();
    var thismonth = mydate.getMonth()+1;
    var thisday = mydate.getDate();
    var getArr;

    $.ajax({
        type: 'GET',
        url: '/lps3/student/class/'+ $('#class_id').val() +'/calender/',
        dataType: "json",
        success: function (data){
            if(data.status == true){
                getArr = data.data; // 20160225: "开学日", 20160421: "缺勤", 20160423: "准时", 20160425: "迟到", 20160428: "班会", 20160709: "毕业日"
                initdata();
            }
        }
    });

    $('.check-plan').click(function(){
        if(getArr){
           $('#check-plan').modal('show');
        }
        return false;
    });
    $('#check-plan .close').live('click',function(){
        $('#check-plan').modal('hide');
        return false;
    });

    //日期初始填充
    function initdata(){
        var tdheight = $(".data_table tbody tr").eq(0).find("td").height();

        $(".data_table tbody td").css("height",tdheight);
        $(".selectdate").val(thisyear+"年"+thismonth+"月");
        var days = getdaysinonemonth(thisyear,thismonth);
        var weekday = getfirstday(thisyear,thismonth);


        setcalender(days,weekday,thisyear,thismonth);
    }

    //算某个月的总天数
    function getdaysinonemonth(year,month){
        month = parseInt(month,10);
        var d = new Date(year,month,0);
        return d.getDate();
    }

    //算某个月的第一天是星期几
    function getfirstday(year,month){
        month = month-1;
        var d = new Date(year,month,1);
        return d.getDay();
    }

    //往日历中填入日期
    function setcalender(days,weekday,thisyear,thismonth){
        var a = 1;
        var month = (thismonth < 10) ? ("0"+ thismonth) : thismonth;

        $(".data_table tbody tr td").removeClass("today over start leave regular late meeting");
        $(".data_table tbody tr td span").html("");
        for(var j=0;j<6;j++){
            for(var i=0;i<7;i++){
                if(j == 0 && i<weekday){
                    $(".data_table tbody tr").eq(0).find("td").eq(i).children('span').html("");
                    $(".data_table tbody tr").eq(0).find("td").eq(i).removeClass("usedate");
                }else{
                    if(a<=days){
                        var day = (a < 10) ? ("0"+ a) : a;
                        var str = thisyear + ""+ month +""+ day; //20160225
                        var type = getArr[str]; //状态 开学日
                        switch (type){
                            case '毕业日':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("over");
                            break;
                            case '开学日':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("start");
                            break;
                            case '缺勤':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("leave");
                            break;
                            case '正常出席':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("regular");
                            break;
                            case '迟到':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("late");
                            break;
                            case '班会':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("meeting");
                            break;
                            case '今天':
                                $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(1).html(type);
                                $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("today");
                            break;
                        }
                        $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').eq(0).html(a); // 1-30
                        $(".data_table tbody tr").eq(j).find("td").eq(i).addClass("usedate");
                        a++;
                    }else{
                        $(".data_table tbody tr").eq(j).find("td").eq(i).children('span').html("");
                        $(".data_table tbody tr").eq(j).find("td").eq(i).removeClass("usedate");
                        a = days+1;
                    }
                }
            }
        }
    }

    //上一个月
    $(".lastmonth").click(function(){
        thismonth--;
        if(thismonth == 0){
            thismonth = 12;
            thisyear--;
        }
        initdata();
    });

    //上一个月
    $(".nextmonth").click(function(){
        thismonth++;
        if(thismonth == 13){
            thismonth = 1;
            thisyear++;
        }
        initdata();
    });
});
