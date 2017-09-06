var init = function(){
	$(".personalCTop .font .personalCico").hover(function(){
		layer.tips($(this).attr("title"), $(this), {
		  tips: [1, '#333333'] //还可配置颜色
		});
	},function(){
		
	});
	var eCavner=document.getElementById('eCmainCavner');
	if(eCavner){
		var myChart = echarts.init(eCavner);
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
				data:['毕业','已完成','正常','落后','休学','退学']
			},
			series: [
				{
					name:'',
					type:'pie',
					radius: ['50%', '70%'],
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
					center: [100, 100],
					labelLine: {
						normal: {
							show: false
						}
					},
					data:opt
				}
			]
		};
		myChart.setOption(option);
	}

	$(".teacherCenterMenu>a").click(function(){
		$(this).addClass("aH").siblings().removeClass("aH");
		$(".teacherCenterTabContent>div").eq($(this).index()).addClass("cur").siblings().removeClass("cur");
	});
	 $('.teacherCenterTeachBxslider>ul,.teacherCenterStudentBxslider>ul').bxSlider({
        captions: true,
        auto: true
    });
    function addNodes(){	
	    var nodesNum = 0;    
	    function addNodes(myId,myNodes){
	        nodesNum = myId.length;
	        myNodes.append("<em>/ "+nodesNum+"</em>");
	    }
	   	addNodes($(".teacherCenterTeachBxslider .bx-pager-item"),$(".teacherCenterTeachBxslider .bx-pager"));
		addNodes($(".teacherCenterStudentBxslider .bx-pager-item"),$(".teacherCenterStudentBxslider .bx-pager"));
	}
	addNodes();
	
	var evt = "onorientationchange" in window ? "orientationchange" : "resize";
	window.addEventListener(evt,function(){
	 	addNodes();
	});
}

init();