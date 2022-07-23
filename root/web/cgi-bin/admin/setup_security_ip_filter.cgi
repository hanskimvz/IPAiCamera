<?
require('../_define.inc');
require('../class/system.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration();
$filter_conf = $system_conf->Security->IpFilter;
shmop_close($shm_id);

?>
<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	</head>
	<body>
		<div class="contentTitle" id="ip_filter_title"></div>
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<div id="ip_address_filter_div">
				<label class="subtitle"><span tkey="ip_address_filter"></label>
				<input type="radio" name="enabled" value="1" id="enable">
				<label for="enable"></label><span tkey="on"></span>
				<input type="radio" name="enabled" value="0" id="disable">
				<label for="disable"></label><span tkey="off"></span><br>
			</div>
			<div id="cyber_vigilant_div" style="display:none;line-height:30px;">
				<input type="checkbox" id="enabled" name="enabled" value="1" ></td>
				<label for="enabled"></label><span tkey="cyber_vigilant_enable"></span><br>
			</div>
			<div id="ip_filter_type">
			<label class="subtitle"><span tkey="setup_ip_filter_type"></span></label>
				<div class="select">
					<select id="type">
						<option value="0" tkey="setup_allow"></option>
						<option value="1" tkey="setup_deny"></option>
					</select>
				</div><br>
			</div>
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>
		<div class="content">
			<label class="maintitle" id="filtered_ip_addresss"></label>	
			<div class="result_table">
				<table class="result_filed">
					<thead class="record_thead">
						<tr class="headline">
							<th tkey="setup_ipaddress"></th>
						</tr>
					</thead>
					<tbody id="result_table_1">
					</tbody>
				</table>
			</div>
		</div>
		<div class="content">
			<label class="subtitle" tkey="setup_ipaddress"></label>
			<input type="text" id="address" />
			<label> [ <span id="address_status"></span> ]</label><br>
		</div>
		<center>
			<button id="btAdd" class="button" tkey="setup_add"></button>
			<button id="btRemove" class="button" tkey="setup_remove"></button>
			<button id="btRemoveAll" class="button" tkey="setup_remove_all"></button> 
		</center>
	</body>
	

	<script>
		var filterInfo = <? show_ip_filter($GLOBALS["filter_conf"], true); ?>;
		var ip = '<? echo $_SERVER['REMOTE_ADDR']; ?>';
	</script>
	<script src="./setup_security_ip_filter.js"></script>
</html>
