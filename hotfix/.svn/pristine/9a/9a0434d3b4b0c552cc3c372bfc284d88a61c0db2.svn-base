(function(){
	$.commonTool = {
		'tab' : function(opt){
			var box = $(opt.tabBox);
			var btn = $(opt.btnBox || box.find('[tab-role=btn-group]')).find('[tab-role=btn]');
			var cnt = $(opt.cntBox || box.find('[tab-role=cnt-group]')).find('[tab-role=cnt]');
			var activeBtn;
			if( opt.active == null ){
				opt.active = 'active'
			}
			btn.each(function(i){

				var _btn = btn.eq(i);

				_btn.on(opt.transitionEventType || 'click', function(){

					if(activeBtn == this){
						return;
					}else{
						activeBtn = this;
					}

					var _cnt = cnt.filter('[tab-mark='+ _btn.attr('tab-target') +']');

					btn.removeClass( opt.active );
					_btn.addClass( opt.active );
					cnt.hide();
					_cnt.fadeIn(function(){

						opt.transitionEndCallback && opt.transitionEndCallback.call(_btn[0], _btn, _cnt);

					});

					opt.transitionCallback && opt.transitionCallback.call(_btn[0], _btn, _cnt);

				});
			}).eq(opt.showIndex || 0).click();
		},
		'slide': function(opt){

			// 从左至右划出动画
			if(opt.direction=='right'){

				var wrap, close, mask;
				var dom = $(opt.dom).show();

				function closeFn(){
					wrap.animate({ width: 0, overflow: 'hidden' }, function(){
						if(dom){
							dom.hide();
							wrap.before(dom);
						}
						wrap.remove();
						opt.mask && mask.remove();
						opt.end && opt.end();
					});
				}

				wrap = $('<div class="slide-dialog" isdialog="true">');
				wrapIn = $('<div style="position:absolute;top:0;right:0;">');
				close = $('<div class="close">');
				mask = $('<div class="mask" style="position:fixed;width:100%;height:100%;top:0;left:0;">');

				opt.mask = opt.mask != null ? opt.mask : true;
				wrap.append(close);
				wrap.css({ position: opt.position || 'absolute', overflow: 'hidden', height: opt.height || dom.height(), top: opt.top, left: opt.left, zIndex: opt.zIndex || 10 });
				mask.css({ zIndex: opt.zIndex || 10 });
				close.click(closeFn);
				opt.mask && opt.maskClose && mask.mousedown(closeFn);

				if(dom && dom[0] && dom[0].parentNode && dom[0].parentNode.nodeName){
					if(dom.parent().parent().attr('isdialog')){
						return;
					}
					dom.before(wrap);
				}else{
					$(document.body).append(wrap);
				}
				wrapIn.css({ width: opt.width, height: opt.height, display: 'block' });
				wrapIn.append(dom);
				opt.mask && wrap.before(mask);
				wrap.append(wrapIn).width(0).animate({ width: opt.width },function(){
					//wrap.css({ overflow: '' });
				});

				return { close : closeFn, layer: wrap }
			}
		},
		'addLock' : function(elm,val,oParent){

			elm = $(elm);
			oParent = $(oParent);
			
			var body = $(document.body);
			var html = '';
			html += '<div class="lock-panel"><div class="lock-panel-in">';
			html += '<span class="lock"></span><span class="text">'+(val != null  ? '' : '报名后可查看学习数据！')+'</span>';
			html += '</div></div>';
			elm.each(function(i,o){
				var pa;
				var paOffset;
				var paPosition;
				var panel = elm.eq(i);
				var lock = $(html);
				var position = panel.css('position');
				var w;
				var h;
				var offset;
				var oPosition = {
					'fixed' : 'fixed',
					'relative' : 'relative',
					'absolute' : 'absolute'
				}
				setSize();
				pa.append( lock );
				$(window).on('resize',function(){
					setSize();
				});
				function setSize(){
					w = panel.outerWidth();
					h = panel.outerHeight();
					offset = panel.offset();
					lock.find('.lock-panel-in').width( w ).height( h );
					/*if( !oPosition[ position ]  ){
						panel.css('position','relative');
					}*/
					if(oParent.length){
						if(oParent.length > 1){
							pa = oParent.eq(i);
						}else{
							pa = oParent;
						}
						paOffset = pa.offset();
						paPosition = pa.css('position');
						if(paPosition !== 'absolute' && paPosition !== 'relative' && paPosition !== 'fixed'){
							pa.css('position','relative');
						}
						lock.width( w ).height( h ).css({ 'left' : offset.left - paOffset.left, 'top' : offset.top - paOffset.top });
					}else{
						pa = body;
						lock.width( w ).height( h ).css({ 'left' : offset.left, 'top' : offset.top });
					}
				}
			});
		},
		'editUserInfo' : function(id,_height){
			function photoControl(curImg){
				result.curImg = curImg;
				curImg.css({ 'position': 'absolute', 'maxWidth': 'none' }).on('load',function(){

					var imgWidth = curImg.width();
					var imgHeight = curImg.height();
					var boxWidth = oFileBox.width();
					var boxHeight = oFileBox.height();

					curImg.css({ 'width': imgWidth, 'marginTop' : (boxHeight - imgHeight) / 2, 'marginLeft' : (boxWidth - imgWidth) / 2 });
					result.imageInfo.imgWidth = imgWidth;
					result.imageInfo.imgHeight = imgHeight;
					result.imageInfo.boxWidth = boxWidth;
					result.imageInfo.boxHeight = boxHeight;

					if( !result.allowControlPhoto ){
						tipShow(4);
						return;
					}

					photo_h_slide.html(' ');
					$.commonTool.QZslider({
						slidBox : photo_h_slide,
						slidMainWidth : 110,
						valueFloat : 0,
						valueLeft : 1,
						valueRight : 100,
						valueInit : 50,
						showRange:true,
						//showValue:true,
						valueChange : function(value){
							var p = value/50;
							var curW = imgWidth * p;
							var curH = imgHeight * p;
							result.imageInfo.scale = p;
							result.imageInfo.imgWidth = curW;
							result.imageInfo.imgHeight = curH;
							result.imageInfo.marginLeft = (parseInt(curImg.css('left')) || 0) + (boxWidth - curW) / 2;
							result.imageInfo.marginTop = (parseInt(curImg.css('top')) || 0) + (boxHeight - curH) / 2;
							curImg.css( 'transform', 'scale('+p+')' );
						}
					});
					photo_h_slide.find('.slider-min').html('-');
					photo_h_slide.find('.slider-max').html('+');
				});
			}
			function msMove(e){
				var img = result.curImg;
				var curLeft, curTop, imgInfo;
				if( img && result.allowControlPhoto ){
					curLeft = msMove._x + e.clientX - msMove._mx;
					curTop = msMove._y + e.clientY - msMove._my;

					img.css({ 'left': curLeft, 'top': curTop });

					imgInfo = result.imageInfo;

					imgInfo.marginLeft = (curLeft || 0) + (imgInfo.boxWidth - imgInfo.imgWidth) / 2;
					imgInfo.marginTop = (curTop || 0) + (imgInfo.boxHeight - imgInfo.imgHeight) / 2;
				}
				return false; //for ie
			}
			function msUp(){
				oDoc.off({ 'mousemove': msMove, 'mouseup': msUp, 'selectstart': msMove });
			}
			function tipShow(ind){
				var cls = 'photo-h-active';
				tips.removeClass(cls).eq(ind).addClass(cls);
			}


			var oDoc = $(document);
			var user_panel = $(id || '#user_panel');
			var photo_h_slide = $(".photo-h-slide :first-child", user_panel);
			var img = null;
			var oFile = $('input[type=file]', user_panel);
			var oFileBox = oFile.parent();
			var oFilePrev = oFile.prev('a');
			var oFilePrevS;
			var tips = oFile.closest('.col-sm-10').find('.photo-h');
			var time;
			var result = {
					'curImg': null
					,'imageInfo': {
						'scale' : 1,
						'boxWidth'  : 0,
						'boxHeight' : 0,
						'imgWidth'  : 0,
						'imgHeight' : 0,
						'marginLeft': 0,
						'marginTop' : 0
					}
					,'allowControlPhoto': false
					,'fileChangeRunAjax' : false
					,'fileChangeCallback': null
					,'tipShow': tipShow
					,'showPhoto' : function(url){
						var img;
						if(url){
							img = $('<img src=\"' + url + '\" />');
							photoControl(img);
							oFileBox.addClass('has-img').find('img').remove();
							oFileBox.append(img);
						}
					}
				};

			if(user_panel.length){
				layer.open({
					type: 1,
					title : 0,
					skin : 'd-common-tool',
					area: ['850px', _height != null ? _height : '540px'], //宽高
					content: user_panel,
					//end: function(){console.log(result)}
				});

				oFileBox.removeClass('has-img');
				oFile.val('');
				$('img', oFileBox).remove();
				tipShow(0);
				photo_h_slide.html('');

				oFilePrevS = oFilePrev.remove().prev('i').remove();
				if(!oFilePrevS.length){
					oFilePrevS = $('<i style="position:absolute;z-index:101;top:0;left:0;height:100%;width:100%;cursor:move">');
					oFilePrev.before( oFilePrevS );
					oFilePrevS.attr('isShow','true');
				}else{
					oFilePrevS.removeAttr('isShow');
				}

				// 只执行一次
				if((!$.commonTool.editUserInfo.isShow) || oFilePrevS.attr('isShow') ){
					$.commonTool.editUserInfo.isShow = true;
					oFile.on({
						'mousedown': function(e){
							time = new Date();
							if(result.curImg){
								oDoc.on('mousemove', msMove);
								oDoc.on('mouseup', msUp);
								oDoc.on('selectstart', msMove);
								msMove._x = parseInt(result.curImg.css('left'))||0;
								msMove._y = parseInt(result.curImg.css('top'))||0;
								msMove._mx = e.clientX;
								msMove._my = e.clientY;
							}
						}
						,'click': function(){var t = new Date() - time
							if( t < 150){
								//oFile.click();
								time = 0;return true;
							}return false
						}
						,'mouseout': function(){ msUp(); }
						,'mouseup' : function(){ msUp(); }
						,'blur'    : function(){ msUp(); }
					});
					oFile.change(function(){
						if(this.value){
							if( result.fileChangeRunAjax ){
								result.fileChangeCallback && result.fileChangeCallback();
							}else{
								img = $.commonTool.getLocaImageUrl(this);
								if(img){
									result.showPhoto(img);
								}else{
									result.fileChangeCallback && result.fileChangeCallback();
								}
							}
							tipShow(1);
							result.allowControlPhoto = true;
						}
					});
				}
			}
			return result;
		},
		'previewControlImage' : function(img){
			var data = {scale:null};
			var photo_h_slide = $("#photo_h_slide");
			var actSlideClass = 'photo-h-active';
			var oParent = photo_h_slide.parent();
			var oWidth = img.width();

			photo_h_slide.html(' ').
			img.css( 'transform', '' );

			$.commonTool.QZslider({
				slidBox : photo_h_slide,
				slidMainWidth : 110,
				valueFloat : 0,
				valueLeft : 1,
				valueRight : 100,
				valueInit : 50,
				showRange:true,
				//showValue:true,
				valueChange : function(value,p){
					var pe = value/50;
					data.scale = pe;
					img.css( 'transform', 'scale('+pe+')' );
				}
			});
			photo_h_slide.find('.slider-min').html('-');
			photo_h_slide.find('.slider-max').html('+');
			return data;
		},
		'getLocaImageUrl' : function(file, url){
			var img, div; 
			if(window.URL && window.URL.createObjectURL && ( url || file.files[0] )){
				img = url || window.URL.createObjectURL(file.files[0]);
				//img = $('<img src=\"' + (url || window.URL.createObjectURL(file.files[0])) + '\" />');
			}else{
				return false;
				// IE9 不支持本地预览，需要先上传图片到服务器
				img = $('<div style="position:relative">');
				div = img.clone();
				div.css({ width: 100, height: 100 });
				img.append(div);
				$(document.body).append(img);
				div[0].style.filter = 'progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=image)';
				img[0].onresize = function(){
					var w = this.scrollWidth,
						h = this.scrollHeight;
					img.css({ width: w, height: h });
					img.off('resize');
				};
				div[0].filters["DXImageTransform.Microsoft.AlphaImageLoader"].src = file.value;
			}
			return img;
		},
		'QZslider' : function( _opt ){
			var plug = [];
			$.each( _opt, function( i, o ){
				!( _opt[ i ] ) && _opt[ i ] !== 0 && _opt[ i ] !== "" && delete( _opt[ i ] );
			});
			_opt = $.extend({
				//默认值
				slidBox :　null,//必须，滑动条Box[ selector string ]
				slidMain : "<span class='slider-main'></span>",//可选，滑动条主要部分Box[ HTML string ]
				slidBar : "<i class='slider-bar'></i>",//可选，滑条已选择部分Box[ HTML string ]
				slidBarBg : "<i class='slider-bar-bg'></i>",//可选，滑条未选择部分Box[ HTML string ]
				slidBlock : "<a class='slider-black' href=''></a>",//可选，滑块Box[ HTML string ]
				slidMin : "<span class='slider-min'></span>",//可选，用以显示最小值的Box[ HTML string ]
				slidMax : "<span class='slider-max'></span>",//可选，用以显示最大值的Box[ HTML string ]
				slidValueShowBox : "<i class='slider-value-show'></i>",//可选，用以修饰展示值的Box[ HTML string ]，展示的值将直接呈现在HTML布局中的input标签中
				slidMainWidth : 180,//可选，[ number ]默认180px
				valueInit : null,//可选，初始值[ number ]
				valueLeft : 0,//可选，滑动器左端值[ number ] 默认0
				valueRight : 0,//可选，滑动器右端值[ number ] 默认0
				valueFloat : 0,//可选，滑动器取值多少位小数点[ number ]默认整数取值
				showValue : false,//可选，是否显示取值[ boolean ]默认隐藏
				editValue : false,//可选，是否可以“通过输入设置值”[ boolean ]，如果需要“通过输入设置值”则必须设置showValue项为true
				showRange : false//可选，是否在滑动器两端显示取值范围[ boolean ]默认隐藏
			},_opt);
			var oDOC = $( document ),
				oBox = $( _opt.slidBox );
			$.each( oBox, fnSlidMain);
			return plug;
			function fnSlidMain(){
				var that = this;
				var result = {
					value : null
				};
				var	oBoxCur = $( that ),
					oInp = (function(){
						var o = $( "input:eq(0)", that );
						if( !o.length ){
							o = $('<input />');
						}
						return o;
					}()),
					oMain = $( _opt.slidMain ),
					oBar = $( _opt.slidBar ),
					oBarBg = $( _opt.slidBarBg ),
					oBlack = $( _opt.slidBlock ),
					oMin = $( _opt.slidMin ),
					oMax = $( _opt.slidMax ),
					oValueShowBox = $( _opt.slidValueShowBox ),
					oTimer,
					numBlackW,
					arrInpValueMinMax = (function(){
						var s = oInp.attr( "valueRange" );
						return s ? s.split( "," ) : [];
					})(),
					numLeft = parseFloat( arrInpValueMinMax[ 0 ] ) || _opt.valueLeft || 0,
					numRight = parseFloat( arrInpValueMinMax[ 1 ] ) || _opt.valueRight || 0,
					numMin = numLeft < numRight ? numLeft : numRight,
					numMax = numMin === numLeft ? numRight : numLeft,
					numInit = (function(){
						var num = parseFloat( oInp.attr( "valueInit" ) ) || _opt.valueInit || 0;
						return fnRangeValue( [ numMin, numMax ], num );
					})(),
					numIsAbleWidth,
					numMouseIntX = 0,
					numBlackLeftOld = 0,
					numBlackLeftCur = 0,
					numInpValue = 0;
				//搭建滑动器
				oMain.prepend( oBarBg, oBar, oBlack );
				//是否显示两端值
				_opt.showRange && (function(){
					oMin.html( numLeft );
					oMax.html( numRight );
					oMain.append( oMin, oMax );
				})();
				//滑动器显示到页面
				oBoxCur.prepend( _opt.slidMainWidth && oMain.width( _opt.slidMainWidth ) );
				//必须存在最大值和最小值，并且" 最大值 !== 最小值 "，否则不能拖动滑块，也不能联动
				if( ( !numMin && numMin !== 0 ) || ( !numMax && numMax !== 0 ) || numMax === numMin ){
					oBlack.css( "cursor", "not-allowed" )
				}else{
					//初始化“滑块”可移动的最大偏移
					numIsAbleWidth = ( _opt.slidMainWidth || oMain.width() ) - ( numBlackW = oBlack.width() ),
					//初始化“滑条”宽度值
					oBar.width( numBlackW/2 );
					//显示滑动器当前取值
					_opt.showValue === true ? ( function(){
						oValueShowBox.append( oInp );
						//显示滑动器当前取值时，联动操作
						oInp.addClass( "slider-inp" ).change( function(){
							oTimer && clearTimeout( oTimer );
							oTimer = setTimeout( function(){ 
								var curVal = oInp.val();
								(/^[\-\+]?\d+(\.\d+)?$/).test( curVal ) && ( curVal = parseFloat( curVal ) );
								if( isNaN( curVal ) || typeof( curVal ) === "string" ) return;
								numInpValue !== curVal && (function(){
									move( ( curVal - numMin ) / ( numMax - numMin ) * numIsAbleWidth || 0, true );
									fnInputVal( curVal );
								})();
							}, 30 );
						} );
						//是否可以编辑显示的值
						_opt.editValue ? oInp.attr( "disabled", false ) : oInp.attr( "disabled", true );
						oBoxCur.hide().append( oValueShowBox ).show();
					})() : oInp.hide();
					//给滑动器设置初始取值
					numInit && $(function(){
						numBlackLeftOld = ( numInit - numMin ) / ( numMax - numMin ) * numIsAbleWidth || 0;
						move( numBlackLeftOld, true );
					});
					//给slider的inp设置初始取值
					fnInputVal( numInit || numMin );
					
					//滑块拖拽事件
					oBlack.mousedown(function(e){
						numMouseIntX = e.clientX - numBlackLeftOld;
						oDOC.bind( "mousemove", fnMouseMove ).bind( "mouseup", fnMouseUp );
						return false;
					}).click(function(){
						return false;
					});
				}
				//fn end
				plug.push(result); //结果输出
				return;
				
				function fnMouseMove( e ){
					numBlackLeftCur = fnRangeValue( [ 0, numIsAbleWidth ], e.clientX - numMouseIntX );
					move( numBlackLeftCur );
					var curVal = numBlackLeftCur / numIsAbleWidth * ( numMax - numMin ) + numMin;
					fnInputVal( numLeft < numRight ? curVal : numMax - curVal );
					return false;
				}
				function fnMouseUp( e ){
					oDOC.unbind( "mousemove", fnMouseMove ).unbind( "mouseup", fnMouseUp );
				}
				function move( val, animate ){
					val = fnRangeValue( [ 0, numIsAbleWidth ], Math.round( val ) );
					if( animate === true ){
						val = numLeft < numRight ? val : numIsAbleWidth - val;
						oBlack.animate( { "left" : val + "px"}, "normal" );
						oBar.animate( { "width" : val + numBlackW / 2 + "px" }, "normal" );
					}else{
						oBlack.css( "left", val + "px" );
						oBar.css( "width", val + numBlackW / 2 + "px" );
					}
					numBlackLeftOld = val;
				}
				function fnInputVal( val ){
					val = fnRangeValue ( [ numMin,  numMax ], val );
					val = !_opt.valueFloat ? Math.round( val ) : val.toFixed( _opt.valueFloat || 0 );
					numInpValue = val;
					oInp.val( val );
					oBlack.attr( "title", val );
					result.value = val;
					_opt.valueChange && _opt.valueChange(val, val / numMax);
				}
				function fnRangeValue( range, val){
					return val <= range[ 0 ] ? range[ 0 ] : val >= range[ 1 ] ? range[ 1 ] : val;
				}
			}
		},
		'ruleShow' : function(showCloseIco){
			var xy_panel = $('#xy_panel');
			layer.open({
				type: 1,
				title : 0,
				skin : 'd-common-tool',
				closeBtn: null != showCloseIco ? showCloseIco : true,
				area: ['850px', '545px'], //宽高
				content: xy_panel
			});
			xy_panel.find('.xy-box').jScrollPane();
		},
		'jiuyeShow' : function(showCloseIco){
			var xy_panel = $('#jiuye_panel');
			layer.open({
				type: 1,
				title : 0,
				skin : 'd-common-tool',
				closeBtn: null != showCloseIco ? showCloseIco : true,
				area: ['850px', '545px'], //宽高
				content: xy_panel
			});
			xy_panel.find('.xy-box').jScrollPane();
		}
	};
}());