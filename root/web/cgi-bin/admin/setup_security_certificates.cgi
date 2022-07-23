<?
require('../_define.inc');
require('../class/network.class');
require('../class/system.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration();
$cert   = $system_conf->Security->Certificates;

shmop_close($shm_id);
?>
<!DOCTYPE html>
<html>
	<body>
		<div class="contentTitle" tkey="cert_configuration"></div>
		<!-- [BEGIN] VIEW -->
		<div id="uiView" style="display:none;">
			<div class="content">
				<label class="maintitle" tkey="cert_server_client_certificate"></label>
				<div class="result_table">
					<table class="result_filed">
						<thead class="record_thead">
							<tr class="headline">
								<th class="th_cert_id">
									<span tkey="setup_cert_name"></span>
								</th>
								<th class="th_cert_issued">
									<span tkey="setup_issued_on"></span>
								</th>
								<th class="th_cert_expire">
									<span class="sb_margin_6" tkey="setup_expires_on"></span>
								</th>
							</tr>
						</thead>
						<tbody id="certificate">
						</tbody>
					</table>
				</div>
			</div>
			<button name="works" id="CreateSSC" class="button extralong" tkey="setup_create_self_signed_cert"></button>
			<button name="works" id="Properties" class="button width_100" tkey="setup_properties"></button>
			<button name="works" id="Delete" class="button width_98" tkey="setup_delete"></button><br>
			<button name="works" id="CreateCSR" class="button extralong" tkey="setup_create_cert_sign_req"></button>
			<button name="works" id="Install" class="button width_200" tkey="setup_cert_install"></button>

			<div class="content">
				<label class="maintitle" tkey="setup_ca_cert"></label>
				<div class="result_table">
					<table class="result_filed">
						<thead class="record_thead">
							<tr class="headline">
								<th class="th_cert_id">
									<span tkey="setup_cert_name"></span>
								</th>
								<th class="th_cert_issued">
									<span tkey="setup_issued_on"></span>
								</th>
								<th class="th_cert_expire">
									<span class="sb_margin_6" tkey="setup_expires_on"></span>
								</th>
							</tr>
						</thead>
						<tbody id="ca">
						</tbody>
					</table>
				</div>
			</div>
			<button name="works" id="CAInstall" class="button extralong" tkey="setup_cert_install"></button>
			<button name="works" id="CAProperties" class="button width_100" tkey="setup_properties"></button>
			<button name="works" id="CADelete" class="button width_98" tkey="setup_delete"></button><br>
		</div>
		<!-- [END] VIEW -->

		<!-- [BEGIN] VIEW (for Indigo Vision)-->
		<div id="uiView_IV" style="display:none;">
		<div id="div_ssc">
				<table id="cert_table">
					<tr>
						<td class="cert_font">Create self-signed certificate</td>
						<td><button name="works" id="CreateSSC" class="button width_200 button_cert" tkey="setup_create"></button></td>
					</tr>
					<tr>
						<td class="cert_font">Create certificate signing request</td>
						<td><button name="works" id="CreateCSR" class="button width_200 button_cert" tkey="setup_create_req"></button></td>
					</tr>
						<td class="cert_font">Installed Client Certificate</td>
						<td><button name="works" id="Install" class="button width_200 button_cert" tkey="setup_cert_install"></button></td>
					</tr>
				</table>
				<div class="content">
					<label class="maintitle" tkey="cert_server_client_certificate"></label>
					<div class="result_table">
						<table class="result_filed">
							<thead class="record_thead">
								<tr class="headline">
									<th class="th_cert_id">
										<span tkey="setup_cert_name"></span>
									</th>
									<th class="th_cert_issued">
										<span tkey="setup_issued_on"></span>
									</th>
									<th class="th_cert_expire">
										<span class="sb_margin_6" tkey="setup_expires_on"></span>
									</th>
								</tr>
							</thead>
							<tbody id="certificate">
							</tbody>
						</table>
					</div>
				</div>
				<div style="text-align:center;">
					<button name="works" id="Properties" class="button width_200" tkey="setup_properties"></button>
					<button name="works" id="Delete" class="button width_200" tkey="setup_delete_cert"></button><br>
				</div>
			</div>
			<hr class="cert_hr">

			<table id="cert_table">
				<tr>
					<td class="cert_font">Install CA certificate</td>
					<td><button name="works" id="CAInstall" class="button width_200 button_cert" tkey="setup_cert_install"></button></td>
				</tr>
			</table>
			<div class="content">
				<label class="maintitle" tkey="setup_ca_cert"></label>
				<div class="result_table">
					<table class="result_filed">
						<thead class="record_thead">
							<tr class="headline">
								<th class="th_cert_id">
									<span tkey="setup_cert_name"></span>
								</th>
								<th class="th_cert_issued">
									<span tkey="setup_issued_on"></span>
								</th>
								<th class="th_cert_expire">
									<span class="sb_margin_6" tkey="setup_expires_on"></span>
								</th>
							</tr>
						</thead>
						<tbody id="ca">
						</tbody>
					</table>
				</div>
			</div>
			<div style="text-align:center;">
				<button name="works" id="CAProperties" class="button width_200" tkey="setup_properties"></button>
				<button name="works" id="CADelete" class="button width_200" tkey="setup_delete_cert"></button><br>
			</div>

		</div>
		<!-- [END] VIEW -->

		<!-- [BEGIN] CERTIFICATE PROPERTIES -->
		<div class="dpnone" id="uiProperties">
			<div class="cert_properties">
				<div class="content">
					<label class="maintitle" tkey="Certificate"></label>
					<table>
						<tr>
							<th tkey="setup_name"></th>
							<td id="Name"></td>
						</tr>
						<tr>
							<th tkey="setup_version"></th>
							<td id="Version"></td>
						</tr>
						<tr>
							<th tkey="setup_serial_number"></th>
							<td id="SerialNumber"></td>
						</tr>
						<tr>
							<th><span tkey="setup_sign_algorithm"></span></th>
							<td><span id="CertSignAlgorithm"></span></td>
						</tr>
						<tr>
							<th><span tkey="setup_issuer"></span></th>
							<td><span id="Issuer"></span></td>
						</tr>
					</table>
				</div>
				<div class="content">
					<label class="maintitle" tkey="setup_validity"></label>
					<table>
						<tr>
							<th><span tkey="setup_issued_on"></span></th>
							<td><span id="NotBefore"></span></td>
						</tr>
						<tr>
							<th><span tkey="setup_expires_on"></span></th>
							<td><span id="NotAfter"></span></td>
						</tr>
						<tr>
							<th><span tkey="setup_subject"></span></th>
							<td id="Subject"></td>
						</tr>
						<tr>
							<th><span>SAN</span></th>
							<td id="SAN"></td>
						</tr>
					</table>
				</div>
				<div class="content">
					<label class="maintitle" tkey="setup_subject_public_key"></label>
					<table>
						<tr>
							<th><span tkey="setup_public_key_algirhtm"></span></th>
							<td><span id="PublicKeyAlgorithm"></span></td>
						</tr>
					</table>
				</div>
				<div class="content">
					<label class="maintitle" tkey="setup_rsa_public_key"></label>
					<table>
						<tr>
							<th><span tkey="setup_modulus"></span>(<span id="PublicKey"></span>bit)</th>
							<td style="word-wrap: break-word" id="Modulus"></td>
						</tr>
						<tr>
							<th><span tkey="setup_exponent"></span></th>
							<td><span id="Exponent"></span></td>
						</tr>
					</table>
				</div>
				<div class="content">
					<label class="maintitle" tkey=setup_signature></label>
					<table>
						<tr>
							<th><span tkey=setup_algorithm></span></th>
							<td><span id=SignatureAlgorithm></span></td>
						</tr>
						<tr>
							<th><span tkey=setup_signature></span></th>
							<td><span id="Signature"></span></td>
						</tr>
					</table>
				</div>
			</div>
			<center>
				<button type="button" name="works" class="button" id="Cancel" tkey="setup_cancel"></button>
			</center>
		</div>
		<!-- [END] CREATE PROPERTIES -->

		<!-- [BEGIN] CREATE SELF-SIGNED CERTIFICATE -->
		<div class="dpnone" id="uiCreateSSC">
			<form method="post" id="frmCreateSelfSignedCert">
				<div class="content">
					<label class="maintitle" tkey="setup_create_self_signed_cert"></label>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name" required><br>
					<label  class="subtitle" tkey="setup_expires_on"></label>
					<input type="text" name="expires" id="expires" required><label id="max_expires"></label><br>
					<label  class="subtitle" tkey="setup_country" ></label>
					<input type="text" name="country" id="country" class="short" placeholder="" maxlength="2" required><br>
					<label  class="subtitle" tkey="setup_state_province"></label>
					<input type="text" name="state" id="state" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_locality"></label>
					<input type="text" name="locality" id="locality" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_organization"></label>
					<input type="text" name="organization" id="organization" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_organization_unit"></label>
					<input type="text" name="organization_unit" id="organization_unit" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_common_name"></label>
					<input type="text" name="common_name" id="common_name" class="extra_long"><br>
					<label class="subtitle">RSA</label>
					<div class="select">
						<select id="rsa_mode">
							<option value="0">2048</option>
							<option value="1">4096</option>
						</select>
					</div><br>
					<label class="subtitle">SHA</label>
					<div class="select">
						<select id="sha_mode">
							<option value="0">1</option>
							<option value="1">256</option>
						</select>
					</div><br>
					<label  class="subtitle" tkey="setup_hostname1"></label>
					<input type="text" name="dns1" id="dns1" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_hostname2"></label>
					<input type="text" name="dns2" id="dns2" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_IP"></label>
					<input type="text" name="ip" id="ip" class="extra_long"><label><br>
				</div>
				<center>
					<button type="submit" class="button" id="btCreateSelfCertOk" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END] CREATE SELF-SIGNED CERTIFICATE -->
		<!-- [BEGIN] CREATE SELF-SIGNED CERTIFICATE (for Indigo Vision)-->
		<div class="dpnone" id="uiCreateSSC_IV">
			<form method="post" id="frmCreateSelfSignedCert">
				<div class="content">
					<label class="maintitle" tkey="setup_create_self_signed_cert"></label>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name" required><br>
					<label  class="subtitle" tkey="setup_expires_on"></label>
					<input type="text" name="expires" id="expires" required><label id="max_expires"></label><br>
					<label  class="subtitle" tkey="setup_country" ></label>
					<input type="text" name="country" id="country" class="short" placeholder="" maxlength="2" required> [2 Charaters ISO format country code. eg,US]<br>
					<label  class="subtitle" tkey="setup_state_province"></label>
					<input type="text" name="state" id="state" class="extra_long" required> [Full state or province name]<br>
					<label  class="subtitle" tkey="setup_locality"></label>
					<input type="text" name="locality" id="locality" class="extra_long" required> [Full city name]<br>
					<label  class="subtitle" tkey="setup_organization"></label>
					<input type="text" name="organization" id="organization" class="extra_long" required> [Organization name]<br>
					<label  class="subtitle" tkey="setup_organization_unit"></label>
					<input type="text" name="organization_unit" id="organization_unit" class="extra_long" required> [Division name]<br>
					<label  class="subtitle" tkey="setup_common_name"></label>
					<input type="text" name="common_name" id="common_name" class="extra_long" required><br>
					<label class="subtitle">RSA</label>
					<div class="select">
						<select id="rsa_mode">
							<option value="0">2048</option>
							<option value="1">4096</option>
						</select>
					</div><br>
					<label class="subtitle">SHA</label>
					<div class="select">
						<select id="sha_mode">
							<option value="0">1</option>
							<option value="1">256</option>
						</select>
					</div><br>
					<label  class="subtitle" tkey="setup_hostname1"></label>
					<input type="text" name="dns1" id="dns1" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_hostname2"></label>
					<input type="text" name="dns2" id="dns2" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_IP"></label>
					<input type="text" name="ip" id="ip" class="extra_long" required> [IP address of the device]<br>
				</div>
				<center>
					<button type="submit" class="button" id="btCreateSelfCertOk" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END] CREATE SELF-SIGNED CERTIFICATE -->

		<!-- [BEGIN] CREATE CERTIFICATE SIGNING REQUEST -->
		<div class="dpnone" id="uiCreateCSR">
			<form method="post" id="frmCreateCertSigningRequest">
				<div class="content">
					<label class="maintitle" tkey="setup_create_cert_sign_req"></label>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name" readonly><br>
					<label  class="subtitle" tkey="setup_country"></label>
					<input type="text" name="country" id="country" class="short" placeholder="" require><br>
					<label  class="subtitle" tkey="setup_state_province"></label>
					<input type="text" name="state" id="state" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_locality"></label>
					<input type="text" name="locality" id="locality" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_organization"></label>
					<input type="text" name="organization" id="organization" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_organization_unit"></label>
					<input type="text" name="organization_unit" id="organization_unit" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_common_name"></label>
					<input type="text" name="common_name" id="common_name" class="extra_long"><br>
					<label class="subtitle">SHA</label>
					<div class="select">
						<select id="sha_mode">
							<option value="0">1</option>
							<option value="1">256</option>
						</select>
					</div><br>
					<label  class="subtitle" tkey="setup_hostname1"></label>
					<input type="text" name="dns1" id="dns1" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_hostname2"></label>
					<input type="text" name="dns2" id="dns2" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_IP"></label>
					<input type="text" name="ip" id="ip" class="extra_long"><br>
				</div>
				<div class="dpnone content">
					<label class="maintitle" tkey="setup_certificate_req_create"></label>
					<textarea id="cert_req_create" oncontextmenu="event.cancleBubble=true" ondragstart="event.cancelBubble=true" onselectstart="event.cancelBubble=true;" readonly></textarea>
				</div>
				<center>
					<button type="submit" class="button" id="btnOK" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END] CREATE CERTIFICATE SIGNING REQUEST -->
		<!-- [BEGIN] CREATE CERTIFICATE SIGNING REQUEST (for Indigo Vision) -->
		<div class="dpnone" id="uiCreateCSR_IV">
			<form method="post" id="frmCreateCertSigningRequest">
				<div class="content">
					<label class="maintitle" tkey="setup_create_cert_sign_req"></label>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name"><br>
					<label  class="subtitle" tkey="setup_country"></label>
					<input type="text" name="country" id="country" class="short" placeholder="" require> [2-character ISO format country code. eg, US]<br>
					<label  class="subtitle" tkey="setup_state_province"></label>
					<input type="text" name="state" id="state" class="extra_long" required> [Full state or province name]<br>
					<label  class="subtitle" tkey="setup_locality"></label>
					<input type="text" name="locality" id="locality" class="extra_long" required> [Full city name]<br>
					<label  class="subtitle" tkey="setup_organization"></label>
					<input type="text" name="organization" id="organization" class="extra_long" required> [Organization name]<br>
					<label  class="subtitle" tkey="setup_organization_unit"></label>
					<input type="text" name="organization_unit" id="organization_unit" class="extra_long" required> [Division name]<br>
					<label  class="subtitle" tkey="setup_common_name"></label>
					<input type="text" name="common_name" id="common_name" class="extra_long" required> [Fully qualified domain name]<br>
					<label class="subtitle">RSA</label>
					<div class="select">
						<select id="rsa_mode">
							<option value="0">2048</option>
							<option value="1">4096</option>
						</select>
					</div><br>
					<label class="subtitle">SHA</label>
					<div class="select">
						<select id="sha_mode">
							<option value="0">1</option>
							<option value="1">256</option>
						</select>
					</div><br>
					<label  class="subtitle" tkey="setup_hostname1"></label>
					<input type="text" name="dns1" id="dns1" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_hostname2"></label>
					<input type="text" name="dns2" id="dns2" class="extra_long"><br>
					<label  class="subtitle" tkey="setup_IP"></label>
					<input type="text" name="ip" id="ip" class="extra_long" required> [IP address of the device]<br>
				</div>
				<div class="dpnone content">
					<label class="maintitle" tkey="setup_certificate_req_create"></label>
					<textarea id="cert_req_create" oncontextmenu="event.cancleBubble=true" ondragstart="event.cancelBubble=true" onselectstart="event.cancelBubble=true;" readonly></textarea>
				</div>
				<center>
					<button type="submit" class="button" id="btnOK" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END] CREATE CERTIFICATE SIGNING REQUEST -->
		<!-- [BEGIN]INSTALL UI -->
 		<div class="dpnone" id="uiInstall">
			<form method="post" id="frmInstall">
				<div class="content">
					<label class="maintitle" tkey="setup_cert_install"></label>
					<input type="radio" name="type" id="cert_csr" value="0">
					<label for="cert_csr"></label>
					<span tkey="setup_csr"></span><br>
					<input type="radio" name="type" id="cert_seperate_type" value="1">
					<label for="cert_seperate_type"></label>
					<span tkey="setup_cert_and_pkey"></span><br>
					<ul id="seperate_type">
						<li>
							<input type="radio" name="key_type" id="key_seperate_type" value="0">
							<label for="key_seperate_type"></label><span tkey="setup_use_seperate_key"></span><br>
							<div id="key_seperate">
								<label tkey="setup_private_key"></label>
								<div id="privkey_file" class="filebox disign_sel">
									<input type="file" name="key" id="key_file" />
									<label for="key_file" tkey="setup_system_selectfile"></label>
									<span id="key_file_name"></span>
								</div><br>
							</div>
						</li>
						<li>
							<input type="radio" name="key_type" id="key_pkcs12_type" value="1">
							<label for="key_pkcs12_type"></label><span tkey="setup_PKCS12"></span><br>
							<div id="key_password">
								<label tkey="setup_password"></label>
								<input type="password" id="password">
							</div>
						</li>
					</ul>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name"><br>
					<label  class="subtitle" tkey="setup_cert_file"></label>
					<div id="file" class="filebox disign_sel">
						<input type="file" name="certificate" id="cert_file" />
						<label for="cert_file" tkey="setup_system_selectfile"></label>
						<span id="cert_file_name"></span>
					</div><br>
				</div>
				<center>
					<button type="submit" class="button" id="btnOK" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END]INSTALL UI -->
		<!-- [BEGIN]INSTALL CA UI -->
 		<div class="dpnone" id="uiCAInstall">
			<form method="post" id="frmCAInstall">
				<div class="content">
					<label class="maintitle" tkey="setup_ca_install"></label>
					<label class="subtitle" tkey="setup_cert_name"></label>
					<input type="text" name="name" id="name"><br>
					<label  class="subtitle" tkey="setup_cert_file"></label>
					<div id="file" class="filebox disign_sel">
						<input type="file" name="ca" id="ca_file" />
						<label for="ca_file" tkey="setup_system_selectfile"></label>
						<span id="ca_file_name"></span>
					</div><br>
				</div>
				<center>
					<button type="submit" class="button" id="btnOK" tkey="setup_ok"></button>
					<button type="button" class="button" name="works" id="Cancel" tkey="setup_cancel"></button>
				</center>
			</form>
		</div>
		<!-- [END]INSTALL CA UI -->
		<script language="javascript">
			var certInfo= <? show_certificates($GLOBALS['cert']->Certificate, true);?>;
			var CAInfo =  <? show_certificates($GLOBALS['cert']->CA, true);?>;
			var APP_ERR_USED_CERTIFICATE = <? echo APP_ERR_USED_CERTIFICATE ?>;
			var APP_ERR_INVALID_COUNTRY_CODE = <? echo APP_ERR_INVALID_COUNTRY_CODE ?>;
		</script>
		<script src="./setup_security_certificates.js"></script>
	</body>
</html>
