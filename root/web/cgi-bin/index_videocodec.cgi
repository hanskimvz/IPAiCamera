<?
require('_define.inc');
require('class/system.class');
require('class/capability.class');
require('class/network.class');
require('class/socket.class');
require('class/ptz.class');
require('class/media.class');

$focus_mode = new CFocusModeRequest();
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$system_caps = new CCapability($shm_id);
$net_conf = new CNetworkConfiguration($shm_id);
$profile_conf = new CProfileConfiguration($shm_id);
//$media_conf   = new CMediaConfiguration($shm_id);
//$mic_conf = $GLOBALS['media_conf']->ProfileConfig;
shmop_close($shm_id);
$get_oem = $system_caps->getOEM();


check_connection_policy_with_authority($system_conf);
echo  getChannelInfo($GLOBALS['profile_conf']);
?>