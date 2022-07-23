<?
require('../_define.inc');
require('../class/capability.class');
require('../class/system.class');
require('../class/socket.class');

$data_str = file_get_contents('../../js/license.json');
$json = json_decode($data_str, true); 

?>
<!DOCTYPE html>
<html>
	<head>
		<title>Open_Source</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false" >
		<div class="contentTitle"><span tkey="setup_system_open_source"></span></div>
		<div class="content">
		    <div class="license_table">
                <table  id="info" class="license_filed">
                   <thead id="info_head" class="license_filed">
                    </thead>
                    <tbody id="info_body"class="license_filed" >
                    </tbody>
			    </table>
            </div>
		</div>
		<script>
            var Sysjson = <? echo json_encode($json) ?>;
		</script>
		<script src="./setup_system_open_source.js"></script>
	</body>
</html>
