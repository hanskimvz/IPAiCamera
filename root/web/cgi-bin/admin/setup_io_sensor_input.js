var menu = getLanguage("setup_alarm_config");
//var settingList = ["sun", "mon" , "tue", "wed", "thu", "fri", "sat", "shour", "smin", "ehour", "emin", "output", "duration", "transfer" ];   // 
var settingList = [ "mode", "mode1"];   // 

//CHART.S
var chart_index = 0;

var intervalID;
var selectedPoint;
var backgroundColor;
var detectLineValue;
var borderColor;
var myLineChart;
var data;
var span_Text_0;
var span_Text_1;
var option;


function addData_ADC0(chart, value_acc_0) {
        chart.data.datasets[0].data.push(value_acc_0);
}
function addData_ADC1(chart, value_acc_1) {
        chart.data.datasets[1].data.push(value_acc_1);
}
function removeData(chart) {
        chart.data.datasets[0].data.splice(0,1);
        chart.data.datasets[1].data.splice(0,1);
}

function movedata(){
    try{
        span_Text_0 = document.getElementById("ADC0").innerText;
        span_Text_1 = document.getElementById("ADC1").innerText;
        //console.log(span_Text_0+ " " + span_Text_1);
        if(myLineChart.data.datasets[0].data.length <= 50){
            addData_ADC0(myLineChart, span_Text_0);
            addData_ADC1(myLineChart, span_Text_1);
        }
        else
        {
            removeData(myLineChart);
            addData_ADC0(myLineChart, span_Text_0);
            addData_ADC1(myLineChart, span_Text_1);
        }
    }
    catch(e)
    {
        //clearInterval(intervalID);
        //intervalID = void 0;
    }

    //console.log(span_Text);
    myLineChart.update();
}

function initChart()
{
	checkMotion("ADC0",3); //
	detectLineValue= 1.0;
	d23= 2.5;
	data = {
        labels: ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""],
        datasets: [
            {
                label: "Alarm 0",
                fill: false,
                lineTension: 0.1,
                backgroundColor: backgroundColor,
                borderColor: "rgba(255,0,0,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 0,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 0,
                pointHitRadius: 0,
                data: []
            },
            {
                label: "Alarm 1",
                fill: false,
                lineTension: 0.1,
                backgroundColor: backgroundColor,
                borderColor: "rgba(255,127,0,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 0,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 0,
                pointHitRadius: 0,
                data: []
            },
            {
              label: 'Up',
	      fill: false,
              data: [detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue,detectLineValue],
              borderColor: "rgba(192,192,192,1)",
              pointRadius: 0,
              type: 'line'
            },
            {
              label: 'Down',
		fill: false,
              data: [d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23,d23],
              borderColor: "rgba(192,192,192,1)",
              pointRadius: 0,
              type: 'line'
	    }	
	]
    };
    option = {
        showLines: true,
        legend: {
                display: false
        },
        tooltips: {
                enabled: false
        }
    };
    myLineChart = Chart.Line('ADCChart0',{
        data:data,
       //options:option
        options: {
            responsive: false,
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: 3.5,
                        stepSize : 0.5,
                    }
                }]
            },
        legend: {
                display: true
        },
        tooltips: {
                enabled: false
        }
        }
    });

    intervalID = setInterval(movedata, 500);
}
//CHART.E


function initUI()
{
	if(capInfo['oem'] == 19 || capInfo['oem'] == 20 || capInfo['oem'] == 21)
	{
		$("#alarm_open").attr("tkey","setup_alarm_open2");
		$("#alarm_close").attr("tkey","setup_alarm_close2");
	}
	if( alramInfo['mode'] == '0')    $("[name=mode][value=0]").trigger("click");
	else if(alramInfo['mode'] == '1')    $("[name=mode][value=1]").trigger("click");
	else if( alramInfo['mode'] == '2')    $("[name=mode][value=2]").trigger("click");
	else if( alramInfo['mode'] == '3')    $("[name=mode][value=3]").trigger("click");

	if( alramInfo['mode1'] == '0')    $("[name=mode1][value=0]").trigger("click");
	else if(alramInfo['mode1'] == '1')    $("[name=mode1][value=1]").trigger("click");
	else if( alramInfo['mode1'] == '2')    $("[name=mode1][value=2]").trigger("click");
	else if( alramInfo['mode1'] == '3')    $("[name=mode1][value=3]").trigger("click");

	if(capInfo.camera_type == "CUBE")
	{
		initChart();
	}else{
		$("#optDeviceTime4").remove();
		$("#optDeviceTime4_label").remove();
		$("#optDeviceADC4").remove();
		$("#optDeviceADC4_label").remove();
        $("#alarm_div1").remove();
        $("#btOK1").remove();
		$("#alarm_chart").remove();
	}
}

function checkDependency(index)
{
   
}
function initEvent()
{
	menu = getLanguage("setup_alarm_config");
	$("#btOK0").click(function(event) {
		function onSuccessApply(msg) {
			var tmp= msg.trim().split('\n');
			console.log(tmp);
			var response = tmp[0];
			if(response == "OK") {		
				alramInfo[settingList[0]] = $("[name="+settingList[0]+"]:checked").val();
				settingSuccess(menu, null);
			} else {
				settingFail(menu, tmp[1]);
			}
			refreshMenuContent();
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
		}	
		var data = null;
		var newValue;
		var orgValue;
		var obj = $("#" + settingList[0]);
		if(($("[name = "+settingList[0]+"]").prop("type")) == "radio") {
			newValue = $("[name="+settingList[0]+"]:checked").val();
		}
		orgValue = alramInfo[settingList[0]];
		console.log(orgValue + " - " + newValue );
		if( orgValue != newValue ) {
			if( data == null)
				data =  "mode=" + newValue;
			else
				data += "&mode=" + newValue;
		}
		if(data != null) {
			data = "msubmenu=sensor&action=apply&id=0&"+ data;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/io.cgi",
			cache   : false,
			data: data,
			success: onSuccessApply, 
			error: onFailApply
		});
	});
	 $("#btOK1").click(function(event) {
                function onSuccessApply(msg) {
                        var tmp= msg.trim().split('\n');
                        console.log(tmp);
                        var response = tmp[0];
                        if(response == "OK") {
                                alramInfo[settingList[1]] = $("[name="+settingList[1]+"]:checked").val();
                                settingSuccess(menu, null);
                        } else {
                                settingFail(menu, tmp[1]);
                        }
                        refreshMenuContent();
                }
                function onFailApply() {
                        settingFail(menu, getLanguage("msg_fail_retry"));
                        refreshMenuContent();
                }

                var data = null;
                var newValue;
                var orgValue;

                var obj = $("#" + settingList[1]);
                if(($("[name = "+settingList[1]+"]").prop("type")) == "radio") {
                      newValue = $("[name="+settingList[1]+"]:checked").val();
                }
                orgValue = alramInfo[settingList[1]];
                console.log(orgValue + " - " + newValue );
                if( orgValue != newValue ) {
                        if( data == null)
                                data =  "mode=" + newValue;
                        else
                               data += "&mode=" + newValue;
                }
                console.log(data);
                if(data != null) {
                        data = "msubmenu=sensor&action=apply&id=1&"+ data;
                }else {
                        settingFail(menu, getLanguage("msg_nothing_changed"));
                        return ;
                }
                $.ajax({
                        type:"get",
                        url: "/cgi-bin/admin/io.cgi",
                        cache   : false,
                        data: data,
                        success: onSuccessApply,
                        error: onFailApply
                });
        });

}
/*
function SetTextBoxEnabled(optMode)
{
	if( $("[name=alarmactivation]:checked").val() == "0" )
	{
		$("#alarmin_setting").find("*").prop("disabled", false);
	} 
	else 
	{
		$("#alarmin_setting").find("*").prop("disabled", true);
	}
}*/

function onLoadPage()
{
	initEvent();
	initUI();
}

$(document).ready( function() {

	onLoadPage();

});
