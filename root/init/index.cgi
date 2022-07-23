<?
require('./_define.inc');
require('./class/system.class');
require('./class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
shmop_close($shm_id);

function getLangSetup($name)
{
	echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
?>
<html>
	<head>
		<meta content="text/html; charset=utf-6" http-equiv="Content-Type">
		<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
		<meta name="google" content="notranslate">
		<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<title>IP Camera</title>
		<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
		<link rel="stylesheet" href="/css/dom.css" type="text/css" /> 
	    <? DependencyOem(); ?>
		<link rel="stylesheet" href="/css/popup.css" type="text/css" />

	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false" >
        <div id="passchcontent" class="content" style="width:700px; margin-top:10%; margin-left:25%;">
        	<center> 
			   <label class="title" id="admin_password"> <span tkey="admin_password"></span></label>
			   <label class="title" id="set_admin_password"> <span tkey="set_admin_password"></span></label>
			</center><br>
            <div class="secontent">
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
				<div id="meter_wrapper" style="width:350px;">
					<div id="meter"></div>
				</div>
				<label> [ <span id="pass_type"></span> ] </label><br>
			</div>
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
		?>
	</script>	
  	<script defer src="/js/jquery1.11.1.min.js"></script>
    <script src="/js/lang.js"></script> 
    <script src="/js/page.js"></script> 
    <script defer src="./index.js"></script>	
</html>
