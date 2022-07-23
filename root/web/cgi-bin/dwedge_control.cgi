<?
header("Content-Type: text/plain");
$media_server = "/etc/init.d/S99digitalwatchdog-mediaserver ";
if( isset($_REQUEST['action']) )
{
	if ( $_REQUEST['action'] == "status" )
	{
		if ( file_exists('/usr/local/apps/digitalwatchdog') )
		{
			echo "Spectrum Edge is installed\r\n";
			# these return 0 if servers are running
			system($media_server ." status", $ms);
			# if it is running then see if it is responsive yet
			if( $ms == 0 )
			{
				ob_start();
				$dw_port=system("netstat -ltpn 2>/dev/null | grep mediaserver | awk '{print $4}' | cut -d ':' -f 2", $ret);
				ob_clean();
				$cmd="wget -q -O - 'http://127.0.0.1:$dw_port/api/ping' 2> /dev/null";
				$handle=popen($cmd, 'r');
				if( $handle )
				{
					$data = fread($handle, 2048);
					if( preg_match('/[moduleGuid]|[pong]/', $data) > 0 )
						echo "server is alive\r\n";
					else
						echo "server is confused\r\n";
				} 
				else 
				{
					echo "server is initializing\r\n";
				}
				pclose($handle);
			}
		}
		else
			echo "Spectrum Edge is not installed\r\n";
	}
	else if ( $_REQUEST['action'] == 'start')
	{
		if( file_exists('/usr/local/apps/digitalwatchdog') )
		{
			system($media_server . " status &> /dev/null", $ret);
			if ( $ret  == 0 )
				echo "Spectrum Edge media server is already running\r\n";
			else
			{
				system($media_server . " start");
			}
		}
	}
	else if( $_REQUEST['action'] == 'restart')
	{
		# We have to redirect stdout and stderr else
		# this cgi won't close correctly since starting
		# exacq does something bad to those fd's
		ob_start();
		system($media_server . ' restart');
		ob_clean();
	}
	else if( $_REQUEST['action'] == 'stop' )
	{
		system($media_server . " " . $_REQUEST['action']);
	}
	else if( $_REQUEST['action'] == 'remove' )
	{
		ob_start();
		system($media_server . ' stop');
		echo "Removing Edge...\r\n";
		system('rm -rf /usr/local/apps/digitalwatchdog');
		echo "Done\r\n";
	}
	else if( $_REQUEST['action'] == 'version') 
	{
		if( file_exists('/usr/local/apps/digitalwatchdog/version.txt') )
		{
			system('cat /usr/local/apps/digitalwatchdog/version.txt') . "\r\n";
		}
		else
		{
			echo "unknown\r\n";
		}
	}
	else 
	{
		echo "Usage: $0 {start|stop|restart|status}";
	}
}
?>
