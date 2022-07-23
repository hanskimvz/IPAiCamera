<?
$max_roll_over_count = 1440*90; // 90days

require('/root/web/cgi-bin/_define.inc');
require('/root/web/cgi-bin/class/system.class');
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
shmop_close($shm_id);
$TimezoneIndex = $system_conf->SystemDatetime->TimeZoneIndex;
$timezone = "Etc/GMT".($TimezoneIndex-12 >0 ? "-".strval($TimezoneIndex-12): "+".strval(12-$TimezoneIndex));
date_default_timezone_set($timezone);

Header('Content-type: text/json; charset=UTF-8');
// cgi-bin/admin/vca-api/api.json
$filename = "/mnt/plugin/.config/vca-cored/configuration/api.json";
$filedb = "/mnt/plugin/.config/vca-cored/configuration/countreport.db";

if (!file_exists($filedb)) {
    file_put_contents($filedb,"");
}
$db_body = file_get_contents($filedb);
$arr_rs = json_decode($db_body, true);
if(!$arr_rs) {
	$arr_rs = array();
}

$json_body = file_get_contents($filename);
$arr = json_decode($json_body, true)['observables'];

// print_r($arr);
$timestamp = time();
$datetime = date("Y-m-d H:i:00", $timestamp);
$timestamp = strtotime($datetime);

array_push($arr_rs, ["timestamp"=>$timestamp, "datetime"=>$datetime, "counters"=>[]]);
$n = sizeof($arr_rs) -1;
if ($n>$max_roll_over_count){
    $arr_rs = array_shift($arr_rs);
}
for ($i=0; $i<sizeof($arr); $i++) {
	if ($arr[$i]['typename'] == 'vca.observable.Counter') {
		// array_push($arr_rs, ["timestamp"=>$timestamp, "datetime"=>$datetime, "idx"=>$i, "name"=>$arr[$i]['name'], "value"=>$arr[$i]['count']]);
		array_push($arr_rs[$n]['counters'], ["idx"=>$i, "name"=>$arr[$i]['name'], "value"=>$arr[$i]['count']]);
		// $arr_rs[$n][$arr[$i]['name']] = $arr[$i]['count'];
	}
}

// print_r($arr_rs);
$json_body = json_encode($arr_rs);
file_put_contents($filedb, $json_body);

// excute
// /usr/bin/php-cgi /mnt/plugin/mk_ct_report.cgi

// crontab -e
// * * * * * /usr/bin/php-cgi /mnt/plugin/mk_ct_report.cgi
?>