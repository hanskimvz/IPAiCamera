<?
require('_define.inc');
require('class/system.class');
require('class/capability.class');
require('class/network.class');
require('class/socket.class');
require('class/ptz.class');
require('class/media.class');
require('class/iot.class');


$focus_mode = new CFocusModeRequest();	
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);

//print_r($shm_id);
$system_conf = new CSystemConfiguration($shm_id);


//print "<pre>"; print_r($GLOBALS); print "</pre>";


$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$profile_conf = new CProfileConfiguration($shm_id);
//$media_conf   = new CMediaConfiguration($shm_id);
//$mic_conf = $GLOBALS['media_conf']->ProfileConfig;
$iot_conf = new CWIFI($shm_id);


shmop_close($shm_id);
$get_oem = $system_caps->getOEM();


function getAudioVolume($name)
{
	echo $name.'.input_volume='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Volume.';';
}
function getAudioSpeakVolume($name)
{
	echo $name.'.output_volume='.$GLOBALS['profile_conf']->AudioOutputConfiguration->OutputLevel.';';
}
function getRTSPPort($name)
{
	echo $name . "=" .$GLOBALS['net_conf']->Protocols->Protocol[1]->Port.";\r\n";
	if(isset($_SERVER['HTTPS']))
	{
	  echo"webPort=" .$GLOBALS['net_conf']->Protocols->Protocol[2]->Port.";\r\n";
	  echo"http_mode=1;\r\n";
	}
	else
	{
	  echo"webPort=" .$GLOBALS['net_conf']->Protocols->Protocol[0]->Port.";\r\n";
	  echo"http_mode=0\r\n";
	}
}

function getLangSetup($name)
{
	echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
check_connection_policy_with_authority($system_conf);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<meta content="text/html; charset=utf-6" http-equiv="Content-Type">
		<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
		<meta name="google" content="notranslate">
		<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<title>IP Camera</title>
		<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
		<link rel="stylesheet" href="/css/main.css" type="text/css" />
		<link rel="stylesheet" href="/css/dom.css" type="text/css" /> 
	    <? DependencyOem(); ?>

<!--[if IE]><!-->
		<link rel="stylesheet" type="text/css" href="/css/main_ie.css" />
<!--<![endif]-->

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div id="frame">
			<div id="div_left">
				<label id="logo"></label>
<? if ( $get_oem == 10) { ?>
                <p id="cbca_model_name"> </p>

<?}?>                    
				<div class="menu">				
					<button id="setup" class="button long" tkey="main_setup" ></button>
					<button id="logout_btn" class="button long" tkey="main_logout" style="display:none; margin-top:0px;"></button>
					<div class="vlc_menu">
					  <div id="buffer_setup"> 
						<p class='title'><span tkey="main_live_buffer"></span></p>
						<div class="select long">
							<select id="bufferingProfile" onChange="VLCManager.changeBuffer(this.value);" class="long graybg"  autocomplete='off'></select>
						</div>
						</div>
						<p class='title'><span tkey="main_stream"></span></p>
						<div class="select long">
							<select id="lstProfile" class="long graybg" autocomplete='off'></select>
						</div>
						<button id="fullScreen" class="button long" tkey="main_full_screen"></button>
					</div>											
					<div class="jpeg_menu" style="display : none">
						<p class='title' tkey="main_live_viewer">Live Viewer</p>
						<div class="select long lang">
							<select id="Streming_Type" class="long graybg lang" autocomplete=off>
								<option value="1" tkey="main_vlc">VLC Plugin</option>
								<option value="2" tkey="main_html5_mjpeg">HTML5[MJPEG] </option>
						<!--	<option value="3" tkey="WebSocket(MJPEG)">WEBSOCKET[MJPEG] </option>  -->
							</select>
						</div> 
					</div>
					<div id="ptz">
						<table id="have_pantilt" class="ptz_arrow">
							<tr>
								<td><button class="ptz_up_left" value="upleft"></button></td>
								<td><button class="ptz_up" value="up"></button></td>
								<td><button class="ptz_up_right" value="upright"></button></td>
							</tr>
							<tr>
								<td><button class="ptz_left" value="left"></button></td>
								<td class="joystick"><figure class="circle"></figure></td> 
								<td><button class="ptz_right" value="right"></button></td>
							</tr>
							<tr>
								<td><button class="ptz_down_left" value="downleft"></button></td>
								<td><button class="ptz_down" value="down"></button></td>
								<td><button class="ptz_down_right" value="downright"></button></td>
							</tr>
						</table>
						<div id="iv_surround">
							<div id="have_zoom" class="ptz_small">
								<button id="m_zoom" class="button extrasmall" value="out">-</button>
								<button id="p_zoom" class="button extrasmall" value="in">+</button>
								<label class="title subtitle"><span tkey="main_zoom"></span></label>
							</div>
							<div id="have_iris" class="ptz_small">
								<button id="m_iris" class="button extrasmall" value="close">-</button>
								<button id="p_iris" class="button extrasmall" value="open">+</button>
								<label class="title subtitle"><span tkey="main_iris"></span></label>
							</div>
							<div id="have_focus" class="ptz_small">
								<button id="m_focus" class="button extrasmall" value="far">-</button>
								<button id="p_focus" class="button extrasmall" value="near">+</button>
								<label class="title subtitle"><span tkey="main_focus"></span></label>
							</div>
							<div id="have_pantilt_speed">
								<div class="slider_box" style="margin-top:5px;">
								<label class="title subtitle"><span tkey=""></span></label>
								<div id="pt_speed_bar"></div>        
								<label id="pan_tilt_value">1</label></div>
								<div><label class="title subtitle" style="margin-top:0px;"><span tkey="Pan/tilt_Speed"></span></label></div>		
							</div>											
							<div id="div_zoom_speed">
								<div id="have_zoom_speed" class="slider_box" style="margin-top:-20px;">
								<label class="title subtitle"><span tkey=""></span></label>
								<div id="pt_zoom_bar"></div>        
								<label id="zoom_value">1</label></div>
								<div><label class="title subtitle" style="margin-top:0px;"><span tkey="Zoom_Speed"></span></label></div>	
							</div>
							<div id="focusmode" class="field switch button long_180">
							<label class="cb-enable"><span id="auto" tkey="setup_auto">Auto</span></label>
							<label class="cb-disable" ><span id="manual" tkey="main_manual">Manual</span></label>
							<input type="checkbox" id="checkbox" class="checkbox" name="field2" autocomplete='off' hidden></input> 
							</div>						
							<label id="focusmodetitle" class="title subtitle" tkey="main_focus_mode">Focus Mode</label>		
							<label id="focus_status" class="subtitle focus long" ></label>	
						</div>
						<div id="have_wiper" class="ptz_small">  <!-- overview mode -->
						<button id="wiper_btn" class="button extrasmall" >W</button>
						<label class="title subtitle"><span tkey="wiper"></span></label>
						</div>
						<div id="have_washer" class="ptz_small">  <!-- overview mode -->
							<button id="washer_btn" class="button extrasmall" >S</button>
							<label class="title subtitle"><span tkey="Washer"></span></label>
						</div>
						<div id="have_wled" class="ptz_small">  <!-- overview mode -->
							<button id="wled_btn" class="button extrasmall" >L</button>
							<label class="title subtitle"><span tkey="WLED"></span></label>
						</div>
					</div>
				</div>
			</div>
			<div id="div_main">
				<label id="iv_logo" style="display:none;"></label>
<!--				<canvas id="jpeg" width="960" height="540" style="display:none; margin:auto;"></canvas>  -->
<!--				<div id="vlc_play"> </div> -->
				<div id="vlc_play"><canvas id="jpeg" width="960" height="540" style="display:none; margin:auto;"></canvas> </div> 
			</div>
			<div id="sub_menu">
				<div id="preset" class="content main_content">         <!--   preset   -->
					<div class="slice" id="home_position">
					<table>
					<tbody>
					<tr><td class ="homeposition12">
						<label id="homeposition" class="c_title" tkey="set_home_position"></label></td><td>
				            <button id="set_home_position" class="button extrasmall2">SET</button>
							<button id="run_home_position" class="button extrasmall2">RUN</button> </td></tr></tbody></table>
					</div>
					<hr>
					<div class="slice" id="presetgroup_1_div">
						<div class="select preset">
							<select id="presetgroup_1" class="graybg preset" autocomplete='off'></select>
						</div>
						<button id="preset_remove" class="button extrasmall " value="0">-</button>
						<button id="preset_set" class="button extrasmall" value="1">+</button>
						<button id="preset_run" class="button extrasmall" value="2">R</button>
					</div>
					<hr>
					<div class="slice" id="presetgroup_2_div">
						<div class="select preset">
							<select id="presetgroup_2" class="graybg preset" autocomplete='off'></select>
						</div>
						<button id="presetour_remove" class="button extrasmall " value="1">-</button>
						<button id="presetour_set" class="button extrasmall" value="2">+</button>
						<button id="presetour_run" class="button extrasmall" value="3">R</button>
					</div>					
				</div>
<!--
				<div id="pir_box" class="content">
					<div class="none_slice">
						<span class="menuTitle">PIR
							<button id="pir" class="button round">Off</button>
						</span><br>
						<input type="checkbox" id="led_auto" onclick="onClickCheckOut();" autocomplete='off'>
						<label for="led_auto"></label>
						<span class="c_title">Auto Off</span>
						<button id="led" onclick="onClickLED(0);" class="button">LED Off</button>
					</div>
				</div>
-->
				<div id="sound_box" class="content main_content russian_content"> <!--   sound_box   -->
					<div class="slice slice2">
						<input type="checkbox" id="cb_speaker" autocomplete='off' ><label for="cb_speaker"></label>
						<span class="c_title" tkey="main_speaker">SPEAKER</span>
						<div class="slider_box ie_slice">
							<div id="volume_bar"></div>        
							<label id="volume_value">50</label>
						</div>        
					</div>
					<hr>
					<div id="cb_mute"class="slice vertical">
						<input type="checkbox" id="cb_mic" autocomplete='off'><label for="cb_mic"></label><span class="c_title" tkey="main_mute" >MUTE</span>
					</div>
				</div>
				<div id="sound_box_audioout" class="content main_content"> <!--   sound_box   -->
					<div class="slice slice2">
						<input type="checkbox" id="cb_speaker" autocomplete='off' >
						<span class="c_title" tkey="main_speaker">SPEAKER</span>
						<div class="slider_box ie_slice">
							<div id="volume_bar_audioout"></div>
							<label id="volume_value_audioout">5</label>
						</div><br>
						<span class="c_title">Audio</span>
						<span class="right">
							<button id="btntestaudio1" class="button round">1</button>
							<button id="btntestaudio2" class="button round">2</button>
						</span><br>
					</div>
					<hr>
					<div id="cb_mute"class="slice vertical">
						<input type="checkbox" id="cb_mic" autocomplete='off'><label for="cb_mic"></label><span class="c_title" tkey="main_mute" >MUTE</span>
					</div>
				</div>
				<div id="c_alarm" class="content main_content russian_content"> 
					<div id="alarmInput_box" class="slice">
						<table>
<? if ( $get_oem == 10) { ?>
						<td class="alarmin12"><label class="c_title" tkey="main_alarm_input_cbca" >ALARM INPUT</label></td>
<? } else { ?>                               
						<td class="alarmin12"><label class="c_title" tkey="main_alarm_input" >ALARM INPUT</label></td>
<?}?>
						<td><span style="left:30px; top:-2px;">
							<button id="alarminput1" class="button round">0</button>
							<button id="alarminput2" class="button round">0</button>
							</span>
						</td>
						</table>
					</div>
					<hr>
					<div id="relayOut_box" class="slice margintop15_sb">	
						<table>			
<? if ( $get_oem == 10) { ?>
							<td class="alarmin12"><label class="c_title" tkey="main_relay_out_cbca">RELAY OUT</label></td>
<? } else { ?>                               
							<td class="alarmin12"><label class="c_title" tkey="main_relay_out">RELAY OUT</label></td>
<?}?>

							<td>
								<input type="checkbox" id="cb_relay_out1" autocomplete='off'>
								<label for="cb_relay_out1"></label>

                                <input type="checkbox" id="cb_relay_out2" autocomplete='off'>
								<label for="cb_relay_out2"></label>		
							</td>
						</table>
<!--					<input type="checkbox" id="cb_relay_out3" autocomplete='off'>
						<label for="cb_relay_out3"></label>		
-->								
					</div>
				</div>
				<div id="time_box" class="content main_content russian_content"> <!--   alarm in/out   -->
					<div id="motion_alarm" class="slice">
						<label class="c_title" tkey="main_motion">MOTION</label>
						<span id="displayMotionStatusArea" class='right'>
						</span>
					</div>
					<hr>
					<div class="slice time_view">
						<label tkey="main_camtime">CameraTime</label><br>
						<label id="timeInfo"></label>
					</div>
				</div>
				 <div id="pir_box" class="content">
                                        <div class="none_slice">
						<span class="c_title">PIR</span>
                                                <span class="right"> 
                                                        <button id="btnpir_e" class="button round">E</button>
                                                        <button id="btnpir_s" class="button round">0</button>
                                                </span><br>
                                                <input type="checkbox" id="pir_autoclear" autocomplete='off'>
                                                <label for="pir_autoclear"></label>
                                                <span class="c_title">Auto Clear</span>
                                                <button id="pir_setclear" class="button button_margin_left half">Pir Clear</button>
                                        </div>
                                </div>

				</div>
			</div>
			<div id="audios-container"  ></div>	 <!-- style="display:none" -->
		</div>
<? if ( $get_oem == 12) { ?>		
		<center><label class="caution" id="http_status"></label></center>
<?}?>		
		<script>
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var IOTInfo = <? $GLOBALS['iot_conf']->getIOTInfoConf() ?>;
			var userInfo = new Object();
			var VideoInfo = <?  getChannelInfo($GLOBALS['profile_conf']); ?>;
			var VideoInputInfo = <? $GLOBALS['profile_conf']->VideoSourceConfigurations->getVideoSourceInfo(); ?>;
            var devInfo = <? $GLOBALS['system_conf']->getDevInfo();?>;
			var wiperInfo = <? get_WiperAction($GLOBALS['profile_conf']); ?>;  <!-- for overview mode wiperaction --!>
			var rtspPort;
			var webPort;
			var http_mode;
			var gLanguage;
			var systemOption;
			var strtime; 
			var prsetInfo = new Object();
			var presetTourInfo = new Object();
            var audioEnc = new Object();
			var audioSpeakEnc = new Object();
			var timeFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->TimeFormat?>;
			var corridor_mode = <?echo $GLOBALS['system_conf']->Corridor->enabled?>;
			var hourFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->HourFormat?>;
			<?
			if($GLOBALS['get_oem'] == 19 || $GLOBALS['get_oem'] == 20 || $GLOBALS['get_oem'] == 21)
			{
				$GLOBALS['system_conf']->Users->getAccessUserInfo_x("userInfo");
			}
			else
			{	
				$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
			}
			getRTSPPort("rtspPort");
			getLangSetup("gLanguage");
            getAudioVolume("audioEnc");
			getAudioSpeakVolume("audioSpeakEnc");
			echo "systemOption=" . $GLOBALS['system_conf']->SystemOption . ";\r\n";
				//SYSTEM OPTION
			echo "var SYSTEM_OPTION_UI_FIXED_DATE_20160504=" . SYSTEM_OPTION_UI_FIXED_DATE_20160504 . ";\r\n";
			$ipc_sock = new IPCSocket();					
			$ipc_sock->Connection($focus_mode, CMD_GET_FOCUS_MODE);	
			printf("var focus_mode = %d ;\r\n",  $focus_mode->mode->mode);
			printf("var encodeVersion=%d;\r\n", $GLOBALS['system_conf']->Security->SystemService->EncodeVersion);
				$ipc_sock = new IPCSocket();
				$focus_mode = new  CFocusMode();
				$ipc_sock->Connection($focus_mode, CMD_GET_FOCUS_MODE);	
		?>
		</script>
<!--		<script defer src="/js/less.min.js" ></script> -->
		<script defer src="/js/jquery1.11.1.min.js"></script>
		<script defer src="/js/jqueryui.js"></script>
		<script defer src="/js/jquery.cookie.js"></script>		
		<script defer src="/js/menu_config.js"></script>
		<script defer src="/js/page.js"></script>
<!--		<script defer src="/js/MediaStreamRecorder.js"></script> -->
<!--		<script defer src="/js/websocket.js"></script> -->
		<script defer src="/js/jpeg.js"></script>
		<script defer src="/js/wsstream.min.js"></script>		
		<script defer src="/js/vlc_v3.js"></script>
		<script src="/js/lang.js"></script>
		<script defer src="./index.js"></script>
	</body>
</html>
