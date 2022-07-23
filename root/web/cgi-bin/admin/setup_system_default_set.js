function onClickApply()
{
    var menu= "Default ";
	menu = getLanguage("setup_system_defaultset");
	var  pop_msg ="";
    var obj = $('[name=optResetOption]:checked');
    var option = obj.val();

    if ( option == 0 || option == 1 ) 
    {
		pop_msg = getLanguage("msg_reboot_reset");
        if (confirm(pop_msg))
        {
            $.ajax({
                url: '/cgi-bin/admin/system.cgi',
                method: 'get',
                data: {
                    msubmenu: 'reset',
                    action: 'defaultset',
                    option: option
                },
                success: function(req)
                {
                    if(req.trim() != "NG")
                    {
						if( capInfo['oem'] == 12)
						{
							pop_msg = getLanguage("msg_default_success_reload_IV");
						}
						else 
						{
							pop_msg = getLanguage("msg_default_success_reload");
						}
                        settingSuccess(menu, pop_msg);
                        if(option == 1){
                            refreshMenuContent("reload");
                        }
                        else {
                            refreshMenuContent("all_factory_set_reload");
                        }

                    }
                    else
                        settingFail(menu);
                },
                error: function(){
					pop_msg = getLanguage("msg_fail_retry");
                    settingFail(menu, pop_msg);
                }
            });
        }
    }
    else if(option == 2)
    {
        //if( confirm("Do you want to start Reset the Camera?") )
        if (confirm(getLanguage("msg_reset_camera")))
        {
            $.ajax(
                {
                    type : 'get',
                    url  : '/cgi-bin/admin/camera.cgi?msubmenu=camera&action=reset',
                    success : function(req){
                        if(req.trim() != "NG")
                        {
							pop_msg = getLanguage("msg_default_camera_success"); 
                            settingSuccess(menu, pop_msg);
                            return;
                        }
                        else
                        {
							pop_msg = getLanguage("msg_default_camera_fail"); 
                            settingFail(menu, pop_msg);
                            refreshMenuContent("reload");
                        }
                    },
                    error	: function(){

                    }
                }
            );
        }
    }
}
function init(){
	if( capInfo['oem'] == 2 ){
		$("#cam").next().remove();
		$("#cam").next().remove();
		$("#cam").next().remove();
		$("#cam").remove();
	}else if( capInfo['oem'] == 8){
		$("#net").click();	
	}
	
}
$(document).ready(function(){
	init();
});
