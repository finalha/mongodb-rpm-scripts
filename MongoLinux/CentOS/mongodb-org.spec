#%define debug_package %{nil}
#%define _binaries_in_noarch_packages_terminate_build   0
#define replicaset name:rs
#%global replicaset rs
#define service name:mongors
#%global servicename mongors
%global dbservicename mongodnetbrain 
%global dbsystemuser	netbrain 
%global dbsystemgroup netbrain
%global rootpath /home/netbrain/mongodb
%global dbpath /home/netbrain/mongodb/bin 
%global datapath /home/netbrain/mongodb/data
%global logpath /home/netbrain/mongodb/log
%global bindip 127.0.0.1
%global dbport 27017
%global replicasetname rsnetbrain
%global cpulimit 90%
%global memorylimit 90%
%global singlenode yes
%global requiressl no
%global image no
 
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
Requires:lsof
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

if [ -z "$rootpath" ] ; then
	rootpath=%{rootpath}
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
echo "SingleNode value is :$singlenode"
echo "ReplicaSetMembers value is :$replicasetmembers"
echo "ReplicaSetKeyFile value is :$replicasetkeyfile"
echo "Image value is :$image"

mkdir -p $RPM_BUILD_ROOT/$dbpath
cp -rv %{_builddir}/%{buildsubdir}/$dbpath/* $RPM_BUILD_ROOT/$dbpath
echo "BUILDROOT:$RPM_BUILD_ROOT"
echo "DBPATH:$dbpath"
chmod a+x $RPM_BUILD_ROOT/$dbpath
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp -v %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/$dbservicename
chmod a+x $RPM_BUILD_ROOT/etc/init.d/$dbservicename
mkdir -p $RPM_BUILD_ROOT/$rootpath
cp -v %{SOURCE2} $RPM_BUILD_ROOT/$rootpath/mongod.conf
cp -v %{SOURCE7} $RPM_BUILD_ROOT/$rootpath/mongodb-keyfile
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
cp -v %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/mongod
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp -vf %{SOURCE4} $RPM_BUILD_ROOT/etc/init.d/disable-transparent-hugepages
mkdir -p $RPM_BUILD_ROOT/etc/tuned/no-thp
cp -vf %{SOURCE5} $RPM_BUILD_ROOT/etc/tuned/no-thp/tuned.conf
mkdir -p $RPM_BUILD_ROOT/$datapath
mkdir -p $RPM_BUILD_ROOT/$logpath
#mkdir -p $RPM_BUILD_ROOT/var/run/mongodb
touch $RPM_BUILD_ROOT/$logpath/mongod.log
mkdir -p $RPM_BUILD_ROOT/etc/ssl
cp -v %{SOURCE6} $RPM_BUILD_ROOT/etc/ssl/mongodb.pem

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
#initial installation
if test $1 = 1
then
if [ ! -f "/etc/install.conf" ]; then  
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

if [ `whoami` = "root" ];then
 echo "You are root user"
else
 echo "You are not root user, the installation will abort"
 exit 1
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

if [ -z "$rootpath" ] ; then
	rootpath=%{rootpath}
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

#if [ -z "$replicasetmembers" ] ; then
#	echo "replicasetmembers can not be found"
#    exit 1
#fi

#echo "$rootpath" | grep -q "/home" || echo "$dbpath" | grep -q "/home" || echo "$datapath" | grep -q "/home" || echo "$logpath" | grep -q "/home"
#if [ $? == 0 ];then  
#	echo "The parameters of rootpath,dbpath,datapath,logpath cannot contain /home"
#	exit 1
#fi

#calc free space of data folder
topdir=$(echo $datapath|cut -d "/" -f2)
topdir="/"$topdir
echo $topdir
freespaceinMB=$(df -h -m $topdir | awk '/^\/dev/{print $4}')
if [ -z "$freespaceinMB" ] ; then
freespaceinMB=$(df -h -m $topdir | awk '/^tmpfs/{print $4}')
fi
#51200MB=50GB
#the command not work in RedHat7
#c=$(echo "$freespaceinMB > 51200" | bc)
#if [ $c -eq 1 ];then : ;else echo "The free space of data folder is less than 50GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
if [ "$freespaceinMB" -ge "51200" ];then : ;else echo "The free space of data folder is less than 50GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
#calc free space of log folder
topdir=$(echo $logpath|cut -d "/" -f2)
topdir="/"$topdir
echo $topdir
freespaceinMB=$(df -h -m $topdir | awk '/^\/dev/{print $4}')
if [ -z "$freespaceinMB" ] ; then
freespaceinMB=$(df -h -m $topdir | awk '/^tmpfs/{print $4}')
fi
#10240MB=10GB
#the command not work in RedHat7
#c=$(echo "$freespaceinMB > 10240" | bc)
#if [ $c -eq 1 ];then : ;else echo "The free space of log folder is less than 10GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
if [ "$freespaceinMB" -ge "10240" ];then : ;else echo "The free space of data folder is less than 50GB. It may result in insufficient disk space after a period of use, the installation will abort";exit 1;fi;
#if ssl equal to yes,check cert.pem and key.pem
if [ "$requiressl" == "yes" ]; then 
if [ ! -f "$certpath" ]; then  
echo "cert file can not be found" 
exit 1 
fi
if [ ! -f "$keypath" ]; then  
echo "ssl key file can not be found" 
exit 1 
fi
fi
#if ssl equal to no, singlenode equal to no ,check the replicasetkeyfile 
if [ "$singlenode" == "no" -a "$requiressl" == "no" -a ! -f "$replicasetkeyfile" ]; then
echo "replicaset key file can not be found" 
exit 1 
fi

if ! /usr/bin/id -g $dbsystemgroup &>/dev/null; then
    /usr/sbin/groupadd -r $dbsystemgroup
fi
if ! /usr/bin/id $dbsystemuser &>/dev/null; then
	/usr/sbin/useradd -g $dbsystemgroup -c $dbsystemuser $dbsystemuser > /dev/null 2>&1
fi
fi

%post
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

if [ -z "$rootpath" ] ; then
	rootpath=%{rootpath}
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

#if [ -z "$replicasetmembers" ] ; then
#	echo "replicasetmembers can not be found"
#    exit 1
#fi

#initial installation
#if test $1 = 1
#then
  service $dbservicename status > /dev/null 2>&1
  if [ $? == 0 ]  
  then
  systemctl stop $dbservicename > /dev/null 2>&1
  fi
  #check port occupied,use lsof -i:portnumber
  checkport=$(lsof -i:$dbport)
  if [ ! -z "$checkport" ]; then  
  echo "The port number is being used" 
  exit 1  
  fi
  #calculate memorylimit
  totalMemoryInGB=$(free -g | awk '/^Mem:/{print $2}')
  echo $totalMemoryInGB
  memorylimitnum=$(echo "$memorylimit"|cut -d "%" -f1)
  #if memorylimit=90%,then memorylimitnum=90
  cgroupMemoryInGB=$(awk "BEGIN {printf \"%.0f\n\", ($totalMemoryInGB*$memorylimitnum)/100}")
  echo $cgroupMemoryInGB
  if [ $cgroupMemoryInGB == 0 ]  
  then
  echo "The memory of mongodb service cannot be 0GB,the installation will abort"
  exit 1
  fi
  #cacheSizeInGB=cgroupMemoryInGB*60%-1>1?cgroupMemoryInGB*60%-1:1
  cachevalueGB=$(awk "BEGIN {printf \"%.0f\n\", ($cgroupMemoryInGB*60)/100-1}")
  #the command not work in RedHat7
  #b=$(echo "$cachevalueGB > 1" | bc)
  #if [ $b -eq 1 ];then cacheSizeInGB=$cachevalueGB;else cacheSizeInGB=1;fi;
  if [ "$cachevalueGB" -ge "1" ];then cacheSizeInGB=$cachevalueGB;else cacheSizeInGB=1;fi;
  echo $cacheSizeInGB
  
  #cp -r /etc/mongod1 $rootpath
  #if [ "$rootpath" == "/etc/mongod1" ]; then
  #cp -r /etc/mongod1 $rootpath  
  #else
  #mv -f /etc/mongod1 $rootpath
  #fi
  if [ ! "$rootpath" == "/etc/mongod1" ]; then
  if [ ! -d "$rootpath" ] ; then
	mkdir -p $rootpath
  fi
  mv -f /etc/mongod1/* $rootpath
  fi
  if [ ! -d "$dbpath" ] ; then
	mkdir -p $dbpath
  fi

  if [ ! -d "$datapath" ] ; then
	mkdir -p $datapath
  fi

  if [ ! -d "$logpath" ] ; then
	mkdir -p $logpath
  fi
  
#  #check some dirs,must be empty  
#  if [ "`ls -A $dbpath`" = "" ]; then
#    :
#  else
#    echo "$dbpath is not empty, the installation will abort"
#    exit 1
#  fi
#  
#  if [ "`ls -A $datapath`" = "" ]; then
#    :
#  else
#    echo "$datapath is not empty, the installation will abort"
#    exit 1
#  fi
#  
#  if [ "`ls -A $logpath`" = "" ]; then
#    :
#  else
#    echo "$logpath is not empty, the installation will abort"
#    exit 1
#  fi

  mv -f $rootpath/bin/* $dbpath >/dev/null 2>&1
  mv -f $rootpath/data/* $datapath >/dev/null 2>&1
  mv -f $rootpath/log/* $logpath >/dev/null 2>&1
  mv /etc/init.d/mongod1 /etc/init.d/$dbservicename
  #modify the content of files
  #chmod -R a+x $dbpath
  #change content of init.d/$dbservicename
  sed -i "s@/etc/mongod1/mongod.conf@$rootpath/mongod.conf@g" /etc/init.d/$dbservicename
  #add cgroup CPU config begin
  sed -i "s@mkdir -p /sys/fs/cgroup/cpu/mongod@mkdir -p /sys/fs/cgroup/cpu/$dbservicename@g" /etc/init.d/$dbservicename
  cpucount=$(nproc)
  cpulimitnum=$(echo "$cpulimit"|cut -d "%" -f1)
  #if cpulimit=90%,then cpulimitnum=90
  cpucfsquotaus=$(awk "BEGIN {printf \"%.0f\n\", (100000*$cpucount*$cpulimitnum)/100}")
  echo $cpucfsquotaus
  if [ $cpucfsquotaus == 0 ]  
  then
  echo "The cfs_quota_us of mongodb service cannot be 0,the installation will abort"
  exit 1
  fi
  sed -i "s@echo 40000 > /sys/fs/cgroup/cpu/mongod/cpu.cfs_quota_us@echo $cpucfsquotaus > /sys/fs/cgroup/cpu/$dbservicename/cpu.cfs_quota_us@g" /etc/init.d/$dbservicename
  sed -i "s@CGROUP_DAEMON=\"cpu:mongod\"@CGROUP_DAEMON=\"cpu:$dbservicename\"@g" /etc/init.d/$dbservicename
  #add cgroup CPU config end
  sed -i "s@MONGO_USER=mongod@MONGO_USER=$dbsystemuser@g" /etc/init.d/$dbservicename
  sed -i "s@MONGO_GROUP=mongod@MONGO_GROUP=$dbsystemgroup@g" /etc/init.d/$dbservicename
  sed -i "s@/etc/mongod1/bin@$dbpath@g" /etc/init.d/$dbservicename
  sed -i "s@/var/run/mongodb@/var/run/$dbservicename@g" /etc/init.d/$dbservicename
  chmod a+x /etc/init.d/$dbservicename
  #mkdir -p /etc/init.d
  #cp -vf %{SOURCE4} /etc/init.d/disable-transparent-hugepages
  chmod 755 /etc/init.d/disable-transparent-hugepages
  #change content of mongod.conf
  sed -i "s@/etc/mongod1/log@$logpath@g" $rootpath/mongod.conf
  sed -i "s@/var/lib/mongodb@$datapath@g" $rootpath/mongod.conf
  sed -i "s/25101/$dbport/g" $rootpath/mongod.conf
  sed -i "s/127.0.0.1/$bindip,127.0.0.1/g" $rootpath/mongod.conf
  sed -i "s@replSetName: rs@replSetName: $replicasetname@g" $rootpath/mongod.conf
  sed -i "s@pidFilePath: /var/run/mongodb/mongod.pid@pidFilePath: /var/run/$dbservicename/mongod.pid@g" $rootpath/mongod.conf
  sed -i "s@cacheSizeGB: 1@cacheSizeGB: $cacheSizeInGB@g" $rootpath/mongod.conf
  if [ "$requiressl" == "yes" ]; then
  sed -i "s@#ssl:@ssl:@g" $rootpath/mongod.conf
  sed -i "s@#mode: requireSSL@mode: requireSSL@g" $rootpath/mongod.conf
  sed -i "s@#PEMKeyFile: /etc/ssl/mongodb.pem@PEMKeyFile: /etc/ssl/mongodb.pem@g" $rootpath/mongod.conf
  fi
  
  mkdir -p /var/run/$dbservicename
  touch $logpath/mongod.log
  touch /var/run/$dbservicename/mongod.pid 
  
  chown -R $dbsystemuser:$dbsystemgroup $rootpath
  chown -R $dbsystemuser:$dbsystemgroup /var/run/$dbservicename
  chown $dbsystemuser:$dbsystemgroup /var/run/$dbservicename/mongod.pid
  chmod -R a+x $rootpath
  #fix ENG-20731 begin
  chown -R $dbsystemuser:$dbsystemgroup /home/netbrain
  #fix ENG-20731 end
  
  chown -R $dbsystemuser:$dbsystemgroup $dbpath
  chmod -R a+x $dbpath  
  chown -R $dbsystemuser:$dbsystemgroup $datapath
  chmod -R a+x $datapath
  chown -R $dbsystemuser:$dbsystemgroup $logpath
  chmod -R a+x $logpath
  
  echo "export PATH=$dbpath:$PATH">>~/.bashrc
  echo "export PATH=$dbpath:$PATH">>/home/$dbsystemuser/.bashrc
  #make .bashrc effective
  #. ~/.bashrc
  #. /home/$dbsystemuser/.bashrc
  #echo "old:$PATH"
  #source ~/.bashrc
  #source /home/$dbsystemuser/.bashrc
  #realpath=$(sed -n '/export PATH=/'p ~/.bashrc)
  #echo $realpath
  #$realpath
  #echo "new:$PATH"
  #exec bash
  
  #config services,cgroup,limits and so on
  /sbin/chkconfig --add $dbservicename
  #modify some config files
  systemctl stop $dbservicename > /dev/null 2>&1
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
  #systemctl set-property $dbservicename CPUShares=1024
  systemctl set-property $dbservicename MemoryLimit=$cgroupMemoryInGB"G"
  #chkconfig cgconfig on
  #get port from parameters input, firewall should allow access to $dbport of this Linux machine
  service firewalld status|grep "running" > /dev/null 2>&1
  if [ $? == 0 ];then
  firewall-cmd --zone=public --add-port=$dbport/tcp --permanent > /dev/null 2>&1
  firewall-cmd --reload > /dev/null 2>&1
  iptables-save | grep $dbport > /dev/null 2>&1
  fi
  #if ssl equal to yes,merge cert.pem+key.pem to mongodb.pem,and replace the old mongodb.pem
  if [ "$requiressl" == "yes" ]; then
  cat "$keypath" "$certpath" > "$rootpath/mongodb.pem"
  \cp -rf "$rootpath/mongodb.pem" "/etc/ssl/mongodb.pem"
  fi
  #mongodb authentication config
  if [ "$singlenode" == "yes" ];then
  sed -i "s@#security:@security:@g" $rootpath/mongod.conf
  sed -i "s@#authorization: disabled@authorization: enabled@g" $rootpath/mongod.conf
  fi
  if [ "$singlenode" == "no" -a "$requiressl" == "no" -a -f "$replicasetkeyfile" ]; then
  rm -rf $rootpath/mongodb-keyfile
  cp -rf $replicasetkeyfile $rootpath/mongodb-keyfile
  chown $dbsystemuser:$dbsystemgroup $rootpath/mongodb-keyfile
  chmod 600 $rootpath/mongodb-keyfile
  sed -i "s@#security:@security:@g" $rootpath/mongod.conf
  sed -i "s@#authorization: disabled@authorization: enabled@g" $rootpath/mongod.conf
  sed -i "s@#keyFile: /mnt/mongod1/mongodb-keyfile@keyFile: $rootpath/mongodb-keyfile@g" $rootpath/mongod.conf
  fi
  fi
  #image special config
  if [ "$image" == "yes" ]; then
  sed -i "s/$bindip,127.0.0.1/127.0.0.1/g" $rootpath/mongod.conf
  echo "Mongodb has been installed successfully"
  #restart system 1 minutes later to make kernel settings work(only root user can run the command)
  shutdown -r 1
  else
  systemctl start $dbservicename > /dev/null 2>&1
  if [ $? == 0 ];then
  #must sleep some seconds
  sleep 20
  if [ "$requiressl" == "yes" ]; then
  $(which echo) "exit"|$dbpath/mongo "$bindip:$dbport" --ssl --sslAllowInvalidCertificates
  else
  $(which echo) "exit"|$dbpath/mongo "$bindip:$dbport"
  fi  
  if [ $? == 0 ];then
  echo "succeed to connect mongodb node:$bindip:$dbport"
  else 
  echo "failed to connect mongodb node:$bindip:$dbport"
  fi
  /sbin/chkconfig $dbservicename on
  echo "Mongodb has been installed successfully"
  #rm -rf /etc/mongod1
  #add crontab:check the mongodb status every 1 minute,if crashed,the task will start the mongodb
    if [[ $(crontab -l) ]]; 
  then
     crontab -l |sed "$ a */1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1"| crontab;
  else
     echo "*/1 * * * * /bin/bash -c 'if ! /usr/sbin/service $dbservicename status|grep -q \"(running)\"; then /usr/sbin/service $dbservicename start; fi' >/dev/null 2>&1" | crontab;
  fi
  #restart system 1 minutes later to make kernel settings work(only root user can run the command)
  shutdown -r 1
else 
echo "failed to start mongodb service:$dbservicename"
exit 1
fi  
fi

%preun
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

if [ -z "$rootpath" ] ; then
	rootpath=%{rootpath}
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
   echo "In order to maintain data integrity, please use mongodump to backup data before uninstalling"
   echo "Mongodb will be uninstalled, please wait"   
   systemctl stop $dbservicename > /dev/null 2>&1   
  /sbin/chkconfig --del $dbservicename
fi

%postun
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

if [ -z "$rootpath" ] ; then
	rootpath=%{rootpath}
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

#uninstallation
if test $1 = 0
then
#if [ -d "$dbpath" ] ; then
#	rm -rf $dbpath/*
#	rmdir $dbpath >/dev/null 2>&1
#fi
#if [ -d "$logpath" ] ; then
#	rm -rf $logpath/*
#	rmdir $logpath >/dev/null 2>&1
#fi	
#if [ -d "$rootpath" ] ; then
#	rm -rf $rootpath/*
#	rmdir $rootpath >/dev/null 2>&1
#fi
#if /usr/bin/id $dbsystemuser &>/dev/null; then
#	/usr/sbin/userdel -f $dbsystemuser >/dev/null 2>&1
#fi	
#if /usr/bin/id -g $dbsystemgroup &>/dev/null; then
#	/usr/sbin/groupdel $dbsystemgroup >/dev/null 2>&1
#fi
if [ -d "$datapath" ] ; then
#rename data folder,add suffix of UTC time 
mv $datapath $datapath$(date -u +"%Y|%b|%d|%T")
fi
if [ -d "$dbpath" ] ; then
	rm -rf $dbpath/*
	rmdir $dbpath >/dev/null 2>&1
fi
if [ -d "$logpath" ] ; then
	rm -rf $logpath/*
	rmdir $logpath >/dev/null 2>&1
fi	
if [ -f "$rootpath/mongodb-keyfile" ] ; then
	rm -rf $rootpath/mongodb-keyfile >/dev/null 2>&1	
fi
if [ -f "$rootpath/mongodb.pem" ] ; then
	rm -rf $rootpath/mongodb.pem >/dev/null 2>&1	
fi
if [ -f "$rootpath/mongod.conf" ] ; then
	mv -f $rootpath/mongod.conf $rootpath/mongod.conf$(date -u +"%Y|%b|%d|%T")
fi
rm -rf /tmp/mongodb-$dbport.sock >/dev/null 2>&1
rm -rf /etc/netbrainrssuccess >/dev/null 2>&1
rm -rf /etc/netbrainuserpwdsuccess >/dev/null 2>&1
#remove the task of mongodb restart
crontab -l |sed "/service $dbservicename start/d" |crontab
echo "Mongodb has been uninstalled successfully"
fi

#upgrade
if test $1 -ge 1
then
  /sbin/service $dbservicename condrestart >/dev/null 2>&1 || :
fi

%files
#%defattr(-,root,root,-)
#%config(noreplace) ${rootpath}/mongod.conf
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

%defattr(-,root,root,-)
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
