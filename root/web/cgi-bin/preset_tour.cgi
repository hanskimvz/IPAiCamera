<?
require('_define.inc');
require('class/system.class');
require('class/socket.class');
require('class/media.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
//$presetconfig = new CPresetConfig();
//$presettourconfig = new CPresetTourConfig();
$system_conf = new CSystemConfiguration($shm_id);
//$media_conf = new CMediaConfiguration();
shmop_close($shm_id);
//$presetconfig = $media_conf->ProfileConfig->PTZConfiguration->presetConfig ;
//$presettourconfig = $media_conf->ProfileConfig->PTZConfiguration->presetTourConfig ;

//$presettour = new CPresetTour();
//$presettourconfig =  new CPresetTourConfig();

function getLangSetup($name)
{
	echo $name . "=" .$GLOBALS['system_conf']->SystemDatetime->Language.";\r\n";
}
?>
<!doctype html>
<html lang="en">
<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<meta http-equiv="X-UA-Compatible" content="IE=10" /> 
		<meta name="google" content="notranslate">
		<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<title>Preset Tour</title>
		<link rel="stylesheet" href="/css/jqueryui.css" type="text/css" />
		<link rel="stylesheet" href="/css/admin.css" type="text/css" />
		<link rel="stylesheet" href="/css/dom.css" type="text/css" />
		<style>
			.width_500{	
				width : 500px;
				margin : 0px 0px 0px 0px ;
			}
			.width_70{	width : 70px;}
			.tour_set{
				 width: 400px;
				 background-color: white ;
			}
			.content table{
				width: inherit; 
				table-layout: fixed
			}	 
			.width_110{	width:110px !important; }	
			.preset {
			    height: 25px !important;
			}
			.tour_css1{
				margin-left : 215px ;				
			}	
			.func_css{
				padding: 5px 10px !important; ;
			}
			.button1{
				margin-top: 5px ;	
			}
			body{
				width : auto ;	
			}
			.outline1{
				outline : #000 solid 1px;
			}
		</style>		
	</head>
<body>
	<div align="center" id="preset_tour_div" >
		<div class="contentTitle" style="display:inline-block">
			<span tkey="PRESET TOUR"></span>	
		
			<div class="select preset_1 width_110 tour_css1">
				<select id="presettour_index" class="preset_1 width_110 outline1" autocomplete='off' style="top: -5px; position:relative;"></select>
			</div>
			<button id="tourindex_add" class="button extrasmall" value="4">+</button>	
		</div>
		
		<div class="content width_500">
			<label class="maintitle"><span tkey="Preset Tour Set"></span></label>
			<div class="result_table">
				<table class="result_filed outline1">
					<thead>
						<tr class="headline">
							<th class="qt1"><span tkey="Index"></span></th>
							<th class="qt2"><span tkey="Function"></span></th>
							<th class="qt3"><span tkey="Delay:1~10(s)"></span></th>
							<th class="qt4"><span tkey="Speed:1~10"></span></th>
						</tr>
					</thead>
					<tbody id="result_table">
					</tbody>
				</table>
			</div>
		</div>
		<div align="right" class="func_css width_500">
			<button id="tourlist_add" class="button width_70 button1"><span tkey="setup_add"></span></button>
			<button id="set_modify" class="button width_70 button1" style="margin-right: 3px;"><span tkey="setup_modify"></span></butoon>
			<button id="set_remove" class="button width_70"><span tkey="setup_delete"></span></button>
		</div>
		<div class="content width_500">
			<table class="tour_set" border="2">
				<tr class="temp">
					<th><span>Index</span></th>				
					<th id="preset_func"><span>Function</span></th>
					<th id="tour_delay"><span>Delay:1~10(s)</span></th>
					<th id="tour_speed"><span>Speed:1~10</span></th>					
				</tr>
				<tr stylpe="border-collapse: collapse;" >
					<th style="width: 100%" ><label id="position_index" name="content" rows="10" style="width:100px; height:20px;" disabled ></label></th>
					<th><div class="select preset_1 width_110">
					<select id="position_func" class="preset_1 width_110" autocomplete='off'></select>
					</div></th>   
					<th style="width: 100%"><input id="position_delay" name="content" value="1" type="text" style="width:100px; height:20px;"></th>
					<th style="width: 100%"><input id="position_speed" name="content" value="1" type="text" style="width:100px; height:20px;"></th>
				</tr>			
			</table>
		</div>
	</div>	
	<script>
		var gLanguage;
		var presetTourInfo = {token:""};
		var presetInfo = {token:""};

		<?
			getLangSetup("gLanguage");

			
	/*		$ipc_sock = new IPCSocket();				
			$ipc_sock->Connection( $presetconfig, CMD_GET_PRESETS);	
			
			$ipc_sock = new IPCSocket();				
			$ipc_sock->Connection( $presettourconfig, CMD_GET_PRESET_TOURS);	    
		
			show_preset($presetconfig, 1);
			show_presettour($presettourconfig, 1);
	*/		
		?>
			

	</script>	
  	<script defer src="/js/jquery1.11.1.min.js"></script>	
    <script defer src="/js/jqueryui.js"></script>  
    <script src="/js/lang.js"></script> 
    <script src="/js/page.js"></script> 
    <script defer src="./preset_tour.js"></script>	
 
</body>
</html>
