//$.ajaxSetup({ cache: false });
var temp_Array = new Object();
var tour_index = 0 ;
var table_index = 0 ;
var lastIndex = 0 ;
var content ;

$(document).ready( function(){		
		getpreset();
		getpresetTour();
		getJson();
    	initLanguage();
    	initUI();
    	initEvent();
    	Sel_tour_index();	
    	set_index();
}); 		
function getpreset(){
	$.ajax({
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: false,
			data : 'getpreset=1' ,
			dataType: 'json', 
			success : function(ret){	
				if( ret.presetInfo == undefined ) return 0;
				presetInfo = ret.presetInfo ;
			}
    }).done(function(){ console.log("요청 성공시 호출") })
	.fail(function(){ console.log("fail") })
	.always(function(){ console.log("always") });
}
function getpresetTour(){
	var promise = $.ajax(
		{
			type : 'get',
			url  : '/cgi-bin/ptz.cgi',
			async: true,
			dataType: 'json', 
			data : 'getpresetTour=1', 
			success : function(ret){		
				presetTourInfo = ret.presetTourInfo ;		
//				console.log(presetTourInfo);
				if( presetTourInfo == undefined ) return 0;
				
				for( var i = 0 ; i < 256 ; i++ ){		
					if( presetTourInfo[i] != undefined )
						$("#presettour_index").append("<option value="+ i +">Preset Tour"+ pad(i+1,2) + "</option>");
				}
				if( $("#presettour_index option").length == 0){
					$("#presettour_index").append("<option value=0 >Preset Tour01</option>");			
				}
//				set_index();
				Sel_tour_index();
			}
		}
	);	
}
function initUI(){
	var chkpreset = 0;

	for( var i = 0 ; i < 256 ; i++ ){
		if( presetInfo[i] != undefined)
			chkpreset = 1;
	}

	if( chkpreset == 0 ){
		alert('At least one preset is required');
		self.close();
	} else {
		for( var i = 0 ; i < 256 ; i++ ){
			if( presetInfo[i] !=undefined )
				$("#position_func").append("<option value="+ i +">["+ (i+1) +"]"+ presetInfo[i]['name'] + "</option>");
		}
	}
}
/*
function init_tourval(){
	
}
function del_presettour(i){
	$("#presettour_index option[value=" + i + "]").remove();
	
	if( $("#presettour_index option").length == 0){
		$("#presettour_index").append("<option value=1 >Preset Tour001</option>");				
	}
}
function del_preset(i){
	$("#position_func option[value=" + i + "]").remove();	
	
	if( $("#position_func option").length == 0){
		$("#position_func").append("<option value= -1 >Preset_000</option>");				
	}			
}
function add_preset(i){
	if( $("#position_func option").length != 0) $("#position_func option[value=-1]").remove()
		
	if( $("#position_func option[value=" + i  +"]").val() == undefined ) 
		$("#position_func").append("<option value="+ i +">preset_" + pad( Number(i+1),3 ) + "</option>");	
}*/
function pad(n, width) {
	  n = n + '';
	  return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}
function Sel_tour_index(){
	tour_index = $("#presettour_index").val() ;
	$("#result_table").find("*").remove();
	for( var i = 0 ; i < 256 ; i++ ){
		if( presetTourInfo[tour_index] == undefined ) break ;
		if( presetTourInfo[tour_index][i] != undefined ){	
//			console.log(i);
//			var presetnum = Number(presetTourInfo[tour_index][i]['preset']) + 1;
			var presetnum = Number(presetTourInfo[tour_index][i]['preset'])  ;
			content = "" ;
			content = "<tr class='list_items' >" ;
			content += "<td class='qt1'>" + (Number(presetTourInfo[tour_index][i]['index'] )+ 1) + "</td>" ; 
//			content += "<td class='qt' value="+ presetTourInfo[tour_index][i]['preset']  +">preset_"+ pad( presetnum,3 ) +"</td>" ; 
//			console.log( presetnum );
			if( presetInfo[presetnum] == undefined) 
				content += "<td class='qt' value= -1 >undefined</td>" ; 
			else
                content += "<td class='qt2' value="+ presetTourInfo[tour_index][i]['preset']  +">["+(presetnum+1) +"]"+presetInfo[presetnum]["name"]+"</td>" ; 
            
                content	+= "<td class='qt3'>" + (presetTourInfo[tour_index][i]['delay'])/1000 + "</td>" ; 
		     	content += "<td class='qt4'>" + (presetTourInfo[tour_index][i]['speed'])/1000 + "</td></tr>" ; 		
		     	$("#result_table").append(content);	
		}
	}	
	for( var i = 0 ; i < 256 ; i++ ){
		if( $("#result_table > tr:eq("+ i +")> td:eq(0)").text() != "" ){
			$("#result_table > tr:eq("+ i +")> td:eq(0)").text(i+1);
		}else
			break ;
	}
	set_index();	
	
}
function set_index(){
	var last_index = 0 ;
	for( var i =0 ; i < 256 ; i ++ ){		
		if( $("#result_table > tr:eq(" + i + ") > td:eq(0)").text() ) last_index = i+1;
//		console.log( last_index ) ;
	}
	$("#position_index").text(last_index+1);	
	
}
function getselectedIndex(){
	 var selectedIndex = $("#result_table > tr.list_items.sel_list_item > td:eq(0)").text() ;
	 return selectedIndex ;
}
function getlastindex(){
	for( var i = 0 ; i < 256 ; i++ ){
		if( $("#result_table > tr:eq("+ i +")> td:eq(0)").text() == "" ){
			lastIndex = i ;
			return Number(lastIndex)  ;
		}
	}
}
function SortTourList_Index(){
	for( var i = 0 ; i < 256 ; i++ ){
		if( $("#result_table > tr:eq("+ i +")> td:eq(0)").text() != "" ){
//			return lastIndex = i+1 ;
			$("#result_table > tr:eq("+ i +")> td:eq(0)").text(i+1);
		}
	}	
}
/*
function sort( name ){
	$( name ).append($("#"+name + " option").remove().sort(function(a, b) {
	    var at = $(a).text(), bt = $(b).text();
	    return (at > bt)?1:((at < bt)?-1:0);
	}));	
	
}*/
function tour_save(){
		$("#tourindex_add, #tourlist_add, #set_modify, #set_remove, #position_func, #position_delay, #position_speed").prop("disabled", true);
        var position ;
        tour_index = $("#presettour_index").val() ;
        presetTourInfo[tour_index] = new Object();

        for(var i = 0 ; i < 256 ; i++){
            if( $("#result_table > tr:eq(" + i + ")> td:eq(0)").text() != "" ){
				presetTourInfo[tour_index][i] = new Object();
                presetTourInfo[tour_index][i] = { index:"", preset:"", delay:"" , speed:"" } ;

                presetTourInfo[tour_index][i]['index'] = $("#result_table > tr:eq(" + i + ")> td:eq(0)").text();
                presetTourInfo[tour_index][i]['preset'] = $("#result_table > tr:eq(" + i + ")> td:eq(1)").attr("value");
                presetTourInfo[tour_index][i]['delay'] = ($("#result_table > tr:eq(" + i + ")> td:eq(2)").text()*1000);
                presetTourInfo[tour_index][i]['speed'] = ($("#result_table > tr:eq(" + i + ")> td:eq(3)").text()*1000);
            }
        }
        var datas = JSON.stringify(presetTourInfo[tour_index]) ;
        $.ajax({
                type : 'post',
                url : '/cgi-bin/ptz.cgi',
                async: true,
                data : {presettour : datas, tour_index: tour_index},
                dataType:"JSON",
                success : function(){
                    alert("Success!");
					$("#tourindex_add, #tourlist_add, #set_modify, #set_remove, #position_func, #position_delay, #position_speed").prop("disabled", false);
//                      opener.parent.seltour_index(tour_index) ;
                },
                error : function(request, status, error ) {   // 오류가 발생했을 때 호출된다.
                    if( request.responseText.trim() == "OK") alert("Success!");
					$("#tourindex_add, #tourlist_add, #set_modify, #set_remove, #position_func, #position_delay, #position_speed").prop("disabled", false);
    //              console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                }
        }).done(function(){ console.log("요청 성공시 호출") })
        .fail(function(){ console.log("fail") })
        .always(function(){ console.log("always") });

		if(opener != undefined)
            opener.parent.seltour_index(tour_index) ;
	Sel_tour_index();
	for( var i = 0 ; i < 256 ; i++ ){
		if( presetInfo[i] !=undefined ){
			$("#position_func").val(i) ;
		    $("#position_delay").val(1) ;
		    $("#position_speed").val(1) ;
			return 0;
		}
	}
}

function initEvent(){
	$("#presettour_index").on("click" , function(){		
		Sel_tour_index();
		set_index();
	});
	$("#tourindex_add").on("click" , function(){			
		var seleted_index = 1 ;
		var input ;
		
		function sel_indextour(){
			for( var i = 0 ; i < 11 ; i++){
				var index = $("#presettour_index option[value=" + i + "]").val() ;
				if( index == null ){
					seleted_index = i+1 ;		
					break ;
				}
			}
		}		
		sel_indextour() ;
		input = prompt('Select the Preset Tour Number ( 1 ~ 10 ).', seleted_index);

		if (!input.match(/^[0-9]+$/)){
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}
		
		if( input == null ) return 0 ;
		if(  input < 1 || input > 10){
			alert("Input the value : 1 ~ 10") ;
			return 0 ; 
		}
		if( presetTourInfo[input-1] != undefined ){
			alert(getLanguage("msg_duplicate_name"));
			return 0 ; 
		}
		$("#presettour_index").append("<option value=" + (input-1)+">Preset Tour"+ pad(input,2) +"</option>");		
		$("#presettour_index").append($("#presettour_index option").remove().sort(function(a, b) {
		    var at = $(a).text(), bt = $(b).text();
		    return (at > bt)?1:((at < bt)?-1:0);
		}));	
	
		$("#presettour_index option[value="+ (input-1) +"]").prop("selected", true);
		
		Sel_tour_index();
		set_index();
	});	
	$("#tourlist_add").on("click" , function(){		
		if( Number(lastIndex) > 255 ){
			alert("input the value : 1 ~ 256") ;
			return 0 ;
		}
		var Valid = new Validation() ;
        if( !Valid.check_range(1, 10, "position_delay"))  return 0;
        if( !Valid.check_range(1, 10, "position_speed"))  return 0;
		if( !($("#position_delay").val()).match(/^[0-9]+$/) || !($("#position_speed").val()).match(/^[0-9]+$/))
		{
            settingFail(menu, getLanguage("msg_onlynumber"));
            return 0;
        }

		$("#position_index").text( Number(getselectedIndex())+1) ;

		content = "<tr class='list_items' >" ;
		content += "<td class='qt'>" + $("#position_index").text() + "</td>" ;
		content += "<td class='qt' value=" + $("#position_func").val() + ">["+ (Number($("#position_func").val())+1) +"]"+ presetInfo[$("#position_func").val()]['name'] + "</td>" ;
		content	+= "<td class='qt'>" + $("#position_delay").val() + "</td>" ; 
		content += "<td class='qt'>" + $("#position_speed").val() + "</td></tr>" ; 
		
		if( $("#result_table > tr.list_items.sel_list_item").val() == undefined){
			$("#result_table").append(content);		
			SortTourList_Index();		
			$("#result_table > tr").removeClass("sel_list_item");			
			$("#result_table > tr:eq("+ (getlastindex()-1) +")").addClass("sel_list_item");
		}
		else{
			$("#result_table > tr.list_items.sel_list_item").after(content);
			SortTourList_Index();	
			var selectedIndex = getselectedIndex() ;
//			console.log( getselectedIndex() );
			$("#result_table > tr").removeClass("sel_list_item");			
			$("#result_table > tr:eq("+ (selectedIndex) +")").addClass("sel_list_item");
		}
		tour_save();
	});
	$("#set_modify").on("click" , function(){
		if( $("#result_table > tr.list_items.sel_list_item").val() == undefined){
			alert(getLanguage("msg_select_from_list")) ;
			return 0;
		} else {
			var Valid = new Validation() ;
			if( !Valid.check_range(1, 10, "position_delay"))  return 0;
			if( !Valid.check_range(1, 10, "position_speed"))  return 0;
			if( !($("#position_delay").val()).match(/^[0-9]+$/) || !($("#position_speed").val()).match(/^[0-9]+$/))
			{
				settingFail(menu, getLanguage("msg_onlynumber"));
				return 0;
			}
			table_index = getselectedIndex()-1 ;
			if( $("#result_table > tr:eq("+ (table_index) +")> td:eq(1)").attr("value") == $("#position_func").val()
				&& $("#result_table > tr:eq("+ (table_index) +")> td:eq(2)").text() == $("#position_delay").val()
				&& $("#result_table > tr:eq("+ (table_index) +")> td:eq(3)").text() == $("#position_speed").val() ){
				alert(getLanguage("msg_nothing_changed"));
				return 0;
			} else {
				$("#result_table > tr:eq("+ (table_index) +")> td:eq(1)").attr("value", $("#position_func").val());
				$("#result_table > tr:eq("+ (table_index) +")> td:eq(1)").text($("#position_func").text());
				$("#result_table > tr:eq("+ (table_index) +")> td:eq(2)").text($("#position_delay").val());
				$("#result_table > tr:eq("+ (table_index) +")> td:eq(3)").text($("#position_speed").val());
			}
		}
		tour_save();
	});
	$("#set_remove").on("click" , function(){
		if( $("#result_table > tr.list_items.sel_list_item").val() == undefined){
			alert(getLanguage("msg_select_from_list")) ;
			return 0;
		} else {
		table_index = getselectedIndex()-1 ;
		lastindex = getlastindex()-1 ;
			for(i = table_index; i < lastindex; i++){
				$("#result_table > tr:eq("+ (i) +")> td:eq(1)").attr("value", $("#result_table > tr:eq("+ (i+1) +")> td:eq(1)").attr("value"));
				$("#result_table > tr:eq("+ (i) +")> td:eq(1)").text($("#result_table > tr:eq("+ (i+1) +")> td:eq(1)").text());
				$("#result_table > tr:eq("+ (i) +")> td:eq(2)").text($("#result_table > tr:eq("+ (i+1) +")> td:eq(2)").text());
				$("#result_table > tr:eq("+ (i) +")> td:eq(3)").text($("#result_table > tr:eq("+ (i+1) +")> td:eq(3)").text());
			}
			$("#result_table > tr:eq("+ (lastindex) +")").remove();
		$("#result_table > tr").removeClass("sel_list_item");
		tour_save();
		}
	});
	$("#result_table").on("click", "tr", function(e) {		
		$("#result_table > tr").removeClass("sel_list_item");
		table_index =$("#result_table > tr").index( this );;
		$("#result_table > tr:eq("+ table_index +")").addClass("sel_list_item");	
				
		$("#result_table > tr:eq(0)> td:eq(2)").text();
		$("#result_table > tr:eq(" + i + ")> td:eq(2)").text();

		$("#position_index").text(Number(table_index)+1) ;
		$("#position_func").val( $("#result_table > tr:eq(" + table_index + ")> td:eq(1)").attr("value")) ;
		$("#position_delay").val( $("#result_table > tr:eq(" + table_index + ")> td:eq(2)").text()) ;
		$("#position_speed").val( $("#result_table > tr:eq(" + table_index + ")> td:eq(3)").text()) ;
	});		
	
	$("#position_delay, #position_speed").on("keyup",  function(e) {  

	});
	$("#position_func").on("click",  function(e) { 

	});
}
