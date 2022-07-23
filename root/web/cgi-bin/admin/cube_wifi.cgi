<?
require('../_define.inc');

function cube_wifi_get_scan_json()
{
    $log_raw_data = array();

    echo "[";
    exec("/bin/sh /root/wifi/wifi_scan.sh ");
    $data_str = file_get_contents('/root/wifi/wifi_scan_result.json');
    echo $data_str;
    echo "]";


}

function cube_wifi_connect($req_ssid, $req_pw)
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
function cube_wifi_status()
{
    $data_str = file_get_contents('/mnt/nand/pconf_cube_wifi.json');
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
    	
    $filepath = "/mnt/nand/pconf_cube_wifi.json";
    $fp = fopen($filepath, 'w');
    fwrite($fp, json_encode($wifi_arr));
    fclose($fp);  

}


function cube_wifi_get_config_json()
{

	$filepath ="/mnt/nand/pconf_cube_wifi.json";
	if(file_exists($filepath))
	{
		$fd=fopen($filepath, "r", true);
		$buffer = fread($fd, filesize("/mnt/nand/pconf_cube_wifi.json"));
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
	if( $_REQUEST['action'] == 'scan_cube_wifi')
	{
		cube_wifi_get_scan_json();
	}
	else if( $_REQUEST['action'] == 'get_config')
	{
		cube_wifi_get_config_json();
	}
	else if( $_REQUEST['action'] == 'connect')
    	{
		$req_ssid = $_REQUEST['ssid'];
		$req_pw = $_REQUEST['pw'];
        	cube_wifi_connect($req_ssid, $req_pw);
		cube_wifi_status();
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

