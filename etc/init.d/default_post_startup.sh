#!/bin/sh

PLUGIN_DIR="/mnt/plugin"
PLUGIN_LIST=`ls -l ${PLUGIN_DIR}/ | grep ^d | awk '{print $9}'`
SCRIPT_NAME="post_startup.sh"

#echo "$PLUGIN_LIST"

for LIST in ${PLUGIN_LIST} ;do
	${PLUGIN_DIR}/${LIST}/${SCRIPT_NAME} $1 $2
done
