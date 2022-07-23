<?
require('../_define.inc');
require('../class/capability.class');
require('../class/system.class');
require('../class/network.class');
require('../class/socket.class');
$system_conf = new CSystemConfiguration();
$system_caps = new CCapability();
$net_conf = new CNetworkConfiguration();


function getsysInfo($name)
{	
	  echo $name."['model_name']='"             .trim($GLOBALS['system_conf']->DeviceInfo->Model)."';\r\n";  
	  echo $name."['manufacturer']='"           .trim($GLOBALS['system_conf']->DeviceInfo->Manufacturer)."';\r\n";  
	  echo $name."['device_name']='"            .trim($GLOBALS['system_conf']->DeviceInfo->DeviceName)."';\r\n";  
	  echo $name."['location']='"               .trim($GLOBALS['system_conf']->DeviceInfo->Location)."';\r\n"; 
//	  $data = $GLOBALS['net_conf']->HwAddress;
	  echo $name."['serialnum']='"              .trim($GLOBALS['net_conf']->HwAddress)."';\r\n"; 
      echo $name."['serialnumber']='"           .trim($GLOBALS['system_conf']->DeviceInfo->SerialNumber)."';\r\n";  
//	  echo $name."['serialnum']='"              .$data[0].$data[1].$data[3].$data[4].$data[6].$data[7].$data[9].$data[10].$data[12].$data[13].$data[15].$data[16]."';\r\n"; 
}

function getslaveversion($name)
{

	if( !file_exists('/tmp/slave_version')){
		echo $name."['slave1']='Not connect';\r\n";
		echo $name."['slave2']='Not connect';\r\n";
		echo $name."['slave3']='Not connect';\r\n";
		return ;
	}

    $file_arr = file('/tmp/slave_version');
    foreach($file_arr as $v){
        $v = str_replace(array("\r\n","\r","\n"),'',$v);
        if($v === "1.0.0.2"){
            $index= 1;         
            continue;
        }
        if($v === "1.0.0.3"){
            $index= 2;         
            continue;
        }
        if($v === "1.0.0.4"){
            $index= 3;         
            continue;
        } 

        $i = explode("=",$v);

        if($i[0] === "build"){
            $build = $i[1];
        }
        else if($i[0] === "version"){
            $version = $i[1];
            continue;
        }

        echo $name."['slave".$index."']='"              .$build."_".$version."';\r\n";  
#        echo $index." : ".$build."_".$version;
#        echo "<br/>\n";    
        $index =0;
        $build =0;
        $version=0;

    }
}

?>
<!DOCTYPE html>
<html>
	<head>
		<title>system information</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false" >
		<div class="contentTitle"><span tkey="setup_system_info"></span></div>
		<div class="content">
			<label class="subtitle"><span tkey="setup_system_name"></span></label>
			<input id="device_name" type="text"><br>
			<div id ="location_div">
				<label class="subtitle"><span tkey="setup_system_location"></span></label>
				<input id="location" type="text"><br>
			</div>
		</div>		
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
		</center>		
		<div class="content">
			<table id="info">
				<tr>
					<th width="150"><span tkey="setup_system_chipset"></span></th>
					<td id='model_name'></td>
				</tr>
				<tr id='serial_num'>
					<th width="150"><span tkey="setup_mac_address"></span></th>
					<td id='serialnum'></td>
				</tr>
                		<tr id='serial_number'>
					<th width="150"><span tkey="setup_system_serialnum"></span></th>
					<td id='serialnumber'></td>
				</tr>				
				<tr>
					<th width="150"><span tkey="setup_system_cameramodule"></span></th>
					<td id='manufacturer'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_maxresolution"></span></th>
					<td id='maxresol'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_maxframerate"></span></th>
					<td id='max_fps'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_cds"></span></th>
					<td id="have_cds">
				</tr>
				<tr>
					<th><span tkey="setup_system_alarmin"></span></th>
					<td id='alarm_in'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_relayout"></span></th>
					<td id='relay_out'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_audio"></span></th>
					<td id="audio_in_out"></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_opticalzoom"></span></th>
					<td id='have_zoom'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_digitalzoom"></span></th>
					<td id='have_digitalzoom'></td>
				</tr>
 				<tr>
					<th><span tkey="setup_system_ptz"></span></th>
					<td id='have_ptz'></td>
				</tr>
        <tr>
					<th><span>AI</span></th>
					<td id='have_AI'></td>
				</tr>
 				<tr id='slave_version'>
					<th ><span tkey="setup_system_slave_version"></span></th>
                    <td> 
                        <table>
                            <tr class="slave1"><td>Slave 1 </td><td id='slave1'> </td></tr>
                            <tr class="slave2"><td>Slave 2 </td><td id='slave2'> </td></tr>
                            <tr class="slave3"><td>Slave 3 </td><td id='slave3'> </td></tr>
                        </table>
                    </td>
				</tr>
<!-- 				<tr>
					<th><span tkey="setup_system_maxpreset"></span></th>
					<td id='preset'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_maxscan"></span></th>
					<td id='scan'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_maxgroup"></span></th>
					<td id='group'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_ir"></span></th>
					<td id='ir'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_pir"></span></th>
					<td id='pir'></td>
				</tr>
				<tr>
					<th><span tkey="setup_system_whiteled"></span></th>
					<td id='wled'></td>
				</tr> -->
			</table>
		</div>
		<script>
			var capInfo = <? $GLOBALS['system_caps']->getCapability() ?>;
			var SysInfo = new Object();
			var SlaveVersionInfo = new Object();
			<?
			getsysInfo("SysInfo"); 
			if($GLOBALS['system_caps']->is_proxy_camera)
			{
        		getslaveversion("SlaveVersionInfo");    
       		}
			?>			  
		</script>
		<script src="./setup_system_capability.js"></script>
	</body>
</html>
