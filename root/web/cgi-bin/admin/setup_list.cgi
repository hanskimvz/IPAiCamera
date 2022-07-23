<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
// require('../class/network.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
// $net_conf = new CNetworkConfiguration($shm_id);
shmop_close($shm_id);
$get_oem = $system_caps->getOEM();


function getRTSPPort($name)
{
	echo $name . "=" .$GLOBALS['net_conf']->Protocols->Protocol[1]->Port.";\r\n";
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Expires" content="Tue, 12 May 1962 1:00:00 GMT">
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	<meta http-equiv="X-UA-Compatible" content="IE=10" /> 	
	<meta name="google" content="notranslate" />
	<title>Recording List and Preview Page</title>
	<noscript> </noscript>
	<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
	<link rel="stylesheet" href="/css/dom.css" type="text/css" />
	<link rel="stylesheet" href="/css/admin.css" type="text/css" />
</head>
<script>
</script>
<body oncontextmenu='return false;' ondragstart='return false;' onselectstart='return false;'>
	<div id="recording">
		<div class="contentTitle">Recording List</div>
		<div class="content list">
			<label class="maintitle">Filter</label>
			<label class="subtitle">
				<input type="checkbox" id="cDate" name="filter"/>
				<label for="cDate"></label>
				<span class="c_title">Date</span>
			</label>
			<input type="text" id="dFromDate" disabled="true" />~
			<input type="text" id="dToDate" disabled="true"/><br>
			<label class="subtitle">
				<input type="checkbox" id="cTime" name="filter" />
				<label for="cTime"></label>
				<span class="c_title">Time</span>
			</label>
			<div class="select quarter">
				<select id="sFromHour" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sFromMin" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sFromSec" class="quarter" disabled="true">
				</select>
			</div>~
			<div class="select quarter">
				<select id="sToHour" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sToMin" class="quarter" disabled="true">
				</select>
			</div>
			<div class="select quarter">
				<select id="sToSec" class="quarter" disabled="true">
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cEvent" name="filter">
				<label for="cEvent"></label>
				<span class="c_title">Event</span>
			</label>
			<div class="select">
				<select id="sEvent" disabled="true">
					<option value="all">ALL</option>
					<option value="4">Motion</option>
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cStorage" name="filter"/>
				<label for="cStorage"></label>
				<span class="c_title">Storage</span>
			</label>
			<div class="select" disabled="true">
				<select id="sStorage" disabled="true">
					<option value="all">ALL</option>
					<option value="SDCARD">SDCard</option>
				</select>
			</div><br>
			<label class="subtitle">
				<input type="checkbox" id="cSort" name="filter"/>
				<label for="cSort"></label>
				<span class="c_title">Sort</span>
			</label>
			<div class="select" disabled="true">
				<select id="sSort" disabled="true">
					<option value="asc">ascending</option>
					<option value="dec">decending</option>
				</select>
			</div><br>
		</div>
		<center>
			<button id="filter" class="button" disabled="true">filter</button>
		</center>
		<div class="content">
			<label class="maintitle">Event:</label><br>
			<div class="result_table">
				<table>
					<tr class="headline">
						<th class="date"> Date </th>
						<th class="time"> Time </th>
						<th class="duration"> Duration </th>
						<th class="event"> Event Number </th>
					</tr>
					<tr>
						<td colspan="4">
							<div style="overflow-y:auto; height:150px; ">
								<table id="result_table"> </table>
							</div>
						</td>
					</tr>
				</table>
			</div>
			<div id="pages">
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
		</div>
		<center>
			<button id="play" class="button">Play</button>
			<button id="remove" class="button">Remove</button>
			<button id="properties" class="button">Properties</button>
			<button id="download" class="button">Download</button>
		</center>
	</div>
	<div id="record_video" class="record_view">
		<div class="contentTitle">Recording Video</div>
		<object type='application/x-vlc-plugin' pluginspage='http://www.videolan.org' \
		version='VideoLAN.VLCPlugin.2' id='vlc' width='512px' \
		height='288px' align='center' vspace='0' events='True' VIEWASTEXT>
		<param name='MRL' value='' />
		<param name='ShowDisplay' value='true' />
		<param name='AutoLoop' value='true' />
		<param name='AutoPlay' value='true' />
		<param name='StartTime' value='0' />
		<param name='branding' value='true' /> 
		<param name='controls' value='true' /> 
		<param name='mute' value='true' />
		<param name='windowless' value='true'/></object>
		<br>
		<button id="replay" class="button">Replay</button>
		<button id="back" class="button">Back</button>
	</div>
	<iframe id="forDownload"></iframe>
</body>
<script src="/js/jquery1.11.1.min.js"></script>
<script src="/js/jqueryui.js"></script>
<script src="/js/page.js"></script>
<!-- <script src="/js/vlc.js"></script> -->
<script>
	var capInfo = new Object();
	var userInfo = new Object();
	// var rtspPort;
	var data = new Array();
	<?
	if($GLOBALS['get_oem'] == 19 || $GLOBALS['get_oem'] == 20 || $GLOBALS['get_oem'] == 21)
	{
		$GLOBALS['system_conf']->Users->getAccessUserInfo_x("userInfo");
	}
	else
	{
		$GLOBALS['system_conf']->Users->getAccessUserInfo("userInfo");
	}


?>
	function renew_data() {
		data = new Array();
		<?
		$filepath = "/media/mmcblk0p1/index.db";
		if( file_exists($filepath))
		{
			$fd = fopen($filepath, "r", true);
			$var = "data";
			$index = 0;
			while( !feof($fd) ) {
				$buffer = fgets($fd, 56);
				if( $buffer !== false )
				{
					$data[$index++] = unpack("a5event/a9duration/a18start/a10storage/a13key",$buffer);
				}
			}
			$max = $index;
			for($index = 0; $index < $max ; $index ++) {
				echo $var ."[" . $index . "]= Object();\n";
				echo $var ."[" . $index . "]['event']='" 	. $data[$index]['event'].	"';\n";
				echo $var ."[" . $index . "]['duration']='" . $data[$index]['duration']."';\n";
				echo $var ."[" . $index . "]['start']='" 	. $data[$index]['start'].	"';\n";
				echo $var ."[" . $index . "]['storage']='" 	. $data[$index]['storage'].	"';\n";
				echo $var ."[" . $index . "]['key']='" 		. $data[$index]['key'].		"';\n";
			}
			fclose($fd);
		}
		?>
	}
	renew_data();
</script>
<script src="./setup_event_record_list.js"></script>
</html>
