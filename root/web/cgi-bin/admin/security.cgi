<?
require('../_define.inc');
require('../class/system.class');
require('../class/socket.class');
require('../class/capability.class');

$shm_id = shmop_open(KEY_SM_SHARED_CONFIG, "a", 0, 0);
$system_conf = new CSystemConfiguration($shm_id);
$security_conf = $system_conf->Security;
$system_caps = new CCapability($shm_id);
shmop_close($shm_id);
$newCertInfo = new CNewCertificateConf();
$delCertInfo = new CCertificate();
$properties = New CCertificateProperties();
$CSR = new CCreateCSR();
$install_cert = new CInstallCertificateConfiguration();
$isJson = false;
$get_oem = $system_caps->getOEM();
//////////////////////////////// RTSP_AUTHENTICATION /////////////////////////////
function change_rtsp_authentication()
{
	if( !isset($_REQUEST['AuthEnabled'] ) ) return 1;
		$GLOBALS['security_conf']->RtspAuthentication->AuthEnabled=$_REQUEST['AuthEnabled'];
	return 0;
} 
function change_rtsp_auth_enabled() 
{
	if( change_rtsp_authentication() < 0 ) return -1;
	return 0;
}

function rtsp_authentication_view_post() 
{
	echo "RtspAuthentication=".	$GLOBALS['security_conf']->RtspAuthentication->AuthEnabled . "\r\n";
}
//////////////////////////////// SERVICE /////////////////////////////
/*
function change_service_telnet()
{
	if( !isset($_REQUEST['support_telnet'] ) ) return 1;
	$GLOBALS['security_conf']->SystemService->SupportTelnet=$_REQUEST['support_telnet'];
	return 0;
} 
*/
function change_service_ssh()
{
	if( !isset($_REQUEST['support_ssh'] ) ) return 1;
	$GLOBALS['security_conf']->SystemService->SupportSSH=$_REQUEST['support_ssh'];
	return 0;
} 
function change_service() 
{
//    if( change_service_telnet() < 0 ) return -1;
	if( change_service_ssh() < 0 ) return -1;
	return 0;
}

function service_view_post() 
{
//	echo "support_telnet=".	$GLOBALS['security_conf']->SystemService->SupportTelnet . "\r\n";
	echo "support_ssh=".	$GLOBALS['security_conf']->SystemService->SupportSSH . "\r\n";
}
//////////////////////////////////////////////////////////////////////


//////////////////////////////// AUTOLOCK /////////////////////////////
function change_autolock_enabled()
{
	if( !isset($_REQUEST['AutoLockEnabled'] ) ) return 1;
	$GLOBALS['security_conf']->AutoLock->AutoLockEnabled=$_REQUEST['AutoLockEnabled'];
	return 0;
} 
function change_autolock_attemp()
{
	if( !isset($_REQUEST['AutoLockAttempt'] ) ) return 1;
	$GLOBALS['security_conf']->AutoLock->AutoLockAttempt=$_REQUEST['AutoLockAttempt'];
	return 0;
} 
function change_autolock() 
{
    if( change_autolock_enabled() < 0 ) return -1;
	if( change_autolock_attemp() < 0 ) return -1;
	return 0;
}

function autolock_view_post() 
{
	echo "AutoLockEnabled=".	$GLOBALS['security_conf']->AutoLock->AutoLockEnabled . "\r\n";
	echo "AutoLockAttempt=".	$GLOBALS['security_conf']->AutoLock->AutoLockAttempt . "\r\n";
}
//////////////////////////////////////////////////////////////////////


///////////////////////////// IP_FILTER //////////////////////////////
function ip_filter_view_post()
{
	show_ip_filter($GLOBALS['security_conf']->IpFilter);
}
function change_ip_filter_enabled()
{
	if( !isset($_REQUEST['enabled']) ) return 1;
	$GLOBALS['security_conf']->IpFilter->Enabled = $_REQUEST['enabled'];
	return 0;
}
function change_ip_filter_type()
{
	if( !isset($_REQUEST['type']) ) return 1;
	$GLOBALS['security_conf']->IpFilter->Type = $_REQUEST['type'];
	return 0;
}
function change_ip_filter()
{
	if( change_ip_filter_enabled() < 0 ) return -1;
	if( change_ip_filter_type() < 0 ) return -1;
	return 0;	
}
function change_ip_filter_add_address()
{
    if( isset($_REQUEST['address']) )
    {
        if (filter_var($_REQUEST['address'], FILTER_VALIDATE_IP,FILTER_FLAG_IPV4))
        {
            return 0;
        }
    }
    return 1;
}
function change_ip_filter_remove_address()
{
	if( !isset($_REQUEST['address']) ) return 1;
	return 0;
}
//////////////////////////////////////////////////////////////////////

/////////////////////////////  802.1X  //////////////////////////////
function ieee8021x_view_post()
{
	show_ieee8021x($GLOBALS['security_conf']->IEEE8021X);
}
function change_ieee8021x_enabled()
{
	if( !isset($_REQUEST['enabled']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->Enabled = $_REQUEST['enabled'];
	return 0;
}
function change_ieee8021x_protocol()
{
	if( !isset($_REQUEST['protocol']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->Protocol = $_REQUEST['protocol'];
	return 0;
}
function change_ieee8021x_epol_version()
{
	if( !isset($_REQUEST['eapol_version']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->EAPOLVersion = $_REQUEST['eapol_version'];
	return 0;
}
function change_ieee8021x_id()
{
	if( !isset($_REQUEST['id']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->UserName= $_REQUEST['id'];
	return 0;
}
function change_ieee8021x_password()
{
	if( !isset($_REQUEST['password']) ) return 1;
    if ( strlen($_REQUEST['password']) > 30 || strlen($_REQUEST['password']) < 8 ) return -1;
	$GLOBALS['security_conf']->IEEE8021X->Password = $_REQUEST['password'];
	return 0;
}
function change_ieee8021x_cert_id()
{
	if( !isset($_REQUEST['cert_id']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->TargetCert->Id = $_REQUEST['cert_id'];
	return 0;
}
function change_ieee8021x_ca_id()
{
	if( !isset($_REQUEST['ca_id']) ) return 1;
	$GLOBALS['security_conf']->IEEE8021X->TargetCA->Id = $_REQUEST['ca_id'];
	return 0;
}
function change_ieee8021x()
{
	if( change_ieee8021x_enabled() < 0 ) return -1;
	if( change_ieee8021x_protocol() < 0 ) return -1;
	if( change_ieee8021x_epol_version() < 0 ) return -1;
	if( change_ieee8021x_id() < 0 ) return -1;
	if( change_ieee8021x_password() < 0 ) return -1;
	if( change_ieee8021x_cert_id() < 0 ) return -1;
	if( change_ieee8021x_ca_id() < 0 ) return -1;
	
	return 0;
}
//////////////////////////////////////////////////////////////////////

///////////////////////////// certificate //////////////////////////////
function create_self_signed_cert_name()
{
	if( !isset($_REQUEST['name']) ) return -1;
	$GLOBALS["newCertInfo"]->Name = $_REQUEST['name'];
	return 0;
}
function create_self_signed_cert_country()
{
	if( !isset($_REQUEST['country'])) return -1;
	$GLOBALS["newCertInfo"]->Country = $_REQUEST['country'];
	return 0;
}
function create_self_signed_cert_expires()
{
	if( !isset($_REQUEST['expires']) ) return -1;
	$GLOBALS["newCertInfo"]->Expires = $_REQUEST['expires'];
	return 0;
}
function create_self_signed_cert_state()
{
	if( !isset($_REQUEST['state']) ) return 1;	
	$GLOBALS["newCertInfo"]->State = $_REQUEST['state'];
	return 0;
}
function create_self_signed_cert_locality()
{
	if( !isset($_REQUEST['locality']) ) return 1;
	$GLOBALS["newCertInfo"]->Locality = $_REQUEST['locality'];
	return 0;
}
function create_self_signed_cert_organization()
{
	if( !isset($_REQUEST['organization']) ) return 1;
	$GLOBALS["newCertInfo"]->Organization = $_REQUEST['organization'];
	return 0;
}
function create_self_signed_cert_organization_unit()
{
	if( !isset($_REQUEST['organization_unit'] ) ) return 1;
	$GLOBALS["newCertInfo"]->OrganizationUnit = $_REQUEST['organization_unit'];
	return 0;
}
function create_self_signed_cert_common_name()
{
	if( !isset($_REQUEST['common_name']) ) return 1;
	$GLOBALS["newCertInfo"]->CommonName = $_REQUEST['common_name'];
	return 0;
}
function create_self_signed_cert_rsa_mode()
{
	if( !isset($_REQUEST['rsa_mode']) ) return 1;
	$GLOBALS["newCertInfo"]->RSAMode= $_REQUEST['rsa_mode'];
	return 0;
}
function create_self_signed_cert_sha_mode()
{
	if( !isset($_REQUEST['sha_mode']) ) return 1;
	$GLOBALS["newCertInfo"]->SHAMode= $_REQUEST['sha_mode'];
	return 0;
}
function create_self_signed_cert_san()
{
	if( isset($_REQUEST['ip']) ||
        isset($_REQUEST['dns1']) ||
        isset($_REQUEST['dns2'])){

        if ( isset($_REQUEST['ip']) ) $GLOBALS['newCertInfo']->ip = $_REQUEST['ip'];
        else $GLOBALS['newCertInfo']->ip = '';

        if ( isset($_REQUEST['dns1']) ) $GLOBALS['newCertInfo']->dns1 = $_REQUEST['dns1'];
        else $GLOBALS['newCertInfo']->dns1 = '';

        if ( isset($_REQUEST['dns2']) ) $GLOBALS['newCertInfo']->dns2 = $_REQUEST['dns2'];
        else $GLOBALS['newCertInfo']->dns2 = '';
    
        return 0;

    }else{
    
        return -1;
    }
}
function create_self_signed_cert()
{
	if( create_self_signed_cert_name() < 0 ) return -1;
	if( create_self_signed_cert_country() < 0 ) return -1;
	if( create_self_signed_cert_expires() < 0 ) return -1;
	if( create_self_signed_cert_state() < 0 ) return -1;
	if( create_self_signed_cert_locality() < 0 ) return -1;
	if( create_self_signed_cert_organization() < 0 ) return -1;
	if( create_self_signed_cert_organization_unit() < 0 ) return -1;
	if( create_self_signed_cert_common_name() < 0 ) return -1;

	if( create_self_signed_cert_rsa_mode() < 0 ) return -1;
	if( create_self_signed_cert_sha_mode() < 0 ) return -1;

    
    if( create_self_signed_cert_san() < 0) return -1;


	return 0;
}
function create_csr_name()
{
	if( !isset($_REQUEST['name']) ) return -1;
	$GLOBALS["CSR"]->Name = $_REQUEST['name'];
	return 0;
}
function create_csr_country()
{
	if( !isset($_REQUEST['country']) ) return -1;
	$GLOBALS["CSR"]->Country = $_REQUEST['country'];
	return 0;
}
function create_csr_state()
{
	if( !isset($_REQUEST['state']) ) return 1;	
	$GLOBALS["CSR"]->State = $_REQUEST['state'];
	return 0;
}
function create_csr_locality()
{
	if( !isset($_REQUEST['locality']) ) return 1;
	$GLOBALS["CSR"]->Locality = $_REQUEST['locality'];
	return 0;
}
function create_csr_organization()
{
	if( !isset($_REQUEST['organization']) ) return 1;
	$GLOBALS["CSR"]->Organization = $_REQUEST['organization'];
	return 0;
}
function create_csr_organization_unit()
{
	if( !isset($_REQUEST['organization_unit'] ) ) return 1;
	$GLOBALS["CSR"]->OrganizationUnit = $_REQUEST['organization_unit'];
	return 0;
}
function create_csr_common_name()
{
	if( !isset($_REQUEST['common_name']) ) return 1;
	$GLOBALS["CSR"]->CommonName = $_REQUEST['common_name'];
	return 0;
}
function create_csr_rsa_mode()
{
	if( !isset($_REQUEST['rsa_mode']) ) return 1;
	$GLOBALS["CSR"]->RSAMode= $_REQUEST['rsa_mode'];
	return 0;
}
function create_csr_sha_mode()
{
	if( !isset($_REQUEST['sha_mode']) ) return 1;
	$GLOBALS["CSR"]->SHAMode= $_REQUEST['sha_mode'];
	return 0;
}
function create_csr_san()
{
	if( isset($_REQUEST['ip']) ||
        isset($_REQUEST['dns1']) ||
        isset($_REQUEST['dns2'])){

        if ( isset($_REQUEST['ip']) ) $GLOBALS['CSR']->ip = $_REQUEST['ip'];
        else $GLOBALS['CSR']->ip = '';

        if ( isset($_REQUEST['dns1']) ) $GLOBALS['CSR']->dns1 = $_REQUEST['dns1'];
        else $GLOBALS['CSR']->dns1 = '';

        if ( isset($_REQUEST['dns2']) ) $GLOBALS['CSR']->dns2 = $_REQUEST['dns2'];
        else $GLOBALS['CSR']->dns2 = '';
    
        return 0;

    }else{
    
        return -1;
    }
}
function create_CSR()
{
	if( create_csr_name() < 0 ) return -1;
	if( create_csr_country() < 0 ) return -1;
	if( create_csr_state() < 0 ) return -1;
	if( create_csr_locality() < 0 ) return -1;
	if( create_csr_organization() < 0 ) return -1;
	if( create_csr_organization_unit() < 0 ) return -1;
	if( create_csr_common_name() < 0 ) return -1;
	if( create_csr_rsa_mode() < 0 ) return -1;
	if( create_csr_sha_mode() < 0 ) return -1;
	if( create_csr_san() < 0 ) return -1;

	return 0;
}

function certificate_view_post()
{
	show_certificates($GLOBALS['security_conf']->Certificates->Certificate);
}
function certificate_get_properties_id()
{
	if( !isset($_REQUEST['id']) ) return -1;
	if( $_REQUEST['id'] == 0 ) return -1;
	$GLOBALS['properties']->Id = $_REQUEST['id'];
	return 0;
}
function certificate_get_properties_datatype()
{
	if( !isset($_REQUEST['data_type'] )) return 1;
	if( $_REQUEST['data_type'] == "json" ) 
		$GLOBALS['isJson'] = true;
	else 
		$GLOBALS['$isJson'] = false;
	return 0;
}

function certificate_get_properties($type=0) // 0: certificate, 1: CA
{
	if( certificate_get_properties_id() < 0 ) return -1;	
	if( certificate_get_properties_datatype() < 0 ) return -1;
	$GLOBALS['properties']->Type = $type;

	$ipc_sock = new IPCSocket();
	$obj= $ipc_sock->Connection($GLOBALS['properties'], CMD_GET_CERTIFICATE_INFO);
	if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
	{
		show_post_ng();
		echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
	}
	else
	{
		show_certificate_properties($obj, $GLOBALS['isJson']);
	}
}

function delete_certificate_id()
{
	if( !isset($_REQUEST['id']) ) return -1;
	$GLOBALS["delCertInfo"]->Id = $_REQUEST['id'];
	return 0;
}

function delete_certificate()
{
	if( delete_certificate_id() < 0 ) return -1;
	return 0;
}

function install_certificate_type()
{
	if( !isset( $_REQUEST['type']) ) return -1;
	$GLOBALS["install_cert"]->Type = $_REQUEST['type'];
	return 0;
}

function install_certificate_name()
{
	if( !isset( $_REQUEST['name']) ) return -1;
	$GLOBALS["install_cert"]->Name= $_REQUEST['name'];
	return 0;
}

function install_certificate_key_type()
{
	if( !isset( $_REQUEST['key_type'])) return 0;
	$GLOBALS["install_cert"]->KeyType= $_REQUEST['key_type'];
	return 0;
}

function install_certificate_password()
{
	if( !isset( $_REQUEST['password']) ) return 0;
	$GLOBALS["install_cert"]->Password= $_REQUEST['password'];
	return 0;
}

function install_certificate_cert_file()
{
	if( !isset( $_FILES['certificate']['name']) ) return -1;
	$file= "/tmp/". $GLOBALS['install_cert']->Name . "_cert";
	if( !move_uploaded_file($_FILES['certificate']['tmp_name'],$file)) return -1;
	return 0;
}
function install_certificate_key_file()
{
	if( !isset($_FILES['key']['name']) ) return 0;
	$file= "/tmp/". $GLOBALS['install_cert']->Name . "_key";
	if( !move_uploaded_file($_FILES['key']['tmp_name'],$file)) return -1;
	return 0;
}

function install_certificate()
{
	if( install_certificate_name()      < 0 ) return -1;
	if( install_certificate_type()      < 0 ) return -1;
	if( install_certificate_key_type()  < 0 ) return -1;
	if( install_certificate_key_file()  < 0 ) return -1;
	if( install_certificate_password()  < 0 ) return -1;
	if( install_certificate_cert_file() < 0 ) return -1;
	return 0;
}

function ca_view_post()
{
	show_certificates($GLOBALS['security_conf']->Certificates->CA);
}
function install_ca_name()
{
	if( !isset( $_REQUEST['name']) ) return -1;
	$GLOBALS["install_cert"]->Name= $_REQUEST['name'];
	return 0;
}
function install_ca_file()
{
	if( !isset( $_FILES['ca']['name']) ) return -1;
	$file= "/tmp/". $GLOBALS['install_cert']->Name . "_cert";
	if( !move_uploaded_file($_FILES['ca']['tmp_name'],$file)) return -1;
	return 0;
}
function install_ca()
{
	if( install_ca_name()      < 0 ) return -1;
	if( install_ca_file() < 0 ) return -1;

	return 0;
}
function delete_ca()
{
	delete_certificate();
}

//////////////////////////////////////////////////////////////////////

function https_view_post()
{
	show_https($GLOBALS['security_conf']->Https, false);
}
function change_https_certificate_id()
{
	if( !isset($_REQUEST['cert_id'] ) ) return 1;
	$GLOBALS['security_conf']->Https->TargetCert->Id = $_REQUEST['cert_id'];
	return 0;
}
function change_https_certificate_name()
{
	if( !isset($_REQUEST['cert_name']) ) return 1;
	$GLOBALS['security_conf']->Https->TargetCert->Name = $_REQUEST['cert_name'];
	return 0;
}
function change_https_connection_policy_for_admin()
{
	if( !isset($_REQUEST['admin_policy'] ) ) return 1;
	$GLOBALS['security_conf']->Https->ConnectionPolicy[0]->value = $_REQUEST['admin_policy'];
	return 0;
}
function change_https_connection_policy_for_operator()
{
	if( !isset($_REQUEST['operator_policy'] ) ) return 1;
	$GLOBALS['security_conf']->Https->ConnectionPolicy[1]->value = $_REQUEST['operator_policy'];
	return 0;
}
function change_https_connection_policy_for_viewer()
{
	if( !isset($_REQUEST['viewer_policy'] ) ) return 1;
	$GLOBALS['security_conf']->Https->ConnectionPolicy[2]->value = $_REQUEST['viewer_policy'];
	return 0;
}
function change_https_connection_policy_for_onvif()
{
	if( !isset($_REQUEST['onvif_policy'] ) ) return 1;
	$GLOBALS['security_conf']->Https->ConnectionPolicy[3]->value = $_REQUEST['onvif_policy'];
	return 0;
}
function change_https_connection_policy_for_rtsp()
{
	if( !isset($_REQUEST['rtsp_policy'] ) ) return 1;
	$GLOBALS['security_conf']->Https->ConnectionPolicy[4]->value = $_REQUEST['rtsp_policy'];
	return 0;
}
function change_https()
{
	if( change_https_certificate_id() < 0 ) return -1;
	if( change_https_certificate_name() < 0 ) return -1;

	if( change_https_connection_policy_for_admin() < 0 ) return -1;
	if( change_https_connection_policy_for_operator() < 0 ) return -1;
	if( change_https_connection_policy_for_viewer() < 0 ) return -1;
	if( change_https_connection_policy_for_onvif() < 0 ) return -1;
	if( change_https_connection_policy_for_rtsp() < 0 ) return -1;
	return 0;
}
header("Content-Type: text/plain");
ob_end_clean ();
if(isset($_REQUEST['msubmenu']))
{
	if( $_REQUEST['msubmenu'] == 'rtsp_authentication' ) 
	{ 
		if( $_REQUEST['action'] == 'view') 
		{
			rtsp_authentication_view_post();
		}
		else if( $_REQUEST['action'] == 'apply') 
		{
			if( change_rtsp_auth_enabled() == 0 ) 
			{
//				show_post_ok();	
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['security_conf']->RtspAuthentication, CMD_SET_RTSP_AUTHENTICATION);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
		}
		else
			show_post_ng();
		exit;
	}
	if( $_REQUEST['msubmenu'] == 'service' ) 
	{ 
		if( $_REQUEST['action'] == 'view') 
		{
			service_view_post();
		}
		else if( $_REQUEST['action'] == 'apply') 
		{
			if(($GLOBALS['get_oem'] == 12) || ($GLOBALS['get_oem'] == 2)){
				show_post_ng();
			}else{
				if( change_service() == 0 ) 
				{
					$ipc_sock = new IPCSocket();
					$ipc_sock->Connection($GLOBALS['security_conf']->SystemService, CMD_SET_SECURITY_SERVICE);
					if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
					{
						show_post_ok();	
					}
					else
					{
						show_post_ng();
					}
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
			}
		}
		else
			show_post_ng();
		exit;
	}
    if( $_REQUEST['msubmenu'] == 'autolock' ) 
	{ 
		if( $_REQUEST['action'] == 'view') 
		{
			autolock_view_post();
		}
		else if( $_REQUEST['action'] == 'apply') 
		{
			if($GLOBALS['get_oem'] != 2){
				show_post_ng();
			}else{
				if( change_autolock() == 0 ) 
				{
					$ipc_sock = new IPCSocket();
					$ipc_sock->Connection($GLOBALS['security_conf']->AutoLock, CMD_SET_SECURITY_AUTOLOCK);
					if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
					{
						show_post_ok();	
					}
					else
					{
						show_post_ng();
					}
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
			}
		}
		else
			show_post_ng();
		exit;
	}
	else if($_REQUEST['msubmenu'] == "ip_filter")
	{
		if( $_REQUEST['action'] == 'view') 
		{
			ip_filter_view_post();
		}
		else if( $_REQUEST['action'] == 'apply') 
		{
			if( change_ip_filter() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['security_conf']->IpFilter, CMD_SET_SECURITY_IP_FILTER);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
            else
			    show_post_ng();
		}
		else if( $_REQUEST['action'] == "add")
		{
			if( change_ip_filter_add_address() == 0 )
			{
				$addr = new CFilteredIPv4Address();
				$addr->Address = $_REQUEST['address'];
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($addr, CMD_ADD_SECURITY_IP_FILTER_ADDR);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
            else
			    show_post_ng();
		}
		else if( $_REQUEST['action'] == 'remove')
		{
			if( change_ip_filter_remove_address() == 0 )
			{
				$addr = new CFilteredIPv4Address();
				$addr->Address = $_REQUEST['address'];
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($addr, CMD_DEL_SECURITY_IP_FILTER_ADDR);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
            else
			    show_post_ng();
		}
		else if( $_REQUEST['action'] == 'remove_all')
		{
			$ipc_sock = new IPCSocket();
			$ipc_sock->Connection(NULL, CMD_DEL_ALL_SECURITY_IP_FILTER_ADDR);
			if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
			{
				show_post_ok();	
			}
			else
			{
				show_post_ng();
			}
			echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
		}
		else
			show_post_ng();
		exit;
	}
	else if( $_REQUEST['msubmenu'] == 'ieee8021x' ) 
	{
		if( $_REQUEST['action'] == 'view') 
		{
			ieee8021x_view_post();
		}
		else if($_REQUEST['action'] == 'apply')
		{
			if( change_ieee8021x() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['security_conf']->IEEE8021X, CMD_SET_IEEE_8021X);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
            else
            {
                show_post_ng();
            }
		}
		else
			show_post_ng();
		exit;
	}
	else if ($_REQUEST['msubmenu'] == "https")
	{
		if( $_REQUEST['action'] == 'view' )
		{
			https_view_post();
		}
		else if( $_REQUEST['action'] == 'apply' )
		{
			if( change_https() == 0 ) 
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['security_conf']->Https, CMD_SET_HTTPS);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
			else 
			{
				show_post_ng();
			}
		}
		exit;
	}
	else if( $_REQUEST['msubmenu'] == 'certificate')
	{
		if( $_REQUEST['action'] == 'view' )
		{
			certificate_view_post();
		}
		else if($_REQUEST['action'] == 'create_self_signed_cert')
		{
			if( create_self_signed_cert() == 0 )
			{
                
                $ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['newCertInfo'], CMD_ADD_SELF_SIGNED_CERT);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
            
            
			}
			else 
			{
				show_post_ng();
			}
		}
		else if($_REQUEST['action'] == 'install')
		{
			if( install_certificate() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$ipc_sock->Connection($GLOBALS['install_cert'], CMD_INSTALL_CERTIFICATE);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] == APP_OK)
				{
					show_post_ok();	
				}
				else
				{
					show_post_ng();
				}
				echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
			}
			else
			{
				show_post_ng();
			}
		}
		else if($_REQUEST['action'] == 'properties')
		{
			certificate_get_properties(0);
		}
		else if($_REQUEST['action'] == 'delete')
		{
			if( delete_ca() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$obj= $ipc_sock->Connection($GLOBALS['delCertInfo'], CMD_DEL_CERTIFICATE);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
				{
					show_post_ng();
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
				else
				{
					show_post_ok();
				}
			}
			else
			{
				show_post_ng();
			}
		}
		else if($_REQUEST['action'] == 'create_cert_sign_req')
		{
			if( create_CSR() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$obj= $ipc_sock->Connection($GLOBALS['CSR'], CMD_CREATE_CSR);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
				{
					show_post_ng();
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
				else
				{
					echo $GLOBALS['CSR']->CSR ."\r\n";
				}
			}
			else
			{
				show_post_ng();
			}
		}
		else
			show_post_ng();
		exit;
	}
	else if( $_REQUEST['msubmenu'] == 'ca')
	{
		if( $_REQUEST['action'] == 'view' )
		{
			ca_view_post();
		}
		else if($_REQUEST['action'] == 'install')
		{
			if( install_ca() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$obj= $ipc_sock->Connection($GLOBALS['install_cert'], CMD_INSTALL_CA);
				if ($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
				{
					show_post_ng();
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
				else
				{
					show_post_ok();
				}
			}
			else
			{
				show_post_ng();
			}
		}
		else if($_REQUEST['action'] == 'delete')
		{
			if( delete_certificate() == 0 )
			{
				$ipc_sock = new IPCSocket();
				$obj= $ipc_sock->Connection($GLOBALS['delCertInfo'], CMD_DEL_CA);
				if($ipc_sock->dataInfo['ErrorCode']['value'] != APP_OK)
				{
					show_post_ng();
					echo "result : ".$ipc_sock->dataInfo['ErrorCode']['value'];
				}
				else
				{
					show_post_ok();
				}
			}
			else
			{
				show_post_ng();
			}
		}
		else if($_REQUEST['action'] == 'properties')
		{
			certificate_get_properties(1);
		}
		else 
			show_post_ng();
		exit;
	}
}
show_post_ng();
?>
