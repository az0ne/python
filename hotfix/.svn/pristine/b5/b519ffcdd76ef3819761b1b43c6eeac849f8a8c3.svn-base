Array.prototype.remove = function(s) {   
    for (var i = 0; i < this.length; i++) {   
        if (s == this[i]){   
            this.splice(i, 1);   
		}
    }   
};
Array.prototype.insert = function (index, item) {
  this.splice(index, 0, item);
};
Array.prototype.quickSort=function() {
		var i = 0;
		var j = this.length - 1;
		var el=this;
		var Sort = function(i, j) {
	
			// 结束条件
			if (i == j) {
				return
			};
	
			var key = el[i];
			
			var stepi = i; // 记录开始位置
			var stepj = j; // 记录结束位置
			while (j > i) {
				// j <<-------------- 向前查找
				if (el[j] >= key) {
					j--;
				} else {
					el[i] = el[j]
					//i++ ------------>>向后查找
					while (j > ++i) {
						if (el[i] > key) {
							el[j] = el[i];
							break;
						}
					}
				}
			}
	
			// 如果第一个取出的 key 是最小的数
			if (stepi == i) {
				Sort(++i, stepj);
				return;
			}
			
			// 最后一个空位留给 key
			el[i] = key;
			
			// 递归
			Sort(stepi, i);
			Sort(j, stepj);
		}
		Sort(i, j);
	
		return el;
	}
String.prototype.replaceAll  = function(s1,s2){
    return this.replace(new RegExp(s1,"gm"),s2);
}
Date.prototype.diff = function(date){
  return Math.floor(this.getTime() - date.getTime())/(24 * 60 * 60 * 1000);
}
Date.prototype.dimm = function(date){
	var bMonth=date.getFullYear()*12+date.getMonth();
	var eMonth=this.getFullYear()*12+this.getMonth();
  return Math.abs(eMonth-bMonth);
}
function Map() {   
    
    this.keys = new Array();   
    
    this.data = new Object();   
     
    this.put = function(key, value) {   
        if(this.data[key] == null){   
            this.keys.push(key);   
        }   
        this.data[key] = value;   
    };   
     
    this.get = function(key) {   
        return this.data[key];   
    };   
      
    this.remove = function(key) {   
        this.keys.remove(key);   
        this.data[key] = null;   
    };  
	 
    this.each = function(fn){   
        if(typeof fn != 'function'){   
            return;   
        }   
        var len = this.keys.length;   
        for(var i=0;i<len;i++){   
            var k = this.keys[i];   
            fn(k,this.data[k],i);   
        }   
    };   
      
    this.entrys = function() {   
        var len = this.keys.length;   
        var entrys = new Array(len);   
        for (var i = 0; i < len; i++) {   
            entrys[i] = {   
                key : this.keys[i],   
                value : this.data[i]   
            };   
        }   
        return entrys;   
    };   
        
    this.isEmpty = function() {   
        return this.keys.length == 0;   
    };   
      
    this.size = function(){   
        return this.keys.length;   
    };   
       
    this.toString = function(){   
        var s = "{";   
        for(var i=0;i<this.keys.length;i++,s+=','){   
            var k = this.keys[i];   
            s += k+"="+this.data[k]+"|";   
        }   
        s+="}";   
        return s;   
    };   
};
//页面url
function changeURLPar(destiny, par, par_value)
{
	var pattern = par+'=([^&]*)';
	var replaceText = par+'='+par_value;

	if (destiny.match(pattern))
	{
		var tmp = new RegExp(par+'=[^&]*');
		tmp = destiny.replace(tmp, replaceText);
		return (tmp);
	}
	else
	{
		if (destiny.match('[\?]'))
		{
			return destiny+'&'+ replaceText;
		}
		else
		{
			return destiny+'?'+replaceText;
		}
	}
	return destiny+'\n'+par+'\n'+par_value;
} 
function getQueryUrl(url) {
	if(url) {
		url=url.substr(url.indexOf("?")+1); 
	}
	var result = {},queryString =url || location.search.substring(1), re = /([^&=]+)=([^&]*)/g, m;
	while (m = re.exec(queryString)) { 
		result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]); 
	}
	return result;
}
function DataBinder( object_id ) {
	// Create a simple PubSub object
	var pubSub = {
		callbacks: {},

		on: function( msg, callback ) {
			this.callbacks[ msg ] = this.callbacks[ msg ] || [];
			this.callbacks[ msg ].push( callback );
		},

		publish: function( msg ) {
			this.callbacks[ msg ] = this.callbacks[ msg ] || [];
			for ( var i = 0, len = this.callbacks[ msg ].length; i < len; i++ ) {
				this.callbacks[ msg ][ i ].apply( this, arguments );
			}
		}
	},

	data_attr = "data-" + object_id,
	message = object_id + ":change",

	changeHandler = function( evt ) {
		var target = evt.target || evt.srcElement, // IE8 compatibility
		prop_name = target.getAttribute(data_attr);

		if ( prop_name && prop_name !== "" ){
			pubSub.publish( message, prop_name, target.value );
		}
	};

	// Listen to change events and proxy to PubSub
	if ( document.addEventListener ) {
		document.addEventListener( "change", changeHandler, false );
	} else {
		// IE8 uses attachEvent instead of addEventListener
		document.attachEvent( "onchange", changeHandler );
	}

	// PubSub propagates changes to all bound elements
	pubSub.on( message, function( evt, prop_name, new_val ) {
		var elements = document.querySelectorAll("[" + data_attr + "=" + prop_name + "]"),tag_name;
		for ( var i = 0, len = elements.length; i < len; i++ ) {
			tag_name = elements[ i ].tagName.toLowerCase();
			if ( tag_name === "input" || tag_name === "textarea" || tag_name === "select" ) {
				elements[ i ].value = new_val;
			} else {
				elements[ i ].innerHTML = new_val;
			}
		}
	});

	return pubSub;
}

function makeNode(dom,cname,str)  //创建结点函数
{
   str=str||"";
  var newParagraph = document.createElement(dom);  //创建新元素p
  var newText = document.createTextNode(str);   //创建新文本
  newParagraph.appendChild(newText);  //追加一个新的子结点
  newParagraph.className=cname;
  return newParagraph;  //返回该段落
}

function appendBefore(nodeAttr,dom,cname, str)  //前插入函数
{
  var node = nodeAttr;
  var newNode = makeNode(dom,cname,str);
  if(node.parentNode)   //如果存在双亲结点
  {
	 node.parentNode.insertBefore(newNode, node);  //在当前节结点前插入新结点
  }
}

function insertWithin(nodeAttr,dom,cname, str)  //中插入函数
{
  var node = nodeAttr;
  var newNode = makeNode(dom,cname,str);
  node.appendChild(newNode);  //追加一个新的结点
}

function appendAfter(nodeAttr,dom,cname, str)    //后插入函数
{
  var node = nodeAttr;
  var newNode = makeNode(dom,cname,str);
  if(node.parentNode)    //如果存在双亲结点
  {
	 if(node.nextSibling)  //如果存在下一子结点
	 {
		  //前插入子结点
		node.parentNode.insertBefore(newNode, node.nextSibling);
	 }else  //如果没有下一子结点
		 //后追加子结点
	 node.parentNode.appendChild(newNode);
  }
  return newNode;
}
//class操作
function hasClass(obj, cls) {
    return obj.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));
}
function addClass(obj, cls) {
    if (!this.hasClass(obj, cls)) obj.className += " " + cls;
}
function removeClass(obj, cls) {
    if (hasClass(obj, cls)) {
        var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
        obj.className = obj.className.replace(reg, ' ');
    }
}
function toggleClass(obj,cls){
    if(hasClass(obj,cls)){
        removeClass(obj, cls);
    }else{
        addClass(obj, cls);
    }
}

/*  author:laoguoyong,zhouyi
------------------------------
日期三级联动,范围选择
------------------------------
参数
* [String] targets:'#year,#month,#day' ；年，月，日的id
* [String] range:'2013-02-03,2019-09-21'；范围，正确格式为xxxx-xx-xx
*
*/
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
	
	var valueLength=0;
	(opt.value)&&(valueLength=opt.value.split('-'))	
	if(opt.value &&valueLength.length>2){
		this.setSelectChecked(this.eYear,valueLength[0]);
		this.setSelectChecked(this.eMonth,valueLength[1]);
		this.setSelectChecked(this.eDay,valueLength[2]);
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
			if(selectEle.options[i].innerHTML == checkValue){ 			
				selectEle.options[i].selected = true;  
				break;  
			}  
		}  
	}
}

//userModel
function UserVail( uid ) {
	var binder = new DataBinder( uid ),

	user = {
		attributes: {},
		// The attribute setter publish changes using the DataBinder PubSub
		set: function( attr_name, val ) {
			this.attributes[ attr_name ] = val;
			binder.publish( uid + ":change", attr_name, val, this );
		},
		get: function( attr_name ) {
			return this.attributes[ attr_name ];
		},
		_binder: binder
	};
	var inputVail=function(type,dom){
		if(type=='empty'){
			if(isNull(dom.value)){
				return "不能为空";
			}
			else{
				return ;
			}
		}
		function isNull( str ){
			if ( str == "" ) return true;
			var regu = "^[ ]+$";
			var re = new RegExp(regu);
			return re.test(str);
		}
		function checkMobile( s ){
			var regu =/^[1][3][0-9]{9}$/;
			var re = new RegExp(regu);
			if (re.test(s)) {
				return true;
			}else{
				return false;
			}
		}
		function isEmail( str ){
			var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
			if(myReg.test(str)) return true;
			return false;
		}
		function isUser( s ){
			var regu = /[A-Za-z].*[0-9]|[0-9].*[A-Za-z]/;
			var re = new RegExp(regu);
			if (re.test(s)) {
				return true;
			}else{
				return false;
			}
		}
		function checkPhone( strPhone ) {
			var phoneRegWithArea = /^[0][1-9]{2,3}-[0-9]{5,10}$/;
			var phoneRegNoArea = /^[1-9]{1}[0-9]{5,8}$/;
			var prompt = "您输入的电话号码不正确!";
			if( strPhone.length > 9 ) {
				if( phoneRegWithArea.test(strPhone) ){
					return true;
				}else{
					return false;
				}
			}else{
				if( phoneRegNoArea.test( strPhone ) ){
					return true;
				}else{
					return false;
				}
			}
		}
		function isChn(str){
			var regu = /^[\u4E00-\u9FA5]+$/;
			var re = new RegExp(regu);
			if(!re.test(str)){
				return false;
			}
			else
				return true;
		}
		function isJ(str){
			var filterString = "";
			filterString = filterString == "" ? "'~`·!$%^&*()<>+/" : filterString;
			var ch;
			var i;
			var temp;
			var error = false;
			for (i = 0; i <= (filterString.length - 1); i++) {
				ch = filterString.charAt(i);
				temp = str.indexOf(ch);
				if (temp != -1) {
					error = true;
					break;
				}
			}
			return error;
		}
		function numL(str,n1,n2){
			if(str.length>=n1&&str.length<=n2){
				return true;
			}
			else{
				return false;
			}
		}
		function isName(str,url,obj,str2){
			var rondomStr1 = Math.round(Math.random()*10000);
			//$.ajax({
//				type: "GET",
//				dataType: "text",
//				url: url+str+"&rondomStr="+rondomStr1,
//				success: function(data){
//					if(data == "not"){
//						verr(obj,str2);
//					}
//					else{
//						vrig(obj);
//					}
//				},
//				error: function (XMLHttpRequest, textStatus, errorThrown) {
//					verr(obj,str2);
//				}
//			});

		}
	}
	// Subscribe to the PubSub
	binder.on( uid + ":change", function( evt, attr_name, new_val, initiator ) {
		var elements = document.querySelectorAll("[data-vail="+attr_name+"]");
		for ( var i = 0, len = elements.length; i < len; i++ ) {
			if(i==0){elements[0].parentNode.style.position="relative";}
			var vtype=elements[i].getAttribute("data-vail-type");
			vtype=vtype||"";vtype=vtype.split(" ");
			for(var j=0,jlen=vtype.length;j<jlen;j++){
				var meg=inputVail(vtype[j],elements[i]);
				if(meg){
					if(elements[i].nextSibling&&elements[i].nextSibling.className.indexOf("showMeg")>-1){
						elements[i].nextSibling.className="showMeg errorFont";
					}
					else{
						var node=appendAfter(elements[i],"span","showMeg errorFont","");
						node.style.top=elements[i].offsetTop;
						node.style.left=(elements[i].offsetLeft+elements[i].offsetWidth+8)+"px";
					}
					addClass(elements[i],"errorInput");
					return ;
				}else{
					if(elements[i].nextSibling&&elements[i].nextSibling.className.indexOf("showMeg")>-1){

						elements[i].nextSibling.className="showMeg rightFont";
					}
					else{
						var node=appendAfter(elements[i],"span","showMeg rightFont","");
						node.style.top=(elements[i].offsetTop+elements[i].offsetHeight/2-10)+"px";
						node.style.left=(elements[i].offsetLeft+elements[i].offsetWidth+4)+"px";
					}
					removeClass(elements[i],"errorInput");
				}
			}
		}
		if ( initiator !== user ) {
			user.set( attr_name, new_val );
		}
	});

	return user;
}