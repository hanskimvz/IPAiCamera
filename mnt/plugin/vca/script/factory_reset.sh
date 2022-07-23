#!/bin/sh

PLUGIN_NAME="vca"
PLUGIN_DIR="/mnt/plugin"
PLUGIN_TMPDIR="/tmp"
PLUGIN_INFO_XMLFILE="${PLUGIN_DIR}/${PLUGIN_NAME}/web/info.dat"
PLUGIN_CONF_PATH="${PLUGIN_DIR}/.config"

echo "============= ${PLUGIN_NAME} factory reset"
#remove user event - IPMPFW-299
#If the VCA "all" event is registered in the IPM event, only the user event is deleted in "plugin_user_event_index.txt" when vca stop
#So parsing is not possible, and the ipm event cannot be deleted.
#Therefore, Should delete the user event and ipm event before vca stop.Therefore, Should delete the user event and ipm event before vca stop.
PLUGIN_EVENT_ID=`xmllint --xpath '/plugin_info/userevent/eventid/text()' ${PLUGIN_INFO_XMLFILE}`
PLUGIN_EVENT_NAME=`xmllint --xpath '/plugin_info/userevent/eventname/text()' ${PLUGIN_INFO_XMLFILE}`
${PLUGIN_DIR}/${PLUGIN_NAME}/bin/userEvtRegister uninstall ${PLUGIN_EVENT_ID} ${PLUGIN_EVENT_NAME}

PLUGIN_STATUS=`xmllint --xpath '/plugin_info/status/text()' ${PLUGIN_INFO_XMLFILE}`

if [ "$1" == "mainfw" ]; then
  #this file will be used in vca_core_app
  touch ${PLUGIN_TMPDIR}/mainfw_factory_reset
fi

${PLUGIN_DIR}/${PLUGIN_NAME}/script/startapp.sh stop fd_reset
rm -rf ${PLUGIN_CONF_PATH}/vca-cored

if [ "$1" == "mainfw" ]; then
  rm -rf ${PLUGIN_CONF_PATH}
fi

#IPMPFW-717 restore default of api.json
if [ -f ${PLUGIN_DIR}/vca_api_default.json ]; then
  mkdir -p ${PLUGIN_CONF_PATH}/vca-cored/configuration
  cp ${PLUGIN_DIR}/vca_api_default.json ${PLUGIN_CONF_PATH}/vca-cored/configuration/api.json
fi

${PLUGIN_DIR}/${PLUGIN_NAME}/pre_startup.sh

#IPMPFW-716 keep plugin status
if [ "$PLUGIN_STATUS" == "running" ]; then
  if [ "$1" == "mainfw" ]; then
    sed -i 's/<status>stopped/<status>running/g' ${PLUGIN_INFO_XMLFILE}
  else
    ${PLUGIN_DIR}/${PLUGIN_NAME}/script/startapp.sh restart
  fi
fi

#save management log
source ${PLUGIN_DIR}/${PLUGIN_NAME}/script/setTZ.sh
echo "$(date "+%Y-%m-%d %H:%M:%S") ${PLUGIN_NAME} factory reset success" >> ${PLUGIN_DIR}/${PLUGIN_NAME}/logs/management.log

echo "${PLUGIN_NAME} factory reset complete"