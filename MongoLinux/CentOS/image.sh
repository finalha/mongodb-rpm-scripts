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
return 1 
break 
fi 

#judge OS architecture,must be 64bit
uname -a|grep x86_64
if [ ! $? == 0 ];then
echo "The architecture of operation system must be 64bit, the installation will abort"
looptag=false
return 1 
break
fi

if [ `whoami` = "root" ];then
 echo "You are root user"
else
 echo "You are not root user, the installation will abort"
 looptag=false
return 1 
break
fi

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
			"RootPath") rootpath=${array[$keyname]} ;;
			"DBPath") dbpath=${array[$keyname]} ;;
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
    
echo "DBServiceName value is :$dbservicename"
echo "DBSystemUser value is :$dbsystemuser"
echo "DBSystemGroup value is :$dbsystemgroup"
echo "RootPath value is :$rootpath"
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
#if not image mode,the script abort
if [ "$image" == "no" ]; then
echo "The mongodb was not installed in image mode, the script will abort" 
looptag=false
return 1 
break
fi
#modify network config
echo Please enter your network device name
read networkdevicename
echo Please enter your ip address
read localipaddress
echo Please enter your gateway
read localgateway
echo Please enter your dns
read localdns
echo Please enter your prefix
read localprefix

if [ ! -f "/etc/sysconfig/network-scripts/ifcfg-$networkdevicename" ]; then  
echo "network config file /etc/sysconfig/network-scripts/ifcfg-$networkdevicename cannot be found" 
looptag=false
return 1 
break 
fi
#sed -i "/BOOTPROTO=/d" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "/IPADDR=/d" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "/PREFIX=/d" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "/GATEWAY=/d" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "/DNS1=/d" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#
#sed -i "$ a BOOTPROTO=static" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "$ a IPADDR=$localipaddress" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "$ a PREFIX=$localprefix" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "$ a GATEWAY=$localgateway" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#sed -i "$ a DNS1=$localdns" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename

sed -i "s@BOOTPROTO=.*@BOOTPROTO=static@g" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
sed -i "s@IPADDR=.*@IPADDR=$localipaddress@g" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
sed -i "s@PREFIX=.*@PREFIX=$localprefix@g" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
sed -i "s@GATEWAY=.*@GATEWAY=$localgateway@g" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
sed -i "s@DNS1=.*@DNS1=$localdns@g" /etc/sysconfig/network-scripts/ifcfg-$networkdevicename
#restart network
service network restart > /dev/null 2>&1
#rename data folder and log folder if the scripts was executed several times
crontab -l |sed "/service $dbservicename start/d" |crontab
service $dbservicename stop > /dev/null 2>&1
sleep 5
if [ -d "$datapath" ] ; then
	mv $datapath $datapath$(date -u +"%Y|%b|%d|%T")
	mkdir -p $datapath
    chown -R $dbsystemuser:$dbsystemgroup $datapath
	chmod -R a+x $datapath
fi
if [ -d "$logpath" ] ; then
	mv $logpath $logpath$(date -u +"%Y|%b|%d|%T")
	mkdir -p $logpath
    chown -R $dbsystemuser:$dbsystemgroup $logpath
	chmod -R a+x $logpath
fi
#modify install.conf
#sed -i "/BindIp/d" /etc/install.conf
#sed -i "$ a BindIp       $localipaddress" /etc/install.conf
sed -i "s@BindIp.*@BindIp       $localipaddress@g" /etc/install.conf
#modify mongod.conf
#sed -i "s/127.0.0.1/$localipaddress,127.0.0.1/g" $rootpath/mongod.conf
sed -i "s@bindIp:.*@bindIp: $localipaddress,127.0.0.1  \# Listen to local interface only, comment to listen on all interfaces.@g" $rootpath/mongod.conf

##Annotate the autostart task in crontab first
#if [[ $(crontab -l) ]]; 
#  then
#	 crontab -l |sed "/service $dbservicename start/d" |crontab;	 
#	 #crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;	 
#	 if [[ $(crontab -l) ]];
#	 then 
#	 crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;
#	 else
#	 echo "*/1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
#	 fi
#  else
#     echo "*/1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
#fi

#remove /etc/imagemongodbconfig.log
if [ -f "/etc/imagemongodbconfig.log" ]; then
rm -rf "/etc/imagemongodbconfig.log"
fi
#Start the service of mongodb
service $dbservicename start > /dev/null 2>&1
if [ $? == 0 ];then
echo "succeed to start service of mongodb:$dbservicename" >> /etc/imagemongodbconfig.log
else
echo "failed to start service of mongodb:$dbservicename" >> /etc/imagemongodbconfig.log
looptag=false
return 1 
break
fi
#remove /etc/netbrainuserpwdsuccess and /etc/netbrainrssuccess
if [ -f "/etc/netbrainrssuccess" ]; then
rm -rf "/etc/netbrainrssuccess"
fi
if [ -f "/etc/netbrainuserpwdsuccess" ]; then
rm -rf "/etc/netbrainuserpwdsuccess"
fi
. mongodbconfig.sh >> /etc/imagemongodbconfig.log
/sbin/chkconfig $dbservicename on
if [[ $(crontab -l) ]]; 
	then
		crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;
	else
		echo "*/1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
fi
echo "succeed to executed image.sh" >> /etc/imagemongodbconfig.log
looptag=false
return 0 
break  
done;  
