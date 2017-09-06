define(function(require, exports, module) {
	
	require('echarts'); 
	var th;
	//-------------FUNTION-----------------.
	function signUP(){
		init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){
		$(".teacherCenterINGboxL .cavner").each(function(index, element) {
            if(true){				
				var myChart = echarts.init(element);
				var option = {
					tooltip: {
						trigger: 'item',
						formatter: "{b}: {c} ({d}%)"
					},
					legend: {
						orient: 'vertical',
						right:50,
						top:30,
						align:"left",
						data:['已学完','正常','落后','休学']
					},
					series: [
						{
							name:'',
							type:'pie',
							radius: ['60%', '86%'],
							avoidLabelOverlap: false,
							label: {
								normal: {
									show: false,
									position: 'center'
								},
								emphasis: {
									show: false,
									textStyle: {
										fontSize: '30',
										fontWeight: 'bold'
									}
								}
							},
							center: [80, 80],
							labelLine: {
								normal: {
									show: false
								}
							},
							data:[
								{value:$(this).attr("d1"), name:'已学完',itemStyle:{normal:{color:"#5496d1"}}},
								{value:$(this).attr("d2"), name:'正常',itemStyle:{normal:{color:"#5ecfba"}}},
								{value:$(this).attr("d3"), name:'落后',itemStyle:{normal:{color:"#fbb855"}}},
								{value:$(this).attr("d4"), name:'休学',itemStyle:{normal:{color:"#e24849"}}}
							]
						}
					]
				};
				myChart.setOption(option);
			}
        });
		
	}	
	
	
	module.exports = {
		"init":signUP
	};
	
})