<?
require('../_define.inc');
require('../class/iot.class');
require('../class/socket.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$iot_conf = new CWIFI($shm_id);
shmop_close($shm_id);

function iot_wifi_get_scan_json()
{
    $log_raw_data = array();

    echo "[";
    exec("/bin/sh /root/wifi/wifi_scan.sh ");
    $data_str = file_get_contents('/root/wifi/wifi_scan_result.json');
    echo $data_str;
    echo "]";

}

function iot_wifi_connect($req_ssid, $req_pw)
{
    $cmd_buf =" /usr/local/bin/wifi_setup.sh sta nl80211 ".$req_ssid." ".$req_pw;
    echo $cmd_buf;	 	
    $handle = popen($cmd_buf, "r");
    while( $line = fgets($handle) )
    {
         echo $line;
    }
    pclose($handle);
    echo "Success";
}
function iot_wifi_status()
{
    $data_str = file_get_contents('/mnt/nand/pconf_iot_wifi.db');
    $json = json_decode($data_str, true);

    $wifi_arr = $json;  //array();

    $cmd_buf ="/sbin/ifconfig  wlan0 | awk -F'[ :]+' '/inet addr:/ {print $4}' ";
    $handle = popen($cmd_buf, "r");
    while( $line = fgets($handle) )
    {
	$line = str_replace(array("\r\n","\r","\n"),'',$line);
	if($wifi_arr["WIFIType"] == 1 )
		$wifi_arr["DynamicIpAddr"] = $line;
	else
		$wifi_arr["StaticIpAddr"] = $line;
    }
    $cmd_buf ="/sbin/ifconfig  wlan0 | awk -F'[ :]+' '/inet addr:/ {print $8}' ";
    $handle = popen($cmd_buf, "r");
    while( $line = fgets($handle) )
    {
        $line = str_replace(array("\r\n","\r","\n"),'',$line);
        $wifi_arr["SubnetMask"] = $line;
    }
    $cmd_buf =" route -n |grep wlan0  |awk 'NR==1{print $2}'  ";
    $handle = popen($cmd_buf, "r");
    while( $line = fgets($handle) )
    {
        $line = str_replace(array("\r\n","\r","\n"),'',$line);
        $wifi_arr["Gateway"] = $line;
    }

    $wifi_arr["ssid"] = $_REQUEST['ssid'];
    $wifi_arr["psk"] = $_REQUEST['pw'];
    	
    $filepath = "/mnt/nand/pconf_iot_wifi.db";
    $fp = fopen($filepath, 'w');
    fwrite($fp, json_encode($wifi_arr));
    fclose($fp);  

}

function iot_wifi_get_config_json()
{
	$filepath ="/mnt/nand/pconf_iot.db";
	if(file_exists($filepath))
	{
		$fd=fopen($filepath, "r", true);
		$buffer = fread($fd, filesize("/mnt/nand/pconf_iot.db"));
		if( $buffer != false)
		{
			$ex_buf = explode('}', $buffer);
			$buffer = $ex_buf[0]."}";
			//echo "[";
			echo $buffer;
			//echo json_encode($buffer);
			//echo "]";
		}
	}
}

//------------------------------------------------------------------------------------------------------
// 	Sdk
//------------------------------------------------------------------------------------------------------
header("Content-Type: text/plain");
if ($_REQUEST['msubmenu'] == 'wifi_setup' )
{
	if( $_REQUEST['action'] == 'scan_iot_wifi')
	{
		iot_wifi_get_scan_json();
	}
	else if( $_REQUEST['action'] == 'view')
	{
		echo $GLOBALS['iot_conf']->getIOTInfoConf();
	}
	else if( $_REQUEST['action'] == 'get_config')
	{
		iot_wifi_get_config_json();
	}
	else if( $_REQUEST['action'] == 'connect')
    	{
 	        $GLOBALS['iot_conf']->pir_tmp = 0;
		$GLOBALS['iot_conf']->ssid = $_REQUEST['ssid'];
		$GLOBALS['iot_conf']->psk = $_REQUEST['pw'];

	        $ipc_sock = new IPCSocket();
	        $ipc_sock->Connection($GLOBALS['iot_conf'], CMD_SET_IOT);
        	if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
            		show_post_ok();
        	} else {
            		show_post_ng();
            		echo "\r\nresult: ".$ipc_sock->dataInfo['ErrorCode']['value']."\r\n";
        	}
    	}
	else if( $_REQUEST['action'] == 'pir_clear')
        {
 	        $GLOBALS['iot_conf']->pir_count = 0;
 	        $GLOBALS['iot_conf']->pir_tmp = 1;

                $ipc_sock = new IPCSocket();
                $ipc_sock->Connection($GLOBALS['iot_conf'], CMD_SET_IOT);
                if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
                        show_post_ok();
                } else {
                        show_post_ng();
                        echo "\r\nresult: ".$ipc_sock->dataInfo['ErrorCode']['value']."\r\n";
                }
        }
	else if( $_REQUEST['action'] == 'pir_autoclear')
        {
		$GLOBALS['iot_conf']->pir_autoclear = $_REQUEST['autoclear'];
 	        $GLOBALS['iot_conf']->pir_count = 0;
 	        $GLOBALS['iot_conf']->pir_tmp = 1;

                $ipc_sock = new IPCSocket();
                $ipc_sock->Connection($GLOBALS['iot_conf'], CMD_SET_IOT);
                if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK) {
                        show_post_ok();
                } else {
                        show_post_ng();
                        echo "\r\nresult: ".$ipc_sock->dataInfo['ErrorCode']['value']."\r\n";
                }
        }
	exit;
}
else if ( $_REQUEST['msubmenu'] == 'wifi_state' )
{
	if ( $_REQUEST['action'] == 'view' )
	{
		echo '<meta http-equiv="Refresh" content="0; URL=setup_basic_ele_log.cgi">';
	}
	exit;
}

show_post_ng();
?>

