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
oldIFS=$IFS
#IFS=' '
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

#copy ./install.conf to /etc/install.conf
\cp -rf ./install.conf /etc/install.conf
if [ $? -ne 0 ]; then
echo "fail to copy install.conf, the installation will abort"
looptag=false
returnresult 1 
break
fi

#read parameters in /etc/install.conf
while IFS='' read -r line || [[ -n "$line" ]];do 
  read -r key value <<< "$line"
  if [[ ! $line =~ ^# && $line ]]; then
      #echo "Key:$key -Value:$value"
	  declare -A array
	  array[$key]="$value"
  fi
done < "/etc/install.conf"
for keyname in "${!array[@]}";do
		case $keyname in 
			"DBServiceName") dbservicename=${array[$keyname]} ;;
			"DBSystemUser") dbsystemuser=${array[$keyname]} ;;
			"DBSystemGroup") dbsystemgroup=${array[$keyname]} ;;
			"ConfPath") confpath=${array[$keyname]} ;;
			#"DBPath") dbpath=${array[$keyname]} ;;
			"DataPath") datapath=${array[$keyname]} ;;
			"LogPath") logpath=${array[$keyname]} ;;
			"BindIp") bindip=${array[$keyname]} ;;
			"DBPort") dbport=${array[$keyname]} ;;
			"ReplicaSetName") replicasetname=${array[$keyname]} ;;
			"CPULimit") cpulimit=${array[$keyname]} ;;
			"MemoryLimit") memorylimit=${array[$keyname]} ;;
			"RequireSSL") requiressl=${array[$keyname]} ;;	
			"CertPath") certpath=${array[$keyname]} ;;
			"KeyPath") keypath=${array[$keyname]} ;;
			"DBUser") dbuser=${array[$keyname]} ;;
			"DBPassword") dbpassword=${array[$keyname]} ;;
			"SingleNode") singlenode=${array[$keyname]} ;;	
			"ReplicaSetMembers") replicasetmembers=${array[$keyname]} ;;
			"Image") image=${array[$keyname]} ;;
        esac			
		#echo "key  : $keyname"
        #echo "value: ${array[$keyname]}"
done;
dbpath=/bin
    
echo "DBServiceName value is :$dbservicename"
echo "DBSystemUser value is :$dbsystemuser"
echo "DBSystemGroup value is :$dbsystemgroup"
echo "ConfPath value is :$confpath"
echo "DBPath value is :$dbpath"
echo "DataPath value is :$datapath"
echo "LogPath value is :$logpath"
echo "BindIp value is :$bindip"
echo "DBPort value is :$dbport"
echo "ReplicaSetName value is :$replicasetname"
echo "CPULimit value is :$cpulimit"
echo "MemoryLimit value is :$memorylimit"
echo "RequireSSL value is :$requiressl"
echo "CertPath value is :$certpath"
echo "KeyPath value is :$keypath"
echo "DBUser value is :$dbuser"
echo "DBPassword value is :******"
echo "SingleNode value is :$singlenode"
echo "ReplicaSetMembers value is :$replicasetmembers"
echo "Image value is :$image"

#copy rpm to /etc/preinstallcomponents
echo "Installing third-party components will take a few minutes, please wait"
mkdir -p /etc/preinstallcomponents
\cp -rf ./preinstallcomponents/* /etc/preinstallcomponents

./preinstallcomponents.sh
if [ $? -ne 0 ]; then
echo "fail to execute preinstallcomponents.sh, the installation will abort"
looptag=false
returnresult 1 
break
fi

rpm -ivh mongodbconfig-1-0.noarch.rpm
service $dbservicename status|grep "running" > /dev/null 2>&1
if [ $? -ne 0 ];then
echo "fail to install mongodbconfig-1-0.noarch.rpm, the installation will abort"
looptag=false
returnresult 1 
break
fi

if [ "$singlenode" == "no" ]; then
for   rsmember  in   $replicasetmembers    
	do      
	rsip=$(echo $rsmember|cut -d ":" -f1)
	rsport=$(echo $rsmember|cut -d ":" -f2)
	if [ "$requiressl" == "yes" ]; then
    $(which echo) "exit"|$dbpath/mongo "$rsip:$rsport" --ssl --sslAllowInvalidCertificates
    else
    $(which echo) "exit"|$dbpath/mongo "$rsip:$rsport"
    fi
	if [ $? -ne 0 ];then
	#echo "failed to connect mongodb node:$rsip:$rsport, the installation will finish"
	echo "please make sure that mongodb node:$rsip:$rsport has been installed, the replica set will be configured after all nodes of mongodb installed successfully"
    looptag=false
    returnresult 0 
    break
	fi
done
fi
	
#if [ "$image" == "no" ]; then
#. mongodbconfig.sh
#else
#. image.sh
#fi

./mongodbconfig.sh
if [ $? -ne 0 ]; then
echo "fail to execute initialization scripts, the installation will abort"
looptag=false
returnresult 1 
break
fi

echo "succeed to execute install.sh"
echo "Please restart the operating system to make kernel settings of mongodb take effect"
looptag=false
returnresult 0 
break
done;
IFS=$oldIFS	