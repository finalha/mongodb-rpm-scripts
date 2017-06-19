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

#if [ `whoami` = "root" ];then
# echo "You are root user"
#else
# echo "You are not root user, the installation will abort"
# looptag=false
#returnresult 1 
#break
#fi

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
   #judge if gridfs-mongodbconfig.sh has been execute successfully
   if [ "${parameter[12]}" == "yes" ]; then
   $(which echo) "exit"|${parameter[4]}/mongo --host 127.0.0.1:${parameter[8]} -u "${parameter[15]}" -p "${parameter[16]}" --authenticationDatabase admin --ssl --sslAllowInvalidCertificates > /dev/null 2>&1
   else
   $(which echo) "exit"|${parameter[4]}/mongo --host 127.0.0.1:${parameter[8]} -u "${parameter[15]}" -p "${parameter[16]}" --authenticationDatabase admin > /dev/null 2>&1
   fi
   if [ $? == 0 ];then
   echo "gridfs-mongodbconfig.sh has been execute successfully for mongodb service:${parameter[0]}"
   looptag=false
   returnresult 0 
   break
   fi
   
   #config replicaset for three,five,seven or more nodes
  if [ "${parameter[12]}" == "yes" ]; then
  $(which echo) "exit"|${parameter[4]}/mongo "${parameter[7]}:${parameter[8]}" --ssl --sslAllowInvalidCertificates
  else
  $(which echo) "exit"|${parameter[4]}/mongo "${parameter[7]}:${parameter[8]}"
  fi
if [ $? == 0 ];then
  echo "succeed to connect mongodb node:${parameter[7]}:${parameter[8]}"
  #must sleep some seconds
  sleep 20
  if [ "${parameter[17]}" == "no" ]; then
    if [ -f "/etc/initreplica.js" ]; then  
    rm -rf /etc/initreplica.js
    fi 

    echo "var cfg = { _id: '${parameter[9]}'," >> "/etc/initreplica.js"
    echo "members: [" >> "/etc/initreplica.js"
    #echo " { _id: 0, host: '${parameter[7]}:${parameter[8]}', priority: 1000}," >> "/etc/initreplica.js"
    #i=1
	i=0
    for   rsmember  in   ${parameter[18]}    
    do      
    rsip=$(echo $rsmember|cut -d ":" -f1)
    rsport=$(echo $rsmember|cut -d ":" -f2)
    #if [ "$rsip:$rsport" = "${parameter[7]}:${parameter[8]}" ];then
    #continue
    #fi
    echo " { _id: $i, host: '$rsip:$rsport', priority: $(expr 1000 - 30 \* $i)}," >> "/etc/initreplica.js"
    i=$(expr $i + 1)
    done
    echo $i
    #change the last }, to be , arbiterOnly: true} ,means the last to be arbiter
    arbiterstr=$(sed -n '$p' "/etc/initreplica.js" | sed 's/\(.*\)},/\1, arbiterOnly: true}/')
    echo $arbiterstr
    sed -i '$d' "/etc/initreplica.js" 
    echo $arbiterstr >> "/etc/initreplica.js"
    
    echo "]" >> "/etc/initreplica.js"
    echo "};" >> "/etc/initreplica.js"
    echo "var error = rs.initiate(cfg);" >> "/etc/initreplica.js"
    echo "printjson(error);" >> "/etc/initreplica.js"    
    if [ ! -f "/etc/netbrainrssuccess${parameter[0]}" ]; then
    if [ "${parameter[12]}" == "yes" ]; then    
    ${parameter[4]}/mongo 127.0.0.1:${parameter[8]}/admin --ssl --sslAllowInvalidCertificates "/etc/initreplica.js"
    else
    ${parameter[4]}/mongo 127.0.0.1:${parameter[8]}/admin "/etc/initreplica.js"
    fi
    if [ $? == 0 ];then
    echo "succeed to init replicaset ${parameter[9]} of mongodb"    
    fi
    fi    
  else
  if [ ! -f "/etc/netbrainrssuccess${parameter[0]}" ]; then
  if [ "${parameter[12]}" == "yes" ]; then  
  $(which echo) "rs.initiate()"|${parameter[4]}/mongo "127.0.0.1:${parameter[8]}" --ssl --sslAllowInvalidCertificates
  else
  $(which echo) "rs.initiate()"|${parameter[4]}/mongo "127.0.0.1:${parameter[8]}"
  fi
  if [ $? == 0 ];then
    echo "succeed to init single node replicaset ${parameter[9]} of mongodb service:${parameter[0]}"
    echo "succeed to init replicaset ${parameter[9]} of mongodb service:${parameter[0]}" > /etc/netbrainrssuccess${parameter[0]}
  fi
  fi
  fi
  else 
  echo "failed to connect mongodb node:${parameter[7]}:${parameter[8]}"
  looptag=false
  returnresult 1 
  break
  fi
##restart mongodb service to make replicaset work
#systemctl restart ${parameter[0]} > /dev/null 2>&1
##must sleep some seconds
#sleep 10  
#add username and password (both username and password must not be empty) for replicaset or only this node
if [ ! -z "${parameter[15]}" -a ! -z "${parameter[16]}" ] ; then
    #must sleep some seconds
    sleep 20
#use js to get db.isMaster().ismaster 30 times, if get ture 10 times continuously, the replicaset is stable
    if [ -f "/etc/judgersstable.js" ]; then  
    rm -rf /etc/judgersstable.js
    fi 
    echo "var totaltimes = 30;" >> "/etc/judgersstable.js"
    echo "var continuoustimes = 0;" >> "/etc/judgersstable.js"
    echo "var successtag = 1;" >> "/etc/judgersstable.js"
    echo "for (i = 0; i < totaltimes; i++) {" >> "/etc/judgersstable.js"
    echo "var result = db.isMaster().ismaster;" >> "/etc/judgersstable.js"
    echo "if(result == true)" >> "/etc/judgersstable.js"
    echo "{" >> "/etc/judgersstable.js"
    echo "continuoustimes = continuoustimes+1;" >> "/etc/judgersstable.js"
    echo "}" >> "/etc/judgersstable.js"
    echo "else" >> "/etc/judgersstable.js"
    echo "{" >> "/etc/judgersstable.js"
    echo "continuoustimes = 0;" >> "/etc/judgersstable.js"
    echo "continue;" >> "/etc/judgersstable.js"
    echo "}" >> "/etc/judgersstable.js"
    echo "if(continuoustimes == 10)" >> "/etc/judgersstable.js"
    echo "{" >> "/etc/judgersstable.js"
    echo "successtag = 0;" >> "/etc/judgersstable.js"
    echo "printjson(successtag);" >> "/etc/judgersstable.js"
    echo "break;" >> "/etc/judgersstable.js"
    echo "}" >> "/etc/judgersstable.js"
    echo "}" >> "/etc/judgersstable.js"
    if [ "${parameter[12]}" == "yes" ]; then
    fullstring=$(${parameter[4]}/mongo 127.0.0.1:${parameter[8]} --ssl --sslAllowInvalidCertificates "/etc/judgersstable.js")
    else
    fullstring=$(${parameter[4]}/mongo 127.0.0.1:${parameter[8]} "/etc/judgersstable.js")    
    fi
    echo "fullstring = $fullstring"
    resultstring=${fullstring: -1}    
    echo "resultstring = $resultstring"
    #if not stable,exit shell
    if [ "$resultstring" == "1" ]; then
    echo "The node of mongodb is not stable, the shell will abort"
    looptag=false
    returnresult 1 
    break
    fi
    
    if [ "$resultstring" == "t" ]; then
    echo "The node of mongodb is not stable, the shell will abort"
    looptag=false
    returnresult 1 
    break
    fi
    
    if [ "$resultstring" == "0" ]; then
    if [ -f "/etc/adduserpassword.js" ]; then  
    rm -rf /etc/adduserpassword.js
    fi
    #echo "var existuser = db.getSiblingDB(\"admin\").getUsers()[0].user;" >> "/etc/adduserpassword.js"
    #echo "printjson(existuser);" >> "/etc/adduserpassword.js"
    #echo "if(existuser != \"${parameter[15]}\"){" >> "/etc/adduserpassword.js"
    echo "var userpassword = {" >> "/etc/adduserpassword.js"
    echo "user: \"${parameter[15]}\"," >> "/etc/adduserpassword.js"
    echo "pwd: \"${parameter[16]}\"," >> "/etc/adduserpassword.js"
    echo "roles: [ { role: \"root\", db: \"admin\" } ]" >> "/etc/adduserpassword.js"
    echo "};" >> "/etc/adduserpassword.js"
    echo "var error = db.createUser(userpassword);" >> "/etc/adduserpassword.js"
    #echo "var error = db.createUser(userpassword);}" >> "/etc/adduserpassword.js"
    
        
    if [ ! -f "/etc/netbrainuserpwdsuccess${parameter[0]}" ]; then
    if [ "${parameter[12]}" == "yes" ]; then
    ${parameter[4]}/mongo 127.0.0.1:${parameter[8]}/admin --ssl --sslAllowInvalidCertificates "/etc/adduserpassword.js"
    else
    ${parameter[4]}/mongo 127.0.0.1:${parameter[8]}/admin "/etc/adduserpassword.js"
    fi
    if [ $? == 0 ];then
    echo "succeed to add username:\"${parameter[15]}\",password:\"******\" for mongodb service:${parameter[0]}"
    echo "succeed to add username:\"${parameter[15]}\",password:\"******\" for mongodb service:${parameter[0]}" > /etc/netbrainuserpwdsuccess${parameter[0]}
    else
    echo "failed to add username:\"${parameter[15]}\",password:\"******\" for mongodb"
    looptag=false
    returnresult 1 
    break
    fi 
    fi
    
#restart mongodb service to make user and password work
systemctl restart ${parameter[0]} > /dev/null 2>&1
#must sleep some seconds
sleep 10
#test user and password work or not
if [ "${parameter[12]}" == "yes" ]; then
$(which echo) "exit"|${parameter[4]}/mongo --host 127.0.0.1:${parameter[8]} -u "${parameter[15]}" -p "${parameter[16]}" --authenticationDatabase admin --ssl --sslAllowInvalidCertificates
else
$(which echo) "exit"|${parameter[4]}/mongo --host 127.0.0.1:${parameter[8]} -u "${parameter[15]}" -p "${parameter[16]}" --authenticationDatabase admin
fi
if [ $? == 0 ];then
echo "succeed to login mongodb with username:\"${parameter[15]}\",password:\"******\""
else
echo "failed to login mongodb with username:\"${parameter[15]}\",password:\"******\""
fi
fi
fi
done
looptag=false
returnresult 0 
break     
done;  
