/* 
* Author:验收时间
* Date：2014-4-26
*/
(function($) {
	$.fn.valid = function(iSet) {
		iSet = $.extend({
			selectBoxCls: 'i_selectbox'
		}, iSet || {});
		/*empty为空,js防止注入，email邮箱，phone手机，tph电话，pwd密码，rep重复密码,num长度*/
		var pwd="";
		var orbo=true;
		this.each(function() {
			var th=$(this);
			$(this).find("input[type=text],input[type=password],textarea").each(function(index, element) {
				$(this).blur(function(){
						if($(this).attr("valid").indexOf('empty')>-1){
						  	if(isNull($(this).val())){
								verr($(this),"不能为空");
								txt=false;
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('js')>-1&&!$(this).hasClass("validerror")){
						  	if(isJ($(this).val())){
								verr($(this),"禁止特殊符号");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('num')>-1){
							if($(this).attr("num").length>0){
								var n1=parseInt($(this).attr("num").split("-")[0],10);
								var n2=parseInt($(this).attr("num").split("-")[1],10);

								if(!numL($(this).val(),n1,n2)){
									verr($(this),"请输入"+n1+"~"+n2+"个字");
								}
								else{
									vrig($(this));
								}
							}
						}
						if($(this).attr("valid").indexOf('pwd')>-1&&!$(this).hasClass("validerror")){
							pwd=$(this).val();
						}
						if($(this).attr("valid").indexOf('rep')>-1&&!$(this).hasClass("validerror")){
							if(pwd!=$(this).val()){
								verr($(this),"密码不一致");
							}
						}
						if($(this).attr("valid").indexOf('email')>-1&&!$(this).hasClass("validerror")){
						  	if(!isEmail($(this).val())){
								verr($(this),"邮箱格式不正确");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('tph')>-1&&!$(this).hasClass("validerror")){
						  	if(!checkPhone($(this).val())){
								verr($(this),"电话号码不正确");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('uu')>-1&&!$(this).hasClass("validerror")){
						  	if(!isUser($(this).val())){
								verr($(this),"密码必须包含字母数字");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('valiname')>-1&&!$(this).hasClass("validerror")){
							
						  	isName($(this).val(),$(this).attr("url"),$(this),$(this).attr("mess")+"已经存在");
							
						}
					
				});
            	
            });
			$(this).find("select").each(function(index, element) {
				$(this).change(function(){
					if($(this).attr("valid")!=undefined){
						if($(this).attr("valid").indexOf('select')>-1){
							
							if($(this).val()==""||$(this).val()=="0"){
								verr($(this),"请选择企业规模");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('nofont')>-1){
							var ggg=$(this).val();
							if($(this).val()==""){
								verr($(this),"");
							}
							else{
								
							}
						}
					}
				});
				$(this).blur(function(){
					if($(this).attr("valid")!=undefined){
						if($(this).attr("valid").indexOf('select')>-1){
							
							if($(this).val()==""||$(this).val()=="0"){
								verr($(this),"请选择企业规模");
							}
							else{
								vrig($(this));
							}
						}
						if($(this).attr("valid").indexOf('nofont')>-1){
							var ggg=$(this).val();
							if($(this).val()==""){
								verr($(this),"请选择市县区");
							}
							else{
								
							}
						}
					}
				});
			});
			
			$(this).find("input").filter('input:submit').each(function(index, element) {				
				th.submit(function(){
					orbo=true;
					th.find("input[type=text],input[type=password],textarea").trigger("blur");
					th.find("select").trigger("blur");
					th.find("input[type=text],input[type=password],textarea").each(function(index, element) {
						if($(this).hasClass("validerror")){
							orbo=false;
						}
					});
					th.find("select").each(function(index, element) {
						if($(this).hasClass("validerror")){
							orbo=false;
						}
					});
					if(orbo){
						return true;
					}
					else{
						return false;
					}
				});
			});
			
		});
		function verr(th,str){
			th.addClass("validerror");
			if(!(th.parent().find("span").length>0)){
				th.parent().append("<span class='verror'>"+str+"</span>");
				
			}
			else{
				th.parent().find("span").remove();
				th.parent().append("<span class='verror'>"+str+"</span>");
			}
		}
		function vrig(th){
			th.removeClass("validerror");
			if(!(th.parent().find("span").length>0)){
				
				th.parent().append("<span class='vright'></span>");
			}
			else{
				th.parent().find("span").remove();
				th.parent().append("<span class='vright'></span>");
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
			$.ajax({
				type: "GET",
				dataType: "text",
				url: url+str+"&rondomStr="+rondomStr1,
				success: function(data){
					if(data == "not"){
						verr(obj,str2);
					}
					else{
						vrig(obj);
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					verr(obj,str2);
				}
			});

		}
		
		return this;
	};
})(jQuery);