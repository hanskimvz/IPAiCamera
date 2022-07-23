<?
require('../_define.inc');
require('../class/system.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);

//--
function getInfo($name)
{		
	echo $name."['dst_enable']="			.$GLOBALS['system_conf']->SystemDatetime->dst_enable.";\r\n";
	
	echo $name."['dst_start_mon']="	    .$GLOBALS['system_conf']->SystemDatetime->dst_start_mon.";\r\n";
	echo $name."['dst_start_ordinal']="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_ordinal.";\r\n";
	echo $name."['dst_start_week']="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_week.";\r\n";
	echo $name."['dst_start_hour']="	.$GLOBALS['system_conf']->SystemDatetime->dst_start_hour.";\r\n";

	echo $name."['dst_end_mon']="	    .$GLOBALS['system_conf']->SystemDatetime->dst_end_mon.";\r\n";
	echo $name."['dst_end_ordinal']="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_ordinal.";\r\n";
	echo $name."['dst_end_week']="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_week.";\r\n";
	echo $name."['dst_end_hour']="	.$GLOBALS['system_conf']->SystemDatetime->dst_end_hour.";\r\n";
	
	echo $name."['dst_bias']="	.$GLOBALS['system_conf']->SystemDatetime->dst_bias.";\r\n";
}
?>
<!DOCTYPE html>
<html>
<head>
	<title>Action Rule Contfiguration</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="Dst_Settings"></span></div>
	<div id="record_index">
		<div class="content">
			<label class="maintitle"><span tkey="setup_general_setting"></span></label>
			<input type="radio" value="0" name="dst_enable" id="enabled_off" >
			<label for="enabled_off"></label><span tkey="off"></span>
			<input type="radio" value="1" name="dst_enable" id="enabled_on" >
			<label for="enabled_on"></label><span tkey="on"></span><br>
			
		
		</div>
		<div class="content" id="dst_timecontent">
			<label class="maintitle"><span tkey="setup_dst_timesettings"></span></label>
			<label class="subtitle"><span tkey="setup_dst_startime"></span></label>				
			<div class="select width_50">
				<select id="dst_start_mon" class="width_50">
				</select>
			</div>
			<div class="select width_70">
				<select id="dst_start_ordinal" class="width_70">
				</select>
			</div>
			<div class="select width_60">
				<select id="dst_start_week" class="width_60">
				</select>
			</div>
			<div class="select width_50">
				<select id="dst_start_hour" class="width_50">
				</select>
			</div><span class="dstmargin" tkey="setup_dst_clock"></span><br>
			
			<label class="subtitle"><span tkey="setup_dst_endtime"></span></label>		
			<div class="select width_50">
				<select id="dst_end_mon" class="width_50">
				</select>
			</div>
			<div class="select width_70">
				<select id="dst_end_ordinal" class="width_70">
				</select>
			</div>
			<div class="select width_60">
				<select id="dst_end_week" class="width_60">
				</select>
			</div>
			<div class="select width_50">
				<select id="dst_end_hour" class="width_50">
				</select>
			</div><span class="dstmargin" tkey="setup_dst_clock"></span><br>
			
<!--		<label class="subtitle"><span tkey="setup_dst_baistime"></span></label>	
			<div class="select width_60">
				<select id="dst_bias" class="width_60">
				</select>
			</div><br>	 -->
		</div>
				
		<center>
			<button class="button" id="btOK"><span tkey="apply"></span></button>
		</center>
		<script>
			var dstInfo = new Object();

			<? 

				getInfo("dstInfo"); 
			?>
		</script>
		<script src="./setup_system_dst.js"></script>
</body>
</html>
