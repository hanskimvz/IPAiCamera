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
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
 <link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
 <link rel="stylesheet" href="/css/dom.css" type="text/css" />  
 <? DependencyOem(); ?>


  <title>Session time-out</title>
 </head>
 <body>
 <div style="width:auto; height:auto; text-align:center; vertical-align:middle;">
 <div style="margin:230px;">
<?
if(isset($_REQUEST['value']) ){	
    if($_REQUEST['value']=="firstpass" ){
?>
         <h1><span tkey="admin_password_change_msg"></span></h1>
<?
    }else if($_REQUEST['value']=="logout_btn"){
?>		
         <h1><span tkey="logout_msg"></span></h1>
<?
    }else if($_REQUEST['value']=="session_time_out"){
?>
        <h1><span tkey="signed_out_msg"></span></h1>
<?
    }
}else{
}
?>

<h1><span id="re_login_msg" tkey="re_login_msg"></span></h1>
<h1><span id="login_again_msg" tkey="login_again_msg"></span></h1>
  		<button id="re_login_btn" class="button" tkey="re_login_btn" onClick="location.href='./index.cgi'"></button>
  		<button id="login_btn" class="button" tkey="login_btn" onClick="location.href='./index.cgi'"></button>
	</div>
 </div>

	<script >
			var gLanguage;
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			<? getLangSetup("gLanguage"); ?>
	</script>	
  	<script defer src="/js/jquery1.11.1.min.js"></script>
  	<script defer src="/js/less.min.js"></script>		
    <script defer src="/js/jqueryui.js"></script>  
    <script src="/js/lang.js"></script> 
    <script src="/js/page.js"></script> 
    <script defer src="./logout.js"></script>	
    <script defer src="/js/jquery.cookie.js"></script>	    
</body>

</html>

