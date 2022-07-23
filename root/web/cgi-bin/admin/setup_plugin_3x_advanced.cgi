<?
require('../_define.inc');
?>

<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
<div id="recording">
 <div class="contentTitle"> Advance Settings </span></div>
 <div class="content">

        <label class="maintitle"><span tkey="LED Control"></span></label><br>
	<div id="LED Control">
		<input type="checkbox" id="ch0" name="SessionTimeout" value='0'>
		<label for="ch0"></label>Show Armed Status<br><br>
		<input type="checkbox" id="ch1" name="SessionTimeout" value='0'>
		<label for="ch1"></label>Activat PIR Alarm LED<br>
	</div>
  </div>

 <div class="content">

        <label class="maintitle"><span tkey="UPnP Control"></span></label><br>
        <div id="upup conftrol">
		<input type="checkbox" id="ch2" name="Enable UPnP" value='0'>
		<label for="ch2"></label>Enable UPnP<br>
        </div>
        <br>
</div>
	<center>
	       <button class="button" id="btOK"><span tkey="apply"></span></button>
        </center>

 </div>
</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script src="./setup_plugin_3x_advanced.js"></script>
</html>


