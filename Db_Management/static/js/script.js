var lineChartData = {
	//X坐标数据
	labels : ["周一","周二","周三","周四","周五","周六","周日"],
	datasets : [
		{	
			//统计表的背景颜色
			fillColor : "rgba(255,255,255,0)",
			//统计表画笔颜色
			strokeColor : "#d61d1d",
			//点的颜色
			pointColor : "#d61d1d",
			//点边框的颜色
			pointStrokeColor : "#fff",
			//鼠标触发时点的颜色
			pointHighlightFill : "#fff",
			//鼠标触发时点边框的颜色
			pointHighlightStroke : "rgba(255,220,220,1)",
			//Y坐标数据
			data : [500,550,700,450,600,508,680]
		},
		{
			fillColor : "rgba(255,255,255,0)",
			strokeColor : "rgba(92, 184, 92, 1)",
			pointColor : "rgba(23, 126, 23, 1)",
			pointStrokeColor : "#fff",
			pointHighlightFill : "#fff",
			pointHighlightStroke : "rgba(151,187,205,1)",
			data : [900,350,600,841,580,628,780]
		}
	]

}

window.onload = function(){
	var ctx = document.getElementById("canvas").getContext("2d");
	window.myLine = new Chart(ctx).Line(lineChartData, {
		responsive: true
	});
}