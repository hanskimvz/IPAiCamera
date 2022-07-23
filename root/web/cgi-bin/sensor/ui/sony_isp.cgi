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
<!--
			<tr>
				<td><label class="subtitle" tkey="setup_av_contrast">Contrast</label></td>
				<td>
					<div class="slider_box">
						<div id="contrast" name="contrast" class="long"></div>  
						<label name="Contrast_STR">0</label>
					</div>
				</td>
			</tr>
-->			
			<tr>
				<td><label class="subtitle" tkey="setup_av_saturation">Saturation</label></td>
				<td>
					<div class="slider_box">
						<div id="saturation" name="saturation" class="long"></div>  
						<label name="Saturation_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
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
				<td><label class="subtitle" tkey="setup_av_aeenable">Auto Exposure</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_en">
							<option value=0> Auto </option>
							<option value=1> Manual </option>
							<option value=2> Shutter Priority </option>
							<option value=3> Iris Priority </option>
						    <option value=4> Bright Mode </option>
						</select>
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
			<tr id="shutter_tr" >
				<td><label class="subtitle" tkey="setup_shutter">Shutter Speed</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_shutter">
							<option value=0> 1/1 </option>
							<option value=1> 1/2 </option>
							<option value=2> 1/4 </option>
							<option value=3> 1/8 </option>
							<option value=4> 1/15 </option>
							<option value=5> 1/30 </option>
							<option value=6> 1/60 </option>
							<option value=7> 1/90 </option>
							<option value=8> 1/100 </option>
							<option value=9> 1/125 </option>
							<option value=10> 1/180 </option>
							<option value=11> 1/250 </option>
							<option value=12> 1/350 </option>
							<option value=13> 1/500 </option>
							<option value=14> 1/725</option>
							<option value=15> 1/1000</option>
							<option value=16> 1/1500 </option>
							<option value=17> 1/2000 </option>
							<option value=18> 1/3000 </option>
							<option value=19> 1/4000 </option>
							<option value=20> 1/6000</option>
							<option value=21> 1/10000</option>							
						</select>
					</div>
				</td>
			</tr>
			<tr id="ae_iris_tr">
				<td><label class="subtitle" tkey="setup_ae_iris">Iris</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_iris">
							<option value=0> close </option>
							<option value=1> F14 </option>
							<option value=2> F11 </option>
							<option value=3> F9.6 </option>
							<option value=4> F8 </option>
							<option value=5> F6.8 </option>
							<option value=6> F5.6 </option>
							<option value=7> F4.8 </option>
							<option value=8> F4 </option>
							<option value=9> F3.4 </option>
							<option value=10> F2.8 </option>
							<option value-11> F2.4 </option>
							<option value=12> F2 </option>	
							<option value=13> F1.6 </option>						
						</select>
					</div>
				</td>
			</tr>
			<tr id="ae_gain_tr">
				<td><label class="subtitle" tkey="setup_ae_gain">Gain</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_gain">
							<option value=1> 0dB </option>
							<option value=2> 3.6dB </option>
							<option value=3> 7.1dB </option>
							<option value=4> 10.7dB </option>
							<option value=5> 14.3dB </option>
							<option value=6> 17.8dB </option>
							<option value=7> 21.4dB </option>
							<option value=8> 25.0dB </option>
							<option value=9> 28.6dB </option>
							<option value=10> 32.1dB </option>
							<option value=11> 35.7dB </option>
							<option value=12> 39.3dB </option>
							<option value=13> 42.8dB </option>	
							<option value=14> 46.4dB </option>
							<option value=15> 50.0dB </option>														
						</select>
					</div>
				</td>
			</tr>						
			<tr id="ae_bright_tr">   
				<td><label class="subtitle" tkey="setup_bright" >Bright</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_bright">
							<option value=0> close/0dB </option>
							<option value=1> F14/0dB </option>
							<option value=2> F11/0dB </option>
							<option value=3> F9.6/0dB </option>
							<option value=4> F8/0dB </option>
							<option value=5> F6.8/0dB </option>
							<option value=6> F5.6/0dB </option>
							<option value=7> F4.8/0dB </option>
							<option value=8> F4/0dB </option>
							<option value=9> F3.4/0dB </option>
							<option value=10> F2.8/0dB </option>
							<option value=11> F2.4/0dB </option>
							<option value=12> F2/0dB </option>
							<option value=13> F1.6/0dB </option>
							<option value=14> F1.6/3.6dB </option>
							<option value=15> F1.6/7.1dB </option>
							<option value=16> F1.6/10.7dB </option>
							<option value=17> F1.6/14.3dB </option>
							<option value=18> F1.6/17.8dB </option>
							<option value=19> F1.6/21.4dB </option>
							<option value=20> F1.6/25.0dB </option>
							<option value=21> F1.6/28.6dB </option>
							<option value=22> F1.6/32.1dB </option>
							<option value=23> F1.6/35.7dB </option>
							<option value=24> F1.6/39.3dB </option>
							<option value=25> F1.6/42.8dB </option>	
							<option value=26> F1.6/46.4dB </option>
							<option value=27> F1.6/50.0dB </option>														
						</select>
					</div>				
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_slow_shutter">Slow Shutter</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="sshutter">
							<option value=0> Off </option>
							<option value=1> On </option>
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_gain_limit">Gain Limit</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="gain_limit">
							<option value=4> 10.7dB </option>
							<option value=5> 14.3dB </option>
							<option value=6> 17.8dB </option>
							<option value=7> 21.4dB </option>
							<option value=8> 25.0dB </option>
							<option value=9> 28.6dB </option>
							<option value=10> 32.1dB </option>
							<option value=11> 35.7dB </option>
							<option value=12> 39.3dB </option>
							<option value=13> 42.8dB </option>	
							<option value=14> 46.4dB </option>
							<option value=15> 50.0dB </option>	
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
					<input id="tdn_auto" name="dnmode" type="radio" value=0>
					<label for="tdn_auto"></label><span tkey="setup_auto" ></span>
					<input id="tdn_day" name="dnmode" type="radio" value=1>
					<label for="tdn_day"></label><span tkey="setup_dn_day" ></span>
					<input id="tdn_night" name="dnmode" type="radio" value=2>
					<label for="tdn_night"></label><span tkey="setup_dn_night"></span>
					<input id="tdn_sched" name="dnmode" type="radio" value=3>
					<label for="tdn_sched"></label><span tkey="setup_dn_sched"></span>
				</td>
			</tr>	
			<tr class="dn_threshold_tr">   
				<td><label class="subtitle" tkey="setup_color_level" >Threshold Level</label></td>
				<td>
					<div class="slider_box">
						<div id="tdn_color_level" name="tdn_color_level" class="long"></div>        
						<label name="tdn_color_level_STR">0</label>
					</div>
				</td>
			</tr>				
			<tr class="dn_threshold_tr">   
				<td><label class="subtitle" tkey="setup_bw_level" >Threshold Level</label></td>
				<td>
					<div class="slider_box">
						<div id="tdn_bw_level" name="tdn_bw_level" class="long"></div>        
						<label name="tdn_bw_level_STR">0</label>
					</div>
				</td>
			</tr>
			
			<tr class="iSchedule">
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
			<tr class="iSchedule">
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
			<tr>
				<td>
					<label class="subtitle" tkey="setup_hr_sens">High Sensitivity</label>
				</td>
				<td>
					<input id="hr_sens_off" name="hr_sens" type="radio" value=0>
					<label for="hr_sens_off"></label><span tkey="off"></span>
					<input id="hr_sens_on" name="hr_sens" type="radio" value=1>
					<label for="hr_sens_on"></label><span tkey="on"></span>
				</td>
			</tr>
			<tr class="ir_c_tr">
				<td>
					<label class="subtitle" tkey="setup_ir_c">IR correction</label>
				</td>
				<td>
					<input id="ir_c_off" name="ir_c" type="radio" value=0>
					<label for="ir_c_off"></label><span tkey="off"></span>
					<input id="ir_c_on" name="ir_c" type="radio" value=1>
					<label for="ir_c_on"></label><span tkey="on"></span>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Backlight_Switch">
	<div>
		<table>
			<tr name="support_hdr">
				<td><label class="subtitle width160" tkey="setup_av_hdr"></label></td>
				<td>
					<div class="select">
						<select name="hdr" id="hdr" class='radius'>
							<option value='0' tkey="off"></option>
							<option value='1' tkey="on"></option>
						</select>	
					</div>
				</td>
			</tr>
			<tr name="support_hdr">
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
			<tr name="support_blc">
				<td><label class="subtitle width160" tkey="setup_av_blc"></label></td>
				<td>
					<input id="blc_off" name="blc" type="radio" value=0 >
					<label for="blc_off"></label><span tkey="off">Off</span>
					<input id="blc_on" name="blc" type="radio" value=1>
					<label for="blc_on"></label><span tkey="on">On</span>
				</td>
			</tr>			
		</table>
	</div>
</div>

<div id="White_Balance">
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_awb_mode">White Balance Mode</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="awb_mode">
							<option value=0 tkey="setup_auto"> Auto </option>
							<option value=1> Indoor </option>
							<option value=2> Outdoor </option>
							<option value=3> ATW </option>
							<option value=4> One Push WB </option>  
							<option value=5> Manual </option>
							<option value=6> Outdoor Auto </option>
						</select>
					</div>
				</td>
			</tr>
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
				<td><label class="subtitle" tkey="setup_b_gain">B Gain</label></td>
				<td>
					<div class="slider_box">
						<div id="b_gain" name="b_gain" class="long"></div>        
						<label name="Bgain_STR">0</label>
					</div>
				</td>
			</tr>	
			<tr class="div_awb_one_push">
				<td><label class="subtitle" tkey="setub_push_trigger">psuh trigger</label></td>
				<td>
					<div style="margin-top: 8px;"><button name="awb_one_push" class="button push" >PUSH</button></div>
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
					<label class="subtitle" tkey="setup_dnr">Noise Reductionn</label>
				</td>
				<td>
					<div class="slider_box">
						<div id="dnr" name="dnr" class="long"></div>        
						<label name="dnr_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_defog">Defog</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="defog">
							<option value=0 tkey="off"> off </option>
							<option value=1> low </option>
							<option value=2> middle </option>
							<option value=3> high </option>

						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<label class="subtitle" tkey="setup_fc_stabilizer">Image Stablilzer</label>
				</td>
				<td>
					<input id="stabilizer_off" name="stabilizer" type="radio" value=0>
					<label for="stabilizer_off"></label><span tkey="off"></span>
					<input id="stabilizer_on" name="stabilizer" type="radio" value=1>
					<label for="stabilizer_on"></label><span tkey="on"></span>
				</td>
			</tr>
			<tr>
				<td>
					<label class="subtitle" tkey="setup_hr_mode">High resolution</label>
				</td>
				<td>
					<input id="hr_mode_off" name="hr_mode" type="radio" value=0>
					<label for="hr_mode_off"></label><span tkey="off"></span>
					<input id="hr_mode_on" name="hr_mode" type="radio" value=1>
					<label for="hr_mode_on"></label><span tkey="on"></span>
				</td>
			</tr>
<!--				
			<tr>
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
-->				
<!--			
			<tr>
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
-->			
<!--		<tr>
				<td>
					<label class="subtitle" tkey="setup_fc_push">Push</label>
				</td>
				<td>
					<button id="refresh" class="button"><span tkey="setup_push"></span></button>
				</td>
			</tr>
-->
		</table>
	</div>
</div>
<!--
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
-->
