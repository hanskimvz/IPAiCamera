<?
require('buildtime_define.inc');
require_once('class/auth.class');


define("UPGRADE_SOCKET_PATH", "/opt/sock/server/upgrade_server");

define('MAX_PROFILE',						16);
define('NUM_FIXED_PROFILE', 				2);    // not removable profiles
define('MAX_VIDEO_SOURCE',				1);
define('MAX_AUDIO_SOURCE',				1);
define('MAX_VIDEO_ENCODER',				MAX_PROFILE);
define('MAX_AUDIO_DECODER',				1);
define('MAX_AUDIO_ENCODER',				1);
define('MAX_PTZ',							1);
define('MAX_METADATA',					1);
define('MAX_PRIVACY_MASK',				16);
define('MAX_VIDEO_CHANNEL', 			4);
define('MAX_MEDIA_SOURCE',              4);

// sytem
define('MAX_USER',						    32);	// MAX_USER_COUNT
define('MAX_SCOPE',						    10);
define('LEN_SCOPEITEM',	          				64);
define('LEN_HOSTNAME',	          				32);

//  network
define('MAX_DNS', 						    2);	// MAX_DNS_SERVER
define('MAX_NTP', 						    5);	// MAX_NTP_SERVER
define('MAX_DDNS',						    3);
define('MAX_IPV4ADDRESS',				1);
define('MAX_IPV6ADDRESS',				1);
define('MAX_NETWORK_INTERFACE',		1);
define('MAX_NETWORK_PROTOCOL',			3);
define('MAX_NETWORK_PROTOCOL_PORT',	1);
define('MAX_IPV4_GATEWAY',				1);
define('MAX_ZERO_CONFIG_ADDRESS', 		1);

//camera
define('MAX_CAMERA_CODE', 		57);
define('MAX_CAMERA_NAME',		32);
define('MAX_CAMERA_VALUE',		4);
define('MAX_CAMERA_PROFILE', 	10);

// device
define('MAX_SENSOR',						8);
define('MAX_RELAY',						4);

define('MAX_MOTION_AREA_RULE',			4);
define('MAX_STORAGE',					1);

// String Length Definition
define('LONG_STR_LEN',					64);
define('SHORT_STR_LEN',         32);

// storage 
define('MAX_STORAGE_DEVICE', 			4);

// record
define('MAX_RECORDING_JOB',	 			8);
define('FILE_FORMAT_NONE',				0);
define('FILE_FORMAT_TS',				1);
//define('FILE_FORMAT_MKV',				2);
//define('FILE_FORMAT_AVI',				3);
define("STORAGE_TYPE_NONE", 			0);
define("STORAGE_TYPE_SDCARD", 			1);

// trigger
define("MAX_NUM_TRIGGER", 				5);
define("MAX_NUM_EVENT_TYPE",			5);
define("MAX_NUM_ACTION_JOB",			5);

define("MAX_FILTERED_IPV4_ADDRESS",		15);

define("MAX_CERTIFICATE",				100);
define("KIND_OF_USER_AUTH",		    	5);

// ptz
define("MAX_PRESET_COUNT",				256);
define("MAX_PRESET_TOUR_POSITION",				256);
define("MAX_PRESET_TOUR_COUNT",				10);

define("MAX_FW_SIZE",				 80*1024*1024);
define("MAX_CV22_FW_SIZE",				 500*1024*1024);

// event code
define("ON_EVENT_BASE"                 , 12);
define("ON_EVENT_MOTION"               , 13);
define("ON_EVENT_SCHEDULER"            , 14);
define("ON_EVENT_SENSOR_ALARM"         , 15);
define("ON_EVENT_RELAY"                , 16);
define("ON_EVENT_NETWORK_DISCONNECTED" , 17);
define("ON_EVENT_SD_FULL"              , 18);
define("ON_EVENT_SD_FAILURE"           , 19);
define("ON_EVENT_IP_ADDR_CONFLICTED"   , 20);
define("ON_EVENT_TEMPERATURE_CRITICAL" , 21);
define("ON_EVENT_ILLEGAL_LOGIN" , 22);
define("ON_EVENT_USER_EVENT1" , 23);
define("ON_EVENT_USER_EVENT2" , 24);
define("ON_EVENT_USER_EVENT3" , 25);
define("ON_EVENT_USER_EVENT4" , 26);
define("ON_EVENT_USER_EVENT5" , 27);
define("ON_EVENT_USER_EVENT6" , 28);
define("ON_EVENT_USER_EVENT7" , 29);
define("ON_EVENT_USER_EVENT8" , 30);
define("ON_EVENT_USER_EVENT9" , 31);
define("ON_EVENT_USER_EVENT10", 32);
define("ON_EVENT_USER_EVENT11", 33);
define("ON_EVENT_USER_EVENT12", 34);
define("ON_EVENT_USER_EVENT13", 35);
define("ON_EVENT_USER_EVENT14", 36);
define("ON_EVENT_USER_EVENT15", 37);
define("ON_EVENT_USER_EVENT16", 38);
define("ON_EVENT_TEMPERATURE_DETECTED" , 39); // hdseo for thermal
define("ON_EVENT_CUSTOM_SNAP" , 40); //hdseo for iNode
define("ON_EVENT_PIR_DETECTED" ,41 );
define("ON_EVENT_SYS_INIT", 42);			// cmlee
define("ON_EVENT_LOCAL_RECORD_SNAP", 43);			// cmlee
define("ON_EVENT_END"                  , 43);
define("ON_EVENT_STORAGE_MOUNTED" 	   , 44);

// RecordEventMask
define("EVENT_MASK_CONTINOUS",				0);
define("EVENT_MASK_MOTION", 				(1 << 1) );
define("EVENT_MASK_SCHEDULE",				(1 << 2) );
define("EVENT_MASK_SENSOR_ALARM",			(1 << 3) );
define("EVENT_MASK_RELAY",					(1 << 4) );
define("EVENT_MASK_NETWORKDISCONNECTED",	(1 << 5) );
define("EVENT_MASK_SD_FULL", 				(1 << 6) );
define("EVENT_MASK_SD_FAILURE", 			(1 << 7) );
define("EVENT_MASK_IP_ADDR_CONFLICTED", 	(1 << 8) );
define("EVENT_MASK_TEMPERATURE_CRITICAL", 	(1 << 9) );
define("EVENT_MASK_ILLEGAL_LOGIN", 	(1 << 10) );
define("EVENT_MASK_USER_EVENT1", 	(1 << 11) );
define("EVENT_MASK_USER_EVENT2", 	(1 << 12) );
define("EVENT_MASK_USER_EVENT3", 	(1 << 13) );
define("EVENT_MASK_USER_EVENT4", 	(1 << 14) );
define("EVENT_MASK_USER_EVENT5", 	(1 << 15) );
define("EVENT_MASK_USER_EVENT6", 	(1 << 16) );
define("EVENT_MASK_USER_EVENT7", 	(1 << 17) );
define("EVENT_MASK_USER_EVENT8", 	(1 << 18) );
define("EVENT_MASK_USER_EVENT9", 	(1 << 19) );
define("EVENT_MASK_USER_EVENT10", 	(1 << 20) );
define("EVENT_MASK_USER_EVENT11", 	(1 << 21) );
define("EVENT_MASK_USER_EVENT12", 	(1 << 22) );
define("EVENT_MASK_USER_EVENT13", 	(1 << 23) );
define("EVENT_MASK_USER_EVENT14", 	(1 << 24) );
define("EVENT_MASK_USER_EVENT15", 	(1 << 25) );
define("EVENT_MASK_USER_EVENT16", 	(1 << 26) );
define("EVENT_MASK_TEMPERATURE_DETECTED", 	(1 << 27) );
define("EVENT_MASK_CUSTOM_SNAP", 			(1 << 28) );
define("EVENT_MASK_PIR_DETECTED", 	(1 << 29) );
define("EVENT_MASK_SYS_INIT", 		(1 << 30) );
define("EVENT_MASK_STORAGE_MOUNTED",(1 << 31) );

// if you want to add the new event, you have to define the up there and change the number
////////////////////////////////////////////////////////////////////////////////////////////////////
// Definition
////////////////////////////////////////////////////////////////////////////////////////////////////
define('SETUP_PARAM_ALL',	0);	                    // 
define('SETUP_PARAM_CAPABILITY',1);
define('SETUP_PARAM_NETWORK',	2);		              //  tNetworkConfiguration
define('SETUP_PARAM_SYSTEM',	3);		              // tSystemConfiguration
define('SETUP_PARAM_EVENT',	4);		                //  tEventConfiguration
define('SETUP_PARAM_MEDIA',	5);		                //  tMediaConfiguration
define('SETUP_PARAM_RECORD',	6);		              // tRecordConfiguration
define('SETUP_PARAM_CAMERA',	7);		              // tCameraConfiguration
define('SETUP_PARAM_ETC',	8);			                // tETCConfiguration
define('SETUP_PARAM_DEVICE_INFORMATION',	9);	    // tDeviceInformation
define('SETUP_PARAM_USERS',	10);				            // tUsers
define('SETUP_PARAM_DATETIME',	11);				      // tSystemDateTime
define('SETUP_PARAM_IO_CONFIGURATION',	12);	    // tDeviceIO
define('SETUP_PARAM_OSD',	13); 					          // OSD : tOSD
define('SETUP_PARAM_VIDEO_QPROI',14);            //QPROI : tVideoQproiConfiguration
define('SETUP_PARAM_CHANNEL',	15);				        // tChannelConfiguration
define('SETUP_PARAM_VIDEO_ENCODER',	16);		      //  tVideoEncoderConfiguration[2]
define('SETUP_PARAM_AUDIO_ENCODER',	17);				  // tAudioEncoderConfiguration
define('SETUP_PARAM_PROFILES',	18);						  // profiles ???? : tProfiles
define('SETUP_PARAM_PROFILE_CONFIGURATION',	19);	// profile_configuration ???? : tProfileConfiguration
define('SETUP_PARAM_MEDIA_SOURCES',	20);				  //  media_source ???? : tMediaSource
define('SETUP_PARAM_TRIGGERS_CONFIGURATION',	21);				  
define('SETUP_PARAM_ACTION_RULES', 22);
define('SETUP_PARAM_EVENT_RULES', 23);
define('SETUP_PARAM_FTP_UPGRADE', 24);
define('SETUP_PARAM_SMART_LBR', 25);   //SmartLBR
define('SETUP_PARAM_PRIVACY_MASK', 26);   
define('SETUP_PARAM_IOT',	27);
define('SETUP_PARAM_MAX',	28);

// HANDLE CODE
define('CMD_GET_CAPABILITY'                 , 1);
define('CMD_GET_DEVICE_INFORMATION'         , 2);
define('CMD_SET_DEVICE_INFORMATION'         , 3);
define('CMD_GET_ENDPOINT_REFERENCE'         , 4);
define('CMD_SET_USERS'                      , 5);
define('CMD_GET_USERS'                      , 6);
define('CMD_ADD_USER'                       , 7);
define('CMD_DEL_USER'                       , 8);
define('CMD_SET_USER'                       , 9);
define('CMD_GET_DATETIME'                   , 10);
define('CMD_SET_DATETIME'                   , 11);
define('CMD_GET_IO_CONFIGURATION'           , 12);
define('CMD_SET_IO_CONFIGURATION'           , 13);
define('CMD_SET_RELAY_OUTPUT_STATE'         , 14);
define('CMD_GET_SENSOR_STATE'               , 15);
define('CMD_GET_OSD'                        , 16);
define('CMD_SET_OSD'                        , 17);
define('CMD_SET_SYSTEM_FACTORY_DEFAULT'     , 18);
define('CMD_SYSTEM_REBOOT'                  , 19);
define('CMD_GET_NETWORK_CONFIGURATION'      , 20);
define('CMD_SET_NETWORK_CONFIGURATION'      , 21);
define('CMD_GET_EVENT_CONFIGURATION'        , 22);
define('CMD_SET_EVENT_CONFIGURATION'        , 23);
define('CMD_GET_CHANNEL_CONFIGURATION'      , 24);
define('CMD_SET_CHANNEL_CONFIGURATION'      , 25);
define('CMD_GET_VIDEO_ENCODE_CONFIGURATION' , 26);
define('CMD_SET_VIDEO_ENCODE_CONFIGURATION' , 27);
define('CMD_GET_PROFILES'                   , 28);
define('CMD_SET_PROFILES'                   , 29);
define('CMD_SET_PROFILE_CONFIGURATION'      , 30);
define('CMD_GET_PROFILE_CONFIGURATION'      , 31);
define('CMD_ADD_PROFILE'                    , 32);
define('CMD_DEL_PROFILE'                    , 33);
define('CMD_SET_PROFILE'                    , 34);
define('CMD_GET_MEDIA_SOURCE'               , 35);
define('CMD_START_MULTICAST_STREAMING'      , 36);
define('CMD_STOP_MULTICAST_STREAMING'       , 37);
define('CMD_SET_SYNCHRONIZATION_POINT'      , 38);
define('CMD_GET_RTSP_CONNECTIONS'           , 39);
define('CMD_DEL_RTSP_CONNECTION'            , 40);
define('CMD_SYSTEM_UPGRADE'                 , 41);
define('CMD_GET_CAMERA_SETUP'               , 42);
define('CMD_SET_CAMERA_SETUP'               , 43);
define('CMD_SET_CAMERA_PARAM'               , 44);
define('CMD_SET_NTP_SYNC'                   , 45);
define('CMD_SET_CAMERA_DEAFULT'             , 46);
define('CMD_SET_SETUP_INI'                  , 47);
define('CMD_GET_EVENT_STATUS'               , 48);
define('CMD_GET_UPLOAD_STATUS'              , 49);
define('CMD_TEST_FTP'                       , 50);
define('CMD_TEST_SMTP'                      , 51);
define('CMD_SET_CAMERA_RESTORE'             , 52);
define('CMD_SET_CAMERA_GROUP_DEFAULT0'      , 53);
define('CMD_SET_CAMERA_GROUP_DEFAULT1'      , 54);
define('CMD_SET_CAMERA_GROUP_DEFAULT2'      , 55);
define('CMD_SET_CAMERA_GROUP_DEFAULT3'      , 56);
define('CMD_SET_CAMERA_GROUP_DEFAULT4'      , 57);
define('CMD_SET_CAMERA_GROUP_DEFAULT5'      , 58);
define('CMD_SET_CAMERA_GROUP_DEFAULT6'      , 59);
define('CMD_SET_CAMERA_GROUP_DEFAULT7'      , 60);
define('CMD_SET_CAMERA_GROUP_DEFAULT8'      , 61);
define('CMD_SET_CAMERA_GROUP_DEFAULT9'      , 62);
define('CMD_GET_RECORDING_JOB'              , 63);
define('CMD_ADD_RECORDING_JOB'              , 64);
define('CMD_SET_RECORDING_JOB'              , 65);
define('CMD_DEL_RECORDING_JOB'              , 66);
define('CMD_GET_TRIGGERS_CONFIGURATION'     , 67);
define('CMD_ADD_EVENT_CONF'                 , 68);
define('CMD_SET_EVENT_CONF'                 , 69);
define('CMD_DEL_EVENT_CONF'                 , 70);
define('CMD_ADD_ACTION_CONF'                , 71);
define('CMD_SET_ACTION_CONF'                , 72);
define('CMD_DEL_ACTION_CONF'                , 73);
define('CMD_SET_FORMAT_SDCARD'              , 74);
define('CMD_SET_UNMOUNT_SDCARD'             , 75);
define('CMD_GET_FTP_UPGRADE'                , 76);
define('CMD_SET_FTP_UPGRADE'                , 77);
define('CMD_START_FTP_UPGRADE'              , 78);
define('CMD_PTZ_MOVE'                       , 79);
define('CMD_PTZ_ARROW'                       , 80);
define('CMD_PTZ_ZOOM'                       , 81);
define('CMD_PTZ_POSITION_MOVE'              , 82);
define('CMD_PTZ_GET_POSITION'               , 83);
define('CMD_PTZ_GET_POSITION_ALL'           , 84);
define('CMD_PTZ_GET_STATUS'                 , 85);
define('CMD_PTZ_STOP'                       , 86);
define('CMD_PTZ_SET_SPEED'                  , 87);
define('CMD_PTZ_GET_SPEED'                  , 88);
define('CMD_FOCUS_MOVE'                     , 89);
define('CMD_FOCUS_POSITION_MOVE'            , 90);
define('CMD_FOCUS_GET_POSITION'             , 91);
define('CMD_IRIS_MOVE'                      , 92);
define('CMD_IRIS_POSITION_MOVE'             , 93);
define('CMD_IRIS_GET_POSITION'              , 94);
define('CMD_SET_FOCUS_MODE'                 , 95);
define('CMD_GET_FOCUS_MODE'                 , 96);
define('CMD_GET_RECORDING_CHANNEL'          , 97);
define('CMD_SET_RECORDING_CHANNEL'          , 98);
define('CMD_GET_FISHEYE_CONFIG'             , 99);
define('CMD_SET_FISHEYE_CONFIG'             , 100);
define('CMD_SET_FISH_CENTER'                , 101);
define('CMD_GET_VIDEO_QPROI'                ,102);
define('CMD_SET_VIDEO_QPROI'                ,103);
define('CMD_GET_SMART_LBR'                  ,104);
define('CMD_SET_SMART_LBR'                  ,105);
define('CMD_GET_VIDEO_ENCODE_OPTIONS'       ,106);
define('CMD_GET_IMAGING_OPTIONS'			,107); 
define('CMD_GET_IMAGING_SETTINGS'			,108);
define('CMD_SET_IMAGING_SETTINGS'			,109);
define('CMD_GET_PRIVACY_MASK'				,110);
define('CMD_SET_PRIVACY_MASK'				,111);
define('CMD_GET_PTZ_NODES'					,112);
define('CMD_GET_CAMERA_PROFILES'			,113);
define('CMD_ADD_CAMERA_PROFILE'				,114);
define('CMD_MODIFY_CAMERA_PROFILE'			,115);
define('CMD_APPLY_CAMERA_PROFILE'			,116);
define('CMD_DELETE_CAMERA_PROFILE'			,117);
define('CMD_GET_SNAPSHOT_IMAGE'				,118);
define('CMD_SET_LANGUAGE'					,119);
define('CMD_GET_SECURITY'					,120);
define('CMD_SET_SECURITY_SERVICE'			,121);
define('CMD_SYSTEM_LOGCLEAR'				,122);
define('CMD_SET_SECURITY_IP_FILTER'			,123);
define('CMD_ADD_SECURITY_IP_FILTER_ADDR'	,124);
define('CMD_DEL_SECURITY_IP_FILTER_ADDR'	,125);
define('CMD_DEL_ALL_SECURITY_IP_FILTER_ADDR',126);
define('CMD_GET_GMT_DATETIME'				,127);
define('CMD_SET_IEEE_8021X'					,128);
define('CMD_ADD_SELF_SIGNED_CERT'			,129);
define('CMD_GET_CERTIFICATE_INFO'			,130);
define('CMD_DEL_CERTIFICATE'				,131);
define('CMD_CREATE_CSR'						,132);
define('CMD_INSTALL_CERTIFICATE'			,133);
define('CMD_INSTALL_CA'                     ,134);
define('CMD_DEL_CA'                         ,135);
define('CMD_SET_HTTPS'						,136);
define('CMD_SET_RTSP_AUTHENTICATION'		,137);
define('CMD_SET_FISHEYE_BUFFER_OFFSET'		,138);

define('CMD_GET_PRESETS'		,139);
define('CMD_SET_PRESET'		,140);
define('CMD_REMOVE_PRESET'		,141);
define('CMD_GOTO_PRESET'		,142);
define('CMD_GET_PRESET_TOURS'		,143);
define('CMD_ADD_PRESET_TOUR'		,144);
define('CMD_SET_PRESET_TOUR'		,145);
define('CMD_REMOVE_PRESET_TOUR'		,146);
define('CMD_OPERATE_PRESET_TOUR'		,147);

define('CMD_SET_HOME_POSITION'		,148);
define('CMD_GOTO_HOME_POSITION'		,149);
define('CMD_PTZ_POSITION_RELATIVE_MOVE'		,150);
define('CMD_POWER_PTZ_MOVE'		,151);

define('CMD_GET_CAMERA_PARAM'               , 152);
define('CMD_SET_TIME_FORMAT'                , 153);
define('CMD_CLEAR_RECOVERY_MODE'			,154);
define('CMD_SET_TRIGGERS_CONF'				,155);
define('CMD_SET_SENSOR_ALIGNMENT'			,156);
define('CMD_TEST_AUDIO_LOOPBACK'            ,157);
define('CMD_SET_CDS_ADJ'			,158);
define('CMD_SET_PTZ_AUX'			,159);
define('CMD_CLEAR_PTZ_AUX'			,160);

define('CMD_SYSTEM_UPDATE_READY'			,161);
define('CMD_SYSTEM_UPDATE_STOP'			,162);

define('CMD_EXPORT_RECORDFILE'			,163);
define('CMD_NOTIRY_ILLIGAL_LOGIN'			,164);
define('CMD_NOTIRY_FAIL_LOGIN'			,165);
define('CMD_NOTIRY_SUCCESS_LOGIN'			,166);
define('CMD_SET_SMART_ACF'			,167);

define('CMD_USER_LOGOUT'			,168);
define('CMD_SET_SMART_RC'			,169);

define('CMD_SYSTEM_DOWNLOAD_CONFIG'         ,170);
define('CMD_SYSTEM_UPLOAD_CONFIG'           ,171);

define('CMD_SET_DIGITAL_ZOOM'               ,172);
define('CMD_SET_PANTILT_AUTO_FLIP'          ,173);
define('CMD_SET_POWERUP_ACTION'             ,174);
define('CMD_SET_PARKING_ACTION'             ,175);
define('CMD_SET_VIDEO_PROFILE'              ,176);
define('CMD_SET_LED_CONTROL'			    ,177);
define('CMD_MOTION_FIRM_UPLOAD_START'       ,178);
define('CMD_CUSTOM_SNAP'			        ,179);
define('CMD_SET_INODE_CONFIGURATION'		,180);
define('CMD_SET_CORRIDOR'                   ,181);
define('CMD_SET_DEWARP'                     ,182);
define('CMD_SET_VOUT_RESOLUTION'            ,183);
define('CMD_GET_IOT'                        ,184);
define('CMD_SET_IOT'                        ,185);
define('CMD_SET_SETUP_INI_NO_REBOOT'        ,186);
define('CMD_SET_SECURITY_AUTOLOCK'			,187);//AUTOLOCK
define('CMD_SET_TESTTOUR'					,188);
define('CMD_TEST_HTTP'						,189);
define('CMD_SET_WIPER'         				,190);    // overview mode
define('CMD_SET_INVERT'         			,191);    // overview mode
define('CMD_SET_WASHER'         			,192);    // overview mode
define('CMD_VALIDATE_USER'					,193);
define('CMD_LOCAL_RECORD_SNAP'				,194); //for 3xLogic local record
define('CMD_SET_MOTION_CONFIGURATION'       ,195);
define('CMD_GET_HR_IMAGE'        			,196);    
define('CMD_SET_HR_IMAGE'         			,197);    

define('CMD_SET_SRTP'         ,198);    
define('CMD_TEST_FOCUSCAST'		,199);
define('CMD_TEST_AUDIOOUT'     ,200);


// ERROR CODE
define('APP_NONE'                           , 0);			//
define('APP_OK'                             , 1);			//
define('APP_ERR_FAILED'                     , 2);			//
define('APP_ERR_INVALID_ADDR'               , 3); 		//
define('APP_ERR_INVALID_PORT'               , 4); 		//
define('APP_ERR_INVALID_CONFIG'             , 5);	//
define('APP_ERR_INVALID_STRING'             , 6);     //
define('APP_ERR_OUT_OF_RANGE'               , 7);	//
define('APP_ERR_CONFIG_NOT_EXIST'           , 8); //
define('APP_ERR_CONFIG_CONFLICT'            , 9);	//
define('APP_ERR_CONFIG_MODIFY'              , 10);    //
define('APP_ERR_CAPABILITY_NOT_SUPPORTED'   , 11); //
define('APP_ERR_INVALID_TIMEZONE'           , 12);
define('APP_ERR_INVALID_DATETIME'           , 13);
define('APP_ERR_INVALID_HOSTNAME'           , 14);
define('APP_ERR_INVALID_IPv4_ADDR'          , 15);
define('APP_ERR_INVALID_IPv6_ADDR'          , 16);
define('APP_ERR_OPERATION_PROHIBITED'       , 17);
define('APP_ERR_SERVICE_NOT_SUPPORTED'      , 18);
define('APP_ERR_INVALID_GATEWAY_ADDRESS'    , 19);
define('APP_ERR_EMPTY_SCOPE_LIST'           , 20);
define('APP_ERR_SCOPE_OVERWRITE_FAILURE'    , 21);
define('APP_ERR_SCOPE_MAX_LIMIT'            , 22);
define('APP_ERR_NOTFOUND_SCOPE'             , 23);
define('APP_ERR_REMOVE_FIXED_SCOPE'         , 24);
define('APP_ERR_USERNAME_CRASH'             , 25);
define('APP_ERR_PASSWORD_TOO_LONG'          , 26);
define('APP_ERR_USERNAME_TOO_LONG'          , 27);
define('APP_ERR_PASSWORD_TOO_WEAK'          , 28);
define('APP_ERR_USER_MAX_LIMIT'             , 29);
define('APP_ERR_USERNAME_NOT_FOUND'         , 30);
define('APP_ERR_DELETE_FIXED_USER'          , 31);
define('APP_ERR_INCOMPLETE_CONFIGURATION'   , 32);
define('APP_ERR_PROFILE_ALREADY_EXIST'      , 33);
define('APP_ERR_PROFILE_DELETE_FAILED'      , 34);
define('APP_ERR_PROFILE_MAX_LIMIT'          , 35);
define('APP_ERR_PROFILE_NOT_EXIST'          , 36);
define('APP_ERR_REMOVE_FIXED_PROFILE'       , 37);
define('APP_ERR_TEST_TRANSMITTER_CONNECT'   , 38);
define('APP_ERR_TEST_TRANSMITTER_LOGIN'     , 39);
define('APP_ERR_TEST_TRANSMITTER_DATA'      , 40);
define('APP_ERR_TEST_TRANSMITTER_ATTACH'    , 41);
define('APP_ERR_RECORD_JOB_OVER_LIMITATION' , 42);
define('APP_ERR_ENCRYPTED_VIDEO'            , 43);
define('APP_ERR_USED_CERTIFICATE'			, 44);
define('APP_ERR_INVALID_COUNTRY_CODE'		, 45);
define('APP_ERR_MEDIA_SERVER_IS_RUNNING'	, 46);

// Unique Key of Shared Memory
define('KEY_SM_SHARED_CONFIG',			0x30000001);
define('KEY_SM_SHARED_CAMERA_PROFILE',	0x30000002);
define('KEY_SM_SYSTEM_SYSTEM',	        0x30000003);
define('KEY_SM_LOG_LIST_SYS',		0x30000011);

define('KEY_SM_RTSP_CONNECTIONS',	0x30000015);
define('KEY_SM_STORAGE_INFO',       0x30000017);
	
// video/audio
define('CODEC_NONE',		0);
define('CODEC_H264',		1);
define('CODEC_MJPEG',		2);
define('CODEC_HEVC',		3);

define('G711_CODEC',		10);
define('G726_CODEC',		11);
define('AAC_CODEC',		12);

define('RESOL_1080p',		0);
define('RESOL_720p',		1);
define('RESOL_SVGA',		2);
define('RESOL_D1',			3);
define('RESOL_VGA',	    	4);
define('RESOL_CIF',			5);
define('RESOL_QCIF',		6);

define('BITRATE_VBR',		0);
define('BITRATE_CBR',		1);

define('COLORSYS_NTSC',		0);
define('COLORSYS_PAL',		1);
define('COLORSYS_AUTO',		2);

// backup -
define('IMG_BMP',			0);
define('IMG_JPG',			1);

// user -
define('MAX_BASIC_USER',	11);
define('USER_ADMIN',		1);
define('USER_OPERATOR',		2);
define('USER_VIEWER',		4);

// ftp, smtp -
define('M_TEST_FTP_OK',            2);
define('M_TEST_FTP_DOING',         1);
define('M_TEST_FTP_NONE',          0);
define('M_TEST_FTP_CONNECT_ERR',  -1);
define('M_TEST_FTP_LOGIN_ERR',    -2);
define('M_TEST_FTP_PROTOCOL_ERR', -3);
define('M_TEST_FTP_ATTACH_ERR',   -4);

define('M_TEST_SMTP_OK',           2);
define('M_TEST_SMTP_DOING',        1);
define('M_TEST_SMTP_NONE',         0);
define('M_TEST_SMTP_CONNECT_ERR', -1);
define('M_TEST_SMTP_LOGIN_ERR',   -2);
define('M_TEST_SMTP_BODY_ERR',    -3);
define('M_TEST_SMTP_ATTACH_ERR',  -4);

// log -
define('LOGITEM_PER_PAGE',	22);

// date/time -
define('NTP_SYNC_FAILED',    0);
define('NTP_WRONG_ADDRESS',  1);
define('NTP_SERVER_CHANGED', 2);
define('NTP_SYNC_SUCCESS',   3);
define('NTP_SYNCHRONIZING',  4);


define('OFFSET_BASE',		0);
define('SIZE_POS_INFO',		12);
define('OFFSET_CONFIG',		256);
define('SIZE_HAEDER',		256);


define("CERT_ROOT_PATH" , "/mnt/nand/certificates");
define("CERT_NAME"      , "_cert.pem");
define("KEY_NAME"       , "_key.pem");


// system option.
define('SYSTEM_OPTION_UI_FIXED_DATE_20160504',	0x01);
define('SYSTEM_OPTION_DW_EDGE',	0x02);

define('BASKET_HEADER_SIZE', 4);
define('LOG_HEADER_SIZE'   , 20);
define('MAX_LOG_BASKET'    , 3);
define('MAX_LOG_ON_BASKET' , 300);
define('MAX_LOG'           , (MAX_LOG_BASKET * MAX_LOG_ON_BASKET));

function show_post_ng()
{
	echo "NG\r\n";
}

function show_post_ok()
{
	echo "OK\r\n";
}

function show_post_not_support()
{
	echo "NOT SUPPORT\r\n";
}

function show_post_OUT_OF_RANGE()
{
	echo "OUT OF RANGE\r\n";
}

function ResponseResult($_value)
{
	$msgType = array('NG', 'OK');
	header("Content-Type: text/plain");
	header("Content-Length: 2");
	echo $msgType[$_value];
	exit;
}

// Arrayed data(structured data) into binary string
function MakePayload($_dataInfo)
{
	$payload = '';
	foreach($_dataInfo as $data)
	{
		//$payload .= pack(strtolower($data['type']), trim($data['value']));
		$payload .= pack(strtolower($data['type']), $data['value']);
	}
	return $payload;
}




// Get unpack format from arrayed data
function MakeDataFormat($_dataInfo)
{
	$dataFormat = '';
	while($data = current($_dataInfo))
	{
		$dataFormat .= $data['type'].key($_dataInfo)."/";
		next($_dataInfo);
	}
	return $dataFormat;
}

// make unpack format
function MakeUnpackFormat($_name, $_length, $_maxValue)
{
  $unpackFormat = '';
	for ($index=0; $index<$_maxValue; ++$index)
	{
		$unpackFormat .= 'a'.$_length.$_name.$index.'/';
	}
	return $unpackFormat;
}

function GetDataInfoLength($_dataInfo)
{
	$totalLength = 0;
	foreach ($_dataInfo as $data)
	{
		$length = (int)substr($data['type'], 1);
		$type = substr($data['type'], 0, 1);
		if ($type == 'i' ||  $type == 'I')
		{
			$length *= 4;
		}
		$totalLength += $length;
	}
	return $totalLength;
}

// Binary string into arrayed data
function SetDataInfo($_dataClass, $_dataArray)
{
	// binary string into unpacked data
	if (is_string($_dataArray)) {
		$_dataArray = unpack(MakeDataFormat($_dataClass->dataInfo), $_dataArray);
	}
	// unpacked data into arrayed data
	foreach ($_dataClass->dataInfo as $key=>$data)
	{
		$_dataClass->dataInfo[$key]['value'] = $_dataArray[$key];
	}	
	
	//foreach ($_dataArray as $name=>$value)
	//{
	//	foreach ($_dataClass->dataInfo as $key=>$data)
	//	{
	//		if ($name == $key)
	//		{	
	//			$_dataClass->dataInfo[$name]['value'] = $value;
	//			break;
	//		}
	//	}
	//}
}
//--------------------------------------------------------------------------------------------
// Check the connected browser.
// Internet Explorer : 
function getBrowser()
{
    $u_agent = $_SERVER['HTTP_USER_AGENT'];
    $bname = 'Unknown';

    if(preg_match('/MSIE/i',$u_agent) && !preg_match('/Opera/i',$u_agent)) { $bname = 'Internet Explorer'; $ub = "MSIE"; }
    elseif(preg_match('/Firefox/i',$u_agent)) { $bname = 'Mozilla Firefox'; $ub = "Firefox"; }
    elseif(preg_match('/Chrome/i',$u_agent)) { $bname = 'Google Chrome'; $ub = "Chrome"; }
    elseif(preg_match('/Safari/i',$u_agent)) { $bname = 'Apple Safari'; $ub = "Safari"; }
    elseif(preg_match('/Opera/i',$u_agent)) { $bname = 'Opera'; $ub = "Opera"; }
    elseif(preg_match('/Netscape/i',$u_agent)) { $bname = 'Netscape'; $ub = "Netscape"; }
   
    return $bname;
}
function view_array($name, $array)
{
	foreach($array as $k=>$v)
	{
		if( is_array($v)){
			printf("[%s%02d]\r\n",$name,$k+1);
			view_array(NULL, $v);
		}
		else if( is_object($v) )
			view_object($v);
		else
			echo "$name$k=$v\r\n";
	}
}
function view_encode($obj)
{
	foreach($obj as $k=>$v)
	{
		if( is_array($v))
			view_array($k , $v);
		else if ( is_object($v))
			view_encode($v);
		else
			echo "$k=$v\r\n";
	}
}
function get_channel_index($VinSourceConfs)
{
	// channel is the highest priority 
	if( isset($_REQUEST['channel']) ) return $_REQUEST['channel'];

	// check vaidation of vinput
	if( get_class($VinSourceConfs) != "CVideoSourceConfigurations" ) return -1;
	if( !isset($_REQUEST['source']) || !isset($_REQUEST['stream']) ) return -1;

	$source = $_REQUEST['source']; // 0: all vin, 1~N : vin1~vinN

	if( $source < 0 || $source > MAX_MEDIA_SOURCE ) return -1; 
	if( $source ) 
		--$source;

	$stream = $_REQUEST['stream']; // 0: MainStream, 1: SubStream, 2: Image/Third
	if( $stream < 0 || $stream >= MAX_VIDEO_CHANNEL ) return -1;

	return $VinSourceConfs->Config[$source]->StreamNums->num[$stream]->value;
}

function check_connection_policy_with_authority($config)
{
	$auth_data = $_SERVER['PHP_AUTH_DIGEST'];
	preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $auth_data, $digest);

	for($i=0; $i<count($digest[1]); $i++)
	{
		if($digest[1][$i] == 'username')
		{
			$access_user_id = $digest[2][$i];
			break;
		}
	}
	for ($i=0; $i<MAX_USER ; $i++)
	{
		if( $config->Users->User[$i]->Enabled == 1)
		{
			if (trim($config->Users->User[$i]->Name) == $access_user_id)
			{
				$access_user_level = trim($config->Users->User[$i]->Level);
				break;
			}
		}
	}
	
	$policy = $config->Security->Https->ConnectionPolicy[0]->value;
	
	if( $policy == 0 ){ // allow http
		if(isset($_SERVER['HTTPS']))
		{
			$redirect = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
			header('HTTP/1.1 301 Moved Permanently');
			header('Location: ' . $redirect);
			exit();
		}
	} else if( $policy == 1 ){ //allow https
		if(empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] == "off")
		{
			$redirect = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
			header('HTTP/1.1 301 Moved Permanently');
			header('Location: ' . $redirect);
			exit();
		}
	}
}
function DependencyOem(){
	if( trim($GLOBALS['system_caps']->oem) == "ESCA")
		echo '<link rel="stylesheet" href="/css/esca.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "CDUS")
		echo '<link rel="stylesheet" href="/css/cdus.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "JSS")
		echo '<link rel="stylesheet" href="/css/jss.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "RVI")
		echo '<link rel="stylesheet" href="/css/rvi.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "RUBEZH")
		echo '<link rel="stylesheet" href="/css/rubezh.css" type="text/css" />';        
	else if( trim($GLOBALS['system_caps']->oem) == "CBCA")
		echo '<link rel="stylesheet" href="/css/cbca.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "VCA")
		echo '<link rel="stylesheet" href="/css/vca.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "WAVESYS")
		echo '<link rel="stylesheet" href="/css/wavesys.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "IV")
		echo '<link rel="stylesheet" href="/css/IV.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "ClickIT")
		echo '<link rel="stylesheet" href="/css/ClickIT.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "HS")
		echo '<link rel="stylesheet" href="/css/HS.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "DTI")
		echo '<link rel="stylesheet" href="/css/dti.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "JCI")
		echo '<link rel="stylesheet" href="/css/jci.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "EUKLIS")
		echo '<link rel="stylesheet" href="/css/euklis.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "STANLEY")
		echo '<link rel="stylesheet" href="/css/stanley.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "_3XLOGIC")
		echo '<link rel="stylesheet" href="/css/3xlogic.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "SONITROL")
		echo '<link rel="stylesheet" href="/css/sonitrol.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "ACTIVEWITNESS")
		echo '<link rel="stylesheet" href="/css/activewitness.css" type="text/css" />';
	else if( trim($GLOBALS['system_caps']->oem) == "UR_SECURE"){
		echo '<link rel="stylesheet" href="/css/cbca.css" type="text/css" />';
		echo '<link rel="stylesheet" href="/css/ur_secure.css" type="text/css" />';
	}else if( trim($GLOBALS['system_caps']->oem) == "JOGAN"){
		echo '<link rel="stylesheet" href="/css/jogan.css" type="text/css" />';
	}else if( trim($GLOBALS['system_caps']->oem) == "OVERVIEW"){
		echo '<link rel="stylesheet" href="/css/overview.css" type="text/css" />';
	}else if( trim($GLOBALS['system_caps']->oem) == "LANACCESS"){
		echo '<link rel="stylesheet" href="/css/lanaccess.css" type="text/css" />';
    }else if( trim($GLOBALS['system_caps']->oem) == "MICROVIEW"){
		echo '<link rel="stylesheet" href="/css/microview.css" type="text/css" />';
	}else if( trim($GLOBALS['system_caps']->oem) == "WAVESTORE"){
		echo '<link rel="stylesheet" href="/css/wavestore.css" type="text/css" />';
	}

	
	if( trim($GLOBALS['system_caps']->oem) == "ESCA"
	   	|| trim($GLOBALS['system_caps']->oem) == "CDUS" 
		|| trim($GLOBALS['system_caps']->oem) == "INODIC" 
		|| trim($GLOBALS['system_caps']->oem) == "S1" 
		|| trim($GLOBALS['system_caps']->oem) == "SB" 
		|| trim($GLOBALS['system_caps']->oem) == "SEON" 
		|| trim($GLOBALS['system_caps']->oem) == "SEON1" 
		|| trim($GLOBALS['system_caps']->oem) == "SEON2"
		|| trim($GLOBALS['system_caps']->oem) == "SEON_LP" 
		|| trim($GLOBALS['system_caps']->oem) == "CBCA" 
		|| trim($GLOBALS['system_caps']->oem) == "ClickIT" 
		|| trim($GLOBALS['system_caps']->oem) == "HS" 
		|| trim($GLOBALS['system_caps']->oem) == "DTI" 
		|| trim($GLOBALS['system_caps']->oem) == "NEWGLAB" 
		|| trim($GLOBALS['system_caps']->oem) == "JCI" 
		|| trim($GLOBALS['system_caps']->oem) == "EUKLIS" 
		|| trim($GLOBALS['system_caps']->oem) == "STANLEY" 
		|| trim($GLOBALS['system_caps']->oem) == "_3XLOGIC" 
		|| trim($GLOBALS['system_caps']->oem) == "SONITROL"	
		|| trim($GLOBALS['system_caps']->oem) == "ACTIVEWITNESS" 
		|| trim($GLOBALS['system_caps']->oem) == "OPTEX" 
		|| trim($GLOBALS['system_caps']->oem) == "UR_SECURE"
		|| trim($GLOBALS['system_caps']->oem) == "JOGAN"
		|| trim($GLOBALS['system_caps']->oem) == "OVERVIEW"
		|| trim($GLOBALS['system_caps']->oem) == "LANACCESS"
        || trim($GLOBALS['system_caps']->oem) == "HI_NT"
	)
		echo '<link rel="stylesheet" href="/css/sb.css" type="text/css" />';  // ESCA, SB, CDUS, INODIC, S1, SEON, ClickIT, HS, DTI, NEWGLAB, JCI, EUKLIS, STANLEY, 3XLOGIC, SONITROL, HI_NT
}
?>
