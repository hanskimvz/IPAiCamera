<?
require('../../../../../../root/web/cgi-bin/_define.inc');
require('../../../../../../root/web/cgi-bin/class/media.class');
require('../../../../../../root/web/cgi-bin/class/system.class');
$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$profile_conf = new CProfileConfiguration($shm_id);
$system_conf = new CSystemConfiguration();
shmop_close($shm_id);
$file = '../config/tracking_engine.conf';
if (isset($_POST['newData'])) {
  $updatedData = $_POST['newData'];
  file_put_contents($file, $updatedData);
}
?>
<!DOCTYPE html><html>
<head>
<title>Burnt-in Annotation Configuration</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
  <div class="contentTitle"><span tkey="setup_vca_enable_config"></span></div>
  <div id="checkDepen" style="display:none;margin-left:4px;margin-bottom:2px;font-size:13px; color:#b90000;font-weight:600;"></div>
  <div id="startVca" style="display:none;margin-left:4px;margin-bottom:2px;font-size:13px; color:#b90000;font-weight:600;"></div>
  <div class="content vcarules">
    <div class="maintitle"><span tkey="setup_vca_enable"></span></div>
    <div id="activation_ui">
      <label class="subtitle"><span tkey="vca_activation"></span></label>
      <input type="radio" name="vca_enabled" value=1 id="vca_enabled_on"><label for="vca_enabled_on"></label><span tkey="on"></span>
      <input type="radio" name="vca_enabled" value=0 id="vca_enabled_off"><label for="vca_enabled_off"></label> <span tkey="off"></span><br>
    </div>
  </div>
  <div class="content" id="selEngine_content" style="display: block;">
    <div class="maintitle"><span tkey="setup_vca_enable_tracker_engine"></span></div>
    <div id="select_engine" style="padding-left:10px">
      <input type="radio" name="tracker_engine" value=0 id="tracker_engine_OT"><label for="tracker_engine_OT"></label><span id="span_tracker_engine_OT" tkey="setup_vca_enable_tracker_engine_OT"></span><br>
      <input type="radio" name="tracker_engine" value=1 id="tracker_engine_DL_OT"><label for="tracker_engine_DL_OT"></label><span id="span_tracker_engine_DL_OT" tkey="setup_vca_enable_tracker_engine_DLOT"></span><br>
      <input type="radio" name="tracker_engine" value=2 id="tracker_engine_DL_PT"><label for="tracker_engine_DL_PT"></label><span id="span_tracker_engine_DL_PT" tkey="setup_vca_enable_tracker_engine_DLPT"></span><br>
    </div>
    <span style="display: inline-block; margin:4px 10px; font-size:11px; color:red;" tkey="setup_vca_enable_engine_caution"></span>
  </div>
  <center>
    <button id="btOK"  class="button" ><span tkey="apply"></span></button>
  </center>
  <script>
    var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>;
    var fwInfo;
		<?
		echo "fwInfo='". trim($system_conf->DeviceInfo->BuildVersion)."_". trim($system_conf->DeviceInfo->FirmwareVersion)."';\r\n;";
		?>
  </script>
  <script src="/cgi-bin/admin/vca/enable/setup_vca_enable.js"></script>
</body>
</html>