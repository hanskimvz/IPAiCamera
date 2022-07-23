<?
require('../_define.inc');
require('../class/capability.class');
require('../class/system.class');
require('../class/socket.class');
$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();

function getntpstatus($name){
	$file_path = '/root/ntpstat';
	if(file_exists($file_path)){
		$file_arr = file($file_path);
		foreach($file_arr as $v){
			$v = str_replace(array("\r\n","\r","\n"),'',$v);
			$data = explode('=',$v);
			echo $name."['".$data[0]."']='".$data[1]."';\r\n"; 
		}
		echo $name."['ntp_on_off']='".$GLOBALS['system_conf']->SystemDatetime->Type."';\r\n";
	}
}

function getsdcardstatus($name){
	$fs = exec("mount | grep root | awk '{print $5}' | cut -d '%' -f 1");

	if( $fs == "ext4" ){
		$sdcard="/dev/mmcblk1p1";
	}
	else{
		$sdcard="/dev/mmcblk0p1";
	}

	$insert_status = file_exists($sdcard);

	if($insert_status){
		$mount_status = exec("mount | grep $sdcard");
		if($mount_status){
			echo $name."['status']='2';\r\n";
		}
		else {
			echo $name."['status']='1';\r\n";
		}
	}
	else{
		echo $name."['status']='0';\r\n";
	}

	if($GLOBALS['system_caps']->is_proxy_camera)
	{
		$nfs1 = exec("mount | grep 'nfs1'| cut -d ' ' -f 3");
		if ($nfs1 === "/nfs1")
			echo $name."['status1']='2';\r\n";
		else
			echo $name."['status1']='1';\r\n";                                                                                           
		$nfs2 = exec("mount | grep 'nfs2'| cut -d ' ' -f 3");
		if ($nfs2 === "/nfs2")
			echo $name."['status2']='2';\r\n";
		else
			echo $name."['status2']='1';\r\n";                                                                                           
		$nfs3 = exec("mount | grep 'nfs3'| cut -d ' ' -f 3");
		if ($nfs3 === "/nfs3")
			echo $name."['status3']='2';\r\n";
		else
			echo $name."['status3']='1';\r\n";          
	}
}

?>
<!DOCTYPE html>
<html>
	<head>
		<title>system diagnostics</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false" >
		<div class="contentTitle"><span tkey="setup_system_diagnostics"></span></div>
		<div class="content" id="diag_content" style="line-height:20px;"></div>
		<br>
		<label class="caution" id="core_caution"></label>
		<center>
			 <button id="core_download" class="button"><span tkey="setup_download"></span></button>
		</center>
		<script>
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var SysInfo = new Object();
            var ntpInfo = new Object();
            var sdInfo = new Object();
            <?
                getntpstatus("ntpInfo");
                getsdcardstatus("sdInfo");
            ?>
		</script>
		<script src="./setup_system_diagnostics.js"></script>
	</body>
</html>
