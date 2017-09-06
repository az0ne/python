function Scroll(obj){
	this.insert_location = obj.insert_location  // 轮播添加到什么位置下
	this.switch_time = obj.switch_time || 2000;
	this.imgs = obj.imgs;  //轮播图片信息(包括：链接地址，图片地址，图片alt;格式：[{'href':xxx,'src':xxx,'alt':xxx}])
	this.page_total = obj.imgs.length; //轮播图片数量
	this.current_page = obj.current_page || 0;  // 起始轮播页码
	this.width = obj.width || 1000; // 每一页的宽度
	this.timer1 = null;  // 滚动一页的计时器
	this.timer2 = null;  // 自动滚动一页的计时器
	this.container = null;  // 轮播的主结构
	this.out = null;  // 轮播容器
	this.inner = null;  // 包裹容器
	this.next = null;  // 切换下一张图片按钮
	this.prev = null;  // 切换上一张图片按钮
	this.imgs_index = null;  // 图片集下标
	this.direction = obj.direction || true;  // 控制上下切换图片按钮
	this.index = obj.index || true;  // 控制轮播页下标
}

Scroll.prototype.init = function(){

	//创建框架
	this.container = document.createElement("div");
	this.container.classList.add("lbi-container");
	this.container.style.width = this.width + "px";
	this.out = document.createElement("div");
	this.out.classList.add("lbi-out");
	this.out.style.width = this.width + "px";
	this.inner = document.createElement("div");
	this.inner.classList.add("lbi-inner");
	this.inner.style.width = this.width * (this.page_total+1)+"px";
	this.insert_location.appendChild(this.container).appendChild(this.out).appendChild(this.inner);

	// 创建轮播图片
	for(var i=0;i<this.imgs.length;i++){
		var _a = document.createElement("a");
		_a.href = this.imgs[i].href;
		_a.target = '0';
		var _li = document.createElement("li");
		var _img = document.createElement("img");
		_img.style.width = this.width+"px";
		_img.src = this.imgs[i].src;
		_img.alt = this.imgs[i].alt || "";
		this.inner.appendChild(_a).appendChild(_li).appendChild(_img);
	}
	var _a = document.createElement("a");
	_a.href = this.imgs[0].href;
	_a.target = '0';
	var _li = document.createElement("li");
	var _img = document.createElement("img");
	_img.style.width = this.width+"px";
	_img.src = this.imgs[0].src;
	_img.alt = this.imgs[0].alt || "";
	this.inner.appendChild(_a).appendChild(_li).appendChild(_img);
	
	// 判断是否添加图片上下张切换
	if(this.direction){
		this.next = document.createElement("div");
		this.next.classList.add("switch");
		this.next.classList.add("lbi-next");
		this.prev = document.createElement("div");
		this.prev.classList.add("switch");
		this.prev.classList.add("lbi-prev");
		this.container.appendChild(this.next);
		this.container.appendChild(this.prev);
	}
	
	// 判断是否添加图片下标
	if(this.index){
		this.imgs_index = document.createElement("ul");
		this.imgs_index.classList.add("lbi-imgs-index");
		for(var i=0;i<this.page_total;i++){
			var li = document.createElement("li");
			if(i==0){
				li.classList.add("lbi-current");
			}
			this.imgs_index.appendChild(li);
		}
		this.container.appendChild(this.imgs_index);
	}
	this.autoMove();
}
Scroll.prototype.move = function(n){
	var self = this, step = 0, max_step = 20, start_pos = self.out.scrollLeft,
		end_pos = this.width * n, every = (end_pos-start_pos)/max_step;
	clearInterval(self.timer1);
	self.timer1 = setInterval(function(){
		step++;
		if(step>=max_step){
			clearInterval(self.timer1);
			self.out.scrollLeft = end_pos;
			step = 0;
		}
		start_pos += every;
		self.out.scrollLeft = start_pos;
	},10);
}
Scroll.prototype.autoMove = function(){
	var self = this;
	clearInterval(self.timer2);
	self.timer2 = setInterval(function(){
		self.current_page++;
		if(self.current_page>self.page_total){
			self.current_page = 1;
			self.out.scrollLeft = 0;
		}
		self.move(self.current_page);
		self.current();
	},self.switch_time);
	self.mouseOver();
	self.arrow();
	self.tap();
}
Scroll.prototype.arrow = function(){
	var self = this;
	if(!self.next){
		return;
	}
	self.prev.onclick = function(){
		clearInterval(self.timer1);
		clearInterval(self.timer2);
		self.current_page--;
		if(self.current_page<0){
			self.current_page = self.page_total - 1;
			self.out.scrollLeft = self.width * self.page_total;
		}
		self.move(self.current_page);
		self.current();
		self.autoMove();
	}
	self.next.onclick = function(){
		clearInterval(self.timer1);
		clearInterval(self.timer2);
		self.current_page++;
		if(self.current_page>self.page_total){
			self.current_page = 1;
			self.out.scrollLeft = 0;
		}
		self.move(self.current_page);
		self.current();
		self.autoMove();
	}
}
Scroll.prototype.tap = function(){
	var self = this;
	if(!self.imgs_index){
		return;
	}
	var imgs_index = self.imgs_index.getElementsByTagName("li");
	for(var i=0;i<imgs_index.length;i++){
		imgs_index[i].onclick = function(){
			for(var j=0;j<imgs_index.length;j++){
				imgs_index[j].className = "";
				if(this==imgs_index[j]){
					self.current_page = j;
					self.move(self.current_page);
					self.current();
					self.autoMove();
				}
			}
		}
	}
}
Scroll.prototype.current = function(){
	var self = this;
	if(!self.imgs_index){
		return;
	}
	var imgs_index = self.imgs_index.getElementsByTagName("li");
	for(var i=0;i<self.page_total;i++){
		imgs_index[i].className = "";
	}
	if(self.current_page == self.page_total){
		imgs_index[0].className = "lbi-current";
	}else{
		imgs_index[self.current_page].className = "lbi-current";
	}
}
Scroll.prototype.mouseOver = function(){
	var self = this, container_child = self.container.childNodes;
	for(var i=0;i<container_child.length;i++){
		if(container_child[i].nodeType == 1){
			container_child[i].onmouseover = function(){
				clearInterval(self.timer1);
				clearInterval(self.timer2);
			}
			container_child[i].onmouseout = function(){
				self.move(self.current_page);
				self.current();
				self.autoMove();
			}
		}
	}
}
