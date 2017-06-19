#!/bin/bash
function returnresult()
{
   if [ $1 = "0" ];then
        return 0
   else
        return 1
   fi
}

looptag=true

while $looptag ;do 
#judge OS version,must be CentOS7.x
#cat /etc/redhat-release = Red Hat Enterprise Linux Server release 7.0 (Maipo)
#rpm -q centos-release = centos-release-7-2.1511.el7.centos.2.10.x86_64
osversion=$(rpm -q centos-release|cut -d "-" -f3)
if [ -z "$osversion" ]; then 
osversion=$(cat /etc/redhat-release|cut -d " " -f7|cut -d "." -f1)
fi
#osversion=7
if [ $osversion -lt 7 ]; then  
echo "The version of operation system must be 7.0 or above, the installation will abort"
looptag=false
returnresult 1
break 
fi 

#judge OS architecture,must be 64bit
uname -a|grep x86_64
if [ ! $? == 0 ];then
echo "The architecture of operation system must be 64bit, the installation will abort"
looptag=false
returnresult 1
break
fi

if [ `whoami` = "root" ];then
 echo "You are root user"
else
 echo "You are not root user, the installation will abort"
 looptag=false
returnresult 1
break
fi

echo Please enter the name of mongodb service\(default:mongodnetbrain\)
read dbservicename
echo "dbservicename is: $dbservicename" 
echo -e "Please enter your choose\n1 for stop mognodb service\n2 for start mongodb service"
read choose

if [ "$choose" = "1" ];then
systemctl stop $dbservicename > /dev/null 2>&1
#backup the bin folder,and the UTC time suffix
if [ $? == 0 ];then
    #delete the auto-start task in cron, then stop mongodb service
    crontab -l |sed "/service $dbservicename start/d" |crontab
    echo "succeed to stop mongodb service:$dbservicename"
    looptag=false
    returnresult 0
    break
else
    echo "failed to stop mongodb service:$dbservicename, the script will abort"
    looptag=false
    returnresult 1
    break
fi
fi

if [ "$choose" = "2" ];then
#start mongodb service,and the auto-start task in cron
systemctl start $dbservicename > /dev/null 2>&1
if [ $? == 0 ];then
    if [[ $(crontab -l) ]]; 
    then
        crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;
    else
        echo "*/1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
    fi
    echo "succeed to start mongodb service:$dbservicename"
    looptag=false
    returnresult 0
    break
else
    echo "failed to start mongodb service:$dbservicename, the script will abort"
    looptag=false
    returnresult 1
    break
fi
fi
done;  
