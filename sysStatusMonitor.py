# -*- coding: UTF8 -*-

# Author: Shane
# CreteTime: 2014-3-13
# Mail: ngy01112003@163.com
# Version: 1.0

"""
 This Script provide the statics of system.
 Inclue Cpu, Memory, Disk, Nic etc.
 Based on the Windows xp sp3, python 2.7.6, psutil 1.2.1.
"""

import sys
import os
import datetime
import psutil
#from psutil._compat import print 

#字节转换
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


###监控CPU使用率###
def getCpuPer():
    
    #获取CPU使用率
    perCPU = psutil.cpu_percent(interval=1)
    print "CPU Usage：", int(perCPU), "%"

###监控内存###
def getMemStatus():
    
    #获取内存状态
    phymem = psutil.phymem_usage()  
    buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()  
    cached = getattr(psutil, 'cached_phymem', lambda: 0)()  
    used = phymem.total - (phymem.free + buffers + cached)  
    line = "Memory Usage: %5s%%    Used:%s    Total:%s" % (  
        phymem.percent,  
        str(int(used / 1024 / 1024)) + "M",  
        str(int(phymem.total / 1024 / 1024)) + "M"  
    ) 
    print (line)

###监控磁盘信息###
def getPartitionStatus():
    
    #获取磁盘分区信息
    pars = psutil.disk_partitions()
    #print ""
    print "\nDisk Partition Status:"
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"       #定义打印格式
    print (templ % ("Partition", "Total", "Used", "Free", "Use", "Type",
                    "Mount"))                       #打印表头

    for par in pars:
        if os.name == "nt":
            if "cdrom" in par.opts or par.fstype == '':
                continue

        disk = psutil.disk_usage(par.mountpoint)
        print (templ % (                            #打印具体的信息
            par.device,
            bytes2human(disk.total),
            bytes2human(disk.used),
            bytes2human(disk.free),
            int(disk.percent),
            par.fstype,
            par.mountpoint))

    #获取磁盘IO信息
    diskIo = psutil.disk_io_counters()
    print "\nDisk IO Status:"
    templ = "%-7s %12s %12s %12s %12s %12s"       #定义打印格式
    print (templ % ("Read_Count", "Wriet_Count", "Read_Bytes",
                    "Write_Bytes", "Read_Time", "Write_Time")) 
    print (templ % (diskIo.read_count,
                    diskIo.write_count,
                    bytes2human(diskIo.read_bytes),
                    bytes2human(diskIo.write_bytes),
                    int(diskIo.read_time/1000),
                    int(diskIo.write_time/1000)))

###获取网卡状态###
def getNicStatus():
    
    nics = psutil.net_io_counters(pernic=True)
    nicKeys = nics.keys()
    
    print "\nNIC IO Status:"
    templ = "%-30s %12s %17s %17s %17s %12s %12s  %9s %9s"       #定义打印格式
    print (templ % ("Nic Name","Bytes_Sent", "Bytes_Recv", "Packets_Sent", "Packets_Recv",
                    "ErrorIn", "ErrorOut","DropIn","DropOut"))
    
    for name in nicKeys:
        nicStatus = nics[name]
        print (templ % (name,
                        bytes2human(nicStatus.bytes_sent),
                        bytes2human(nicStatus.bytes_recv),
                        str(nicStatus.packets_sent),
                        nicStatus.packets_recv,
                        nicStatus.errin,
                        nicStatus.errout,
                        nicStatus.dropin,
                        nicStatus.dropout))

###主函数入口###
def main():
#    getLoginUser()
    getCpuPer()
#    getMemStatus()
    getPartitionStatus()
 #   getNicStatus()

#入口
if __name__ == "__main__":
    sys.exit(main())
