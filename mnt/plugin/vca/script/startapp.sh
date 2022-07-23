#!/bin/sh

APPNAME=vca_core_app
PLUGIN_DIR="/mnt/plugin"
PLUGIN_NAME="vca"
APP_DIR="${PLUGIN_DIR}/${PLUGIN_NAME}/bin"
APP_INFO_FILE="${PLUGIN_DIR}/${PLUGIN_NAME}/web/info.dat"
RUNDIR="/var/run"

SECOND_ARG="$2"

#copy libconfbridge.so file
MAINFW_BUILD_DATE=`tr -d "\"," < /mnt/nand/pconf_system.db | grep BuildVersion | awk '{print $3}'`
DEPENDENCY_DATE="2020.06.05"
if [ "$MAINFW_BUILD_DATE" \< "$DEPENDENCY_DATE" ]; then
  EXIST_CONFBRIDGE_FILE=`cat ${PLUGIN_DIR}/copyfile_history | grep libconfbridge.so`

  if [ "$EXIST_CONFBRIDGE_FILE" != "libconfbridge.so" ]; then
    cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/libs/libconfbridge.so /usr/lib/libconfbridge.so
    echo "libconfbridge.so" >> ${PLUGIN_DIR}/copyfile_history
    echo "copy libconfbridge.so file complete"
  fi
fi

#copy plugin_upload cgi file
DEPENDENCY_DATE="2020.09.29"
if [ "$MAINFW_BUILD_DATE" \< "$DEPENDENCY_DATE" ]; then
  EXIST_PLUGINUPLOAD_FILE=`cat ${PLUGIN_DIR}/copyfile_history | grep plugin_upload`

  if [ "$EXIST_PLUGINUPLOAD_FILE" != "plugin_upload" ]; then
    cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/web/ipnc/plugin_upload /root/web/cgi-bin/admin/plugin_upload
    cp -rf ${PLUGIN_DIR}/${PLUGIN_NAME}/script/stop_plugins.sh /etc/init.d/stop_plugins.sh
    echo "plugin_upload" >> ${PLUGIN_DIR}/copyfile_history
    echo "copy plugin_upload complete"
  fi
fi

#remove copyfile_history
if [ "$SECOND_ARG" == "fwupdate" ]; then
  echo "************* remove copyfile_history"
  rm -rf ${PLUGIN_DIR}/copyfile_history
fi

#make vca license url
${PLUGIN_DIR}/${PLUGIN_NAME}/script/make_vca_license_url.sh

check_process() {
  if [ $1 = "stop" ]; then
    cnt=1
    while [ "$cnt" -le "30" ]; do
      sleep 1
      check_pid=`pidof $APPNAME`
      echo "$APPNAME stopping $cnt"
      if [  -z "${check_pid}" ]; then
        echo "$APPNAME stoped"
        return 0
      fi
      cnt=$(($cnt+1))
    done
  fi

  if [ $1 = "running" ]; then
    cnt=1
    while [ "$cnt" -le "10" ]; do
      sleep 1
      if [ -f /tmp/plugin/vca/wait_vca_run ]; then
        echo "not yet vca run"
        continue;
      fi
      check_pid=`pidof $APPNAME`
      echo "$APPNAME starting $cnt"
      if [ ! -z "${check_pid}" ]; then
        echo "$APPNAME running"
        return 0
      fi
      cnt=$(($cnt+1))
    done
  fi
  echo "check process error!!!"
  return 1
}

start_daemon() {
  if [ -f "${RUNDIR}/${APPNAME}.pid" ]; then
    echo "Process alive"
    exit 1
  fi

  while [ 1 ]; do
    _exist_lo=`ifconfig | grep lo`
    _exist_eth0=`ifconfig | grep eth0`
    _exist_ip=`ifconfig eth0 | grep "inet addr"`
    if [ -z "${_exist_lo}" ] || [ -z "${_exist_eth0}" ] || [ -z "${_exist_ip}" ]; then
      echo "Network fail!!!"
      sleep 1
    else
      echo "Network exist. ${PLUGIN_NAME} will run"
      sleep 1
      break
    fi
  done

if [ ! -d ${PLUGIN_DIR}/.vdm ]; then
  rm -rf ${PLUGIN_DIR}/.vdm
  mkdir -p ${PLUGIN_DIR}/.vdm
  if [ -f /tmp/plugin/vca/.conf ]; then
    cp /tmp/plugin/vca/.conf ${PLUGIN_DIR}/.vdm
  fi
  echo "$(date "+%Y-%m-%d %H:%M:%S") ${PLUGIN_NAME} recover license" >> ${PLUGIN_DIR}/${PLUGIN_NAME}/logs/management.log
fi
  #NN MODEL
  if [ -f "/tmp/plugin/vca/api_partial.json" ]; then
    mv ${PLUGIN_DIR}/.config/vca-cored/tracking_engine.conf /tmp/plugin/vca/tracking_engine.conf
    /mnt/plugin/vca/script/factory_reset.sh
    mv /tmp/plugin/vca/tracking_engine.conf ${PLUGIN_DIR}/.config/vca-cored/tracking_engine.conf
    cp -rf /tmp/plugin/vca/api_partial.json /mnt/plugin/.config/vca-cored/configuration/api.json
    rm -rf /tmp/plugin/vca/api_partial.json
  fi

  ARGS="--none"
  engine=`awk -F '\"' '{print $4}' /mnt/plugin/.config/vca-cored/tracking_engine.conf`
  if [ "$engine" == "object_tracker" ]; then
    ARGS="--none"
  fi
  if [ "$engine" == "dl_object_tracker" ]; then
    ARGS="--objecttracker"
  fi
  if [ "$engine" == "dl_people_tracker" ]; then
    ARGS="--pose"
  fi
  touch /tmp/plugin/vca/wait_vca_run
  echo "tracking engine $engine"
#export VCA_LOGGING_PATH=/mnt/plugin/vca/logs/vcasdk
#export VCA_LOGGING_LEVELS='{"*":["all"], "vca.core.AppChannel":[""], "vca.web.backend.civetweb.service":[""]}'
  /sbin/start-stop-daemon --start --quiet --oknodo --background --pidfile ${RUNDIR}/${APPNAME}.pid -m --exec ${APP_DIR}/${APPNAME} ${OPTION} -- $ARGS

  check_process running
  ret=$?
  if [ "$ret" = 0 ]; then
    echo "change $APPNAME status as running"
    sed -i 's/<status>stopped/<status>running/g' $APP_INFO_FILE
    /mnt/plugin/make_plugin_info.sh
  fi

#start vcaEvent
  ${PLUGIN_DIR}/${PLUGIN_NAME}/script/startvcaevent.sh start
#start audio-out
  ${PLUGIN_DIR}/${PLUGIN_NAME}/script/startaudio.sh start
  echo "success"
}

stop_daemon() {
#first stop vcaEvent
  ${PLUGIN_DIR}/${PLUGIN_NAME}/script/startvcaevent.sh stop
#stop audio-out
  ${PLUGIN_DIR}/${PLUGIN_NAME}/script/startaudio.sh stop

  if [ -f "${RUNDIR}/${APPNAME}.pid" ]; then
    /sbin/start-stop-daemon --stop --retry 5 --pidfile ${RUNDIR}/${APPNAME}.pid

    if [ "$SECOND_ARG" != "fwupdate" ]; then
      check_process stop
      ret=$?
      if [ "$ret" = 0 ]; then
        echo "change $APPNAME status as stop"
      else
        echo "force kill $APPNAME!!!!"
        killall -9 $APPNAME
      fi
      sed -i 's/<status>running/<status>stopped/g' $APP_INFO_FILE
      /mnt/plugin/make_plugin_info.sh
      if [ -f "${RUNDIR}/${APPNAME}.pid" ]; then
        rm -f ${RUNDIR}/${APPNAME}.pid
      fi
    fi
  fi
  rm -rf /tmp/.shm_meta*
}
if [ "$SECOND_ARG" == "booting" ]; then
  echo "start ${PLUGIN_NAME} during booting"
  sleep 20
fi

case "$1" in
  start)
    echo "Starting ${APPNAME}..."
    start_daemon
    ;;
  stop)
    echo "Stopping ${APPNAME}..."
    stop_daemon
    ;;
  restart)
    echo "Restarting ${APPNAME}..."
    stop_daemon
    sleep 1
    start_daemon
    ;;
  *)
    echo -e "Usage: $0 start|stop|restart"
   ;;
esac

exit 0
