<?
require('../_define.inc');
require('../class/capability.class');
require('../class/media.class');
require('../class/event.class');
require('../class/socket.class');


$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
if(!$shm_id) exit;
$system_caps = new CCapability($shm_id);
$channel_conf = new CChannelConfiguration($shm_id);
$event_conf = new CEventConfiguration($shm_id);
shmop_close($shm_id);


//--- alarm_input #1~8
function alarmin_view_post($num)
{
	if ($GLOBALS['system_caps']->sensor_count == 0) {
		show_post_ng();
		return;
	}

	echo "device="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->device."\r\n";
	echo "activation="	.$GLOBALS['event_conf']->alarm_input_conf[$num]->always."\r\n";
	echo "sun="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->sun."\r\n";
	echo "mon="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->mon."\r\n";
	echo "tue="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->tue."\r\n";
	echo "wed="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->wed."\r\n";
	echo "thu="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->thu."\r\n";
	echo "fri="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->fri."\r\n";
	echo "sat="			.$GLOBALS['event_conf']->alarm_input_conf[$num]->week->sat."\r\n";
	echo "shour="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->start_hour."\r\n";
	echo "smin="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->start_min."\r\n";
	echo "ehour="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->end_hour."\r\n";
	echo "emin="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->end_min."\r\n";
	echo "output="		.$GLOBALS['event_conf']->alarm_input_conf[$num]->action->output."\r\n";
	echo "duration="	.$GLOBALS['event_conf']->alarm_input_conf[$num]->action->duration."\r\n";
	echo "transfer="	.$GLOBALS['event_conf']->alarm_input_conf[$num]->action->transfer."\r\n";
}

function change_alarmin_device($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['device'])) return 1;
	if($_REQUEST['device']<0 || $_REQUEST['device']>2) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->device = $_REQUEST['device'];
	return 0;
}

function change_alarmin_always($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['activation'])) return 1;
	if($_REQUEST['activation']<0 || $_REQUEST['activation']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->always = $_REQUEST['activation'];
	return 0;
}

function change_alarmin_sun($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['sun'])) return 1;
	if($_REQUEST['sun']<0 || $_REQUEST['sun']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->sun = $_REQUEST['sun'];
	return 0;
}

function change_alarmin_mon($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['mon'])) return 1;
	if($_REQUEST['mon']<0 || $_REQUEST['mon']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->mon = $_REQUEST['mon'];
	return 0;
}

function change_alarmin_tue($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['tue'])) return 1;
	if($_REQUEST['tue']<0 || $_REQUEST['tue']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->tue = $_REQUEST['tue'];
	return 0;
}

function change_alarmin_wed($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['wed'])) return 1;
	if($_REQUEST['wed']<0 || $_REQUEST['wed']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->wed = $_REQUEST['wed'];
	return 0;
}

function change_alarmin_thu($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['thu'])) return 1;
	if($_REQUEST['thu']<0 || $_REQUEST['thu']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->thu = $_REQUEST['thu'];
	return 0;
}

function change_alarmin_fri($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['fri'])) return 1;
	if($_REQUEST['fri']<0 || $_REQUEST['fri']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->fri = $_REQUEST['fri'];
	return 0;
}

function change_alarmin_sat($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['sat'])) return 1;
	if($_REQUEST['sat']<0 || $_REQUEST['sat']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->week->sat = $_REQUEST['sat'];
	return 0;
}

function change_alarmin_starthour($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['shour'])) return 1;
	if($_REQUEST['shour']<0 || $_REQUEST['shour']>23) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->start_hour = $_REQUEST['shour'];
	return 0;
}

function change_alarmin_startmin($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['smin'])) return 1;
	if($_REQUEST['smin']<0 || $_REQUEST['smin']>59) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->start_min = $_REQUEST['smin'];
	return 0;
}

function change_alarmin_endhour($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['ehour'])) return 1;
	if($_REQUEST['ehour']<0 || $_REQUEST['ehour']>23) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->end_hour = $_REQUEST['ehour'];
	return 0;
}

function change_alarmin_endmin($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['emin'])) return 1;
	if($_REQUEST['emin']<0 || $_REQUEST['emin']>59) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->time_range->end_min = $_REQUEST['emin'];
	return 0;
}

function change_alarmin_output($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['output'])) return 1;
	if($_REQUEST['output']<0 || $_REQUEST['output']>$GLOBALS['system_caps']->relay_count) 
		return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->action->output = $_REQUEST['output'];
	return 0;
}

function change_alarmin_duration($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['duration'])) return 1;
	if($_REQUEST['duration']<0 || $_REQUEST['duration']>5) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->action->duration = $_REQUEST['duration'];
	return 0;
}

function change_alarmin_transfer($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['transfer'])) return 1;
	if($_REQUEST['transfer']<0 || $_REQUEST['transfer']>1) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->action->transfer = $_REQUEST['transfer'];
	return 0;
}

function change_alarmin_camaction($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['camaction'])) return 1;
	if($_REQUEST['camaction']<ACTION_NONE || $_REQUEST['camaction']>ACTION_GROUP) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction = $_REQUEST['camaction'];
	return 0;
}

function change_alarmin_camindex($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['actionindex'])) return 1;
	
	//if ($GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction== ACTION_NONE)				return 1;
	//else if ($GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction == ACTION_PRESET)		$max_index = MODEL_MAXPRESET($GLOBALS['std_conf']['model_num']);
	//else if ($GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction == ACTION_SCAN)		$max_index = MODEL_MAXSCAN($GLOBALS['std_conf']['model_num']);
	//else if ($GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction == ACTION_PATTERN)		$max_index = MODEL_MAXPATTERN($GLOBALS['std_conf']['model_num']);
	//else if ($GLOBALS['event_conf']->alarm_input_conf[$num]->action->camerafunction == ACTION_GROUP)		$max_index = MODEL_MAXGROUP($GLOBALS['std_conf']['model_num']);
		
	//if($_REQUEST['actionindex']<0 || $_REQUEST['actionindex']>$max_index) return -1;

	$GLOBALS['event_conf']->alarm_input_conf[$num]->action->functionindex = $_REQUEST['actionindex'];
	return 0;
}

function change_alarmin($alarm_num)
{
	if ($alarm_num >= $GLOBALS['system_caps']->sensor_count)	return -1;

	if (change_alarmin_device($alarm_num) < 0) return -1;
	if (change_alarmin_always($alarm_num) < 0) return -1;
	if (change_alarmin_sun($alarm_num) < 0) return -1;
	if (change_alarmin_mon($alarm_num) < 0) return -1;
	if (change_alarmin_tue($alarm_num) < 0) return -1;
	if (change_alarmin_wed($alarm_num) < 0) return -1;
	if (change_alarmin_thu($alarm_num) < 0) return -1;
	if (change_alarmin_fri($alarm_num) < 0) return -1;
	if (change_alarmin_sat($alarm_num) < 0) return -1;
	if (change_alarmin_starthour($alarm_num) < 0) return -1;
	if (change_alarmin_startmin($alarm_num) < 0) return -1;
	if (change_alarmin_endhour($alarm_num) < 0) return -1;
	if (change_alarmin_endmin($alarm_num) < 0) return -1;
	if (change_alarmin_output($alarm_num) < 0) return -1;
	if (change_alarmin_duration($alarm_num) < 0) return -1;
	if (change_alarmin_transfer($alarm_num) < 0) return -1;
	
	return 0;
}

//--- motion
function motion_view_post()
{
	for( $src=0; $src < MAX_MEDIA_SOURCE ; ++$src )
	{
		echo "[source".($src+1) ."]\r\n";
		for ($i = 0; $i < 4; $i++) {
			echo "enable".$i."=".$GLOBALS['event_conf']->motion_confs->conf[$src]->{'enable'.$i}."\r\n";
		}

		for ($i = 0; $i < 4; $i++) {
			echo "x".$i."=".$GLOBALS['event_conf']->motion_confs->conf[$src]->area[$i]->x."\r\n";
			echo "y".$i."=".$GLOBALS['event_conf']->motion_confs->conf[$src]->area[$i]->y."\r\n";
			echo "w".$i."=".$GLOBALS['event_conf']->motion_confs->conf[$src]->area[$i]->w."\r\n";
			echo "h".$i."=".$GLOBALS['event_conf']->motion_confs->conf[$src]->area[$i]->h."\r\n";
		}

		for ($i = 0; $i < 4; $i++) {
			$val = $GLOBALS['event_conf']->motion_confs->conf[$src]->{'sens'.$i};
			$val = $val & 0xff ; 
			echo "sens".$i."=".$val."\r\n";
		}
	}

/*	echo "enable="		.$GLOBALS['event_conf']->motion_conf->enable."\r\n";
	echo "sensitivity="	.$GLOBALS['event_conf']->motion_conf->sens."\r\n";
	echo "activation="	.$GLOBALS['event_conf']->motion_conf->always."\r\n";
	echo "sun="			.$GLOBALS['event_conf']->motion_conf->week->sun."\r\n";
	echo "mon="			.$GLOBALS['event_conf']->motion_conf->week->mon."\r\n";
	echo "tue="			.$GLOBALS['event_conf']->motion_conf->week->tue."\r\n";
	echo "wed="			.$GLOBALS['event_conf']->motion_conf->week->wed."\r\n";
	echo "thu="			.$GLOBALS['event_conf']->motion_conf->week->thu."\r\n";
	echo "fri="			.$GLOBALS['event_conf']->motion_conf->week->fri."\r\n";
	echo "sat="			.$GLOBALS['event_conf']->motion_conf->week->sat."\r\n";
	echo "shour="		.$GLOBALS['event_conf']->motion_conf->time_range->start_hour."\r\n";
	echo "smin="		.$GLOBALS['event_conf']->motion_conf->time_range->start_min."\r\n";
	echo "ehour="		.$GLOBALS['event_conf']->motion_conf->time_range->end_hour."\r\n";
	echo "emin="		.$GLOBALS['event_conf']->motion_conf->time_range->end_min."\r\n";
	
	
	if ($GLOBALS['system_caps']->relay_count > 0)
	{
		echo "output="		.$GLOBALS['event_conf']->motion_conf->action->output."\r\n";
		echo "duration="	.$GLOBALS['event_conf']->motion_conf->action->duration."\r\n";
	}
	echo "transfer="	.$GLOBALS['event_conf']->motion_conf->action->transfer."\r\n";	
*/

	if($GLOBALS['system_caps']->board_chipset == 'TI_DM36X')
	{
		/*
		0??? ????????? ???????????? ?????? ?????? Area??? ?????????
		
		1080P	: 20(FFFFF000) * 16
		720P	: 16(FFFF0000) *  9
		D1/4CIF	:  9(FF800000) *  6
		CIF		:  4(F0000000) *  3
		*/
		
		$valid_row = 18;
		$valid_col = 0xFFFFF000;
		
		if ($GLOBALS['channel_conf']->Channel[0]->Encoding == CODEC_H264)
		{
			if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 1920)
			{
				$valid_row = 16;
				$valid_col = 0xFFFFF000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 1280)
			{
				$valid_row = 9;
				$valid_col = 0xFFFF0000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 704 || $GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 720)
			{
				$valid_row = 6;
				$valid_col = 0xFF800000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 352 || $GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 360)
			{
				$valid_row = 3;
				$valid_col = 0xF0000000;
			}
		}

		for ($i=0; $i<18; $i++)
		{
			if ($i>=$valid_row)
			{
				echo "area" . ($i+1) . "=" . sprintf("0x%08X", "00000000") . "\r\n";
				continue;
			}
			$area_num = sprintf("setup_area%d", ($i+1));
			echo "area" . ($i+1) . "=" . sprintf("0x%08X", ($GLOBALS['event_conf']->motion_conf->motion_area[$area_num]) & $valid_col) . "\r\n";
		}
	}
	else if($GLOBALS['system_caps']->board_chipset == 'AMBA_A5S')
	{
	
	}

}

function change_motion_enable()
{
	for ($i = 0; $i < 4; $i++) {
		if (isset($_REQUEST['enable'.$i])) {
			$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->{'enable'.$i} = $_REQUEST['enable'.$i];
		}
	}

	return 0;
}

//<-- add _BY_LAUDS_120503
function change_motion_sensitivity()
{
	for ($i = 0; $i < 4; $i++) {
		if (!isset($_REQUEST['size'.$i])) $_REQUEST['size'.$i] = 0 ;
		if (isset($_REQUEST['sens'.$i]) && isset($_REQUEST['size'.$i])) {
			$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->{'sens'.$i} = 
				(($_REQUEST['size'.$i] & 0xff)<< 16) | ($_REQUEST['sens'.$i] & 0xff);
		}
	}
	return 0;
}

function isHex($hex)
{
    // Validation
    $hex = preg_replace('/^(0x|X)?/i', '', $hex);
    $hex = preg_replace('/[[:blank:]]/', '', $hex);

    if(empty($hex)) return false;
    if(!preg_match('/^[0-9A-F]*$/i', $hex)) return false;

    return true;
}

function change_motion_area()
{
	if($GLOBALS['system_caps']->board_chipset == 'TI_DM36X')
	{
		if ($GLOBALS['channel_conf']->Channel[0]->Encoding == CODEC_H264)
		{
			if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 1920)
			{
				$valid_row = 16;
				$valid_col = 0xFFFFF000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 1280)
			{
				$valid_row = 9;
				$valid_col = 0xFFFF0000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 704 || $GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 720)
			{
				$valid_row = 6;
				$valid_col = 0xFF800000;
			}
			else if ($GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 352 || $GLOBALS['channel_conf']->Channel[0]->Resolution->Width == 360)
			{
				$valid_row = 3;
				$valid_col = 0xF0000000;
			}
		}
		
		for ($i=0; $i<18; $i++)
		{
			if ($i>=$valid_row)	continue;
			
			$area_num = sprintf("area%d", ($i+1));
			if(!isset($_REQUEST[$area_num]))		continue;
			if(isHex($_REQUEST[$area_num])==false)	return -1;
			
			$input_val = hexdec($_REQUEST[$area_num]);
			if ($input_val < 0 || $input_val > $valid_col)	return -1;

			$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->motion_area[$area_num] = $input_val;
		}
	}
	//else if((trim($GLOBALS['system_caps']->board_chipset) == 'amba_a5s66')|| (trim($GLOBALS['system_caps']->board_chipset) == 'amba_s2lm55'))
	else
	{
		for ($i = 0; $i < 4; $i++) {
			if (isset($_REQUEST['x'.$i]) && isset($_REQUEST['y'.$i]) && isset($_REQUEST['w'.$i]) && isset($_REQUEST['h'.$i])) {
				$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->area[$i]->x = $_REQUEST['x'.$i];
				$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->area[$i]->y = $_REQUEST['y'.$i];
				$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->area[$i]->w = $_REQUEST['w'.$i];
				$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->area[$i]->h = $_REQUEST['h'.$i];
			}
		}
	
	}
	return 0;
}
//--> add _BY_LAUDS_120503

function change_motion_always()
{
	if(!isset($_REQUEST['activation'])) return 1;
	if($_REQUEST['activation']<0 || $_REQUEST['activation']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->always = $_REQUEST['activation'];
	return 0;
}

function change_motion_sun()
{
	if(!isset($_REQUEST['sun'])) return 1;
	if($_REQUEST['sun']<0 || $_REQUEST['sun']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->sun = $_REQUEST['sun'];
	return 0;
}

function change_motion_mon()
{
	if(!isset($_REQUEST['mon'])) return 1;
	if($_REQUEST['mon']<0 || $_REQUEST['mon']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->mon = $_REQUEST['mon'];
	return 0;
}

function change_motion_tue()
{
	if(!isset($_REQUEST['tue'])) return 1;
	if($_REQUEST['tue']<0 || $_REQUEST['tue']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->tue = $_REQUEST['tue'];
	return 0;
}

function change_motion_wed()
{
	if(!isset($_REQUEST['wed'])) return 1;
	if($_REQUEST['wed']<0 || $_REQUEST['wed']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->wed = $_REQUEST['wed'];
	return 0;
}

function change_motion_thu()
{
	if(!isset($_REQUEST['thu'])) return 1;
	if($_REQUEST['thu']<0 || $_REQUEST['thu']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->thu = $_REQUEST['thu'];
	return 0;
}

function change_motion_fri()
{
	if(!isset($_REQUEST['fri'])) return 1;
	if($_REQUEST['fri']<0 || $_REQUEST['fri']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->fri = $_REQUEST['fri'];
	return 0;
}

function change_motion_sat()
{
	if(!isset($_REQUEST['sat'])) return 1;
	if($_REQUEST['sat']<0 || $_REQUEST['sat']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->week->sat = $_REQUEST['sat'];
	return 0;
}

function change_motion_starthour()
{
	if(!isset($_REQUEST['shour'])) return 1;
	if($_REQUEST['shour']<0 || $_REQUEST['shour']>23) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->time_range->start_hour = $_REQUEST['shour'];
	return 0;
}

function change_motion_startmin()
{
	if(!isset($_REQUEST['smin'])) return 1;
	if($_REQUEST['smin']<0 || $_REQUEST['smin']>59) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->time_range->start_min = $_REQUEST['smin'];
	return 0;
}

function change_motion_endhour()
{
	if(!isset($_REQUEST['ehour'])) return 1;
	if($_REQUEST['ehour']<0 || $_REQUEST['ehour']>23) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->time_range->end_hour = $_REQUEST['ehour'];
	return 0;
}

function change_motion_endmin()
{
	if(!isset($_REQUEST['emin'])) return 1;
	if($_REQUEST['emin']<0 || $_REQUEST['emin']>59) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->time_range->end_min = $_REQUEST['emin'];
	return 0;
}

function change_motion_alarmout()
{
	if(!isset($_REQUEST['output'])) return 1;
	if($_REQUEST['output']<0 || $_REQUEST['output']>MODEL_RELAYOUT($GLOBALS['std_conf']['model_num'])) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->action->output = $_REQUEST['output'];
	return 0;
}

function change_motion_duration()
{
	if(!isset($_REQUEST['duration'])) return 1;
	if($_REQUEST['duration']<0 || $_REQUEST['duration']>5) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->action->duration = $_REQUEST['duration'];
	return 0;
}

function change_motion_transfer()
{
	if(!isset($_REQUEST['transfer'])) return 1;
	if($_REQUEST['transfer']<0 || $_REQUEST['transfer']>1) return -1;

	$GLOBALS['event_conf']->motion_confs->conf[$GLOBALS['src']]->action->transfer = $_REQUEST['transfer'];
	return 0;
}

function change_motion()
{
	if (change_motion_enable() < 0) 		return -1;
// <-- add _BY_LAUDS_120503
	if (change_motion_sensitivity() < 0)	return -1;
	if (change_motion_area() < 0)			return -1;
// --> add _BY_LAUDS_120503
	if (change_motion_always() < 0) 		return -1;
	if (change_motion_sun() < 0) 			return -1;
	if (change_motion_mon() < 0) 			return -1;
	if (change_motion_tue() < 0) 			return -1;
	if (change_motion_wed() < 0) 			return -1;
	if (change_motion_thu() < 0) 			return -1;
	if (change_motion_fri() < 0) 			return -1;
	if (change_motion_sat() < 0) 			return -1;
	if (change_motion_starthour() < 0)		return -1;
	if (change_motion_startmin() < 0) 		return -1;
	if (change_motion_endhour() < 0) 		return -1;
	if (change_motion_endmin() < 0) 		return -1;
	if (change_motion_alarmout() < 0) 		return -1;
	if (change_motion_duration() < 0) 		return -1;
	if (change_motion_transfer() < 0) 		return -1;

	return 0;
}


//--- temperature
function temperature_view_post()
{
	for( $src=0; $src < MAX_MEDIA_SOURCE ; ++$src )
	{
		echo "[source".($src+1) ."]\r\n";
		for ($i = 0; $i < 8; $i++) {
			echo "enable".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'enable'.$i}."\r\n";
		}

		for ($i = 0; $i < 8; $i++) {
			echo "x".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->area[$i]->x."\r\n";
			echo "y".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->area[$i]->y."\r\n";
			echo "w".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->area[$i]->w."\r\n";
			echo "h".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->area[$i]->h."\r\n";
		}

		for ($i = 0; $i < 8; $i++) {
			$val = $GLOBALS['event_conf']->temperature_confs->conf[$src]->{'temperature'.$i};
			echo "temperature".$i."=".$val."\r\n";
		}
		for ($i = 0; $i < 8; $i++) {
			$val = $GLOBALS['event_conf']->temperature_confs->conf[$src]->{'filteringtime'.$i};
			echo "filteringtime".$i."=".$val."\r\n";
		}

		for ($i = 0; $i < 8; $i++) {
			echo "tolerance".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'tolerance'.$i}."\r\n";
		}
		for ($i = 0; $i < 8; $i++) {
			echo "rule".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'rule'.$i}."\r\n";
		}		
		for ($i = 0; $i < 8; $i++) {
			echo "emissivitytype".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'emissivitytype'.$i}."\r\n";
			echo "emissivity".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'emissivity'.$i}."\r\n";
			echo "measurement".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'measurement'.$i}."\r\n";
			echo "slopegradient".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'slopegradient'.$i}."\r\n";
			echo "osd".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'osd'.$i}."\r\n";
			echo "max_temp".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'max_temp'.$i}."\r\n";
			echo "min_temp".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'min_temp'.$i}."\r\n";
			echo "avg_temp".$i."=".$GLOBALS['event_conf']->temperature_confs->conf[$src]->{'avg_temp'.$i}."\r\n";
		}
		echo "convert_md =".$GLOBALS['event_conf']->temperature_confs->conf[$src]->convert_md."\r\n";

	}
}

function change_temperature_enable()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['enable'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'enable'.$i} = $_REQUEST['enable'.$i];
		}
	}

	return 0;
}


function change_temperature_rule()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['rule'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'rule'.$i} = $_REQUEST['rule'.$i];
		}
	}

	return 0;
}


function change_temperature_tolerance()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['tolerance'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'tolerance'.$i} = $_REQUEST['tolerance'.$i];
		}
	}

	return 0;
}


function change_temperature_filteringtime()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['filteringtime'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'filteringtime'.$i} = ($_REQUEST['filteringtime'.$i]);
		}
	}

	return 0;
}

function change_temperature_temperature()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['temperature'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'temperature'.$i} = ($_REQUEST['temperature'.$i] * 100);
		}
	}

	return 0;
}

function change_temperature_area()
{
	
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['x'.$i]) && isset($_REQUEST['y'.$i]) && isset($_REQUEST['w'.$i]) && isset($_REQUEST['h'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->area[$i]->x = $_REQUEST['x'.$i];
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->area[$i]->y = $_REQUEST['y'.$i];
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->area[$i]->w = $_REQUEST['w'.$i];
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->area[$i]->h = $_REQUEST['h'.$i];
		}
	}
	
	return 0;
}
//--> add _BY_LAUDS_120503

function change_temperature_emissivitytype()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['emissivitytype'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'emissivitytype'.$i} = ($_REQUEST['emissivitytype'.$i]);
		}
	}

	return 0;
}

function change_temperature_emissivity()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['emissivity'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'emissivity'.$i} = ($_REQUEST['emissivity'.$i]);
		}
	}

	return 0;
}

function change_temperature_measurement()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['measurement'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'measurement'.$i} = ($_REQUEST['measurement'.$i]);
		}
	}

	return 0;
}

function change_temperature_slopegradient()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['slopegradient'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'slopegradient'.$i} = ($_REQUEST['slopegradient'.$i] * 100);
		}
	}

	return 0;
}

function change_temperature_osd()
{
	for ($i = 0; $i < 8; $i++) {
		if (isset($_REQUEST['osd'.$i])) {
			$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->{'osd'.$i} = $_REQUEST['osd'.$i];
		}
	}

	return 0;
}

function change_temperature_convert_md()
{
	if(!isset($_REQUEST['convert_md'])) return 1;
	if($_REQUEST['convert_md']<0 || $_REQUEST['convert_md']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->convert_md = $_REQUEST['convert_md'];
	return 0;
}

function change_temperature_always()
{
	if(!isset($_REQUEST['activation'])) return 1;
	if($_REQUEST['activation']<0 || $_REQUEST['activation']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->always = $_REQUEST['activation'];
	return 0;
}

function change_temperature_sun()
{
	if(!isset($_REQUEST['sun'])) return 1;
	if($_REQUEST['sun']<0 || $_REQUEST['sun']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->sun = $_REQUEST['sun'];
	return 0;
}

function change_temperature_mon()
{
	if(!isset($_REQUEST['mon'])) return 1;
	if($_REQUEST['mon']<0 || $_REQUEST['mon']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->mon = $_REQUEST['mon'];
	return 0;
}

function change_temperature_tue()
{
	if(!isset($_REQUEST['tue'])) return 1;
	if($_REQUEST['tue']<0 || $_REQUEST['tue']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->tue = $_REQUEST['tue'];
	return 0;
}

function change_temperature_wed()
{
	if(!isset($_REQUEST['wed'])) return 1;
	if($_REQUEST['wed']<0 || $_REQUEST['wed']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->wed = $_REQUEST['wed'];
	return 0;
}

function change_temperature_thu()
{
	if(!isset($_REQUEST['thu'])) return 1;
	if($_REQUEST['thu']<0 || $_REQUEST['thu']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->thu = $_REQUEST['thu'];
	return 0;
}

function change_temperature_fri()
{
	if(!isset($_REQUEST['fri'])) return 1;
	if($_REQUEST['fri']<0 || $_REQUEST['fri']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->fri = $_REQUEST['fri'];
	return 0;
}

function change_temperature_sat()
{
	if(!isset($_REQUEST['sat'])) return 1;
	if($_REQUEST['sat']<0 || $_REQUEST['sat']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->week->sat = $_REQUEST['sat'];
	return 0;
}

function change_temperature_starthour()
{
	if(!isset($_REQUEST['shour'])) return 1;
	if($_REQUEST['shour']<0 || $_REQUEST['shour']>23) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->time_range->start_hour = $_REQUEST['shour'];
	return 0;
}

function change_temperature_startmin()
{
	if(!isset($_REQUEST['smin'])) return 1;
	if($_REQUEST['smin']<0 || $_REQUEST['smin']>59) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->time_range->start_min = $_REQUEST['smin'];
	return 0;
}

function change_temperature_endhour()
{
	if(!isset($_REQUEST['ehour'])) return 1;
	if($_REQUEST['ehour']<0 || $_REQUEST['ehour']>23) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->time_range->end_hour = $_REQUEST['ehour'];
	return 0;
}

function change_temperature_endmin()
{
	if(!isset($_REQUEST['emin'])) return 1;
	if($_REQUEST['emin']<0 || $_REQUEST['emin']>59) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->time_range->end_min = $_REQUEST['emin'];
	return 0;
}

function change_temperature_alarmout()
{
	if(!isset($_REQUEST['output'])) return 1;
	if($_REQUEST['output']<0 || $_REQUEST['output']>MODEL_RELAYOUT($GLOBALS['std_conf']['model_num'])) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->action->output = $_REQUEST['output'];
	return 0;
}

function change_temperature_duration()
{
	if(!isset($_REQUEST['duration'])) return 1;
	if($_REQUEST['duration']<0 || $_REQUEST['duration']>5) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->action->duration = $_REQUEST['duration'];
	return 0;
}

function change_temperature_transfer()
{
	if(!isset($_REQUEST['transfer'])) return 1;
	if($_REQUEST['transfer']<0 || $_REQUEST['transfer']>1) return -1;

	$GLOBALS['event_conf']->temperature_confs->conf[$GLOBALS['src']]->action->transfer = $_REQUEST['transfer'];
	return 0;
}

function change_temperature()
{
	if (change_temperature_enable() < 0) 		return -1;
	if (change_temperature_rule() < 0)			return -1;
	if (change_temperature_tolerance() < 0)		return -1;
	if (change_temperature_filteringtime() < 0)	return -1;
	if (change_temperature_temperature() < 0)	return -1;
	if (change_temperature_area() < 0)			return -1;
	if (change_temperature_convert_md() < 0)	return -1;
	if (change_temperature_always() < 0) 		return -1;
	if (change_temperature_sun() < 0) 			return -1;
	if (change_temperature_mon() < 0) 			return -1;
	if (change_temperature_tue() < 0) 			return -1;
	if (change_temperature_wed() < 0) 			return -1;
	if (change_temperature_thu() < 0) 			return -1;
	if (change_temperature_fri() < 0) 			return -1;
	if (change_temperature_sat() < 0) 			return -1;
	if (change_temperature_starthour() < 0)		return -1;
	if (change_temperature_startmin() < 0) 		return -1;
	if (change_temperature_endhour() < 0) 		return -1;
	if (change_temperature_endmin() < 0) 		return -1;
	if (change_temperature_alarmout() < 0) 		return -1;
	if (change_temperature_duration() < 0) 		return -1;
	if (change_temperature_transfer() < 0) 		return -1;
	if (change_temperature_emissivitytype() < 0) 		return -1;
	if (change_temperature_emissivity() < 0) 		return -1;
	if (change_temperature_measurement() < 0) 		return -1;
	if (change_temperature_slopegradient() < 0) 		return -1;
	if (change_temperature_osd() < 0) 		return -1;

	return 0;
}

//--- schedule
function schedule_view_post()
{
	echo "enable="		.$GLOBALS['event_conf']->schedule_conf->enable."\r\n";
	echo "interval="	.$GLOBALS['event_conf']->schedule_conf->interval_value."\r\n";
/*	echo "unit="		.$GLOBALS['event_conf']->schedule_conf->interval_unit."\r\n";
	echo "activation="	.$GLOBALS['event_conf']->schedule_conf->always."\r\n";
	echo "sun="			.$GLOBALS['event_conf']->schedule_conf->week->sun."\r\n";
	echo "mon="			.$GLOBALS['event_conf']->schedule_conf->week->mon."\r\n";
	echo "tue="			.$GLOBALS['event_conf']->schedule_conf->week->tue."\r\n";
	echo "wed="			.$GLOBALS['event_conf']->schedule_conf->week->wed."\r\n";
	echo "thu="			.$GLOBALS['event_conf']->schedule_conf->week->thu."\r\n";
	echo "fri="			.$GLOBALS['event_conf']->schedule_conf->week->fri."\r\n";
	echo "sat="			.$GLOBALS['event_conf']->schedule_conf->week->sat."\r\n";
	echo "shour="		.$GLOBALS['event_conf']->schedule_conf->time_range->start_hour."\r\n";
	echo "smin="		.$GLOBALS['event_conf']->schedule_conf->time_range->start_min."\r\n";
	echo "ehour="		.$GLOBALS['event_conf']->schedule_conf->time_range->end_hour."\r\n";
	echo "emin="		.$GLOBALS['event_conf']->schedule_conf->time_range->end_min."\r\n";*/
}

function change_sched_enabled()
{
	if (!isset($_REQUEST['enable'])) return 1;
	if ($_REQUEST['enable'] < 0 || $_REQUEST['enable'] > 1) return -1;
	
	$GLOBALS['event_conf']->schedule_conf->enable = $_REQUEST['enable'];
	return 0;
}

function change_sched_interval()
{
	if ( !isset($_REQUEST['interval'])) return 1;

	$GLOBALS['event_conf']->schedule_conf->interval_value = $_REQUEST['interval'];
	return 0;
}

function change_sched_unit()
{
	if(!isset($_REQUEST['unit'])) return 1;
	if($_REQUEST['unit'] < 0 || $_REQUEST['unit'] > 1) return -1;

	$GLOBALS['event_conf']->schedule_conf->interval_unit = $_REQUEST['unit'];
	return 0;
}

function change_sched_always()
{
	if(!isset($_REQUEST['activation'])) return 1;
	if($_REQUEST['activation'] < 0 || $_REQUEST['activation'] > 1) return -1;

	$GLOBALS['event_conf']->schedule_conf->always = $_REQUEST['activation'];
	return 0;
}

function change_sched_sun()
{
	if(!isset($_REQUEST['sun'])) return 1;
	if($_REQUEST['sun']<0 || $_REQUEST['sun']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->sun = $_REQUEST['sun'];
	return 0;
}

function change_sched_mon()
{
	if(!isset($_REQUEST['mon'])) return 1;
	if($_REQUEST['mon']<0 || $_REQUEST['mon']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->mon = $_REQUEST['mon'];
	return 0;
}

function change_sched_tue()
{
	if(!isset($_REQUEST['tue'])) return 1;
	if($_REQUEST['tue']<0 || $_REQUEST['tue']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->tue = $_REQUEST['tue'];
	return 0;
}

function change_sched_wed()
{
	if(!isset($_REQUEST['wed'])) return 1;
	if($_REQUEST['wed']<0 || $_REQUEST['wed']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->wed = $_REQUEST['wed'];
	return 0;
}

function change_sched_thu()
{
	if(!isset($_REQUEST['thu'])) return 1;
	if($_REQUEST['thu']<0 || $_REQUEST['thu']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->thu = $_REQUEST['thu'];
	return 0;
}

function change_sched_fri()
{
	if(!isset($_REQUEST['fri'])) return 1;
	if($_REQUEST['fri']<0 || $_REQUEST['fri']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->fri = $_REQUEST['fri'];
	return 0;
}

function change_sched_sat()
{
	if(!isset($_REQUEST['sat'])) return 1;
	if($_REQUEST['sat']<0 || $_REQUEST['sat']>1) return -1;

	$GLOBALS['event_conf']->schedule_conf->week->sat = $_REQUEST['sat'];
	return 0;
}

function change_sched_starthour()
{
	if(!isset($_REQUEST['shour'])) return 1;
	if($_REQUEST['shour']<0 || $_REQUEST['shour']>23) return -1;

	$GLOBALS['event_conf']->schedule_conf->time_range->start_hour = $_REQUEST['shour'];
	return 0;
}

function change_sched_startmin()
{
	if(!isset($_REQUEST['smin'])) return 1;
	if($_REQUEST['smin']<0 || $_REQUEST['smin']>59) return -1;

	$GLOBALS['event_conf']->schedule_conf->time_range->start_min = $_REQUEST['smin'];
	return 0;
}

function change_sched_endhour()
{
	if(!isset($_REQUEST['ehour'])) return 1;
	if($_REQUEST['ehour']<0 || $_REQUEST['ehour']>23) return -1;

	$GLOBALS['event_conf']->schedule_conf->time_range->end_hour = $_REQUEST['ehour'];
	return 0;
}

function change_sched_endmin()
{
	if(!isset($_REQUEST['emin'])) return 1;
	if($_REQUEST['emin']<0 || $_REQUEST['emin']>59) return -1;

	$GLOBALS['event_conf']->schedule_conf->time_range->end_min = $_REQUEST['emin'];
	return 0;
}

function change_schedule()
{
	if (change_sched_enabled() < 0) return -1;
	if (change_sched_interval() < 0) return -1;
	if (change_sched_unit() < 0) return -1;
	if (change_sched_always() < 0) return -1;
	if (change_sched_sun() < 0) return -1;
	if (change_sched_mon() < 0) return -1;
	if (change_sched_tue() < 0) return -1;
	if (change_sched_wed() < 0) return -1;
	if (change_sched_thu() < 0) return -1;
	if (change_sched_fri() < 0) return -1;
	if (change_sched_sat() < 0) return -1;
	if (change_sched_starthour() < 0) return -1;
	if (change_sched_startmin() < 0) return -1;
	if (change_sched_endhour() < 0) return -1;
	if (change_sched_endmin() < 0) return -1;
	
	return 0;
}

//-- tracking
function tracking_view_post()
{
	echo "sensitivity="			.$GLOBALS['tracking_conf']['sensitivity']."\r\n";
	echo "track_all="			.$GLOBALS['tracking_conf']['track_all']."\r\n";
	echo "pan_min="				.$GLOBALS['tracking_conf']['pan_min']."\r\n";
	echo "pan_max="				.$GLOBALS['tracking_conf']['pan_max']."\r\n";
	echo "tilt_min="			.$GLOBALS['tracking_conf']['tilt_min']."\r\n";
	echo "tilt_max="			.$GLOBALS['tracking_conf']['tilt_max']."\r\n";
	echo "timeout_to_zoomout="	.$GLOBALS['tracking_conf']['timeout_to_zoomout']."\r\n";
	echo "timeout_to_home="		.$GLOBALS['tracking_conf']['timeout_to_home']."\r\n";
	echo "osc_magnitude="		.$GLOBALS['tracking_conf']['osc_magnitude']."\r\n";
	echo "osc_count="			.$GLOBALS['tracking_conf']['osc_count']."\r\n";
	echo "obj_size_to_start="	.$GLOBALS['tracking_conf']['obj_size_to_start']."\r\n";
	echo "obj_size_to_zoomin="	.$GLOBALS['tracking_conf']['obj_size_to_zoomin']."\r\n";
	echo "obj_size_to_zoomout="	.$GLOBALS['tracking_conf']['obj_size_to_zoomout']."\r\n";
}

function change_tracking_sens()
{
	if (!isset($_REQUEST['sensitivity'])) return 1;
	if ($_REQUEST['sensitivity'] < 1 || $_REQUEST['sensitivity'] > 5) return -1;
	$GLOBALS['tracking_conf']['sensitivity'] = $_REQUEST['sensitivity'];
	shm_update_c2(OFFSET_EXTERN+20, $_REQUEST['sensitivity']);
	return 0;
}
function change_tracking_track_all()
{
	if (!isset($_REQUEST['track_all'])) return 1;
	if ($_REQUEST['track_all'] < 0 || $_REQUEST['track_all'] > 1) return -1;
	$GLOBALS['tracking_conf']['track_all'] = $_REQUEST['track_all'];
	shm_update_i(OFFSET_EXTERN,     $_REQUEST['track_all']);
	return 0;
}
function change_tracking_pan_min()
{
	if (!isset($_REQUEST['pan_min'])) return 1;
	if ($_REQUEST['pan_min'] < 0 || $_REQUEST['pan_min'] > 360) return -1;
	$GLOBALS['tracking_conf']['pan_min'] = $_REQUEST['pan_min'];
	shm_update_i(OFFSET_EXTERN+4,   $_REQUEST['pan_min']);
	return 0;
}
function change_tracking_pan_max()
{
	if (!isset($_REQUEST['pan_max'])) return 1;
	if ($_REQUEST['pan_max'] < 0 || $_REQUEST['pan_max'] > 360) return -1;
	$GLOBALS['tracking_conf']['pan_max'] = $_REQUEST['pan_max'];
	shm_update_i(OFFSET_EXTERN+8,   $_REQUEST['pan_max']);
	return 0;
}
function change_tracking_tilt_min()
{
	if (!isset($_REQUEST['tilt_min'])) return 1;
	if ($_REQUEST['tilt_min'] < 0 || $_REQUEST['tilt_min'] > 90) return -1;
	$GLOBALS['tracking_conf']['tilt_min'] = $_REQUEST['tilt_min'];
	shm_update_i(OFFSET_EXTERN+12,  $_REQUEST['tilt_min']);
	return 0;
}
function change_tracking_tilt_max()
{
	if (!isset($_REQUEST['tilt_max'])) return 1;
	if ($_REQUEST['tilt_max'] < 0 || $_REQUEST['tilt_max'] > 90) return -1;
	$GLOBALS['tracking_conf']['tilt_max'] = $_REQUEST['tilt_max'];
	shm_update_i(OFFSET_EXTERN+16,  $_REQUEST['tilt_max']);
	return 0;
}
function change_tracking_timeout_to_zoomout()
{
	if (!isset($_REQUEST['timeout_to_zoomout'])) return 1;
	if ($_REQUEST['timeout_to_zoomout'] < 1 || $_REQUEST['timeout_to_zoomout'] > 255) return -1;
	$GLOBALS['tracking_conf']['timeout_to_zoomout'] =$_REQUEST['timeout_to_zoomout'];
	shm_update_c2(OFFSET_EXTERN+21, $_REQUEST['timeout_to_zoomout']);
	
	return 0;
}
function change_Tracking_timeout_to_home()
{
	if (!isset($_REQUEST['timeout_to_home'])) return 1;
	if ($_REQUEST['timeout_to_home'] < 1 || $_REQUEST['timeout_to_home'] > 255) return -1;
	$GLOBALS['tracking_conf']['timeout_to_home'] =$_REQUEST['timeout_to_home'];
	shm_update_c2(OFFSET_EXTERN+22, $_REQUEST['timeout_to_home']);
	
	return 0;
}
function change_tracking_osc_magnitude()
{
	if (!isset($_REQUEST['osc_magnitude'])) return 1;
	if ($_REQUEST['osc_magnitude'] < 1 || $_REQUEST['osc_magnitude'] > 100) return -1;
	$GLOBALS['tracking_conf']['osc_magnitude'] =$_REQUEST['osc_magnitude'];
	shm_update_c2(OFFSET_EXTERN+23, $_REQUEST['osc_magnitude']);
	
	return 0;
}
function change_tracking_osc_count()
{
	if (!isset($_REQUEST['osc_count'])) return 1;
	if ($_REQUEST['osc_count'] < 1 || $_REQUEST['osc_count'] > 255) return -1;
	$GLOBALS['tracking_conf']['osc_count'] =$_REQUEST['osc_count'];
	shm_update_c2(OFFSET_EXTERN+24, $_REQUEST['osc_count']);
	
	return 0;
}
function change_tracking_objsize_to_start()
{
	if (!isset($_REQUEST['obj_size_to_start'])) return 1;
	if ($_REQUEST['obj_size_to_start'] < 1 || $_REQUEST['obj_size_to_start'] > 100) return -1;
	$GLOBALS['tracking_conf']['obj_size_to_start'] =$_REQUEST['obj_size_to_start'];
	shm_update_c2(OFFSET_EXTERN+25, $_REQUEST['obj_size_to_start']);
	
	return 0;
}
function change_tracking_objsize_to_zoomin()
{
	if (!isset($_REQUEST['obj_size_to_zoomin'])) return 1;
	if ($_REQUEST['obj_size_to_zoomin'] < 1 || $_REQUEST['obj_size_to_zoomin'] > 100) return -1;
	$GLOBALS['tracking_conf']['obj_size_to_zoomin'] =$_REQUEST['obj_size_to_zoomin'];
	shm_update_c2(OFFSET_EXTERN+26, $_REQUEST['obj_size_to_zoomin']);
	
	return 0;
}
function change_Tracking_objsize_to_zoomout()
{
	if (!isset($_REQUEST['obj_size_to_zoomout'])) return 1;
	if ($_REQUEST['obj_size_to_zoomout'] < 1 || $_REQUEST['obj_size_to_zoomout'] > 100) return -1;
	$GLOBALS['tracking_conf']['obj_size_to_zoomout'] =$_REQUEST['obj_size_to_zoomout'];
	shm_update_c2(OFFSET_EXTERN+27, $_REQUEST['obj_size_to_zoomout']);
	
	return 0;
}

function change_tracking()
{
	if (change_tracking_sens() < 0) return -1;
	if (change_tracking_track_all() < 0) return -1;
	if (change_tracking_pan_max() < 0) return -1;
	if (change_tracking_pan_min() < 0) return -1;
	if (change_tracking_tilt_max() < 0) return -1;
	if (change_tracking_tilt_min() < 0) return -1;
	if (change_tracking_timeout_to_zoomout() < 0) return -1;
	if (change_Tracking_timeout_to_home() < 0) return -1;
	if (change_tracking_osc_magnitude() < 0) return -1;
	if (change_tracking_osc_count() < 0) return -1;
	if (change_tracking_objsize_to_start() < 0) return -1;
	if (change_tracking_objsize_to_zoomin() < 0) return -1;
	if (change_Tracking_objsize_to_zoomout() < 0) return -1;
	
	return 0;
}


//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
$src = 0;
if( isset( $_REQUEST['source'] ) ) {
	$val = $_REQUEST['source'];
	if( $val >= 0 && $val <= $GLOBALS['system_caps']->video_in )
		$src = $val;
}
if ( isset($_REQUEST['submenu']) )
{
if ( $_REQUEST['submenu'] == 'alarmin1' || $_REQUEST['submenu'] == 'alarmin2' )
{
	if ( $_REQUEST['submenu'] == 'alarmin1' )		$alarm_num = 0;
	else if ( $_REQUEST['submenu'] == 'alarmin2' )	$alarm_num = 1;
	
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_event_alarm_input' . ($alarm_num+1).'.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_alarmin($alarm_num);
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'motion' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_event_motion_detection.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_motion();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'schedule' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_event_schedule.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_schedule();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			show_post_ok();
		}
		else
		{
			show_post_ng();
		}
	}
	exit;
}
else if ( $_REQUEST['submenu'] == 'tracking' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_event_motion_tracking.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_tracking();
		
	}
	exit;
}
}
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if ( isset($_REQUEST['msubmenu']) )
{
if ( $_REQUEST['msubmenu'] == 'alarmin1' || $_REQUEST['msubmenu'] == 'alarmin2' )
{
	if ($GLOBALS['system_caps']->sensor_count == 0)
	{
		show_post_ng();
		exit;
	}
	
	if ( $_REQUEST['msubmenu'] == 'alarmin1' )		$alarm_num = 0;
	else if ( $_REQUEST['msubmenu'] == 'alarmin2' )	$alarm_num = 1;

	if ( $_REQUEST['action'] == 'view' )
	{
		alarmin_view_post($alarm_num);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_alarmin($alarm_num) == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
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
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'motion' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		motion_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_motion() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
                if($ipc_sock->dataInfo['ErrorCode']['value'] == 0)
                    echo "msg_nothing_changed\r\n";
			}
		}
		else
			show_post_ng();
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'temperature_detect' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		temperature_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_temperature() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();
			}
			else
			{
				show_post_ng();
                if($ipc_sock->dataInfo['ErrorCode']['value'] == 0)
                    echo "msg_nothing_changed\r\n";
			}
		}
		else
			show_post_ng();
	}
	else
		show_post_ng();
	
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'schedule' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		schedule_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_schedule() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
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
	}
	else
		show_post_ng();
		
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'tracking' )
{
	show_post_ng();
	exit;
}

show_post_ng();
}
?>
