<?
require('../../../../../../root/web/cgi-bin/_define.inc');
require('../../../../../../root/web/cgi-bin/class/media.class');
require('../../../../../../root/web/cgi-bin/class/system.class');
$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$profile_conf = new CProfileConfiguration($shm_id);
$file = '../../../../../../root/web/cgi-bin/admin/vca/config/bia.conf';
shmop_close($shm_id);
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
  <div class="contentTitle"><span tkey="setup_vca_bia_config"></span></div>
  <div id="startVca" style="display:none;margin-left:4px;margin-bottom:2px;font-size:13px; color:#b90000;font-weight:600;"></div>
  <div class="content vcarules">
    <div class="maintitle"><span tkey="setup_vca_bias"></span></div>
    <div id="activation_ui">
      <label class="subtitle"><span tkey="vca_display"></span></label>
      <input type="radio" name="bia_enabled" value=1 id="bia_enabled_on"><label for="bia_enabled_on"></label><span tkey="on"></span>
      <input type="radio" name="bia_enabled" value=0 id="bia_enabled_off"><label for="bia_enabled_off"></label> <span tkey="off"></span><br>
      
      <label class="subtitle"><span tkey="vca_display_bia_on"></span></label>
      <input type="radio" value="0" name="bia" id="main_stream" ><label for="main_stream"></label><span class="c_title" tkey="setup_main_stream"></span>
      <input type="radio" value="1" name="bia" id="sub_stream" ><label for="sub_stream"></label><span class="c_title" tkey="setup_sub_stream"></span>
      <input type="radio" value="2" name="bia" id="third_stream" ><label for="third_stream"></label><span class="c_title" tkey="setup_third_stream"></span><br>

      <!-- <label class="subtitle"><span tkey="vca_blob"></span></label>
      <input type="radio" name="blob_enabled" value=1 id="blob_enabled_on"><label for="blob_enabled_on"></label><span tkey="on"></span>
      <input type="radio" name="blob_enabled" value=0 id="blob_enabled_off"><label for="blob_enabled_off"></label> <span tkey="off"></span><br> -->
      <div id="bia_caution" style="margin:4px 10px;font-size:11px; color:#727272;"></div>
    </div>
  </div>
  <div id="biaSetup" class="content">
    <div class="maintitle"><span tkey="bia_settings"></span></div>
    <div id="activation_ui">
      <label class="subtitle"><span tkey="display_zone"></span></label>
      <input type="radio" name="display_zones" value=1 id="display_zones_on"><label for="display_zones_on"></label><span tkey="on"></span>
      <input type="radio" name="display_zones" value=0 id="display_zones_off"><label for="display_zones_off"></label> <span tkey="off"></span><br>
      
      <label class="subtitle"><span tkey="display_object"></span></label>
      <input type="radio" name="display_objects" value=1 id="display_objects_on"><label for="display_objects_on"></label><span tkey="on"></span>
      <input type="radio" name="display_objects" value=0 id="display_objects_off"><label for="display_objects_off"></label> <span tkey="off"></span><br>

      <div id="objectContent">
        <div id="obj_OT_only_content">
          <label class="subtitle"><span tkey="obj_classification"></span></label>
          <input type="radio" name="obj_classifications" value=1 id="obj_classifications_on"><label for="obj_classifications_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_classifications" value=0 id="obj_classifications_off"><label for="obj_classifications_off"></label> <span tkey="off"></span>
          <span class="c_title" id="start_cali_mes" tkey="start_cali" ></span><br>

          <label class="subtitle"><span tkey="obj_height"></span></label>
          <input type="radio" name="obj_heights" value=1 id="obj_heights_on"><label for="obj_heights_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_heights" value=0 id="obj_heights_off"><label for="obj_heights_off"></label> <span tkey="off"></span><br>

          <label class="subtitle"><span tkey="obj_speed"></span></label>
          <input type="radio" name="obj_speeds" value=1 id="obj_speeds_on"><label for="obj_speeds_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_speeds" value=0 id="obj_speeds_off"><label for="obj_speeds_off"></label> <span tkey="off"></span><br>

          <label class="subtitle"><span tkey="obj_area"></span></label>
          <input type="radio" name="obj_areas" value=1 id="obj_areas_on"><label for="obj_areas_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_areas" value=0 id="obj_areas_off"><label for="obj_areas_off"></label> <span tkey="off"></span><br>
        </div>
  
        <label class="subtitle"><span tkey="obj_ID"></span></label>
        <input type="radio" name="obj_id" value=1 id="obj_ID_on"><label for="obj_ID_on"></label><span tkey="on"></span>
        <input type="radio" name="obj_id" value=0 id="obj_ID_off"><label for="obj_ID_off"></label> <span tkey="off"></span><br>

        <div id="obj_confidence" style="display: none;">
          <label class="subtitle"><span tkey="obj_confidence"></span></label>
          <input type="radio" name="confidence" value=1 id="obj_confidence_on"><label for="obj_confidence_on"></label><span tkey="on"></span>
          <input type="radio" name="confidence" value=0 id="obj_confidence_off"><label for="obj_confidence_off"></label> <span tkey="off"></span><br>
        </div>

        <div id="obj_dwell_time">
          <label class="subtitle"><span tkey="obj_dwell_time"></span></label>
          <input type="radio" name="obj_dwell_time" value=1 id="obj_dwell_time_on"><label for="obj_dwell_time_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_dwell_time" value=0 id="obj_dwell_time_off"><label for="obj_dwell_time_off"></label> <span tkey="off"></span><br>
        </div>

        <div id="objectColorContent">
          <label class="subtitle"><span tkey="obj_color"></span></label>
          <input type="radio" name="obj_color" value=1 id="obj_color_on"><label for="obj_color_on"></label><span tkey="on"></span>
          <input type="radio" name="obj_color" value=0 id="obj_color_off"><label for="obj_color_off"></label> <span tkey="off"></span><br>
        </div>
      </div>
      
      <label class="subtitle"><span tkey="display_eve_mes"></span></label>
      <input type="radio" name="display_eve_mesg" value=1 id="display_eve_mesg_on"><label for="display_eve_mesg_on"></label><span tkey="on"></span>
      <input type="radio" name="display_eve_mesg" value=0 id="display_eve_mesg_off"><label for="display_eve_mesg_off"></label> <span tkey="off"></span><br>

      <label class="subtitle"><span tkey="display_sys_mes"></span></label>
      <input type="radio" name="display_sys_mesg" value=1 id="display_sys_mesg_on"><label for="display_sys_mesg_on"></label><span tkey="on"></span>
      <input type="radio" name="display_sys_mesg" value=0 id="display_sys_mesg_off"><label for="display_sys_mesg_off"></label> <span tkey="off"></span><br>

      <label class="subtitle"><span tkey="display_line_counter"></span></label>
      <input type="radio" name="display_line_counters" value=1 id="display_line_counters_on"><label for="display_line_counters_on"></label><span tkey="on"></span>
      <input type="radio" name="display_line_counters" value=0 id="display_line_counters_off"><label for="display_line_counters_off"></label> <span tkey="off"></span><br>

      <label class="subtitle"><span tkey="display_counter"></span></label>
      <input type="radio" name="display_counters" value=1 id="display_counters_on"><label for="display_counters_on"></label><span tkey="on"></span>
      <input type="radio" name="display_counters" value=0 id="display_counters_off"><label for="display_counters_off"></label> <span tkey="off"></span><br>
    </div>
  </div>
  <center>
    <button id="btOK"  class="button" ><span tkey="apply"></span></button>
  </center>
  <script>
    var VideoInfo = <? getChannelInfo($GLOBALS['profile_conf']); ?>
  </script>
  <script src="/cgi-bin/admin/vca/bia/setup_vca_bia.js"></script>
</body>
</html>