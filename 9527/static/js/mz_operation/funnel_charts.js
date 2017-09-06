function load_funnel_chart(div_id, form_id, start_date, end_date) {
    // 基于准备好的dom，初始化echarts图表
    var Chart = echarts.init(document.getElementById(div_id));
    var seriesArray = $("#" + form_id).serializeArray();
    var legendArray = new Array();
    
    $.each(seriesArray, function (index, value) {
        legendArray.push(value.name)
    })
	
    var sum = 0.0;
    var total_count = 0;
    var total_amount = 0;
    $.each(seriesArray, function (index, value) {
	var _t = value.value.split("|");
	var _v = _t[0];
	var _c = _t[1];
        sum = sum + parseFloat(_c);
	total_count = total_count + parseInt(_c);
	total_amount = total_amount + parseInt(_v);
    });

    $.each(seriesArray, function (index, value) {
	var _t = value.value.split("|");
	var _v = _t[0];
	var _c = _t[1];

	var __t = seriesArray[index].value.split("|");
	var __v = __t[0];
	var __c = __t[1];

        seriesArray[index].name = seriesArray[index].name + "  数量: " + _c + " 概率金额: " + _v;

        // seriesArray[index].value = (parseInt(__c) / sum * 100).toFixed(2);
	seriesArray[index].value = 100 - index * 20;
	if (index == 5) {
	    seriesArray[index].value = seriesArray[index].value + 10;
	}
    });

    $("#funnel_amount").text(total_amount.toFixed(2));
    $("#funnel_count").text(total_count);
    

    var option = {
        title: {
            text: '',
            subtext: start_date + "<=时间<" + end_date
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c}%"
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                // restore : {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: legendArray
        },
        calculable: true,
        series: [
            {
                name: '***漏斗图',
                type: 'funnel',
                width: '40%',
                data: seriesArray

            }

        ]
    };

    // 为echarts对象加载数据
    Chart.setOption(option);
}


function load_line_chart(div_id, data, x_data, start_date, end_date) {
    // 基于准备好的dom，初始化echarts图表
    var Chart = echarts.init(document.getElementById(div_id));
    var seriesArray1 = data
    var legendArray = new Array();
    $.each(seriesArray1, function (index, value) {
        legendArray.push(value.name)
    })
    if (start_date < end_date) {
        var subtext = start_date + "<=时间<" + end_date
    }
    else {
        var subtext = end_date + "<=时间<" + start_date
    }
    var option = {
        title: {
            text: '',
            subtext: subtext
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: legendArray
        },
        toolbox: {
            show: true,
            feature: {
                // mark: {show: true},
                dataView: {show: true, readOnly: false},
                // magicType: {show: true, type: ['line', 'bar']},
                // restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: x_data
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: seriesArray1
    };


    // 为echarts对象加载数据
    Chart.setOption(option);
}

function funnel_chart_ajax() {
    var start_date = $('#funnel_start_date_id').val();
    var end_date = $('#funnel_end_date_id').val();
    var department_name = $('#funnel_department_name_id').val();
    var username = $('#funnel_username_id').val();

    if (start_date != "" && end_date != "") {
        $.ajax({
            url: '/operation/charts/funnel_chart_ajax/',
            data: {
		'funnel_start_date': start_date,
		'funnel_end_date': end_date,
		'funnel_department_name': department_name,
		'funnel_username': username
	    },
            dateType: 'json',
            success: function (result) {
                if (result.status == "success") {
                    $("#funnel_form").children('input').remove()
                    $.each(result.data, function (index, value) {
                        $("#funnel_form").append("<input type='hidden' name='" + value.name + "' value='" + value.value[1]+ "|" + value.value[0] + "'>")
                    })
                    load_funnel_chart("funnel_chart", 'funnel_form', result.start_date, result.end_date)

                }
                else {
                    layer.alert("服务器异常，数据加载失败！");
                }
            },

        });
    }
    else {
        layer.alert("请选择起始时间和结束时间！");
    }
}

function line_chats_ajax(div_id, type) {
    var start_date = $('#line_start_date_id_' + type).val();
    var end_date = $('#line_end_date_id_' + type).val();
    var department_name = $('#line_department_name_id_' + type).val();
    var username = $('#line_username_id_' + type).val();
    
    if (start_date != "" && end_date != "") {
        $.ajax({
            url: '/operation/charts/sale_line_charts/',
            data: {
	    	'line_start_date': start_date,
	    	'line_end_date': end_date,
	    	'line_department_name': department_name,
	    	'line_username': username,
	    	'api_type': type},
            dateType: 'json',
            success: function (result) {
                if (result.status == "success") {
                    var data = result.data
                    var dates = result.dates
                    load_line_chart(div_id, data, dates, result.start_date, result.end_date);
                    // 渲染表格数据
                    $("#example thead tr th").remove();
                    $("#example thead tbody").remove()
                    $("#example thead tr").append("<th></th>")
                    $.each(dates, function (index, value) {
                        $("#example thead tr").append("<th>" + value + "</th>")
                    })
                    $.each(data, function (index, value) {
                        $("#example tbody").append("<tr><td>" + value.name + "</td></tr>")
                        $.each(value.data, function (index1, value1) {
                            $("#example tbody tr:last-child").append("<td>" + value1 + "</td>")
                        })
                    })
                }
                else {
                    layer.alert("服务器异常，数据加载失败！");
                }

            }
        });
    }
    else {
        layer.alert("请选择起始时间和结束时间！");
    }

}

$(".username_change").change(function(){
    
    var _id = $(this).attr("username_id")
    
    $.ajax({
        url: '/operation/charts/user_chart_ajax/',
        data: {
	    'department_name': $(this).val()
	},
        dateType: 'json',
        success: function (result) {
            if (result.status == "success") {
                var users = result.users;
		var txt = ""

		for (var i=0; i < users.length; i++) {
		    txt = txt + '<option value="' + users[i] + '">' + users[i] + '</option>';
		}
		$("#" + _id).html(txt)
            }
            else {
                layer.alert("服务器异常，数据加载失败！");
            }
        }
    });
})
