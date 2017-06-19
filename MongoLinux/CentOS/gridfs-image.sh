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
   
unset array
while IFS='' read -r line || [[ -n "$line" ]];do 
  read -r key value <<< "$line"
  if [[ ! $line =~ ^# && $line ]]; then
      #echo "Key:$key -Value:$value"
	  declare -A array
	  array[$key]=${array[$key]}"$value,"
  fi
done < "/etc/gridfs-install.conf"
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

number=$(grep -o '\[mongodb' /etc/gridfs-install.conf |wc -l)
unset parameter
for i in `seq $number` 
do   
   parameter[0]="$(echo $dbservicename|cut -d "," -f$i)"
   parameter[1]="$(echo $dbsystemuser|cut -d "," -f$i)"
   parameter[2]="$(echo $dbsystemgroup|cut -d "," -f$i)"
   parameter[3]="$(echo $rootpath|cut -d "," -f$i)"
   parameter[4]="$(echo $dbpath|cut -d "," -f$i)"
   parameter[5]="$(echo $datapath|cut -d "," -f$i)"
   parameter[6]="$(echo $logpath|cut -d "," -f$i)"
   parameter[7]="$(echo $bindip|cut -d "," -f$i)"
   parameter[8]="$(echo $dbport|cut -d "," -f$i)"
   parameter[9]="$(echo $replicasetname|cut -d "," -f$i)"
   parameter[10]="$(echo $cpulimit|cut -d "," -f$i)"
   parameter[11]="$(echo $memorylimit|cut -d "," -f$i)"
   parameter[12]="$(echo $requiressl|cut -d "," -f$i)"
   parameter[13]="$(echo $certpath|cut -d "," -f$i)"
   parameter[14]="$(echo $keypath|cut -d "," -f$i)"
   parameter[15]="$(echo $dbuser|cut -d "," -f$i)"
   parameter[16]="$(echo $dbpassword|cut -d "," -f$i)"
   parameter[17]="$(echo $singlenode|cut -d "," -f$i)"
   parameter[18]="$(echo $replicasetmembers|cut -d "," -f$i)"
   parameter[19]="$(echo $image|cut -d "," -f$i)"
   
   echo "$i: ${parameter[*]}"
   
   #if not image mode,the script abort
   if [ "parameter[19]" == "no" ]; then
   echo "The mongodb was not installed in image mode, the script will abort" 
   looptag=false
   return 1 
   break
   fi
   
   #rename data folder and log folder if the scripts was executed several times
   crontab -l |sed "/service ${parameter[0]} start/d" |crontab
   service ${parameter[0]} stop > /dev/null 2>&1
   sleep 5
   if [ -d "parameter[5]" ] ; then
   	mv ${parameter[5]} parameter[5]$(date -u +"%Y|%b|%d|%T")
   	mkdir -p ${parameter[5]}
       chown -R parameter[1]:${parameter[2]} ${parameter[5]}
   	chmod -R a+x ${parameter[5]}
   fi
   if [ -d "parameter[6]" ] ; then
   	mv ${parameter[6]} parameter[6]$(date -u +"%Y|%b|%d|%T")
   	mkdir -p ${parameter[6]}
       chown -R parameter[1]:${parameter[2]} ${parameter[6]}
   	chmod -R a+x ${parameter[6]}
   fi
   #modify install.conf
   sed -i "s@BindIp.*@BindIp       $localipaddress@g" /etc/gridfs-install.conf
   #modify mongod.conf
   sed -i "s@bindIp:.*@bindIp: $localipaddress,127.0.0.1  \# Listen to local interface only, comment to listen on all interfaces.@g" parameter[3]/mongod.conf
   
   ##Annotate the autostart task in crontab first
   #if [[ $(crontab -l) ]]; 
   #  then
   #	 crontab -l |sed "/service ${parameter[0]} start/d" |crontab;	 
   #	 #crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if ! /usr/sbin/service ${parameter[0]} status|grep -q \"(running)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1"| crontab;	 
   #	 if [[ $(crontab -l) ]];
   #	 then 
   #	 crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if ! /usr/sbin/service ${parameter[0]} status|grep -q \"(running)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1"| crontab;
   #	 else
   #	 echo "*/1 * * * * /bin/bash -c 'if ! /usr/sbin/service ${parameter[0]} status|grep -q \"(running)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1" | crontab;
   #	 fi
   #  else
   #     echo "*/1 * * * * /bin/bash -c 'if ! /usr/sbin/service ${parameter[0]} status|grep -q \"(running)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1" | crontab;
   #fi
   
   #remove /etc/imagemongodbconfig.log
   if [ -f "/etc/imagemongodbconfig.log" ]; then
   rm -rf "/etc/imagemongodbconfig.log"
   fi
   #Start the service of mongodb
   service ${parameter[0]} start > /dev/null 2>&1
   if [ $? == 0 ];then
   echo "succeed to start service of mongodb:parameter[0]" >> /etc/imagemongodbconfig.log
   else
   echo "failed to start service of mongodb:parameter[0]" >> /etc/imagemongodbconfig.log
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
   /sbin/chkconfig ${parameter[0]} on
   if [[ $(crontab -l) ]]; 
   	then
   		crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if /usr/sbin/service ${parameter[0]} status|grep -q \"(dead)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1"| crontab;
   	else
   		echo "*/1 * * * * /bin/bash -c 'if /usr/sbin/service ${parameter[0]} status|grep -q \"(dead)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1" | crontab;
   fi   
   done
   . gridfs-mongodbconfig.sh >> /etc/imagemongodbconfig.log
   if [ $? == 0 ];then
   echo "succeed to executed image.sh" >> /etc/imagemongodbconfig.log
   else
   echo "failed to executed image.sh" >> /etc/imagemongodbconfig.log
   looptag=false
   return 1 
   break
   fi
looptag=false
return 0 
break  
done;  
