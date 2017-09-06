
define(["lodash"], function(_) {
"use static";


var $provinceSelect = $("select[name='province']"),
    $citySelect = $("select[name='city']");

$provinceSelect.on("change", function(event) {
    // 更新 $citySelect
    var provinceId = $provinceSelect.val();

    $.get(window.mz.url.get_city_by_province_id, {
        province_id: provinceId

    }, "json").done(function(res) {
        if (res.length > 0) {
            var citysHtml = "",
                compiled = _.template('<option value="<%= id %>"><%= name %></option>');

            _.forEach(res, function(city) {
                citysHtml += compiled(city);
            });

            $citySelect.html(citysHtml);
        }
    }).error(function(xhr) {
    
    });
});

// 根据 $citySelect.val() 初始化 $provinceSelect
var currentCityId = $citySelect.data("city_id");
if (currentCityId) {
    $.get(window.mz.url.get_province_id_by_city_id, {
        city_id: currentCityId
    }).done(function(res) {
        var provinceId = res.province_id;
        $provinceSelect.find("[value=" + provinceId + "]").attr("selected", "");
        $provinceSelect.trigger("change");
    }).error(function(xhr) {
        
    });
} else {
    $provinceSelect.trigger("change");
}


});


