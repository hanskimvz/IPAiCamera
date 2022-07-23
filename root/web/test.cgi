<?
require('/root/web/cgi-bin/_define.inc');
require('/root/web/cgi-bin/class/system.class');
$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
shmop_close($shm_id);

print "<pre>"; print_r($system_conf); print "</pre>";

?>