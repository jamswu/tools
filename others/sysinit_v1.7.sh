#!/bin/bash
#Version 1.7
#For CentOS_mini
#Made on 2015-01-20

echo "   "
echo "#############################################################################"
echo "#  Initialize for the CentOS 6.4/6.5 mini_installed.                        #"
echo "#                                                                           #"
echo "#  Please affirm this OS connected net already before running this script ! #" 
echo "#############################################################################"
echo "   "

format() {
          echo "-------Finished.--------"
          sleep 6
          echo "---------------------------"
          echo "  "
         }

##########################################################################
# Set time
echo "Set time."
/bin/cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &> /dev/null
yum -y install ntpdate &> /dev/null
ntpdate  0.centos.pool.ntp.org &> /dev/null
hwclock -w
format

##########################################################################
# Create Log
echo "Create log file."
DATE1=`date +"%F %H:%M"`
DATE2=`date +"%F"`
LOG=/var/log/sysinitinfo.log
echo $DATE1 >> $LOG
echo "------------------------------------------" >> $LOG
echo "For CentOS_mini" >> $LOG
echo "==================================================" >> $LOG
echo "Set timezone is Shanghai" >> $LOG
echo "Finished ntpdate" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Disabled Selinux
echo "Disabled SELinux."
sed -i 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/sysconfig/selinux
echo "=================================================="
echo "Disabled SELinux." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Stop iptables
echo "Stop iptables."
service iptables stop &> /dev/null
chkconfig --level 35 iptables off
echo "Stop iptables." >> $LOG
echo "==================================================" >> $LOG
format

##########################################################################
# Epel
echo "Install epel"
rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm &> /dev/null
echo "=================================================="
echo "Install epel" >> $LOG
echo "==================================================" >> $LOG
format

##########################################################################
#Yum install Development tools
echo "Install Development tools"
echo "It will be a moment,wait......"
yum -y groupinstall "Development tools" &> /dev/null
yum -y install bind-utils lrzsz &> /dev/null
echo "=================================================="
echo "Install Development tools" >> $LOG
echo "==================================================" >> $LOG
format

##########################################################################
# Yum update bash and openssl
echo "Update bash and openssl"
yum -y update bash &> /dev/null
yum -y update openssl &> /dev/null
yum -y update glibc &> /dev/null
echo "=================================================="
echo "Update bash and openssl" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set ssh
echo "Disabled EmptyPassword."
echo "Disabled SSH-DNS."
echo "Set timeout is 10m."
sed -i "s/^#PermitEmptyPasswords/PermitEmptyPasswords/" /etc/ssh/sshd_config
sed -i "s/^#LoginGraceTime 2m/LoginGraceTime 10m/" /etc/ssh/sshd_config
echo "UseDNS no" >> /etc/ssh/sshd_config 
echo "=================================================="
echo "Disabled EmptyPassword." >> $LOG
echo "Disabled SSH-DNS." >> $LOG
echo "Set timeout is 10m." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set default init 3
echo "Default init 3."
sed -i 's/^id:5:initdefault:/id:3:initdefault:/' /etc/inittab
echo "=================================================="
echo "Default init 3." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Stop Service
echo "Some services are turned off now."
for SER in rpcbind postfix portreserve certmonger mdmonitor blk-availability lvm2-monitor udev-post cups dhcpd firstboot gpm haldaemon hidd ip6tables ipsec isdn kudzu lpd mcstrans messagebus microcode_ctl netfs nfs nfslock nscd acpid anacron apmd atd auditd autofs avahi-daemon avahi-dnsconfd bluetooth cpuspeed pcscd portmap readahead_early restorecond rpcgssd rpcidmapd rstatd sendmail setroubleshoot snmpd sysstat xfs xinetd yppasswdd ypserv yum-updatesd
 do
    /sbin/chkconfig --list $SER &> /dev/null
  if [ $? -eq 0 ]
    then
      chkconfig --level 35  $SER off
    echo "$SER" >> $LOG
  fi
 done
echo "=================================================="
echo "Some services are turned off now:" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Del unnecessary users
echo "Del unnecessary users."
for USERS in adm lp sync shutdown halt mail news uucp operator games gopher
 do
  grep $USERS /etc/passwd &>/dev/null
  if [ $? -eq 0 ]
   then
    userdel $USERS &> /dev/null
    echo $USERS >> $LOG
  fi
 done
echo "=================================================="
echo "Del unnecessary users." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Del unnecessary groups
echo "Del unnecessary groups."
for GRP in adm lp mail news uucp games gopher mailnull floppy dip pppusers popusers slipusers daemon
 do
  grep $GRP /etc/group &> /dev/null
  if [ $? -eq 0 ]
   then
    groupdel $GRP &> /dev/null
    echo $GRP >> $LOG
  fi
 done
echo "=================================================="
echo "Del unnecessary groups." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Disabled reboot by keys ctlaltdelete
echo "Disabled reboot by keys ctlaltdelete"
sed -i 's/^exec/#exec/' /etc/init/control-alt-delete.conf
echo "=================================================="
echo "Disabled reboot by keys ctlaltdelete" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set ulimit
echo "Set ulimit 1000000"
echo "*    soft    nofile  1000000" >> /etc/security/limits.conf
echo "*    hard    nofile  1000000" >> /etc/security/limits.conf
echo "*    soft    nproc 102400" >> /etc/security/limits.conf
echo "*    hard    nproc 102400" >> /etc/security/limits.conf
sed -i 's/1024/1000000/' /etc/security/limits.d/90-nproc.conf
echo "=================================================="
echo "Set ulimit 1000000" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set login message
echo "Set login message."
echo "This is not a public Server" > /etc/issue
echo "This is not a public Server" > /etc/redhat-release
echo "=================================================="
echo "Set login message." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Record SUID and SGID files
echo "Record SUID and SGID files."
echo "SUID --- " > /var/log/SuSg_"$DATE2".log
find / -path '/proc'  -prune -o -perm -4000 >> /var/log/SuSg_"$DATE2".log
echo "------------------------------------------------------ " >> /var/log/SuSg_"$DATE2".log
echo "SGID --- " >> /var/log/SuSg_"$DATE2".log
find / -path '/proc'  -prune -o -perm -2000 >> /var/log/SuSg_"$DATE2".log
echo "=================================================="
echo "Record SUID and SGID." >> $LOG
echo "Record is in /var/log/SuSg_"$DATE2".log" >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Disabled crontab send mail
echo "Disable crontab send mail."
sed -i 's/^MAILTO=root/MAILTO=""/' /etc/crontab 
sed -i 's/^mail\.\*/mail\.err/' /etc/rsyslog.conf
echo "=================================================="
echo "Disable crontab send mail." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set ntp client
echo "Set ntp client."
SED() {
    cp -p /etc/ntp.conf /etc/ntp.conf.bak
    sed -i '/^server/d' /etc/ntp.conf
    sed -i '/^includefile/ i\server 0.centos.pool.ntp.org iburst' /etc/ntp.conf
    sed -i '/0.centos.pool.ntp.org/ a\server 1.centos.pool.ntp.org iburst' /etc/ntp.conf
    sed -i '/1.centos.pool.ntp.org/ a\server 2.centos.pool.ntp.org iburst' /etc/ntp.conf
    sed -i '/2.centos.pool.ntp.org/ a\server 3.centos.pool.ntp.org iburst' /etc/ntp.conf
    chkconfig --level 35 ntpd on &> /dev/null
    echo "=================================================="
}
rpm -q ntp &> /dev/null
if [ $? -eq 0 ]
  then
    SED
  else
   yum -y install ntp &> /dev/null
   SED
fi
echo "Set ntp client." >> $LOG
echo "==================================================" >> $LOG
format

###########################################################################
# Set sysctl.conf
echo "Set sysctl.conf"
echo "net.core.somaxconn = 2048" >> /etc/sysctl.conf
echo "net.core.rmem_default = 262144" >> /etc/sysctl.conf
echo "net.core.wmem_default = 262144" >> /etc/sysctl.conf
echo "net.core.rmem_max = 16777216" >> /etc/sysctl.conf
echo "net.core.wmem_max = 16777216" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem = 4096 4096 16777216" >> /etc/sysctl.conf
echo "net.ipv4.tcp_wmem = 4096 4096 16777216" >> /etc/sysctl.conf
echo "net.ipv4.tcp_mem = 786432 2097152 3145728" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 16384" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 20000" >> /etc/sysctl.conf
echo "net.ipv4.tcp_fin_timeout = 15" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse = 1" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_recycle = 1" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_orphans = 131072" >> /etc/sysctl.conf
echo "net.ipv4.ip_local_port_range = 1024 65535" >> /etc/sysctl.conf
echo "Set sysctl.conf ---- " >> $LOG
/sbin/sysctl  -p >> $LOG
echo "==================================================" >> $LOG
format
###########################################################################
# Done
echo "Finished,You can check infomations in $LOG ."
echo "System will reboot in 60s."
shutdown -r 1
