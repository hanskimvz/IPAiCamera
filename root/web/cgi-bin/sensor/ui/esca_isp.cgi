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
<!--		<tr>
				<td><label class="subtitle" tkey="setup_av_hue">Hue</label></td>
				<td>
					<div class="slider_box">
						<div id="hue" name="hue" class="long"></div>  
						<label name="Hue_STR">0</label>
					</div>
				</td>
			</tr>
-->				
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
							<option value=0 tkey="setup_auto"> Auto </option>
							<option value=1 tkey="setup_manual_c"> Manual </option>
						</select>
					</div>
				</td>
			</tr>			
			<tr id="shutter_tr" >
				<td><label class="subtitle" tkey="setup_shutter">Shutter Speed</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_shutter">
							<option value=0> 1/30 </option>
							<option value=1> 1/60 </option>
							<option value=2> 1/120 </option>
							<option value=3> 1/250 </option>
							<option value=4> 1/700 </option>
							<option value=5> 1/1000</option>
							<option value=6> 1/2000 </option>
							<option value=7> 1/4000 </option>
							<option value=8> 1/8000</option>
							<option value=9> 1/16000</option>	
							<option value=10> 1/30000</option>
							<option value=11> 1/60000</option>															
						</select>
					</div>
				</td>
			</tr>

			<tr>
				<td><label class="subtitle" tkey="setup_gain_limit">Gain Limit</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="ae_gain_limit">
							<option value=0> 0dB </option>
							<option value=1> 2.1dB </option>
							<option value=2> 4.2dB </option>
							<option value=3> 6.3dB </option>
							<option value=4> 8.4dB </option>
							<option value=5> 10.5dB </option>
							<option value=6> 12.6dB </option>
							<option value=7> 14.7dB </option>
							<option value=8> 16.8dB </option>
							<option value=9> 18.9dB </option>
							<option value=10> 21dB </option>
							<option value=11> 23.1dB </option>
							<option value=12> 25.2dB </option>
							<option value=13> 27.3dB </option>
							<option value=14> 29.4dB </option>
							<option value=15> 31.5dB </option>	
							<option value=16> 33.6dB </option>
							<option value=17> 35.7dB </option>	
							<option value=18> 37.8dB </option>
							<option value=19> 39.9dB </option>
							<option value=20> 41dB </option>	
						
						</select>
					</div>
				</td>
			</tr>								
			<tr>
			<td><label class="subtitle" tkey="setup_slow_shutter">Slow Shutter</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="sshutter">
							<option value=0 tkey="off"> Off </option>
							<option value=1> 2x </option>
							<option value=2> 3x </option>
							<option value=3> 4x </option>
							<option value=4> 5x </option>
							<option value=5> 6x </option>
							<option value=6> 7x </option>
							<option value=7> 8x </option>																												
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
					<input id="tdn_sched" name="dnmode" type="radio" value=3>
					<label for="tdn_sched"></label><span tkey="setup_dn_sched"></span>
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
			<tr class="dn_threshold_tr">   
				<td><label class="subtitle" tkey="setup_color_level" >Threshold Level</label></td>
				<td>
					<div class="slider_box">
						<div id="tdn_color_level" name="tdn_color_level" class="long"></div>        
						<label name="tdn_color_level_STR">0</label>
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
					<label class="subtitle" tkey="setup_led_mode">IR LED Mode</label>
				</td>
				<td>
					<input id="led_mode_off" name="led_mode" type="radio" value=0>
					<label for="led_mode_off"></label><span tkey="off"></span>
					<input id="led_mode_on" name="led_mode" type="radio" value=1>
					<label for="led_mode_on"></label><span tkey="on"></span>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="setup_led_satu" >Threshold Level</label></td>
				<td>
					<div class="slider_box">
						<div id="led_satu" name="led_satu" class="long"></div>        
						<label name="led_satu_STR">0</label>
					</div>
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
							<option value='1' tkey="HLC"></option>
							<option value='2' tkey="BLC"></option>
							<option value='3' tkey="WDR"></option>							
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
							<option value=1> Outdoor </option>
							<option value=2> Indoor </option>
							<option value=3> Preset </option> 
							<option value=4> Manual </option>   
							<option value=5> Auto Ext </option>
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_Kelvin">Kelvin</label></td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="kelvin">
							<option value=0 tkey="setup_fc_low"> Low </option>
							<option value=1 tkey="setup_fc_middle"> Middle </option>
							<option value=2 tkey="setup_fc_high"> High </option>

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
			<tr class="div_wb_preset">
				<td><label class="subtitle" tkey="setub_push_trigger">psuh trigger</label></td>
				<td>
					<div style="margin-top: 8px;"><button name="wb_preset" class="button push" style="width:80px;height:22px;">PUSH</button></div>
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
					<div class="select">
						<select size="1" class="radius" name="dnr">
							<option value=0 tkey="setup_auto"> Off </option>
							<option value=1 tkey="setup_fc_low"> Low </option>
							<option value=2 tkey="setup_fc_middle"> Middle </option>
							<option value=3 tkey="setup_fc_high"> High </option>
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_defog">Defog</label></td>
	<!--		<td>
				<div class="select">
						<select size="1" class="radius" name="defog">
							<option value=0 tkey="off"> off </option>
							<option value=1 tkey="setup_auto"> auto </option>
							<option value=2 tkey="setup_manual_c"> manual </option>
						</select>
					</div>			
				</td> 
	 -->
				<td>
					<input id="defog_off" name="defog" type="radio" value=0>
					<label for="defog_off"></label><span tkey="off"></span>
					<input id="defog_auto" name="defog" type="radio" value=1>
					<label for="defog_auto"></label><span tkey="setup_auto"></span>
					<input id="defog_manual" name="defog" type="radio" value=2>
					<label for="defog_manual"></label><span tkey="setup_manual_c"></span>					
				</td>
			</tr>
			<tr class="defog_level">
				<td>
					<label class="subtitle" tkey="setup_defog_level">Image Stablilzer</label>
				</td>
				<td>
					<div class="select">
						<select size="1" class="radius" name="defog_level">
							<option value=0 tkey="setup_fc_low">  </option>
							<option value=1 tkey="setup_fc_middle">  </option>
							<option value=2 tkey="setup_fc_high">  </option>
						</select>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<label class="subtitle" tkey="setup_deblur">High resolution</label>
				</td>
				<td>
					<input id="deblur_off" name="deblur" type="radio" value=1>
					<label for="deblur_off"></label><span tkey="off"></span>
					<input id="deblur_on" name="deblur" type="radio" value=0>
					<label for="deblur_on"></label><span tkey="on"></span>
				</td>
			</tr>		
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
<div id="Video_Enhancement">
	<title>Video Enhancement</title>
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_flickerless">Anti Flicker</label></td>
				<td>
					<input id="flicker_off" name="a_flicker" type="radio" value=0>
					<label for="flicker_off"></label><span tkey="off">Off</span>
					<input id="flicker_on" name="a_flicker" type="radio" value=1>
					<label for="flicker_on"></label><span tkey="on">On</span>
				</td>
			</tr>
		</table>
	</div>
</div>
<div id="LV_Filter_Operation">
	<title>LV_Filter_Operation</title>
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_operation">Operation</label></td>
				<td>
					<input id="filter_operation_off" name="filter_operation" type="radio" value=0>
					<label for="filter_operation_off"></label><span tkey="off">Off</span>
					<input id="filter_operation_on" name="filter_operation" type="radio" value=1>
					<label for="filter_operation_on"></label><span tkey="on">On</span>
				</td>
			</tr>
			<tr>
				<td><label class="subtitle" tkey="setup_filter_mode">Mode</label></td>
				<td>
					<input id="filter_mode_off" name="filter_mode" type="radio" value=0>
					<label for="filter_mode_off"></label><span tkey="setup_auto">Auto</span>
					<input id="filter_mode_on" name="filter_mode" type="radio" value=1>
					<label for="filter_mode_on"></label><span tkey="setup_manual_c">Manual</span>
				</td>
			</tr>					
			<tr>
				<td><label class="subtitle" tkey="setup_enhance">Mode</label></td>
				<td>
					<input id="filter_enhance_auto" name="filter_enhance" type="radio" value=0>
					<label for="filter_enhance_auto"></label><span tkey="setup_auto">Auto</span>
					<input id="filter_enhance_fog" name="filter_enhance" type="radio" value=1>
					<label for="filter_enhance_fog"></label><span tkey="setup_fog">Fog</span>
					<input id="filter_enhance_night" name="filter_enhance" type="radio" value=2>
					<label for="filter_enhance_night"></label><span tkey="setup_night">Night</span>					
				</td>
			</tr>
								
<!--		<tr>   
				<td><label class="subtitle" tkey="setup_cb_offset">Cb gain</label></td>
				<td>
					<div class="slider_box">
						<div id="cb_offset" name="cb_offset" class="long"></div>        
						<label name="cb_offset_STR">0</label>
					</div>
				</td>
			</tr>	

			<tr>   
				<td><label class="subtitle" tkey="cr_offset">Cr gain</label></td>
				<td>
					<div class="slider_box">
						<div id="cr_offset" name="cr_offset" class="long"></div>        
						<label name="cr_offset_STR">0</label>
					</div>
				</td>
			</tr>
-->									
		</table>
	</div>
</div>
<div id="LV_Filter_Settings">
	<title>LV_Filter_Settings</title>
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_area">Mode</label></td>
				<td>
					<input id="filter_area_full" name="filter_area" type="radio" value=0>
					<label for="filter_area_full"></label><span tkey="setup_full">Full</span>
					<input id="filter_area_half" name="filter_area" type="radio" value=1>
					<label for="filter_area_half"></label><span tkey="setup_half">Half</span>
					<input id="filter_area_center" name="filter_area" type="radio" value=2>
					<label for="filter_area_center"></label><span tkey="setup_center">Center</span>					
				</td>
			</tr>			
			<tr class="div_enhance_level_a">   
				<td><label class="subtitle" tkey="setup_enhance_level">Night Detect</label></td>
				<td>
					<div class="slider_box">
						<div id="enhance_level_a" name="enhance_level_a" class="long"></div>        
						<label name="enhance_level_a_STR">0</label>
					</div>
				</td>
			</tr>
			<tr class="div_enhance_level_m">   
				<td><label class="subtitle" tkey="setup_enhance_level">Night Detect</label></td>
				<td>
					<div class="slider_box">
						<div id="enhance_level_m" name="enhance_level_m" class="long"></div>        
						<label name="enhance_level_m_STR">0</label>
					</div>
				</td>
			</tr>			
			<tr>   
				<td><label class="subtitle" tkey="setup_night_detect">Color enhance</label></td>
				<td>
					<div class="slider_box">
						<div id="night_detect" name="night_detect" class="long"></div>        
						<label name="night_detect_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="setup_color_enhance">3D-NR</label></td>
				<td>
					<div class="slider_box">
						<div id="color_enhance" name="color_enhance" class="long"></div>        
						<label name="color_enhance_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="3D-NR">Cb offset</label></td>
				<td>
					<div class="slider_box">
						<div id="3dnr" name="3dnr" class="long"></div>        
						<label name="3dnr_STR">0</label>
					</div>
				</td>
			</tr>		
			<tr>   
				<td><label class="subtitle" tkey="cb_gain">Cr offset</label></td>
				<td>
					<div class="slider_box">
						<div id="cb_gain" name="cb_gain" class="long"></div>        
						<label name="cb_gain_STR">0</label>
					</div>
				</td>
			</tr>
			<tr>   
				<td><label class="subtitle" tkey="cr_gain">Cr gain</label></td>
				<td>
					<div class="slider_box">
						<div id="cr_gain" name="cr_gain" class="long"></div>        
						<label name="cr_offset_STR">0</label>
					</div>
				</td>
			</tr>	
		</table>
	</div>
</div>
<div id="LV_Filter_Mode">
	<title>LV_Filter_Settings</title>
	<div>
		<table>
			<tr>
				<td><label class="subtitle" tkey="setup_filter_hw_dn_mode">Mode</label></td>
				<td>
					<input id="daynightmode" name="filter_hw_dn_mode" type="radio" value=0>
					<label for="daynightmode"></label><span tkey="setup_day&night">Full</span>
					<input id="lvhwfiltermode" name="filter_hw_dn_mode" type="radio" value=1>
					<label for="lvhwfiltermode"></label><span tkey="setup_LV_HW_Filter">Half</span>		
				</td>
			</tr>			
			<tr id="hwdnmode" >
				<td><label class="subtitle" tkey="setup_hwdnmode">hwdnmode</label></td>
				<td>
					<input id="hwdnmodeauto" name="filter_dn_mode" type="radio" value=2>
					<label for="hwdnmodeauto"></label><span tkey="setup_auto">auto</span>
					<input id="hwdnmodeoff" name="filter_dn_mode" type="radio" value=0>
					<label for="hwdnmodeoff"></label><span tkey="off_c">Off</span>
					<input id="hwdnmodeon" name="filter_dn_mode" type="radio" value=1>
					<label for="hwdnmodeon"></label><span tkey="on_c">On</span>	
				</td>
			</tr>	
			<tr>   
				<td><label class="subtitle" tkey="setup_filter_enable_threshold"</label></td>
				<td>
					<div class="slider_box">
						<div id="filter_enable_threshold" name="filter_enable_threshold" class="long"></div>        
						<label name="filter_enable_threshold_STR">0</label>
					</div>
				</td>
			</tr>			
			<tr>   
				<td><label class="subtitle" tkey="setup_filter_disable_threshold"</label></td>
				<td>
					<div class="slider_box">
						<div id="filter_disable_threshold" name="filter_disable_threshold" class="long"></div>        
						<label name="filter_disable_threshold_STR">0</label>
					</div>
				</td>
			</tr> 
			<tr>
				<td><label class="subtitle" tkey="setup_non_setting_time_mode">Mode</label></td>
				<td>
					<input id="non_time_setting_mode_disable" name="filter_non_time_setting_mode" type="radio" value=0>
					<label for="non_time_setting_mode_disable"></label><span tkey="off_c">Full</span>
					<input id="non_time_setting_mode_enable" name="filter_non_time_setting_mode" type="radio" value=1>
					<label for="non_time_setting_mode_enable"></label><span tkey="on_c">Half</span>		
				</td>
			</tr>				
			<tr class="tr_nonsettingtime">
				<td><label class="subtitle" tkey="setup_filter_disable_setting_time"></label></td>
				<td>
					<div class="select third">
						<select size="1" class="radius third" name="filter_disable_str_setting_hour"></select>
					</div>:
					<div class="select third">
						<select size="1" class="radius third" name="filter_disable_str_setting_min"></select>
					</div> ~ 					
					<div class="select third">
						<select size="1" class="radius third" name="filter_disable_end_setting_hour"></select>
					</div>:
					<div class="select third">
						<select size="1" class="radius third" name="filter_disable_end_setting_min"></select>
					</div>					
				</td>
				<td>

				</td>				
			</tr>
		</table>
	</div>
</div>
