<?
require('../_define.inc');
require('../class/system.class');
require('../class/media.class');
require('../class/capability.class');
require('../class/network.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$profile_conf = new CProfileConfiguration();
shmop_close($shm_id);

// print md5('hanskim:IP Camera:Wjdtjd12'); // a547e14a09d7b7a9fe0bcdb75a2099b
// print '</br>'; 
// print md5('user:IP Camera:pass'); // b4fdcc5685399b08e8607d4122e5982c

//print "<pre>"; print_r($GLOBALS['system_conf']->DeviceInfo); print "</pre>";
//$GLOBALS['system_conf']->DeviceInfo->Manufacturer='VCANICE';

//print "<pre>"; print_r($GLOBALS['system_conf']); print "</pre>";
$get_oem = $system_caps->getOEM();

function getRTSPPort($name)
{
	echo $name . "=" .$GLOBALS['net_conf']->Protocols->Protocol[1]->Port.";\r\n";
}
function getLangSetup($name)
{
    echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
check_connection_policy_with_authority($system_conf);
?>
<!DOCTYPE html>
<html class="setup_html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
	<meta name="google" content="notranslate" />
	<title>Administrator Tool</title>
	<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
	
	<link rel="stylesheet" href="/css/dom.css" type="text/css" />	
	<link rel="stylesheet" href="/css/upload.css" type="text/css" />
	<link rel="stylesheet" href="/css/admin.css" type="text/css" />
	<? DependencyOem(); ?>
	<script src="/js/less.min.js" type="text/javascript"></script>
</head>
<!-- <body oncontextmenu='return false' ondragstart='return false' onselectstart='return false'> -->
<body>
	<div id="left_frame">
		<label id="logo"></label>
		<div id="sub_menu"></div>
	</div>
	<div id="tabs" name="tabs"></div>
</body>
<script>
	var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
    var devInfo = <? $GLOBALS['system_conf']->getDevInfo();?>;
	var VideoInputInfo = <? $GLOBALS['profile_conf']->VideoSourceConfigurations->getVideoSourceInfo(); ?>;
	var userInfo = new Object();
	var systemOption;
	var rtspPort;
	var gLanguage;
	var tdn;
	var cdsAdj;
	var timeFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->TimeFormat?>;
	var hourFormat=<?echo $GLOBALS['system_conf']->SystemDatetime->HourFormat?>;
	<?
	if($GLOBALS['get_oem'] == 19 || $GLOBALS['get_oem'] == 20 || $GLOBALS['get_oem'] == 21)
	{	
	   $GLOBALS['system_conf']->Users->getAccessUserInfo_x("userInfo");
	}
	else
	{
		$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
	}


	printf("var encodeVersion=%d;\r\n", $GLOBALS['system_conf']->Security->SystemService->EncodeVersion);
	getRTSPPort("rtspPort");
	getLangSetup("gLanguage");
	echo "systemOption=" . $GLOBALS['system_conf']->SystemOption . ";\r\n";
	echo "tdn='".$GLOBALS['system_conf']->DeviceInfo->TDN . "';\r\n";
	echo "cdsAdj='".$GLOBALS['system_conf']->DeviceInfo->CDS_ADJ . "';\r\n";
	
	//SYSTEM OPTION
	echo "var SYSTEM_OPTION_UI_FIXED_DATE_20160504=" . SYSTEM_OPTION_UI_FIXED_DATE_20160504 . ";\r\n";
	echo "var SYSTEM_OPTION_DW_EDGE=" . SYSTEM_OPTION_DW_EDGE. ";\r\n";
	?>
	var corridor_mode = <?echo $GLOBALS['system_conf']->Corridor->enabled?>;
</script>
<script src="/js/lang.js"></script>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/menu_config.js"></script>
<script src="/js/page.js"></script>
<script src="/js/jpeg.js"></script>
<script src="/js/vlc_v2.js"></script>
<script src="/js/local_rec.js"></script>
<script src="./setup_main.js"></script>
</html>

<script>
</script>