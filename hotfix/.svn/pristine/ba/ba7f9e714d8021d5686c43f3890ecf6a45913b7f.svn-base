function GySetDate(opt){
        //elem
        var targets = opt.targets.split(',');
        this.eYear = this.getId(targets[0].slice(1));
        this.eMonth = this.getId(targets[1].slice(1));
        this.eDay = this.getId(targets[2].slice(1));
        if(!this.eYear||!this.eMonth||!this.eDay) return;
        //范围值

        var r = opt.range.indexOf(','),
            aStarts = opt.range.slice(0,r).split('-'), // 转为：['2013','05','20']
            aEnds = opt.range.slice(r+1,opt.range.length).split('-'); // 转为：['2018','08','20']
        //Number类型
        this.startYear = parseInt(aStarts[0],10);
        this.startMonth = parseInt(aStarts[1],10);
        this.startDay = parseInt(aStarts[2],10);
        this.endYear = parseInt(aEnds[0],10);
        this.endMonth = parseInt(aEnds[1],10);
        this.endDay = parseInt(aEnds[2],10);

        this.init();
        var valueLength = 0;
        (opt.value) && (valueLength = opt.value.split('-'))
        if (opt.value && valueLength.length > 2) {
            this.setSelectChecked(this.eYear, valueLength[0]);
            this.setSelectChecked(this.eMonth, valueLength[1]);
            this.setSelectChecked(this.eDay, valueLength[2]);
        }
    }
    GySetDate.prototype = {
        init:function(){
            var _that = this;
            // 初始化日期
            this.setYears({'start':this.startYear,'end':this.endYear});
            this.setMonths({'start':this.startMonth});
            this.setDays({'year':this.startYear,'month':this.startMonth,'start':this.startDay});
            // 年选择
            this.eYear.onchange = function(){
                var year = parseInt(this.value);
                switch(true){
                    case (year == _that.startYear):{
                        _that.setMonths({'start':_that.startMonth});
                        _that.setDays({'year':_that.startYear,'month':_that.startMonth,'start':_that.startDay});
                    };break;
                    case (year == _that.endYear):{
                        _that.setMonths({'start':1,'end':_that.endMonth});
                        if(_that.endMonth>1){
                            _that.setDays({'year':_that.endYear,'month':1,'start':1});
                        }else{
                            _that.setDays({'year':_that.endYear,'month':1,'start':1,'end':_that.endDay});
                        }
                    };break;
                    default:{
                        _that.setMonths({'start':1});
                        _that.setDays({'start':1,'year':year,'month':1});
                    }
                }

            }
            // 月选择
            this.eMonth.onchange = function(){
                var year = parseInt(_that.eYear.options[_that.eYear.selectedIndex].value),
                    month = parseInt(this.value);
                switch(true){
                    case (year==_that.endYear&&month==_that.endMonth):{
                        _that.setDays({'start':1,'year':year,'month':month,'end':_that.endDay});
                    };break;
                    case (year==_that.startYear&&month==_that.startMonth):{
                        _that.setDays({'year':_that.startYear,'month':_that.startMonth,'start':_that.startDay});
                    };break;
                    default:{
                        _that.setDays({'start':1,'year':year,'month':month});
                    }
                }

            }
        },
        /*设置年，月，日
        ----------------------------------
        参数值都为Number类型
        */
        // 参数 {'start':xx,'end':xxx}
        setYears:function(opt){
            this.eYear.innerHTML = '';
             for(var n=opt.start;n<=opt.end;n++){
                this.eYear.add(new Option(n,n));
            }
        },
        // 参数 {'start':xx,'end':xxx}
        // 参数 'end' 为可选，忽略，则开始到12月
        setMonths:function(opt){
            this.eMonth.innerHTML = '';
            var months = opt.end || 12;
            for(var n=opt.start;n<=months;n++){
                if(n<10) n = '0'+n;
               this.eMonth.add(new Option(n,n));
            }
        },
        // 参数 {'start':xx,'year':xxx,'month':xx,'star':xx,'end':xxx}
        // 参数 'end' 为可选，忽略，则开始到本月底（根据月份判断的）
        setDays:function(opt){
             this.eDay.innerHTML = '';
             var days = opt.end || this.getDays(opt.year,opt.month);
             for(var n=opt.start;n<=days;n++){
                if(n<10) n = '0'+n;
                this.eDay.add(new Option(n,n));
             }
        },
        /* 根据 年，月，返回正确的天数，如 2016-2，返回是29天（润年）
        --------------------------------------------------------------
        参数值都为Number类型
        */
        getDays:function(year,month){
             // var aDay = [31,28|29,31,30,31,30,31,31,30,31,30,31];
            // 二月份的天数数据处理
            var FedDays = year%4==0?29:28,
                returnDays = '';
            var month = month<10?month = '0'+month:month.toString();
            switch(month){
                case '01':
                case '03':
                case '05':
                case '07':
                case '08':
                case '10':
                case '12': returnDays = 31;break;
                case '04':
                case '06':
                case '09':
                case '11': returnDays = 30;break;
                case '02': returnDays = FedDays;break;
            }
            return returnDays;
        },
        /*工具辅助函数
        ----------------------------------
        */
        getId:function(id){
            return document.getElementById(id);
        },
    	setSelectChecked:function(selectEle, checkValue){
		for(var i=0; i<selectEle.options.length; i++){
		//console.log((selectEle.options[i].innerHTML == checkValue))
			if(selectEle.options[i].innerHTML == checkValue){
				selectEle.options[i].selected = true;
				break;
			}
		}
	}
    }