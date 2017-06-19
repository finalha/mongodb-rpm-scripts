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
installpath=/bin/netbrainlicense
servicename=netbrainlicense
configfile=licenseAgentSetting.conf

while $looptag ;do
#create netbrainlicense user and group
if ! /usr/bin/id -g netbrain &>/dev/null; then
    /usr/sbin/groupadd -r netbrain > /dev/null 2>&1
fi
if ! /usr/bin/id netbrain &>/dev/null; then
	/usr/sbin/useradd -r netbrain > /dev/null 2>&1
	/usr/sbin/useradd -g netbrain -c netbrain netbrain --shell=/bin/false --no-create-home > /dev/null 2>&1
fi
#copy files in bin folder
mkdir -p $installpath
\cp -rf ./bin/* $installpath
chmod -R a+x $installpath
chown -R netbrain:netbrain $installpath
#copy config file to /etc/init
\cp -rf ./$configfile /etc
chmod a+x /etc/$configfile
chown -R netbrain:netbrain /etc/$configfile

#copy service file and register service
\cp -rf ./$servicename /etc/init.d
chmod a+x /etc/init.d/$servicename
/sbin/chkconfig --add $servicename
  #systemctl start $servicename > /dev/null 2>&1
  #systemctl start $servicename
  cd $installpath
  ./licensed -f /etc/$configfile
  if [ $? == 0 ]; then
  echo "WF License Agent Server has been started"
  /sbin/chkconfig $servicename on
  else
  echo "WF License Agent Server has been installed successfully but cannot been started, please contact your administrator"
  looptag=false
  returnresult 1 
  break
  fi

#add autotask of service into crontab
if [[ $(crontab -l) ]]; 
  then
     crontab -l |sed "$ a */10 * * * * /bin/bash -c 'if /usr/sbin/service $servicename status|grep -q \"(dead)\"; then /usr/sbin/service $servicename start; fi' >/dev/null 2>&1"| crontab;
  else
     echo "*/10 * * * * /bin/bash -c 'if /usr/sbin/service $servicename status|grep -q \"(dead)\"; then /usr/sbin/service $servicename start; fi' >/dev/null 2>&1" | crontab;
fi

echo "succeed to execute install.sh"
looptag=false
returnresult 0
break
done;