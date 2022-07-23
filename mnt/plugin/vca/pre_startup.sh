#!/bin/sh

PLUGIN_NAME="vca"
PLUGIN_DIR="/mnt/plugin"
PLUGIN_TMPDIR="/tmp/plugin"

IPNC_LIBDIR="/usr/lib"
IPNC_SHAREDIR="/usr/lib/share"
IPNC_WEPDIR="/root/web"

VCACORE_LIB_DIR="${PLUGIN_DIR}/${PLUGIN_NAME}/lib"
VCACORE_LICENSE_APP_DIR="${PLUGIN_DIR}/${PLUGIN_NAME}/bin"
VCACORE_LICENSE_VDM_DIR="/var/lib/vdm"
VCACORE_WEB_SHARE_DIR="${PLUGIN_DIR}/${PLUGIN_NAME}/web/share"
VCACORE_WEB_SRC_DIR="vca-cored"
VCACORE_WEB_FONT_DIR="minrenderbia"

#copy setup_main.js
IPNC_JS_VER=`cat /root/web/cgi-bin/admin/setup_main.js  | grep udp_version | awk -F = '{print $2}'`
NEW_JS_VER=`cat ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_main.js  | grep udp_version | awk -F = '{print $2}'`

if [ "${IPNC_JS_VER}" \< "${NEW_JS_VER}" ]; then
  echo "Old_Ver:$IPNC_JS_VER < New_Ver$NEW_JS_VER Copy setup_main.js"
  #IPMPFW-592 backup original file
  if [ ! -f /root/web/cgi-bin/admin/setup_main.js.back.vcaedge ]; then
    cp -rf /root/web/cgi-bin/admin/setup_main.js /root/web/cgi-bin/admin/setup_main.js.back.vcaedge
  fi
  cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_main.js /root/web/cgi-bin/admin/setup_main.js
#  _cnt=1
#  while [ "$_cnt" -le "3" ]
#  do
#    cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_main.js /root/web/cgi-bin/admin/setup_main.js
#    _cnt=$(($_cnt+1))
#  done
fi

#copy setup_system_plugin_upload.cgi
IPNC_JS_VER=`cat /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi  | grep udp_version | awk -F = '{print $2}'`
NEW_JS_VER=`cat ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_system_plugin_upload.cgi  | grep udp_version | awk -F = '{print $2}'`

if [ "${IPNC_JS_VER}" \< "${NEW_JS_VER}" ]; then
  #IPMPFW-592 backup original file
  if [ ! -f /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi.back.vcaedge ]; then
    cp -rf /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi.back.vcaedge
  fi
  _cnt=1
  while [ "$_cnt" -le "3" ]
  do
    echo "Old_Ver:$IPNC_JS_VER < New_Ver$NEW_JS_VER Copy setup_system_plugin_upload.cgi"
    cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_system_plugin_upload.cgi /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi
    _cnt=$(($_cnt+1))
    END_OF_FILE=`cat /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi  | grep end_of_file`
    if [ ! -z "$END_OF_FILE" ]; then
      break
    fi
  done
fi

#copy setup_system_plugin_upload.js
IPNC_JS_VER=`cat /root/web/cgi-bin/admin/setup_system_plugin_upload.js  | grep udp_version | awk -F = '{print $2}'`
NEW_JS_VER=`cat ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_system_plugin_upload.js  | grep udp_version | awk -F = '{print $2}'`

if [ "${IPNC_JS_VER}" \< "${NEW_JS_VER}" ]; then
  #IPMPFW-592 backup original file
  if [ ! -f /root/web/cgi-bin/admin/setup_system_plugin_upload.js.back.vcaedge ]; then
    cp -rf /root/web/cgi-bin/admin/setup_system_plugin_upload.js /root/web/cgi-bin/admin/setup_system_plugin_upload.js.back.vcaedge
  fi

  _cnt=1
  while [ "$_cnt" -le "3" ]
  do
    echo "Old_Ver:$IPNC_JS_VER < New_Ver$NEW_JS_VER Copy setup_system_plugin_upload.js"
    #cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_system_plugin_upload.js /root/web/cgi-bin/admin/setup_system_plugin_upload.js
    rm /root/web/cgi-bin/admin/setup_system_plugin_upload.js
    cat ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/setup_system_plugin_upload.js >> /root/web/cgi-bin/admin/setup_system_plugin_upload.js
    _cnt=$(($_cnt+1))
    END_OF_FILE=`cat /root/web/cgi-bin/admin/setup_system_plugin_upload.js  | grep end_of_file`
    if [ ! -z "$END_OF_FILE" ]; then
      break
    fi
  done
fi

#make /mnt/XXXX/logs
if [ ! -d ${PLUGIN_DIR}/${PLUGIN_NAME}/logs ]; then
  mkdir -p ${PLUGIN_DIR}/${PLUGIN_NAME}/logs
fi

#copy uninstall script
if [ ! -d ${PLUGIN_TMPDIR}/${PLUGIN_NAME} ]; then
  mkdir -p ${PLUGIN_TMPDIR}/${PLUGIN_NAME}
fi
cp ${PLUGIN_DIR}/${PLUGIN_NAME}/script/uninstall.sh ${PLUGIN_TMPDIR}/${PLUGIN_NAME}

#copy port.conf
MAINFW_BUILD_DATE=`tr -d "\"," < /mnt/nand/pconf_system.db | grep BuildVersion | awk '{print $3}'`
if [ -z "$MAINFW_BUILD_DATE" ];then #old FW. because of old fw don't mount /mnt/nand when booting
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/etc/legacy_port.conf ${PLUGIN_TMPDIR}/port.conf
else
  DEPENDENCY_DATE="2020.08.21"
  if [ "$MAINFW_BUILD_DATE" \< "$DEPENDENCY_DATE" ]; then
    cp ${PLUGIN_DIR}/${PLUGIN_NAME}/etc/legacy_port.conf ${PLUGIN_TMPDIR}/port.conf
  else
    cp ${PLUGIN_DIR}/${PLUGIN_NAME}/etc/port.conf ${PLUGIN_TMPDIR}/port.conf
  fi
fi

if [ ! -L ${PLUGIN_DIR}/port.conf ]; then
  rm -rf ${PLUGIN_DIR}/port.conf
  ln -s ${PLUGIN_TMPDIR}/port.conf ${PLUGIN_DIR}/port.conf
fi

#link /root/web/plugin
if [ ! -L /root/web/plugin ]; then
  ln -s ${PLUGIN_TMPDIR} /root/web/plugin
fi

#link /var/lib/vdm
rm -rf ${VCACORE_LICENSE_VDM_DIR}
mkdir -p ${PLUGIN_DIR}/.vdm
ln -s ${PLUGIN_DIR}/.vdm ${VCACORE_LICENSE_VDM_DIR}

#create dir /mnt/plugin/.config/vca-cored & /mnt/plugin/.config/vca-cored/event
mkdir -p ${PLUGIN_DIR}/.config/vca-cored/event
mkdir -p ${PLUGIN_DIR}/.config/vca-cored/configuration

#link /.config/vca-cored : VCA configuration //no use now
#mkdir -p /root/.config
#rm -rf /root/.config/vca-cored
#ln -s ${PLUGIN_DIR}/.config/vca-cored /root/.config/vca-cored

#create linked files for libvca & license & font
rm -rf ${IPNC_LIBDIR}/${PLUGIN_NAME}
mkdir -p ${IPNC_LIBDIR}/${PLUGIN_NAME}
ln -s ${VCACORE_LIB_DIR} ${IPNC_LIBDIR}/${PLUGIN_NAME}/lib  #if use this folder, must add make link option "-Wl,-rpath,/usr/lib/vca" when compile the vca_core_app
ln -s ${VCACORE_LICENSE_APP_DIR} ${IPNC_LIBDIR}/${PLUGIN_NAME}/bin
ln -s ${VCACORE_WEB_SHARE_DIR} ${IPNC_LIBDIR}/${PLUGIN_NAME}/share

#create linked files for web
rm -rf ${IPNC_WEPDIR}/cgi-bin/admin/vca
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www ${IPNC_WEPDIR}/cgi-bin/admin/vca
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/advanced/advanced.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/advanced/setup_vca_advanced.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/license/license.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/license/setup_vca_license.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/rules/rules.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/rules/setup_vca_rules.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/tamper/tamper.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/tamper/setup_vca_tamper.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/counters/counters.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/counters/setup_vca_counters.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/calibration/calibration.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/calibration/setup_vca_calibration.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/classification/classification.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/classification/setup_vca_classification.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/calass/calibrationassist.html ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/calass/setup_vca_calibrationassist.cgi

#This is a separate link to bypass authentication.
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/classification/make_class_namelist.cgi ${IPNC_WEPDIR}/cgi-bin/make_class_namelist.cgi

#create BIA conf
BIA_CONTENT="{\"BIAenable\": \"0\", \"streamid\": \"1\", \"resolution\": \"1920x1080\", \"snapshotBIA\" : \"0\", \
\"blob\" : \"0\", \
\"zones\" : \"1\", \
\"objects\" : \"1\", \
\"class\" : \"1\", \
\"height\" : \"0\", \
\"speed\" : \"0\", \
\"area\" : \"0\", \
\"evt_msg\" : \"0\", \
\"sys_msg\" : \"1\", \
\"line_counters\" : \"1\", \
\"counters\" : \"1\", \
\"obj_id\" : \"0\", \
\"confidence\" : \"0\", \
\"dwell_time\" : \"0\" \
}"
if [ -f ${PLUGIN_DIR}/.config/vca-cored/streamforBIA.json ]; then
  mv ${PLUGIN_DIR}/.config/vca-cored/streamforBIA.json ${PLUGIN_DIR}/.config/vca-cored/bia.conf
fi

if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/bia.conf ]; then
  echo $BIA_CONTENT > ${PLUGIN_DIR}/.config/vca-cored/bia.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/bia.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/bia.conf

#copy mimic config files
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/mimic.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/mimic_default.conf ${PLUGIN_DIR}/.config/vca-cored/mimic.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/mimic.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/mimic.conf

#copy event config files
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/event/tcp.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/tcp_default.conf ${PLUGIN_DIR}/.config/vca-cored/event/tcp.conf
fi
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/event/http.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/http_default.conf ${PLUGIN_DIR}/.config/vca-cored/event/http.conf
fi
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/event/trigger.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/trigger_default.conf ${PLUGIN_DIR}/.config/vca-cored/event/trigger.conf
fi

if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/event/vcatomd.conf ]; then
  touch ${PLUGIN_DIR}/.config/vca-cored/event/vcatomd.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/event/tcp.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/tcp.conf
ln -s ${PLUGIN_DIR}/.config/vca-cored/event/http.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/http.conf
ln -s ${PLUGIN_DIR}/.config/vca-cored/event/trigger.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/trigger.conf
ln -s ${PLUGIN_DIR}/.config/vca-cored/event/vcatomd.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/vcatomd.conf

#create & link reset coutner conf
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/resetCounter.conf ]; then
  touch ${PLUGIN_DIR}/.config/vca-cored/resetCounter.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/resetCounter.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/resetCounter.conf

#copy nn_model config files
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/tracking_engine.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/tracking_engine_default.conf ${PLUGIN_DIR}/.config/vca-cored/tracking_engine.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/tracking_engine.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/tracking_engine.conf

#copy nn_model config files
if [ ! -f ${PLUGIN_DIR}/.config/vca-cored/dl_confidence.conf ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/dl_confidence_default.conf ${PLUGIN_DIR}/.config/vca-cored/dl_confidence.conf
fi
ln -s ${PLUGIN_DIR}/.config/vca-cored/dl_confidence.conf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www/config/dl_confidence.conf


#create linked files for cgi
if [ ! -d ${IPNC_WEPDIR}/nvc-cgi ]; then
  mkdir -p ${IPNC_WEPDIR}/nvc-cgi/admin
  mkdir -p ${IPNC_WEPDIR}/nvc-cgi/viewer
fi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/nvc-cgi/avstream.cgi ${IPNC_WEPDIR}/nvc-cgi/avstream.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/nvc-cgi/avstream.cgi ${IPNC_WEPDIR}/nvc-cgi/admin/avstream.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/nvc-cgi/avstream.cgi ${IPNC_WEPDIR}/nvc-cgi/viewer/avstream.cgi
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/nvc-cgi/vca_event_action.cgi ${IPNC_WEPDIR}/cgi-bin/admin/vca_event_action

#create linked files for library
ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/lib/libboost_system.so.1.67.0 ${IPNC_LIBDIR}/libboost_system.so.1.67.0

CHECK_MULTISENSOR=`tr -d "\"," < /mnt/nand/pconf_capability.db | grep camera_type | awk '{print $3}'`

if [ $CHECK_MULTISENSOR == "PROXY_SERVER" ] || [ $CHECK_MULTISENSOR == "PREDATOR_SERVER" ] || [ $CHECK_MULTISENSOR == "PROXY_DUAL_SERVER" ]; then
  ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www ${IPNC_WEPDIR}/plugin/vca
  ln -s ${IPNC_WEPDIR}/cgi-bin/admin/trigger.cgi ${PLUGIN_DIR}/${PLUGIN_NAME}/web/www
  ln -s ${IPNC_WEPDIR}/cgi-bin/_define.inc ${PLUGIN_DIR}/${PLUGIN_NAME}/web
  ln -s ${IPNC_WEPDIR}/cgi-bin/buildtime_define.inc ${PLUGIN_DIR}/${PLUGIN_NAME}/web
  ln -s ${IPNC_WEPDIR}/cgi-bin/class ${PLUGIN_DIR}/${PLUGIN_NAME}/web
fi

if [ ! -f ${IPNC_LIBDIR}/libprotobuf.so.17 ]; then
  ln -s ${PLUGIN_DIR}/${PLUGIN_NAME}/lib/libprotobuf.so.17.0.0 ${IPNC_LIBDIR}/libprotobuf.so.17
fi

iptables -A INPUT -p tcp -s 127.0.0.1 --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp -s 127.0.0.1 --dport 8081 -j ACCEPT
iptables -A INPUT -p tcp --dport 8080 -j DROP
iptables -A INPUT -p tcp --dport 8081 -j DROP
iptables-save
