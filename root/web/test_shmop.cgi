<?
// cgi-bin/admin/vca-api/api.json
$filename = "/mnt/plugin/.config/vca-cored/configuration/api.json";

$json_body = file_get_contents($filename);
$arr = json_decode($json_body, true);

print_r($arr['observables']);

// var_dump($json_body);



// $fp = fsockopen("127.0.0.1", 80, $errno, $errstr, 30);pwd
// if (!$fp) {
//     echo "$errstr ($errno)<br />\n";
// } else {
//     $out = "GET / HTTP/1.1\r\n";
//     $out .= "Host: 127.0.0.1\r\n";
//     $out .= "Connection: Close\r\n\r\n";
//     fwrite($fp, $out);
//     while (!feof($fp)) {
//         echo fgets($fp, 128);
//     }
//     fclose($fp);
// }


exit();
// require('./cgi-bin/_define.inc');
// require("./cgi-bin/_upgrade.inc");
// require('./cgi-bin/class/system.class');
// require('./cgi-bin/class/capability.class');
// require('./cgi-bin/class/network.class');
// require('./cgi-bin/class/socket.class');

// 모드 "a" (세그멘트에 읽기전용으로 접근)
// 모드 "w" (세그멘트에 읽기, 쓰기)
// 모드 "c" (새로운 세그멘트를 작성, 그 세그멘트가 기존에 있는 경우는 읽기, 쓰기로 열기)
// 모드 "n" (새로운 세그멘트를 작성, 그 세그멘트가 기존에 있는 경우는 열기 실패로 인정하여 종료)
// 세번째 파라미터는 세그멘트이 퍼미션이다. 이 파라미터는 8진수의 값을 지정할 필요가 있다.
define('OFFSET_BASE',		0);
define('SETUP_PARAM_CAPABILITY',1);
define('SIZE_POS_INFO',		12);

function MakeDataFormat($_dataInfo)
{
	$dataFormat = '';
	while($data = current($_dataInfo))
	{
		$dataFormat .= $data['type'].key($_dataInfo)."/";
		next($_dataInfo);
	}
	return $dataFormat;
}
function GetDataInfoLength($_dataInfo)
{
	$totalLength = 0;
	foreach ($_dataInfo as $data)
	{
		$length = (int)substr($data['type'], 1);
		$type = substr($data['type'], 0, 1);
		if ($type == 'i' ||  $type == 'I')
		{
			$length *= 4;
		}
		$totalLength += $length;
	}
	return $totalLength;
}

function SetDataInfo($_dataClass, $_dataArray)
{
	// binary string into unpacked data
    // print_r($_dataArray);
	if (is_string($_dataArray)) {
		$_dataArray = unpack(MakeDataFormat($_dataClass->dataInfo), $_dataArray);
	}
    // print_r($_dataArray);
	// unpacked data into arrayed data
	foreach ($_dataClass->dataInfo as $key=>$data)
	{
		$_dataClass->dataInfo[$key]['value'] = $_dataArray[$key];
	}	
	
	//foreach ($_dataArray as $name=>$value)
	//{
	//	foreach ($_dataClass->dataInfo as $key=>$data)
	//	{
	//		if ($name == $key)
	//		{	
	//			$_dataClass->dataInfo[$name]['value'] = $value;
	//			break;
	//		}
	//	}
	//}
}

class CCapability
{
	private $shm_id;
	
	public 	$command;
	public 	$payload;
	public  $payloadLength;
	public	$dataInfo;
	public  $packFormat;
	public  $is_proxy_camera = false;

	function __construct($shmid = 0) 
	{
		$this->dataInfo = array('board_chipset'         => array('value'=>'', 'type'=>'a32'),
								'image_sensor'          => array('value'=>'', 'type'=>'a32'),
								'camera_module'         => array('value'=>'', 'type'=>'a32'),
								'ptz_module'            => array('value'=>'', 'type'=>'a32'),
								'camera_type'           => array('value'=>'', 'type'=>'a32'),
								'oem'                   => array('value'=>'', 'type'=>'a32'),
								'image_direction'       => array('value'=>0,  'type'=>'c1'),
								'max_resolution_width'  => array('value'=>0,  'type'=>'i1'),
								'max_resolution_height' => array('value'=>0,  'type'=>'i1'),
								'max_fps'               => array('value'=>0,  'type'=>'i1'),
								'max_stream'            => array('value'=>0,  'type'=>'c1'),
								'channels'              => array('value'=>0,  'type'=>'c1'),
								'video_in'              => array('value'=>0,  'type'=>'c1'),
								'video_out'             => array('value'=>0,  'type'=>'c1'),
								'osd'                   => array('value'=>0,  'type'=>'c1'),
								'audio_in'              => array('value'=>0,  'type'=>'c1'),
								'audio_in_gain'         => array('value'=>0,  'type'=>'c1'),
								'audio_out'             => array('value'=>0,  'type'=>'c1'),
								'audio_out_gain'        => array('value'=>0,  'type'=>'c1'),
								'sensor_count'          => array('value'=>0,  'type'=>'c1'),
								'relay_count'           => array('value'=>0,  'type'=>'c1'),
								'have_pantilt'          => array('value'=>0,  'type'=>'c1'),
								'have_zoom'             => array('value'=>0,  'type'=>'c1'),
								'have_zoom_button'      => array('value'=>0,  'type'=>'c1'),
								'have_digitalzoom'      => array('value'=>0,  'type'=>'c1'),
								'have_focus'            => array('value'=>0,  'type'=>'c1'),
								'have_iris'             => array('value'=>0,  'type'=>'c1'),
								'have_cds'              => array('value'=>0,  'type'=>'c1'),
								'have_sdcard'           => array('value'=>0,  'type'=>'c1'),
								'focus_mode'            => array('value'=>0,  'type'=>'c1'),
								'cds_adc'				=> array('value'=>0,  'type'=>'c1'),
								'ir_gpio'				=> array('value'=>0,  'type'=>'c1'),
								'mem_size'				=> array('value'=>0,  'type'=>'i1'),
								'max_record'			=> array('value'=>0,  'type'=>'c1'),
								'max_privacy'			=> array('value'=>7,  'type'=>'c1'),
								'rs485'					=> array('value'=>7,  'type'=>'c1'),
								'day_gpio'				=> array('value'=>0,  'type'=>'c1'),
								'night_gpio'			=> array('value'=>0,  'type'=>'c1'),
								'temperature_support'	=> array('value'=>0,  'type'=>'c1'), // temp_adc
								'relay' 		 		=> array('value'=>0,  'type'=>'a4'),
								'sensor' 				=> array('value'=>0,  'type'=>'a8'),
								'recovery_mode' 		=> array('value'=>0,  'type'=>'c1'),
								'tele_gpio' 			=> array('value'=>0,  'type'=>'c1'),
								'wide_gpio' 			=> array('value'=>0,  'type'=>'c1'),
								'photo_sensor_gpio' 	=> array('value'=>0,  'type'=>'c1'),
								'pwm' 					=> array('value'=>0,  'type'=>'c1'));
		// $this->payloadLength = 0;
		// $this->payloadLength += GetDataInfoLength($this->dataInfo);	

		$this->packFormat 	= MakeDataFormat($this->dataInfo);	

        // print ($this->packFormat);

		// $this->shm_id = 0;
		// if($shmid == 0)
		// {
		// 	$this->shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
		// 	if(!$this->shm_id) 
		// 	  exit;	

		// 	$shmid = $this->shm_id;  
		// }			
//                                             0                                     12         12
		$data_head = shmop_read($shmid, OFFSET_BASE + SETUP_PARAM_CAPABILITY*SIZE_POS_INFO, SIZE_POS_INFO);		// SIZE_POS_INFO = 4*3
		$positionInfo = unpack("i1index/i1offset/i1size", $data_head);
        print_r($positionInfo);

		$offset 		= $positionInfo['offset'];	
		$total_size      = $positionInfo['size'];

		// if($this->payloadLength != $total_size)
		// {
		//   echo 'CCapability failed: reason: data size is different'."\r\n";
		// 	exit;
		// }
		$data   = shmop_read($shmid, $offset, $total_size);
        
		// $this->UnpackDataInfo($data);
        $_dataArray = unpack($this->packFormat, $data);
        print_r($_dataArray);


		// if( $this->camera_type == "PROXY_CLIENT" 
		// 		|| $this->camera_type == "PREDATOR_CLIENT"
		// 		|| $this->camera_type == "PROXY_DUAL_CLIENT")
		// {
		// 	$this->is_proxy_camera = true;
		// }
	}
	// function __get($name)
	// {
	// 	switch($name)
	// 	{
	// 		case 'oem':
	// 		case 'image_direction':
	// 		case 'max_resolution_width':
	// 		case 'max_resolution_height':
	// 		case 'max_fps':
	// 		case 'max_stream':
	// 		case 'channels':
	// 		case 'video_in':
	// 		case 'video_out':
	// 		case 'osd':
	// 		case 'audio_in':
	// 		case 'audio_in_gain':
	// 		case 'audio_out':
	// 		case 'audio_out_gain':
	// 		case 'sensor_count':
	// 		case 'relay_count':
	// 		case 'have_pantilt':
	// 		case 'have_zoom':
	// 		case 'have_zoom_button':
	// 		case 'have_digitalzoom':
	// 		case 'have_focus':
	// 		case 'have_iris' :
	// 		case 'have_cds' :
	// 		case 'have_sdcard' :
	// 		case 'focus_mode':
	// 		case 'cds_adc':
	// 		case 'ir_gpio':
	// 		case 'mem_size':
	// 		case 'max_record':
	// 		case 'max_privacy':
	// 		case 'rs485':
	// 		case 'recovery_mode':
	// 		case 'pwm':
	// 		case 'is_proxy_camera':
	// 			{
	// 				return $this->dataInfo[$name]['value'];
	// 			}
	// 			break;
	// 		case 'camera_type':
	// 		case 'board_chipset' :
	// 		case 'image_sensor'  :
	// 		case 'camera_module' :
	// 		case 'ptz_module'    :
	// 			{
	// 				return trim($this->dataInfo[$name]['value']);
	// 			}
	// 		case 'temperature_support' : // temp_adc
	// 			{
	// 				return $this->dataInfo[$name]['value'] > 0 ? 1 : 0;
	// 			}
	// 	}
	// }

	// function __set($name,  $val) 
	// {
	// 	switch($name)
	// 	{
	// 		case 'board_chipset':			
	// 		case 'image_sensor':	
	// 		case 'camera_module':
	// 		case 'ptz_module':
	// 		case 'camera_type':
	// 		case 'oem':
	// 		case 'image_direction':
	// 		case 'max_resolution_width':
	// 		case 'max_resolution_height':
	// 		case 'max_fps':
	// 		case 'max_stream':
	// 		case 'channels':
	// 		case 'video_in':
	// 		case 'video_out':
	// 		case 'osd':
	// 		case 'audio_in':
	// 		case 'audio_in_gain':
	// 		case 'audio_out':
	// 		case 'audio_out_gain':
	// 		case 'sensor_count':
	// 		case 'relay_count':
	// 		case 'have_pantilt':
	// 		case 'have_zoom':
	// 		case 'have_zoom_button':
	// 		case 'have_digitalzoom':
	// 		case 'have_focus':	
	// 	    case 'have_iris' :	
	// 		case 'have_cds':
	// 		case 'have_sdcard' :
	// 		case 'focus_mode':
	// 		case 'cds_adc':
	// 		case 'ir_gpio':
	// 		case 'mem_size':
	// 		case 'max_record':
	// 		case 'max_privacy':
	// 		case 'rs485':
	// 		case 'recovery_mode':
	// 		case 'pwm':
	// 		{
	// 			$this->dataInfo[$name]['value'] = $val;
	// 		}
	// 		break;
	// 	}	
	// }
	// function __destruct() 
	// {
	//   if($this->shm_id)
	// 	  shmop_close($this->shm_id);
	// }
	
	// function SetPayload()
	// {
	// 	$this->command = 0;

	// 	$this->payload = '';
	// 	$this->payload .= MakePayload($this->dataInfo);		
	// }		

	// function UnpackDataInfo($_dataArray)
	// {
	// 	if (is_string($_dataArray)) 
	// 	{
	// 		$_dataArray = unpack($this->packFormat, $_dataArray);
	// 	}
    //     print_r ($_dataArray);
	// 	// SetDataInfo($this, $_dataArray);
	// 	//$this->SetPayload();
	// }			
// 	function getCapability($isJson=true)
// 	{

// 		$data = array();
// 		$data["board_chipset"]         = trim($this->board_chipset);
// 		$data["image_sensor"]          = trim($this->image_sensor);
// 		$data["camera_module"]         = trim($this->camera_module);
// 		$data["ptz_module"]            = trim($this->ptz_module);
// 		$data["camera_type"]           = trim($this->camera_type);
// //		$data["oem"]                   = trim($this->oem);
// 		$data["oem"]           		   = $GLOBALS['oem_map'][trim($this->oem)];
// 		$data["image_direction"]       = trim($this->image_direction);
// 		$data["max_resolution_width"]  = $this->max_resolution_width;
// 		$data["max_resolution_height"] = $this->max_resolution_height;
// 		$data["max_fps"]               = $this->max_fps;
// 		$data["channels"]              = $this->channels;
// 		$data["video_in"]              = $this->video_in;
// 		$data["video_out"]             = $this->video_out;
// 		$data["osd"]                   = $this->osd;
// 		$data["audio_in"]              = $this->audio_in;
// 		$data["audio_in_gain"]         = $this->audio_in_gain;
// 		$data["audio_out"]             = $this->audio_out;
// 		$data["audio_out_gain"]        = $this->audio_out_gain;
// 		$data["sensor_count"]          = $this->sensor_count;
// 		$data["relay_count"]           = $this->relay_count;
// 		$data["have_pantilt"]          = $this->have_pantilt;
// 		$data["have_zoom"]             = $this->have_zoom;
// 		$data["have_zoom_button"]      = $this->have_zoom_button;
// 		$data["have_digitalzoom"]      = $this->have_digitalzoom;
// 		$data["have_focus"]            = $this->have_focus;
//         $data["have_iris"]             = $this->have_iris;
// 		$data["have_cds"]              = $this->have_cds;
// 		$data["have_sdcard"]           = $this->have_sdcard;
// 		$data["focus_mode"]            = $this->focus_mode;
// 		$data["max_record"]            = $this->max_record;
// 		$data["max_stream"]            = $this->max_stream;
// 		$data['max_privacy']           = $this->max_privacy;
// 		$data['rs485']                 = $this->rs485;
// 		$data['recovery_mode']         = $this->recovery_mode;
// 		$data['is_proxy_camera']       = $this->is_proxy_camera;
// 		$data['temperature_support']   = $this->temperature_support;
// 		$data['pwm']   				   = $this->pwm;
// 		if( $isJson ) {
// 			echo json_encode($data);
// 		}
// 		else {
// 			echo view_encode($data);
// 		}
// 	}
	// function getOEM()
	// {
	// 	$oem = $GLOBALS['oem_map'][trim($this->oem)];
	// 	return $oem;
	// }
}
// $shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$shm_id = shmop_open(0x30000001, "a", 0, 0);
// $system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
// $net_conf = new CNetworkConfiguration($shm_id);
// $get_oem = $system_caps->getOEM();
// var_dump($shm_id);
// $x = shmop_read($shm_id, 0, 0);
// $data_head = shmop_read($shmid, OFFSET_BASE + SETUP_PARAM_CAPABILITY*SIZE_POS_INFO, SIZE_POS_INFO);		// SIZE_POS_INFO = 4*3
// $positionInfo = unpack("i1index/i1offset/i1size", $data_head);
shmop_close($shm_id);

// print_r($system_caps);



// print_r($system_conf);

// $filename = "/mnt/plugin/.config/vca-cored/configuration/api.json";

// print_r(json_decode(file_get_contents($filename), true));

?>