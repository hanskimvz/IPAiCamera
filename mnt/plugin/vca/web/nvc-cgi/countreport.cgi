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
if ( !isset($_GET['reportfmt']) || !in_array($_GET['reportfmt'], ['csv', 'table', 'json','chart'])){
    print ("<br>Error: reportfmt in  ['csv', 'table', 'json','chart']");
    exit();
}
if (!isset($_GET['order']) || !in_array($_GET['order'], ['asc', 'ascending', 'desc','descending'])){
    print ("<br>Error: order in ['asc', 'ascending', 'desc','descending']");
    exit();
}
if( !isset($_GET['sampling']) ||  (strval(intval($_GET['sampling'])) !=  strval($_GET['sampling'])) ||($_GET['sampling']%60 !=0) ) {
    print ("<br>Error: sampling must be integer and multipled by 60, 1 minute intervaly");
    exit();
}
if (!isset($_GET['value']) || !in_array($_GET['value'], ['abs', 'diff'])){
    print ("<br>Error: value in ['abs', 'diff']");
    exit();
}


function datestrtotime($str){
    global $start;
    global $last;
    global $step;
    $arr = ['yesterday','today','now', "thisweek", "thismonth", "lastweek", "lastmonth"];
    $str = strtolower($str);
    foreach($arr as $arr) {
        if (!strncmp($arr, $str, strlen($arr))) {
            $offset = str_replace($arr, "",$str);
            if ($arr == "thisweek") {
                $arr = date("Y-m-d 00:00:00", strtotime("last sunday"));
            }
            else if ($arr == "lastweek") {
                $arr = date("Y-m-d 00:00:00", strtotime("last sunday")-3600*24*7);
            }            
            else if ($arr == "thismonth") {
                $arr = date("Y-m-d 00:00:00", strtotime("first day of this Month"));
            }
            else if ($arr == "lastmonth") {
                $arr = date("Y-m-d 00:00:00", strtotime("first day of last Month"));
            }
            $ts = strtotime(date("Y-m-d H:i:00", strtotime($arr)));

            $ts += intval($offset);
            $str = date("Y-m-d H:i:s", $ts);
            break;
            // return $ts;
        }
    }
    $ts = strtotime($str);
    if($start > $ts){
        $ts = $start;
    }
    if($last < $ts){
        $ts = $last;
    }
    $ts = strtotime(date("Y-m-d H:i:00", ceil($ts/$step)*$step));
    return $ts;
}


// http://192.168.132.6/cgi-bin/operator/countreport.cgi?reportfmt=csv&to=now-600&counter=active&sampling=600&order=Ascending&value=diff&from=today
$filedb = "/mnt/plugin/.config/vca-cored/configuration/countreport.db";

if (!file_exists($filedb)) {
    file_put_contents($filedb,"");
}
$db_body = file_get_contents($filedb);
$arr = json_decode($db_body, true);
if (!$arr){
    $arr = array();
}
// print "<pre>"; print_r($arr); print "</pre>";
$start = $arr[0]['timestamp'];
$last  = $arr[sizeof($arr)-1]['timestamp'];
// print $start."-".$last;
$counters = array();
$ct_names = array();
foreach($arr as $arr_rs){
    foreach($arr_rs['counters'] as $ct){
        if (!in_array($ct['name'],$ct_names)) {
            array_push($ct_names, $ct['name']);
        }
        $counters[$arr_rs['timestamp']][$ct['name']] = $ct['value'];
    }
}

for ($s=$start; $s<=$last; $s+=60){
    foreach($ct_names as $ct_name){
        if (!isset($counters[$s][$ct_name])){
            $counters[$s][$ct_name] = $counters[$s-60][$ct_name];
        }
    }
}



// print (date("Y-m-d H:i:s", strtotime("today")));


$arr_rs = array();
$step = $_GET['sampling'];
$ts_from = datestrtotime($_GET['from']);
$ts_to = datestrtotime($_GET['to']);

$duration = ceil(($ts_to - $ts_from) / $step);

// print "\n\rfrom: ".$ts_from.", ".date("Y-m-d H:i:s",$ts_from);
// print "\n\rto: ".$ts_to.", ".date("Y-m-d H:i:s",$ts_to);
// print "\n\rstep: ".$step;
// print "\n\rduration: ".$duration;

$arr_ts = array();
$arr_rs = array();
for ($i=-1; $i<$duration; $i++){
    $arr_ts[$i] = $ts_from + $step *$i;
    if ($i <0){
        continue;
    }
    foreach($ct_names as $ct_name){
        if (!isset($counters[$arr_ts[$i-1]][$ct_name])){
            $counters[$arr_ts[$i-1]][$ct_name] = $counters[$arr_ts[$i]][$ct_name];
        }
        if($_GET['value'] == 'abs') {
            $arr_rs[$arr_ts[$i]][$ct_name] = $counters[$arr_ts[$i]][$ct_name];
        }
        else {
            $arr_rs[$arr_ts[$i]][$ct_name] = $counters[$arr_ts[$i]][$ct_name] - $counters[$arr_ts[$i-1]][$ct_name];
        }
    }
}

if ($_GET['reportfmt'] == 'json'){
    Header('Content-type: text/json; charset=UTF-8');
    $arr_t = array();
    foreach($arr_rs as $ts => $arr){
        $arr_t[date("Y-m-d H:i:00",$ts)] = $arr;
    }
    print json_encode($arr_t, JSON_PRETTY_PRINT);
    exit();
}

if ($_GET['order'] == 'desc' || $_GET['order'] == 'descending'){
    $arr_ts = array_reverse($arr_ts);
}


$tag_s = ""; $tag_p = ""; $tag_n = ","; $tag_l = "\r\n";
if ($_GET['reportfmt'] == 'table'){
    $tag_s = "<tr>"; $tag_p = "<td>"; $tag_n = "</td>"; $tag_l = "</tr>\r\n";
}

$table_body = $tag_s.$tag_p."Records:".$duration." Counter:".sizeof($ct_names).$tag_n;
$i=0;
foreach($ct_names as $ct_name){
    $table_body .= $tag_p.($i++).":".$ct_name.$tag_n;
}
$table_body .= $tag_l;

// print_r($ct_names);
// print_r($counters);

for ($i=0; $i<$duration; $i++){
    $ts = $arr_ts[$i];
    $table_body .= $tag_s.$tag_p.date("Y/m/d H:i:s", $ts).$tag_n;
    foreach($ct_names as $ct_name){
        $table_body .= $tag_p.$arr_rs[$ts][$ct_name].$tag_n;
    }
    $table_body .= $tag_l;
}

if ($_GET['reportfmt'] == 'table'){
    Header('Content-type: text/html; charset=UTF-8');
    $table_body = '<style type="text/css">
        body {background-color: #fff; color: #222; font-family: sans-serif;}
        pre {margin: 0; font-family: monospace;}
        a:link {color: #009; text-decoration: none; background-color: #fff;}
        a:hover {text-decoration: underline;}
        table {border-collapse: collapse; border: 0; box-shadow: 1px 2px 3px #eee;}
        .center {text-align: center;}
        .center table {margin: 1em auto; text-align: left;}
        .center th {text-align: center !important;}
        td, th {border: 1px solid #aaa; font-size: 75%; vertical-align: baseline; padding: 4px 5px;}
        input {border: 1px solid #aaa; font-size: 100%; vertical-align: baseline; padding: 4px 5px;}
    </style>
    <table>'.$table_body.'</table>';
    print $table_body;
    exit();
}
else if ($_GET['reportfmt'] == 'csv'){
    Header('Content-type: text/csv; charset=UTF-8');
    print $table_body;
    exit();
}
else if ($_GET['reportfmt'] == 'chart'){
    $arr_wcolor = array (
		'red' => 'rgb(255, 99, 132)', 
		'orange' => 'rgb(255, 159, 64)', 
		'yellow' => 'rgb(255, 205, 86)', 
		'green' => 'rgb(75, 192, 192)', 
		'blue' => 'rgb(54, 162, 235)', 
		'purple'=> 'rgb(153, 102, 255)', 
		'grey'=> 'rgb(201, 203, 207)', 
		'black'=> 'rgb(60, 60, 60)',
	);	
    $arr_t = array();
    $arr_ts = array();
    foreach($ct_names as $ct_name){
        $arr_d[$ct_name] = array();
    }
    foreach($arr_rs as $ts => $arr){
        array_push($arr_ts,date("Y-m-d H:i:00",$ts));
        foreach($arr as $ct_name => $val){
            // print $val;
            array_push($arr_d[$ct_name], $val);
        }
        // print_r($arr);
        
    }
    foreach($ct_names as $ct_name){
        $rand_color = array_shift($arr_wcolor);
        array_push($arr_t, ['label'=> $ct_name, 'data' => $arr_d[$ct_name], 'borderWidth'=>3, 'borderColor'=>$rand_color, 'backgroundColor'=>$rand_color, 'fill'=>false, 'tension'=>0.5]);
    }
    $x_labels = json_encode($arr_ts, true);
    $dataset = json_encode($arr_t, true);
    $str_js = '
        <script src="/js/Chart.bundle.min.js"></script>		
        <canvas id="myChart" width="1200" height="600"></canvas>
        <script>
            const ctx = document.getElementById("myChart").getContext("2d");
            let config =  {
                type: "line",
                data: {},
                options: {
                    responsive: false,
                    plugins: {
                        title: {
                            display: true,
                        },
                        legend:{
                            display:true,
                            position:"top",
                            labels:{
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode:"index",
                        axis:"y"
                    },
                    scales: {
                        x: {
                            display: true,
                            type: "time",
                            time: {
                                parser: "MM/DD/YYYY HH:mm",
                                tooltipFormat: "ll HH:mm",
                                unit: "day",
                                unitStepSize: 1,
                                displayFormats: {
                                "day": "MM/DD/YYYY"
                                }
                            },
                            title: {
                                display: true
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: "Count"
                            },
                            suggestedMin: 0,
                            suggestedMax: 200
                        }
                    }
                },
            };
            const myChart = new Chart(ctx, config);
            let data = {
                labels: '.$x_labels.',
                datasets: '.$dataset.'
            };
            myChart.data = data;
            myChart.update();
        </script>';
    print $str_js;
}

// print "<pre>"; print_r($arr_rs); print "</pre>";

?>
