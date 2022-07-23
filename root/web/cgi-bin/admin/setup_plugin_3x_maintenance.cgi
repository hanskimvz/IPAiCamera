<?
require('../_define.inc');
?>

<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
<div id="recording">
 <div class="contentTitle"> Main Tenance</div>
 <div class="content">
        <label class="maintitle"><span tkey="Reboot"></span></label>
	<div id="Reboot">
	<button id="btAdd" class="button half"><span tkey="reboot"></span></button>
        <label class="subtitle">Reboot the device.</label>
	</div>
 </div>
		
 <div class="content">

        <label class="maintitle"><span tkey="Reset Camera Settting"></span></label>
         <div id="port information">
            <label class="subtitle">Recording configuration</label>
            <div class="select"><select id="ResetConfiguration">
                        <option value="default" >Default</option>
                        <option value="highresolution">High Resolution</option>
            </select></div>
            <button id="btAdd" class="button half"><span tkey="apply"></span></button>
            <br>
         </div>
        <br>
  </div> 	

 <div class="content">
	<label class="maintitle"><span tkey="Registation"></span></label>
	 <div id="registration">
            <label class="subtitle">Unregistered Modules</label>
            <div class="select"><select id="UnregisteredList">
	    </select></div>
	    <br>
	    <label class="subtitle">Registration Key</label>
	    <input id="RegisterKey" class="text" type="text" disabled="disabled">	

	    <button id="btAdd" class="button half"><span tkey="register"></span></button>	
	    <br>
	    	
         </div>
 </div>

</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script src="./setup_plugin_3x_maintenance.js"></script>
</html>


