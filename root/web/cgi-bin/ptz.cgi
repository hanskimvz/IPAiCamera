<?
require('./_define.inc');
require('class/media.class');
require('class/ptz.class');
require('class/socket.class');
require('class/capability.class');


$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps  = new CCapability($shm_id);
$media_conf = new CMediaConfiguration();
//$presettour =  $GLOBALS['media_conf']->ProfileConfig->PTZConfiguration->presetTourConfig->tour[$index];
shmop_close($shm_id);

function wiper_view_post() // overview mode
{
  echo "input_wiper_enable=" . (int)$GLOBALS['media_conf']->ProfileConfig->PTZConfiguration->WiperAction->Enable . "\r\n";
  echo "input_wiper_speed=" . (int)$GLOBALS['media_conf']->ProfileConfig->PTZConfiguration->WiperAction->Speed. "\r\n";
  echo "input_wiper_timeout=" . (int)$GLOBALS['media_conf']->ProfileConfig->PTZConfiguration->WiperAction->Timeout . "\r\n";
}

if(isset( $_REQUEST['ptz_info'] )){
    if($GLOBALS['system_caps']->have_pantilt != 0){
        echo 'ptz';
    }
 	else if ($GLOBALS['system_caps']->have_zoom != 0)
	{
        echo 'z';
	}
    else {
		show_post_ng();
    }
	exit;
}
if ( isset($_REQUEST['continuouspantiltmove']) )
{
	//continuouspantiltmove=100,0
}

/*
	+-----------------------------------+
	|   setup1 = 1: pan/tilte 2: zoom	|
	+-----------------------------------+
 */
 if ( isset($_REQUEST['setup1']) )
{

}
$src = 0;
if( isset( $_REQUEST['source'] ) ) {
	$val = $_REQUEST['source'];
	if( $val >= 0 && $val <= $GLOBALS['system_caps']->video_in )
		$src = $val;
}
if( $src ) $src--; // VIN1 => array[0]
 /*
	+-----------------------------------------------------------------------+
	|   pantiltspeed = 														|
	|	speed =																|
	+-----------------------------------------------------------------------+
 */

if ( isset($_REQUEST['pantiltspeed']) || isset($_REQUEST['zoomspeed']) )
{
	$ptz_speed_req = new CPTZSpeedRequest();
	$ptz_speed_req->id = $src;
	if ( isset($_REQUEST['pantiltspeed']))
	{
	  $pt_speed = $_REQUEST['pantiltspeed'];	
	  $ptz_speed_req->speed->PanTilt = $pt_speed;//*$pt_speed*$pt_speed*10; // 1~10 => 1 ~ 10000
	}
	if ( isset($_REQUEST['zoomspeed']))
	{
	  $pt_zoom_speed = $_REQUEST['zoomspeed'];		
	  $ptz_speed_req->speed->Zoom = $pt_zoom_speed;//($pt_zoom_speed - 1)*1000 + 100;
	}

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($ptz_speed_req, CMD_PTZ_SET_SPEED);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
/*
	+-----------------------------------------------------------------------+
	|   move = left,right,down,up,upleft,upright,downleft,downright,stop	|
	|	speed = 1 ~ 10												|
	+-----------------------------------------------------------------------+
 */

if ( isset($_REQUEST['move']) )
{
  $jog_flag = 0;
	$requestCommand = $_REQUEST['move'];
	$x = 0;
	$y = 0;
	$z = 0;
	
	$speed = 1;
	  if ( isset($_REQUEST['speed']) )
	  {
			$pt_speed = $_REQUEST['speed'];
			if ( $pt_speed < 1 ) $pt_speed = 1;
			if ( $pt_speed > 100 ) $pt_speed =  100;
			$speed = $pt_speed * 100;  
			$jog_flag = 1;  
	  }
	switch ($requestCommand) {
		case 'left':			$x = -1; $y = 0; $z = 0;		break;
		case 'right':			$x = 1; $y = 0; $z = 0;		break;
		case 'up':			$x = 0; $y = 1; $z = 0;		break;
		case 'down':			$x = 0; $y = -1; $z = 0;		break;
		case 'upleft':			$x = -1; $y = 1; $z = 0;		break;
		case 'upright':		$x = 1; $y = 1; $z = 0;		break;
		case 'downleft':		$x = -1; $y = -1; $z = 0;		break;
		case 'downright':		$x = 1; $y = -1; $z = 0;		break;
		case 'stop':			$x = 0; $y = 0; $z = 0;		break;
		case 'jog':		
		{
		  $speed = 1;
		  $x = 0; $y = 0; $z = 0;	$jog_flag = 1;
		  if ( isset($_REQUEST['pan_speed']) )
		  {
		    $x = $_REQUEST['pan_speed'] * 1000;
	}
		  if ( isset($_REQUEST['tilt_speed']) )
	{
		    $y = $_REQUEST['tilt_speed'] * 1000;
		  }		
		  if ( isset($_REQUEST['zoom_speed ']) )
		  {
		    $z = $_REQUEST['zoom_speed'] * 1000;
		  }  
		}
		break;
	}

  if($jog_flag)
  {
	$ptz_ctrl = new  CPTZMoveRequest();
	$ptz_ctrl->id = $src;
	  	$ptz_ctrl->PanTilt = 1;
	  	$ptz_ctrl->Zoom = 0;
	$ptz_ctrl->vector->x = $x * $speed;
	$ptz_ctrl->vector->y = $y * $speed;
	$ptz_ctrl->vector->z = $z * $speed;
	$ptz_ctrl->timeout = -1;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($ptz_ctrl, CMD_PTZ_MOVE);
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
	{
	  	$ptz_ctrl = new  CPTZArrowRequest();
	  	$ptz_ctrl->id = $src;
	  	$ptz_ctrl->pan = $x;
	  	$ptz_ctrl->tilt = $y;
	  	$ipc_sock = new IPCSocket();
	  	$ipc_sock->Connection($ptz_ctrl, CMD_PTZ_ARROW);
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
/*
	+-----------------------------------+
	|   zoom = in,out,stop				|
	+-----------------------------------+
 */
if ( isset($_REQUEST['zoom']) )
{
	$requestCommand = $_REQUEST['zoom'];
	$x = 0;
	$y = 0;
	$z = 0;
	$speed = 5000;
	
	switch ($requestCommand) {
		case 'in':				$x = 0; $y = 0; $z = 1;		break;
		case 'out':			$x = 0; $y = 0; $z = -1;		break;
		case 'stop':			$x = 0; $y = 0; $z = 0;		break;
	}

	$ptz_ctrl = new  CZoomRequest();
	$ptz_ctrl->id = $src;
	$ptz_ctrl->zoom = $z ;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($ptz_ctrl, CMD_PTZ_ZOOM);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
/*
	+-----------------------------------+
	|	focus=near,far,stop				|
	+-----------------------------------+
 */
if ( isset($_REQUEST['focus']) )
{
	$requestCommand = $_REQUEST['focus'];
	$value = 0;
	
	switch ($requestCommand) {
		case 'far':				$value = -10000;		break;
		case 'near':			$value = 10000;		break;
		case 'stop':			$value = 0;		break;
	}
	
	$focus_ctrl = new  CFocusMoveRequest();
	$focus_ctrl->id = $src;
	$focus_ctrl->value  = $value ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($focus_ctrl, CMD_FOCUS_MOVE);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
/*
	+-----------------------------------+
	|	iris=open,close					|
	+-----------------------------------+
 */
if ( isset($_REQUEST['iris']) )
{
	$requestCommand = $_REQUEST['iris'];
	$value = 0;
	
	switch ($requestCommand) {
		case 'open':			$value = 10000;		break;
		case 'close':			$value = -10000;		break;
		case 'stop':			$value = 0;		break;
	}
		
	$iris_ctrl = new  CIrisMoveRequest();
	$iris_ctrl->id = $src;
	$iris_ctrl->value  = $value ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($iris_ctrl, CMD_IRIS_MOVE);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
/*
	+-----------------------------------+
	|	focusmode=auto, manual 			|
	+-----------------------------------+
 */
if ( isset($_REQUEST['focusmode']) )
{
	$requestCommand = $_REQUEST['focusmode'];
	$value = 0;
	
	switch ($requestCommand) {
		case 'auto':				$value = 1;		break;
		case 'manual':			$value = 0;		break;
	}
    $focus_mode_data = 0;
    $focus_mode_data = $focus_mode_data | $value << $src;
	$focus_mode = new  CFocusModeRequest();
	$focus_mode->id = $src;
	$focus_mode->mode->mode  = $focus_mode_data ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($focus_mode, CMD_SET_FOCUS_MODE);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}

/*
	+-----------------------------------+
	|	out1=on,off						|
	+-----------------------------------+
 */
if ( isset($_REQUEST['out1']) )
{
	
}

/*
	+-------------------------------------------+
	|	savepreset,gotopreset,removepreset		|
	+-------------------------------------------+
*/
if( isset($_REQUEST['savegroup'])){
	$prsettourindex = $_REQUEST['savegroup'] ;

	$presettourconfig = new CPresetTourSetRequest();	
	$presettourconfig->index = $prsettourindex - 1  ;
	$presettour = new CPresetTourConfig();

	$presettourconfig->tour = $presettour->tour[$prsettourindex];

	for($i=0 ; $i < 256 ; $i++)
	{		
		if(isset($_REQUEST['idx'.$i])){			
			$presettourconfig->tour->Position[$i]->mode  = 1 ;
		}
		if(isset($_REQUEST['idx'.$i])){			
			$presettourconfig->tour->Position[$i]->preset  = $_REQUEST['idx'.$i] - 1 ;
		}
		if(isset($_REQUEST['dt'.$i])){			
			$presettourconfig->tour->Position[$i]->param0  = $_REQUEST['dt'.$i];
		}
		if(isset($_REQUEST['sp'.$i])){			
			$presettourconfig->tour->Position[$i]->param1  = $_REQUEST['sp'.$i] ;
		}		
	}	
	
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($presettourconfig, CMD_SET_PRESET_TOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}	
}
if( isset($_POST['presettour'])){
	$preset_recv = json_decode($_POST['presettour'], true);
//	var_dump($preset_recv);
	
	$prsettourindex = $_POST['tour_index'] ;
//  $positonindex = 0; // 0~ 255	
	
	$presettourconfig = new CPresetTourSetRequest();
	
	$presettourconfig->index = $prsettourindex ;
	$presettour =  new CPresetTourConfig();

	$presettourconfig->tour = $presettour->tour[$prsettourindex];
	
	for($i=0 ; $i < 256 ; $i++)
	{
		if(isset($preset_recv[$i]['preset'])){			
			$potionindex = $preset_recv[$i]['index'] -1 ;				
			$presettourconfig->tour->Position[$potionindex]->mode  = 1 ;
			$presettourconfig->tour->Position[$potionindex]->preset  = $preset_recv[$i]['preset'] ;
			$presettourconfig->tour->Position[$potionindex]->param0  = $preset_recv[$i]['delay'] ;
			$presettourconfig->tour->Position[$potionindex]->param1  = $preset_recv[$i]['speed'] ;
		}
	}
		
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($presettourconfig, CMD_SET_PRESET_TOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
if ( isset($_REQUEST['savepreset']) )
{
    $index = 0; // 0~ 255

	$preset = new CPresetSetRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['savepreset'] ;
	if ( isset($_REQUEST['name']) )
	{
	  if (strlen($_REQUEST['name']) > 30) 
	  {
	    show_post_ng();
	    return;
	  }
	  $preset->name  = $_REQUEST['name'] ;
	}
	if ( isset($_REQUEST['shortcut']) )
	{
	  $preset->shortcut  = $_REQUEST['shortcut'] ;
	}
	
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_SET_PRESET);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['gotopreset']) )
{
    $index = 0; // 0~ 255

	$preset = new CPresetGotoRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['gotopreset'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_GOTO_PRESET);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['removepreset']) )
{
    $index = 0; // 0~ 255

	$preset = new CPresetRemoveRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['removepreset'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_REMOVE_PRESET);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['addpresettour']) )
{
	$prsettourindex = $_REQUEST['addpresettour'] ;
    $positonindex = 0; // 0~ 255	
	
	$presettourconfig = new CPresetTourSetRequest();
	
	$presettourconfig->index = $prsettourindex ;
	$presettour =  new CPresetTourConfig();
if(1)	{
	$presettourconfig->tour = $presettour->tour[$prsettourindex];
}else{		
	$presettourconfig->tour =  $GLOBALS['media_conf']->ProfileConfig->PTZConfiguration->presetTourConfig->tour[$prsettourindex];	
}
	$positonindex = $_REQUEST['postionindex'] ;	
//	for($i=0 ; $i < 256 ; $i++){
		$presettourconfig->tour->Position[$positonindex]->preset  = $_REQUEST['preset'] ;
		$presettourconfig->tour->Position[$positonindex]->param0  = $_REQUEST['delay'] ;
		$presettourconfig->tour->Position[$positonindex]->param1  = $_REQUEST['speed'] ;
//	}

//	for($i=0 ; $i < 256 ; $i++){
//		$presettourconfig->tour->Position[$positonindex]->preset  = $preset_recv[0][$i]['preset'] ;
//		$presettourconfig->tour->Position[$positonindex]->param0  = $preset_recv[0][$i]['delay'] ;
//		$presettourconfig->tour->Position[$positonindex]->param1  = $preset_recv[0][$i]['speed'] ;
//	}
//
//	echo $presettourconfig->tour->Position[$positonindex]->param0  ;
//	echo $presettourconfig->tour->Position[$positonindex]->param1  ;
		
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($presettourconfig, CMD_SET_PRESET_TOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['removepresettour']) )
{
    $index = $_REQUEST['removepresettour']; // 0~ 255

	$preset = new CPresetTourSetRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['removepresettour'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_REMOVE_PRESET_TOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['runscan']) )
{

}
else if ( isset($_REQUEST['runpattern']) )
{

}
else if ( isset($_REQUEST['runpresettour']) )
{
	$index = $_REQUEST['runpresettour']; // 0~ 255

	$preset = new CPresetTourSetRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['runpresettour'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_OPERATE_PRESET_TOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}

}
else if ( isset($_REQUEST['sethomeposition']) )
{
	$index = $_REQUEST['sethomeposition']; // 

	$preset = new CPresetTourSetRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['sethomeposition'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_SET_HOME_POSITION);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['gotohomeposition']) )
{
	$index = $_REQUEST['gotohomeposition']; // 

	$preset = new CPresetTourSetRequest();
	$preset->id = 0;
	$preset->index  = $_REQUEST['gotohomeposition'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_GOTO_HOME_POSITION);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}

}
else if ( isset($_REQUEST['getpreset']) )
{
	$presetconfig = new CPresetConfig();

	$ipc_sock = new IPCSocket();				
	$ipc_sock->Connection( $presetconfig, CMD_GET_PRESETS);	

	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_preset($presetconfig, 1);					
//		show_post_ok();
	}
	else
	{
		show_post_ng();
	}

}
else if ( isset($_REQUEST['getpresetTour']) )
{
	$presettourconfig =  new CPresetTourConfig();
	
	$ipc_sock = new IPCSocket();				
	$ipc_sock->Connection( $presettourconfig, CMD_GET_PRESET_TOURS);	
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_presettour($presettourconfig, 1);	
//		show_post_ok();
	}
	else
	{
		show_post_ng();
	}

}
else if ( isset($_REQUEST['setaux']) )
{
    $index = $_REQUEST['setaux']; // 0~ 255

	$preset = new CPresetTourRemoveRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['setaux'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_SET_PTZ_AUX);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['clearaux']) )
{
    $index = $_REQUEST['clearaux']; // 0~ 255

	$preset = new CPresetTourRemoveRequest();
	$preset->id = $src;
	$preset->index  = $_REQUEST['clearaux'] ;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($preset, CMD_CLEAR_PTZ_AUX);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
else if ( isset($_REQUEST['testtour']) )
{
	$presettourconfig = new CPresetTourSetRequest();
	$presettour = new CPresetTourConfig();
	$presettourconfig->index = 0  ;
	$presettourconfig->tour = $presettour->tour[1];

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($presettourconfig, CMD_SET_TESTTOUR);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();
	}
	else
	{
		show_post_ng();
	}
}
 /*
	+-----------------------------------------------------------------------+
	|   Digital zoom, auto flip, powerup action, parking actio							|
	|	                                    											  					|
	+-----------------------------------------------------------------------+
 */

if ( isset($_REQUEST['msubmenu']))
{
  $ptz_req;
  $ptz_command;
  if($_REQUEST['msubmenu'] == 'dzoom')
  {
    if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
    {
        if ( isset($_REQUEST['enabled']))
        {
        	$ptz_req = new CPtzCommonSetRequest();
        	$ptz_req->id = $src;   
        	$ptz_req->value = $_REQUEST['enabled'];
        	$ptz_command = CMD_SET_DIGITAL_ZOOM;
        }
    }
    else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
    {
      //$media_conf = new CMediaConfiguration();
      //$digitalZoom =  $media_conf->ProfileConfig->PTZConfiguration->DigitalZoomMode;    
    }
    else
    {
      show_post_ng();
      return;
    }
  }
  else if($_REQUEST['msubmenu'] == 'autoflip')
  {
    if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
    {
        if ( isset($_REQUEST['enabled']))
        {
        	$ptz_req = new CPtzCommonSetRequest();
        	$ptz_req->id = $src;   
        	$ptz_req->value = $_REQUEST['enabled'];
        	$ptz_command = CMD_SET_PANTILT_AUTO_FLIP;    
        }
    }
    else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
    {
      //$media_conf = new CMediaConfiguration();
      //$autoFlip =  $media_conf->ProfileConfig->PTZConfiguration->AutoFlip;        
    }    
    else
    {
      show_post_ng();
      return;
    }  
  }
  else if($_REQUEST['msubmenu'] == 'wiper') // overview mode
  {
	  if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
	  {
		  if(isset($_REQUEST['enabled']))
		  {
			  if(!isset($_REQUEST['speed']) || !isset($_REQUEST['timeout']))
			  {
				  show_post_ng();
				  return;
			  }
			  $ptz_req = new CWiperActionSetRequest();
			  $ptz_req->id = 0;
			  if(isset($_REQUEST['enabled']))
			  {
				  $ptz_req->WiperAction->Enable = $_REQUEST['enabled'];
			  }
			  if(isset($_REQUEST['speed']))
			  {
				  $ptz_req->WiperAction->Speed = $_REQUEST['speed'];
			  }
			  if(isset($_REQUEST['timeout']))
			  {
				  $ptz_req->WiperAction->Timeout = $_REQUEST['timeout'];
			  }
			  $ptz_command = CMD_SET_WIPER;
		  }
	  }
	  else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
	  {
		  wiper_view_post(); //check wiper data
		  //$media_conf = new CMediaConfiguration();
		  //$autoFlip =  $media_conf->ProfileConfig->PTZConfiguration->AutoFlip;
	  }
	  else
	  {
		  show_post_ng();
		  return;
	  }
  }
  else if($_REQUEST['msubmenu'] == 'invert')  // overview mode
  {
	  if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
	  {
		  if ( isset($_REQUEST['enabled']))
		  {
			  $ptz_req = new CPtzCommonSetRequest();
			  $ptz_req->id = 0;
			  $ptz_req->value = $_REQUEST['enabled'];
			  $ptz_command = CMD_SET_INVERT;
		  }
	  }
	  else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
	  {
		  //$media_conf = new CMediaConfiguration();
		  //$invert =  $media_conf->ProfileConfig->PTZConfiguration->InvertMode;
	  }
	  else
	  {
		  show_post_ng();
		  return;
	  }
  }
  else if($_REQUEST['msubmenu'] == 'washer')  // overview mode
  {
	  if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
	  {
		  if ( isset($_REQUEST['enabled']))
		  {
			  $ptz_req = new CPtzCommonSetRequest();
			  $ptz_req->id = 0;
			  $ptz_req->value = $_REQUEST['enabled'];
			  $ptz_command = CMD_SET_WASHER;
		  }
	  }
	  else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
	  {
		  //$media_conf = new CMediaConfiguration();
		  //$washer =  $media_conf->ProfileConfig->PTZConfiguration->WasherRT;
	  }
	  else
	  {
		  show_post_ng();
		  return;
	  }
  }
  else if($_REQUEST['msubmenu'] == 'powerupaction')
  {
    if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
    {
      if ( isset($_REQUEST['enabled']))
      {
        if($_REQUEST['enabled'] != 0)
        {
          if(!isset($_REQUEST['actiontype']) )
          {
            show_post_ng();
            return;        
          }
        }
      	$ptz_req = new CPowerUpActionSetRequest();
      	$ptz_req->id = $src;   
      	if(isset($_REQUEST['enabled']))
      	{
      	  $ptz_req->powerUpAction->Enable = $_REQUEST['enabled'];    
      	}
      	if(isset($_REQUEST['actiontype']))
      	{
      	  $ptz_req->powerUpAction->Action = $_REQUEST['actiontype'];
      	}    
      	if(isset($_REQUEST['index']))
      	{
      	  $ptz_req->powerUpAction->Number = $_REQUEST['index']; 
      	}  
        $ptz_command = CMD_SET_POWERUP_ACTION;   
      }
    }
    else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
    {
      //$media_conf = new CMediaConfiguration();
      //$media_conf->ProfileConfig->PTZConfiguration->PowerUpAction->Enable;  
      //$media_conf->ProfileConfig->PTZConfiguration->PowerUpAction->Action; 
      //$media_conf->ProfileConfig->PTZConfiguration->PowerUpAction->Number;     
    }    
    else
    {
      show_post_ng();
      return;
    }  
  }
  else if($_REQUEST['msubmenu'] == 'parkingaction')
  {
    if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
    {
      if ( isset($_REQUEST['enabled']))
      {
        if($_REQUEST['enabled'] != 0)
        {
          if(!isset($_REQUEST['actiontype']) || !isset($_REQUEST['waittime']) )
          {
            show_post_ng();
            return;        
          }
        }    
      	$ptz_req = new CParkingActionSetRequest();
      	$ptz_req->id = $src;   
      	if(isset($_REQUEST['enabled']))
      	{
      	  $ptz_req->parkingAction->Enable = $_REQUEST['enabled'];    
      	}
      	if(isset($_REQUEST['waittime']))
      	{
      	  $ptz_req->parkingAction->WaitTime = $_REQUEST['waittime']; 
      	}
      	if(isset($_REQUEST['actiontype']))
      	{
      	  $ptz_req->parkingAction->Action = $_REQUEST['actiontype'];    
      	}
      	if(isset($_REQUEST['index']))
      	{
      	  $ptz_req->parkingAction->Number = $_REQUEST['index'];   
      	}
        $ptz_command = CMD_SET_PARKING_ACTION; 
      }
    }
    else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
    {
      //$media_conf = new CMediaConfiguration();
      //$media_conf->ProfileConfig->PTZConfiguration->ParkingAction->Enable;  
      //$media_conf->ProfileConfig->PTZConfiguration->ParkingAction->WaitTime;
      //$media_conf->ProfileConfig->PTZConfiguration->ParkingAction->Action; 
      //$media_conf->ProfileConfig->PTZConfiguration->ParkingAction->Number;       
    }    
    else
    {
      show_post_ng();
      return;
    }  
  }
  else if($_REQUEST['msubmenu'] == 'absolutemove')
  {
	  if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
	  {
		  $ptz_req = new CPTZPositionMoveRequest();
		  $ptz_req->id = 0;
		  if(!isset($_REQUEST['x']) || !isset($_REQUEST['y']) || !isset($_REQUEST['z']) || !isset($_REQUEST['speed']))
		  {
			  show_post_ng();
			  return;
		  }
		  else
		  {
			  $ptz_req->position->x = $_REQUEST['x'] * 100000;
			  $ptz_req->position->y = $_REQUEST['y'] * 100000;
			  $ptz_req->position->z = $_REQUEST['z'] * 100000;
			  $ptz_req->speed->PanTilt = $_REQUEST['speed'] * 10000;
			  $ptz_req->speed->Zoom = $_REQUEST['speed'] * 10000;  // not used
			  $ptz_req->PanTilt = 1;
			  $ptz_req->Zoom = 1;
		  }
		  $ptz_command = CMD_PTZ_POSITION_MOVE;
	  }
	  else if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'view')
	  {
		  $ptz_pos = new CPTZPositionGetRequest();
		  $ipc_sock = new IPCSocket();
		  $ipc_sock->Connection($ptz_pos, CMD_PTZ_GET_POSITION);
		  echo "x : " . $ptz_pos->ptz->x / 100000 . "\r\n<br>";
		  echo "y : " . $ptz_pos->ptz->y / 100000 . "\r\n<br>";
		  echo "z : " . $ptz_pos->ptz->z / 100000 . "\r\n<br>";
	  }
	  else
	  {
		  show_post_ng();
		  return;
	  }
  }

  if ( isset($_REQUEST['action']) && $_REQUEST['action'] == 'apply')
  {
	  $ipc_sock = new IPCSocket();
	  $ipc_sock->Connection($ptz_req, $ptz_command);
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
?>
