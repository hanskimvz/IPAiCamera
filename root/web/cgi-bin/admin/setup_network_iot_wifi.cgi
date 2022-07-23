<?
require('../_define.inc');
require('../class/network.class');
require('../class/iot.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$iot_conf = new CWIFI($shm_id);
shmop_close($shm_id);

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
           		    <input id="sel_pw" type="password" class="short">
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

        <div class="content" >
            <label class="maintitle"><span tkey="setup_network_type"></span></label>

            <label class="subtitle">WiFi Status</label>
            <input id="connected" type="radio" value=0 name="ip_connected" disabled>
            <label for="connected"></label>connected
            <input id="notconnected" type="radio" value=1 name="ip_connected" disabled>
            <label for="notconnected"></label>not connected
	<div id="static_ip_setting">
            <label class="subtitle"><span tkey="setup_ipaddress"></span></label>
            <input id="wifi_ip" type="text" disabled><br>

            <label class="subtitle"><span tkey="setup_subnet_mask"></span></label>
            <input id="wifi_sm" type="text" disabled><br>

            <label class="subtitle"><span tkey="setup_default_gateway"></span></label>
            <input id="wifi_gw" type="text" disabled><br>
         </div>

		<center>
			<button id="refresh" class="button"><span tkey="setup_refresh"></span></button>
		</center>
	</div>
</body>

<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
        <script type="text/javascript">
		var IOTInfo = <? $GLOBALS['iot_conf']->getIOTInfoConf() ?>;
        </script>
<script src="./setup_network_iot_wifi.js"></script>
</html>


