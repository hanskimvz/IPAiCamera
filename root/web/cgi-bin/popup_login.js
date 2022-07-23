//$.ajaxSetup({ cache: false });
$(document).ready( function(){
		Util.setOEM("logo");
		getJson();
    	initLanguage();
    	init();
    	dependency_css();
//    	$.cookie('chpass', null);
//    	$.cookie('chpass1' , 0 , { expires : 1 });	
//    	$.cookie('chpass', null , { expires : date });	
}); 		
$("#change_pass").on("click", function(){
	opener.popupflag = 2 ;
	
	if( typeof(opener.ctrlAdminTool) != "undefined")
	opener.ctrlAdminTool.close(); 
	
	if( typeof(opener.ctrlpopup) != "undefined")
	opener.ctrlpopup.close(); 

	opener.$("#setup").trigger("click");

//	window.location.replace("/cgi-bin/admin/setup_main.cgi") ;
});  
$("#check_later").on("click", function(){
	window.close();
});
function init(){	
	$("#popupchk").bind("click",function(){
		if( $("#popupchk").prop("checked") == 1){
			if( typeof($.cookie('chpass')) == "undefined" ){	
				var date = new Date();
			    var minutes = 1440;             // 60 x 24 = 1440 a day;
				date.setTime(date.getTime() + (minutes * 60 * 1000));
				$.cookie('chpass' , 0 , { expires : date });	
				window.open('about:blank','_self').self.close();
			}
		}
	});

}