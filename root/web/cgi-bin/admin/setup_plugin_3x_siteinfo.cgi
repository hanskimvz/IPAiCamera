<?
require('../_define.inc');
?>

<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
<div id="recording">
 <div class="contentTitle"> Site Information </span></div>
 <div class="content">
        <label class="maintitle"><span tkey="Site Information"></span></label>
	<div id="site information">
            <label class="subtitle"><span tkey="CompanyName"></span></label>
            <input id="CompanyName" type="text"><br>
            <label class="subtitle"><span tkey="SiteName"></span></label>
            <input id="SiteName" type="text"><br>
            <label class="subtitle"><span tkey="CameraName"></span></label>
            <input id="CameraName" type="text"><br>
            <label class="subtitle"><span tkey="AliasName"></span></label>
            <input id="AliasName" type="text"><br>
         </div>
	<center>
		<button id="refresh" class="button"><span tkey="setup_refresh"></span></button>
		<button id="btOK2" class="button"><span tkey="apply"></span></button>
	</center>
 </div>
 <div class="content">	
	<label class="maintitle"><span tkey="Port Information"></span></label>
	 <div id="port information">
            <label class="subtitle"><span tkey="setup_language_country"></span></label>
            <div class="select"><select id="VigilDataPort">
                        <option value="22801">22801</option>
                        <option value="22851">22851</option>
                        <option value="22901">22901</option>
                        <option value="22951">22951</option>
                        <option value="23001">23001</option>
                        <option value="23051">23051</option>
                        <option value="23101">23101</option>
                        <option value="23151">23151</option>
                        <option value="23201">23201</option>
                        <option value="23251">23251</option>
                        <option value="23301">23301</option>
                        <option value="23351">23351</option>
                        <option value="23401">23401</option>
                        <option value="23451">23451</option>
                        <option value="23501">23501</option>
                        <option value="23551">23551</option>
	    </select></div>
	    <button id="btAdd" class="button half"><span tkey="apply"></span></button>	
	    <br>

            <label class="subtitle"><span tkey="setup_language_country"></span></label>
            <div class="select"><select id="VigilDataPort">
                        <option value="0">Automatic</option>
                        <option value="80">80</option>
                        <option value="443">443</option>
	    </select></div>
	    <button id="btAdd" class="button half"><span tkey="apply"></span></button>	
	    <br>
	    	
         </div>

 </div>
</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script src="./setup_plugin_3x_siteinfo.js"></script>
</html>


