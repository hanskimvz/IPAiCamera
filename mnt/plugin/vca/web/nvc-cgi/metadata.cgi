
<?
require('/root/web/cgi-bin/_define.inc');
require('/root/web/cgi-bin/class/system.class');
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
shmop_close($shm_id);
$TimezoneIndex = $system_conf->SystemDatetime->TimeZoneIndex;
$timezone = "Etc/GMT".($TimezoneIndex-12 >0 ? "-".strval($TimezoneIndex-12): "+".strval(12-$TimezoneIndex));
date_default_timezone_set($timezone);

//validate Get param
foreach($_GET as $key=>$val){
    $_GET[$key] = strtolower($val);
}
// print_r($_GET);
if ( !isset($_GET['fmt'])) {
    $_GET['fmt'] = 'json';
} 
// http://192.168.132.6/cgi-bin/operator/metadata.cgi?fmt=json

$filename = "/mnt/plugin/.config/vca-cored/configuration/api.json";
$json_str = file_get_contents($filename);
$arr = json_decode($json_str, true);
if (!$arr){
    $arr = array();
}

print "<pre>"; print_r($arr); print "</pre>";
$xml_str = '<?xml version="1.0"?>
<vca>
<schema_version></schema_version>
<vca_hdr>
<frame_id></frame_id>
<vca_status>0</vca_status>
<trk_mode>0</trk_mode>
</vca_hdr>
';


/*
<?xml version="1.0"?>
<vca>
<schema_version></schema_version>
<vca_hdr>
<frame_id>325299</frame_id>
<vca_status>0</vca_status>
<trk_mode>0</trk_mode>
</vca_hdr>
<vca_cfg>
<meaunits>metric</meaunits>
<cfg_update></cfg_update>
<detection_point></detection_point>
</vca_cfg>
<objects>
</objects>
<events>
</events>
<counts>
<count>
<id>3</id>
<name>Counter2</name>
<val>8573</val>
</count>
<count>
<id>2</id>
<name>Counter</name>
<val>0</val>
</count>
</counts>
</vca>
*/
?>