#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#zabbixmysqllogin.py
#author: zaki
#version: 1.0.0
#desc: monitor mysql login
#date: 2015/06/30

from subprocess import Popen,PIPE
import datetime,re
import cPickle,sys
pattern_user=re.compile(r'-u.+')
pattern_host=re.compile(r'-h.+')
pattern_port=re.compile(r'-P.+\d*')
pattern_socket=re.compile(r'--socket=(.*sock)')
pattern_socket_s=re.compile(r'-S(.*sock)')
pattern_socket_port=re.compile(r'--port=(\d*)')
def Cmd(cmd=""):
    p=Popen(cmd,stdout=PIPE,shell=True)
    data=p.stdout.read()
    return data
def runoption():
    linepeople=Cmd("who")
    mysql_conn=Cmd("ps aux|grep mysql|grep -v grep|grep pts|grep -w 'S+'|grep '\-u'")
    host_name=(Cmd("hostname")).strip('\n')
    linepeople=linepeople.split('\n')
    mysql_conn=mysql_conn.split('\n')
    linepeople.remove("")
    mysql_conn.remove("")
    #print mysql_conn
    #print linepeople
    count_conn=[]
    try:
        if mysql_conn !=[] and linepeople != []:
            try:
                var_judge=cPickle.load(open("/tmp/.data.pkl","rb"))
            except (IOError,EOFError):
                var_judge=[]
                cPickle.dump(var_judge,open("/tmp/.data.pkl","wb"))
                var_judge=cPickle.load(open("/tmp/.data.pkl","rb"))
            for line in mysql_conn:
                data=line.split()
                count_conn.append(data[1])
                
                #print data[1],var_judge
                if data[1] in var_judge:                
                    continue
                var_judge.append(data[1])
                #print var_judge
                user_name=pattern_user.findall(line)[0].strip('-u').split()[0]
                db_host=pattern_host.findall(line)
                db_port=pattern_port.findall(line)
                db_socket=pattern_socket.findall(line)
                if not db_socket:
                    db_socket=pattern_socket_s.findall(line)
                if not db_host:
                    db_host="127.0.0.1"
                else:
                    db_host=db_host[0].strip('-h').split()[0]
                if not db_port and db_socket:
                    mysql_daemon=Cmd("ps aux|grep '%s'|grep -v grep|grep '\-u'" % db_socket[0])
                    #print mysql_daemon
                    if mysql_daemon:
                        db_port =pattern_socket_port.findall(mysql_daemon)
                        if not db_port:
                           db_port="3306"
                        else:
                           db_port=pattern_socket_port.findall(mysql_daemon)[0]
                elif not db_port and not db_socket:
                    db_port="3306"
                else:
                    db_port=db_port[0].strip('-P').split()[0]
                for line1 in linepeople:
                    user_line=line1.split()
                    if data[6] == user_line[1]:
                        print "login:"+user_line[0]+"在"+data[8]+"通过"+host_name+"主机的"+data[6]+"终端,利用"+user_name+"数据库用户,登陆主机为"+db_host+"上的端口为"+db_port+"的mysql服务!</br>"
            #print var_judge,count_conn
            var_judge=list(set(count_conn)&set(var_judge))                              
            #print var_judge
            cPickle.dump(var_judge,open("/tmp/.data.pkl","wb"))
        else:
            var_judge=[]
            cPickle.dump(var_judge,open("/tmp/.data.pkl","wb"))
    except IOError,e:
        print  str(e)
        sys.exit()
    except:
        pass   
runoption()    
    
 




