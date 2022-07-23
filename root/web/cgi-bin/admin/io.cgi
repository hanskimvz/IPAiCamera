<?
require('../_define.inc');
require('../class/system.class');
require('../class/socket.class');
require('../class/capability.class');


$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
if(!$shm_id) exit;
$sys_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);

shmop_close($shm_id);


//--- sensor_input #1~8
function sensor_view_post($num)
{
	if ($GLOBALS['sys_conf']->DeviceIo->SensorSettings->Size == 0) {
		show_post_ng();
		return;
	}
  $id = "0";
  $id = $num;
  echo "id="		.$id."\r\n";
  echo "mode="		.$GLOBALS['sys_conf']->DeviceIo->SensorSettings->Sensor[$num]->Mode."\r\n";
}

function change_sensor_device($num)
{
	if($num<0 || $num>7) return -1;
	if(!isset($_REQUEST['mode'])) return 1;
	if($_REQUEST['mode']<0 || $_REQUEST['mode']>3) return -1; // off, no, nc

	$GLOBALS['sys_conf']->DeviceIo->SensorSettings->Sensor[$num]->Mode = $_REQUEST['mode'];
	return 0;
}

//--- relay_out #1~4
function relay_view_post($num)
{
	if ($GLOBALS['sys_conf']->DeviceIo->RelaySettings->Size == 0) {
		show_post_ng();
		return;
	}
  $id = "0";
  $id = $num;
  echo "id="		.$id."\r\n";
	echo "mode="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->Mode."\r\n";
	echo "idlestate="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->IdleState."\r\n";
	echo "duration="		.$GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->DelayTime."\r\n";
}

function change_relay_device($num)
{
	if($num<0 || $num>3) return -1;
	if(!isset($_REQUEST['mode']) && !isset($_REQUEST['idlestate']) && !isset($_REQUEST['duration'])) return 1;
	if(isset($_REQUEST['mode']))
	{
	  if($_REQUEST['mode']<0 || $_REQUEST['mode']>1) return -1;
	  $GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->Mode = $_REQUEST['mode'];
	}
	if(isset($_REQUEST['idlestate']))
	{
	  if($_REQUEST['idlestate']<0 || $_REQUEST['idlestate']>1) return -1;
	  $GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->IdleState = $_REQUEST['idlestate'];
	}
	if(isset($_REQUEST['duration']))
	{
	  if($_REQUEST['duration']<1 || $_REQUEST['duration']>30) return -1;
	  $GLOBALS['sys_conf']->DeviceIo->RelaySettings->Relay[$num]->DelayTime = $_REQUEST['duration'];
	}		
	return 0;
}
//--- temperature
function temperature_view_post()
{
		echo "mode="		.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->mode."\r\n";
		echo "threshold="		.$GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->threshold."\r\n"; 
}

function change_temperature_device()
{
	if(isset($_REQUEST['mode']))
	{
	  if($_REQUEST['mode']<0 || $_REQUEST['mode']>1) return -1;
	  $GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->mode = $_REQUEST['mode'];
	}
	if($_REQUEST['mode'] == 0)
	{
		if(isset($_REQUEST['threshold']))
		{
		  if($_REQUEST['threshold']<50 || $_REQUEST['threshold']>100) return -1;
		  $GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->threshold = $_REQUEST['threshold'];
		}
	}
	else
	{
		if(isset($_REQUEST['threshold']))
		{
		  if($_REQUEST['threshold']<122 || $_REQUEST['threshold']>212) return -1;
		 
		  $GLOBALS['sys_conf']->DeviceIo->TemperatureSettings->threshold = $_REQUEST['threshold'];
		}		
	}

	return 0;
}
//--- rs485
function rs485_view_post()
{
		echo "protocol="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->protocol."\r\n";
		echo "address="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->address."\r\n"; 
		echo "baudrate="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->baudrate."\r\n";
		echo "databit="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->databit."\r\n"; 
		echo "stopbit="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->stopbit."\r\n";
		echo "parity="		.$GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->parity."\r\n"; 
}
function check_valid( $value , $min , $max )
{
	if(isset($_REQUEST[$value]))
	{
	  if($_REQUEST[$value]< $min || $_REQUEST[$value]> $max) return -1;
	  $GLOBALS['sys_conf']->DeviceIo->SerialPortsSetting->$value = $_REQUEST[$value];
	}

	return 0 ;	
}
function change_rs485()
{
	if( check_valid( "protocol", 0 , 1 ) != 0 ) return -1  ;
	if( check_valid( "address", 0 , 255 ) != 0 ) return -1  ;
	if( check_valid( "baudrate", 0 , 9 ) != 0 ) return -1  ;
	if( check_valid( "databit", 0 , 3 ) != 0 ) return -1  ;
	if( check_valid( "stopbit", 0 , 1 ) != 0 ) return -1  ;
	if( check_valid( "parity", 0 , 2 ) != 0 ) return -1  ;
	
	return 0 ;
}
//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
ob_end_clean ();
if ( isset($_REQUEST['msubmenu']) )
{
	if ( $_REQUEST['msubmenu'] == 'sensor')
	{
	  $sensor_num = 0;
		if ( isset($_REQUEST['id']) )
		{
		  $sensor_num = $_REQUEST['id'];
		}  
		if ($GLOBALS['sys_conf']->DeviceIo->SensorSettings->Size <= $sensor_num)
		{
			show_post_ng();
			exit;
		}
		if ( $_REQUEST['action'] == 'view' )
		{
			sensor_view_post($sensor_num);
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if ( change_sensor_device($sensor_num) == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['sys_conf']->DeviceIo, CMD_SET_IO_CONFIGURATION);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
					echo "asd1";
				}
			}
			else
				show_post_ng();
		}
		else
			show_post_ng();
		
		exit;
	}
	else if(  $_REQUEST['msubmenu'] == 'relay' )
	{
	    $relay_num = 0;
		if ( isset($_REQUEST['id']) )
		{
		  $relay_num = $_REQUEST['id'];
		}  
		if ( $GLOBALS['system_caps']->relay_count <= $relay_num)
		{
			show_post_ng();
			exit;
		}
		if ( $_REQUEST['action'] == 'view' )
		{
			relay_view_post($relay_num);
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if ( change_relay_device($relay_num) == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['sys_conf']->DeviceIo, CMD_SET_IO_CONFIGURATION);
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
	else if(  $_REQUEST['msubmenu'] == 'temperature' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			temperature_view_post();
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if ( change_temperature_device() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['sys_conf']->DeviceIo, CMD_SET_IO_CONFIGURATION);
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
	else if(  $_REQUEST['msubmenu'] == 'rs485' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			rs485_view_post();
		}
		else if ( $_REQUEST['action'] == 'apply' )
		{
			if ( change_rs485() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['sys_conf']->DeviceIo, CMD_SET_IO_CONFIGURATION);
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
				show_post_ng();
			}

		}
		else
			show_post_ng();
		
		exit;
	}	
}
?>
