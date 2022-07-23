<?
// camera setup.

define('CAMERA_CODE_START'    , 0);
define('CAMERA_AE_MODE'       , 1);
define('CAMERA_EXP_LEVEL'     , 2);
define('CAMERA_AE_SPOT'       , 3);
define('CAMERA_AE_SPOT_POS'   , 4);
define('CAMERA_AE_SHUTTER'    , 5);
define('CAMERA_AE_IRIS'       , 6);
define('CAMERA_AE_GAIN'       , 7);
define('CAMERA_AE_BRIGHT'     , 8);
define('CAMERA_SLOW_SHUTTER'  , 9);
define('CAMERA_GAIN_LIMIT'    , 10);
define('CAMERA_AWB_ENABLE'    , 11);
define('CAMERA_AWB_MODE'      , 12);
define('CAMERA_AWB_ONE_PUSH'  , 13);
define('CAMERA_R_GAIN'        , 14);
define('CAMERA_B_GAIN'        , 15);
define('CAMERA_HUE'           , 16);
define('CAMERA_SATURATION'    , 17);
define('CAMERA_BRIGHTNESS'    , 18);
define('CAMERA_CONTRAST'      , 19);
define('CAMERA_SHARPNESS'     , 20);
define('CAMERA_BACKLIGHT'     , 21);
define('CAMERA_WDR_MODE'      , 22);
define('CAMERA_WDR_LEVEL'     , 23);
define('CAMERA_MIRROR'        , 24);
define('CAMERA_FLIP'          , 25);
define('CAMERA_DEFOG'         , 26);
define('CAMERA_STABILIZER'    , 27);
define('CAMERA_DNR'           , 28);
define('CAMERA_A_FLICKER'	  , 29);
define("CAMERA_HR_MODE"		  , 30);
define("CAMERA_HLC"	          , 31);
define("CAMERA_HIGH_SENS"	  , 32);
define("CAMERA_IR_CORRECTION" , 33);
define("CAMERA_DN_MODE"		  , 34);
define('CAMERA_DN_THRESHOLE'   , 35);
define('CAMERA_TDN_BW_LEVEL'   , 36);
define('CAMERA_TDN_COLOR_LEVEL'   , 37);
define('CAMERA_CHROMA_SUPPRESS', 38);
define('CAMERA_TDN_COLOR_HOUR' , 39);
define('CAMERA_TDN_COLOR_MIN'  , 40);
define('CAMERA_TDN_BW_HOUR'    , 41);
define('CAMERA_TDN_BW_MIN'     , 42);
define('CAMERA_CODE_END'       , 43);


$list  = array("START",     
    "ae_en",
	"exp_level", 
	"ae_spot",
	"ae_spot_pos",
    "ae_shutter",
    "ae_iris",
    "ae_gain",
    "ae_bright",
    "sshutter",
    "gain_limit",
    "awb_en",
	"awb_mode",
	"awb_one_push",
    "r_gain",
	"b_gain",
	"hue",
	"saturation",
	"brightness",
	"contrast",
	"sharpness",
	"blc",
	"hdr",
	"hdr_level",
	"mirror",
	"flip",
    "defog",
    "stabilizer",
	"dnr",
    "flip",	
    "hr_mode",
    "hlc",
    "hr_sens",
    "ir_c",
    "dnmode",
    "dn_threshold",
	"tdn_bw_level",
	"tdn_color_level",		
	"chromas",
	"color_hour",
	"color_min",
	"bw_hour",
	"bw_min",
);
?>
