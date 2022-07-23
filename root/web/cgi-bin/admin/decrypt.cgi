<?php
define('FILE_ENCRYPTION_BLOCKS', 10000);
define('PATH', '/mnt/nand/');
define('PATH_ENC', '/root/web/pconf_enc/');
define('PATH_TAR', '/root/web/pconf_enc.tar');

function decryptFile($data , $destTo)
{
	$source = $destTo.".enc";
	$dest = $destTo;
	$key = substr(sha1($data, true), 0, 16);

	$error = false;
	if ($fpOut = fopen($dest, 'w')) {
		if ($fpIn = fopen($source, 'rb')) {
			$iv = fread($fpIn, 16);
			while (!feof($fpIn)) {
				$ciphertext = fread($fpIn, 16 * (FILE_ENCRYPTION_BLOCKS + 1)); 
				$plaintext = openssl_decrypt($ciphertext, 'AES-128-CBC', $key, OPENSSL_RAW_DATA, $iv);
				$iv = substr($ciphertext, 0, 16);
				fwrite($fpOut, $plaintext);
			}
			fclose($fpIn);
		} else {
			$error = true;
		}
		fclose($fpOut);
	} else {
		$error = true;
	}
	return $error ? false : $destTo;
}

function decompressFile($from,$destTo)
{
	try{
		exec('tar -xvf '.$from.' -C '.$destTo);
//		echo "decompress Success : ".$destTo."\n";
	}catch (Exception $e) {
		echo 'Error : ';
		echo $e->getMessage();
	}

}
function check_file($files)
{
	$enc_success = 0;
	for($i = 0; $i<count($files); $i++)
	{   
		if(0 == filesize( PATH_ENC.$files[$i] ))
		{   
			$enc_success = -1; 
		}   
		else
		{   
			$enc_success = 0;
		}   
	}   
	return $enc_success;
}

function check_header($files)
{
	$enc_success = 0;
	$files_hash = array();

	$str = file_get_contents(PATH_ENC.'header.json');
	$json =  json_decode($str, true);
	$str_cap = file_get_contents(PATH.'pconf_capability.db');
	$json_cap =  json_decode($str_cap, true);
    $str_sys = file_get_contents(PATH.'pconf_system.db');
	$json_sys =  json_decode($str_sys, true);


	for($i = 0; $i<count($files); $i++)
	{
		$files_hash[$i][0] = $files[$i];
		$files_hash[$i][1] = hash_file('sha1',PATH_ENC.$files[$i]);
		if($json["Checksum"][$i][0] == $files_hash[$i][0]){
			if($json["Checksum"][$i][1] != $files_hash[$i][1])
			{
				$enc_success = -3;
			}
		}

	}
	if($json_cap["board_chipset"] != $json["Model"] || $json_cap["oem"] !=  $json["OEM"])
	{   
		$enc_success = -1; 
	}
	else if($json_sys["DeviceInfo"]["BuildVersion"] != $json["BuildVersion"])
	{
		$enc_success = -2; 
	}

	return $enc_success;
}
function restore($files)
{
	$s =0;
//	error_log("restore ".count($files)."\n", "3", "/root/web/error.log");
	for($i = 0; $i<count($files); $i++)
	{   
		$old_path = PATH_ENC.$files[$i];
		$new_path = PATH.$files[$i];

		$filecontents = file_get_contents($old_path);

		if($files[$i] == "pconf_camera.db")
		{
			$json_camdb = json_decode(file_get_contents($new_path), true);
			$cam0profileinfo = $json_camdb[0]['profileInfo'];
			$cam1profileinfo = $json_camdb[1]['profileInfo'];
			$cam2profileinfo = $json_camdb[2]['profileInfo'];
			$cam3profileinfo = $json_camdb[3]['profileInfo'];

			$json = json_decode($filecontents, true);
			$json[0]['profileInfo'] = $cam0profileinfo;
			$json[1]['profileInfo'] = $cam1profileinfo;
			$json[2]['profileInfo'] = $cam2profileinfo;
			$json[3]['profileInfo'] = $cam3profileinfo;
			$filecontents = json_encode($json, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);
		}
		if($files[$i] == "pconf_network.db")
		{
			$json_netdb = json_decode(file_get_contents($new_path), true);
			$dns = $json_netdb['DNS'];  
			$hwAddr = $json_netdb['HwAddress'];  
			$ipv4 = $json_netdb['IPv4'];  
			$ipv6 = $json_netdb['IPv6'];  
			$mtuset = $json_netdb['MTUSetting'];  
			$protocol = $json_netdb['Protocols'];  
			$token = $json_netdb['Token'];  

			$json_old = json_decode($filecontents, true);
			$json_old['DNS'] = $dns;
			$json_old['HwAddress'] = $hwAddr;
			$json_old['IPv4'] = $ipv4;
			$json_old['IPv6'] = $ipv6;
			$json_old['MTUSetting'] = $mtuset;
			$json_old['Protocols'] = $protocol;
			$json_old['Token'] = $token;
			$filecontents = json_encode($json_old, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);
		}
		if($files[$i] == "pconf_system.db")
		{
			$json_sysdb = json_decode(file_get_contents($new_path), true);
			$certificates = $json_sysdb['Security']['Certificates'];
			if ($GLOBALS['get_oem'] == 2)
				$users = $json_sysdb['Users'];

			$json = json_decode($filecontents, true);
			$json['Security']['Certificates'] = $certificates;
			if ($GLOBALS['get_oem'] == 2)
				$json['Users'] = $users;
			$filecontents = json_encode($json, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);
		}

		if(!file_put_contents ( $new_path,$filecontents))
			$s = -1; 

	}
	if($s == -1) 
		return -1;
	else
		return 0;

}
function remove_all($files ,$dir){
	for($i = 0; $i<count($files); $i++)
	{   
		$loc = $dir."/".$files[$i];

		if(file_exists($loc))
			unlink($loc);

		if(file_exists($loc.'.enc'))
			unlink($loc.'.enc');
	}   
	if(file_exists($dir.'/header.json'))
		unlink($dir.'/header.json');
	unlink(PATH_TAR);
	rmdir($dir);
}

function dec_main($data){

	if(!is_dir(PATH_ENC)){
		mkdir(PATH_ENC);
	}   
//	error_log("dec_main \n", "3", "/root/web/error.log");

	$files = array('pconf_camera.db','pconf_etc.db','pconf_event.db','pconf_media.db','pconf_record.db','pconf_system.db','pconf_trigger.db','pconf_network.db');
	decompressFile(PATH_TAR,PATH_ENC);
	for($i = 0; $i<count($files); $i++)
	{
		decryptFile($data,PATH_ENC.$files[$i]);
//		echo $files[$i]."(hash) = ".hash_file('sha1',PATH_ENC.$files[$i])."\n";
	}

	if(check_file($files) == -1) 
	{
		remove_all($files,PATH_ENC);
//		echo "Fail : Please enter the correct password\n";
		return -2;
	}
	else if(check_header($files) == -1)
	{
		remove_all($files,PATH_ENC);
//		echo "Fail : Camera information does not match\n";
		return -3;
	}
	else if(check_header($files) == -2)
	{
		remove_all($files,PATH_ENC);
		return -4;
	}
	else if(check_header($files) == -3)
	{
		remove_all($files,PATH_ENC);
		return -5;
	}
	else
	{
		if(restore($files) == -1) {
			return -1;
		}
		remove_all($files,PATH_ENC);
		return 0;
	}
}

?>

