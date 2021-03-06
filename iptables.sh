#!/bin/bash
iptables -F
iptables -X
iptables -F -t nat
iptables -X -t nat
iptables -Z -t nat
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#共享上网
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

iptables -A INPUT -p tcp  --dport 9200 -j ACCEPT
iptables -A OUTPUT -p tcp  --sport 9200 -j ACCEPT
#允许本机访问本机
iptables -A INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT
#开放端口
for port in 80 8080 8081 139 445 6001 9000 21 5503 389 636:
    do
        iptables -A INPUT -p tcp --dport $port -j ACCEPT
        iptables -A OUTPUT -p tcp --sport $port -j ACCEPT
    done

#屏蔽单个IP的命令是
#iptables -I INPUT -s 123.45.6.7 -j DROP
#封整个段即从123.0.0.1到123.255.255.254的命令
#iptables -I INPUT -s 123.0.0.0/8 -j DROP
##封IP段即从123.45.0.1到123.45.255.254的命令
#iptables -I INPUT -s 124.45.0.0/16 -j DROP
#封IP段即从123.45.6.1到123.45.6.254的命令是
#iptables -I INPUT -s 123.45.6.0/24 -j DROP
#端口转发
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 80 -j DNAT --to-destination  10.0.0.6:80
#iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 8080 -j DNAT --to-destination  10.0.0.5:80
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 8000 -j DNAT --to-destination  10.0.0.6:8000
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1022 -j DNAT --to-destination  10.0.0.2:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1023 -j DNAT --to-destination  10.0.0.3:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1024 -j DNAT --to-destination  10.0.0.4:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1025 -j DNAT --to-destination  10.0.0.5:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1026 -j DNAT --to-destination  10.0.0.6:22
iptables -t nat -A POSTROUTING -d 10.0.0.6 -p tcp --dport 22 -j SNAT --to-source 10.0.0.1
iptables -t nat -A POSTROUTING -d 10.0.0.6 -p tcp --dport 80 -j SNAT --to-source 10.0.0.1
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1027 -j DNAT --to-destination  54.241.15.17:22
#iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 8080 -j DNAT --to-destination  10.0.0.3:80
#iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 8088 -j DNAT --to-destination  10.0.0.3:80
#iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 80 -j DNAT --to-destination  10.0.0.5:80
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 3306 -j DNAT --to-destination  10.0.0.2:3306
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 389 -j DNAT --to-destination  10.0.0.5:389
#ftp 被动模式
iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 5000:5010 -j ACCEPT  
iptables -A OUTPUT -p tcp -m state --state NEW -m tcp --dport 5000:5010 -j ACCEPT  

#芝麻开门
#记录日志，前缀SSHOPEN:<br />
iptables -A INPUT -p icmp --icmp-type 8 -m length --length 2028 -j LOG --log-prefix "SSHOPEN:"
iptables -A OUTPUT -p icmp --icmp-type 8 -m length --length 2028 -j LOG --log-prefix "SSHOPEN:"
#指定数据包78字节，包含IP头部20字节，ICMP头部8字节。<br />
iptables -A INPUT -p icmp --icmp-type 8 -m length --length 2028 -m recent --set --name sshopen --rsource -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type 8 -m length --length 2028 -m recent --set --name sshopen --rsource -j ACCEPT
iptables -A INPUT -p tcp --dport 22 --syn -m recent --rcheck --seconds 15 --name sshopen --rsource -j ACCEPT
iptables -A OUTPUT -p tcp --dport 22 --syn -m recent --rcheck --seconds 15 --name sshopen --rsource -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
####################################
version=`head -n 1 /etc/issue|awk '{print $1}'|tr '[A-Z]' '[a-z]'`
if [ "$version" = "ubuntu" ];then
    /etc/init.d/iptables-persistent save
    /etc/init.d/iptables-persistent restart
elif [ "$version" = "centos" ];then  
    /etc/init.d/iptables save
    /etc/init.d/iptables restart
fi
