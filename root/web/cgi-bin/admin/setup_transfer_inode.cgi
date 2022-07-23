<?
require('../_define.inc');
require('../class/network.class');
require('../class/event.class');
require('../class/record.class');
require('../class/trigger.class');

$event_conf = new CEventConfiguration();
$net_conf = new CNetworkConfiguration();
$triggers_conf= new CTriggersConfiguration();
$action_rules 	= $triggers_conf->action_rules;
$record_conf = new CRecordConfiguration();

//--- ip
function getiNodeInfo()
{	
	$data['enabled']     = $GLOBALS['net_conf']->FtpSetting->Enabled;
	$data['ftp_addr']    = trim($GLOBALS['net_conf']->FtpSetting->Server);
	$data['upload_path'] = trim($GLOBALS['net_conf']->FtpSetting->Directory);
	$data['port']        = trim($GLOBALS['net_conf']->FtpSetting->Port);
	$data['id']          = trim($GLOBALS['net_conf']->FtpSetting->Username);
	$data['pass']        = trim($GLOBALS['net_conf']->FtpSetting->Password);
	$data['type']        = trim($GLOBALS['net_conf']->iNodeSetting->Type);
	$data['image_num']        = trim($GLOBALS['event_conf']->transfer_conf->numofimg);
	$data['pre_duration']        = trim($GLOBALS['event_conf']->transfer_conf->preduration);
	$data['post_duration']        = trim($GLOBALS['event_conf']->transfer_conf->postduration);
	$data['duration']        = trim($GLOBALS['action_rules']->action[0]->duration);
	$data['autodelete']        = trim($GLOBALS['event_conf']->StorageDevices->Device[0]->AutoDelete);
	$data['target_stream']        = trim($GLOBALS['record_conf']->target_stream->value);
    $data['rec_pre_duration']        = trim($GLOBALS['record_conf']->job_conf[0]->pre_duration);
	$data['rec_post_duration']        = trim($GLOBALS['record_conf']->job_conf[0]->post_duration);
	echo json_encode($data);
}



?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>ftp settings</title>
	</head>

	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_inode_config"></span></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="enabled" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off"></span>
			<input type="radio" value="1" name="enabled" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on"></span><br>
		</div>
		<div  id="Ftpcontent" class="content">
			<label class="maintitle"><span tkey="setup_server_info"></span></label>
										<!-- 
										<label class="subtitle"><span tkey="setup_ftp_mode"></span></label>
										<input type="radio" value="1" name="pasv_mode" id="pasv_mode_on" >
										<label for="pasv_mode_on"></label><span tkey="setup_passive_mode"></span>
										<input type="radio" value="0" name="pasv_mode" id="pasv_mode_off" >
										<label for="pasv_mode_off"></label><span tkey="setup_active_mode"></span><br>
										-->
			<label class="subtitle"><span tkey="setup_inode_serveraddress"></span></label>
			<input id="ftp_addr" type="text" class="inputText"><br>	
			
			<label class="subtitle"><span tkey="setup_inode_path"></span></label>
			<input id="upload_path" type="text" class="inputText"><br>
				
			<label class="subtitle"><span tkey="setup_inode_port"></span></label>
			<input id="port" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_id"></span></label>
			<input id="id" type="text" class="inputText"><br>
			
			<label class="subtitle"><span tkey="setup_user_passwd"></span></label>
			<input id="pass" type="password" class="inputText"><br>
		</div>	 
		<div id="operation_layer" class="content">
			<label class="subtitle" tkey="setup_operation_duration"></label>
			<input class="short" type="number" id="duration"><label tkey="setup_transfer_sec"></label>
			[ 0 ~ 60 ]
			<br>

			<label class="subtitle"><span tkey="setup_pre_alarm_duration"></span></label>
			<input type="number" id="pre_duration" class="short" max="30" ><span tkey='setup_transfer_sec'></span> [ 1 ~ 5 ]<br>
								
			<label class="subtitle"><span tkey="setup_post_alarm_duration"></span></label>
			<input type="number" id="post_duration" class="short" max="30"><span tkey="setup_transfer_sec"></span> [ 1 ~ 30 ]<br>	

		</div>
		<div id="type_select" class="content">
			<label class="maintitle"><span tkey="setup_inode_transfer_type"></span></label>
			<input type="radio" value="0" name="type" id="images" >
			<label for="images"></label><span tkey="Images"></span>
			<input type="radio" value="1" name="type" id="video" >
			<label for="video"></label><span tkey="Video"></span><br>
		</div>		
		<div id="Imagescontent" class="content">
			<label class="maintitle"><span tkey="setup_prepost_alarm_image"></span></label>				

			<label class="subtitle"><span tkey="setup_transition_imagenumber"></span></label>
			<input type="number" id="image_num" class="short" max="5"><span tkey="setup_image_per_seconds""></span> [ 1 ~ 5 ]<br>							
		</div>
		<div id="Videocontent" class="content">
			<label class="maintitle"><span tkey="setup_record_setting"></span></label>

			<label class="subtitle"><span tkey="setup_record_stream"></span></label>
			<div class="select">
				<select id="target_stream">
					<option value='-1' tkey="setup_none"></option>
					<option value='0' tkey="setup_main_stream"></option>
					<option value='1' tkey="setup_sub_stream"></option>
				</select>
			</div><br>

			<label class="subtitle"><span tkey="setup_auto_delete"></span></label>
			<div class="select">
				<select id="autodelete">
					<option value="0" tkey="setup_none"></option>
					<option value="1" tkey="setup_1day"></option>
					<option Value="2" tkey="setup_7days"></option>
					<option Value="3" tkey="setup_15days"></option>
					<option Value="4" tkey="setup_1month"></option>
				</select>
			</div><br>
		</div>

		<center>
			<button id="btOK" class="button" ><span tkey="apply"></span></button>
		</center>
		<script type="text/javascript">
			var iNodeInfo = <? getiNodeInfo(); ?>
		</script>
		<script src="./setup_transfer_inode.js"></script>
	</body>
</html>
