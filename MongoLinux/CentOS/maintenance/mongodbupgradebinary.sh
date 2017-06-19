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
break 
fi 

#judge OS architecture,must be 64bit
uname -a|grep x86_64
if [ ! $? == 0 ];then
echo "The architecture of operation system must be 64bit, the installation will abort"
looptag=false
break
fi

if [ `whoami` = "root" ];then
 echo "You are root user"
else
 echo "You are not root user, the installation will abort"
 looptag=false
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
			"ReplicaSetKeyFile") replicasetkeyfile=${array[$keyname]} ;;
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
echo "ReplicaSetKeyFile value is :$replicasetkeyfile"

#delete the auto-start task in cron, then stop mongodb service
crontab -l |sed "/service $dbservicename start/d" |crontab
systemctl stop $dbservicename > /dev/null 2>&1
#backup the bin folder,and the UTC time suffix
if [ $? == 0 ]  
then
	if [ -d "$dbpath" ] ; then
		mv $dbpath $dbpath$(date -u +"%Y|%b|%d|%T")
	fi
else
	echo "failed to stop mongodb service:$dbservicename, the script will abort"
    looptag=false
    break
fi
#copy the new bin folder,chown and chmod
if [ $? == 0 ]  
then
	if [ ! -d "$dbpath" ] ; then
		mkdir -p $dbpath
	fi
	mv -f ./bin/* $dbpath >/dev/null 2>&1
	chown -R $dbsystemuser:$dbsystemgroup $dbpath
	chmod -R a+x $dbpath
else
	echo "failed to backup the bin folder of mongodb:$dbpath, the script will abort"
    looptag=false
    break	
fi
#start mongodb service,and the auto-start task in cron
systemctl start $dbservicename > /dev/null 2>&1
if [ $? == 0 ]  
then
	if [[ $(crontab -l) ]]; 
	then
		crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;
	else
		echo "*/1 * * * * /bin/bash -c 'if /usr/sbin/service $dbservicename status|grep -q \"(dead)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
	fi
else
	echo "failed to start mongodb service:$dbservicename, the script will abort"
    looptag=false
    break
fi
echo "succeed to upgrade the binary file of mongodb"
looptag=false
break  
done;  
