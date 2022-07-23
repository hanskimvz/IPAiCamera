#!/bin/sh

export PATH=.:/bin:/sbin:/usr/bin:/usr/local/bin:/usr/sbin:$PATH

# Color code
white="\033[0m"
red="\033[31m"
blue="\033[34m"
green="\033[32m"
yellow="\033[33m"

# CPRO ModelInfo file
MODEL_INFO=/root/ModelInfo.ini

# DRAM DLL Register Address 
DLL0=0xec170090
DLL1=0xec170094
DLL2=0xec1700f0
DLL3=0xec1700f4

get_model_info()
{
	EXPR=$(echo -e /\\[$MODEL\\]/,/\\[.*\\]/{/[A-Za-z0-9]-[A-Za-z0-9]/d\;p})
	sed -n $EXPR $MODEL_INFO
}

set_dll()
{
	echo -e "Setting DLL values for $green$MODEL$white"
	for DLL in $DLL0 $DLL1 $DLL2 $DLL3;do
		$AMBA_DEBUG -w $DLL -d $MODEL_DLL
		echo $DLL: $MODEL_DLL
	done
}

amba_debug_check()
{
        AMBA_DEBUG=$(which amba_debug)
        if [ $? -ne 0 ]
        then
                echo -e "$red [SET DRAM DLL] ERROR: amba_debug not found. $white"
                exit 1
        fi

        lsmod | grep ambad > /dev/null
        if [ $? -ne 0 ]
        then
                echo -e "$red [SET DRAM DLL] ERROR: ambad module not found. $white"
                exit 1
        fi
        return 0
}

model_info_check()
{
	if [ ! -e $MODEL_INFO ]
	then
		echo -e "$red[SET DRAM DLL] ERROR: $MODEL_INFO not found$white"
		exit 1
	fi
}

read_dll()
{
	echo ""
	echo "==== DRAM DLL values ====="
        echo " address         value "
        echo "--------------------------"
        for DLL in $DLL0 $DLL1 $DLL2 $DLL3;do
                $AMBA_DEBUG -r $DLL | tr -d '\012'
                echo ""
        done
	echo "=========================="
	echo ""
}

get_model_dll()
{
	MODEL_DLL=$(get_model_info | grep -i ^dll | cut -d '=' -f 2 | sed -n 's/0x[0-9a-fA-F]\{8\}/\0/p')
}

main()
{
	if [ $ARGC -ne 1 ]
	then
		echo "usage: $0 [model-name]"
		echo "ex) $0 NAB5-SLAH2"
		exit 1
	fi

	model_info_check
	amba_debug_check
	get_model_dll

	if [ $MODEL_DLL ]
	then
		echo -e "DLL value for $green$MODEL$white in the $MODEL_INFO : $green $MODEL_DLL $white"
		set_dll
		read_dll
	else
		echo -e "$red[ERROR]$white Invalid DRAM DLL value for $green$MODEL$white in the $MODEL_INFO : `get_model_info | grep ^dll | cut -d '=' -f 2 ` $white"
	fi
}

ARGC=$#
MODEL=$1

main
