var d_json=null;

$(document).ready( function() {
    onLoadPage();
});

function get_dJson(){

    $.ajaxSetup({'async': false});
	var file='/js/diagnostics.json';

    $.getJSON(file, function(json) {
        d_json = json;
    }); 
    $("#diag_content").append("<label class='maintitle'>Uptime</label>");
    $.ajax(
            {
                type    : 'get',
                url     : '/cgi-bin/admin/about.cgi?msubmenu=about&action=view',
                success : function(req){
                    var split = req.split('\n');

                    for(var i=0; i<split.length;i++){
                        if(split[i].match('uptime')){
                            var uptime = split[i].trim().split('=');
                            $("#diag_content").append("<label>"+uptime[1]+"</label><br>");
                        }
                    }
                },
                error :function(){
                            $("#diag_content").append("<label> Uptime Error</label><br>");
                }
            }
          );
	$("#diag_content").append("<label class='maintitle'>SD Card</label>");
	
    
	if (capInfo.is_proxy_camera){
		if(sdInfo.status == 2){                                                                                                    
			$("#diag_content").append("<label>SD Card1 Mounted successfully </label><br>");
		}else{
			$("#diag_content").append("<label>SD Card1 Not inserted or mounted (Insert or format the SD card1) </label><br>");
		}
		if(sdInfo.status1 == 2){                                                                                                    
			$("#diag_content").append("<label>SD Card2 Mounted successfully </label><br>");
		}else{
			$("#diag_content").append("<label>SD Card2 Not inserted or mounted (Insert or format the SD card2) </label><br>");
		}
		if (capInfo.video_in == 4){
			if(sdInfo.status2 == 2){
				$("#diag_content").append("<label>SD Card3 Mounted successfully </label><br>");
			}else{
				$("#diag_content").append("<label>SD Card3 Not inserted or mounted (Insert or format the SD card3) </label><br>");
			}
			if(sdInfo.status3 == 2){
				$("#diag_content").append("<label>SD Card4 Mounted successfully </label><br>");
			}else{
				$("#diag_content").append("<label>SD Card4 Not inserted or mounted (Insert or format the SD card4) </label><br>");
			}
		}
	}
	else {
		if((capInfo["oem"] == 12) || (capInfo["oem"] == 19) || (capInfo["oem"] == 20) || (capInfo["oem"] == 21)){
			if(sdInfo.status == 1 ){
				$("#diag_content").append("<label>SD Card Inserted but not mounted (SD card format required to use) </label><br>");
			}else if(sdInfo.status == 2){
				$("#diag_content").append("<label>SD Card Mounted successfully </label><br>");
			}else{
				$("#diag_content").append("<label>SD Card Not inserted  </label><br>");
			}
		}
		else{
			for(var i=0; i<d_json[0]["sd card"].length; i++){
				$("#diag_content").append("<label>"+d_json[0]["sd card"][i]+"</label><br>");
			}
		}
	}
	if( capInfo.camera_module == "cv22_internal_isp" ){
		$("#diag_content").append("<label class='maintitle'>EMMC</label>");
	}	else{
		$("#diag_content").append("<label class='maintitle'>NAND</label>");
	}
	for(var i=0; i<d_json[1]["nand"].length; i++){
		$("#diag_content").append("<label>"+d_json[1]["nand"][i]+"</label><br>");
	}
	$("#diag_content").append("<label class='maintitle'>EEPROM</label>");
	for(var i=0; i<d_json[2]["eeprom"].length; i++){
		$("#diag_content").append("<label>"+d_json[2]["eeprom"][i]+"</label><br>");
	}
	$("#diag_content").append("<label class='maintitle'>Audio</label>");
	for(var i=0; i<d_json[3]["audio"].length; i++){
		$("#diag_content").append("<label>"+d_json[3]["audio"][i]+"</label><br>");
	}
	$("#diag_content").append("<label class='maintitle'>System Files</label>");
	for(var i=0; i<d_json[4]["system files"].length; i++){
		$("#diag_content").append("<label>"+d_json[4]["system files"][i]+"</label><br>");
	}

	$("#diag_content").append("<label class='maintitle'>NTP Status</label>");
    if(ntpInfo.ntp_on_off != 0){
	$("#diag_content").append("<label>NTP: Off</label><br>");
    }else{
	    $("#diag_content").append("<label>NTP: On</label><br>");
	    $("#diag_content").append("<label>Connect: "+ntpInfo.ntp_connect+"</label><br>");
	    $("#diag_content").append("<label>Last NTP Connected Date&Time: "+ntpInfo.last_datetime+"</label><br>");
    }
    
    $.ajaxSetup({'async': true});
}

function initValue()
{
	get_dJson();
	var file="ipnc.core";
	var check_file="ipnc.core.md5sum";
	
	var getFile='/'+file;
	if(FileExist(getFile)){
		$("#core_download").css("display","block");
		$("#core_caution").append("If you want to download the core dump file , press the Download button");
	}else{
		$("#core_download").css("display","none");
	}

	$("#core_download").click(function(e){
			download(file);
			setTimeout(function(){
				download(check_file);
			},1000);
	});
}
function download(file){
	var data;
	var getFile='/'+file;

	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", getFile, false); 
	rawFile.onreadystatechange = function () 
	{
		if(rawFile.readyState === 4)
		{
			if(rawFile.status === 200 || rawFile.status == 0)
			{
				data = rawFile.responseText;
			}
		}
	}
	rawFile.send();

	var blob = new Blob([data], { type: 'text/csv' });
	if (window.navigator.msSaveOrOpenBlob) {
		window.navigator.msSaveBlob(blob, file);
	}
	else {
		window.location = getFile;
	}
}
function FileExist(urlToFile) {
	var xhr = new XMLHttpRequest();
	xhr.open('HEAD', urlToFile, false);
	xhr.send();

	if (xhr.status == "404") {
		return false;
	} else {
		return true;
	}
}
function onLoadPage()
{
	initValue();
	initLanguage();
}

