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
echo $oldIFS
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

#copy ./gridfs-install.conf to /etc/gridfs-install.conf
\cp -rf ./gridfs-install.conf /etc/gridfs-install.conf
if [ $? -ne 0 ]; then
echo "fail to copy gridfs-install.conf, the installation will abort"
looptag=false
returnresult 1 
break
fi

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

rpm -ivh gridfs-mongodbconfig-1-0.noarch.rpm
#service $dbservicename status > /dev/null 2>&1
if [ $? -ne 0 ];then
echo "fail to install gridfs-mongodbconfig-1-0.noarch.rpm, the installation will abort"
looptag=false
returnresult 1 
break
fi

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

number=$(grep -o '\[mongodb' /etc/gridfs-install.conf |wc -l)
unset parameter
for i in `seq $number` 
do   
   parameter[0]="$(echo $dbservicename|cut -d "," -f$i)"
   parameter[1]="$(echo $dbsystemuser|cut -d "," -f$i)"
   parameter[2]="$(echo $dbsystemgroup|cut -d "," -f$i)"
   parameter[3]="$(echo $confpath|cut -d "," -f$i)"
   #parameter[4]="$(echo $dbpath|cut -d "," -f$i)"
   parameter[4]="/bin"
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
   #the second loop begin
   if [ "${parameter[17]}" == "no" ]; then
   for   rsmember  in   ${parameter[18]}
   	do      
   	rsip=$(echo $rsmember|cut -d ":" -f1)
   	rsport=$(echo $rsmember|cut -d ":" -f2)
   	if [ "$requiressl" == "yes" ]; then
    $(which echo) "exit"|${parameter[4]}/mongo "$rsip:$rsport" --ssl --sslAllowInvalidCertificates
    else
    $(which echo) "exit"|${parameter[4]}/mongo "$rsip:$rsport"
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
   #the second loop stop
done

#echo "the image is : ${parameter[19]}"
#if [ "${parameter[19]}" == "no" ]; then
#. gridfs-mongodbconfig.sh
#else
#. gridfs-image.sh
#fi

./gridfs-mongodbconfig.sh
if [ $? -ne 0 ]; then
echo "fail to execute initialization scripts, the installation will abort"
looptag=false
returnresult 1 
break
fi

echo "succeed to execute gridfs-install.sh"
echo "Please restart the operating system to make kernel settings of mongodb take effect"
looptag=false
returnresult 0 
break
done;
IFS=$oldIFS	