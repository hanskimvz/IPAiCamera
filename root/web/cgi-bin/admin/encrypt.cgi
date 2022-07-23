<?php
define('FILE_ENCRYPTION_BLOCKS', 10000);
define('PATH', '/mnt/nand/');
define('PATH_ENC', '/root/web/pconf_enc/');
function encryptFile($data , $target)
{
		$source = PATH.$target;
		$dest = $source.'.enc';


		$key = substr(sha1($data, true), 0, 16);
		$iv = openssl_random_pseudo_bytes(16);
		$error = false;
		if ($fpOut = fopen($dest, 'w')) {
			fwrite($fpOut, $iv);
			if ($fpIn = fopen($source, 'r')) {
				while (!feof($fpIn)) {
					$plaintext = fread($fpIn, 16 * FILE_ENCRYPTION_BLOCKS);
					$ciphertext = openssl_encrypt($plaintext, 'AES-128-CBC', $key, OPENSSL_RAW_DATA, $iv);
					$iv = substr($ciphertext, 0, 16);
					fwrite($fpOut, $ciphertext);
				}
				fclose($fpIn);
			} else {
				$error = true;
			}
			fclose($fpOut);
		} else {
			$error = true;
		}

		return $error ? false : $dest;
}
function compressFile($fromDir, $target)
{ 
	try{
		ini_set('max_execution_time', '300');
		ini_set('set_time_limit', '0');
		exec('cd '.$fromDir.' && tar -cvf '.$target.' *');
	}catch (Exception $e){
		echo "Error : ";
		echo $e->getMessage();
	}
}
function make_header($files_hash){
	$str = file_get_contents(PATH.'pconf_capability.db');
	$json =  json_decode($str, true);

	$str2 = file_get_contents(PATH.'pconf_system.db');
	$json2 =  json_decode($str2, true);

	$header_info = array(
			"Model" => $json["board_chipset"],
			"OEM" => $json["oem"],
			"Date" => date("Y-m-d H:i:s"),
			"BuildVersion" => $json2["DeviceInfo"]["BuildVersion"],
			"Checksum" => $files_hash
			);  
	$formattedData = json_encode($header_info,JSON_PRETTY_PRINT);
	$filename = 'header.json';
	$handle = fopen($filename,'w+');
	fwrite($handle,$formattedData);
	fclose($handle);
	copy('header.json',PATH_ENC.'header.json');
	unlink('header.json');
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
	rmdir($dir);
}

function enc_main($data){
	$files = array('pconf_camera.db','pconf_etc.db','pconf_event.db','pconf_media.db','pconf_record.db','pconf_system.db','pconf_trigger.db','pconf_network.db');
	$files_hash = array();

	for($i = 0; $i<count($files); $i++){
		encryptFile($data , $files[$i]);
		$files_hash[$i][0] = $files[$i];
		$files_hash[$i][1] = hash_file('sha1', PATH.$files[$i]);
//		echo $files_hash[$i][0]." : ". $files_hash[$i][1]."\n";
	}
	$dir = PATH_ENC;
	if(!is_dir($dir)){
			mkdir($dir);
	}
	make_header($files_hash);
	for($i = 0; $i<count($files); $i++){
		$old_loc = PATH.$files[$i].'.enc';
		$new_loc = PATH_ENC.$files[$i].'.enc';
		if(file_exists($old_loc)) {
			if(!copy($old_loc, $new_loc)) { 
				echo "Fail to copy file (".$old_loc.")\n"; 
			}
			else if(file_exists($new_loc)){
				if(!unlink($old_loc)){ 
					if(unlink($new_loc)){ 
						echo "Fail to move file (".$old_loc.")\n"; 
					}
				}
			}
		}   
	}
	$fromDir = PATH_ENC;
	$target = '/root/web/pconf_enc.tar';
	compressFile($fromDir,$target);
	remove_all($files,PATH_ENC);
}
?>
