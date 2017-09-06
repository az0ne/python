function ScrollCalendar(options){
	var nowtime = new Date(),
		thisyear = nowtime.getFullYear(),
		thismonth = nowtime.getMonth()+1,
		thisdate = nowtime.getDate(),
		thisday = nowtime.getDay();

	var define = {
        'startTime': GetDateStr(-thisday),
        'endTime': GetDateStr(600),
        'dateLi':'ul li',
        'arrowLeft':'.left',
		'arrowRight':'.right'
    };

    var option = options;
    $.extend(define, options);
    var startDate = new Date(define.startTime || option.startTime);
    var endDate = new Date(define.endTime || option.endTime);

	var days,$dateli,$arrL,$arrR,
	
	$dateli = $(define.dateLi || option.dateLi);
	$arrL = $(define.arrowLeft || option.arrowLeft);
	$arrR = $(define.arrowRight || option.arrowRight);
	//算某个月的总天数
	days = getdaysinonemonth(thisyear,thismonth);
	//当前日期时，显示就近7天的数据
	currentCalender(days,thisyear,thismonth,thisdate,thisday);
	
	/*
	 * 点击向左箭头，时间减少
	 * clickArrow--点击获取相应li的时间值，并做判断是否超出
	 * 如果超出则不允许继续点击
	 * lessCalender--减少时间
	 * ajaxContentFun--加载相应内容
	 */
	$arrL.on('click',function(){
		var firstLi,timestamp;
		firstLi = $dateli.eq(0).find('span').text();
		$('.onlineBox .arrR').css('visibility','visible');
		//获得时间戳
		timestamp = clickArrow(firstLi,startDate);
		var sevenBeforeTimestamp = new Date(timestamp[0]);
		sevenBeforeTimestamp.setDate(sevenBeforeTimestamp.getDate()-7);
		//判断是否小于开始时间
		if(sevenBeforeTimestamp<=timestamp[1]){
			$('.onlineBox .arrL').css('visibility','hidden');
		};
		if(timestamp[0]<=timestamp[1]){
			return;
		};
		//减少时间
		lessCalender(firstLi);
		//执行ajax内容函数
		ajaxContentFun($dateli,thisyear,true);
	});
	
	/*
	 * 点击向右箭头，时间增加
	 * clickArrow--点击获取相应li的时间值，并做判断是否超出
	 * 如果超出则不允许继续点击
	 * addCalender--增加时间
	 * ajaxContentFun--加载相应内容
	 */
	$arrR.on('click',function(){
		var lastLi,timestamp;
		lastLi = $dateli.eq(6).find('span').text();
		$('.onlineBox .arrL').css('visibility','visible');
		//获得时间戳
		timestamp = clickArrow(lastLi,endDate);
		var sevenAfterTimestamp = new Date(timestamp[0]);
		sevenAfterTimestamp.setDate(sevenAfterTimestamp.getDate()+7);

		//判断是否大于结束时间
		if(sevenAfterTimestamp>=timestamp[1]){
			$('.onlineBox .arrR').css('visibility','hidden');
		};
		if(timestamp[0]>=timestamp[1]){
			return;
		};
		//增加时间
		addCalender(lastLi);
		//执行ajax内容函数
		ajaxContentFun($dateli,thisyear,true);
	});

	/*
	 * 算某个月的总天数
	 */
	function getdaysinonemonth(year,month){
	    month = parseInt(month,10);
	    var d = new Date(year,month,0);
	    return d.getDate();
	}
	/*
	 * 判断是否是当天
	 */
	function isToday(date){
	    var today = new Date().toLocaleDateString();
	    var date = new Date(date).toLocaleDateString();
	    return today == date;
	}
	
	/*
	 * 当前日期时，显示就近7天的数据
	 */
	function currentCalender(days,year,month,date,weekday){
		//显示当天日期之前的日期
		for(var i=0;i<weekday;i++){
			if(date - (weekday - i) > 0){
				$dateli.eq(i).find('span').text(month+'月'+(date - (weekday - i))+'日');
			}else{
				if((date - weekday) > 0){
	    			$dateli.eq(i).find('span').text(month+'月'+(days - (date - i))+'日')
	    		}else{
	    			days = getdaysinonemonth(year,(month - 1));
	    			var months = month - 1;
	    			var years = '';
	    			if(months==0){months=12;years = (year-1) + '年';}
	    			$dateli.eq(i).find('span').text(years+months+'月'+(days - ((weekday - date) - i))+'日')
	    		}
			}
		}
		//显示当天日期及之后的日期
		for(var j=weekday;j<7;j++){
			if(j == weekday){
				$dateli.eq(j).addClass('cur');
				$dateli.eq(j).find('span').text(month+'月'+date+'日')
			}else{
				var day = date + (j-weekday);
				if(day > days){
					var months = month + 1;
	    			var years = '';
	    			if(months==13){months=1;years = (year+1) + '年';}
					$dateli.eq(j).find('span').text(years+months+'月'+(day-days)+'日');
				}else{
					$dateli.eq(j).find('span').text(month+'月'+day+'日')
				}
			}
		}

		var firstLi = $dateli.eq(0).find('span').text();
		var lastLi = $dateli.eq(6).find('span').text();
		//获得时间戳
		timestampB = clickArrow(firstLi,startDate);
		timestampA = clickArrow(lastLi,endDate);

		if(timestampB[0]>timestampB[1]){
			$('.onlineBox .arrL').css('visibility','visible');
		};

		if(timestampA[0]<timestampA[1]){
			$('.onlineBox .arrR').css('visibility','visible');
		};

		ajaxContentFun($dateli,thisyear,false);
	}
	
	/*
	 * 点击获取相应li的时间值
	 */
	function clickArrow(getLi,dates){
		var gettimestamp,timestamps,dateCell;
		//得到指定时间的年/月/日
		dateCell = getDateCell(getLi);
		dateCell[1] = (dateCell[1] > 10) ? dateCell[1] : "0"+dateCell[1];
		dateCell[2] = (dateCell[2] > 10) ? dateCell[2] : "0"+dateCell[2];
		//得到指定时间与开始（结束）时间的时间戳
		gettimestamp = Date.parse(new Date(dateCell[0]+'-'+dateCell[1]+'-'+dateCell[2]));
		timestamps = Date.parse(dates);
		//返回指定时间、开始（结束）时间
		return [gettimestamp,timestamps];
	}

	/*
	 * 获取指定li的日期值，并分解成年、月、日，返回相应值
	 */
	function getDateCell(getLis){
		var year,month,dates,getValue,getValueArry;
		getValue = getLis.replace(/[^0-9]/ig,",");
		getValueArry = getValue.split(",");
		//判断获得的值是几个
		if(getValueArry.length > 3){
			year = getValueArry[0];
			month = getValueArry[1];
			dates = getValueArry[2];
		}else{
			year = thisyear;
			month = getValueArry[0];
			dates = getValueArry[1];
		}
		//返回年/月/日
		return [year,month,dates];
	}

	/*
	 * 增加日期
	 */
	function addCalender(getLi){
		var year,month,dates,years,months,datess,newyear,getym;
		//得到指定li的年/月/日
		dateCell = getDateCell(getLi);
		year = dateCell[0];month = dateCell[1];dates = dateCell[2];
		//循环体
		for(var i=0;i<7;i++){
			//判断是否是当前年，并获取年份值；将月份转为数字型
			getym = getYM(year,month);
			years = getym[0];months = getym[1];
			//得到天数
			datess=parseInt(dates)+(i+1);
			if(datess>days){
				datess=datess-days;
				months=months+1;
				if(months == 13){
					months=1;
					newyear = parseInt(year)+1;
					if(newyear == thisyear){
						years = '';
					}else{
						years=newyear+'年';
					}
				}
			}
			//改变li的状态(当天加cur，否则去掉)
			changeClass(i,years,year,months,datess);
		}
		//重新获取月份的总天数
		days = getdaysinonemonth(year,month);
	}

	/*
	 * 减少日期
	 */
	function lessCalender(getLi){
		var year,month,dates,years,months,datess,newyear,getym;
		//得到指定li的年/月/日
		dateCell = getDateCell(getLi);
		year = dateCell[0];month = dateCell[1];dates = dateCell[2];
		//循环体
		for(var i=0;i<7;i++){
			//判断是否是当前年，并获取年份值；将月份转为数字型
			getym = getYM(year,month);
			years = getym[0];months = getym[1];
			//得到天数
			datess=parseInt(dates)-(7-i);
			if(datess<1){
				//重新获取月份的总天数(前一个月)
				days = getdaysinonemonth(year,(month-1));
				datess=datess+days;
				months=months-1;
				if(months == 0){
					months=12;
					newyear = parseInt(year)-1;
					if(newyear == thisyear){
						years = '';
					}else{
						years=newyear+'年';
					}
				}
			}
			//改变li的状态(当天加cur，否则去掉)
			changeClass(i,years,year,months,datess);
		}
	}

	//改变li的状态(当天加cur，否则去掉)
	function changeClass(i,years,year,months,datess){
		$dateli.eq(i).removeClass('cur').find('span').text(years+months+'月'+datess+'日');
		if(isToday(year+'-'+months+'-'+datess)){
			$dateli.eq(i).addClass('cur');
		}
	}
	
	//判断是否是当前年，并获取年份值；将月份转为数字型
	function getYM(year,month){
		var years,months;
		if(year == thisyear){
			years ='';
		}else{
			years=year+'年';
		}
		months=parseInt(month);
		
		return [years,months];
	}

}

/*
 * @ 获取几天前/几天后的时间
 */
function GetDateStr(AddDayCount){
var dd = new Date(), y, m, d;
    dd.setDate(dd.getDate()+AddDayCount);//获取AddDayCount天后的日期
    y = dd.getFullYear();
    m = dd.getMonth()+1;//获取当前月份的日期
	m = (m > 10) ? m : "0"+m;
    d = dd.getDate();
	d = (d > 10) ? d : "0"+d;
    return y+"-"+m+"-"+d;
}