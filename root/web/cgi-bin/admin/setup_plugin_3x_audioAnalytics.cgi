<?
require('../_define.inc');
?>

<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
<div id="recording">
 <div class="contentTitle"> Audio Analytics </span></div>
 <div class="content">
        <label class="maintitle"><span tkey="Impact Audio"></span></label>
	<div id="Impact Control">
		<br>
                <input type="checkbox" id="subAA_ImpactAudio" name="laAA_EnableImpactAudio" value='0'>
                <label for="subAA_ImpactAudio"></label>Enable<br>
		<br>
                <input type="checkbox" id="TriggerOutputOnImpactAudio" name="SessionTimeout" value='0'>
                <label for="TriggerOutputOnImpactAudio"></label>Active PIR Alarm LED<br>
        </div>

	<div id="import information">
            <label class="subtitle">Environmental&nbsp;Sensitivity</label>
            <div class="select"><select id="AA_EnvironmentalSensitivity">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10</option>
                        <option value="11">11</option>
                        <option value="12">12</option>
                        <option value="13">13</option>
                        <option value="14">14</option>
                        <option value="15">15</option>
	    </select></div>
	    <br>	
		
            <label class="subtitle">Total&nbsp;Power</label>
            <div class="select"><select id="AA_TotalPower">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10</option>
                        <option value="11">11</option>
                        <option value="12">12</option>
                        <option value="13">13</option>
                        <option value="14">14</option>
                        <option value="15">15</option>
	    </select></div>
         </div>
 </div>
 <div class="content">
        <label class="maintitle"><span tkey="Glass Break"></span></label>
	<div id="Glass Break">
		<br>
                <input type="checkbox" id="subAA_GlassBreak"" name="SessionTimeout" value='0'>
                <label for="subAA_GlassBreak""></label>Enable<br>
		<br>
                <input type="checkbox" id="TriggerOutputOnGlassBreak" name="SessionTimeout" value='0'>
                <label for="TriggerOutputOnGlassBreak"></label>Trigger output<br>
         </div>
 </div>

 <div class="content">
        <label class="maintitle"><span tkey="Self Test"></span></label>
	<div id="site information">
		<br>
                <input type="checkbox" id="AA_SelfTestEnable" name="SessionTimeout" value='0'>
                <label for="AA_SelfTestEnable"></label>Enable<br><br>
         </div>
 </div>

 <center>
         <button class="button" id="btOK"><span tkey="apply"></span></button>
 </center>


</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script src="./setup_plugin_3x_siteinfo.js"></script>
</html>


