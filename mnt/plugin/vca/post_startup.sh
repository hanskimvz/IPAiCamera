#!/bin/sh

PLUGIN_DIR="/mnt/plugin"
PLUGIN_TMPDIR="/tmp/plugin"
PLUGIN_NAME="vca"
SCRIPT_DIR="${PLUGIN_DIR}/${PLUGIN_NAME}/script"
SCRIPT_NAME="startapp.sh"

MAINFW_BUILD_DATE=`tr -d "\"," < /mnt/nand/pconf_system.db | grep BuildVersion | awk '{print $3}'`
#should be check setup.sh for copying libueo.so
DEPENDENCY_DATE="2021.10.22"
if [ "$MAINFW_BUILD_DATE" \< "$DEPENDENCY_DATE" ]; then
  cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/onvif/libueo_old.so ${PLUGIN_TMPDIR}/${PLUGIN_NAME}/libueo.so
else
  cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/onvif/libueo_new.so ${PLUGIN_TMPDIR}/${PLUGIN_NAME}/libueo.so
fi
ln -s ${PLUGIN_TMPDIR}/${PLUGIN_NAME}/libueo.so  ${PLUGIN_DIR}/${PLUGIN_NAME}/onvif/libueo.so
touch /tmp/libueo.module.changed
#run app start script
CHECK_APP_RUN=`grep -rn status ${PLUGIN_DIR}/${PLUGIN_NAME}/web/info.dat | grep running`

function strstr ()
{
  [ ${#2} -eq 0 ] && { echo "$1" ; return 0; }

  case "$1" in
  *$2*) ;;
  *) return 0;;
  esac

  first=${1/$2*/}

  return 1;
}

BOARD_CHIP=`tr -d "\"," < /mnt/nand/pconf_capability.db | grep board_chipset | awk '{print $3}'`
CHIPSET_NAME="none"
strstr $BOARD_CHIP cv22
find_str=$?
if [ $find_str == 1 ]; then
  CHIPSET_NAME="cv22"
  modprobe cavalry
  /usr/local/bin/cavalry_load -f /lib/firmware/cavalry.bin -r
fi

if [ ! -z "$CHECK_APP_RUN" ]; then
	${SCRIPT_DIR}/${SCRIPT_NAME} $1 $2 &
fi

#${SCRIPT_DIR}/recover_plugin.sh &
