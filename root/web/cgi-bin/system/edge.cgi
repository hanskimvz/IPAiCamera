<?
include "../_define.inc";
include "../class/network.class";
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$NetConfig = new CNetworkConfiguration($shm_id);
shmop_close($shm_id);

// print_r($NetConfig);
/* this is license server error code */
define('RESPONSE_CODE_PRODUCT_INVALID_EXCEL_FORMAT',       -401);
define('RESPONSE_CODE_PRODUCT_EMPTY_EXCEL_FILE',           -402);
define('RESPONSE_CODE_PRODUCT_NO_CAAS_LICENSE_AVAILABLE',  -403);
define('RESPONSE_CODE_PRODUCT_NO_SUCH_CASS_LICENSE',       -404);
define('RESPONSE_CODE_PRODUCT_CAAS_LICENSE_TIMEOUT',       -405);
define('RESPONSE_CODE_PRODUCT_SERIAL_DUPLICATED',          -406);

$license = "";
$media_server = "127.0.0.1:7001";
$server_info = new stdClass();
$server_info->addr = "";
$server_info->port = 80;
$server_info->user = "caas";
$server_info->password = "caas1234";
$server_info->cookies = "";

function show_post_ng_with_message($msg) {
    echo "NG" . ( $msg ? " : " . $msg : '' ) . "\r\n";
}

function errorstring($errno) {
    $msg = "Undefined errno";
    switch ($errno) {
        case -401:
            $msg = "invalid excel format"; break;
        case -402:
            $msg = "empty excel file"; break;
        case -403:
            $msg = "no available caas license"; break;
        case -404:
            $msg = "no such cass license"; break;
        case -405:
            $msg = "cass license timeout"; break;
        case -406:
            $msg = "serial duplicated"; break;
    }
    return $msg;
}

//set_error_handler(function() { });
header("Content-Type: text/plain");
class HttpRequest {
    protected $method;
    protected $protocol;
    protected $url;
    protected $user;
    protected $password;

    // data 
    protected $data;

    // flag 
    protected $need_auth;
    protected $need_cookie;


    protected function saveCookie($ahr) {
        global $server_info;
        $matches = array();
        foreach ($ahr as $line){
            if( preg_match("/(sid=[^;]+)/i", $line, $matches) == 1 ){
                $server_info->cookies = $matches[0];
            }
        }
    }

    function __construct ($_protocol, $_url, $_method = "GET", $_auth=false) {
        $this->protocol  = $_protocol;
        $this->url       = $_url;
        $this->method    = $_method;
        $this->need_auth = $_auth;
        $this->user      = "admin";
        $this->password  = "admin";
        $this->data = "";
    }
	function __destruct()  {

    }

    /* to send data to sever */
    function set_data($_data) {
        $this->data = $_data;
    }

    /* if you changed the password */
    function credential($_user, $_password) {
        $this->user     = $_user;
        $this->password = $_password;
    }

    function connect() {
        global $server_info;

        $addr = $this->protocol . "://";
        if( $this->need_auth === true ) {
            $addr .= $this->user . ":" . $this->password ."@";
        }
        $addr .= $this->url;

        $options = array(
            "http" => array(
                "header"  => "Content-type: application/x-www-form-urlencoded\r\n" . 
                ( $this->need_cookie == true ?  "Cookie: ". $server_info->cookies : ''),
                "method"  => $this->method,
            )
        );

        if( $this->method === "GET") {
            $addr .= "?" . $this->data;
        }
        else {
            $options["http"]["content"] = $this->data;
        }
        $context  = stream_context_create($options);
        $data = file_get_contents($addr, false, $context);
        
        $this->saveCookie($http_response_header);
        return $data;
    }
    function setcookie($_value){
        $this->need_cookie = $_value;
    }
}
function parse_mediaserver_response($_data) {
    $json_data = array();
    $json_data = json_decode($_data, true);
    if( isset($json_data["error"]) && $json_data["error"] === "0" ) {
        return true;
    }
    return false;
}

function check_ping() {
    global $media_server;
    $req = new HttpRequest("http", $media_server."/api/ping/");
    $content = $req->connect();
    if( $content === false || parse_mediaserver_response($content) === false ) {
        show_post_ng_with_message("mediaserver is died!");
        return 1;
    }
    return 0;
}

function check_server(){
    $timeout = 3;
    $err =0;
    global $server_info;

    if( @$_REQUEST["addr"] ) {
        $server_info->addr = $_REQUEST["addr"];
    }
    if( @$_REQUEST["port"] ) {
        $server_info->port = $_REQUEST["port"];
    }
    if( @$_REQUEST["user"] ) {
        $server_info->user = $_REQUEST["user"];
    }
    if( @$_REQUEST["password"] ) {
        $server_info->password = $_REQUEST["password"];
    }
    
    $fp = @fsockopen($server_info->addr, $server_info->port, $errno, $errstr, $timeout);
    if( $fp ) {
        $login_param = array(
            "command" => "LoginRequest", 
            "properties" => array(
                "userid" => $server_info->user, 
                "password" => $server_info->password
            )
        );   
        $url = $server_info->addr . ":" . $server_info->port . "/auth.cgi";
        $req = new HttpRequest("http", $url, "POST", $auth=false);
        $req->credential($server_info->user, $server_info->password);
        $req->set_data(json_encode($login_param));
        
        $data = $req->connect();
        if( $data !== false ) {
            $response = json_decode($data);
            if( $response->command == "LoginResponse" && $response->return->code === '0' ) {
                return 0;
            }
            else {
                show_post_ng_with_message("authentication is failed!!(".errorstring($response->return->code).")");
                return 1;
            }
        }
    }
    show_post_ng_with_message("can't connected the server(".$server_info->addr.':'.$server_info->port.")");
    return 1;
}

function get_license(){
    global $license;
    global $server_info;
    $url = $server_info->addr . ":" . $server_info->port . "/product/api.cgi";
    $req = new HttpRequest("http", $url, "POST", $auth=false);
    $req->credential($server_info->user, $server_info->password);
    $get_license_param = new stdClass();
    $get_license_param->command = "GetUnusedCaaSLicenseRequest";
    $get_license_param->properties = array();
    $req->set_data(json_encode($get_license_param));

    $req->setcookie(true);
    $data = $req->connect();

    if( $data !== false ){
        $response = json_decode($data);
        if( $response->return->code == 0 ) {
            $license = $response->properties->license; 
            return 0;
        }
        else {
            show_post_ng_with_message("authentication is failed!!(".errorstring($response->return->code).")");
            return 1;
        }
    }
    show_post_ng_with_message("can't connected the server(".$server_info->addr.':'.$server_info->port.")");
    return 1;
}

function set_license(){
    global $license;
    global $server_info;
    global $NetConfig;
    global $media_server;

    // register license which be get from license server to mediaserver.
    $req = new HttpRequest("http", $media_server."/api/activateLicense", "GET", $auth = true);
    $req->set_data("key=" . $license);
    $content = $req->connect();
    if ($content === FALSE) {
        show_post_ng_with_message("can't connected the server(".$mediaserver . ")");
        return 1;
    }
    $json_res = array();
    $json_res = json_decode($content, true);
    if( isset($json_res["error"]) && $json_res["error"] !== "0" ) {
        show_post_ng_with_message("failed(" . $json_res["errorString"] . ")");
        return 1;
    }

    // must send this cgi server to check the used license during 1 minutes;
    // if you didn't this cgi, license is reused to the others 
    $req_param = new stdClass();
    $req_param->command = "SetUsedCaaSLicenseRequest";
    $req_param->properties = new stdClass();
    $req_param->properties->license = $license;
    $req_param->properties->serial = trim($NetConfig->HwAddress);

    $url = $server_info->addr . ":" . $server_info->port . "/product/api.cgi";
    $sreq = new HttpRequest("http", $url, "POST", $auth=false);
    $sreq->credential($server_info->user, $server_info->password);
    $sreq->setcookie(true);
    $sreq->set_data(json_encode($req_param));

    $response = json_decode($sreq->connect());
    if( $response->return->code == 0 ) {
        return 0;
    }
    show_post_ng_with_message("failed SetUsedCaaSLicenseRequest!!(".errorstring($response->return->code).")");
    return 1;
}

function initial_edge() {
    global $media_server;

    $req = new HttpRequest("http", $media_server."/api/setupLocalSystem","POST", $auth = true);
    $data = new stdClass();
    $data->systemName = "Caas";
    $data->adminAccount = "admin";
    $data->password = "admin12345";
    $data->systemSettings = new stdClass();
    $data->systemSettings->cameraSettingsOptimization = "true";
    $data->systemSettings->autoDiscoveryEnabled = "true"; 
    $data->systemSettings->statisticsAllowed = "true"; 

    $req->set_data(json_encode($data));

    $content = $req->connect();
    if ($content !== FALSE) {
        $json_res = array();
        $json_res = json_decode($content, true);
        if( isset($json_res["error"]) && $json_res["error"] === "0" ) {
            return 0;
        }
        else {
            show_post_ng_with_message("failed(" . $json_res["errorString"] . ")");
            return 1;
        }
    }
    show_post_ng_with_message("can't connected the server(".$server_info->addr.':'.$server_info->port.")");
    return 1;
}

function view_license() {
    global $media_server;

    $req = new HttpRequest("http", $media_server."/ec2/getLicenses","GET", $auth = true);
    $req->credential('admin', 'admin12345');
    $content = $req->connect();
    if ($content !== FALSE) {
        $json_res = json_decode($content, true);
        foreach($json_res as $l) {
            echo $l["key"]. "\r\n";
        }
        return; 
    }
    show_post_ng();
}
if( isset($_GET["action"] ) ) {
    switch ($_GET["action"])
    {
    case "init" :
        if( check_ping() )   break;
        if( check_server() ) break;
        if( get_license() )  break;
        if( set_license() )  break;
        if( initial_edge() ) break;

        echo "OK\n";
        exit;
    case "view" :
        if( check_ping() )   break;
        view_license(); 
        exit;
    default :
        show_post_ng();
        break;
    }
}
else {
    show_post_ng();
}
?>
