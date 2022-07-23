#!/bin/sh
PLUGIN_DIR="/mnt/plugin"
STARTUP_SCRIPT="post_startup.sh"

if [ ! -L ${PLUGIN_DIR}/${STARTUP_SCRIPT} ]; then
    rm -rf ${PLUGIN_DIR}/${STARTUP_SCRIPT}
    ln -s /etc/init.d/default_post_startup.sh ${PLUGIN_DIR}/${STARTUP_SCRIPT}
fi

if [ -f ${PLUGIN_DIR}/${STARTUP_SCRIPT} ]; then
	${PLUGIN_DIR}/${STARTUP_SCRIPT} start booting
fi
