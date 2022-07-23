<?
require('./_define.inc');
require('./class/system.class');
require('./class/socket.class');
require('./class/network.class');
require('./class/media.class');
		  
$system_conf = new CSystemConfiguration();
$net_conf = new CNetworkConfiguration();
      
//--- date/time
function datetime_view_post()
{
	try
	{
		$ipc_sock = new IPCSocket();
		$ipc_sock->Connection($GLOBALS['system_conf']->SystemDatetime, CMD_GET_DATETIME);
		if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
		{
			$SystemTime = $GLOBALS['system_conf']->SystemDatetime->SystemTime;
			printf("system_time=%04d/%02d/%02d %02d:%02d:%02d\r\n", $SystemTime->year, $SystemTime->mon, $SystemTime->day, $SystemTime->hour, $SystemTime->min, $SystemTime->sec);
			echo "sync_type="   . $GLOBALS['system_conf']->SystemDatetime->Type . "\r\n";
			if ( $GLOBALS['system_conf']->SystemDatetime->Type == 0 )
			{	//sync with ntp
				echo "ntp_server="	. "0" . "\r\n";
				echo "ntp_addr="	. $GLOBALS['net_conf']->NTP->Address . "\r\n";
			}  	
		}
		else
		{
			show_post_ng();
		}
	}	
	catch(Exception $e)
	{	
		echo  "error_datetime";			
	}
}


//------------------------------------------------------------------------------------------------------
// 	Html
//------------------------------------------------------------------------------------------------------
if(isset($_REQUEST['submenu']))
{
  if ( $_REQUEST['submenu'] == 'datetime' )
	{
		if ( $_REQUEST['action'] == 'view' )
		{
			echo '<meta http-equiv="Refresh" content="0; URL=setup_system_date_time.cgi">';
		}
		exit;
	}
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------

if(isset($_REQUEST['msubmenu']))
{
	if ( $_REQUEST['msubmenu'] == 'datetime' )
	{
    header("Content-Type: text/plain");
    ob_end_clean();
	
		if ( $_REQUEST['action'] == 'view' )
		{
			datetime_view_post();
		}
		else
			show_post_ng();

		exit;
	}

	else if ( $_REQUEST['msubmenu'] == 'rtsp' )
	{
		if ( $_REQUEST['action'] == 'session_info' )
		{
      header("Content-Type: text/plain");
      ob_end_clean();
    		
			$shm_id = shmop_open(KEY_SM_RTSP_CONNECTIONS, "a", 0, 0);
			if (!$shm_id) exit;
			
			$data = shmop_read($shm_id, 0, 4);
			$rtsp_connections = unpack("i1count", $data);
	
			$index = 0;
			if ($rtsp_connections['count'] > 0)
			{
				for($i=0; $i<20; $i++)
				{
					$data = shmop_read($shm_id, 4 + ($i)*16, 16);
					$rtsp_connections[$index] = unpack("i1sock/i1addr/i1port/i1type", $data);
					$type = ($rtsp_connections[$index]['type'] == 0) ? "TCP" : "UDP";
					if ( $rtsp_connections[$index]['sock'] >= 0)
					{
						echo $index.' '.long2ip($rtsp_connections[$index]['addr']).' '.$rtsp_connections[$index]['port'].' '.$type."\r\n";
						$index++;
					}
				}
				echo $index."\r\n";
			}
			shmop_close($shm_id);	
			
			exit;
		}
		else if ( $_REQUEST['action'] == 'codec_info' )
		{
		  $profile_conf = new CProfileConfiguration();
		  echo  getChannelInfo($profile_conf);
		  exit;      
		}
	}	
}	
show_post_ng();

?>
