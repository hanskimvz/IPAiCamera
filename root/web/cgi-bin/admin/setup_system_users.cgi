<?
require('../_define.inc');
require('../class/system.class');
?>
<!DOCTYPE html>
<html>
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	<title>users management</title>
</head>
<body>
	<div class="contentTitle"><span tkey="setup_system_user_config"></span></div>
	<div id="View">
 		<div class="content">
			<table id="profile">
				<tr id="profile_title">
					<th class="t1"></th>
					<th><span tkey="setup_system_id"></span></th>
					<th><span tkey="setup_system_authority"></span></th>
				</tr>
			</table>
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
			<button id="btAdd" class="button half"><span tkey="setup_add"></span></button>
			<button id="btModify" class="button half"><span tkey="setup_modify"></span></button>
			<button id="btDelete" class="button half"><span tkey="setup_delete"></span></button>
		</center>
	</div>

	<div id="Modify">
		<div  class="content">
			<label class="subtitle"><span tkey="setup_system_id"></span></label>
			<input id="m_id" type="text" class="inputText"><br>
			<label class="subtitle"><span tkey="setup_system_passwd"></span></label>
			<input id="m_pass" type="password" class="inputText"><br>
			<div id="meter_wrapper_ui">
				<div id="meter_wrapper">
					<div id="meter"></div>
				</div>
				<label> [ <span id="pass_type"></span> ] </label><br>
			</div>
			<label class="subtitle"><span tkey="setup_system_verify"></span></label>
			<input id="m_pass_confirm" type="password" class="inputText"><br>
			<div id = "pass_hint_div">
				<label class="subtitle"><span tkey="setup_system_pass_hint"></span></label>
				<input id="m_pass_hint" type="text" class="inputText"><br>
			</div>
			<label class="subtitle"><span tkey="setup_system_userauthority"></span></label>
			<div class="select">
				<select id="m_auth">
					<option value="0">Administrator</option>
					<option value="1">Operator</option>
					<option value="2">Viewer</option>
				</select>
			</div>
            <div class="content change_pass" id="msg_change_pass">
            </div>
		</div>
		<center>
			<button id="btOK" class="button"><span tkey="apply"></span></button>
			<button id="btCancle" class="button"><span tkey="cancel"></span></button>
		</center>
		
	</div>
	<script>
		var usersInfo = new Array();
		<? 
		$system_conf = new CSystemConfiguration();
		$system_conf->Users->getAllUsersInfo('usersInfo');
		?>
	</script>
	<script src="./setup_system_users.js"></script>
</body>
</html>
