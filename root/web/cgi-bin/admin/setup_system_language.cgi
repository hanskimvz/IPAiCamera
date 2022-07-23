<?
require('../_define.inc');
require('../class/system.class');
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);

//--- ip
function getlanguageInfo($name)
{	
	echo $name ."['language']="	  .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}

?>
<!DOCTYPE html>
<html>
<head>
	<title>Action Rule Contfiguration</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="Language"></span></div>
	<div id="record_index">
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<label class="subtitle"><span tkey="setup_language_country"></span></label>
			<div class="select">
				<select id="language"></select>
			</div>
		</div>
		<center>
			<button class="button" id="btOK"><span tkey="apply"></span></button>
		</center>
		<script>
			var languageInfo = new Object();
			<? 
				getlanguageInfo("languageInfo"); 
			?>
		</script>
	<script src="./setup_system_language.js"></script>
</body>
</html>
