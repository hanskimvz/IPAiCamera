/*
var device=0;
var always=1;
var week_sun=1;
var week_mon=1;
var week_tue=1;
var week_wed=1;
var week_thu=1;
var week_fri=1;
var week_sat=1;
var start_hour=0;
var start_min=0;
var end_hour=23;
var end_min=59;
var action_output=0;
var action_duration=20000;
var action_transfer=1;
var action_camerafunction=3000;
var action_functionindex=0;
*/

var selDurationIdx = new Object;
selDurationIdx['3000'] = 0;
selDurationIdx['5000'] = 1;
selDurationIdx['10000'] = 2;
selDurationIdx['20000'] = 3;
selDurationIdx['30000'] = 4;

var selAlarmInIntervalIdx = new Object;
selAlarmInIntervalIdx['3000'] = 0;
selAlarmInIntervalIdx['5000'] = 1;
selAlarmInIntervalIdx['10000'] = 2;
selAlarmInIntervalIdx['20000'] = 3;
selAlarmInIntervalIdx['30000'] = 4;

function onLoadOption(obj, max)
{
	for(i = 0 ; i < max  ; i++)
	{
		opt = document.createElement("option");
		opt.innerText = i;
		opt.value = i;
		obj.appendChild(opt);
	}
	//todo: adding selected value;
}

function getElement(name, val)
{
	//$("input:text[name='n_t_ip']").val(ip);
	//$("input:radio[name='n_t_dhcp']:radio[value='0']").attr("checked", true);

	var type = $("[name="+ name + "]").attr('type');

	if(type == 'text')
	{
		return $("[name=" + name + "]");
	}
	else if(type == 'radio')
	{
		return $("input:radio[name=" + name + "]:radio[value=" + val +"]");
	}
}

var h = new Object();

function onLoadPage()
{
	if (device == 0)
		getElement('optDeviceType', '0').attr("checked", true);
	else
		getElement('optDeviceType', '5').attr("checked", true);

	if (always != 0) {
		getElement('optActivationTime', '1').attr("checked", true);
		onClickActivationTime(1);
	} else {
		getElement('optActivationTime', '0').attr("checked", true);
		onClickActivationTime(0);
	}

	onLoadOption(document.getElementById('selSHour'), 24);
    onLoadOption(document.getElementById('selSMin'), 60);
    onLoadOption(document.getElementById('selEHour'), 24);
    onLoadOption(document.getElementById('selEMin'), 60);

	selSHour.selectedIndex = start_hour;	
	selSMin.selectedIndex = start_min;	
	selEHour.selectedIndex = end_hour;	
	selEMin.selectedIndex = end_min;	


	chkSun.checked = week_sun;
	chkMon.checked = week_mon;
	chkTue.checked = week_tue;
	chkWed.checked = week_wed;
	chkThu.checked = week_thu;
	chkFri.checked = week_fri;
	chkSat.checked = week_sat;
	
	//selTransfer.selectedIndex = action_transfer ? 1 : 0;	
	selWLED.selectedIndex = action_output ? 1 : 0;

	selDuration.selectedIndex = selDurationIdx[action_duration];	
	selAlarmInInterval.selectedIndex = selAlarmInIntervalIdx[action_camerafunction];	
}

function onClickActivationTime( nIndex )	// nIndex = always
{
	var flag = false;
	if ( nIndex == 1 )	flag = true;
	
	chkSun.disabled = chkMon.disabled = chkTue.disabled = chkWed.disabled = chkThu.disabled = chkFri.disabled = chkSat.disabled = flag;
	document.getElementById('selSHour').disabled = flag;
	document.getElementById('selSMin').disabled = flag;
	document.getElementById('selEHour').disabled = flag;
	document.getElementById('selEMin').disabled = flag;
}

function onChangeCameraAction()
{
}

function checkForm()
{
	return true;
}

function getRadioValue(obj)
{
	var i;
	for (i=0; i<obj.length; i++)
		if (obj[i].checked) return obj[i].value;
	
	return 0;
}
function getCheckValue(obj)
{
	if (obj.checked) return 1;
	return 0;
}

function is_Changed()
{
	if (selSHour.value * 60 + selSMin.value > selEHour.value * 60 + selEMin.value) {
		alert("Start Time must be less than End Time.");
		return false;
	}

	data += "&emin=" +  selEMin.value;

    var data = "submenu=alarmin1&action=apply";

	changed = true; // fixeme: check params

    if (getElement('optDeviceType', '0').is(":checked") ) {
		data += "&device=0";
	} else {
		data += "&device=5";
	}
    if (getElement('optActivationTime', '0').is(":checked") ) {
		data += "&activation=0;"
	} else {
		data += "&activation=1;"
	}
	data += "&interval=" +  selAlarmInInterval.value;
	data += "&sun=" +  getCheckValue(chkSun);
	data += "&mon=" +  getCheckValue(chkMon);
	data += "&tue=" +  getCheckValue(chkTue);
	data += "&wed=" +  getCheckValue(chkWed);
	data += "&thu=" +  getCheckValue(chkThu);
	data += "&fri=" +  getCheckValue(chkFri);
	data += "&sat=" +  getCheckValue(chkSat);
	data += "&shour=" +  selSHour.value;
	data += "&smin=" +  selSMin.value;
	data += "&ehour=" +  selEHour.value;
	data += "&emin=" +  selEMin.value;
	data += "&output=" +  selWLED.value;
	data += "&duration=" +  selDuration.value;
	//data += "&transfer=" +  selTransfer.value;

	if( changed )
	{
		return data;
	}
	else
	{
		alert("Nothing changed.");
		return false;
	}
}

function onClickApply()
{
	var param = is_Changed();

	if(param != false)
	{
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/admin/event.cgi',
			data : param,
			cache	: false,
			success : onSuccess,
			error	: onFail
		});
	}
}

function onSuccess(req)
{
	alert(req);
	onClickMenu();
//	document.location.reload();
}

function onFail(req)
{
	alert("fail");
	onClickMenu();
//	document.location.reload();
}

$(document).ready( function() {
    onLoadPage();
});
