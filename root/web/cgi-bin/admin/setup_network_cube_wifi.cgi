<?
require('../_define.inc');
?>


<!DOCTYPE html>
<html>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
	<div id="recording">
		<div class="contentTitle">WI-FI Configure</span></div>
		<div class="content">
			<label class="maintitle">WI-FI Select</label>
			<div class="log_table">
				<table class="result_filed" >
					<thead class="record_thead" >
						<tr class="headline">
							<th class="qt">Index</th>
							<th class="qt">SSID</span></th>
							<th class="qt">SIG</th>
							<th class="qt">WPA</th>
						</tr>
					</thead>
					<tbody id="result_table">
					</tbody>
				</table>
			</div>
			<div class="content" id= "network_port">
		            <label  class="subtitle">Select SSID:</label>
           		    <input id="sel_ssid" type="text" class="short">
		            <label  class="subtitle">Password:</label>
           		    <input id="sel_pw" type="text" class="short">
		</div>

			<div id="pages" style="display:none">
				<div class="left">
					<button id="first_page" class="button"> << </button>
					<button id="prev_page" class="button"> < </button>
				</div>
				<div id="page_list"></div>
				<div class="right">
					<button id="next_page" class="button"> > </button>
					<button id="last_page" class="button"> >> </button>
				</div>
			</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
		</div>

        <div class="content">
            <label class="maintitle"><span tkey="setup_network_type"></span></label>
            <input id="static" type="radio" value=0 name="ip_type">
            <label for="static"></label><span tkey="static"></span>
            <input id="dhcp" type="radio" value=1 name="ip_type">
            <label for="dhcp"></label><span tkey="dynamic"></span>
	<div id="static_ip_setting">
            <label class="subtitle"><span tkey="setup_ipaddress"></span></label>
            <input id="wifi_ip" type="text"><br>

            <label class="subtitle"><span tkey="setup_subnet_mask"></span></label>
            <input id="wifi_sm" type="text"><br>

            <label class="subtitle"><span tkey="setup_default_gateway"></span></label>
            <input id="wifi_gw" type="text"><br>
         </div>

		<center>
			<button id="refresh" class="button"><span tkey="setup_refresh"></span></button>
			<button id="btOK2" class="button"><span tkey="apply"></span></button>
		</center>
	</div>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<script src="./setup_network_cube_wifi.js"></script>
</html>


