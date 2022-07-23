<?
require('../_define.inc');
require('../class/socket.class');
require('../class/trigger.class');
require('../class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$triggers_conf= new CTriggersConfiguration($shm_id);
$action_rules 	= $triggers_conf->action_rules;
$event_rules 	= $triggers_conf->event_rules;
$system_caps = new CCapability($shm_id);
$get_oem = $system_caps->getOEM();

function change_sched_always($index) 
{
	if(!isset($_REQUEST['always'])) return 1;
	if($_REQUEST['always'] < 0 || $_REQUEST['always'] > 1) return -1;
	$GLOBALS['event_rules']->event[$index]->schedule->always = $_REQUEST['always'];
	return 0;
}
function change_sched_sun($index) 
{
	if(!isset($_REQUEST['sun'])) return 1;
	if($_REQUEST['sun']<0 || $_REQUEST['sun']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->sun = $_REQUEST['sun'];
	return 0;
}
function change_sched_mon($index)
{
	if(!isset($_REQUEST['mon'])) return 1;
	if($_REQUEST['mon']<0 || $_REQUEST['mon']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->mon = $_REQUEST['mon'];
	return 0;
}
function change_sched_tue($index) 
{
	if(!isset($_REQUEST['tue'])) return 1;
	if($_REQUEST['tue']<0 || $_REQUEST['tue']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->tue = $_REQUEST['tue'];
	return 0;
}
function change_sched_wed($index) 
{
	if(!isset($_REQUEST['wed'])) return 1;
	if($_REQUEST['wed']<0 || $_REQUEST['wed']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->wed = $_REQUEST['wed'];
	return 0;
}
function change_sched_thu($index) 
{
	if(!isset($_REQUEST['thu'])) return 1;
	if($_REQUEST['thu']<0 || $_REQUEST['thu']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->thu = $_REQUEST['thu'];
	return 0;
}
function change_sched_fri($index) 
{
	if(!isset($_REQUEST['fri'])) return 1;
	if($_REQUEST['fri']<0 || $_REQUEST['fri']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->fri = $_REQUEST['fri'];
	return 0;
}
function change_sched_sat($index)
{
	if(!isset($_REQUEST['sat'])) return 1;
	if($_REQUEST['sat']<0 || $_REQUEST['sat']>1) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->week->sat = $_REQUEST['sat'];
	return 0;
}
function change_sched_starthour($index)
{
	if(!isset($_REQUEST['shour'])) return 1;
	if($_REQUEST['shour']<0 || $_REQUEST['shour']>23) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->time_range->start_hour = $_REQUEST['shour'];
	return 0;
}
function change_sched_startmin($index) 
{
	if(!isset($_REQUEST['smin'])) return 1;
	if($_REQUEST['smin']<0 || $_REQUEST['smin']>59) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->time_range->start_min = $_REQUEST['smin'];
	return 0;
}
function change_sched_endhour($index)
{
	if(!isset($_REQUEST['ehour'])) return 1;
	if($_REQUEST['ehour']<0 || $_REQUEST['ehour']>23) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->time_range->end_hour = $_REQUEST['ehour'];
	return 0;
}
function change_sched_endmin($index)
{
	if(!isset($_REQUEST['emin'])) return 1;
	if($_REQUEST['emin']<0 || $_REQUEST['emin']>59) return -1;

	$GLOBALS['event_rules']->event[$index]->schedule->time_range->end_min = $_REQUEST['emin'];
	return 0;
}
function change_schedule($i)
{
	if (change_sched_always($i) < 0) return -1;
	if (change_sched_sun($i) < 0) return -1;
	if (change_sched_mon($i) < 0) return -1;
	if (change_sched_tue($i) < 0) return -1;
	if (change_sched_wed($i) < 0) return -1;
	if (change_sched_thu($i) < 0) return -1;
	if (change_sched_fri($i) < 0) return -1;
	if (change_sched_sat($i) < 0) return -1;
	if (change_sched_starthour($i) < 0) return -1;
	if (change_sched_startmin($i) < 0) return -1;
	if (change_sched_endhour($i) < 0) return -1;
	if (change_sched_endmin($i) < 0) return -1;
	
	return 0;
}

function event_rules_get_json() {
	$data=array();
	$used = 0;
	for($index = 0 ; $index < MAX_NUM_TRIGGER; ++$index) {
		$target = $GLOBALS['event_rules']->event[$index];

		if($target->id == 0) continue;

		$data[$used]["id"]        = $target->id;
		$data[$used]["enabled"]   = $target->enabled;
		$data[$used]["name"]      = trim($target->name);
		$data[$used]["action_id"] = $target->action_id;
		$data[$used]["always"]    = $target->schedule->always;
		$data[$used]["sun"]       = $target->schedule->week->sun;
		$data[$used]["mon"]       = $target->schedule->week->mon;
		$data[$used]["tue"]       = $target->schedule->week->tue;
		$data[$used]["wed"]       = $target->schedule->week->wed;
		$data[$used]["thu"]       = $target->schedule->week->thu;
		$data[$used]["fri"]       = $target->schedule->week->fri;
		$data[$used]["sat"]       = $target->schedule->week->sat;
		$data[$used]["shour"]     = $target->schedule->time_range->start_hour;
		$data[$used]["smin"]      = $target->schedule->time_range->start_min;
		$data[$used]["ehour"]     = $target->schedule->time_range->end_hour;
		$data[$used]["emin"]      = $target->schedule->time_range->end_min;

		for($z = 0 ; $z < MAX_NUM_EVENT_TYPE; ++$z){
			$data[$used]["event_type"][$z]["enabled"]=$target->event_type[$z]->enabled;
			$data[$used]["event_type"][$z]["type"]=$target->event_type[$z]->type;
			$data[$used]["event_type"][$z]["code"]=$target->event_type[$z]->code;
			$data[$used]["event_type"][$z]["index"]=$target->event_type[$z]->index;
		}
		++$used;
	}
	if( $used )
		echo json_encode($data);
	else
		echo "[]";
}	
function event_rules_view_post() 
{
	$enable = 1;
	for($index = 0 ; $index < MAX_NUM_TRIGGER; ++$index)
	{	
		$data = $GLOBALS['event_rules']->event[$index];
		if($data->id != 0)
		{
			echo "event=".$index . "\r\n";
			echo "id=" 			. $data->id. "\r\n";
			echo "enabled=" 	. $data->enabled 	. "\r\n";
			echo "name="		. trim($data->name) . "\r\n";
			echo "action_id="	. $data->action_id 	. "\r\n";

			echo "schedule->always=" 				. $data->schedule->always 		. "\r\n";
			echo "schedule->Week->sun="				. $data->schedule->week->sun	. "\r\n";
			echo "schedule->Week->mon="				. $data->schedule->week->mon	. "\r\n";
			echo "schedule->Week->tue="				. $data->schedule->week->tue	. "\r\n";
			echo "schedule->Week->wed="				. $data->schedule->week->wed	. "\r\n";
			echo "schedule->Week->thu="				. $data->schedule->week->thu	. "\r\n";
			echo "schedule->Week->fri="				. $data->schedule->week->fri	. "\r\n";
			echo "schedule->Week->sat="				. $data->schedule->week->sat	. "\r\n";
			echo "schedule->TimeRange->start_hour="	. $data->schedule->time_range->start_hour 	. "\r\n";
			echo "schedule->TimeRange->start_min=" 	. $data->schedule->time_range->start_min 	. "\r\n";
			echo "schedule->TimeRange->end_hour=" 	. $data->schedule->time_range->end_hour		. "\r\n";
			echo "schedule->TimeRange->end_min=" 	. $data->schedule->time_range->end_min		. "\r\n";

			for($z = 0 ; $z< MAX_NUM_EVENT_TYPE; ++$z)
			{	
				if($data->event_type[$z]->enabled)
				{
					echo "  event_type=" . $z. "\r\n";
					echo "  event_conf->type=" 	. $data->event_type[$z]->type 	. "\r\n";
					echo "  event_conf->code=" 	. $data->event_type[$z]->code 	. "\r\n";
					echo "  event_conf->index=" 	. $data->event_type[$z]->index 	. "\r\n";
				}
			}
			$enable = 0;
		}
	}
	return $enable;
}

function change_event_rules_enabled($index) 
{
	if( !isset($_REQUEST['enabled'])) return 1;
	if( $_REQUEST['enabled'] != 0 && $_REQUEST['enabled'] != 1 ) return -1;
		$data = $GLOBALS['event_rules']->event[$index];

	$GLOBALS['event_rules']->event[$index]->enabled = $_REQUEST['enabled'];
	return 0;
}
function change_event_rules_name($index)
{
	if( !isset($_REQUEST['name'])) return 1;
	if (strlen($_REQUEST['name']) > 30 || strlen($_REQUEST['name']) < 3 ) return -1;
	$GLOBALS['event_rules']->event[$index]->name = $_REQUEST['name'];
	return 0;
}
function change_event_rules_action_id($index)
{
	if( !isset($_REQUEST['action_id']) ) return 1;
	$GLOBALS['event_rules']->event[$index]->action_id = $_REQUEST['action_id'];
	return 0;
}
function change_event_type($index) 
{
	$data = $GLOBALS['event_rules']->event[$index];
	$changed = 1;
	for($i = 0 ; $i < MAX_NUM_EVENT_TYPE; ++$i)
	{
		if(isset($_REQUEST['event'.$i.'_enabled'])){
			$data->event_type[$i]->enabled = $_REQUEST['event'.$i.'_enabled'];
			if(isset($_REQUEST['event'.$i.'_type']) ) {
				$data->event_type[$i]->type = $_REQUEST['event'.$i.'_type'];
			}
			if(isset($_REQUEST['event'.$i.'_code']) ) {
				$data->event_type[$i]->code = $_REQUEST['event'.$i.'_code'];
			}
			if(isset($_REQUEST['event'.$i.'_index']) ) {
				$data->event_type[$i]->index= $_REQUEST['event'.$i.'_index'];
			}
			$changed = 0;
		}
	}
	return $changed;
}
function add_trigger_event()
{
	for( $index = 0 ; $index < MAX_NUM_TRIGGER ; ++$index) 
	{
		if( $GLOBALS['event_rules']->event[$index]->id == 0 ) {
			break;
		}
	}
	if( $index == MAX_NUM_TRIGGER ) return -1;
	if( change_event_rules_enabled($index) < 0 ) 	return -1;
	if( change_event_rules_name($index) 	< 0 ) 	return -1;
	if( change_event_rules_action_id($index) < 0 ) return -1;
	if( change_schedule($index) < 0 ) return -1;
	if( change_event_type($index) != 0 ) return -1;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['event_rules']->event[$index], CMD_ADD_EVENT_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else {
		show_post_ok();
	}
	return 0;
}
function modify_trigger_event()
{
	if( !isset($_REQUEST['id']) ) return -1;

	// check Index
	for( $index=0 ; $index < MAX_NUM_TRIGGER ; $index++) {
		if( $_REQUEST['id'] == $GLOBALS['event_rules']->event[$index]->id)
			break;
	}
	if( $index >= MAX_NUM_TRIGGER || $GLOBALS['event_rules']->event[$index]->id == 0) return 1;
	
	if( change_event_rules_enabled($index) < 0 ) 	return -1;
	if( change_event_rules_name($index) 	< 0 ) 	return -1;
	if( change_event_rules_action_id($index) < 0 ) return -1;

	if( change_schedule($index) < 0 ) return -1;
	if( change_event_type($index) != 0 ) return -1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['event_rules']->event[$index], CMD_SET_EVENT_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else {
		show_post_ok();
	}
	return 0;
}
function del_trigger_event()
{
	if( !isset($_REQUEST['id']) ) return -1;

	// check Index;
	for( $index=0 ; $index < MAX_NUM_TRIGGER ; $index++) {
		if( $_REQUEST['id'] == $GLOBALS['event_rules']->event[$index]->id){
			break;
		}
	}
	if( $index >= MAX_NUM_TRIGGER || $GLOBALS['event_rules']->event[$index]->id == 0) return 1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['event_rules']->event[$index], CMD_DEL_EVENT_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else {
		show_post_ok();
	}
	return 0;
}

function trigger_action_view_post()
{
	$enable = 1;
	for($index = 0 ; $index < MAX_NUM_TRIGGER; ++$index)
	{	
		$data = $GLOBALS['action_rules']->action[$index];
		if($data->id != 0)
		{
			echo "action="	. $index 			. "\r\n";
			echo "id=" 		. $data->id 		. "\r\n";
			echo "name=" 	. trim($data->name)	. "\r\n";
			if( $GLOBALS['get_oem'] != 2){
				echo "duration="	. $data->duration		. "\r\n";
			}
			
			for($z = 0 ; $z< MAX_NUM_ACTION_JOB; $z++)
			{	
				if($data->action_job[$z]->type != 0)
				{
					echo "action_job=" . $z. "\r\n";
					echo "action_job->type=" 	. $data->action_job[$z]->type 	. "\r\n";
					echo "action_job->index="	. $data->action_job[$z]->index 	. "\r\n";
				}
			}
			$enable = 0;
		}
	}
	return $enable;
}
function change_action_job($index)
{
	$data = $GLOBALS['action_rules']->action[$index];
	$changed = 1;
	for($i = 0 ; $i < MAX_NUM_ACTION_JOB ; ++$i){
		if( !isset($_REQUEST['action'.$i.'_type'])) continue;
		$data->action_job[$i]->type = $_REQUEST['action'.$i.'_type'];
		switch ($data->action_job[$i]->type)
		{
		case 2: // FTP
		case 3: // SMTP
        	case 9: // FTP_CLIP
			if( $GLOBALS['system_caps']->video_in > 1 ) {
				$data->action_job[$i]->index = $_REQUEST['action'.$i.'_index'];
				$changed = 0;
			}
		case 1: // REC
		case 4:
        	case 5: // HTTP
			if(isset($_REQUEST['action'.$i .'_index'])) {
				$data->action_job[$i]->index = $_REQUEST['action'.$i.'_index'];
				$changed = 0;
			}
		case 6: // PRESET
			if(isset($_REQUEST['action'.$i .'_index'])) {
				$data->action_job[$i]->index = $_REQUEST['action'.$i.'_index'];
				$changed = 0;
			}
		case 7: // PRESET_TOUR
			if(isset($_REQUEST['action'.$i .'_index'])) {
				$data->action_job[$i]->index = $_REQUEST['action'.$i.'_index'];
				$changed = 0;
			}
		case 8: // WHITE_LED
			if(isset($_REQUEST['action'.$i .'_index'])) {
				$data->action_job[$i]->index = $_REQUEST['action'.$i.'_index'];
				$changed = 0;
			}
			break;
		}
	}
	return $changed;
}
function change_trigger_name($index)
{
	if( !isset($_REQUEST['name'])) return 1;
	if (strlen($_REQUEST['name']) > 30 || strlen($_REQUEST['name']) < 3 ) return -1;
	$GLOBALS['action_rules']->action[$index]->name = $_REQUEST['name'];
	return 0;
}
function change_trigger_interval($index)
{

	if( !isset($_REQUEST['duration'])) return 1;
	if ($_REQUEST['duration'] > 60 || $_REQUEST['duration'] < 0 ) return -1;
	$GLOBALS['action_rules']->action[$index]->duration = $_REQUEST['duration'];
	return 0;
}
function add_trigger_action()
{
	for( $index = 0 ; $index < MAX_NUM_TRIGGER ; ++$index) {
		if( $GLOBALS['action_rules']->action[$index]->id == 0 ) {
			break;
		}
	}
	if( $index >= MAX_NUM_TRIGGER ) return -1;
	if( change_trigger_name($index) < 0) return -1;
	if( change_trigger_interval($index) < 0) return -1;
	if( change_action_job($index) < 0) return -1;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['action_rules']->action[$index], CMD_ADD_ACTION_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else {
		show_post_ok();
	}
	return 0;
}
function modify_trigger_action()
{
	if( !isset($_REQUEST['id']) ) return -1;

	// check index
	for($index=0; $index < MAX_NUM_TRIGGER ; ++$index) {
		if( $_REQUEST['id'] == $GLOBALS['action_rules']->action[$index]->id){
			break;
		}
	}
	if( $index >= MAX_NUM_TRIGGER || $_REQUEST['id'] == 0) return 1;

	if( change_trigger_name($index) < 0) return -1;
	if( change_trigger_interval($index) < 0) return -1;
	if( change_action_job($index) < 0) return -1;
	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['action_rules']->action[$index], CMD_SET_ACTION_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else  {
		show_post_ok();
	}
	return 0;
}
function del_trigger_action()
{
	if( !isset($_REQUEST['id']) ) return -1;

	// check index
	for($index=0; $index < MAX_NUM_TRIGGER ; ++$index) {
		if( $_REQUEST['id'] == $GLOBALS['action_rules']->action[$index]->id){
			break;
		}
	}
	if( $index >= MAX_NUM_TRIGGER || $_REQUEST['id'] == 0) return 1;

	$ipc_sock = new IPCSocket();
	$ipc_sock->Connection($GLOBALS['action_rules']->action[$index], CMD_DEL_ACTION_CONF);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK) {
		show_post_ng();
		echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
		return 1;
	} else {
		show_post_ok();
	}
	return 0;
}
function action_rules_get_json()
{
	echo '[';
	for($index = 0 ; $index < MAX_NUM_TRIGGER; ++$index)
	{	
		$data = $GLOBALS['action_rules']->action[$index];
		if($data->id != 0)
		{
			echo "{";
			echo 'id:' 			. $data->id;
			echo ', name:"'		. trim($data->name) .'"';
			echo ', duration:' 	. $data->duration;
			echo ', action_job: [';
			for($z = 0 ; $z < MAX_NUM_EVENT_TYPE; ++$z)
			{	
				echo '{ type:' 		. $data->action_job[$z]->type;
				echo ', index:' . $data->action_job[$z]->index . '},';
			}
			echo "]";
			$enable = 0;
			echo "},";
		}
	}
	echo ']';
}
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if ($_REQUEST['msubmenu'] == 'event' ) {
	$changed = 0;
	if( $_REQUEST['action'] == 'view') {
		event_rules_view_post();
		exit;
	} else if( $_REQUEST['action'] == 'add') {
		add_trigger_event();
		exit;
	} else if( $_REQUEST['action'] == 'modify') {
		modify_trigger_event();
		exit;
	} else if( $_REQUEST['action'] == 'remove') {
		del_trigger_event();
		exit;
	} else if( $_REQUEST['action'] == 'get') {
		event_rules_get_json();
		exit;
	}
	exit;
} else if ($_REQUEST['msubmenu'] == 'action' ) {
	if( $_REQUEST['action'] == 'view') {
		trigger_action_view_post();

		exit;
	} else if( $_REQUEST['action'] == 'add') {
		add_trigger_action();
		exit;
	} else if( $_REQUEST['action'] == 'modify') {
		modify_trigger_action();
		exit;
	} else if( $_REQUEST['action'] == 'remove') {
		del_trigger_action();
		exit;
	} else if( $_REQUEST['action'] == 'get') {
		action_rules_get_json();
		exit;
	}
}
show_post_ng();
?>
