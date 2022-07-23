<?
// camera setup.


define('CAMERA_CODE_START'    , 0);
define('CAMERA_AE_LOCK'       , 1);
define('CAMERA_SHUTTER'     , 2);
define('CAMERA_SHUTTER_SPEED'       , 3);
define('CAMERA_AGC'   , 4);
define('CAMERA_DSS'    , 5);
define('CAMERA_AWB_MODE'       , 6);
define('CAMERA_WB_PRESET'       , 7);
define('CAMERA_KELVIN'     , 8);
define('CAMERA_R_GAIN'  , 9);
define('CAMERA_B_GAIN'    , 10);
define('CAMERA_SATURATION'    , 11);
define('CAMERA_BRIGHTNESS'      , 12);
define('CAMERA_SHARPNESS'  , 13);
define('CAMERA_WDR_BLC'        , 14);
define('CAMERA_WDR_LEVEL'        , 15);
define('CAMERA_MIRROR'           , 16);
define('CAMERA_FLIP'    , 17);
define('CAMERA_DEFOG'    , 18);
define('CAMERA_DEFOG_LEVEL'      , 19);
define('CAMERA_DNR'     , 20);
define('CAMERA_DEBLUR'     , 21);
define('CAMERA_ANTI_FLK'      , 22);
define('CAMERA_DN_MODE'     , 23);
define('CAMERA_TDN_BW_THRESHOLE'        , 24);
define('CAMERA_TDN_COLOR_THRESHOLE'          , 25);
define('CAMERA_IRLED_MODE'         , 26);
define('CAMERA_LED_SATU'    , 27);
define('CAMERA_TDN_COLOR_HOUR'           , 28);
define('CAMERA_TDN_COLOR_MIN'	  , 29);
define("CAMERA_TDN_BW_HOUR"		  , 30);
define("CAMERA_TDN_BW_MIN"	          , 31);
define("CAMERA_FILTER_OPERATION"	  , 32);
define("CAMERA_FILTER_MODE" , 33);
define("CAMERA_FILTER_ENHANCE"		  , 34);
define('CAMERA_FILTER_ENHANCE_LEVEL_A'   , 35);
define('CAMERA_FILTER_ENHANCE_LEVEL_M'   , 36);
define('CAMERA_FILTER_NIGHT_DETECT', 37);
define('CAMERA_FILTER_COLOR_ENHANCE' , 38);
define('CAMERA_FILTER_DNR'  , 39);
define('CAMERA_FILTER_CB_OFFSET'    , 40);
define('CAMERA_FILTER_CB_GAIN'     , 41);
define('CAMERA_FILTER_CR_OFFSET'       , 42);
define('CAMERA_FILTER_CR_GAIN'       , 43);
define('CAMERA_FILTER_AREA'       , 44);
define('CAMERA_FILTER_FOG_LEVEL'       , 45);
define('CAMERA_FILTER_HW_DN_MODE'    , 46);
define('CAMERA_FILTER_DN_MODE'    , 47);
define('CAMERA_FILTER_ENABLE_THRESHOLD'     , 48);
define('CAMERA_FILTER_DISABLE_THRESHOLD'     , 49);
define('CAMERA_FILTER_NON_TIME_SETTING_MODE'     , 50);
define('CAMERA_FILTER_DISABLE_STR_SETTING_HOUR'  , 51);
define('CAMERA_FILTER_DISABLE_STR_SETTING_MIN'   , 52);
define('CAMERA_FILTER_DISABLE_END_SETTING_HOUR'  , 53);
define('CAMERA_FILTER_DISABLE_END_SETTING_MIN'   , 54);
define('CAMERA_CODE_END'       , 55);


$list  = array("START",     
    "ae_lock",
	"ae_en", 
	"ae_shutter",
    "ae_gain_limit",
    "sshutter",
    "awb_mode",
    "wb_preset",
    "kelvin",
    "r_gain",
	"b_gain",
    "saturation",
	"brightness",
	"sharpness",
	"hdr",
	"hdr_level",
	"mirror",
	"flip",
     "defog",
    "defog_level",
	"dnr",	
	"deblur",
     "a_flicker",
     "dnmode",
	"tdn_bw_level",
	"tdn_color_level",		
	"led_mode",
    "led_satu",	
	"color_hour",
	"color_min",
	"bw_hour",
	"bw_min",		
    "filter_operation",
    "filter_mode",
    "filter_enhance",
    "enhance_level_a",
	"enhance_level_m",
    "night_detect",
    "color_enhance",
	"3dnr",
	"cb_offset",
	"cb_gain",
	"cr_offset",
	"cr_gain",
	"filter_area",
	"foglevel",
	"filter_hw_dn_mode",		
	"filter_dn_mode",
	"filter_enable_threshold",
	"filter_disable_threshold",
	"filter_non_time_setting_mode",
	"filter_disable_str_setting_hour",
	"filter_disable_str_setting_min",
	"filter_disable_end_setting_hour",
	"filter_disable_end_setting_min",		
);
?>
