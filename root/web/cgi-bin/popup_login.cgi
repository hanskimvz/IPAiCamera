<?
require('_define.inc');
require('class/system.class');
require('class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
shmop_close($shm_id);
function getLangSetup($name)
{
	echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
		<meta name="google" content="notranslate">
		<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<title>IP Camera</title>
		<link rel="stylesheet" href="/css/dom.css" type="text/css" />
		<link rel="stylesheet" href="/css/popup.css" type="text/css" />    
		
		<? DependencyOem(); ?>	
		<script defer src="/js/less.min.js"></script>	
	</head>
	<body id="popupbody" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<span tkey="pass_warning1" class="warning"></span><br>
	<br><div class="popup">
		<span tkey="pass_warning2"></span>
	</div >
	<span class="popup" tkey="pass_day"></span>
	<input id="popupchk" type="checkbox" autocomplete="off">
	<label for="popupchk"></label>
    	<center>
			<button id="change_pass" class="button"><span tkey="change_pass"></span></button>    		
    		<button id="check_later" class="button"><span tkey="check_later"></span></button>  
		</center>		
	<script>
		var gLanguage;
		var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
		<?
			getLangSetup("gLanguage");
		?>
	</script>	
  	<script defer src="/js/jquery1.11.1.min.js"></script>
  	<script defer src="/js/less.min.js"></script>		
    <script defer src="/js/jqueryui.js"></script>  
    <script src="/js/lang.js"></script> 
    <script src="/js/page.js"></script> 
    <script defer src="./popup_login.js"></script>	
    <script defer src="/js/jquery.cookie.js"></script>	    
    </body>
</html>
    
    
