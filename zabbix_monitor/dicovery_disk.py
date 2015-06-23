#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#discover_disk.py
#author: zaki
#version:1.0.0
#desc: discover_disk
#date: 2015/06/30
from subprocess import Popen,PIPE
import json
from sys import argv,exit
try:
    if not argv[1]:
        exit()
except:
    exit()
def Cmd(cmd=""):
    data=Popen(cmd,stdout=PIPE,shell=True).communicate()[0]
    return data
def disk_discover():
    args="/bin/cat /proc/diskstats |grep -E '\ssd[a-z]\s|\sxvd[a-z]\s|\svd[a-z]\s'|awk '{print $3}'|sort|uniq 2>/dev/null"
    data=Cmd(args)
    disks=[]
    for disk in data.split('\n'):
        if disk:
            disks.append({'{#DISK_NAME}':disk})
    #print json.dumps({'date':disks},indent=4,separators=(',',':'))
    print json.dumps({'data':disks},skipkeys=True)
def disk_iostart(disk=""):
    iostat=Cmd("/usr/bin/iostat -dxkt 1 2 %s |/usr/bin/tail -n3" % disk).split('\n')
    if iostat and iostat[0] != '':
        data=dict(zip(iostat[0].split(),iostat[1].split()))
        print float(data[argv[2]])
    else:
        pass
if __name__ == '__main__':
    try:    
        if argv[1] == "disk_cover":
            disk_discover()
        else:
            disk_iostart(argv[1])
    except:
        exit()

