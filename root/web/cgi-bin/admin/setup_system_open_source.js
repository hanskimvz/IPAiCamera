var menu = "System info";
var settingList = ["device_name"];



$(document).ready( function() {
    onLoadPage();
});



function onLoadPage()
{
    initValue();
	initLanguage();

}
function initValue()
{
    $("#info_head").append("<tr class=\"headline\"><th width=\"33%\">Open Source Name</th> <th width=\"32%\">Version</th> <th width=\"32%\">License</th></tr>");
    for( var i=0; i<Sysjson.list.length;i++){
        $("#info_body").append("<tr class=\"license_items\"><td width=\"33%\">"+Sysjson.list[i]["name"]+"</td><td width=\"32%\">"+Sysjson.list[i]["version"]+"</td><td width=\"32%\"> "+Sysjson.list[i]["license"]+"</td></tr>");
    }
}
