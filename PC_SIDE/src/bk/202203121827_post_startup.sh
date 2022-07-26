#!/bin/sh
echo "################################################"
echo "### Enable Crond and Counting report service ###"
echo "################################################"

CRONDIR="/var/spool/cron"
FILECRON="/var/spool/cron/crontabs/root"
STRCRON="* * * * * /usr/bin/php-cgi /mnt/plugin/crpt/mk_ct_report.cgi"

if [ ! -d $CRONDIR ]; then 
    echo "Create directory, $CRONDIR"
    mkdir $CRONDIR
fi

if [ ! -d $CRONDIR/crontabs ]; then 
    echo "Create directory, $CRONDIR/crontabs"
    mkdir $CRONDIR/crontabs
fi

if [ ! -f $FILECRON ]; then 
    echo "Create file, $FILECRON"
    echo "$STRCRON" > $FILECRON
fi

MODCRON=`cat $FILECRON | grep mk_ct_report.cgi | awk '{print $0}'`
# echo "$MODCRON"
if [ ! "$MODCRON" ] ;  then
    echo "appending string"
    echo "\r\n$STRCRON" >> $FILECRON
fi

ES=`ps -ef |grep crond | grep -v grep | awk '{print $1}'`
# echo "$ES"
if [ ! "$ES" ] ;  then
    echo "Service Crond start" 
    /usr/sbin/crond
fi