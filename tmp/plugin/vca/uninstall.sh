#!/bin/sh

PLUGIN_NAME="vca"
PLUGIN_DIR="/mnt/plugin"
PLUGIN_INFO_XMLFILE="${PLUGIN_DIR}/${PLUGIN_NAME}/web/info.dat"
IPNC_LIBDIR="/usr/lib"
PLUGIN_LOGBACKUP_DIR="/mnt/plugin/.logbackup"

#remove user event - IPMPFW-299
#If the VCA "all" event is registered in the IPM event, only the user event is deleted in "plugin_user_event_index.txt" when vca stop.
#So parsing is not possible, and the ipm event cannot be deleted.
#Therefore, Should delete the user event and ipm event before vca stop.Therefore, Should delete the user event and ipm event before vca stop.
PLUGIN_EVENT_ID=`xmllint --xpath '/plugin_info/userevent/eventid/text()' ${PLUGIN_INFO_XMLFILE}`
PLUGIN_EVENT_NAME=`xmllint --xpath '/plugin_info/userevent/eventname/text()' ${PLUGIN_INFO_XMLFILE}`
${PLUGIN_DIR}/${PLUGIN_NAME}/bin/userEvtRegister uninstall ${PLUGIN_EVENT_ID} ${PLUGIN_EVENT_NAME}

#stop the plugin
${PLUGIN_DIR}/${PLUGIN_NAME}/script/startapp.sh stop

#remove plugin configuration - IPMPFW-299
rm -rf ${PLUGIN_DIR}/.config/vca-cored

#remove vca lib link
rm -rf ${IPNC_LIBDIR}/${PLUGIN_NAME}

#save management log
source ${PLUGIN_DIR}/${PLUGIN_NAME}/script/setTZ.sh
echo "$(date "+%Y-%m-%d %H:%M:%S") ${PLUGIN_NAME} uninstall success" >> ${PLUGIN_DIR}/${PLUGIN_NAME}/logs/management.log

#backup log
mkdir -p ${PLUGIN_LOGBACKUP_DIR}/${PLUGIN_NAME}
if [ -d ${PLUGIN_DIR}/${PLUGIN_NAME}/logs ]; then
  cp ${PLUGIN_DIR}/${PLUGIN_NAME}/logs/* ${PLUGIN_LOGBACKUP_DIR}/${PLUGIN_NAME}
fi

#remove plugin datas
rm -rf ${PLUGIN_DIR}/${PLUGIN_NAME}

#reload libueo.so
touch /tmp/libueo.module.changed

#IPMPFW-592 restore original file
if [ -f /root/web/cgi-bin/admin/setup_main.js.back.vcaedge ]; then
  mv /root/web/cgi-bin/admin/setup_main.js.back.vcaedge /root/web/cgi-bin/admin/setup_main.js
fi
if [ -f /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi.back.vcaedge ]; then
  mv /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi.back.vcaedge /root/web/cgi-bin/admin/setup_system_plugin_upload.cgi
fi
if [ -f /root/web/cgi-bin/admin/setup_system_plugin_upload.js.back.vcaedge ]; then
  mv /root/web/cgi-bin/admin/setup_system_plugin_upload.js.back.vcaedge /root/web/cgi-bin/admin/setup_system_plugin_upload.js
fi


#update xml file
${PLUGIN_DIR}/make_plugin_info.sh
