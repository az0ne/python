(function(){

	var oDoc = $(document);

	$.chartExtend = {


		// 饼图
		'Pie' : function(opt){
			opt.canvas = $(opt.canvas);
			var ctx = opt.canvas[0].getContext("2d");
			return new Chart(ctx).Pie( opt.data, { 'animationEasing' : 'easeOutCubic', 'tooltipEvents' : ['mousemove','mouseout'] } );
		},


		// 折线图
		'Line' : function(opt){
			opt.canvas = $(opt.canvas);
			var chartBox = opt.canvas.parent();
			var ctx = opt.canvas[0].getContext("2d");
			var maxNum = 0;
			var chartData = (function(data){
				var result = {
						'labels' : [],
						'datasets' : []
					};
				//data = data.unshift({});
				$.each(data, function(k,v){
					if(!k){
						result.labels.push('');
					}
					result.labels.push(v.date||'');
					$.each(opt.legend, function(i,o){
						var value = v[ o.dataKey ];
						if(!result.datasets[i]){
							result.datasets[i] = {
								'strokeColor' : o.lineColor,
								'pointColor' : o.lineColor,
								'pointStrokeColor' : "#fff",
								'label' : o.label,
								'data' : [null]
							};
						}
						result.datasets[i].data.push( value );
						maxNum = Math.max( maxNum, value );
					});
				});

				// 数据补白
				var defaultLength = 8;
				if(data.length < defaultLength){
					result.labels = result.labels.concat( arrayPlace( defaultLength - data.length, '' ) );
				}
				return result;
			}( opt.data ));
			// legend
			opt.canvas.css({ 'width' : chartData.labels.length * 45 }).wrap('<div style="position:relative;overflow:hidden;width:100%;padding-bottom:10px;"/>');

			// chart option
			opt.suf = opt.suf || '';
			var chartOption = {
				'datasetFill' : false, // 不填充折线区域颜色
				'scaleShowLabels': false, // 不显示刻度值
				// 'scaleLabel' : "<%=value+'%'%>", // y轴刻度值格式
				'scaleOverride' : true, // 覆盖y轴默认刻度
				'scaleStepWidth' : opt.yStepWidth || Math.round(maxNum / ((opt.defaultStep || 5) - 1)), // y轴刻度间隔
				'scaleStartValue' : opt.yStartValue || 0, // y轴初始刻度
				'scaleSteps' : opt.defaultStep || 5, // y轴刻度步数
				'legendTemplate': "<div class=\"chart-legend chart-<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><span class=\"legend-item\"><i style=\"background-color:<%=datasets[i].strokeColor%>\"></i><em><%if(datasets[i].label){%><%=datasets[i].label%></em><%}%></span><%}%></div>", // 图例调用generateLegend()时，返回字符串格式
				'tooltipTemplate' : '<%=this.datasetLabel + \": \" + value + \"'+ opt.suf +'\" %>', // 气泡提示文案格式
				'isMultiple' : false, // 是否在气泡提示中显示多重数据
				'tooltipEvents' : ['mousemove','mouseout'], // 允许执行的鼠标事件
				// 鼠标事件回调函数
				'eventCallback' : function(e,activePoints){
					var oCur, oCurPoint;
					var xy = Chart.helpers.getRelativePosition(e);

					if( activePoints.length ){
						oCurPoint = [];
						for(var i = activePoints.length; i > 0; i-- ){
							oCur = activePoints[ i-1 ];
							if( xy.x > oCur.x - 4 && xy.x < oCur.x + 4 && xy.y > oCur.y - 4 && xy.y < oCur.y + 4 ){
								// 只显示鼠标经过"点"的数据
								oCurPoint = [oCur];
							}
						}
						this.showTooltip( oCurPoint );
					}else{
						this.showTooltip(activePoints);
					}
				}}
			// 实例化图表
			var curChart = (new Chart( ctx )).Line( chartData, chartOption);

			var labels = (function(){
				var step = chartOption.scaleSteps;
				var height = (opt.canvas.height() - 35) / step;
				var right = opt.canvas.parent()[0].clientWidth;
				var result = '';
				while(step>-1){
					result += '<li style="width:3em;position:absolute;right:0;left:0;top:'+ ((chartOption.scaleSteps-step) * height + 5) +'px;text-align:right;color:#666">'+ step * chartOption.scaleStepWidth + (step?opt.suf : '') +'</li>';
					step--;
				}
				return result;
			}());

			chartBox
			.css({ 'position' : 'relative', 'paddingLeft' : '3em', 'display' : 'inline-block', 'max-width' : '100%' })
			.append( $('<ul style="font-size:12px;"/>').append(labels) )
			.parent().prepend( $(curChart.generateLegend()) );

			// 图表滚动
			var oCanvasParent = opt.canvas.parent();
			//opt.canvas.after('<div style="height:15px;"/>');
			opt.canvas.parent().css('paddingBottom', 15);
			// 自定义拖拽滚动
			opt.canvas.width() > oCanvasParent.width() && dragScroll( opt.canvas, opt.canvas.closest('.tab-cnt') );

			return curChart;
		},


		// 雷达图
		'Radar' : function(opt){
			opt.canvas = $(opt.canvas);
			var chartData = (function(opt){
				var result = {
					'labels' : [],
					'datasets' : []
				};
				// 数据补白
				if( opt.labels.length < 5 ){
					opt.labels = opt.labels.concat( arrayPlace( 5 - opt.labels.length, '' ) );
				}
				$.each(opt.data, function(i,o){
					$.each(opt.labels, function(k,v){
						var legend = opt.legend[i] || {};
						if(!result.datasets[i]){
							result.datasets[i] = {
								'fillColor' : legend.fillColor,
								'strokeColor' : legend.lineColor,
								'pointColor' : legend.lineColor,
								'pointStrokeColor' : "#fff",
								'label' : legend.label,
								'data' : []
							};
						}
						result.labels[ k ] = v ? v.label : '';
						result.datasets[i].data.push( v ? o[ v.dataKey ] : '' );
					});
				});
				return result;
			}(opt));
			var chartOption = {
					'pointLabelFontSize' : 12,
					'tooltipEvents' : ['mousemove','mouseout'],
					'legendTemplate': "<div class=\"chart-legend chart-<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><span class=\"legend-item\"><i style=\"background-color:<%=datasets[i].strokeColor%>\"></i><em><%if(datasets[i].label){%><%=datasets[i].label%></em><%}%></span><%}%></div>",
					'isMultiple' : false, // 是否在气泡提示中显示多重数据
					'eventCallback' : function(e,activePointsCollection){
						var oCur, oCurPoint;
						var xy = Chart.helpers.getRelativePosition(e);

						if( activePointsCollection.length ){
							oCurPoint = [];
							for(var i = activePointsCollection.length; i > 0; i-- ){
								oCur = activePointsCollection[ i-1 ];
								if( xy.x > oCur.x - 4 && xy.x < oCur.x + 4 && xy.y > oCur.y - 4 && xy.y < oCur.y + 4 ){
									// 只显示鼠标经过"点"的数据
									oCurPoint = [oCur];
								}
							}
							this.showTooltip( oCurPoint );
						}else{
							this.showTooltip(activePointsCollection);
						}
					}
				};
			var curChart = new Chart( opt.canvas[0].getContext("2d") ).Radar( chartData, chartOption);
			// Radar的实例重新自定义了 getPointsAtEvent方法，此处删除自定义，调用原型中继承的方法
			delete curChart.getPointsAtEvent;

			opt.canvas.before( $(curChart.generateLegend()) );

			return curChart;
		},

		// 柱图
		'Bar' : function(opt){
			opt.canvas = $(opt.canvas);
			var chartData = {
				'labels' : [],
				'datasets': []
			};
			var chartOption = {
				'scaleOverride' : true, // 覆盖y轴默认刻度
				'xStepWidth' : opt.xStepWidth || 75, // X轴刻度间隔
				'scaleStepWidth' : opt.yStepWidth || 20, // y轴刻度间隔
				'scaleStartValue' : opt.yStartValue || 0, // y轴初始刻度
				'barValueSpacing' : 25,
				'scaleSteps' : 5 // y轴刻度步数
			};
			var defaultLength = 5;
			if(opt.data.length < defaultLength){
				opt.data = opt.data.concat( arrayPlace( defaultLength - opt.data.length, '' ) );
			}
			$.each(opt.data, function(k,v){
				var sLabel = v.course_name || '';
				/*if(sLabel.length > 4){
					sLabel = sLabel.slice(0,5)+'...';
				}*/
				chartData.labels.push(sLabel);
				$.each(opt.legend || [null], function(i,o){
					if(!chartData.datasets[i]){
						chartData.datasets[i] = {
							'fillColor' : o.fillColor,
							'strokeColor' : o.strokeColor,
							'pointColor' : '#fff',
							'pointStrokeColor' : "#fff",
							'data' : []
						};
					}
					chartData.datasets[i].data.push(v.course_score || '' );
				});
				
			});
			opt.canvas.width( opt.data.length * chartOption.xStepWidth + 30 );
			var curChart = new Chart( opt.canvas[0].getContext("2d") ).Bar( chartData, chartOption);
			//opt.canvas.parent()[0].style.overflow = 'auto'
			//自定义滚动
			dragScroll(opt.canvas, opt.canvas.parent());

			return curChart;
		},


		// 柱图 edit 1
		'BarE1' : function(opt){
			opt.canvas = $(opt.canvas);
			var chartOption = {
				'scaleShowLabels' : false,
				'tooltipEvents' : ['mousemove','mouseout'],
				'barOuterMargin' : 5,
				'barInnerMargin' : 2,
				'xPlace' : 100,
				'xStep' : 30,
				'yPlace' : 6,
				'yColWidth' : 41,
				'gridLineWidth' : 1,
				'scaleFontSize' : 14,
				'scaleFontFamily' : '"Noto Sans CJK SC", "Source Han Sans CN", "STXihei", "Microsoft yahei", sans-serif',
				'tooltipTemplate' : '<%=this.legend + \': \' + this.value%>',
				'legendTemplate' : "<div class=\"chart-legend chart-<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><span class=\"legend-item\"><i style=\"background-color:<%=datasets[i].strokeColor%>\"></i><em><%if(datasets[i].label){%><%=datasets[i].label%></em><%}%></span><%}%></div>",
				'showGridLineX' : true,
				'showGridLineY' : true
			};
			var chartData = {
				'maxValue' : opt.maxValue,
				'labels' : [],
				'xLabels' : null,
				'datasets': []
			};
			var defaultLength = 10;

			if( opt.data.length < defaultLength ){
				opt.data = opt.data.concat( arrayPlace( defaultLength - opt.data.length, '' ) );
			}

			$.each(opt.data, function(k, v){
				$.each(opt.labels, function(i,o){
					if(!chartData.datasets[i]){
						chartData.datasets[i] = {
							'fillColor' : o.color[1],
							'strokeColor' : o.color[0],
							'label' : o.label || '',
							'data' : []
						}
					}
					chartData.datasets[i].data.push( v[ o.dataKey ] || '' );
				});
				chartData.labels.push( v.name || '' );
			});

			opt.canvas.height( opt.data.length * chartOption.yColWidth + chartOption.yPlace + 10 );
			opt.canvas.width( opt.canvas.parent().width() - 5 );

			//chartData.xLabels = arrayPlace( opt.data.length, '' );

			//console.log( chartData );
			var curChart = new Chart( opt.canvas[0].getContext("2d") ).BarE1( chartData, chartOption);

			// 添加图例
			opt.canvas.parent().before( $(curChart.generateLegend()) );

			// 自定义滚动
			dragScroll(opt.canvas, opt.canvas.parent());

			return curChart;
		},


		// 柱图 edit 2
		'BarE2' : function(opt){
			opt.canvas = $(opt.canvas);
			var colorKey, color = opt.colorGroup;
			var chartData = {
				'color' : [],
				'labels' : [],
				'xLabels' : null,
				'datasets': []
			};
			var dataSort = [];
			var defaultLength = 12;

			if(opt.data.length < defaultLength){
				opt.data = opt.data.concat( arrayPlace( defaultLength - opt.data.length, '') );
			}

			// 取出用户数据
			$.each(opt.data, function(k,v){
				$.each(opt.datasets || [null], function(i,o){
					if(!chartData.datasets[i]){
						chartData.datasets[i] = {
							'data' : []
						};
					}
					chartData.datasets[i].data.push(v.kpi);
				});
			});
			// 数据从大到小排序
			$.each(chartData.datasets, function(i,o){
				o.data.sort(function(a,b){ return b-a; });
			});
			$.each(chartData.datasets, function(i,o){
				$.each(chartData.datasets[i].data, function(k,v){
					opt.data && $.each(opt.data, function(x,val){
						if( v === val.kpi ){
							// labels
							chartData.labels.push(val.name || '');
							if( val.kpi >= 100 ){
								colorKey = 100;
							}else if( val.kpi < 100 && val.kpi >= 75){
								colorKey = 75;
							}else if( val.kpi < 75 && val.kpi >= 50){
								colorKey = 50;
							}else if( val.kpi < 50 && val.kpi >= 25){
								colorKey = 25;
							}else if( val.kpi < 25 && val.kpi >= 0){
								colorKey = 0;
							}
							chartData.color.push( color[ colorKey ] );
							// 记录结果
							dataSort.push(val);
							opt.data.splice(x,1);
							return false;
						}
					});
				});
			});

			opt.suf = opt.suf || '';

			var chartOption = {
				//'scaleShowLabels': false, // 不显示刻度值
				'scaleLabel' : "<%=value+\'"+opt.suf+"\'%>", // y轴刻度值格式
				'scaleOverride' : true, // 覆盖y轴默认刻度
				'scaleStepWidth' : opt.yStepWidth || 25, // y轴刻度间隔
				'scaleStartValue' : opt.yStartValue || 0, // y轴初始刻度
				'scaleSteps' : opt.defaultStep || 4, // y轴刻度步数
				'barValueSpacing' : 30,
				'tooltipTemplate' : '<%=this.label + \": \" + value + \"'+ opt.suf +'\" %>' // 气泡提示文案格式
			};
			var colWidth = 90;
			var curWidth = dataSort.length * colWidth;

			opt.canvas.width( curWidth );
			// 插件 x轴 label 为空字符串
			chartData.xLabels = arrayPlace( dataSort.length, '' );
			// 自定义创建 x轴 刻度
			opt.canvas.next('.chart-x-a').remove();
			opt.canvas.after( $( xDomInfo( dataSort, colWidth - 2 ) ).width( curWidth ) );
			// 图表实例
			var curChart = new Chart( opt.canvas[0].getContext("2d") ).BarE2( chartData, chartOption);
			// 自定义拖拽滚动
			opt.canvas.width() > opt.canvas.parent().width() && dragScroll( opt.canvas, opt.canvas.closest('.tab-cnt') );
			return curChart;

			function xDomInfo(data,width){
				var html = '<ul class="chart-x-a clearfix">';
				$.each(data || [], function(k,v){
					if(v){
						html += '<li style="width:';
						html += width;
						html += 'px"><a href="';
						html += v.url != null ? v.url : v.src || 'javascript:;';
						html += '" style="display:inline-block"><span class="img"><img class="img-circle" src="';
						html += v.img;
						html += '" alt="';
						html += v.name;
						html += '" title="';
						html += v.name;
						html += '" /></span><span class="text">';
						html += v.name;
						html += '</span></a></li>';
					}
				});
				html += '</ul>';
				return html;
			}
		}
	};


	// 常用方法

	// 占位数组
	function arrayPlace(i,val){
		var arr = [];
		for(;i>0;i--){ arr[i-1] = val; }
		return arr;
	}
	// 定义拖拽滚动
	function dragScroll(elm, areaElm,oo){
		var xy = {}, oParent, isInner, paneApi, scrollBar;
		elm = $(elm);
		areaElm = $(areaElm);
		oParent = elm.parent();
		// JS定义滚动条
		oParent.jScrollPane();
		paneApi = oParent.data('jsp');
		scrollBar = oParent.find('.jspHorizontalBar,.jspVerticalBar');
		scrollBar.hide();
		areaElm.hover(function(){
			scrollBar.fadeIn();
		},function(){
			scrollBar.fadeOut();
		});
		xy.stepX = Math.ceil(paneApi.getContentWidth()/oParent.width())*2;
		xy.stepY = Math.ceil(paneApi.getContentHeight()/oParent.height())*2;
		// 绑定拖拽事件
		elm.on({
			'mousedown' : function(e){
				xy.x = e.pageX;
				oDoc.on({'mousemove' : moveFn, 'mouseup' : upFn});
				return false;
			},
			'mouseup' : upFn,
			'mouseout' : function(){
				isInner = false;
			},
			'mouseover' : function(){
				isInner = true;
			}
		});
		function moveFn(e){
			var valX = e.pageX - xy.x > 0 ? -xy.stepX : xy.stepX;
			var valY = e.pageY - xy.y > 0 ? -xy.stepY : xy.stepY;
			var px = paneApi.getPercentScrolledX();
			var py = paneApi.getPercentScrolledY();
			if(isInner){
				/*if( px != xy.curPX || ( px == 1 && valX < 0 ) || ( px == 0 && valX > 0 ) ){
					paneApi.scrollBy(valX,null);
				}
				if( py != xy.curPY || ( py == 1 && valY < 0 ) || ( py == 0 && valY > 0 ) ){
					paneApi.scrollBy(null,valY)
				}*/
				paneApi.scrollBy(valX,valY)
				xy.x = e.pageX;
				xy.y = e.pageY;
				xy.curPX = px;
				xy.curPY = py;
			}
			return false;
		}
		function upFn(e){
			oDoc.off({'mousemove' : moveFn, 'mouseup' : upFn});
			return true;
		}
	}
}());