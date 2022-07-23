#!/bin/sh
ambd=/usr/local/bin/amba_debug

if [ ! -e $ambd ]
then
	echo "Amba debug not found."
	exit
fi

check_sdcard()
{
SD0_Controller=0xe0005000
SD_present_state_offset=0x24
SD_present_state=$(echo $((SD0_Controller)) $((SD_present_state_offset)) | awk '{print or($1,$2)}')

sd_state_value=$($ambd -r $SD_present_state | awk '{print $2}')
card_inserted=$(echo $sd_state_value | awk '{print rshift(and($1,0x10000),16)}')
card_state_stable=$(echo $sd_state_value | awk '{print rshift(and($1,0x20000),17)}')
card_detect_pin_level=$(echo $sd_state_value | awk '{print rshift(and($1,0x40000),18)}')
write_protect_switch_pin_level=$(echo $sd_state_value | awk '{print rshift(and($1,0x80000),19)}')

if [ $card_inserted -eq 1 ]
then
	sd_use=$(df -h | grep mmcblk1p1 | awk '{print $5}' | cut -d '%' -f 1)
	if [ $sd_use ]
	then
		if [ $sd_use -lt 99 ]
		then
			if [ -e /root/ipnc ]
			then
				ipnc_md5sum=$(md5sum /root/ipnc | awk '{print $1}')
				cp /root/ipnc /sdcard/test.dat;sync
				copied_md5sum=$(md5sum /sdcard/test.dat | awk '{print $1}')
				rm /sdcard/test.dat;sync
				if [ $ipnc_md5sum != $copied_md5sum ]
				then
					echo \"SD-card read/write error\" # output
					return 1
				fi
			fi
			sd_write_speed=$(dd bs=1024 count=1024 if=/dev/zero of=/sdcard/dumy 2> /tmp/dd.out;cat /tmp/dd.out | tail -n 1 | awk '{print $NF}';rm /tmp/dd.out)
			sd_read_speed=$(dd bs=1024 count=1024 if=/sdcard/dumy of=/dev/null 2> /tmp/dd.out;cat /tmp/dd.out | tail -n 1 | awk '{print $NF}';rm /tmp/dd.out)
			rm /sdcard/dumy
			echo \"SD card write speed: $sd_write_speed\",	# output
			echo \"SD card read speed: $sd_read_speed\"		# output
		else
			echo \"There is not enough space on the sd card.\"	# output
		fi
	else
		echo \"SD-card is not mounted.\"	# output
	fi
else
	echo \"SD card is not inserted\"		# output
fi
}

check_emmc()
{
	emmc_use=$(df -h | grep /dev/mmcblk0p5 | awk '{print $5}' | cut -d '%' -f 1) 
	if [ $emmc_use ]
	then
		if [ $emmc_use -le 70 ]
		then
			if [ -e /root/ipnc ]
			then
				ipnc_md5sum=$(md5sum /root/ipnc | awk '{print $1}')
				cp /root/ipnc /mnt/nand/test.dat;sync
				copied_md5sum=$(md5sum /mnt/nand/test.dat | awk '{print $1}')
				rm /mnt/nand/test.dat;sync
				if [ $ipnc_md5sum != $copied_md5sum ]
				then
					echo \"EMMC read/write error\"	# output
					return 1
				fi
			fi
			sd_write_speed=$(dd bs=1024 count=1024 if=/dev/zero of=/mnt/nand/dumy 2> /tmp/dd.out;cat /tmp/dd.out | tail -n 1 | awk '{print $NF}';rm /tmp/dd.out)
			sd_read_speed=$(dd bs=1024 count=1024 if=/mnt/nand/dumy of=/dev/null 2> /tmp/dd.out;cat /tmp/dd.out | tail -n 1 | awk '{print $NF}';rm /tmp/dd.out)
			rm /mnt/nand/dumy
			echo \"EMMC write speed: $sd_write_speed\",	# output
			echo \"EMMC read speed: $sd_read_speed\"	# output
		else
			echo \"There is not enough space on the EMMC partition\"	# output
		fi
	else
		echo \"EMMC partition is not mounted.\"	# output
	fi
}

check_eeprom()
{
	/root/i2cdiag  -c /etc/eeprom.i2c.conf -r 0x0 0x20 > /dev/null
	if [ $? -eq 0 ]
	then
		echo \"EEPROM read OK\"	# output
	else
		echo \"EEPROM read Fail\"	# output
	fi
}

check_audio_chip()
{
MODEL=`/root/eeprom_cpro -r pname`
if [ "${MODEL:0:10}" == "NEP1-W30H2" ] || [ "${MODEL:0:10}" == "NEP5-W30H2" ] || [ "${MODEL:0:10}" == "NEP6-W30H2" ] || [ "${MODEL:0:10}" == "NEP2-S03H2" ]
then
	/root/i2cdiag  -c /etc/audio.i2c0.conf -w 0x0- 0x00 >/dev/null
else
	/root/i2cdiag  -c /etc/audio.i2c.conf -w 0x0- 0x00 >/dev/null
fi
	if [ $? -eq 0 ]
	then
		echo \"Audio ACK OK\"	# output
	else
		echo \"Audio ACK Fail\"	# output
	fi
}

##############################################################################
echo "["						# json

echo "{"
echo "\"sd card\": ["
check_sdcard
echo "]},"

echo "{"
echo "\"nand\":["
check_emmc
echo "]},"

echo "{"
echo "\"eeprom\":["
check_eeprom
echo "]},"

echo "{"
echo "\"audio\":["
check_audio_chip
echo "]},"

echo "{"
echo "\"system files\":["
/root/verchk.sh > /dev/null
grep ERROR report
if [ $? -eq 0 ]
then
	echo \""File system tampered\""
else
	echo "\"File system OK\""
fi
echo "]}"

echo "]"
