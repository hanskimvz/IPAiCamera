<!DOCTYPE html>
<html>
	<head>
		<title>default set</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="setup_system_defaultset"></span></div>
		<div class="content">
			<input type="radio" value="0" id="all" name="optResetOption" checked>
			<label for="all"></label><span tkey="setup_all"></span><br>
			<input type="radio" value="1" id='net' name="optResetOption">
			<label for="net"></label><span tkey="setup_system_exceptnetwork"></span><br>
			<input type="radio" value="2" id='cam' name="optResetOption">
			<label for="cam"></label><span tkey="setup_system_onlycamerasettings"></span><br>
		</div>
		<center>
			<button name="btOK" type="button" class="button" onclick="onClickApply();"><span tkey="apply"></span></button>
		</center>
		<script src="./setup_system_default_set.js"></script>
	</body>
</html>
