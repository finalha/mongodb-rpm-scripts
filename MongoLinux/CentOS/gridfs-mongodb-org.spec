#%define debug_package %{nil}
#%define _binaries_in_noarch_packages_terminate_build   0
%global dbservicename  mongodnetbrain1,mongodnetbrain2,
%global dbsystemuser   netbrain,netbrain,
%global dbsystemgroup  netbrain,netbrain,
%global confpath /opt/mongodb1,/opt/mongodb2,
%global dbpath /bin,/bin, 
%global datapath /opt/mongodb1/data,/home/netbrain/mongodb2/data
%global logpath /opt/mongodb1/log,/opt/mongodb2/log
%global bindip 127.0.0.1,127.0.0.1,
%global dbport 27017,27018,
%global replicasetname rsnetbrain,rsnetbrain,
%global cpulimit 90%,90%,
%global memorylimit 90%,90%,
%global singlenode yes,yes,
%global requiressl no,no,
%global image no,no,
 
Name: mongodbconfig
Prefix: /usr
Conflicts: mongo-10gen-enterprise, mongo-10gen-enterprise-server, mongo-10gen-unstable, mongo-10gen-unstable-enterprise, mongo-10gen-unstable-enterprise-mongos, mongo-10gen-unstable-enterprise-server, mongo-10gen-unstable-enterprise-shell, mongo-10gen-unstable-enterprise-tools, mongo-10gen-unstable-mongos, mongo-10gen-unstable-server, mongo-10gen-unstable-shell, mongo-10gen-unstable-tools, mongo18-10gen, mongo18-10gen-server, mongo20-10gen, mongo20-10gen-server, mongodb, mongodb-server, mongodb-dev, mongodb-clients, mongodb-10gen, mongodb-10gen-enterprise, mongodb-10gen-unstable, mongodb-10gen-unstable-enterprise, mongodb-10gen-unstable-enterprise-mongos, mongodb-10gen-unstable-enterprise-server, mongodb-10gen-unstable-enterprise-shell, mongodb-10gen-unstable-enterprise-tools, mongodb-10gen-unstable-mongos, mongodb-10gen-unstable-server, mongodb-10gen-unstable-shell, mongodb-10gen-unstable-tools, mongodb-enterprise, mongodb-enterprise-mongos, mongodb-enterprise-server, mongodb-enterprise-shell, mongodb-enterprise-tools, mongodb-nightly, mongodb-org-unstable, mongodb-org-unstable-mongos, mongodb-org-unstable-server, mongodb-org-unstable-shell, mongodb-org-unstable-tools, mongodb-stable, mongodb18-10gen, mongodb20-10gen, mongodb-enterprise-unstable, mongodb-enterprise-unstable-mongos, mongodb-enterprise-unstable-server, mongodb-enterprise-unstable-shell, mongodb-enterprise-unstable-tools, mongodbconfig
Version: 1
Release: 0
Obsoletes: mongo-10gen
Provides: mongo-10gen
Summary: MongoDB open source document-oriented database system (metapackage)
License: AGPL 3.0
URL: http://www.mongodb.org
Group: Applications/Databases

#Source0: %{name}-%{version}.tar.gz

#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#Requires: openssl
#Requires: python >= 3.4.3
#Requires: pymongo >= 3.0.2
#Requires:bc
Requires(pre):lsof
#Requires:libcgroup
#Requires:libcgroup-tools
Requires(pre):numactl
Requires(pre):libcgroup
Requires(pre):libcgroup-tools
#Requires(pre):yum -y install libcgroup
#Requires(pre):yum -y install libcgroup-tools
Source0: mongodbconfig-1.0.tgz
Source1: init.d-mongod
Source2: mongod.conf
Source3: mongod.sysconfig
Source4: disable-transparent-hugepages
Source5: tuned.conf
Source6: mongodb.pem
Source7: mongodb-keyfile
BuildArch: noarch

BuildRoot: %{_tmppath}/%{name}-buildroot


%description

%prep

%setup

%build

%install
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

if [ -z "$dbservicename" ] ; then
	dbservicename=%{dbservicename}
fi

if [ -z "$dbsystemuser" ] ; then
	dbsystemuser=%{dbsystemuser}
fi

if [ -z "$dbsystemgroup" ] ; then
	dbsystemgroup=%{dbsystemgroup}
fi

if [ -z "$confpath" ] ; then
	confpath=%{confpath}
fi

if [ -z "$dbpath" ] ; then
	dbpath=%{dbpath}
fi

if [ -z "$datapath" ] ; then
	datapath=%{datapath}
fi

if [ -z "$logpath" ] ; then
	logpath=%{logpath}
fi

if [ -z "$bindip" ] ; then
	bindip=%{bindip}
fi

if [ -z "$dbport" ] ; then
	dbport=%{dbport}
fi

if [ -z "$replicasetname" ] ; then
	replicasetname=%{replicasetname}
fi

if [ -z "$cpulimit" ] ; then
	cpulimit=%{cpulimit}
fi

if [ -z "$memorylimit" ] ; then
	memorylimit=%{memorylimit}
fi

if [ -z "$requiressl" ] ; then
	requiressl=%{requiressl}
fi

if [ -z "$singlenode" ] ; then
	singlenode=%{singlenode}
fi

if [ -z "$image" ] ; then
	image=%{image}
fi

number=$(grep -o '\[mongodb' /etc/gridfs-install.conf |wc -l)
unset parameter
for i in `seq $number` 
do   
   parameter[0]="$(echo $dbservicename|cut -d "," -f$i)"
   parameter[1]="$(echo $dbsystemuser|cut -d "," -f$i)"
   parameter[2]="$(echo $dbsystemgroup|cut -d "," -f$i)"
   parameter[3]="$(echo $confpath|cut -d "," -f$i)"
   parameter[4]="$(echo $dbpath|cut -d "," -f$i)"
   #parameter[4]="/bin"
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
   
   mkdir -p $RPM_BUILD_ROOT/${parameter[4]}
   cp -rv %{_builddir}/%{buildsubdir}/${parameter[4]}/* $RPM_BUILD_ROOT/${parameter[4]}
   echo "BUILDROOT:$RPM_BUILD_ROOT"
   echo "DBPATH:${parameter[4]}"
   chmod a+x $RPM_BUILD_ROOT/${parameter[4]}
   mkdir -p $RPM_BUILD_ROOT/etc/init.d
   cp -v %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/${parameter[0]}
   chmod a+x $RPM_BUILD_ROOT/etc/init.d/${parameter[0]}
   mkdir -p $RPM_BUILD_ROOT/${parameter[3]}
   cp -v %{SOURCE2} $RPM_BUILD_ROOT/${parameter[3]}/mongod.conf
   cp -v %{SOURCE7} $RPM_BUILD_ROOT/${parameter[3]}/mongodb-keyfile
   mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
   cp -v %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/mongod
   mkdir -p $RPM_BUILD_ROOT/etc/init.d
   cp -vf %{SOURCE4} $RPM_BUILD_ROOT/etc/init.d/disable-transparent-hugepages
   mkdir -p $RPM_BUILD_ROOT/etc/tuned/no-thp
   cp -vf %{SOURCE5} $RPM_BUILD_ROOT/etc/tuned/no-thp/tuned.conf
   mkdir -p $RPM_BUILD_ROOT/${parameter[5]}
   mkdir -p $RPM_BUILD_ROOT/${parameter[6]}   
   touch $RPM_BUILD_ROOT/${parameter[6]}/mongod.log
   mkdir -p $RPM_BUILD_ROOT/etc/ssl
   cp -v %{SOURCE6} $RPM_BUILD_ROOT/etc/ssl/mongodb.pem
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
#initial installation
if test $1 = 1
then
if [ ! -f "/etc/gridfs-install.conf" ]; then  
echo "config file can not be found" 
exit 1 
fi 

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
exit 1 
fi 

#judge OS architecture,must be 64bit
uname -a|grep x86_64
if [ ! $? == 0 ];then
echo "The architecture of operation system must be 64bit, the installation will abort"
exit 1
fi

#if [ `whoami` = "root" ];then
# echo "You are root user"
#else
# echo "You are not root user, the installation will abort"
# exit 1
#fi

unset array
while IFS='' read -r line || [[ -n "$line" ]];do 
  read -r key value <<< "$line"
  if [[ ! $line =~ ^# && $line ]]; then
      #echo "Key:$key -Value:$value"
	  declare -A array
	  if [ "$key" == "DBServiceName" -o "$key" == "ConfPath" -o "$key" == "DBPath" -o "$key" == "DataPath" -o "$key" == "LogPath" -o "$key" == "DBPort" -o "$key" == "ReplicaSetName" -o "$key" == "DBUser" -o "$key" == "DBPassword" ];then
	  #echo "Key:$key -Value:$value"
	  echo "${array[$key]}" | grep -wq "$value"
	  if [ $? == 0 ];then
	  echo "The parameters of DBServiceName, ConfPath, DBPath, DataPath, LogPath, DBPort, ReplicaSetName, DBUser, DBPassword in gridfs-install.conf must differ from one another"
	  exit 1
	  else
	  array[$key]=${array[$key]}"$value,"
	  fi
	  else
	  array[$key]=${array[$key]}"$value,"
	  fi
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

if [ -z "$dbservicename" ] ; then
	dbservicename=%{dbservicename}
fi

if [ -z "$dbsystemuser" ] ; then
	dbsystemuser=%{dbsystemuser}
fi

if [ -z "$dbsystemgroup" ] ; then
	dbsystemgroup=%{dbsystemgroup}
fi

if [ -z "$confpath" ] ; then
	confpath=%{confpath}
fi

if [ -z "$dbpath" ] ; then
	dbpath=%{dbpath}
fi

if [ -z "$datapath" ] ; then
	datapath=%{datapath}
fi

if [ -z "$logpath" ] ; then
	logpath=%{logpath}
fi

if [ -z "$bindip" ] ; then
	bindip=%{bindip}
fi

if [ -z "$dbport" ] ; then
	dbport=%{dbport}
fi

if [ -z "$replicasetname" ] ; then
	replicasetname=%{replicasetname}
fi

if [ -z "$cpulimit" ] ; then
	cpulimit=%{cpulimit}
fi

if [ -z "$memorylimit" ] ; then
	memorylimit=%{memorylimit}
fi

if [ -z "$requiressl" ] ; then
	requiressl=%{requiressl}
fi

if [ -z "$singlenode" ] ; then
	singlenode=%{singlenode}
fi

if [ -z "$image" ] ; then
	image=%{image}
fi

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
   
   #calc free space of data folder
   topdir=$(echo ${parameter[5]}|cut -d "/" -f2)
   topdir="/"$topdir
   echo $topdir
   freespaceinMB=$(df -h -m $topdir | awk '/^\/dev/{print $4}')
   if [ -z "$freespaceinMB" ] ; then
   freespaceinMB=$(df -h -m $topdir | awk '/^tmpfs/{print $4}')
   fi
   #get the last node of replicasetmembers,if the node is arbitor,the free space of data folder cannot less than 30G
   arbitoripandport=$(echo ${parameter[18]}|awk -F " " '{print $NF}')
   arbitorip=$(echo $arbitoripandport|cut -d ":" -f1)
   if [ "$arbitorip" == "${parameter[7]}" ]; then
   if [ "$freespaceinMB" -ge "30720" ];then : ;else echo "The free space of data folder is less than 30GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi; 
   else
   #51200MB=50GB
   if [ "$freespaceinMB" -ge "51200" ];then : ;else echo "The free space of data folder is less than 50GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
   fi
   #calc free space of log folder
   topdir=$(echo ${parameter[6]}|cut -d "/" -f2)
   topdir="/"$topdir
   echo $topdir
   freespaceinMB=$(df -h -m $topdir | awk '/^\/dev/{print $4}')
   if [ -z "$freespaceinMB" ] ; then
   freespaceinMB=$(df -h -m $topdir | awk '/^tmpfs/{print $4}')
   fi
   #10240MB=10GB
   if [ "$freespaceinMB" -ge "10240" ];then : ;else echo "The free space of log folder is less than 10GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
   #if ssl equal to yes,check cert.pem and key.pem
   if [ "${parameter[12]}" == "yes" ]; then 
   if [ ! -f "${parameter[13]}" ]; then  
   echo "cert file can not be found" 
   exit 1 
   fi
   if [ ! -f "${parameter[14]}" ]; then  
   echo "ssl key file can not be found" 
   exit 1 
   fi
   fi
   
   totalMemoryInKB=$(free | awk '/^Mem:/{print $2}')
   echo $totalMemoryInKB
   if [ $totalMemoryInKB == 0 ]  
   then
     echo "The total memory cannot be 0KB, the installation will abort"
     exit 1
   fi
   
   ip a|grep ${parameter[7]}
   if [ ! $? == 0 ];then
     echo "Please fill out the actual IP address in install.conf, the installation will abort"
     exit 1
   fi

   if [ "${parameter[7]}" == "127.0.0.1" -o "${parameter[7]}" == "192.168.1.1" ];then
     echo "Please fill out the actual IP address in install.conf(can't be 127.0.0.1 or 192.168.1.1), the installation will abort"
     exit 1
   fi
     
   if ! /usr/bin/id -g ${parameter[2]} &>/dev/null; then
       /usr/sbin/groupadd -r ${parameter[2]}
   fi
   if ! /usr/bin/id ${parameter[1]} &>/dev/null; then
    /usr/sbin/useradd -r ${parameter[1]} > /dev/null 2>&1
   	/usr/sbin/useradd -g ${parameter[2]} -c ${parameter[1]} ${parameter[1]} --shell=/bin/false --no-create-home > /dev/null 2>&1
   fi
   done
fi

%post
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

if [ -z "$dbservicename" ] ; then
	dbservicename=%{dbservicename}
fi

if [ -z "$dbsystemuser" ] ; then
	dbsystemuser=%{dbsystemuser}
fi

if [ -z "$dbsystemgroup" ] ; then
	dbsystemgroup=%{dbsystemgroup}
fi

if [ -z "$confpath" ] ; then
	confpath=%{confpath}
fi

if [ -z "$dbpath" ] ; then
	dbpath=%{dbpath}
fi

if [ -z "$datapath" ] ; then
	datapath=%{datapath}
fi

if [ -z "$logpath" ] ; then
	logpath=%{logpath}
fi

if [ -z "$bindip" ] ; then
	bindip=%{bindip}
fi

if [ -z "$dbport" ] ; then
	dbport=%{dbport}
fi

if [ -z "$replicasetname" ] ; then
	replicasetname=%{replicasetname}
fi

if [ -z "$cpulimit" ] ; then
	cpulimit=%{cpulimit}
fi

if [ -z "$memorylimit" ] ; then
	memorylimit=%{memorylimit}
fi

if [ -z "$requiressl" ] ; then
	requiressl=%{requiressl}
fi

if [ -z "$singlenode" ] ; then
	singlenode=%{singlenode}
fi

if [ -z "$image" ] ; then
	image=%{image}
fi

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
   
   service ${parameter[0]} status > /dev/null 2>&1
  if [ $? == 0 ]  
  then
  systemctl stop ${parameter[0]} > /dev/null 2>&1
  fi
  #check port occupied,use lsof -i:portnumber
  checkport=$(lsof -i:${parameter[8]})
  if [ ! -z "$checkport" ]; then  
  echo "The port number is being used" 
  exit 1  
  fi
  #calculate memorylimit
  totalMemoryInGB=$(free -g | awk '/^Mem:/{print $2}')
  echo $totalMemoryInGB
  memorylimitnum=$(echo "${parameter[11]}"|cut -d "%" -f1)
  #if memorylimit=90%,then memorylimitnum=90
  cgroupMemoryInGB=$(awk "BEGIN {printf \"%.0f\n\", ($totalMemoryInGB*$memorylimitnum)/100}")
  echo $cgroupMemoryInGB
  #cacheSizeInGB=cgroupMemoryInGB*60%-1>1?cgroupMemoryInGB*60%-1:1
  cachevalueGB=$(awk "BEGIN {printf \"%.0f\n\", ($cgroupMemoryInGB*60)/100-1}")
  if [ "$cachevalueGB" -ge "1" ];then cacheSizeInGB=$cachevalueGB;else cacheSizeInGB=1;fi;
  echo $cacheSizeInGB
  
  if [ ! "${parameter[3]}" == "/etc/mongod1" ]; then
  if [ ! -d "${parameter[3]}" ] ; then
	mkdir -p ${parameter[3]}
  fi
  \cp -rf /etc/mongod1/* ${parameter[3]}
  fi
  if [ ! -d "${parameter[4]}" ] ; then
	mkdir -p ${parameter[4]}
  fi

  if [ ! -d "${parameter[5]}" ] ; then
	mkdir -p ${parameter[5]}
  fi

  if [ ! -d "${parameter[6]}" ] ; then
	mkdir -p ${parameter[6]}
  fi
  
  #if mongodb binary not exit,copy;if exists,check md5 value,if equal to binarys in rpm,contine;if not equal,break;  
  if [ -f "${parameter[4]}/mongod" ];then
  oldmongodmd5=$(md5sum ${parameter[4]}/mongod|cut -d " " -f1)
  newmongodmd5=$(md5sum ${parameter[3]}/bin/mongod|cut -d " " -f1)
  if [ ! $oldmongodmd5 = $newmongodmd5 ];then
  	echo "The file ${parameter[4]}/mongod already exists, and the value of MD5 is different from the file in rpm, the installation will abort"
    exit 1
  fi
  fi
  if [ ! -f "${parameter[4]}/mongo" -a ! -f "${parameter[4]}/mongobridge" -a ! -f "${parameter[4]}/mongod" -a ! -f "${parameter[4]}/mongodump" -a ! -f "$dbpath/mongoperf" -a ! -f "${parameter[4]}/mongorestore" -a ! -f "${parameter[4]}/mongos" -a ! -f "${parameter[4]}/mongostat" ]; then
  mv -f ${parameter[3]}/bin/* ${parameter[4]} >/dev/null 2>&1
  rm -rf ${parameter[3]}/bin >/dev/null 2>&1  
  fi
    
  mv -f ${parameter[3]}/data/* ${parameter[5]} >/dev/null 2>&1
  mv -f ${parameter[3]}/log/* ${parameter[6]} >/dev/null 2>&1
  \cp -rf /etc/init.d/mongod1 /etc/init.d/${parameter[0]}
  #modify the content of files
  sed -i "s@/etc/mongod1/mongod.conf@${parameter[3]}/mongod.conf@g" /etc/init.d/${parameter[0]}
  #add cgroup CPU config begin
  sed -i "s@mkdir -p /sys/fs/cgroup/cpu/mongod@mkdir -p /sys/fs/cgroup/cpu/${parameter[0]}@g" /etc/init.d/${parameter[0]}
  cpucount=$(nproc)
  cpulimitnum=$(echo "${parameter[10]}"|cut -d "%" -f1)
  #if cpulimit=90%,then cpulimitnum=90
  cpucfsquotaus=$(awk "BEGIN {printf \"%.0f\n\", (100000*$cpucount*$cpulimitnum)/100}")
  echo $cpucfsquotaus
  if [ $cpucfsquotaus == 0 ]  
  then
  echo "The cfs_quota_us of mongodb service cannot be 0,the installation will abort"
  exit 1
  fi
  sed -i "s@echo 40000 > /sys/fs/cgroup/cpu/mongod/cpu.cfs_quota_us@echo $cpucfsquotaus > /sys/fs/cgroup/cpu/${parameter[0]}/cpu.cfs_quota_us@g" /etc/init.d/${parameter[0]}
  sed -i "s@CGROUP_DAEMON=\"cpu:mongod\"@CGROUP_DAEMON=\"cpu:${parameter[0]}\"@g" /etc/init.d/${parameter[0]}
  #add cgroup CPU config end
  sed -i "s@MONGO_USER=mongod@MONGO_USER=${parameter[1]}@g" /etc/init.d/${parameter[0]}
  sed -i "s@MONGO_GROUP=mongod@MONGO_GROUP=${parameter[2]}@g" /etc/init.d/${parameter[0]}
  sed -i "s@/etc/mongod1/bin@${parameter[4]}@g" /etc/init.d/${parameter[0]}
  sed -i "s@/var/run/mongodb@/var/run/${parameter[0]}@g" /etc/init.d/${parameter[0]}
  chmod a+x /etc/init.d/${parameter[0]}
  #mkdir -p /etc/init.d
  #cp -vf %{SOURCE4} /etc/init.d/disable-transparent-hugepages
  chmod 755 /etc/init.d/disable-transparent-hugepages
  #change content of mongod.conf
  sed -i "s@/etc/mongod1/log@${parameter[6]}@g" ${parameter[3]}/mongod.conf
  sed -i "s@/var/lib/mongodb@${parameter[5]}@g" ${parameter[3]}/mongod.conf
  sed -i "s/25101/${parameter[8]}/g" ${parameter[3]}/mongod.conf
  sed -i "s/127.0.0.1/${parameter[7]},127.0.0.1/g" ${parameter[3]}/mongod.conf
  sed -i "s@replSetName: rs@replSetName: ${parameter[9]}@g" ${parameter[3]}/mongod.conf
  sed -i "s@pidFilePath: /var/run/mongodb/mongod.pid@pidFilePath: /var/run/${parameter[0]}/mongod.pid@g" ${parameter[3]}/mongod.conf
  sed -i "s@cacheSizeGB: 1@cacheSizeGB: $cacheSizeInGB@g" ${parameter[3]}/mongod.conf
  if [ "${parameter[12]}" == "yes" ]; then
  sed -i "s@#ssl:@ssl:@g" ${parameter[3]}/mongod.conf
  sed -i "s@#mode: requireSSL@mode: requireSSL@g" ${parameter[3]}/mongod.conf
  sed -i "s@#PEMKeyFile: /etc/ssl/mongodb.pem@PEMKeyFile: /etc/ssl/mongodb.pem@g" ${parameter[3]}/mongod.conf
  fi
  
  mkdir -p /var/run/${parameter[0]}
  touch ${parameter[6]}/mongod.log
  touch /var/run/${parameter[0]}/mongod.pid 
  
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[3]}
  chown -R ${parameter[1]}:${parameter[2]} /var/run/${parameter[0]}
  chown ${parameter[1]}:${parameter[2]} /var/run/${parameter[0]}/mongod.pid
  chmod -R a+x ${parameter[3]}
  #fix ENG-20731 begin
  #chown -R ${parameter[1]}:${parameter[2]} /home/netbrain
  #fix ENG-20731 end
  
  #chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}
  #chmod -R a+x ${parameter[4]}  
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongo
  chmod -R a+x ${parameter[4]}/mongo
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongobridge
  chmod -R a+x ${parameter[4]}/mongobridge
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongod
  chmod -R a+x ${parameter[4]}/mongod
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongodump
  chmod -R a+x ${parameter[4]}/mongodump
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongoperf
  chmod -R a+x ${parameter[4]}/mongoperf
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongorestore
  chmod -R a+x ${parameter[4]}/mongorestore
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongos
  chmod -R a+x ${parameter[4]}/mongos
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[4]}/mongostat
  chmod -R a+x ${parameter[4]}/mongostat
  
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[5]}
  chmod -R a+x ${parameter[5]}
  chown -R ${parameter[1]}:${parameter[2]} ${parameter[6]}
  chmod -R a+x ${parameter[6]}
  
  echo "export PATH=${parameter[4]}:$PATH">>~/.bashrc
  #echo "export PATH=${parameter[4]}:$PATH">>/home/${parameter[1]}/.bashrc
  #make .bashrc effective
  . ~/.bashrc
  #. /home/${parameter[1]}/.bashrc

  #config services,cgroup,limits and so on
  /sbin/chkconfig --add ${parameter[0]}
  #modify some config files
  systemctl stop ${parameter[0]} > /dev/null 2>&1
  if [ $? == 0 ]  
  then
  #remove match lines,add lines later in /etc/security/limits.conf.try command
  sed -i "/*          hard    nproc/d" /etc/security/limits.conf
  sed -i "/*          soft    nproc/d" /etc/security/limits.conf
  #sed -i "/$/a *          hard    nproc    64000" /etc/security/limits.conf
  #sed -i "/$/a *          soft    nproc    64000" /etc/security/limits.conf
  echo "*          hard    nproc    64000">>/etc/security/limits.conf
  echo "*          soft    nproc    64000">>/etc/security/limits.conf
  echo "*          hard    nofile   64000">>/etc/security/limits.conf
  echo "*          soft    nofile   64000">>/etc/security/limits.conf
  ulimit -n 64000
  ulimit -u 64000
  #remove match lines,add lines later in /etc/security/limits.d/20-nproc.conf on CentOS 7
  sed -i "/*          hard    nproc/d" /etc/security/limits.d/20-nproc.conf
  sed -i "/*          soft    nproc/d" /etc/security/limits.d/20-nproc.conf
  #sed -i "/$/a *          hard    nproc    64000" /etc/security/limits.d/20-nproc.conf
  #sed -i "/$/a *          soft    nproc    64000" /etc/security/limits.d/20-nproc.conf
  echo "*          hard    nproc    64000">>/etc/security/limits.d/20-nproc.conf
  echo "*          soft    nproc    64000">>/etc/security/limits.d/20-nproc.conf
  #kernel settings on CentOS7
  chkconfig --add disable-transparent-hugepages
  chkconfig disable-transparent-hugepages on
  #mkdir /etc/tuned/no-thp
  #cp -vf %{SOURCE5} /etc/tuned/no-thp/tuned.conf
  tuned-adm profile no-thp
  cat /sys/kernel/mm/transparent_hugepage/enabled
  cat /sys/kernel/mm/transparent_hugepage/defrag
  #add cgroup configuration
  #service cgconfig restart
  #systemctl set-property ${parameter[0]} CPUShares=1024
  systemctl set-property ${parameter[0]} MemoryLimit=$cgroupMemoryInGB"G"
  #chkconfig cgconfig on
  #get port from parameters input, firewall should allow access to ${parameter[8]} of this Linux machine
  service firewalld status|grep "running" > /dev/null 2>&1
  if [ $? == 0 ];then
  firewall-cmd --zone=public --add-port=${parameter[8]}/tcp --permanent > /dev/null 2>&1
  firewall-cmd --reload > /dev/null 2>&1
  iptables-save | grep ${parameter[8]} > /dev/null 2>&1
  fi
  #if ssl equal to yes,merge cert.pem+key.pem to mongodb.pem,and replace the old mongodb.pem
  if [ "${parameter[12]}" == "yes" ]; then
  cat "${parameter[14]}" "${parameter[13]}" > "${parameter[3]}/mongodb.pem"
  \cp -rf "${parameter[3]}/mongodb.pem" "/etc/ssl/mongodb.pem"
  fi
  #mongodb authentication config
  if [ "${parameter[17]}" == "yes" ];then
  sed -i "s@#security:@security:@g" ${parameter[3]}/mongod.conf
  sed -i "s@#authorization: disabled@authorization: enabled@g" ${parameter[3]}/mongod.conf
  fi
  if [ "${parameter[17]}" == "no" -a "${parameter[12]}" == "no" ]; then
  chown ${parameter[1]}:${parameter[2]} ${parameter[3]}/mongodb-keyfile
  chmod 600 ${parameter[3]}/mongodb-keyfile
  sed -i "s@#security:@security:@g" ${parameter[3]}/mongod.conf
  sed -i "s@#authorization: disabled@authorization: enabled@g" ${parameter[3]}/mongod.conf
  sed -i "s@#keyFile: /mnt/mongod1/mongodb-keyfile@keyFile: ${parameter[3]}/mongodb-keyfile@g" ${parameter[3]}/mongod.conf
  fi
  fi
  #image special config
  if [ "${parameter[19]}" == "yes" ]; then
  sed -i "s/${parameter[7]},127.0.0.1/127.0.0.1/g" ${parameter[3]}/mongod.conf
  echo "Mongodb has been installed successfully"
  /sbin/chkconfig ${parameter[0]} off
  #hint the customer to restart the operating system
  echo "Please restart the operating system to make kernel settings of mongodb take effect"
  else
  systemctl start ${parameter[0]} > /dev/null 2>&1
  if [ $? == 0 ];then
  #must sleep some seconds
  sleep 20
  if [ "${parameter[12]}" == "yes" ]; then
  $(which echo) "exit"|${parameter[4]}/mongo "${parameter[7]}:${parameter[8]}" --ssl --sslAllowInvalidCertificates
  else
  $(which echo) "exit"|${parameter[4]}/mongo "${parameter[7]}:${parameter[8]}"
  fi  
  if [ $? == 0 ];then
  echo "succeed to connect mongodb node:${parameter[7]}:${parameter[8]}"
  else 
  echo "failed to connect mongodb node:${parameter[7]}:${parameter[8]}"
  fi
  /sbin/chkconfig ${parameter[0]} on
  echo "Mongodb has been installed successfully"
  #rm -rf /etc/mongod1
  #add crontab:check the mongodb status every 1 minute,if crashed,the task will start the mongodb
    if [[ $(crontab -l) ]]; 
  then
     crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if /usr/sbin/service ${parameter[0]} status|grep -q \"(dead)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1"| crontab;
  else
     echo "*/1 * * * * /bin/bash -c 'if /usr/sbin/service ${parameter[0]} status|grep -q \"(dead)\"; then /usr/sbin/service ${parameter[0]} start; fi' >/dev/null 2>&1" | crontab;
  fi
  #hint the customer to restart the operating system
  echo "Please restart the operating system to make kernel settings of mongodb take effect"
  else 
  echo "failed to start mongodb service:${parameter[0]}"
  exit 1
  fi  
  fi
  done
rm -rf /etc/mongod1 >/dev/null 2>&1
  
%preun
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

if [ -z "$dbservicename" ] ; then
	dbservicename=%{dbservicename}
fi

if [ -z "$dbsystemuser" ] ; then
	dbsystemuser=%{dbsystemuser}
fi

if [ -z "$dbsystemgroup" ] ; then
	dbsystemgroup=%{dbsystemgroup}
fi

if [ -z "$confpath" ] ; then
	confpath=%{confpath}
fi

if [ -z "$dbpath" ] ; then
	dbpath=%{dbpath}
fi

if [ -z "$datapath" ] ; then
	datapath=%{datapath}
fi

if [ -z "$logpath" ] ; then
	logpath=%{logpath}
fi

if [ -z "$bindip" ] ; then
	bindip=%{bindip}
fi

if [ -z "$dbport" ] ; then
	dbport=%{dbport}
fi

if [ -z "$replicasetname" ] ; then
	replicasetname=%{replicasetname}
fi

if [ -z "$cpulimit" ] ; then
	cpulimit=%{cpulimit}
fi

if [ -z "$memorylimit" ] ; then
	memorylimit=%{memorylimit}
fi

if [ -z "$requiressl" ] ; then
	requiressl=%{requiressl}
fi

if [ -z "$singlenode" ] ; then
	singlenode=%{singlenode}
fi

if [ -z "$image" ] ; then
	image=%{image}
fi

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
   
   #echo "$i: ${parameter[*]}"
   
   #uninstallation
   if test $1 = 0
   then
   #backup data
   #if [ "$uninstallsavedata" == "yes" ]; then
   #currentdate=$(date +%Y%m%d)
   ##$(which mongodump) --host "$bindip" --port "$dbport" --out "$datapath/mongodbbackup/mongodump-$currentdate"
   #$dbpath/mongodump --host "$bindip" --port "$dbport" --out "$datapath/mongodbbackup/mongodump-$currentdate"
   #	if [ $? == 0 ];then
   #	echo "Mongodb backup successfully, please check folder $datapath/mongodbbackup/mongodump-$currentdate"
   #	else
   #	echo "Mongodb backup failed, the uninstallation will abort"
   #	exit 1
   #	fi
   #fi
   echo "Your current data will be kept under ${parameter[5]} after mongodb is uninstalled"
   echo "Mongodb service: ${parameter[0]} will be uninstalled, please wait"
   systemctl status ${parameter[0]} > /dev/null 2>&1
   if [ $? == 0 ];then
   systemctl stop ${parameter[0]} > /dev/null 2>&1   
   /sbin/chkconfig --del ${parameter[0]}
   fi
   fi
done   

%postun
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

if [ -z "$dbservicename" ] ; then
	dbservicename=%{dbservicename}
fi

if [ -z "$dbsystemuser" ] ; then
	dbsystemuser=%{dbsystemuser}
fi

if [ -z "$dbsystemgroup" ] ; then
	dbsystemgroup=%{dbsystemgroup}
fi

if [ -z "$confpath" ] ; then
	confpath=%{confpath}
fi

if [ -z "$dbpath" ] ; then
	dbpath=%{dbpath}
fi

if [ -z "$datapath" ] ; then
	datapath=%{datapath}
fi

if [ -z "$logpath" ] ; then
	logpath=%{logpath}
fi

if [ -z "$bindip" ] ; then
	bindip=%{bindip}
fi

if [ -z "$dbport" ] ; then
	dbport=%{dbport}
fi

if [ -z "$replicasetname" ] ; then
	replicasetname=%{replicasetname}
fi

if [ -z "$cpulimit" ] ; then
	cpulimit=%{cpulimit}
fi

if [ -z "$memorylimit" ] ; then
	memorylimit=%{memorylimit}
fi

if [ -z "$requiressl" ] ; then
	requiressl=%{requiressl}
fi

if [ -z "$singlenode" ] ; then
	singlenode=%{singlenode}
fi

if [ -z "$image" ] ; then
	image=%{image}
fi

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
   
   #echo "$i: ${parameter[*]}"
   
   #uninstallation
   if test $1 = 0
   then
   if [ -d "${parameter[5]}" ] ; then
   #rename data folder,add suffix of UTC time 
   mv ${parameter[5]} ${parameter[5]}$(date -u +"%Y|%b|%d|%T")
   fi
   if [ -d "${parameter[4]}" ] ; then
   	#rm -rf ${parameter[4]}/*
   	#rmdir ${parameter[4]} >/dev/null 2>&1
	rm -rf ${parameter[4]}/mongo
	rm -rf ${parameter[4]}/mongobridge
	rm -rf ${parameter[4]}/mongod
	rm -rf ${parameter[4]}/mongodump
	rm -rf ${parameter[4]}/mongoperf
	rm -rf ${parameter[4]}/mongorestore
	rm -rf ${parameter[4]}/mongos
	rm -rf ${parameter[4]}/mongostat
   fi
   if [ -d "${parameter[6]}" ] ; then
   	rm -rf ${parameter[6]}/*
   	rmdir ${parameter[6]} >/dev/null 2>&1
   fi	
   if [ -f "${parameter[3]}/mongodb-keyfile" ] ; then
   	rm -rf ${parameter[3]}/mongodb-keyfile >/dev/null 2>&1	
   fi
   if [ -f "${parameter[3]}/mongodb.pem" ] ; then
   	rm -rf ${parameter[3]}/mongodb.pem >/dev/null 2>&1	
   fi
   if [ -f "${parameter[3]}/mongod.conf" ] ; then
   	mv -f ${parameter[3]}/mongod.conf ${parameter[3]}/mongod.conf$(date -u +"%Y|%b|%d|%T")
   fi
   rm -rf /tmp/mongodb-$dbport.sock >/dev/null 2>&1
   rm -rf /etc/netbrainrssuccess* >/dev/null 2>&1
   rm -rf /etc/netbrainuserpwdsuccess* >/dev/null 2>&1
   #remove the task of mongodb restart
   crontab -l |sed "/service ${parameter[0]} start/d" |crontab
   echo "Mongodb service: ${parameter[0]} has been uninstalled successfully"
   fi
   
   #upgrade
   if test $1 -ge 1
   then
     /sbin/service ${parameter[0]} condrestart >/dev/null 2>&1 || :
   fi
done   

%files
#%defattr(-,root,root,-)
#%config(noreplace) ${confpath}/mongod.conf
#${dbpath}/*
##%{_mandir}/man1/mongod.1*
#/etc/init.d/${dbservicename}
#/etc/init.d/disable-transparent-hugepages
#/etc/tuned/no-thp/tuned.conf
#%config(noreplace) /etc/sysconfig/mongod
#%attr(0755,${dbsystemuser},${dbsystemgroup}) %dir ${datapath}
#%attr(0755,${dbsystemuser},${dbsystemgroup}) %dir ${logpath}
#%attr(0755,${dbsystemuser},${dbsystemgroup}) %dir /var/run/mongodb
#%attr(0640,${dbsystemuser},${dbsystemgroup}) %config(noreplace) %verify(not md5 size mtime) ${logpath}/mongod.log
#%doc GNU-AGPL-3.0
#%doc README
#%doc THIRD-PARTY-NOTICES
#%doc MPL-2

#%defattr(-,root,root,-)
%config(noreplace) /etc/mongod1/mongod.conf
/etc/mongod1/mongodb-keyfile
/etc/mongod1/bin/*
#%{_mandir}/man1/mongod.1*
/etc/init.d/mongod1
/etc/init.d/disable-transparent-hugepages
/etc/tuned/no-thp/tuned.conf
/etc/ssl/mongodb.pem
%config(noreplace) /etc/sysconfig/mongod
%config(noreplace) /etc/mongod1/log/mongod.log
%doc GNU-AGPL-3.0
%doc README
%doc THIRD-PARTY-NOTICES
%doc MPL-2

%changelog
