var menu = "PTZ Setting";
//var settingList = ["parking_enabled", "powerup_enabled", "autoflip_enabled"];
var shortcut_mode = [ -1, -1, -1, -1, -1, -1 ]; // 0 : wiper, 1 : wiper routine, 2 : washer position , 3 : washer Routine , 4 : Wled, 5 : IR toggle

function getpreset(){
	$.ajax({
		type : 'get',
		url  : '/cgi-bin/ptz.cgi',
		async: false,
		data : 'getpreset=1' ,
		dataType: 'json',
		success : function(ret){
			console.log(ret);
//			if( ret.presetInfo == undefined ) return 0;
			presetInfo = ret.presetInfo ;
			for( var j = 0 ; j < shortcut_mode.length ; j++) // j : id - preset_no_0 ~ max
			{
				$("#preset_no_"+j).append("<option value='-1' >Select Preset</option>");
				//Load Preset, shortcuts
				for( var i = 0 ; i < 255 ; i++ ){
					if( typeof(presetInfo) != 'undefined' ) {
						if( presetInfo[i] != undefined ) {
							$("#preset_no_"+j).append("<option value="+ i +">["+pad(i+1,3)+"]"+ presetInfo[i]["name"] + "</option>");
							// shortcut mode saving
							if(presetInfo[i]["shortcut"] != 0)
								shortcut_mode[(presetInfo[i]["shortcut"]) - 1] = i;
						}
						else {
							$("#preset_no_"+j).append("<option value="+ i +">["+pad(i+1,3)+"]"+ "Not Set" + "</option>");
						}
					}
					else // preset empty
					{
						$("#preset_no_"+j).append("<option value="+ i +">["+pad(i+1,3)+"]"+ "Not Set" + "</option>");
					}
				}
			}
		}
	}).done(function(){ console.log("요청 성공시 호출") })
		.fail(function(){ console.log("fail") })
		.always(function(){ console.log("always") });
}

function initUI() {
	if( capInfo.have_cds == 0)
		shortcut_mode = [ -1, -1, -1, -1 ]; // non-ir model Wled,IR delete

	for(var i = 0; i < shortcut_mode.length; i++) 
	{
		$("#preset_no_content").append("<label class='subtitle'><span tkey='shortcut"+i+"'></span></label><div class='select'><select id='preset_no_"+i+"'></select></div><br>");
	}
}
function initValue()
{
	//shortcuts
	for(var i = 0; i < shortcut_mode.length; i++)
	{
		$("#preset_no_"+i).val(shortcut_mode[i]);
	}
	
}
function initEvent()
{
	//shortcuts
	$("#btOK").on("click" , function(){
		var changed = 0;
		for(var i=0; i < shortcut_mode.length; i++)
		{
			if ( shortcut_mode[i] != $("#preset_no_"+i).val() ) // check changed value
			{
				changed = 1;

				var data = "savepreset="+$("#preset_no_"+i).val();
				data += "&shortcut="+(i+1);
				console.log("data check");
				console.log(data);
				$.ajax({
					type:"get",
					url: "/cgi-bin/ptz.cgi",
					data: data,
					success: function(){
						//settingSuccess(menu, null);
						//refreshMenuContent();
					},
					error: function(){
						pop_msg = getLanguage("msg_fail_retry");
						settingFail(menu, pop_msg);
						refreshMenuContent();
					}
				});
			}
		}

		if (changed == 0) // nothing changed
		{
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		else
		{
			settingSuccess(menu, null);
			refreshMenuContent();
		}
	});
}
function pad(n, width) {
      n = n + '';
      return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}

function onLoadPage() 
{
	initUI();
	getpreset();
	initValue();
	initEvent();
}
$(document).ready( function() {
    onLoadPage();
});
