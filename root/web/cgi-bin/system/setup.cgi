<? 
require('../_define.inc');
require('../class/system.class');
require('../class/socket.class');
require('../class/capability.class');
require('../class/media.class');
require('../class/ptz.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$media_conf  = new CMediaConfiguration($shm_id);
//$profile_conf = new CProfileConfiguration($shm_id);
$profile_conf = $media_conf->ProfileConfig;
shmop_close($shm_id);
// print "<pre>"; print_r($system_conf); print "</pre>";
$get_oem = $system_caps->getOEM();
$osds_conf    = $GLOBALS['system_conf']->Osds;
function check_fisheye_model(){
	return (trim($GLOBALS['system_caps']->camera_type) =="fisheye" );
}
function change_fisheye_input_buffer_offset_x() {
	if( !isset($_REQUEST["offset_x"]) ) return 1;
	$GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->x = $_REQUEST["offset_x"];
	return 0;
}

function change_fisheye_input_buffer_offset_y() {
	if( !isset($_REQUEST["offset_y"]) ) return 1;
	$GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->y = $_REQUEST["offset_y"];
	return 0;

}
function change_fisheye_input_buffer_offset() {
	if( change_fisheye_input_buffer_offset_x() < 0 ) return -1;
	if( change_fisheye_input_buffer_offset_y() < 0 ) return -1;

	return 0;
}

function fisheye_input_buffer_offset_view_post($isjson=false){
	if(!$isjson){	
		echo "offset_x=" . $GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->x . "<br>";
		echo "offset_y=" . $GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->y .  "<br>";
	}else{	
		$data = array();
	
		$used = 0;
			
		$data['cali_center']['pos_x']    = $GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->x ;
		$data['cali_center']['pos_y']    = $GLOBALS["system_conf"]->DeviceInfo->FisheyeInputOffset->y ;
		
		echo json_encode($data);
	}	
	return 0;
}
function gpio_value($name){

    if(!file_exists("/tmp/test_result")){
        echo $name."['button']='0';\r\n";  
        echo $name."['wl']='0';\r\n";  
        echo $name."['d1']='0';\r\n";  
        echo $name."['d2']='0';\r\n";  
        echo $name."['audioout']='0';\r\n";  
        return 0;
    }
    $file_arr = file('/tmp/test_result');
    foreach($file_arr as $v){
        $v = str_replace(array("\r\n","\r","\n"),'',$v);
        $i = explode("=",$v);

        echo $name."['".$i[0]."']='".$i[1]."';\r\n";  
    }
}

if( isset( $_REQUEST['msubmenu']) )
{
	header("Content-Type: text/plain");
	ob_end_clean();
	if ( $_REQUEST['msubmenu'] == 'log' )
	{
		if ( $_REQUEST['action'] == 'clear' )
		{
      	 	$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_SYSTEM_LOGCLEAR);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
			}	
		}
		else
			show_post_ng();
		exit;
	}
	else if( $_REQUEST['msubmenu'] == 'fisheye' && check_fisheye_model() ) {
		if ($_REQUEST['action'] == 'apply'){ 

			if( change_fisheye_input_buffer_offset() == 0 ) {

				$data = $GLOBALS['system_conf']->DeviceInfo->FisheyeInputOffset;

				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($data, CMD_SET_FISHEYE_BUFFER_OFFSET);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
					fisheye_input_buffer_offset_view_post(1);
//					show_post_ok();
				}
				else {
					show_post_ng();
				}
			}
		}
		else if ($_REQUEST['action'] == 'view') {
			fisheye_input_buffer_offset_view_post();
		}
		exit;
	}
	else if ($_REQUEST['msubmenu'] == 'cdsAdj')
	{
		if ($_REQUEST['action'] == 'apply')
		{ 
			if ( isset($_REQUEST['cdsAdj']) && $_REQUEST['cdsAdj'] != null) {
					$GLOBALS['system_conf']->DeviceInfo->CDS_ADJ = $_REQUEST['cdsAdj'];
			}

			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_CDS_ADJ);
  			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
  			{
  				show_post_ok();
  			}
  			else
  			{
  				show_post_ng();
  			}					

			exit;		
		}
	}
	else if ($_REQUEST['msubmenu'] == 'system')
	{
		if ($_REQUEST['action'] == 'apply')
		{ 
			$flag = 0;
			$serialflag = 0; //no reboot save device info flag
			$delete = 0;
			if ( isset($_REQUEST['color_system']) && $_REQUEST['color_system'] != null) {
				if (($_REQUEST['color_system'] >= COLORSYS_NTSC && $_REQUEST['color_system'] <= COLORSYS_PAL)  &&
					($GLOBALS['system_conf']->DeviceInfo->VideoType != $_REQUEST['color_system']) )
				{
					$GLOBALS['system_conf']->DeviceInfo->VideoType = $_REQUEST['color_system'];
					$flag = 1;
				}
			}
			if ( isset($_REQUEST['tdn']) && $_REQUEST['tdn'] != null) {
				if (($_REQUEST['tdn'] >= 0 && $_REQUEST['tdn'] <= 1)  &&
					($GLOBALS['system_conf']->DeviceInfo->TDN != $_REQUEST['tdn']) )
				{
					$GLOBALS['system_conf']->DeviceInfo->TDN = $_REQUEST['tdn'];
					$flag = 1;
				}
			}

			if ( isset($_REQUEST['model_num']) && $_REQUEST['model_num'] != null) 
			{
				if($GLOBALS['system_conf']->DeviceInfo->ProductName != $_REQUEST['model_num'])
				{
					$GLOBALS['system_conf']->DeviceInfo->ProductName= $_REQUEST['model_num'];
					$flag = 1;
				}
			}
			if ( isset($_REQUEST['model_name']) && $_REQUEST['model_name'] != null) 
			{
				if ( ($GLOBALS['system_conf']->DeviceInfo->Model != $_REQUEST['model_name']) &&
					(strlen($_REQUEST['model_name']) <= 30 ) )
				{
					$GLOBALS['system_conf']->DeviceInfo->Model = $_REQUEST['model_name'];
					$flag = 1;
				}
			}

			if ( isset($_REQUEST['model_manufacturer']) && $_REQUEST['model_manufacturer'] != null) 
			{
				if ( ($GLOBALS['system_conf']->DeviceInfo->Manufacturer != $_REQUEST['model_manufacturer']) &&  
					(strlen($_REQUEST['model_manufacturer']) <= 60) )
				{
					$GLOBALS['system_conf']->DeviceInfo->Manufacturer = $_REQUEST['model_manufacturer'];
					$flag = 1;
				}
			}
			if ( isset($_REQUEST['thermal_offset']) && $_REQUEST['thermal_offset'] != null) 
			{
				if ( ($GLOBALS['system_conf']->DeviceInfo->Thermal_offset != $_REQUEST['thermal_offset']) &&  
					(strlen($_REQUEST['thermal_offset']) <= 32) )
				{
					$GLOBALS['system_conf']->DeviceInfo->Thermal_offset = $_REQUEST['thermal_offset'];
					$flag = 1;
				}
			}
			if ( isset($_REQUEST['serialnumber']) && $_REQUEST['serialnumber'] != null) 
			{
                if ( (($GLOBALS['system_conf']->DeviceInfo->SerialNumber === "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")||($GLOBALS['system_conf']->DeviceInfo->SerialNumber === "")) &&  
					(strlen($_REQUEST['serialnumber']) < 32) && preg_match('`^[A-Za-z0-9]*\.?[A-Za-z0-9]*$`', $_REQUEST['serialnumber']) )                
				//if ( ($GLOBALS['system_conf']->DeviceInfo->SerialNumber != $_REQUEST['serialnumber']) &&  
				//	(strlen($_REQUEST['serialnumber']) < 32) )
				{
					$GLOBALS['system_conf']->DeviceInfo->SerialNumber = $_REQUEST['serialnumber'];
					$serialflag = 1;
				}
                else {
					show_post_ng();
				}
			}
			if (isset($_REQUEST['delete_log']) && $_REQUEST['delete_log'] != null) 
			{
				if ($_REQUEST['delete_log'] == 1) 
				{
					$delete = 1;
				}
			}

			$ipc_sock = new IPCSocket();
			if ($delete) 
			{
                $ipc_sock->Connection(NULL, CMD_SYSTEM_LOGCLEAR);
                if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
  			    {
  				    show_post_ok();
  			    }
  			    else
  			    {
  				    show_post_ng();
  			    }			
  			    exit;			  
			}
            if($serialflag)
            {
                $ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_SETUP_INI_NO_REBOOT);
                if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
                {
                    show_post_ok();
                }
                else
                {
                    show_post_ng();
                }
            }
            else if($flag)
            {
                $ipc_sock->Connection($GLOBALS['system_conf']->DeviceInfo, CMD_SET_SETUP_INI);
                if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
                {
                    show_post_ok();
                }
                else
                {
                    show_post_ng();
                }					
            }
		} else if ($_REQUEST['action'] == 'view') {
			if($GLOBALS['system_conf']->DeviceInfo->VideoType == COLORSYS_NTSC)
				$data = "NTSC";
			else
				$data = "PAL";
			printf("color_system=%s\r\n", $data);
			printf("tdn=%d\r\n", $GLOBALS['system_conf']->DeviceInfo->TDN);
			printf("cdsAdj=%d\r\n", $GLOBALS['system_conf']->DeviceInfo->CDS_ADJ);
			printf("model_num=%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->ProductName));
			printf("model_name=%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->Model));
			printf("model_manufacturer=%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->Manufacturer));
			printf("thermal_offset=%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->Thermal_offset));
			printf("serialnumber=%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->SerialNumber));
			printf("fwInfo=%s_%s\r\n", trim($GLOBALS['system_conf']->DeviceInfo->BuildVersion), trim($system_conf->DeviceInfo->FirmwareVersion) );
			printf("camInfo=%s\r\n", trim($system_conf->DeviceInfo->ModuleVersion) );
		} else if ($_REQUEST['action'] == 'test') {
			if ( isset($_REQUEST['audio_loopback']) && $_REQUEST['audio_loopback'] != null) {
				if ($_REQUEST['audio_loopback'] >= 0 && $_REQUEST['audio_loopback'] <= 1)
				{
						$req = new CFocusMode();
						$req->mode = $_REQUEST['audio_loopback'];				
						$ipc_sock = new IPCSocket();
					  	$ipc_sock->Connection($req, CMD_TEST_AUDIO_LOOPBACK);
			  			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			  			{
			  				show_post_ok();
		}
			  			else
			  			{
			  				show_post_ng();
			  			}
				}
			}		
		}
		
		if ($_REQUEST['action'] == 'logclear')
		{ 
			
			
		}
		exit;
	}
	else if ($_REQUEST['msubmenu'] == 'hwtest')
	{
		if ($_REQUEST['action'] == 'auto')
		{
			system("/root/hw_test auto");	
		}
        else if ($_REQUEST['action'] == 'button')
        {
			system("/root/hw_test button");	

        }
        else if ($_REQUEST['action'] == 'wl')
        {
			system("/root/hw_test wl ");	

        }
        else if ($_REQUEST['action'] == 'd1')
        {
			system("/root/hw_test d1");	

        }
        else if ($_REQUEST['action'] == 'd2')
        {
			system("/root/hw_test d2");	

        }
        else if ($_REQUEST['action'] == 'audioout')
        {
			system("/root/hw_test audioout");	

        }
        else if ($_REQUEST['action'] == 'focuscast')
		{
			$remote = new CFocusCast();
			if ( isset($_REQUEST['portNo']) && $_REQUEST['portNo'] != null) {
					$remote->Port = $_REQUEST['portNo'];
			}
			else
				$remote->Port = 9988;
			$remote->Addr = $_SERVER['REMOTE_ADDR'];
      	 	$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($remote, CMD_TEST_FOCUSCAST);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				for($i=0 ; $i<$GLOBALS['system_caps']->video_in ; ++$i)
				{
					echo $GLOBALS['osds_conf']->Osd[$i]->focus_enabled; 
				}
			}
			else
			{
				show_post_ng();
			}
		}		
        else
            show_post_ng();

		exit;
	}
	else
	{
		show_post_ng();   
	}
}
function getLangSetup($name) {
    echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	<title>SYSTEM MANAGEMENT</title>
	<link rel="stylesheet" href="/css/dom.css" type="text/css" />
    <? 
	if( $get_oem == 5) 
    	echo '<link rel="stylesheet" href="/css/esca.css" type="text/css" />';	
    else  if( $get_oem == 10 ) 
    	echo '<link rel="stylesheet" href="/css/cbca.css" type="text/css" />';	
	else {
		echo '<link rel="stylesheet" href="/css/admin.css" type="text/css"/>';
	}
	?>
    
	<style>
		table { background-color: #c5c5c5; margin: 5px 5px; padding: 5px 5px; width:550px;}
		body{ padding: 10px;}
		input{ display: inline-block; vertical-align: middle;}
		.title{ font-weight:bold; font-size:11pt;}
		.caution { color:#AA0000; font-size: 9pt; font-weight:bold; border-bottom: none; text-align: right;}
		.fisheye_div{ float: left; }
		.option1{
			width: 550px;
			height: 535px;
			position: absolute;
			margin: 5px;
		}
		.fisheye_button{
			padding-left: 160px;		}
		#fisheye_jpeg{
			display: block; 
			background:black;
			 margin-top: 5px;			
		}	
		th { width: 180px; line-height:20px; text-align: left;}
	</style>    
</head>
<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div style="float:left;">
		<table>
			<tr>
				<td class="title">LOG MANAGEMENT</td>
				<td><button name="cmdApplyAll" class="button button_custom" onclick="onLogClear();" >LOG CLEAR</button></td>
			</tr>
		</table>
		<table>
			<tr>
				<td class="title">SYSTEM MANAGEMENT</td>
				<td class="caution">CAUTION!</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkColorSys" value="1" onclick="onClickSelection(this);" id="color"><label for="color"></label><span>COLOR SYSTEM</span>
				</th>
				<td>
					<input id="ntsc" type="radio" name="optColorSys" value="0"><label for='ntsc'></label><span>NTSC</span>
					<input id="pal" type="radio" name="optColorSys" value="1"><label for="pal"></label><span>PAL</span>
				</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkTdn" value="1" onclick="onClickSelection(this);" id="tdn"><label for="tdn"></label><span>TDN</span>
				</th>
				<td>
					<input id="tdn_en" type="radio" name="optTdn" value="1"><label for='tdn_en'></label><span>Enabled</span>
					<input id="tdn_dis" type="radio" name="optTdn" value="0"><label for="tdn_dis"></label><span>Disabled</span>
				</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkModel" value="1" onclick="onClickSelection(this);" id="model"><label for="model"></label><span>MODEL</span>
				</th>
				<td>
					<div class="select" style="width:200px;">
						<select id="model" name="selModelNum" style="width:200px; display:block;">
	
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkModelName" value="1" onclick="onClickSelection(this);" id="name"><label for="name"></label><span>NAME</span>
				</th>
				<td>
					<input type="text" maxlength="30" class="inputText" style="width:200px; height:20px; ime-mode:disabled;" name="txtModelName" value="">
				</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkModelManufacturer" value="1" onclick="onClickSelection(this);" id="manufacturer"><label for="manufacturer"></label><span>MANUFACTURER</span>
				</th>
				<td>
					<input type="text" maxlength="60" class="inputText" style="width:200px; height:20px; ime-mode:disabled;" name="txtModelManufacturer" value="" >
				</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkThermaloffset" value="1" onclick="onClickSelection(this);" id="thermal_offset"><label for="thermal_offset"></label><span>THERMAL OFFSET</span>
				</th>
				<td>
					<input type="text" maxlength="60" class="inputText" style="width:200px; height:20px; ime-mode:disabled;" name="txtThermaloffset" value="" >
				</td>
			</tr>
			<tr>
				<td colspan="2" align="center">
					<button name="cmdApplyAll" class="button" style="margin-top:20px;" onclick="onClickApplyAll();" >Apply</button>
				</td>
			</tr>
		</table>
		<table class="Device_management">
			<tr>
				<td class="title">DEVICE MANAGEMENT</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkdevname" value="1" onclick="onClickSelection(this);" id="devicename"><label for="devicename"></label><span>DEVICE NAME</span>
				</th>
				<td>
					<input type="text" maxlength="30" class="inputText" style="width:200px; height:20px; ime-mode:disabled;" name="txtdevicename" value="" >
				</td>
				<td>
					<button name="cmdApply" class="button button_custom" onclick="onClickdevicename();" >apply</button>
				</td>
			</tr>
		</table>
		<table class="CDS_offset">
			<tr>
				<td class="title">CDS OFFSET</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkCDSAdj" value="1" onclick="onClickSelection(this);" id="cdsAdj"><label for="cdsAdj"></label><span>Target CDS</span>
				</th>
				<td>
					<input type="text" maxlength="10" class="inputText" style="width:200px; height:20px; ime-mode:disabled;" name="txtCDSAdj" value="" numberonly="true">
				</td>
				<td><button name="cmdApply" class="button button_custom" onclick="onSetCDSoffset();" >AutoSet</button></td>
			</tr>	
			<tr>
				<td></td>
				<td>
					<span> CDS = </span><span id="displayCDSStatus" ></span>
					<span id="CDSCor"></span>
				</td>
			<tr>		
		</table>
		<table class="FOCUS_osd">
			<tr>
				<td colspan=3 class="title">Hardware Test</td>
			</tr>
			<tr id="auto_id" style="text-align: center;" >
				<th>
					</label><span>Auto</span>
				</th>
				<td><button name="autoApply" class="button button_custom" id="test_auto" >Auto</button></td>
			</tr>	
			<tr colsapn="4" style="text-align: center;">
				<td id="bt_id" style="width:20%;">
					<button class="button button_custom" id="test_button">button</button>
                    <br>
					<span id="button_text"> </span>
				</td>
				<td id="wl_id" style="width:20%;">
					<button class="button button_custom" id="test_wl">white LED</button>
                    <br>
					<span id="wl_text"> </span>
				</td>
				<td id="d1_id" style="width:20%;">
					<button class="button button_custom" id="test_d1">DO1</button>
                    <br>
					<span id="d1_text"> </span>
				</td>
				<td id="d2_id" style="width:20%;">
					<button class="button button_custom" id="test_d2">DO2</button>
                    <br>
					<span id="d2_text"> </span>
				</td>
				<td id="ao_id" style="width:20%;">
					<button class="button button_custom" id="test_audioout">AUDIO</button>
                    <br>
					<span id="audioout_text"> </span>
				</td>
				<td>
				<input type="text" maxlength="8" class="inputText" style="width:200px; height:20px;" name="txtPortNo" value="" numberonly="true">
				</td>
				<td><button name="cmdApply" class="button button_custom" onclick="onFocusCast();">FOCUS</button></td>
			<tr>		
		</table>
		<table class="fisheye_table">
			<!-- START FISHEYE_INPUT_BUFFER_OFFSET -->
			<tr>
				<td class="title">FISHEYE OFFSET CONTROL</td>
			</tr>
			<tr>
				<th>
					<input type="checkbox" name="chkOffsetX" onclick="onClickSelection(this);" id="chkOffsetX">
					<label for="chkOffsetX"></label><span>OFFSET X</span>
				</th>
				<td id="cal_x">
				</td>
			</tr>
			<tr id="cal_y_tr">
				<th>
					<input type="checkbox" name="chkOffsetY" onclick="onClickSelection(this);" id="chkOffsetY">
					<label for="chkOffsetY"></label><span>OFFSET Y</span>
				</th>
				<td id="cal_y">
				</td>
			</tr>
			<tr>
				<td colspan="2" align="center" class="fisheye_button">
					<button id="cmdApplyFisheyeOffset" class="button" >Apply</button>
					<button id="cmdApplyFisheyeCali" class="button">Auto Calibration</button>
				</td>
			</tr>
		</table>
		<!-- END FISHEYE_INPUT_BUFFER_OFFSET -->
    </div>    
	<div class="fisheye_div">
			<canvas id="fisheye_jpeg" width=320 height=240 ></canvas>
    </div>


<script>
	var gLanguage;
	var devInfo = <? $GLOBALS['system_conf']->getDevInfo();?> ;
	var model_list = new Array();
	var capInfo = <?  $GLOBALS['system_caps']->getCapability(); ?>;
	var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
	var fishInfo = <? $GLOBALS['media_conf']->getFisheyeInformation(NULL, 1); ?>;
    var testgpioInfo = new Object();
<?

	$filepath = "/root/ModelInfo.ini";
	$data = parse_ini_file($filepath, true);
	echo "model_list=" . json_encode($data) . ";\r\n";
	getLangSetup("gLanguage");

	$filepath_offset = "/root/imx226.cfg";
	if(file_exists($filepath_offset))
	{
		$content = file_get_contents($filepath_offset);
		$val = explode("\n", $content);
		foreach($val as $item){
			echo $item."\n";
		}
	}
    gpio_value("testgpioInfo");
?>
</script>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/lang.js"></script>
<script src="/js/page.js"></script>
<script src="/js/jpeg.js"></script>
<script src="./setup.js"></script>
<script defer src="/js/menu_config.js"></script>
</body>
</html>
