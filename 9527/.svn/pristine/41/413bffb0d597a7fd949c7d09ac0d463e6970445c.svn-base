
// 初始化最小单位为日的选择器
function initDateSelector2Day(start_selector, end_selector) {

    var startDate = $(start_selector).datetimepicker({
        format: 'yyyy-mm-dd',
        language:  'zh-CN',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0,
        endDate: function() {
           return new Date()
        }()
    });
    var endDate = $(end_selector).datetimepicker({
        format: 'yyyy-mm-dd',
        language:  'zh-CN',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0,
        startDate: function() {
            var start_date = new Date(startDate.val());
            start_date.setDate(start_date.getDate() + 1);
            return start_date
        }(),
        endDate: function() {
            var end_date = new Date();
            end_date.setDate(end_date.getDate() + 1);
            return end_date;
        }()
    });
    startDate.on('changeDate', function (ev) {
        var start_date = new Date(ev.date);
        start_date.setDate(start_date.getDate() + 1);
        endDate.datetimepicker('setStartDate', start_date);
    });
}

// 初始化最小单位为月的选择器
function initDateSelector2Month(start_selector, end_selector) {

    var startDate = $(start_selector).datetimepicker({
        format: 'yyyy-mm',
        language:  'zh-CN',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 3,
        minView: 3,
        forceParse: 0,
        endDate: function() {
           return new Date()
        }()
    });
    var endDate = $(end_selector).datetimepicker({
        format: 'yyyy-mm',
        language:  'zh-CN',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 3,
        minView: 3,
        forceParse: 0,
        startDate: function() {
            var start_date = new Date(startDate.val());
            start_date.setMonth(start_date.getMonth() + 1);
            return start_date
        }(),
        endDate: function() {
            var end_date = new Date();
            end_date.setMonth(end_date.getMonth() + 1);
            return end_date;
        }()
    });
    startDate.on('changeDate', function (ev) {
        var start_date = new Date(ev.date);
        start_date.setMonth(start_date.getMonth() + 1);
        endDate.datetimepicker('setStartDate', start_date);
    });
}
// 绑定 切换按月还是按日日期控件 事件
function markDateTypeEvent(charts_selector, start_selector, end_selector) {
    $(charts_selector+' #date_type').change(function () {
        // 清除已有事件
        $(start_selector).datetimepicker('remove');
        $(end_selector).datetimepicker('remove');

        // 清除已有数据
        $(start_selector).val('');
        $(end_selector).val('');

        if ($(this).val() == '1') {
            initDateSelector2Day(start_selector, end_selector);
        } else if ($(this).val() == '2') {
            initDateSelector2Month(start_selector, end_selector);
        }
    });

}


/// <reference path="typings/jquery/jquery.d.ts" />
var Chart = (function () {
    function Chart(chart_id, width, height, data_url, chart_selector, start_selector, end_selector) {
        $('#'+chart_id).css({'width': width, 'height': height});
        this.chart = echarts.init(document.getElementById(chart_id));
        this.data_url = data_url;
        this.chart_selector = chart_selector;
        this.start_selector = start_selector;
        this.end_selector = end_selector;

        this.initDateSelector2Day()
    }
    Chart.prototype.showYBaseFrame = function () {
        var baseOpt = {
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                data: [0]
            }
        };
        this.chart.setOption(baseOpt);
    };
    Chart.prototype.showXBaseFrame = function () {
        var baseOpt = {
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: [0]
            },
            yAxis: {
                type: 'value',
                data: [0]
            }
        };
        this.chart.setOption(baseOpt);
    };
    ;
    Chart.prototype.buildYOption = function (data, x_suffix) {
        return {
            title: {
                text: data.title.text,
                subtext: data.title.subtext
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: "{a} <br/>{b} : {c}"+(x_suffix ? x_suffix : '')
            },
            legend: {
                data: data.legend,
                //backgroundColor: '#01c26f',
                borderColor: '#01c26f'
            },
            color: ['#007d65'],
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01],
                axisLabel: {
                    formatter: '{value}' + (x_suffix ? x_suffix : '')
                }
            },
            yAxis: {
                type: 'category',
                data: data.y_axis_data
            },
            series: data.series_data
        };
    };
    ;
    Chart.prototype.buildXOption = function (data) {
        return {
            title: {
                text: data.title.text,
                subtext: data.title.subtext
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: data.legend
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '6%',
                right: '10%',
                bottom: '12%',
                containLabel: true
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: true,
                    start: 0,
                    end: 100,
                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2
                    }
                }
            ],
            xAxis: {
                type: 'category',
                boundaryGap: false,
                axisLabel: {
                    interval: 0,
                    rotate: 40
                },
                data: data.x_axis_data
            },
            yAxis: {
                type: 'value'
            },
            series: data.series_data
        };
    };
    ;
    Chart.prototype.insertData = function (data) {
        this.chart.clear();
        this.chart.setOption(data);
    };
    ;
    Chart.prototype.setData2Input = function (data, input_selector) {
        $(input_selector).val(JSON.stringify(data));
    };
    ;
    Chart.prototype.removeY = function (self, vals) {
        var data = JSON.parse($(self.chart_selector + ' #main_data').val());
        var _loop_1 = function(i) {
            var val = vals[i];
            var index = jQuery.inArray(val, data.y_axis_data);
            data.y_axis_data.splice(index, 1);
            data.series_data.forEach(function (element) {
                element.data.splice(index, 1);
            }, this_1);
        };
        var this_1 = this;
        for (var i = 0; i < vals.length; i++) {
            _loop_1(i);
        }
        self.insertData(self.buildYOption(data));
    };
    ;
    Chart.prototype.checkboxMarkEvent = function (chart_selector) {
        var self = this;
        $(chart_selector + ' #filter #inlineCheckbox1').click(function () {
            var notChecked = $(chart_selector + ' #filter #inlineCheckbox1').not("input:checked");
            var vals = [];
            for (var i = 0; i < notChecked.length; i++) {
                vals.push($(notChecked[i]).val());
            }
            self.removeY(self, vals);
        });
    };
    ;
    Chart.prototype.initCheckbox = function (data_list) {
        var cb = '';
        var new_data_list = data_list.concat();
        new_data_list.reverse();
        new_data_list.forEach(function (e) {
            cb += '<label class="checkbox-inline">' +
                '<input type="checkbox" id="inlineCheckbox1" value="' + e + '" checked>' + e +
                '</label>';
        }, this);
        return cb;
    };
    ;
    Chart.prototype.doFailedProcess = function (self, data) {
        self.chart.hideLoading();
        // console.log('错误信息：' + data.msg);
        //layer.msg('错误信息：'+data.msg, {time: 2000, icon: 5});
        if (data.code == 403) {
            layer.alert('错误信息：'+data.msg, {icon: 5, closeBtn: 0}, function () {
                window.location = '/'
            });
        } else {
            layer.alert('错误信息：'+data.msg, {icon: 5});
        }
        console.error(data.debug_msg);
    };
    ;
    Chart.prototype.loadYData = function (self, params, x_suffix) {
        // let self = this;
        $.ajax({
            url: self.data_url,
            data: params ? params : {},
            dataType: 'json',
            type: 'GET',
            beforeSend: function () {
                self.chart.showLoading();
            },
            success: function (data) {
                self.rewriteDate(data);
                if (data.success) {
                    var temp = self.buildYOption(data, x_suffix);
                    var cb = self.initCheckbox(data.y_axis_data); // 初始化多选框数据
                    self.insertData(temp); // 插入图表数据
                    self.setData2Input(data, self.chart_selector + " #main_data"); // 保存当前数据
                    $(self.chart_selector + ' #filter').html(cb); // 渲染多选框
                    self.checkboxMarkEvent(self.chart_selector); // 给多选框绑定事件
                    self.chart.hideLoading();
                }
                else {
                    self.doFailedProcess(self, data);
                }
            },
            error: function () {
                self.chart.hideLoading();
                // console.error('服务器异常，请刷新重试。');
                layer.msg('服务器异常，请刷新重试。', {time: 1000, icon: 5});
            }
        });
    };
    ;
    Chart.prototype.loadXData = function (self, params) {
        // let self = this;
        $.ajax({
            url: self.data_url,
            data: params ? params : {},
            dataType: 'json',
            type: 'GET',
            beforeSend: function () {
                self.chart.showLoading();
            },
            success: function (data) {
                self.rewriteDate(data);
                if (data.success) {
                    var temp = self.buildXOption(data);
                    //var cb = initCheckbox(data.y_axis_data);
                    self.insertData(temp);
                    //setData2Input(data, chart_selecter+" #main_data");
                    //$(chart_selecter+' #filter').html(cb);
                    //checkboxMarkEvent(chart, chart_selecter);
                    self.chart.hideLoading();
                }
                else {
                    self.doFailedProcess(self, data);

                }
            },
            error: function () {
                self.chart.hideLoading();
                layer.msg('服务器异常，请刷新重试。', {time: 1000, icon: 5});
                // console.error('服务器异常，请刷新重试。');
            }
        });
    };
    Chart.prototype.buildCalcOption = function (data, equation) {
        var series_data = [];
        var keys = [];
        var orig_data = data['series_data'][0];
        for (var key1 in orig_data) {
            keys.push(key1);
        }
        for (var key2 in orig_data) {
            orig_data[key2].forEach(function(element) {
                series_data.push(equation);
            });
            break;
        }

        for (var ki = 0; ki < keys.length; ki++) {
            for (var si = 0; si < series_data.length; si++) {
                series_data[si] = series_data[si].replace(new RegExp(keys[ki], 'g'), orig_data[keys[ki]][si]);
            }
        }

        for (var si2 = 0; si2 < series_data.length; si2++) {
            try {
                series_data[si2] = eval(series_data[si2]);
                if (series_data[si2] == Infinity) {
                    series_data[si2] = 0
                }
                series_data[si2] = Math.round(series_data[si2]*1000)/1000;
            } catch (error) {
                series_data[si2] = null;
            }
        }

        return {
            title: {
                text: data.title.text,
                subtext: data.title.subtext
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: [equation]
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '6%',
                right: '10%',
                bottom: '12%',
                containLabel: true
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: true,
                    start: 0,
                    end: 100,
                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2
                    }
                }
            ],
            xAxis: {
                type: 'category',
                boundaryGap: false,
                axisLabel: {
                    interval: 0,
                    rotate: 40
                },
                data: data.x_axis_data
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    "name": equation,
                    "type": "line",
                    "data": series_data
                }
            ]
        };
    };
    ;
    Chart.prototype.loadCalcData = function (self, params, equation) {
        $.ajax({
            url: self.data_url,
            data: params ? params : {},
            dataType: 'json',
            type: 'GET',
            beforeSend: function () {
                self.chart.showLoading();
            },
            success: function (data) {
                self.rewriteDate(data);
                if (data.success) {
                    var temp = self.buildCalcOption(data, equation);
                    self.insertData(temp);
                    self.chart.hideLoading();
                }
                else {
                    self.doFailedProcess(self, data);
                }
            },
            error: function () {
                self.chart.hideLoading();
                layer.msg('服务器异常，请刷新重试。', {time: 1000, icon: 5});
                // console.error('服务器异常，请刷新重试。');
            }
        });
    };
    Chart.prototype.initSearch = function (loadData, suffix) {
        var self = this;
        $(self.chart_selector + ' #search_btn').click(function () {
            var real_data = $(self.chart_selector + ' #from').serializeArray();
            var params = {};
            $.each(real_data, function (i, field) {
                params[field.name] = field.value;
            });
            loadData(self, params, suffix);
        });
        self.initShortcut(loadData, suffix);
    };
    ;
    Chart.prototype.initShortcut = function (loadData, suffix) {
        var self = this;
        $(self.chart_selector + ' .shortcut .shortcut-btn').click(function () {
            var shortcut = $(this).attr('data-shortcut');

            var real_data = $(self.chart_selector + ' #from').serializeArray();
            var params = {};
            $.each(real_data, function (i, field) {
                params[field.name] = field.value;
            });
            params['shortcut'] = shortcut;

            loadData(self, params, suffix);
        });
    };
    ;
    // 初始化最小单位为月的选择器
    Chart.prototype.initDateSelector2Day = function() {

        var startDate = $(this.start_selector).datetimepicker({
            format: 'yyyy-mm-dd',
            language:  'zh-CN',
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            minView: 2,
            forceParse: 0,
            endDate: function() {
               return new Date()
            }()
        });
        var endDate = $(this.end_selector).datetimepicker({
            format: 'yyyy-mm-dd',
            language:  'zh-CN',
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            minView: 2,
            forceParse: 0,
            startDate: function() {
                var start_date = new Date(startDate.val());
                start_date.setDate(start_date.getDate() + 1);
                return start_date
            }(),
            endDate: function() {
                var end_date = new Date();
                end_date.setDate(end_date.getDate() + 1);
                return end_date;
            }()
        });
        startDate.on('changeDate', function (ev) {
            var start_date = new Date(ev.date);
            start_date.setDate(start_date.getDate() + 1);
            endDate.datetimepicker('setStartDate', start_date);
        });
    };
    // 初始化最小单位为月的选择器
    Chart.prototype.initDateSelector2Month = function() {

        var startDate = $(this.start_selector).datetimepicker({
            format: 'yyyy-mm',
            language:  'zh-CN',
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 3,
            minView: 3,
            forceParse: 0,
            endDate: function() {
               return new Date()
            }()
        });
        var endDate = $(this.end_selector).datetimepicker({
            format: 'yyyy-mm',
            language:  'zh-CN',
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 3,
            minView: 3,
            forceParse: 0,
            startDate: function() {
                var start_date = new Date(startDate.val());
                start_date.setMonth(start_date.getMonth() + 1);
                return start_date
            }(),
            endDate: function() {
                var end_date = new Date();
                end_date.setMonth(end_date.getMonth() + 1);
                return end_date;
            }()
        });
        startDate.on('changeDate', function (ev) {
            var start_date = new Date(ev.date);
            start_date.setMonth(start_date.getMonth() + 1);
            endDate.datetimepicker('setStartDate', start_date);
        });
    };
    // 绑定 切换按月还是按日日期控件 事件
    Chart.prototype.markDateTypeEvent = function() {
        var self = this;
        var charts_selector = this.chart_selector;

        $(charts_selector+' #date_type').change(function () {
            // 清除已有事件
            $(self.start_selector).datetimepicker('remove');
            $(self.end_selector).datetimepicker('remove');

            // 清除已有数据
            $(self.start_selector).val('');
            $(self.end_selector).val('');

            if ($(this).val() == '1') {
                self.initDateSelector2Day();
            } else if ($(this).val() == '2') {
                self.initDateSelector2Month();
            }
        });

    };
    Chart.prototype.rewriteDate = function (data) {
        $(this.start_selector).val(data.start_date);
        $(this.end_selector).val(data.end_date);

        $(this.start_selector).datetimepicker('update');
        $(this.end_selector).datetimepicker('update');
    };
    return Chart;
}());


//var charts_data_uri = '/operation/charts/data/';
//
//// 初始化时间选择器
//initDateSelector2Day('#start_date', '#end_date');
//
//// 新建图表
//var chart_instance = new Chart('main', '700px', '500px', charts_data_uri+'?type=total', '#charts1');
//chart_instance.showYBaseFrame();
//chart_instance.loadYData(chart_instance);
//chart_instance.initSearch(chart_instance.loadYData);
//
//
//// 初始化时间选择器
//initDateSelector2Day('#start_date2', '#end_date2');
//
//// 新建图表
//var chart_instance2 = new Chart('main2', '700px', '500px', charts_data_uri+'?type=mixedin', '#charts2');
//chart_instance2.showYBaseFrame();
//chart_instance2.loadYData(chart_instance2, {}, '%');
//chart_instance2.initSearch(chart_instance2.loadYData, '%');
//
//
//// 初始化时间选择器
//initDateSelector2Day('#start_date3', '#end_date3');
//markDateTypeEvent('#charts3', '#start_date3', '#end_date3');
//
//// 新建图表
//var chart_instance3 = new Chart('main3', '900px', '600px', charts_data_uri+'?type=line', '#charts3');
//chart_instance3.showXBaseFrame();
//chart_instance3.loadXData(chart_instance3);
//chart_instance3.initSearch(chart_instance3.loadXData);
//
//
//// 初始化时间选择器
//initDateSelector2Day('#calc_start_date', '#calc_end_date');
//// 新建图表
//var chart_instance4 = new Chart('calc_main', '900px', '600px', charts_data_uri+'?type=calc_line');
//chart_instance4.showXBaseFrame();
