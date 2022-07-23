<?
require('../_define.inc');
?>
<!DOCTYPE html>
<html>
<head>
	<title>Action Rule Configuration</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body  oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
	<div class="contentTitle"><span tkey="setup_action_rule_config"></span></div>
	<div id="actions_list">
		<div class="content">
			<label class="maintitle"><span tkey="setup_action_rule"></span></label>
			<div class="result_table">
				<table class="result_filed">
					<thead >
						<tr class="headline">
							<th class="athird"><span tkey="setup_name"></span></th>
							<th class="athird"><span tkey="setup_reserve_action"></span></th>
							<th class="athird"><span tkey="setup_action"></span></th>
						</tr>
					</thead>
					<tbody id="result_table"></tbody>
				</table>
			</div>
		</div>
		<center>
			<button id="add" class="button"><span tkey="setup_add"></span></button>
			<button id="modify" class="button"><span tkey="setup_modify"></span></button>
			<button id="delete" class="button"><span tkey="setup_delete"></span></button>
		</center>
	</div>
	<div id="action_add_modify">
		<div class="content">
			<div class="maintitle" tkey="setup_general_setting"></div>
			<label class="subtitle" tkey="setup_name"></label>
			<input type="text" id="name" /><br>
			<div id="operation_layer">
			<label class="subtitle" tkey="setup_operation_duration"></label>
			<input class="short" type="number" id="duration"><label tkey="setup_transfer_sec"></label>
			[ 0 ~ 60 ]
			</div>
		</div>
		<div class="content">
		<?
			for($i = 0 ; $i < MAX_NUM_ACTION_JOB ; $i++) {
				echo "<div id='action_rule" . $i . "'>";
				echo "<div id='action_title".$i."''>";
				echo "<label id='actuion_label".$i."' class='subtitle' tkey='setup_action".($i+1)."'>";
				echo "Action".($i+1)."</label>";
				echo "<div class='select'>";
				echo "<select id='action". $i . "_type' name='types'>";
				echo "</select></div></div>";
				echo "<div id='detail" . $i . "' name='details'>";
				echo "</div></div>";
			}
		?>
		</div>
		<center>
			<button class="button" id="save"><span tkey="setup_save"></span></button>
			<button class="button" id="cancel"><span tkey="setup_cancel"></span></button>
		</center>	
	</div>
	<script>
		var MaxNumRecord		= <? echo MAX_RECORDING_JOB ?>;
		var MaxNumTrigger		= <? echo MAX_NUM_TRIGGER ?>;
		var ActionConditionMax 	;
		var presetInfo = {token:""};
		var presetTourInfo = {token:""};
		if(capInfo['oem'] == 6 || capInfo.camera_module == "ov_isp") ActionConditionMax = 1 ;
		else ActionConditionMax = <? echo MAX_NUM_ACTION_JOB ?>;
	</script>
	<script src="./setup_event_action_rules.js"></script>
</body>
</html>
