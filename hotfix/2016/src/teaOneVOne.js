/*! LPS4.0 2016-12-19
 */
$(function() {
	function e(e) {
		var t = $(e).attr("pop_href");
		void 0 != t && $.ajax({
			type: "GET",
			url: t,
			dataType: "json",
			success: function(e) {
				console.log(e), $(".zy_yourHomework3 .pt>span").html(e.papertitle), a = e.quizs, o(), $("#yourHomework").modal("hide"), $("#yourHomework3").modal("show")
			},
			error: function() {
				alert("service data error")
			}
		})
	}

	function t(e) {
		var t = a[e - 1];
		$(".zy_yourHomework3 .ptt").html(e + ".&nbsp;" + t.question);
		var o = "",
			i = t.answer,
			n = 0;
		for(var s in i) {
			var r = "";
			t.user_choose == l[n] && t.user_choose != t.correct && (r = "error"), t.correct == l[n] && (r = "right"), o += '<li class="' + r + '"><span>' + l[n] + "</span>" + i[l[n]] + "</li>", n++
		}
		$(".zy_yourHomework3_div ul").html(o)
	}

	function o() {
		s = a.length;
		for(var e = "", o = 0; s > o; o++) {
			var i = a[o],
				n = "aH";
			i.user_choose != i.correct && (n = "error"), e += '<a class="an ' + n + '" num="' + (o + 1) + '"></a>'
		}
		$(".zy_yourHomework3 .examinationBottom>.znum").html(e), $(".zy_yourHomework3 .examinationBottom a").unbind().click(function() {
			t($(this).attr("num")), $(this).addClass("active").siblings().removeClass("active")
		}).eq(0).trigger("click")
	}

	function i(e) {
		var t = $(e).attr("pop_href");
		void 0 != t && $.ajax({
			type: "GET",
			url: t,
			dataType: "html",
			success: function(e) {
				$("#yourHomework").modal("hide"), $("#yourHomework2").html(e), $("#yourHomework2").modal("show")
			},
			error: function() {
				alert("service data error")
			}
		})
	}

	function n(e) {
		$.ajax({
			type: "GET",
			url: e,
			dataType: "html",
			success: function(e) {
				if(!$(".modal-backdrop").length>0){
				$("#yourHomework").html(e), $("#yourHomework").modal({
					show: !0,
					keyboard: !1,
					backdrop: "static"
				})
				}
			}
		})
	}
	$(".teacherICO").on("mouseover", function() {
		layer.tips($(this).attr("title"), $(this), {
			tips: [1, "#333"]
		})
	}), $(".tabTitle>span").on("click", function() {
		$(this).addClass("cur").siblings().removeClass("cur"), $(".tabCon>div").eq($(this).index()).addClass("cur").siblings().removeClass("cur")
	});
	var a = [],
		s = 0,
		l = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
	$("#yourHomework").on({
		click: function() {
			i(this)
		}
	}, ".zy_yourHomework .liH .yourHomeworkProject"), $("#yourHomework").on({
		click: function() {
			e(this)
		}
	}, ".zy_yourHomework .liH .yourHomeworkTest");
	var r, c = function(e) {
			return(e + "").replace(/[^\x00-\xff]/g, "aa").length
		},
		d = function(e) {
			var t = "";
			t += '<div id="imgzoom"><i class="imgzoom-close"></i><div id="imgzoom-image-ctn">', t += '<img class="img" src="' + e + '" alt="">', t += "</div></div>", $("body").append(t), console.log(t);
			var o = $("#imgzoom-image-ctn");
			o.find(".img").load(function() {
				o.css({
					left: "50%",
					top: "50%",
					marginLeft: -o.outerWidth() / 2,
					marginTop: -o.outerHeight() / 2
				})
			}), $("#imgzoom").fadeIn("fast", "linear").css({
				"z-index": "1100",
				top: "0px"
			}), $(".imgzoom-close").on("click", function() {
				$("#imgzoom").remove()
			})
		},
		u = "";
	$("#yourHomework2").on("show.bs.modal", function() {
		$(".yourHomeworkD a").unbind().hover(function() {
			layer.tips($(this).attr("v"), $(this), {
				tips: [1, "#68c8b6"],
				time: 2e3
			})
		}, function() {}).click(function() {
			$(this).addClass("aH").siblings().removeClass("aH")
		})
	}), $(".personal_select").iSimulateSelect({
		width: 132,
		height: 0,
		selectBoxCls: "personal_info_selectD",
		optionCls: "personal_info_selectD_Op"
	}), $(".personal_select").change(function() {
		_order = $(this).val(), _url = window.location.pathname + "?s_order=" + _order, window.location.href = _url
	}), $(".teacherStulist li").unbind().hover(function() {
		$(this).children(".s_details").addClass("HH")
	}, function() {
		$(this).children(".s_details").removeClass("HH")
	}), $(".zy_onoffBtn").unbind().click(function() {
		$(this).toggleClass("on"), setTimeout("startClass()", 600)
	}), $("#yourHomework").on({
		click: function() {
			$(this).parent().parent().toggleClass("liH"), $(this).parents("li").find("dd").removeAttr("onclick"), p.jScrollPane({
				mouseWheelSpeed: 10
			})
		}
	}, ".zy_yourHomework_divUL li>.a .s1"), $(".modal").on({
		click: function() {
			$("#yourHomework").modal("hide"), $("#yourHomework2").modal("hide")
		}
	}, ".zy_newclose"), $(".zy_newclose").on("click", function() {
		$("#yourHomework3").modal("hide")
	}), $(".teacherTasklist li span").on("click", function() {
		var e = $(this).attr("pop_href");
		void 0 != e && (u = e, r = $(this), n(e))
	});
	var p;
	$("#yourHomework").on("shown.bs.modal", function() {
		p = $(".zy_yourHomework").jScrollPane({
			mouseWheelSpeed: 80
		})
	}), $("#yourHomework").on({
		click: function() {
			var e = $(this).attr("pop_href");
			void 0 != e && $.ajax({
				type: "GET",
				url: e,
				dataType: "html",
				success: function(e) {
					$("#yourHomework").modal("hide"), $("#yourHomework2").html(e), $("#yourHomework2").modal("show")
				},
				error: function() {
					alert("service data error")
				}
			})
		}
	}, ".zy_yourHomework_divUL li > .a > .s2"), $("#yourHomework").on({
		click: function() {
			var e = $(this).attr("pop_href");
			void 0 != e && $.ajax({
				type: "GET",
				url: e,
				dataType: "html",
				success: function(e) {
					$("#yourHomework").modal("hide"), $("#yourHomework2").html(e), $("#yourHomework2").modal("show")
				},
				error: function() {
					alert("service data error")
				}
			})
		}
	}, ".zy_yourHomework_divUL li > .a > .yhbtn"), $("#yourHomework2").on({
		click: function() {
			$("#yourHomework2").modal("hide"), $("#yourHomework").modal("show")
		}
	}, ".modal-dialog .pt a"), $(".zy_yourHomework3 .pt a").on("click", function() {
		$("#yourHomework3").modal("hide"), $("#yourHomework").modal("show")
	}), $(".zy_yourHomework3 .examinationBottom .ebtn.prev").unbind().click(function() {
		$(".zy_yourHomework3 .examinationBottom a.active").prev().trigger("click")
	}), $(".zy_yourHomework3 .examinationBottom .ebtn.next").unbind().click(function() {
		$(".zy_yourHomework3 .examinationBottom a.active").next().trigger("click")
	}), $("#yourHomework2").on({
		click: function(e) {
			e.stopPropagation(), e.preventDefault(), d($(this).find("img").attr("src"))
		}
	}, ".zy_yourHomework2_divImg > a"), $("#yourHomework2").on("shown.bs.modal", function() {
		$(".zy_yourHomework2").jScrollPane({
			mouseWheelSpeed: 100
		})
	});
	var m = $(".yourHomeworkD a");
	m.each(function() {
		$(this).on("click", function() {
			$(this).addClass("aH").siblings().removeClass("aH")
		})
	}), $("#yourHomework2").on({
		click: function() {
			var e = $("#desc-remark").val(),
				t = Math.ceil(c(e) / 2);
			0 == $(".yourHomeworkD a.aH").length || "" == e ? layer.msg("请评分，写评语！") : t > 200 ? layer.msg("已超出200字！") : $.ajax({
				type: "POST",
				url: $("#project_marking").val(),
				data: {
					score: $(".Arial").filter(".aH").text(),
					desc: e
				},
				dataType: "json",
				success: function(e) {
					"success" == e.status || "'LocMemCache' object has no attribute 'client'" == e.message ? ($("#yourHomework2").modal("hide"), layer.msg("评分成功！"), 0 == e.number ? r.children("i").remove() : r.children("i").html(e.number), n(u)) : layer.msg(e.message)
				}
			})
		}
	}, "#remark-submit")
});