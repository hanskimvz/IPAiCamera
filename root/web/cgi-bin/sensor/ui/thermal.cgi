<div id="Image_Enhancement">
	<div>
		<table>
			<tr name="setup_thermal_inverse">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_inverse">Inverse Control</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_inverse" id="thermal_inverse" class='radius'>
							<option value='0' tkey="off"></option>
							<option value='1' tkey="on"></option>
						</select>
					</div>
				</td>
			</tr>
			<tr name="setup_thermal_flip_mirror">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_flip_mirror">Flip / Mirror</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_flip" id="thermal_flip" class='radius'>
							<option value='0' >Flip : Off / Mirror : Off</option>
							<option value='1' >Flip : Off / Mirror : On</option>
							<option value='2' >Flip : On  / Mirror : Off</option>
							<option value='3' >Flip : On  / Mirror : On</option>
						</select>
					</div>
				</td>
			</tr>

			<tr name="set_thermal_color">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_color">Thermal Color</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_color" id="thermal_color" class='radius'>
							<option value='0' tkey="setup_thermal_color_gray"></option>
							<option value='1' tkey="setup_thermal_color_iron"></option>
							<option value='2' tkey="setup_thermal_color_purple"></option>
							<option value='3' tkey="setup_thermal_color_purple_yellow"></option>
							<option value='4' tkey="setup_thermal_color_rainbow"></option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Thermal_Settings">
	<div>
		<table>
			<tr name="setup_thermal_agc">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_agc">Auto Gain Control</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_agc" id="thermal_agc" class='radius'>
							<option value='0' tkey="off"></option>
							<option value='1' tkey="on"></option>
						</select>
					</div>
				</td>
			</tr>

			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_mgcc" >MGC Contrast</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_mgcc" name="thermal_mgcc" class="long"></div>        
						<label name="thermal_mgcc_value">0</label>
					</div>
				</td>
			</tr>

			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_mgcb" >MGC Brightness</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_mgcb" name="thermal_mgcb" class="long"></div>        
						<label name="thermal_mgcb_value">0</label>
					</div>
				</td>
			</tr>


			<tr name="setup_thermal_egde_mode">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_egde_mode">Edge Enhance Mode</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_edge_mode" id="thermal_edge_mode" class='radius'>
							<option value='0' tkey="off"></option>
							<option value='3' tkey="on"></option>
						</select>
					</div>
				</td>
			</tr>
			
			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_egde_level" >Image Enhance Value</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_edge_level" name="thermal_edge_level" class="long"></div>        
						<label name="thermal_edge_level_value">0</label>
					</div>
				</td>
			</tr>

			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_limit" >Contrast Enhancement</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_limit" name="thermal_limit" class="long"></div>        
						<label name="thermal_limit_value">0</label>
					</div>
				</td>
			</tr>

			
			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_gamma" >Gamma Correction</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_gamma" name="thermal_gamma" class="long"></div>        
						<label name="thermal_gamma_value">0</label>
					</div>
				</td>
			</tr>	

			<tr name="setup_thermal_denoise">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_denoise">De-Noise Filter</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_denoise" id="thermal_denoise" class='radius'>
							<option value='0' >Filter1 : Off / Filter2 : Off</option>
							<option value='1' >Filter1 : On  / Filter2 : Off</option>
							<option value='2' >Filter1 : Off / Filter2 : On</option>
							<option value='3' >Filter1 : On  / Filter2 : On</option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="Shutter_Settings">
	<div>
		<table>
			<tr name="setup_thermal_shutter_mode">
				<td>
					<label class="subtitle width160" tkey="setup_thermal_shutter_mode">Shutter Mode</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_shutter_mode" id="thermal_shutter_mode" class='radius'>
							<option value='0' tkey="temperature"></option>
							<option value='1' tkey="setup_time"></option>
							<!--<option value='2' tkey="setup_manual_c"></option>-->
						</select>
					</div>
				</td>
			</tr>

			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_shutter_time" >Shutter Time</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_shutter_time" name="thermal_shutter_time" class="long"></div>        
						<label name="thermal_shutter_time_value">0</label>
					</div>
				</td>
			</tr>

			<tr>   
				<td><label class="subtitle" tkey="setup_thermal_shutter_temp" >Shutter Temperature</label></td>
				<td>
					<div class="slider_box">
						<div id="thermal_shutter_temp" name="thermal_shutter_temp" class="long"></div>        
						<label name="thermal_shutter_temp_value">0</label>
					</div>
				</td>
			</tr>			

		</table>
	</div>
</div>
<!--
<div id="Factory_Reset">
	<div>
		<table>
			<tr name="Factory_Reset">
				<td>
					<label class="subtitle width160" tkey="Factory_Reset">Factory Reset</label>
				</td>
				<td>
					<div class="select">
						<select name="thermal_factory" id="thermal_factory" class='radius'>
							<option value='0' tkey="off"></option>
							<option value='1' tkey="on"></option>
						</select>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>
-->
