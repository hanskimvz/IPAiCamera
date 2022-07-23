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
    	<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
       	<link rel="stylesheet" href="/css/dom.css" type="text/css" />	
    	<link rel="stylesheet" href="/css/upload.css" type="text/css" />
    	<link rel="stylesheet" href="/css/admin.css" type="text/css" />
		
		<? DependencyOem(); ?>	
		<link rel="stylesheet" href="/css/popup.css" type="text/css" />    
		<script defer src="/js/less.min.js"></script>	
	</head>
	<body class="passchbody" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false" style="width:100%;">
        <div id="passchcontent" class="content">
        	<center> 
			   <label class="title" id="admin_password"> <span tkey="admin_password"></span></label>
			   <label class="title" id="set_admin_password"> <span tkey="set_admin_password"></span></label>
			<br><br>
            <div id="passpopup" class="secontent">
		    	<label class="subtitle"><span tkey="setup_system_passwd"></span></label>
		    	<input id="m_pass" type="password" class="inputText"><br>
		    	<label class="subtitle"><span tkey="setup_system_verify"></span></label>
		    	<input id="m_pass_confirm" type="password" class="inputText"><br>
				<div id = "pass_hint_div">
					<label class="subtitle"><span tkey="setup_system_pass_hint"></span></label>
					<input id="m_pass_hint" type="text" class="inputText"><br>
				</div>
            </div>
			<div id="meter_wrapper_ui">
				<div id="meter_wrapper">
					<div id="meter"></div>
				</div>
				<label> [ <span id="pass_type"></span> ] </label><br>
			</div>
			</center>
			<br>
			<div class="content change_pass" id="msg_change_pass">
			</div>
			<div class="content change_pass" id="msg_change_pass_dw">
				<span tkey="pass_msg_dw"></span><br>
			</div>
    	    <center>
		    	<button id="change_pass" class="button"></button>    		
        		<button id="check_later" class="button"><span tkey="check_later"></span></button>  
    		</center>		
        </div>
	<script>
		var gLanguage;
        var userInfo = new Object();
		var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
		<?
			getLangSetup("gLanguage");
            //$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
		?>
	</script>	
  	<script defer src="/js/jquery1.11.1.min.js"></script>
  	<script defer src="/js/less.min.js"></script>		
    <script defer src="/js/jqueryui.js"></script>  
    <script src="/js/lang.js"></script> 
    <script src="/js/page.js"></script> 
    <script defer src="./popup_change_pass.js"></script>	
    <script defer src="/js/jquery.cookie.js"></script>	    
    </body>
</html>
    
    
