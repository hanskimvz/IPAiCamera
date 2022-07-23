<?
require('../_define.inc');
require('../class/camera.class');
require('../class/capability.class');
require('../class/socket.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$camera_configs = new CCameraConfigurations($shm_id);
$system_caps = new CCapability($shm_id);
// using another shared memory
$profiles = $camera_configs->config[0]->profile_info;

$thermal_type = '/(thermal)/';
$seekthermal_type = '/(seekware)/';

if( preg_match($thermal_type, $system_caps->camera_type) ) 
{
	require('../sensor/thermal.inc');
} 
else if( preg_match($seekthermal_type, $system_caps->camera_type) ) 
{
	require('../sensor/seekthermal.inc');
} 
else if( preg_match("/sony_/i", $system_caps->camera_module )){
	require('../sensor/sony_define.inc');
}
else if( preg_match("/wonwoo_/i", $system_caps->camera_module )){
	require('../sensor/wonwoo_define.inc');
}
else if( preg_match("/ytot_/i", $system_caps->camera_module )){
	require('../sensor/ytot_define.inc');
}
else if( preg_match("/esca_/i", $system_caps->camera_module )){
	require('../sensor/esca_define.inc');
}
else if( preg_match("/ov_/i", $system_caps->camera_module )){
	require('../sensor/ov_define.inc');
}
else{
	if( preg_match("/amba_s2e/i", $system_caps->board_chipset )){
		require('../sensor/_s2e_define.inc');
	} else if( preg_match("/amba_s2l/i", $system_caps->board_chipset)) {
		require('../sensor/_s2l_define.inc');
	} else if( preg_match("/amba_s3l/i", $system_caps->board_chipset)) {
		require('../sensor/_s3l_define.inc');
	} else if( preg_match("/amba_s5l/i", $system_caps->board_chipset)) {
		require('../sensor/_s5l_define.inc');
	} else if( preg_match("/amba_s2/i", $system_caps->board_chipset)) {
		require('../sensor/_s2_define.inc');
	} else if( preg_match("/amba_cv22/i", $system_caps->board_chipset)) {
		require('../sensor/_cv22_define.inc');
	} else if( preg_match("/amba_s6lm/i", $system_caps->board_chipset)) {
		require('../sensor/_s6lm_define.inc');
	} else {
		require('../sensor/_a5s_define.inc');
	}
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
function view_camera_profile()
{
	$count=0;
	for( $i=0; $i < MAX_CAMERA_PROFILE ; $i++)
		if( $GLOBALS['profiles']->Profile[$i]->Id != 0 ) $count++;
	echo "Profile(" . $count . "/" . MAX_CAMERA_PROFILE . ")\r\n";

	$count=0;
	for( $i=0; $i < MAX_CAMERA_PROFILE ; $i++)
	{
		if( $GLOBALS['profiles']->Profile[$i]->Id != 0 )
		{
			echo "[profile". (++$count) . "]\r\n";
			echo "id=" . trim($GLOBALS['profiles']->Profile[$i]->Id) . "\r\n";
			echo "fixed=" . trim($GLOBALS['profiles']->Profile[$i]->Fixed) . "\r\n";
			echo "name="  . trim($GLOBALS['profiles']->Profile[$i]->ProfileName) . "\r\n";
		}
	}
}

function change_camera_profile_id()
{
	if( !isset($_REQUEST['id'])) return 1;
	return 0;
}
function change_camera_profile_name()
{
	if( !isset($_REQUEST['name'])) return 1;
	return 0;
}
function add_camera_profile()
{
	if( change_camera_profile_name() ) return 1;
	$new_profile = new CameraProfileHeader();
	$new_profile->Id = 0;
	$new_profile->ProfileName= $_REQUEST['name'];
	$new_profile->Fixed = 0;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($new_profile, CMD_ADD_CAMERA_PROFILE);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		return 0;
	}
	else
	{
		return 1;
	}
}

function apply_camera_profile()
{
	$result = false;
	if( !change_camera_profile_id() ) {
		for( $index=0; $index < MAX_CAMERA_PROFILE ; $index++ ) {
			if($_REQUEST['id'] == $GLOBALS['profiles']->Profile[$index]->Id ){
				$apply_profile = $GLOBALS['profiles']->Profile[$index];
				$result = true;
				break;
			}
		}
	}
	if( !change_camera_profile_name() ) {
		$name = trim($_REQUEST['name']);
		for( $index=0; $index < MAX_CAMERA_PROFILE ; $index++ ) {
			if($name == trim($GLOBALS['profiles']->Profile[$index]->ProfileName) ){
				$result = true;
				$apply_profile = $GLOBALS['profiles']->Profile[$index];
				break;
			}
		}
	}


	if( $result ) {
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($apply_profile, CMD_APPLY_CAMERA_PROFILE);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else 
		{
			show_post_ng();
			echo "[ERROR_CODE:".$ipc_sock->dataInfo['ErrorCode']['value'] . "]\r\n";
		}
	}
	return 1;
}
function modify_camera_profile()
{
	if( change_camera_profile_id() ) return 1;
	if( change_camera_profile_name() ) return 1;
	$modify_profile = new CameraProfileHeader();
	$modify_profile->Id = $_REQUEST['id'];
	$modify_profile->ProfileName= $_REQUEST['name'];
	$modify_profile->Fixed = 0;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($modify_profile, CMD_MODIFY_CAMERA_PROFILE);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) return 1;

	return 0;
}

function delete_camera_profile()
{
	$result = false;
	if( !change_camera_profile_id() ){
		for( $index=0; $index < MAX_CAMERA_PROFILE ; $index++ ) {
			if($_REQUEST['id'] == $GLOBALS['profiles']->Profile[$index]->Id ){
				$del_profile = $GLOBALS['profiles']->Profile[$index];
				$result = true;
				break;
			}
		}
	}
	if( !change_camera_profile_name() ) {
		$name = trim($_REQUEST['name']);
		for( $index=0; $index < MAX_CAMERA_PROFILE ; $index++ ) {
			if($name == trim($GLOBALS['profiles']->Profile[$index]->ProfileName) ){
				$del_profile = $GLOBALS['profiles']->Profile[$index];
				$result = true;
				break;
			}
		}
	}
	if( $result ) {
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($del_profile, CMD_DELETE_CAMERA_PROFILE);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			return 0;
	}

	return 1;
}

function ViewPrivacy()
{
	for( $idx = 0 ; $idx < MAX_MEDIA_SOURCE ; $idx++ )
	{
		echo "[source=".($idx+1) ."]\r\n";
		$privacy_mask = $GLOBALS['camera_configs']->config[$idx]->privacy_mask;
		echo "Enable=" . $privacy_mask->Enabled . "\r\n";
		for($j=0; $j<MAX_PRIVACY_MASK; ++$j)
		{
			echo "[area".$j ."]\r\n";
			echo "start_x=" . $privacy_mask->privacy_info[$j]->StartX . "\r\n";
			echo "start_y=" . $privacy_mask->privacy_info[$j]->StartY . "\r\n";
			echo "width="   . $privacy_mask->privacy_info[$j]->Width  . "\r\n";
			echo "height="  . $privacy_mask->privacy_info[$j]->Height . "\r\n";
		}
		echo "\r\n";
	}
}

function ViewCamera($src=0)
{
	$camData = $GLOBALS['camera_configs'];
	echo "[source=".($src+1) ."]\r\n";
	for( $i = (CAMERA_CODE_START + 1) ; $i < CAMERA_CODE_END ; $i ++) {
		$list = $GLOBALS['list'];
		if( $list[$i] == "hdr" ) {
			echo "wdr=".$camData->config[$src]->code[$i]->data .";\r\n";
		}
		else if( $list[$i] == "hdr_level" ){
			echo "wdr_level=".$camData->config[$src]->code[$i]->data .";\r\n";
		}
		else {
			echo $list[$i] ."=".$camData->config[$src]->code[$i]->data .";\r\n";
		}
	}
	echo "\r\n";
}

function alignment_get_type($SensorAlignment)
{
	if ( !isset($_REQUEST['type']) ) return 1;
	switch ( $_REQUEST['type'] )
	{
	case 'stop' :
		$SensorAlignment->Type = 2; break;
	case 'continous' :
		$SensorAlignment->Type = 1; break;
	case 'step' :
		$SensorAlignment->Type = 0; break;
	default :
		return 1;
	}
	return 0;
}

function alignment_get_direction($SensorAlignment)
{
	if ( !isset($_REQUEST['direction']) ) return 0;
	$SensorAlignment->Direction = $_REQUEST['direction'];
	return 0;
}

$is_changed = false;

$count = count($_REQUEST) -2 ;

$MAX_LIST = count($list);

$preview = false;
$menu = null;

header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['action']) && $_REQUEST['action'] == 'preview')
	$preview = true;

if(isset($_REQUEST['submenu']) && $_REQUEST['submenu']) $menu = $_REQUEST['submenu'];
if(isset($_REQUEST['msubmenu']) && $_REQUEST['msubmenu']) $menu = $_REQUEST['msubmenu'];

$src = 0;
if( isset( $_REQUEST['source'] ) ) {
	$val = $_REQUEST['source'];
	if( $val >= 0 && $val <= $GLOBALS['system_caps']->video_in )
		$src = $val;
}
if( $src ) $src--; // VIN1 => array[0]
if( $menu == 'camera')
{
	if ($_REQUEST['action'] == 'apply' || $preview )
	{
        for( $i = 0 ; $i < $MAX_LIST ; $i++)
        {
            if( $GLOBALS['system_caps']->camera_type == 'PREDATOR_CLIENT' || $GLOBALS['system_caps']->camera_type == 'PREDATOR_SERVER'){
                if( isset( $_REQUEST[ 'tdn_bw_level' ])||isset( $_REQUEST[ 'tdn_color_level' ])){
                    show_post_ng();
                    exit;
                }
            }

            if( isset( $_REQUEST[ 'wdr' ])) 
				$_REQUEST[ 'hdr' ] = $_REQUEST[ 'wdr' ];
			if( isset( $_REQUEST[ 'wdr_level' ]))
				$_REQUEST[ 'hdr_level' ] = $_REQUEST[ 'wdr_level' ];
            
			if( isset( $_REQUEST[ $list[$i] ] ) && ( $preview == true 
				|| $_REQUEST[ $list[$i] ] != $GLOBALS['camera_configs']->config[$src]->code[$i]->data ) )
			{
				//if( $preview )
				//{
				//	$ipc_sock = new IPCSocket();
				//	$param = new CCameraParam();
				//	$param->index =  $i;
				//	$param->value = $_REQUEST[ $list[$i] ];
				//	$ipc_sock->Connection($param, CMD_SET_CAMERA_PARAM);
				//	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				//	{
				//		show_post_ok();
				//		exit;
				//	}
				//	else
				//	{
				//		show_post_ng();
				//		echo "Error Code=" . $ipc_sock->dataInfo['ErrorCode']['value'];
				//		exit;
				//	}
				//}
				//else
				$GLOBALS['camera_configs']->config[$src]->code[$i]->data = $_REQUEST[ $list[$i]];
				$is_changed = true;
			}
		}
		// APPLY 
		if( $is_changed && ! $preview)
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['camera_configs'], CMD_SET_CAMERA_SETUP, $src );
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
				exit;
			}
			else
			{
				show_post_ng();
				echo "Error Code=" . $ipc_sock->dataInfo['ErrorCode']['value'];
				exit;
			}
		}
	}
	else if ( $_REQUEST['action'] == 'reset')
	{
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection(0, CMD_SET_CAMERA_DEAFULT);

		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
			exit;
		}
		else
		{
			show_post_ng();
			exit;
		}
	}
	else if ( $_REQUEST['action'] == 'view' )
	{
		if( !isset($_REQUEST['source'] ) ) {
			for( $idx = 0 ; $idx < $GLOBALS['system_caps']->video_in ; $idx++) {
				ViewCamera($idx);
			}
		}
		else {
			// VIN1 => array[0]
			ViewCamera($src);
		}
		exit;
	}
	else if ( $_REQUEST['action'] == 'restore') 
	{
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection(0, CMD_SET_CAMERA_RESTORE);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
			exit;
		}
		else
		{
			show_post_ng();
			exit;
		}
	}
	else if ( $_REQUEST['action'] == 'setwbpreset' )
	{
		$ipc_sock = new IPCSocket();
		$cameraparam = new CCameraParam();
		if( preg_match("/sony_/i", $system_caps->camera_module )) 	$cameraparam->index = CAMERA_AWB_ONE_PUSH ;
		else if( preg_match("/esca/i", $system_caps->camera_module )) 	$cameraparam->index = CAMERA_WB_PRESET ;

		$cameraparam->value = $_REQUEST['value'];
		$ipc_sock->Connection( $cameraparam, CMD_SET_CAMERA_PARAM);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
			exit;
		}
		else
		{
			show_post_ng();
			exit;
		}
	}
	else if ( $_REQUEST['action'] == 'sethwfilter' )
	{
		$ipc_sock = new IPCSocket();
		$cameraparam = new CCameraParam();

		$cameraparam->index = CAMERA_DN_MODE ;

		$cameraparam->value = $_REQUEST['value'];
		$ipc_sock->Connection( $cameraparam, CMD_SET_CAMERA_PARAM);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
			exit;
		}
		else
		{
			show_post_ng();
			exit;
		}
	}
	else if ( $_REQUEST['action'] == 'getfoglevel' )
	{
		$ipc_sock = new IPCSocket();
		$cameraparam = new CCameraParam();
		$cameraparam->index = CAMERA_FILTER_FOG_LEVEL ;
		$ipc_sock->Connection( $cameraparam, CMD_GET_CAMERA_PARAM);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			echo "foglevel=".$cameraparam->value ;
			//			show_post_ok();
			exit;
		}
		else
		{
			show_post_ng();
			exit;
		}
	}
	else if ( $_REQUEST['action'] == 'default') 
	{
		if( isset($_REQUEST['menu'] ) )
		{
			$param = new CCameraParam();
			$param->value = $src;
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($param, (CMD_SET_CAMERA_GROUP_DEFAULT0 + $_REQUEST['menu']) );
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
				exit;
			}
			else
			{
				show_post_ng();
				exit;
			}
		}
	}
	else if ( $_REQUEST['action'] == 'setparam') 
	{
		if( isset($_REQUEST['code'])  && isset($_REQUEST['value']) ) 
		{
				$ipc_sock = new IPCSocket();
				$param = new CCameraParam();
				$param->index = $_REQUEST['code'];
				$param->value = $_REQUEST['value'];
				$ipc_sock->Connection($param, CMD_SET_CAMERA_PARAM);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
					exit;
				}
				else
				{
					show_post_ng();
					echo "Error Code=" . $ipc_sock->dataInfo['ErrorCode']['value'];
					exit;
				}
		}
	}
}
//todo : hjlee
else if( $menu == "profiles")
{
	if( !isset($_REQUEST['action']) )
	{
		show_post_ng();
		exit;
	}
	$action = $_REQUEST['action'];
	if( $action == "view" ) 
	{
		view_camera_profile();
		exit;
	}
	else if($action == "add") 
	{
		if( add_camera_profile() )
			show_post_ng();
		else
			show_post_ok();
		exit;
	}
	else if($action == "modify") 
	{
		if( modify_camera_profile() == 0 )
		{
			show_post_ok();
			exit;
		}
		else 
		{
			show_post_ng();
			exit;
		}
	}
	else if($action == "apply") 
	{
		apply_camera_profile();
		exit;
	}
	else if($action == "delete") 
	{
		if( delete_camera_profile() == 0 )
		{
			show_post_ok();
			exit;
		}
		else 
		{
			show_post_ng();
			exit;
		}
	}
}
else if( $menu == "privacy_mask") 
{
	if( !isset($_REQUEST['action']) )
	{
		show_post_ng();
		exit;
	}
	$action = $_REQUEST['action'];
	if( $action == "view" )
	{
		ViewPrivacy();
		exit;
	}
	else if ( $action == "apply")
	{
		$change = false;
		$privacy_mask = $GLOBALS['camera_configs']->config[$src]->privacy_mask;
		if( isset($_REQUEST['enabled'])) 
		{
			$privacy_mask->Enabled = $_REQUEST['enabled'];
			$change = true;
		}

		for( $i=0 ; $i<MAX_PRIVACY_MASK ;++$i)
		{
			if( isset($_REQUEST['start_x'.$i])) 
			{
				$privacy_mask->privacy_info[$i]->StartX = $_REQUEST['start_x'.$i];
				$change = true;
			}
			if( isset($_REQUEST['start_y'.$i])) 
			{
				$privacy_mask->privacy_info[$i]->StartY = $_REQUEST['start_y'.$i];
				$change = true;
			}
			if( isset($_REQUEST['width'.$i])) 
			{
				$privacy_mask->privacy_info[$i]->Width = $_REQUEST['width'.$i];
				$change = true;
			}
			if( isset($_REQUEST['height'.$i])) 
			{
				$privacy_mask->privacy_info[$i]->Height = $_REQUEST['height'.$i];
				$change = true;
			}
		}
		if( $change )
		{	
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['camera_configs'], CMD_SET_PRIVACY_MASK);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
				exit;
			}
			else
			{
				show_post_ng();
				exit;
			}
		}
	}
}
else if( $menu == "alignment") 
{
	$SensorAlignment = new CSensorAlignment();
	if ( alignment_get_type($SensorAlignment) || alignment_get_direction($SensorAlignment) )
	{
		show_post_ng();
		exit;
	}

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($SensorAlignment,  CMD_SET_SENSOR_ALIGNMENT, $src);
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
show_post_ng();
?>
