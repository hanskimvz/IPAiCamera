<?
require('../_define.inc');
require('../class/event.class');
//require('../class/capability.class');
require('../class/network.class');
require('../class/socket.class');
require('../class/record.class');
require('../class/trigger.class');
require('../class/iNode.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$event_conf = new CEventConfiguration($shm_id);
//$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$triggers_conf= new CTriggersConfiguration($shm_id);
$action_rules 	= $triggers_conf->action_rules;
$record_conf = new CRecordConfiguration($shm_id);

$iNode_conf = new CiNodeConfiguration($shm_id);

shmop_close($shm_id);

//--- transfer setup
function transfer_view_post()
{
	echo "mode=" 			. $GLOBALS['event_conf']->transfer_conf->mode . "\r\n";
	echo "image_num="	 	. $GLOBALS['event_conf']->transfer_conf->numofimg . "\r\n";
	echo "pre_duration=" 	. $GLOBALS['event_conf']->transfer_conf->preduration . "\r\n";
	echo "post_duration=" 	. $GLOBALS['event_conf']->transfer_conf->postduration . "\r\n";
	echo "max_img_enable=" 	. $GLOBALS['event_conf']->transfer_conf->maxImgEnabled . "\r\n";
	echo "max_img_cnt=" 	. $GLOBALS['event_conf']->transfer_conf->maxImgCnt . "\r\n";
	//echo "channel="		. $GLOBALS['transfer_conf']['channel'] . "\r\n";
}

function change_transfer_transmode()
{
	if(!isset($_REQUEST['mode'])) return 1;
	if($_REQUEST['mode']<0 || $_REQUEST['mode']>3) return -1;	// _BY_JGKO_20130620_TRANSFER_DISABLE 

	$GLOBALS['event_conf']->transfer_conf->mode = $_REQUEST['mode'];
	return 0;
}

function change_transfer_recordmode()
{
	//if(!isset($_REQUEST['sd_record'])) return 1;
	//if($_REQUEST['sd_record']<0 || $_REQUEST['sd_record']>1) return -1;

	//$GLOBALS['transfer_conf']['record'] = $_REQUEST['sd_record'];
	//shm_update_c(OFFSET_EVENT+24, $_REQUEST['sd_record']);
	return 0;
}

// _BY_KHLEE_20130709_FLEXIBLE_CODEC
function change_transfer_channel()
{
//	if(!isset($_REQUEST['channel'])) return 1;
//	if($_REQUEST['channel']<0 || $_REQUEST['channel']>3) return -1;

	//$GLOBALS['transfer_conf']['channel'] = $_REQUEST['channel'];
	//shm_update_c(OFFSET_EVENT+25, $_REQUEST['channel']);
	return 0;
}

function change_transfer_numofimage()
{
	if(!isset($_REQUEST['image_num'])) return 1;
	if($_REQUEST['image_num']<1 || $_REQUEST['image_num']>5) return -1;
//	if($_REQUEST['image_num']==4) return -1;

	$GLOBALS['event_conf']->transfer_conf->numofimg = $_REQUEST['image_num'];
	return 0;
}

function change_transfer_preduration()
{
	if(!isset($_REQUEST['pre_duration'])) return 1;
	$GLOBALS['event_conf']->transfer_conf->preduration = $_REQUEST['pre_duration'];
	return 0;
}

function change_transfer_postduration()
{
	if(!isset($_REQUEST['post_duration'])) return 1;
	$GLOBALS['event_conf']->transfer_conf->postduration = $_REQUEST['post_duration'];
	return 0;
}

function change_transfer_maximgenabled()
{
	if(!isset($_REQUEST['max_img_enable'])) return 1;
	$GLOBALS['event_conf']->transfer_conf->maxImgEnabled = $_REQUEST['max_img_enable'];
	return 0;
}

function change_transfer_maximgcnt()
{
	if(!isset($_REQUEST['max_img_cnt'])) return 1;
	$GLOBALS['event_conf']->transfer_conf->maxImgCnt = $_REQUEST['max_img_cnt'];
	return 0;
}

function change_transfer()
{
	if (change_transfer_transmode() < 0) return -1;
	//if (change_transfer_recordmode() < 0) return -1;
	if (change_transfer_numofimage() < 0) return -1;
	if (change_transfer_preduration() < 0) return -1;
	if (change_transfer_postduration() < 0) return -1;
	if (change_transfer_maximgenabled() < 0) return -1;
	if (change_transfer_maximgcnt() < 0) return -1;

	//if (0) //($GLOBALS['system_conf']['system_option'] & _BY_KHLEE_20130709_FLEXIBLE_CODEC)
	//	if (change_transfer_channel() < 0) return -1;
	
	return 0;
}

//--- ftp
function ftp_view_post()
{

	echo  "enabled="       .$GLOBALS['net_conf']->FtpSetting->Enabled             . "\r\n";
	echo  "pasv_mode="    .$GLOBALS['net_conf']->FtpSetting->PassiveModeEnabled  . "\r\n";
	echo  "ftp_addr="     .trim($GLOBALS['net_conf']->FtpSetting->Server)        . "\r\n";
	echo  "upload_path="  .trim($GLOBALS['net_conf']->FtpSetting->Directory)     . "\r\n";
	echo  "port="         .$GLOBALS['net_conf']->FtpSetting->Port                . "\r\n";
	echo  "id="           .trim($GLOBALS['net_conf']->FtpSetting->Username)      . "\r\n";
	echo  "pass="         .trim($GLOBALS['net_conf']->FtpSetting->Password)      . "\r\n";

	if( $GLOBALS['net_conf']->FtpSetting->Status == M_TEST_FTP_OK)
		$test_result = 1;
	else
		$test_result = 0;
	echo "status="		.$test_result . "\r\n";
}
function change_ftp_enabled()
{
	if(!isset($_REQUEST['enabled'])) return 1;
	if($_REQUEST['enabled']<0 || $_REQUEST['enabled']>1) return -1;

	$GLOBALS['net_conf']->FtpSetting->Enabled = $_REQUEST['enabled'];
	return 0;
}
function change_ftp_pasv_mode()
{
	if(!isset($_REQUEST['pasv_mode'])) return 1;
	if($_REQUEST['pasv_mode']<0 || $_REQUEST['pasv_mode']>1) return -1;

	$GLOBALS['net_conf']->FtpSetting->PassiveModeEnabled = $_REQUEST['pasv_mode'];
	return 0;
}

function change_ftp_addr()
{
	if(!isset($_REQUEST['ftp_addr'])) return 1;
	if(strlen($_REQUEST['ftp_addr']) > 62) return -1;

	$GLOBALS['net_conf']->FtpSetting->Server = $_REQUEST['ftp_addr'];
	return 0;
}

function change_ftp_path()
{
	if(!isset($_REQUEST['upload_path'])) return 1;
	if(strlen($_REQUEST['upload_path']) > 255) return -1;

	$GLOBALS['net_conf']->FtpSetting->Directory = $_REQUEST['upload_path'];
	return 0;
}

function change_ftp_port()
{
	if(!isset($_REQUEST['port'])) return 1;
	if($_REQUEST['port']<1 || $_REQUEST['port']>65535) return -1;

	$GLOBALS['net_conf']->FtpSetting->Port = $_REQUEST['port'];
	return 0;
}

function change_ftp_id()
{
	if(!isset($_REQUEST['id'])) return 1;
	if(strlen($_REQUEST['id']) > 30) return -1;

	$GLOBALS['net_conf']->FtpSetting->Username = $_REQUEST['id'];
	return 0;
}

function change_ftp_password()
{
	if(!isset($_REQUEST['pass'])) return 1;
	if(strlen($_REQUEST['pass']) > 30) return -1;

	$GLOBALS['net_conf']->FtpSetting->Password = $_REQUEST['pass'];
	return 0;
}

function change_ftp()
{
	if (change_ftp_enabled()   < 0) return -1;
	if (change_ftp_pasv_mode() < 0) return -1;
	if (change_ftp_addr()      < 0) return -1;
	if (change_ftp_path()      < 0) return -1;
	if (change_ftp_port()      < 0) return -1;
	if (change_ftp_id()        < 0) return -1;
	if (change_ftp_password()  < 0) return -1;
	
	return 0;
}

function ftp_getresult()
{
	$ftp_status = 0;
	$ftp_result = 0;

	if($GLOBALS['net_conf']->FtpSetting->Status == M_TEST_TRANSMITTER_OK)
	{
		$ftp_status = M_TEST_TRANSMITTER_OK;
		$ftp_result = M_TEST_TRANSMITTER_OK;
	}
	else if($GLOBALS['net_conf']->FtpSetting->Status == M_TEST_TRANSMITTER_DOING)
	{
		$ftp_status = M_TEST_TRANSMITTER_DOING;
		$ftp_result = M_TEST_TRANSMITTER_NONE;
	}
	else if($GLOBALS['net_conf']->FtpSetting->Status == M_TEST_TRANSMITTER_NONE)
	{
		$ftp_status = M_TEST_TRANSMITTER_NONE;
		$ftp_result = M_TEST_TRANSMITTER_NONE;
	}
	else
	{
		$ftp_status = M_TEST_TRANSMITTER_OK;
		$ftp_result = 100 + $GLOBALS['net_conf']->FtpSetting->Status;
	}

	echo "[1,$ftp_status,$ftp_result]\r\n";
}
//--- iNode
function inode_view_post()
{
	echo  "enabled="        .$GLOBALS['net_conf']->FtpSetting->Enabled             . "\r\n";
	echo  "ftp_addr="       .trim($GLOBALS['net_conf']->FtpSetting->Server)        . "\r\n";
	echo  "upload_path="    .trim($GLOBALS['net_conf']->FtpSetting->Directory)     . "\r\n";
	echo  "port="           .$GLOBALS['net_conf']->FtpSetting->Port                . "\r\n";
	echo  "id="             .trim($GLOBALS['net_conf']->FtpSetting->Username)      . "\r\n";
	echo  "pass="           .trim($GLOBALS['net_conf']->FtpSetting->Password)      . "\r\n";
	echo  "type="           .trim($GLOBALS['net_conf']->iNodeSetting->Type)        . "\r\n";
	echo  "image_num="	 	.$GLOBALS['event_conf']->transfer_conf->numofimg       . "\r\n";
	echo  "pre_duration=" 	.$GLOBALS['event_conf']->transfer_conf->preduration    . "\r\n";
	echo  "post_duration=" 	.$GLOBALS['event_conf']->transfer_conf->postduration   . "\r\n";

	$data = $GLOBALS['action_rules']->action[0];
	if($data->id != 0)
	{
		echo "duration="	. $data->duration		. "\r\n";
	}
	else{
		echo "duration=0"	. "\r\n"; 
	}
		
	echo  "auto_delete=" 	.$GLOBALS['event_conf']->StorageDevices->Device[0]->AutoDelete . "\r\n";
	echo  "target_stream="	.$GLOBALS['record_conf']->target_stream->value . "\r\n";
}
function change_inode_enabled()
{
	if(!isset($_REQUEST['enabled'])) 
	{
		$GLOBALS['iNode_conf']->Enabled = $GLOBALS['net_conf']->FtpSetting->Enabled;
	}
	else{
		if($_REQUEST['enabled']<0 || $_REQUEST['enabled']>1) return -1;
		$GLOBALS['iNode_conf']->Enabled = $_REQUEST['enabled'];
	}
	return 0;
}

function change_inode_addr()
{
	if(!isset($_REQUEST['ftp_addr']))
	{
		$GLOBALS['iNode_conf']->Server = trim($GLOBALS['net_conf']->FtpSetting->Server);
	}
	else{
		if(strlen($_REQUEST['ftp_addr']) > 62) return -1;
		$GLOBALS['iNode_conf']->Server = $_REQUEST['ftp_addr'];
	}
	return 0;
}

function change_inode_path()
{
	if(!isset($_REQUEST['upload_path']))
	{
		$GLOBALS['iNode_conf']->Directory = trim($GLOBALS['net_conf']->FtpSetting->Directory);
	}
	else
	{
		if(strlen($_REQUEST['upload_path']) > 255) return -1;
		$GLOBALS['iNode_conf']->Directory = $_REQUEST['upload_path'];
	}
	return 0;
}

function change_inode_port()
{
	if(!isset($_REQUEST['port']))
	{
		$GLOBALS['iNode_conf']->Port = $GLOBALS['net_conf']->FtpSetting->Port;
	}
	else
	{
		if($_REQUEST['port']<1 || $_REQUEST['port']>65535) return -1;
		$GLOBALS['iNode_conf']->Port = $_REQUEST['port'];
	}
	return 0;
}

function change_inode_id()
{
	
	if(!isset($_REQUEST['id']))
	{
		$GLOBALS['iNode_conf']->Username = trim($GLOBALS['net_conf']->FtpSetting->Username);
	}
	else
	{
		if(strlen($_REQUEST['id']) > 30) return -1;
		$GLOBALS['iNode_conf']->Username = $_REQUEST['id'];
	}
	return 0;
}

function change_inode_password()
{
	
	if(!isset($_REQUEST['pass']))
	{
		$GLOBALS['iNode_conf']->Password = trim($GLOBALS['net_conf']->FtpSetting->Password);
	}
	else
	{
		if(strlen($_REQUEST['pass']) > 30) return -1;
		$GLOBALS['iNode_conf']->Password = $_REQUEST['pass'];
	}
	
	return 0;
}

function change_inode_type()
{
	
	if(!isset($_REQUEST['type']))
	{
		$GLOBALS['iNode_conf']->Type = trim($GLOBALS['net_conf']->iNodeSetting->Type);
	}
	else
	{
		if($_REQUEST['type']<0 || $_REQUEST['type']>1) return -1;
		$GLOBALS['iNode_conf']->Type = $_REQUEST['type'];
	}
	return 0;
}

function change_inode_numofimage()
{
	if(!isset($_REQUEST['image_num']))
	{
		$GLOBALS['iNode_conf']->numofimg = $GLOBALS['event_conf']->transfer_conf->numofimg;
	}
	else
	{
		if($_REQUEST['image_num']<1 || $_REQUEST['image_num']>5) return -1;
		$GLOBALS['iNode_conf']->numofimg = $_REQUEST['image_num'];
	}
	return 0;
}

function change_inode_preduration()
{
	if(!isset($_REQUEST['pre_duration']))
	{
		$GLOBALS['iNode_conf']->preduration = $GLOBALS['event_conf']->transfer_conf->preduration;
	}
	else
	{
		if($_REQUEST['pre_duration']<1 || $_REQUEST['pre_duration']>5) return -1;
		$GLOBALS['iNode_conf']->preduration = $_REQUEST['pre_duration'];
	}
	return 0;
}

function change_inode_postduration()
{
	if(!isset($_REQUEST['post_duration']))
	{
		$GLOBALS['iNode_conf']->postduration = $GLOBALS['event_conf']->transfer_conf->postduration;
	}
	else
	{
		if($_REQUEST['post_duration']<1 || $_REQUEST['post_duration']>30) return -1;
		$GLOBALS['iNode_conf']->postduration = $_REQUEST['post_duration'];
	}
	return 0;
}

function change_inode_duration()
{
	if(!isset($_REQUEST['duration']))
	{
		if($GLOBALS['action_rules']->action[0]->id != 0)
		{
			$GLOBALS['iNode_conf']->duration = $GLOBALS['action_rules']->action[0]->duration;
		}
		else
		{
			$GLOBALS['iNode_conf']->duration = 0;
		}
	}
	else
	{
		if($_REQUEST['duration']<0 || $_REQUEST['duration']>60) return -1;
		$GLOBALS['iNode_conf']->duration = $_REQUEST['duration'];
	}
	return 0;
}


function change_inode_autodelete()
{
	if(!isset($_REQUEST['autodelete']))
	{
		$GLOBALS['iNode_conf']->AutoDelete = $GLOBALS['event_conf']->StorageDevices->Device[0]->AutoDelete;
	}
	else
	{
		if($_REQUEST['autodelete']<0 || $_REQUEST['autodelete']>4) return -1;
		$GLOBALS['iNode_conf']->AutoDelete = $_REQUEST['autodelete'];
	}
	return 0;
}

function change_inode_targetStream()
{
	if(!isset($_REQUEST['target_stream']))
	{
		$GLOBALS['iNode_conf']->targetStream = $GLOBALS['record_conf']->target_stream->value;
	}
	else
	{
		if($_REQUEST['target_stream']<-1 || $_REQUEST['target_stream']>1) return -1;
		$GLOBALS['iNode_conf']->targetStream = $_REQUEST['target_stream'];
	}
	return 0;
}


function change_inode()
{
	if (change_inode_enabled()   < 0) return -1;
	if (change_inode_addr()      < 0) return -1;
	if (change_inode_path()      < 0) return -1;
	if (change_inode_port()      < 0) return -1;
	if (change_inode_id()        < 0) return -1;
	if (change_inode_password()  < 0) return -1;
	if (change_inode_type()  	 < 0) return -1;
	if (change_inode_numofimage() < 0) return -1;
	if (change_inode_preduration() < 0) return -1;
	if (change_inode_postduration() < 0) return -1;
	if (change_inode_duration() < 0) return -1;
	if (change_inode_autodelete() < 0) return -1;
	if (change_inode_targetStream() < 0) return -1;
	return 0;
}
//--- smtp
function smtp_view_post()
{

	echo  "enabled="      .$GLOBALS['net_conf']->SmtpSetting->Enabled         ."\r\n";
	echo  "smtp_addr="   .trim($GLOBALS['net_conf']->SmtpSetting->Server)    ."\r\n";
    echo  "ssl_enable="  .$GLOBALS['net_conf']->SmtpSetting->SSL_Enabled     ."\r\n";
	echo  "smtp_port="   .$GLOBALS['net_conf']->SmtpSetting->Port            ."\r\n";
	echo  "ssl_port="    .$GLOBALS['net_conf']->SmtpSetting->SSL_Port        ."\r\n";
	echo  "id="          .trim($GLOBALS['net_conf']->SmtpSetting->Username)  ."\r\n";
	echo  "pass="        .trim($GLOBALS['net_conf']->SmtpSetting->Password)  ."\r\n";
	echo  "sender="      .trim($GLOBALS['net_conf']->SmtpSetting->Sender)    ."\r\n";
	echo  "receiver="    .trim($GLOBALS['net_conf']->SmtpSetting->Receiver)  ."\r\n";
	echo  "title="       .trim($GLOBALS['net_conf']->SmtpSetting->Subject)   ."\r\n";
	echo  "message="     .trim($GLOBALS['net_conf']->SmtpSetting->Body)      ."\r\n";
	echo  "detailedinfo=" .trim($GLOBALS['net_conf']->SmtpSetting->DetailedInfo) ."\r\n";
	echo  "cameraname=" .trim($GLOBALS['net_conf']->SmtpSetting->CameraName) ."\r\n";
	echo  "eventrulename=" .trim($GLOBALS['net_conf']->SmtpSetting->EventRuleName) ."\r\n";

	
/*	if ( $GLOBALS['net_conf']->SmtpSetting->Status == M_TEST_TRANSMITTER_OK )
		$test_result = 1;
	else
		$test_result = 0;
	echo "status="		.$test_result . "\r\n";*/
}
function change_smtp_enable()
{
	if(!isset($_REQUEST['enabled'])) return 1;
	if($_REQUEST['enabled']<0 || $_REQUEST['enabled']>1) return -1;
	
	$GLOBALS['net_conf']->SmtpSetting->Enabled= $_REQUEST['enabled'];
	return 0;
}
function change_smtp_ssl_enable()
{
	if(!isset($_REQUEST['ssl_enable'])) return 1;
	if($_REQUEST['ssl_enable']<0 || $_REQUEST['ssl_enable']>1) return -1;
	
	$GLOBALS['net_conf']->SmtpSetting->SSL_Enabled = $_REQUEST['ssl_enable'];
	return 0;
}

function change_smtp_smtp_addr()
{
	if(!isset($_REQUEST['smtp_addr'])) return 1;
	if(strlen($_REQUEST['smtp_addr']) > 62) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Server = $_REQUEST['smtp_addr'];
	return 0;
}

function change_smtp_port()
{
	if(!isset($_REQUEST['smtp_port'])) return 1;
	if($_REQUEST['smtp_port']<1 || $_REQUEST['smtp_port']>65535) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Port = $_REQUEST['smtp_port'];

	return 0;
}

function change_smtp_sslport()
{
	if(!isset($_REQUEST['ssl_port'])) return 1;
	if ( $_REQUEST['ssl_port'] != 465 && $_REQUEST['ssl_port'] != 578 
		&& $_REQUEST['ssl_port']<=1024 && $_REQUEST['ssl_port']>65535 )
		return -1;

	$GLOBALS['net_conf']->SmtpSetting->SSL_Port = $_REQUEST['ssl_port'];
	return 0;
}

function change_smtp_userid()
{
	if(!isset($_REQUEST['id'])) return 1;
	if(strlen($_REQUEST['id']) > 30) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Username = $_REQUEST['id'];
	return 0;
}

function change_smtp_userpass()
{
	if(!isset($_REQUEST['pass'])) return 1;
	if(strlen($_REQUEST['pass']) > 30) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Password = $_REQUEST['pass'];
	return 0;
}

function change_smtp_sender()
{
	if(!isset($_REQUEST['sender'])) return 1;
	if(strlen($_REQUEST['sender']) > 62) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Sender = $_REQUEST['sender'];
	return 0;
}

function change_smtp_receiver()
{
	if(!isset($_REQUEST['receiver'])) return 1;
	if(strlen($_REQUEST['receiver']) > 126) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Receiver = $_REQUEST['receiver'];
	return 0;
}

function change_smtp_subject()
{
	if(!isset($_REQUEST['title'])) return 1;
	if(strlen($_REQUEST['title']) > 127) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Subject = $_REQUEST['title'];
	return 0;
}

function change_smtp_body()
{
	if(!isset($_REQUEST['message'])) return 1;
	if(strlen($_REQUEST['message']) > 255) return -1;

	$GLOBALS['net_conf']->SmtpSetting->Body = $_REQUEST['message'];
	return 0;
}

function change_smtp_detailinfo()
{
	if(!isset($_REQUEST['detailedinfo'])) return 1;
	if(strlen($_REQUEST['detailedinfo']) > 127) return -1;

	$GLOBALS['net_conf']->SmtpSetting->DetailedInfo = $_REQUEST['detailedinfo'];
	return 0;
}

function change_smtp_cameraname()
{
	if(!isset($_REQUEST['cameraname'])) return 1;
	if(strlen($_REQUEST['cameraname']) > 30) return -1;

	$GLOBALS['net_conf']->SmtpSetting->CameraName = $_REQUEST['cameraname'];
	return 0;
}

function change_smtp_eventrulename()
{
	if(!isset($_REQUEST['eventrulename'])) return 1;
	if(strlen($_REQUEST['eventrulename']) > 30) return -1;

	$GLOBALS['net_conf']->SmtpSetting->EventRuleName = $_REQUEST['eventrulename'];
	return 0;
}

function change_smtp()
{
	if  ( change_smtp_enable()     <  0 )  return -1;
	if  ( change_smtp_ssl_enable() <  0 )  return -1;
	if  ( change_smtp_smtp_addr()  <  0 )  return -1;
	if  ( change_smtp_port()       <  0 )  return -1;
	if  ( change_smtp_sslport()    <  0 )  return -1;
	if  ( change_smtp_userid()     <  0 )  return -1;
	if  ( change_smtp_userpass()   <  0 )  return -1;
	if  ( change_smtp_sender()     <  0 )  return -1;
	if  ( change_smtp_receiver()   <  0 )  return -1;
	if  ( change_smtp_subject()    <  0 )  return -1;
	if  ( change_smtp_body()       <  0 )  return -1;
	if  ( change_smtp_detailinfo() <  0 )  return -1;
	if  ( change_smtp_cameraname() <  0 )  return -1;
	if  ( change_smtp_eventrulename() <  0 )  return -1;
	
	return 0;
}


function smtp_getresult()
{
	$smtp_status = 0;
	$smtp_result = 0;

	if($GLOBALS['net_conf']->SmtpSetting->Status == M_TEST_TRANSMITTER_OK)
	{
		$smtp_status = M_TEST_TRANSMITTER_OK;
		$smtp_result = M_TEST_TRANSMITTER_OK;
	}
	else if($GLOBALS['net_conf']->SmtpSetting->Status == M_TEST_TRANSMITTER_DOING)
	{
		$smtp_status = M_TEST_TRANSMITTER_DOING;
		$smtp_result = M_TEST_TRANSMITTER_NONE;
	}
	else if($GLOBALS['net_conf']->SmtpSetting->Status == M_TEST_TRANSMITTER_NONE)
	{
		$smtp_status = M_TEST_TRANSMITTER_NONE;
		$smtp_result = M_TEST_TRANSMITTER_NONE;
	}
	else
	{
		$smtp_status = M_TEST_TRANSMITTER_OK;
		$smtp_result = 100 + $GLOBALS['net_conf']->SmtpSetting->Status;
	}

	echo "[2,$smtp_status,$smtp_result]\r\n";
}



//--- http action
function http_view_post()
{
	echo  "enabled="      .$GLOBALS['net_conf']->HTTPAction->Enabled             ."\r\n";
   // echo  "name="        .trim($GLOBALS['net_conf']->HTTPAction->Name)          ."\r\n";
    echo  "description=" .trim($GLOBALS['net_conf']->HTTPAction->Description)   ."\r\n";
	echo  "http_addr="   .trim($GLOBALS['net_conf']->HTTPAction->Server)        ."\r\n";
	echo  "http_port="   .$GLOBALS['net_conf']->HTTPAction->Port                ."\r\n";
	echo  "id="          .trim($GLOBALS['net_conf']->HTTPAction->Username)      ."\r\n";
	echo  "pass="        .trim($GLOBALS['net_conf']->HTTPAction->Password)      ."\r\n";
	echo  "message="     .trim($GLOBALS['net_conf']->HTTPAction->Body)          ."\r\n";
	
}
function change_http_enable()
{
	if(!isset($_REQUEST['enabled'])) return 1;
	if($_REQUEST['enabled']<0 || $_REQUEST['enabled']>1) return -1;
	
	$GLOBALS['net_conf']->HTTPAction->Enabled= $_REQUEST['enabled'];
	return 0;
}
/*
function change_http_name()
{
	if(!isset($_REQUEST['name'])) return 1;
	if(strlen($_REQUEST['name']) > 62) return -1;

	$GLOBALS['net_conf']->HTTPAction->Name = $_REQUEST['name'];
	return 0;
}*/
function change_http_description()
{
	if(!isset($_REQUEST['description'])) return 1;
	if(strlen($_REQUEST['description']) > 62) return -1;

	$GLOBALS['net_conf']->HTTPAction->Description = $_REQUEST['description'];
	return 0;
}
function change_http_addr()
{
	if(!isset($_REQUEST['http_addr'])) return 1;
	if(strlen($_REQUEST['http_addr']) > 62) return -1;

	$GLOBALS['net_conf']->HTTPAction->Server = $_REQUEST['http_addr'];
	return 0;
}
function change_http_port()
{
	if(!isset($_REQUEST['http_port'])) return 1;
	if($_REQUEST['http_port']<1 || $_REQUEST['http_port']>65535) return -1;

	$GLOBALS['net_conf']->HTTPAction->Port = $_REQUEST['http_port'];

	return 0;
}

function change_http_userid()
{
	if(!isset($_REQUEST['id'])) return 1;
	if(strlen($_REQUEST['id']) > 30) return -1;

	$GLOBALS['net_conf']->HTTPAction->Username = $_REQUEST['id'];
	return 0;
}

function change_http_userpass()
{
	if(!isset($_REQUEST['pass'])) return 1;
	if(strlen($_REQUEST['pass']) > 30) return -1;

	$GLOBALS['net_conf']->HTTPAction->Password = $_REQUEST['pass'];
	return 0;
}

function change_http_body()
{
	if(!isset($_REQUEST['message'])) return 1;
	if(strlen($_REQUEST['message']) > 1024) return -1;

	$GLOBALS['net_conf']->HTTPAction->Body = $_REQUEST['message'];
	return 0;
}

function change_http()
{
	if  ( change_http_enable()      <  0 )  return -1;
    //if  ( change_http_name()        <  0 )  return -1;
    if  ( change_http_description() <  0 )  return -1;
	if  ( change_http_addr()        <  0 )  return -1;
	if  ( change_http_port()        <  0 )  return -1;
	if  ( change_http_userid()      <  0 )  return -1;
	if  ( change_http_userpass()    <  0 )  return -1;
	if  ( change_http_body()        <  0 )  return -1;
	
	return 0;
}


function http_getresult()
{
	$http_status = 0;
	$http_result = 0;

	if($GLOBALS['net_conf']->HTTPAction->Status == M_TEST_TRANSMITTER_OK)
	{
		$http_status = M_TEST_TRANSMITTER_OK;
		$http_result = M_TEST_TRANSMITTER_OK;
	}
	else if($GLOBALS['net_conf']->HTTPAction->Status == M_TEST_TRANSMITTER_DOING)
	{
		$http_status = M_TEST_TRANSMITTER_DOING;
		$http_result = M_TEST_TRANSMITTER_NONE;
	}
	else if($GLOBALS['net_conf']->HTTPAction->Status == M_TEST_TRANSMITTER_NONE)
	{
		$http_status = M_TEST_TRANSMITTER_NONE;
		$http_result = M_TEST_TRANSMITTER_NONE;
	}
	else
	{
		$http_status = M_TEST_TRANSMITTER_OK;
		$http_result = 100 + $GLOBALS['net_conf']->HTTPAction->Status;
	}

	echo "[2,$http_status,$http_result]\r\n";
}


function sdcard_info_post($isJson = false)
{
	$shm_id = shmop_open(KEY_SM_STORAGE_INFO, "a", 0444, 0);
	if(!$shm_id) {
		show_post_ng();
		exit;
	}
	$format  = 'c1mount/c1insert/A256device/A256location/i1total';
	$format .= '/i1used/i1free/iused_percent';
	$size = 530;
	for($i=0; $i < MAX_STORAGE_DEVICE ; $i++)
	{
		// id , offset , size 
		$shm_data = shmop_read($shm_id, $size * $i, $size);
		$data[$i] = unpack($format, $shm_data);
	}
	shmop_close($shm_id);
	if( $isJson ) {
		echo json_encode($data);
	}
	else {
		echo view_array("storage", $data);
	}
}

function change_storage_device_auto_delete($idx)
{
	if (!isset($_REQUEST['auto_delete'])) return 1;
	$GLOBALS['event_conf']->StorageDevices->Device[$idx]->AutoDelete = $_REQUEST['auto_delete'];
	return 0;
}

function change_storage_device_over_write($idx)
{
	if (!isset($_REQUEST['over_write'])) return 1;
	if ($_REQUEST['over_write']<0 || $_REQUEST['over_write']>1) return -1;
	$GLOBALS['event_conf']->StorageDevices->Device[$idx]->OverWrite = $_REQUEST['over_write'];
	return 0;
}
function change_storage_device($idx)
{
	if (change_storage_device_auto_delete($idx) < 0) return -1;
	if (change_storage_device_over_write($idx) < 0) return -1;
	return 0;
}
function sdcard_format($idx)
{
	$ipc_sock = new IPCSocket();
	$StorageDevice= new CInteger();

	$StorageDevice->value = $idx;

	$ipc_sock->Connection($StorageDevice, CMD_SET_FORMAT_SDCARD);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();	
	}
	else
	{
		show_post_ng();
		printf("errorCode : %s\r\n", $ipc_sock->dataInfo['ErrorCode']['value']);
	}
}
function sdcard_unmount($idx)
{
	$ipc_sock = new IPCSocket();
	$StorageDevice= new CInteger();

	$StorageDevice->value = $idx;

	$ipc_sock->Connection($StorageDevice,CMD_SET_UNMOUNT_SDCARD);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
	{
		show_post_ok();	
	}
	else
	{
		show_post_ng();
		printf("errorCode : %s\r\n", $ipc_sock->dataInfo['ErrorCode']['value']);
	}
}
/*
function sdcard_delete()
{
	if($GLOBALS['sdcard_conf']['status'] == 0x03)
	{
		if(isset($_REQUEST['del_option']))
		{
			$GLOBALS['sdcard_conf']['delete_option'] = $_REQUEST['del_option'];
			shm_update_i(OFFSET_EVENT+1831, $_REQUEST['del_option']);
		}

		send_command(M_CGI_SD_DELETE, 0, 0, 0, 0);
		//echo 'OK';
	}
	else if($GLOBALS['sdcard_conf']['status'] == 0x01) // Write protected
	{
		//echo 'WRITEPROTECTED';
	}
	else // No sdcard
	{
		//echo 'NOCARD';
	}
}

function sdcard_getsize()
{
	if ( $GLOBALS['sdcard_conf']['capacity.end'] == 0 )
		$used_percent = 0;
	else
		$used_percent = (int)($GLOBALS['sdcard_conf']['capacity.used']*100 / $GLOBALS['sdcard_conf']['capacity.end']);
	
	$used_size = (int)($GLOBALS['sdcard_conf']['capacity.used']/1000);
	$total_size = (int)($GLOBALS['sdcard_conf']['capacity.end']/1000);

	echo "[".$used_percent.",".$used_size.",".$total_size.",".$GLOBALS['sdcard_conf']['formatting'].",".$GLOBALS['sdcard_conf']['formatting']."]";
}
*/
//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
if ( isset($_REQUEST['submenu']) )
{
if ( $_REQUEST['submenu'] == 'transfer' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_transfer_transfer_setup.cgi">';
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		change_transfer();
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
else if ( $_REQUEST['submenu'] == 'ftp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_transfer_ftp.cgi">';
	}
	else if ( $_REQUEST['action'] == 'getresult' )
	{
		ftp_getresult();
	}
	else if ( $_REQUEST['action'] == 'apply' || $_REQUEST['action'] == 'test' )
	{
		change_ftp();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection(NULL, CMD_TEST_FTP);
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
else if ( $_REQUEST['submenu'] == 'smtp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_transfer_smtp.cgi">';
	}
	else if ( $_REQUEST['action'] == 'getresult' )
	{
		smtp_getresult();
	}
	else if ( $_REQUEST['action'] == 'apply' || $_REQUEST['action'] == 'test' )
	{
		change_smtp();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection(NULL, CMD_TEST_SMTP);
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
else if ( $_REQUEST['submenu'] == 'httpaction' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_transfer_http_action.cgi">';
	}
	else if ( $_REQUEST['action'] == 'getresult' )
	{
		http_getresult();
	}
	else if ( $_REQUEST['action'] == 'apply' || $_REQUEST['action'] == 'test' )
	{
		change_smtp();
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection(NULL, CMD_TEST_HTTP);
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
}
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if ( isset($_REQUEST['msubmenu']))
{
if ( $_REQUEST['msubmenu'] == 'transfer' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		transfer_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_transfer() == 0 )
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
else if ( $_REQUEST['msubmenu'] == 'ftp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		ftp_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_ftp() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
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
else if ( $_REQUEST['msubmenu'] == 'inode' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		inode_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_inode() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['iNode_conf'], CMD_SET_INODE_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				echo "ERROR_CODE=" . $ipc_sock->dataInfo['ErrorCode']['value'] . "\r\n";
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
else if ( $_REQUEST['msubmenu'] == 'smtp' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		smtp_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_smtp() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
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
else if ( $_REQUEST['msubmenu'] == 'httpaction' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		http_view_post();
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if ( change_http() == 0 )
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['net_conf'], CMD_SET_NETWORK_CONFIGURATION);
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
else if ( $_REQUEST['msubmenu'] == 'sdcard' )
{
	$device_no = 0;
	if( isset($_REQUEST['storage_no']) ) {
		$device_no = $_REQUEST['storage_no'];
		if( is_numeric($device_no) == false) {
			show_post_ng();
			exit;
		}
	}
	if ( $_REQUEST['action'] == 'view' )
	{
		$GLOBALS['event_conf']->StorageDevices->getStorageDevciesConfig($device_no);
	}
	else if ( $_REQUEST['action'] == 'format')
	{
		sdcard_format($device_no);
	}
	else if ( $_REQUEST['action'] == 'unmount')
	{
		sdcard_unmount($device_no);
	}
	else if ( $_REQUEST['action'] == 'apply' )
	{
		if( change_storage_device($device_no) >= 0 ){
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection($GLOBALS['event_conf'], CMD_SET_EVENT_CONFIGURATION);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				show_post_ng();
				echo "[".$ipc_sock->dataInfo['ErrorCode']['value'] . "]\r\n";
			}
		}
	}
	else if ( $_REQUEST['action'] == 'info' )
	{
		sdcard_info_post($JSON=false);
	}
	else if ( $_REQUEST['action'] == 'get' )
	{
		sdcard_info_post($JSON=true);
	}
	else
		show_post_ng();
	exit;
}
}
show_post_ng();
?>
