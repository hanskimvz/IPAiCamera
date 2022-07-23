<?
define("_IP", "192.168.1.2"); 
define("_PORT", "65000"); 
$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); 
socket_connect($sock, _IP, _PORT); 
echo "CLIENT >> socket connect to "._IP.":"._PORT."\n"; 
socket_write($sock, "mac=001323A0073A&brand=CAP&model=NS202HD");
for (i=0; i<10; $i++) {
	$recv = socket_read($sock, 4096); 
	if ($recv == "done\0" {
		break;
	}
	echo "CLIENT >> $recv \n"; 

}
socket_close($sock); 
echo "CLIENT >> socket closed.\n"; 
?>
