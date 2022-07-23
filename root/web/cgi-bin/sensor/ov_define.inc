<?
// camera setup.

define('CAMERA_CODE_START'    , 0);
define('CAMERA_AE_MODE'       , 1);
define('CAMERA_EXP_MODE '     , 2);
define('CAMERA_EXP_LEVEL'     , 3);
define('CAMERA_AE_SPOT'       , 4);
define('CAMERA_AE_SPOT_POS'   , 5);
define('CAMERA_AE_SHUTTER'    , 6);
define('CAMERA_AE_IRIS'       , 7);
define('CAMERA_AE_GAIN'       , 8);
define('CAMERA_AE_BRIGHT'     , 9);
define('CAMERA_SLOW_SHUTTER'  , 10);
define('CAMERA_SLOW_SHUTTER_LIMIT'  , 11);
define('CAMERA_AGC'    , 12);
define('CAMERA_AWB_ENABLE'    , 13);
define('CAMERA_AWB_MODE'      , 14);
define('CAMERA_AWB_ONE_PUSH'  , 15);
define('CAMERA_R_GAIN'        , 16);
define('CAMERA_B_GAIN'        , 17);
define('CAMERA_CHROMA_GAIN'   , 18);
define('CAMERA_HUE'           , 19);
define('CAMERA_SATURATION'    , 20);
define('CAMERA_BRIGHTNESS'    , 21);
define('CAMERA_CONTRAST'      , 22);
define('CAMERA_SHARPNESS'     , 23);
define('CAMERA_BACKLIGHT'     , 24);
define('CAMERA_WDR_MODE'      , 25);
define('CAMERA_WDR_LEVEL'     , 26);
define('CAMERA_MIRROR'        , 27);
define('CAMERA_FLIP'          , 28);
define('CAMERA_DEFOG'         , 29);
define('CAMERA_STABILIZER'    , 30);
define('CAMERA_DNR'           , 31);
define('CAMERA_A_FLICKER'	  , 32);
define('CAMERA_DN_MODE'		  , 33);
define('CAMERA_DN_THRESHOLE'   , 34);
define('CAMERA_TDN_BW_LEVEL'   , 35);
define('CAMERA_TDN_COLOR_LEVEL'   , 36);
define('CAMERA_CHROMA_SUPPRESS', 37);
define('CAMERA_TDN_COLOR_HOUR' , 38);
define('CAMERA_TDN_COLOR_MIN'  , 39);
define('CAMERA_TDN_BW_HOUR'    , 40);
define('CAMERA_TDN_BW_MIN'     , 41);
define('CAMERA_WL_MODE'        , 42);
define('CAMERA_IR_MODE'        , 43);
define('CAMERA_CODE_END'       , 44);


$list  = array("START",     
    "ae_en",
	"exp_mode", 
	"exp_level", 
	"ae_spot",
	"ae_spot_pos",
    "ae_shutter",
    "ae_iris",
    "ae_gain",
    "ae_bright",
    "sshutter",
    "sshutter_limit",
    "agc",
    "awb_en",
	"awb_mode",
	"awb_one_push",
    "r_gain",
	"b_gain",
	"chroma_gain",
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
	"a_flicker",
    "dnmode",
    "dn_threshold",
	"tdn_bw_level",
	"tdn_color_level",		
	"chromas",
	"color_hour",
	"color_min",
	"bw_hour",
	"bw_min",
	"wlmode",
	"irmode",
);
?>
