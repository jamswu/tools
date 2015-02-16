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
iptables -A OUTPUT -p tcp  --dport 9200 -j ACCEPT
#允许本机访问本机
iptables -A INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT

iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT

iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 8080 -j ACCEPT

iptables -A INPUT -p tcp --dport 8081 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 8081 -j ACCEPT

iptables -A INPUT -p tcp --dport 139 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 139 -j ACCEPT
#vncserver
iptables -A INPUT -p tcp --dport 445 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 445 -j ACCEPT

iptables -A INPUT -p tcp --dport 6001 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 6001 -j ACCEPT

iptables -A INPUT -p tcp --dport 9000 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 9000 -j ACCEPT

iptables -A INPUT -p tcp --sport 21 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 21 -j ACCEPT

iptables -A INPUT -p tcp --dport 21 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 21 -j ACCEPT
iptables -A INPUT -p tcp --dport 5503 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 5503 -j ACCEPT



#屏蔽单个IP的命令是

#iptables -I INPUT -s 123.45.6.7 -j DROP
#封整个段即从123.0.0.1到123.255.255.254的命令
#iptables -I INPUT -s 123.0.0.0/8 -j DROP
##封IP段即从123.45.0.1到123.45.255.254的命令
#iptables -I INPUT -s 124.45.0.0/16 -j DROP
#封IP段即从123.45.6.1到123.45.6.254的命令是
#iptables -I INPUT -s 123.45.6.0/24 -j DROP

#端口转发
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 8080 -j DNAT --to-destination  10.0.0.2:80
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1022 -j DNAT --to-destination  10.0.0.2:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1023 -j DNAT --to-destination  10.0.0.3:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1024 -j DNAT --to-destination  10.0.0.4:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 1025 -j DNAT --to-destination  10.0.0.5:22
iptables -t nat -A PREROUTING -d www.xingcai.com -p tcp --dport 80 -j DNAT --to-destination  10.0.0.3:80
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

/etc/init.d/iptables-persistent save
/etc/init.d/iptables-persistent restart

