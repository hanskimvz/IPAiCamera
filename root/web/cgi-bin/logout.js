
$(document).ready(function(){
		getJson();
		initLanguage();
		dependency_css();
		initUI();
});
function initUI(){
	if( capInfo["oem"] == 12){
		$('#re_login_btn').css('display','none');
		$('#re_login_msg').css('display','none');
	}else{
		$('#login_btn').css('display','none');
		$('#login_again_msg').css('display','none');
	}
}
