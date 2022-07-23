<?php

//KEY_QUEUE
define('KEY_MQ_UPLOADER',       0x20000039); // ASK
define('KEY_MQ_UPLOADER_RESP',  0x20000040); // ANSWER

//FTP_STATUS
define('FTP_STATUS_IDDLE',     0); 
define('FTP_STATUS_CHECK_FW',  0); /* check the FTP list to find the upradde firmware */
define('FTP_STATUS_GET_FW',    0); /* download new firmware */
define('FTP_STATUS_FIND_FW',   0); /* find new firmware */
define('FTP_STATUS_NONE',      0); /* Lastest firmware */
define('FTP_STATUS_FAIL',      0); /* Fail!! */

//UPLOADER_STATUS
define('CODE_UPGRADE_FINISHED',  100);
define('CODE_UPGRADE_MASTER',    8);
define('CODE_UPGRADE_SLAVE', 	 7);
define('CODE_UPGRADE_BST', 	     4);
define('CODE_UPGRADE_ROOTFS',    3);
define('CODE_UPGRADE_KERNEL',    2);
define('CODE_UPGRADE_BOOT',      1);
define('CODE_UPGRADE_NONE',      0);
define('CODE_UPGRADE_FAIL',      -1);
define('CODE_UNSUPPORTED_MICOM_UPDATE', -99);
define('CODE_INVALID_FIRMWARE',  -100);

//CMD
define('M_UPLOADER_CHANGE_PORT',        20001);
define('M_UPLOADER_EXIT',               20002);
define('M_UPGRADE_COMPLETED',           20003);
define('M_UPGRADE_START',               20004);
define('M_UPGRADE_STOP',                20005);
define('M_UPGRADE_REMOVE_FILE',         20006);
define('M_UPGRADE_STATUS',              20007);
define('M_UPGRADE_START_KBM',           20008);

//CMD_FOR_FTP
define('M_FTP_UPGRADE_FIRMWARE_CHECK',  20009);
define('M_FTP_UPGRADE_DOWNLOAD_START',  20010);
define('M_FTP_UPGRADE_STATUS',          20011);

?>
