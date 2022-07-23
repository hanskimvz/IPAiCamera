#!/bin/sh
PLUGIN_DIR="/mnt/plugin"
PLUGIN_TMP_DIR="/tmp/plugin"
STARTUP_SCRIPT="pre_startup.sh"
PLUGIN_MTD_NUM="10"

if [ ! -d ${PLUGIN_DIR} ]; then
	mkdir ${PLUGIN_DIR}
fi

mkdir -p ${PLUGIN_TMP_DIR}
#link /root/web/plugin
if [ ! -L /root/web/plugin ]; then
  ln -s ${PLUGIN_TMP_DIR} /root/web/plugin
fi

mount -t ext4 /dev/mmcblk0p${PLUGIN_MTD_NUM} ${PLUGIN_DIR}
if [ $? -ne 0 ]
then
  #dd if=/dev/zero of=/dev/mmcblk0p10 #erase emmc nand
  y | mkfs.ext4 /dev/mmcblk0p${PLUGIN_MTD_NUM}
  mount -t ext4 /dev/mmcblk0p${PLUGIN_MTD_NUM} ${PLUGIN_DIR}
fi

lostdir="/mnt/plugin/lost+found"
if [ -d ${lostdir} ]; then
  rm -rf ${lostdir}
fi

if [ ! -L ${PLUGIN_DIR}/${STARTUP_SCRIPT} ]; then
    rm -rf ${PLUGIN_DIR}/${STARTUP_SCRIPT}
    ln -s /etc/init.d/default_pre_startup.sh ${PLUGIN_DIR}/${STARTUP_SCRIPT}
fi

if [ -f ${PLUGIN_DIR}/${STARTUP_SCRIPT} ]; then
	${PLUGIN_DIR}/${STARTUP_SCRIPT}
fi
