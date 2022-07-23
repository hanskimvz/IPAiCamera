<div id="Image_Adjustment">
	<title>Color Settings</title>
	<div>
		<table>
			<tr>   
				<td><label class="subtitle" tkey="setup_av_sharpness">Sharpness</label></td>
				<td>
					<div class="slider_box">
						<div id="sharpness" name="sharpness" class="long"></div>
						<label name="EdgeGain_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="setup_av_brightness">Brightness</label></td>
				<td>
					<div class="slider_box">
						<div id="brightness" name="brightness" class="long"></div>        
						<label name="Brightness_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_av_contrast">Contrast</label></td>
				<td>
					<div class="slider_box">
						<div id="contrast" name="contrast" class="long"></div>  
						<label name="Contrast_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_av_saturation">Saturation</label></td>
				<td>
					<div class="slider_box">
						<div id="saturation" name="saturation" class="long"></div>  
						<label name="Saturation_STR">0</label>
					</div>
				</td>
			</tr>
			<tr id="ANPR">
				<td><label class="subtitle" tkey="setup_av_hue">Hue</label></td>
				<td>
					<div class="slider_box">
						<div id="hue" name="hue" class="long"></div>  
						<label name="Hue_STR">0</label>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Exposure_Settings">
	<div>
		<table>
			<tr>   
				<td><label class="subtitle" tkey="setup_av_aeenable">Auto Exposure </label></td>
				<td>
					<input id="ae_off" name="ae_en" type="radio" value=0>
					<label for="ae_off"></label><span tkey="off"> Disable</span>
					<input id="ae_on" name="ae_en" type="radio" value=1>
					<label for="ae_on"></label><span tkey ="on"> Enable</span>
				</td>
			</tr>
<!--			<tr>
				<td>
					<label class="subtitle" tkey="setup_av_localexpo" >Local Exposure</label>
				</td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="local_exp">
							<option value=0 tkey="off"> Off </option>
							<option value=1 tkey="setup_auto"> Auto </option>
							<option value=2> 1X </option>
							<option value=3> 2X </option>

							<option value=4> 3X </option>
							<option value=5> 4X </option>

						</select>
					</div>
				</td>
			</tr>
-->
      <tr id="shutter_limit_tr">
				<td style="vertical-align:top;"><label class="subtitle" tkey="setup_shutter_limit">Shutter Limit</label></td>
				<td>
          <div>
            <span style="display:inline-block; width:50px;">Max</span>
            <div class="select width_100">
              <select size="1" class="radius width_100" name="shutter_limit_max">
                </select>
            </div>
          </div>
          <div>
            <span style="display:inline-block; width:50px;">Min</span>
            <div class="select width_100">
            <select size="1" class="radius width_100" name="shutter_limit_min">
              </select>
            </div>
          </div>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="setup_ae_level" >Exposure Level</label></td>
				<td>
					<div class="slider_box">
						<div id="exp_level" name="exp_level" class="long"></div>        
						<label name="ExpLevel_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_ae_metering">AE Metering</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_meter">
							<option value=0 tkey="setup_ae_spot">  Spot </option>
							<option value=1 tkey="setup_ae_center"> Center </option>
							<option value=2 tkey="setup_ae_average"> Average </option>
							<!--<option value=3> Custom </option> -->
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_shutter">Shutter Speed</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="shutter">
							<option value=0> 1/15 </option>
							<option value=1> 1/25 </option>
							<option value=2> 1/30 </option>
							<option value=3> 1/50 </option>
							<option value=4> 1/60 </option>
							<option value=5> 1/100 </option>
							<option value=6> 1/120 </option>
							<option value=7> 1/240 </option>
							<option value=8> 1/480 </option>
							<option value=9> 1/600 </option>
							<option value=10> 1/1000 </option>
							<option value=11> 1/2000 </option>
							<option value=12> 1/4000 </option>
							<option value=13> 1/8000 </option>
							<option value=14> 1/16000</option>
							<option value=15> 1/32000</option>
						</select>
					</div>
				</td>
				<td id="m_shutter">
					<div class="m_check">
						<input type="checkbox" id="fixed_shutter" name="fixed_shutter" />
						<label for="fixed_shutter"></label>
						<span class="c_title" tkey="setup_fixed_shutter">Fixed Shutter</span>
					</div>
				</td>
			</tr>
			<tr id="max_shutter_limit_tr">
				<td><label class="subtitle" tkey="setup_max_shutter_limit">Max Shutter Limit</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="sshutter">
							<option value=0> Off </option>
							<option value=1> 1/120 </option>
							<option value=2> 1/240 </option>
							<option value=3> 1/480 </option>
							<option value=4> 1/960 </option>
							<option value=5> 1/2000 </option>
							<option value=6> 1/4000 </option>
						</select>
					</div>
				</td>
			</tr>
			<tr id="slow_shutter_limit_tr">
				<td><label class="subtitle" tkey="setup_slow_shutter">Slow Shutter</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="sshutter">
							<option value=0> Off </option>
							<option value=1> 1/2 </option>
							<option value=2> 1/3 </option>
							<option value=3> 1/5 </option>
							<option value=4> 1/6 </option>
							<option value=5> 1/7.5 </option>
							<option value=6> 1/10 </option>
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_gain_limit">Gain Limit</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="cam_gain">
							<option value=0> 0 db </option>
							<option value=1> 3 db</option>
							<option value=2> 6 db </option>
							<option value=3> 9 db </option>
							<option value=4> 12 db </option>
							<option value=5> 15 db </option>
							<option value=6> 18 db </option>
							<option value=7> 24 db </option>
							<option value=8> 30 db </option>
							<option value=9> 36 db </option>
							<option value=10> 42 db </option>
							<option value=11> 48 db </option>
							<option value=12> 54 db </option>
							<option value=13> 60 db </option>
							<option value=14> 66 db </option>
							<option value=15> 72 db </option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Day_Night_Settings">
	<div>
		<table>
			<tr>
				<td style="width:172px;"><label class="subtitle"><span tkey="setup_day_night_sub"></span></label></td>
				<td>
					<input id="tdn_auto" name="dnmode" type="radio" value=2>
					<label for="tdn_auto"></label><span tkey="setup_auto" ></span>
					<input id="tdn_day" name="dnmode" type="radio" value=0>
					<label for="tdn_day"></label><span tkey="setup_dn_day" ></span>
					<input id="tdn_night" name="dnmode" type="radio" value=1>
					<label for="tdn_night"></label><span tkey="setup_dn_night"></span>
					<input id="tdn_sched" name="dnmode" type="radio" value=5>
					<label for="tdn_sched"></label><span tkey="setup_dn_sched"></span>
				</td>
			</tr>
			<tr id="iColor_level">
				<td><label class="subtitle" tkey="setup_color_level">Color Level</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="tdn_color_level">
						</select>
					</div>
				</td>
			</tr>
			<tr id="iBw_level">
				<td><label class="subtitle" tkey="setup_bw_level">B/W Level</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="tdn_bw_level">
						</select>
					</div>
				</td>
			</tr>
			<tr id="iResp">
				<td><label class="subtitle" tkey="setup_transition_time">Transtion Time</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="tdn_resp">
							<option value=0 tkey="setup_slow"> slow </option>
							<option value=1 tkey="setup_middle"> middle </option>
							<option value=2 tkey="setup_fast"> fast </option>
						</select>
					</div>
				</td>
			</tr>
			<tr name="iSchedule">
				<td><label class="subtitle" tkey="setup_dn_night_time"></label></td>
				<td>
					<div class="select third">
						<select size="1" class="radius third" name="bw_hour"></select>
					</div>:
					<div class="select third">
						<select size="1" class="radius third" name="bw_min"></select>
					</div>
				</td>
			</tr>
			<tr name="iSchedule">
				<td><label class="subtitle" tkey="setup_dn_day_time"></label></td>
				<td>
					<div class="select third">
						<select size="1" class="radius third" name="color_hour"></select>
					</div>:
					<div class="select third">
						<select size="1" class="radius third" name="color_min"></select>
					</div>
				</td>
			</tr>
			<tr name="ir_mode">
				<td>
					<label class="subtitle" tkey="setup_ir_led_enable">IR Mode</label>
				</td>
				<td>
					<input id="ir_off" name="ir_enabled" type="radio" value=0>
					<label for="ir_off"></label><span tkey="setup_disable"></span>
					<input id="ir_on" name="ir_enabled" type="radio" value=1>
					<label for="ir_on"></label><span tkey="setup_enable"></span>
				</td>
			</tr>
			<tr name="iir_strength">
				<td>
					<label class="subtitle" tkey="setup_ir_led_strength">IR Strength</label>
				</td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ir_strength">
							<option value=1 > 1 </option>
							<option value=2 > 2 </option>
							<option value=3 > 3 </option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Backlight_Switch">
	<div>
		<table>
			<tr name="support_blc">
				<td><label class="subtitle width160" tkey="setup_av_blc"></label></td>
				<td>
					<input id="blc_off" name="blc" type="radio" value=0 >
					<label for="blc_off"></label><span tkey="off">Off</span>
					<input id="blc_on" name="blc" type="radio" value=1>
					<label for="blc_on"></label><span tkey="on">On</span>
				</td>
			</tr>
			<tr name="support_hdr">
				<td><label class="subtitle width160" tkey="setup_av_hdr"></label></td>
				<td>
					<div class="select">
						<select name="hdr" id="hdr" class='radius'>
							<option value='0' tkey="off"></option>
							<!--
							<option value='1' tkey="setup_wdr_2x_on"></option>
							<option value=15>Sensor WDR</option>
							-->
						</select>	
					</div>
				</td>
			</tr>
			<tr name="support_hdr_level">
				<td><label class="subtitle width160" tkey="setup_av_hdr_level"></label></td>
				<td>
					<div class="select">
						<select name="hdr_level" id="hdr_level" class='radius'>
							<option value='0' tkey="setup_fc_low"></option>
							<option value='1' tkey="setup_fc_middle"></option>
							<option value='2' tkey="setup_fc_high"></option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="White_Balance">
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_awb_enable">Auto White Balance</label></td>
				<td>
					<input id="awb_off" name="awb_en" type="radio" value=0>
					<label for="awb_off"></label><span tkey="off">Off</span>
					<input id="awb_on" name="awb_en" type="radio" value=1>
					<label for="awb_on"></label><span tkey="on">On</span>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_awb_mode">White Balance Mode</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="awb_mode">
<!--							<option value=0 tkey="setup_auto"> Auto </option>
							<option value=1> 2800K </option>
							<option value=2> 4000K </option>
							<option value=3> 5000K </option>
							<option value=4> 6500K </option>
							<option value=5> 7500K </option>
							<option value=6 tkey="setup_flash"> Flash </option>
							<option value=7 tkey="setup_fluorescent"> Fluorescent </option>
							<option value=8 tkey="setup_fluorescent_h"> Fluorescent_H </option>
							<option value=9 tkey="setup_underwater"> Underwater </option>
							<option value=10 tkey="main_manual"> Manual </option>
-->							
						</select>
					</div>
				</td>
			</tr>
<!--
			<tr>
				<td><label class="subtitle" tkey="setup_awb_method">White Balance Method</label></td>
				<td>
					<div id="awb_method" class="select">
						<select size="1" class="radius" name="awb_method">
							<option value=0> Normal </option>
							<option value=1> Custom </option>
							<option value=2> Grey world </option>
						</select>
					</div>
				</td>
			</tr>
-->
			<tr>
				<td><label class="subtitle" tkey="setup_r_gain">R Gain</label></td>
				<td>
					<div class="slider_box">
						<div id="r_gain" name="r_gain" class="long"></div>        
						<label name="Rgain_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_g_gain">G Gain</label></td>
				<td>
					<div class="slider_box">
						<div id="g_gain" name="g_gain" class="long"></div>        
						<label name="Ggain_STR">0</label>
					</div>
				</td>
			</tr>
			<tr >
				<td><label class="subtitle" tkey="setup_b_gain">B Gain</label></td>
				<td>
					<div class="slider_box">
						<div id="b_gain" name="b_gain" class="long"></div>        
						<label name="Bgain_STR">0</label>
					</div>
				</td>
			</tr>	
		</table>
	</div>
</div>

<div id="Image_Enhancement">
	<div>
		<table>
			<tr>
				<td>
					<label class="subtitle" tkey="setup_fc_mctf">3D Noise Reduction</label>
				</td>
				<td>
					<div class="slider_box">
						<div id="mctf3dnr" name="mctf3dnr" class="long"></div>        
						<label name="Mctf3dnr_STR">0</label>
					</div>
				</td>
			</tr>
<!--
			<tr>
				<td>
					<label class="subtitle" tkey="setup_fc_mctf">MCTF 3D NR</label>
				</td>
				<td>
					<input id="mctf3dnr_off" name="mctf3dnr" type="radio" value=0>
					<label for="mctf3dnr_off"></label><span tkey="off">Off</span>
					<input id="mctf3dnr_low" name="mctf3dnr" type="radio" value=1>
					<label for="mctf3dnr_low"></label><span tkey="setup_low">Low</span>                   
					<input id="mctf3dnr_mid" name="mctf3dnr" type="radio" value=2>
					<label for="mctf3dnr_mid"></label><span tkey="setup_middle">Mid</span>                   
					<input id="mctf3dnr_high" name="mctf3dnr" type="radio" value=3>
					<label for="mctf3dnr_high"></label><span tkey="setup_high">High</span>                   
				</td>
			</tr>
-->
			<tr name="set_mirror">
				<td>
					<label class="subtitle" tkey="setup_fc_mirror">Mirror</label>
				</td>
				<td>
					<input id="mirror_off" name="mirror" type="radio" value=0>
					<label for="mirror_off"></label><span tkey="off"></span>
					<input id="mirror_on" name="mirror" type="radio" value=1>
					<label for="mirror_on"></label><span tkey="on"></span>
				</td>
			</tr>
			<tr name="set_flip">
				<td>
					<label class="subtitle" tkey="setup_fc_flip">Flip</label>
				</td>
				<td>
					<input id="flip_off" name="flip" type="radio" value=0>
					<label for="flip_off"></label><span tkey="off"></span>
					<input id="flip_on" name="flip" type="radio" value=1>
					<label for="flip_on"></label><span tkey="on"></span>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Video_Enhancement">
	<title>Video Enhancement</title>
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_flickerless">Anti Flicker</label></td>
				<td>
					<input id="flicker50" name="a_flicker" type="radio" value=0>
					<label for="flicker50"></label><span>50Hz</span>
					<input id="flicker60" name="a_flicker" type="radio" value=1>
					<label for="flicker60"></label><span>60Hz</span>
				</td>
			</tr>
		</table>
	</div>
</div>
