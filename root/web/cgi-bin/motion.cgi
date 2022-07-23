<?
ini_set('memory_limit', '1M');
require('./_define.inc');
require('./class/event_status.class');
require('./class/socket.class');

$event_alarm = new CEventAlarmStatus();

//--------------------------------------------------------------------------------------------
// Administrator, Operator 만 접근 가능


//--------------------------------------------------------------------------------
if(isset($_REQUEST['msubmenu']))
{
  if ($_REQUEST['msubmenu'] == 'motion') 
  {
	// deprecated
   	header("Content-type: text/plain"); 
  	show_post_ng();
  	exit; 	 
  	if ($_REQUEST['action'] == 'monitor')
  	{

  		$ipc_sock = new IPCSocket();
  		
  		header('Content-type: multipart/x-mixed-replace;boundary=motionboundary');
  
  		if(!strcmp(getBrowser(),"Internet Explorer"))	
  			echo str_pad('',4096);					
  
  		print "\r\n--motionboundary\r\n\r\n";
  		
  		$i=0;
  		
  		do
  		{
  			sleep(1);
  
  			$ipc_sock->Connection($GLOBALS['event_alarm'], CMD_GET_EVENT_STATUS, 0, 1);
  			
  			echo "motion=" . $GLOBALS['event_alarm']->Motion->Data->Value . "\r\n";
  			
  			print "\r\n--motionboundary\r\n\r\n";
  			
  			ob_flush();
  			flush();
  			
  			$i++;
  		} while(1);
  	
  		print "--motionboundary--\r\n";
  	}
  	else {
  		header("Content-type: text/plain");
		ob_end_clean();
  		show_post_ng();
  	}
  }
  else
  {
  	header("Content-type: text/plain");
  	show_post_ng();
  }
}
else
{
	header("Content-type: text/plain");
	show_post_ng();
}

?>
