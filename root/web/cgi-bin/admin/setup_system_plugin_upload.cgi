<?
//udp_version=1.0.5
require('../_define.inc');
require("../class/system.class");
$system_conf = new CSystemConfiguration();
?>
<!DOCTYPE html>
<html>
<head>
	<title>PLUGIN UPLOAD</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="setup_system_plugin_config"></span></div>
	<div id="plugins_list">
		<div class="content">
			<label class="maintitle"><span tkey="setup_plugin_list"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead >
						<tr class="headline">
							<th class="athird"><span tkey="setup_name"></span></th>
							<th class="athird"><span tkey="setup_version"></span></th>
							<th class="athird"><span tkey="setup_status"></span></th>
						</tr>
					</thead>
					<tbody id="result_table">
					</tbody>
				</table>
			</div>
		</div>
		<center>
			<button id="configuration" class="button width_120"><span tkey="setup_configuration"></span></button>
			<button id="startstop" class="button width_100" style="padding: 0;"><span tkey="setup_start_stop"></span></button>
			<button id="uninstall" class="button width_100"><span tkey="setup_uninstall"></span></button>
			<button id="logs" class="button width_100"><span tkey="setup_plugin_logs"></span></button>
		</center>
	</div>
	<div class="content isSelectPL" style='display:none';>
		<div class="maintitle"><span tkey="setup_system_plugin_setting"></span></div>
		<div class="subtitle bottom_5" style="float:left;"><span tkey="setup_system_import_plugin"></span></div>
		<div id="file" class="filebox disign_sel" style="margin-top: 7px; margin-bottom: 7px;">			
		<input type="file" accept=".dat" name="plugin_file" id="impFileInput" onchange="impFunction()"/>
		<label for="impFileInput" tkey="setup_system_selectimport" style="float:left;">Select Import File</label><span id="impdemo"></span>
		</div><br>
		<div id="bia_caution" style="margin:4px 10px;font-size:11px; color:#727272;"></div>
		<label id="imp_status"></label>
		<div id="impProgressbox" >
			<div id="impProgressbar" class="stripes"><div id="impStatustxt">0%</div></div >
		</div>
		<center>
			<button type="button" class="button width_100" id="import-btn" disabled><span tkey="setup_system_import"></span></button>
			<button class="button width_100" id="export"><span tkey="setup_system_export"></span></button>
			<button class="button" id="fd"><span tkey="setup_system_defaultsetting"></span></button>
		</center>
	</div>
	<div class="content marginjpn1">
		<div class="maintitle"><span tkey="setup_system_plugin_infomation"></span></div>
		<div style="display:flex;">
		<div class="subtitle" style="align-items: center;"><span tkey="setup_system_plugin_description"></span></div>
		<div id="description" style="flex: 1;word-break: break-all;line-height:14px;margin-top:10.5px;margin-left:4px;"></div>
		</div>
		<div class="subtitle"><span tkey="setup_system_dependency"></span></div><br>
		<div class="" style="margin-bottom:2.5px;margin-left:25px; display:inline-block;width:115px;"><span tkey="setup_system_base_firmware"></span></div>
		<label id="baseFirm"></label><br>
		<div class="" style="margin-bottom:2.5px;margin-left:25px; display:inline-block;width:115px;"><span tkey="setup_system_plugin_dependency"></span></div>
		<label id="pluginDepen"></label>
	</div>
	<form action="/cgi-bin/admin/plugin_upload" method="post" enctype="multipart/form-data" id="MyPluginUploadForm">
		<div class="content">
			<div class="maintitle"><span tkey="setup_system_pluginupdate"></span></div>
      <div>
        <div class="subtitle s3l" style="display:none"><span tkey="setup_plugin_usage"></span></div><label class="s3l" id="contentUsage" style="display:none"></label><br>
      </div>
      <div style="display: flex; align-items: center;">
        <div class="subtitle bottom_5"><span tkey="setup_system_pluginfile"></span></div>
        <div id="file" class="filebox disign_sel">			
        <input type="file" accept=".enc" name="plugin_file" id="FileInput" onchange="myFunction()"/>
        <label for="FileInput" tkey="setup_system_selectfile" style="float:left;">Select File</label><span id="demo"></span>
        </div><br>
      </div>
			<label id="fw_status"></label>
			<div id="progressbox" >
				<div id="progressbar" class="stripes"><div id="statustxt">0%</div></div >
			</div>
		</div>
		<center>
			<!--<input type="submit" class="button" id="submit-btn" value="Start F/W update" tkey="setup_system_startfwupdate" disabled /> -->
			<button class="button long" id="submit-btn" disabled><span tkey="setup_system_startpluginupdate"></span></button>
		</center>	
	</form>
	
	<script>
		var MaxNumRecord		= <? echo MAX_RECORDING_JOB ?>;
		var MaxNumTrigger		= <? echo MAX_NUM_TRIGGER ?>;
		var fwInfo;
		var fwDate;
		<?
		echo "fwInfo='". trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion)."';\r\n;";
		echo "fwDate='". trim($system_conf->DeviceInfo->BuildVersion)."';\r\n;";
		?>
		function myFunction(){
			var x = document.getElementById("FileInput");
			var txt = "";
			if ('files' in x) {
				if (x.files.length == 0) {
					txt = "Select files.";
					document.getElementById("submit-btn").disabled = true;
				} else {
					for (var i = 0; i < x.files.length; i++) {
						var file = x.files[i];
            if(capInfo.board_chipset.indexOf('amba_s3l') != -1 || capInfo.board_chipset.indexOf('amba_s5l') != -1) {
              var maxFileSizeMB = 25;
              var maxFileSize = (maxFileSizeMB * 1024 * 1024);
              if(file.size > maxFileSize) {
                alert('The File Size must be less than '+ maxFileSizeMB +' MB.');
                return;
              }
            }
						if ('name' in file) {
							txt += "  " + file.name + " ";
						}
						if ('size' in file) {
							txt += " " + file.size + " bytes ";
						}
					}
					document.getElementById("submit-btn").disabled = false;
				}
			} 
			document.getElementById("demo").innerHTML = txt;
			if(txt.length  > 54) {
				$("#demo").css('width','230px');
				$("#demo").css('padding','0em .75em');
				$("#demo").css('position','relative');
				$("#demo").css('float','left');
			}
			else {
				$("#demo").css('padding','0em .75em');
				$("#demo").css('position','relative');
				$("#demo").css('float','left');
			}
		}
		function impFunction(){
			var x = document.getElementById("impFileInput");
			var txt = "";
			if ('files' in x) {
				if (x.files.length == 0) {
					txt = "  Select files.";
					document.getElementById("import-btn").disabled = true;
				} else {
					for (var i = 0; i < x.files.length; i++) {
						var file = x.files[i];
						if ('name' in file) {
							txt += "  " + file.name + " ";
						}
						if ('size' in file) {
							txt += " " + file.size + " bytes ";
						}
					}
					document.getElementById("import-btn").disabled = false;
				}
			} 
			document.getElementById("impdemo").innerHTML = txt;
			if(txt.length  > 54) {
				$("#impdemo").css('width','200px');
				$("#impdemo").css('padding','0em .75em');
				$("#impdemo").css('position','relative');
				$("#impdemo").css('float','left');
			}
			else {
				$("#impdemo").css('padding','0em .75em');
				$("#impdemo").css('position','relative');
				$("#impdemo").css('float','left');
			}
		}
	</script>
	<script src="./setup_system_plugin_upload.js"></script>
</body>
</html>
<!-- end_of_file -->
