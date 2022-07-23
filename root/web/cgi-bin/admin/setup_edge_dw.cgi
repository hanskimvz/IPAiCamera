<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html>
	<head>
		<title></title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle">
			<span tkey="setup_spectrum_edge"></span>
		</div>
		<div class="content">
			<label class="maintitle" tkey="setup_version"></label>
			<pre id="dwedge_version" class="dwedge_msg">

			</pre>
			<label class="maintitle" tkey="setup_status"></label>
			<pre id="dwedge_status" class="dwedge_msg">

			</pre>
			<label class="subtitle" tkey="setup_spectrum_edge_install"></label>
			<div id="file" class="filebox disign_sel">
				<input type="file" name="FileInput" id="FileInput" />
				<label for="FileInput" tkey="setup_system_selectfile" ></label>
			</div><br>
			<div id="progressbox" >
				<div id="progressbar" class="stripes"></div >
				<div id="progress_text"></div>
				<div id="statustxt"></div>
			</div>
			<div name="installed">
				<label class="maintitle" tkey="setup_edge_control"></label>
				<button id="update" class="button" tkey="setup_update" disabled></button><br>
				<button id="start" class="button" tkey="setup_start" value="start"></button>
				<button id="stop" class="button" tkey="setup_stop" value="stop"></button><br>
				<button id="restart" class="button" tkey="restart" value="restart"></button>
				<button id="remove" class="button" tkey="setup_remove" value="remove"></button><br>
			</div>
		</div>
		<center name="notInstalled">
			<button id="install" class="button" tkey="setup_install"></button>
		</center>
	</body>
	<script src="/cgi-bin/admin/setup_edge_dw.js"></script>
</html>
