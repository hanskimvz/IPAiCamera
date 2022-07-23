var menu = getLanguage("setup_system_configuration");
function onLoadPage()
{
	initEvent();
}
function initEvent()
{
	$("[name=config]").change(function(e){
		if( $("[name=config]:checked").val() == 1){
			$("#file_div").css("display","none");
			$("#backup_key").empty();
		}else if( $("[name=config]:checked").val() == 0){
			$("#file_div").css("display","block");
			$("#backup_key").empty();
		}

	}); 
	$("#FileInput").change(function(event){
		var val = event.currentTarget.value;
		var filename = val.split("\\");
		filename = filename[filename.length-1];
		$("#file_status").css("display","block");
		$("#file_Info").css("display","block");
		$("#file_Info").text(filename);
		if (filename.substring(filename.length-3) != "tar"){
			$("#file_status").text("Invalid file. Please check again");
		}else{
			$("#file_status").text("Ready to upload.");
		}
	});
	$("#btOK").click( function(e){

		if($("#backup_key").val()=="")
		{
			settingFail(menu, "Enter Backup Key");
			return false;
		}

		var data ='';
		if($("[name=config]:checked").val()==1)
		{
			data += '&action=encrypt&key='+$("#backup_key").val();
			var url = '/cgi-bin/admin/system.cgi?msubmenu=config';
			$.ajax({
				type:"get",
				url: url,
				data : data,
				beforeSend: function(){ progressUI(true); },
				success: function(data){
					if(!(window.location = url+'&action=download')){
						settingFail(menu, "Fail");
					}
					progressUI(false);

				},
				error: function() {
					settingFail(menu, getLanguage("msg_fail_retry"));
					progressUI(false);
				}
			});
		}
		else if($("[name=config]:checked").val()==0)
		{
			data += '&action=upload&key='+$("#backup_key").val();
			var url = '/cgi-bin/admin/system.cgi?msubmenu=config'+data;
			var file_data = $("#FileInput").prop("files")[0];   
			var form_data = new FormData();
			form_data.append("file", file_data);

			$.ajax({
				url: url,
				data: form_data,
				cache: false,
				contentType: false,
				processData: false,
				method: 'POST',
				type: 'POST', 
				beforeSend: function(){ progressUI(true); },
				success: function(data){
					if(data.trim() == "OK"){
						settingSuccess(menu, getLanguage("msg_success")+" SYSTEM WILL REBOOT");
						progressUI(false);
					}
					else
					{
						settingFail(menu, getLanguage("msg_fail_retry"));
						progressUI(false);
					}
				},
				error: function(e){
					settingFail(menu, getLanguage("msg_fail_retry"));
					progressUI(false);
				}
			});

		}
		else
		{
			settingFail(menu, "Please Select the mode.(Download or Upload)");
			return false;
		}

	});

}
	
$(document).ready(function(){
	onLoadPage();
});
