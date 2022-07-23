<?
require('../_define.inc');
require('../class/event.class');

$event_conf = new CEventConfiguration();

//--- ip
function getTransferInfo($name)
{	
	echo  $name."['mode']="          . $GLOBALS['event_conf']->transfer_conf->mode          . "\r\n";
	echo  $name."['image_num']="     . $GLOBALS['event_conf']->transfer_conf->numofimg      . "\r\n";
	echo  $name."['pre_duration']="  . $GLOBALS['event_conf']->transfer_conf->preduration   . "\r\n";
	echo  $name."['post_duration']=" . $GLOBALS['event_conf']->transfer_conf->postduration  . "\r\n";
	echo  $name."['max_img_enable']="     . $GLOBALS['event_conf']->transfer_conf->maxImgEnabled . "\r\n";
	echo  $name."['max_img_cnt']="  . $GLOBALS['event_conf']->transfer_conf->maxImgCnt     . "\r\n";
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>smtp settings</title>
	</head>

	<body onload="onLoadPage();" oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_transfer_config"></span>
			<div class="contentNotice margin_top_10">
				<span class="caution" tkye="setup_notice"></span>
				<ul class="padding_left30">
					<li><span tkey="setup_trasfer_message1"></span></li>
					<li><span tkey="setup_trasfer_message2"></span></li>
					<li><span tkey="setup_trasfer_message3"></span></li>					
				</ul>
			</div> 
		</div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_prepost_alarm_image"></span></label>				
<!--
			<div class="select short" >
				<select class="short" id="image_num">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="5">5</option>
				</select>
			</div>
-->
			<label class="subtitle"><span tkey="setup_transition_imagenumber"></span></label>
			<input type="number" id="image_num" class="short" max="5"><span tkey="setup_image_per_seconds""></span> [ 1 ~ 5 ]<br>
								
			<label class="subtitle"><span tkey="setup_pre_alarm_duration"></span></label>
			<input type="number" id="pre_duration" class="short" max="30" ><span tkey='setup_transfer_sec'></span> [ 1 ~ 5 ]<br>
								
			<label class="subtitle"><span tkey="setup_post_alarm_duration"></span></label>
			<input type="number" id="post_duration" class="short" max="30"><span tkey="setup_transfer_sec"></span> [ 1 ~ 30 ]<br>	 

			<label class="subtitle"><span tkey="setup_max_numofimg"></span></label>
			<input type="number" id="max_img_cnt" class="short" min="5" max="1000">
			<input type="checkbox" id="max_img_enable" name="max_img_enable"/><label for="max_img_enable"></label> [ Default:Off, 5 ~ 1000 ] <span tkey="setup_smtp_only"></span><br>
		</div>

		<center>
			<button id="btOK" class="button" tkey="apply">Apply</button>
		</center>
		<script type="text/javascript">
			var TransferInfo = new Object();
		<? 
				getTransferInfo("TransferInfo"); 
		?>
		</script>
	    <script src="./setup_transfer_transfer_setup.js"></script> 
	</body>
</html>
