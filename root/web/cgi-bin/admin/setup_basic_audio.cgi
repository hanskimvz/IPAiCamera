<?
require('../_define.inc');
require('../class/system.class');
require('../class/capability.class');
require('../class/media.class');
require('../class/etc.class');

$shm_id       = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_caps  = new CCapability($shm_id);
$profile_conf = new CProfileConfiguration($shm_id);
$etc_conf     = new CEtcConfiguration($shm_id);
//$media_conf   = new CMediaConfiguration($shm_id);
//$profile_conf = $GLOBALS['media_conf']->ProfileConfig;
shmop_close($shm_id);

function getAudioProfileInformation($name)
{
	//echo $name.'.Token="'.trim($GLOBALS['profile_conf']->AudioEncoderConfiguration->Token).'";';
	//echo $name.'.Name="'.trim($GLOBALS['profile_conf']->AudioEncoderConfiguration->Name).'";';
	//echo $name.'.UseCount='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->UseCount.';';
	//echo $name.'.Bitrate='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Bitrate.';';
	//echo $name.'.SessionTimeout='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->SessionTimeout.';';
	//echo $name.'.input_format='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Format.';';

  if($GLOBALS['profile_conf']->AudioEncoderConfiguration->Encoding == 0)
    echo $name.'.input_encode=10;';
  else
	  echo $name.'.input_encode='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Encoding.';';
	echo $name.'.input_samplerate='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->SampleRate.';';
	echo $name.'.input_volume='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Volume.';';
	echo $name.'.input_AmpEnabled='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->AmpEnabled.';';
	echo $name.'.audio_enabled='.$GLOBALS['profile_conf']->AudioEncoderConfiguration->Enabled.';';
	$obj = $GLOBALS['etc_conf']->AudioEncoderOptions[0];
	echo $name.'.aac_supported='.$obj->bAACSupport.';';
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
		<title>AUDIO CONFIGURATION</title>
	</head>
	<body oncontextmenu="return false" onselectstart="return false"  ondragstart="return false">
		<div class="contentTitle"><span tkey="audio_configuration"></span></div>
		<div class="content">
			<label class="maintitle" colspan="2"><span tkey="audio_encode"></span></label>
			<div id="audio_on_off">
				<label class="subtitle"><span tkey="setup_system_audio"></label>
				<input type="radio" name="audio_enabled" value=1 id="audio_enable">
				<label for="audio_enable"></label><span tkey="on"></span>
				<input type="radio" name="audio_enabled" value=0 id="audio_disable">
				<label for="audio_disable"></label> <span tkey="off"></span><br>
			</div>
			<label class="subtitle"><span tkey="audio_codec"></label>
			<div class="select">
				<select id="input_encode">
					<option value=10>G.711 ulaw</option>
				</select>
			</div><br>
			<label class="subtitle"><span tkey="audio_volume"></label>
			<div class="select">
				<select id="input_volume"></select>
			</div><br>
			<label class="subtitle"><span tkey="audio_samplerate"></label>
			<div class="select">
				<select id="input_samplerate">
					<!--
					<option value=8000> 8,000 Hz</option>
					<option value=16000> 16,000 Hz</option>
					<option value=48000> 48,000 Hz</option>
					-->
				</select>
			</div><br>
			<!--
			<label class="subtitle"><span tkey="audio_format"></label>
			<div class="select">
				<select id="input_format">
					<option value=0> 16 Bit </option>
					<option value=1> 20 Bit </option>
					<option value=2> 24 Bit </option>
					<option value=3> 32 Bit </option>
				</select>
			</div><br>
			-->
			<div id="audio_amp_on_off">
				<label class="subtitle"><span>Amp Enable</span></label>
				<input type="radio" name="input_AmpEnabled" value="1" id="amp_on" >
				<label for="amp_on"></label><span tkey="on"></span>
				<input type="radio" name="input_AmpEnabled" value="0" id="amp_off" >
				<label for="amp_off"></label> <span tkey="off"></span><br>
			</div>
		</div>
		<center>
			<button class="button" id="btOK" type="button"><span tkey="setup_save"></span></button>
		</center>
	<script>
		var audioEnc = new Object;
		<?
			getAudioProfileInformation("audioEnc");
		?>
	</script>
	<script src="./setup_basic_audio.js"></script>
	</body>
</html>
