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
ostype=centos
if [ -z "$osversion" ]; then 
osversion=$(cat /etc/redhat-release|cut -d " " -f7|cut -d "." -f1)
ostype=redhat
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

#if [ `whoami` = "root" ];then
# echo "You are root user"
#else
# echo "You are not root user, the installation will abort"
# looptag=false
#returnresult 1 
#break
#fi
#copy install.conf and gridfs-install.conf to /etc
\cp -rf ./install.conf /etc/install.conf >/dev/null 2>&1
\cp -rf ./gridfs-install.conf /etc/gridfs-install.conf >/dev/null 2>&1
#copy ./preinstallcomponents/* to /etc
mkdir -p /etc/preinstallcomponents
\cp -rf ./preinstallcomponents/* /etc/preinstallcomponents >/dev/null 2>&1
#use yum install first;if not work,use yum localinstall 
#CentOS7 install
if [ $ostype = "centos" ];then
rpm -qa|grep lsof-4.87 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install lsof-4.87 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/CentOS7/lsof-4.87-4.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install lsof"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install lsof"
fi

rpm -qa|grep numactl-2.0.9 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install numactl-2.0.9 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/CentOS7/numactl-2.0.9-6.el7_2.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install numactl"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install numactl"
fi

rpm -qa|grep libcgroup-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install libcgroup-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/CentOS7/libcgroup-0.41-11.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install libcgroup"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install libcgroup"
fi

rpm -qa|grep libcgroup-tools-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install libcgroup-tools-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/CentOS7/libcgroup-tools-0.41-11.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install libcgroup-tools"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install libcgroup-tools"
fi
else
#RedHat7 install
rpm -qa|grep lsof-4.87 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install lsof-4.87 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/RedHat7/lsof-4.87-4.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install lsof"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install lsof"
fi

rpm -qa|grep numactl-2.0.9 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install numactl-2.0.9 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/RedHat7/numactl-2.0.9-2.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install numactl"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install numactl"
fi

rpm -qa|grep libcgroup-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install libcgroup-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/RedHat7/libcgroup-0.41-6.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install libcgroup"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install libcgroup"
fi

rpm -qa|grep libcgroup-tools-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y install libcgroup-tools-0.41 >/dev/null 2>&1
if [ $? -ne 0 ]; then
yum -y localinstall /etc/preinstallcomponents/RedHat7/libcgroup-tools-0.41-6.el7.x86_64.rpm >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "fail to install libcgroup-tools"
	looptag=false
    returnresult 1 
break
fi
fi
echo "succeed to install libcgroup-tools"
fi
fi
	echo "succeed to execute preinstallcomponents.sh"
	looptag=false
	returnresult 0
break
done;	