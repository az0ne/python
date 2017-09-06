$(function () {
    var $input = $('.rcABP');
    // 因为span#rcTB的css设置了float: right;
    //var firstInput = function () {
    //    return $('span#rcTB:last')
    //};
    //var lastInput = function () {
    //    return $('span#rcTB:first')
    //};
    var equation_options_url = '/operation/charts/line_charts/equation_options/';

    var lastInput = function () {
        return $('span#rcTB:last')
    };
    var firstInput = function () {
        return $('span#rcTB:first')
    };

    function markParam(param) {
        return '<span class="wordwrap" id="rcTB">' + param + '</span>'
    }

    function markInput(param) {
        if (firstInput().text() == '0') {
            $input.html(markParam(param));
        } else {
            //$input.prepend(markParam(param));
            $input.append(markParam(param));
        }
    }

    // 删除输入框中最后一个字符
    function deleteTheLastKeyOfInput() {
        if ($input.children().length == 1) {
            $input.html(markParam(0));
        } else {
            lastInput().remove();
        }
    }

    // 清空输入框
    function clearInput() {
        $input.html(markParam(0));
    }

    function replaceAll(str, finds, replaces) {
        for (var i = 0; i < finds.length; i++) {
            str = str.replace(new RegExp(finds[i], 'g'), replaces[i])
        }
        return str
    }

    function paramsToString(finds, replaces) {
        var ps = buildEquation();
        finds = finds ? finds : [];
        replaces = replaces ? replaces : [];
        finds = finds.concat([$('#rcMul').val(), $('#rcDiv').val(), $('#rcSub').val()]);
        replaces = replaces.concat(['*', '/', '-']);

        console.log('real: '+ps);
        ps = replaceAll(ps, finds, replaces);
        console.log('replace: '+ps);
        return ps
    }

    function buildEquation() {   // 构造算式
        var cs = $input.children();
        var ps = '';
        //for (var i = cs.length - 1; i >= 0; i--) {
        //    ps += $(cs[i]).text();
        //}
        for (var i = 0; i < cs.length; i++) {
            ps += $(cs[i]).text();
        }
        return ps
    }

    function saveEquation() {   // 保存算式
        var equation = buildEquation();

        var res = checkCalculate();

        if (res) {
            layer.prompt({
                title: '请简要描述公式，并确认',
                formType: 0 //prompt风格，支持0-2
            }, function(description){
                $.ajax({
                    url: equation_options_url,
                    data: {action: 'add', equation: equation, description: description},
                    dataType: 'json',
                    type: 'POST',
                    beforeSend: function () {
                        layer.load();
                    },
                    success: function (data) {
                        if (data.success) {
                            saveEquationSuccess(equation, description, data.data.id);
                            layer.closeAll('loading');
                            layer.msg('保存成功!', {time: 1000});
                        }
                        else {
                            layer.closeAll('loading');
                            layer.msg(data.msg, {time: 2000})
                        }
                    },
                    error: function () {
                        layer.closeAll('loading');
                        layer.msg('服务器异常', {time: 1000, icon: 5});
                    }
                });
            });
        }
    }

    function saveEquationSuccess(equation, description, e_id) {
        var html = '<tr><td colspan="4" class="4col">' +
            '<div class="zero-delete"><span class="equation-delete" data-equation="'+ equation +'" data-id="'+ e_id +'" title="删除公式">x</span></div>' +
            '<input class="rcOpdB b_xlText customEquation" id="'+ e_id +'" type="button" value="'+ equation +'" style="width: 354px;">' +
            '</td></tr>';
        $('#calc_table tbody').append(html);

        $('#'+e_id).mouseover(function () {
            layer.tips("<span class='wordwrap'>公式："+equation+" </br>描述："+description+"</span>", this, {
                tips: [4, '#3595CC'],
                time: 0
            });
        }).mouseout(function() {
            layer.closeAll('tips');
        }).click(function () {
            markInput($(this).val());
        }).prev().children().click(function () {
            deleteEquation(this);
        });
    }

    function deleteEquation(ed) {
        layer.confirm('确定要删除公式：'+$(ed).attr('data-equation')+' 吗？', {
            btn: ['确定', '取消']
        }, function () {
            $.ajax({
                url: equation_options_url,
                data: {action: 'delete', id: $(ed).attr('data-id')},
                dataType: 'json',
                type: 'POST',
                beforeSend: function () {
                    layer.load();
                },
                success: function (data) {
                    if (data.success) {
                        $(ed).parents('tr').remove();

                        layer.closeAll('loading');
                        layer.msg('删除成功!', {time: 1000});
                    }
                    else {
                        layer.closeAll('loading');
                        layer.msg(data.msg, {time: 2000});
                    }
                },
                error: function () {
                    layer.closeAll('loading');
                    layer.msg('服务器异常', {time: 1000, icon: 5});
                }
            });
        }, function () {

        })
    }

    function checkCalculate() {
        try {
            var finds = [];
            var replaces = [];
            var variables = $('.calc_variable');

            // 构造要替换的变量名
            for (var i = 0; i < variables.length; i++) {
                finds.push($(variables[i]).val());
                replaces.push(1.1);
            }
            eval(paramsToString(finds, replaces)); // 验证表达式是否有效
            // test
            //$input.html(markParam(answer));
            return finds;
        } catch (error) {
            layer.alert('错误的表达式', {icon: 5});
            return false;
        }
    }

    function calcTrendChart() {
        var real_data = $('.calc-form-inline').serializeArray();
        var params = {};
        $.each(real_data, function (i, field) {
            params[field.name] = field.value;
        });
        chart_instance4.loadCalcData(chart_instance4, params, paramsToString())
    }

    $(document).ready(function () {
        $('.rcOpdB, .rcOptB').click(function () {
            markInput($(this).val());
        });

        // 后退键事件
        $('#rcBB').unbind().click(function () {
            deleteTheLastKeyOfInput();
        });

        // C键事件
        $('#rcClD').unbind().click(function () {
            clearInput();
        });

        // 保存公式
        $('#rcSave').unbind().click(function () {
            saveEquation();
        });

        $('#calc_search_btn').unbind().click(function () {
            var finds = checkCalculate();
            if (!finds) {
                return false;
            }
            //chart_instance4.showXBaseFrame();
            calcTrendChart();
        });

        $('.customEquation').mouseover(function () {
            layer.tips("<span class='wordwrap'>"+$(this).attr('data-title')+"</span>", this, {
                tips: [4, '#3595CC'],
                time: 0
            });
        }).mouseout(function() {
            layer.closeAll('tips');
        });

        $('.equation-delete').click(function () {
            deleteEquation(this);
        });
    });
});
