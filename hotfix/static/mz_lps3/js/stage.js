var zypoint=function(x,y){
	this.x=x;this.y=y;
}
var zyline=function(startP,endP){
	this.startX=startP.x;
	this.startY=startP.y;
	this.endX=endP.x;
	this.endY=endP.y;
	this.length=function(){
		return Math.sqrt(Math.pow(this.endX-this.startX,2)+Math.pow(this.endY-this.startY,2));
	}
	this.isVC=function(){//false横
		if(Math.abs(this.endX-this.startX)>Math.abs(this.endY-this.startY)){
			return false;
		}
		else{
			return true;
		}
	}
}
function getElementsClass(classnames){ 
	var classobj= new Array();
	var classint=0;
	var tags=document.getElementsByTagName("*");
	for(var i in tags){
		if(tags[i].nodeType==1){
			if(tags[i].getAttribute("class")&&tags[i].getAttribute("class").indexOf(classnames)>-1){ 
				classobj[classint]=tags[i]; 
				classint++; 
			} 
		} 
	} 
	return classobj;
} 
var slots={},c=getElementsClass("loadingProgress"),ctx=[],draw = [];
window.hasLoaded=[];
for(var j=0;j<100;j++){
	window.hasLoaded.push(0);
}
window.loading = false;
window.ulp = ulp;  
for(var i=0;i<c.length;i++){
	ctx.push(c[i].getContext('2d'));
}

function ulp(percent,num){
	window.loading = true;
	var i = 0;
	draw.push(setInterval(function(){
		if (window.hasLoaded[num] > 100) {
			window.loading = false;
			clearInterval(draw);
			draw = null;
			return true;
		}
		if (i<=percent) {
			d(num);
			i++;
			window.hasLoaded[num] += 1;
		} else {
			clearInterval(draw[num]);
			draw[num] = null;
		}
	}, 20));
}

function d(num){
	var lp = getElementsClass("loadedNum")[num];
	lp.innerHTML = window.hasLoaded[num]+"%";
	var loaded = window.hasLoaded[num] * 2 / 100 * Math.PI, cw = 70, hcw = 70;
	
	ctx[num].clearRect (0,0,cw,cw);
	ctx[num].beginPath();
	ctx[num].arc(hcw,hcw,hcw-3, 0, loaded, false);
	ctx[num].lineWidth = 6;
	ctx[num].strokeStyle = '#5ecfba';
	ctx[num].stroke();
}

var ts=[];
function timer(n){    
	var nts=ts[n];
	var dd = parseInt(nts / 60 / 60 / 24, 10);
	var hh = parseInt(nts / 60 / 60 % 24, 10);
	var mm = parseInt(nts / 60 % 60, 10);
	//var ss = parseInt(ts / 1000 % 60, 10);
	dd = checkTime(dd);  
	hh = checkTime(hh);  
	mm = checkTime(mm);  
	//ss = checkTime(ss);  		
	$(".studying").eq(n).find(".t").html(dd + "天" + hh + "时" + mm + "分"); 
	ts[n]-=1;
	if(ts[n]<0) return;
	//setTimeout(timer,1000); 
}  
function checkTime(i){    
   if (i < 10) {    
	   i = "0" + i;    
	}    
   return i;    
}   