<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<div class="contentTitle"><span tkey="setup_camera_profile_conf"></span></div>
	<div class="content">
		<div id="profile_list" class="profile_list" style="max-height:200px;overflow-y:auto;">
			<table id="profile">
				<tr id="profile_title">
					<th width="35%">
						<b><span tkey="setup_camera_profile_number"></span></b>
					</th>
					<th width="15%">
						<b><span tkey="setup_camera_profile_fixed"></span></b>
					</th>
					<th width="50%">
						<b><span tkey="setup_camera_profile_name"></span></b>
					</th>
				</tr>
			</table>
		</div>
<!--
		<div id="profile_configure" class="profile_list">
			<div class="maintitle"><span tkey="setup_camera_profile_item"></span></div>
			<label class="subtitle"><span tkey="setup_camera_profile_name"></span></label>
			<input type="text" id="name" />
		</div>
-->
	</div>
	<center>
		<button id="btAdd" class="button half" value="add">
			<span tkey="setup_add"></span>
		</button>
<!--		
		<button id="btModify" class="button half" value="modify">
			<span tkey="setup_modify"></span>
		</button>
-->		
		<button id="btDelete" class="button half" value="delete">
			<span tkey="setup_delete"></span>
		</button>
		<button id="btApply" class="button half" value="apply">
			<span tkey="apply"></span>
		</button>
	</center>
</body>
</html>
