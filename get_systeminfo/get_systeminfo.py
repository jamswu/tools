#!/usr/bin/env python
# encoding: utf-8
#Author   : zaki
#Mailto   : zaki@weststarinc.co
#Version  : 1.0
#Create   : 2015-01-28


import platform,commands

def get_platform():
    """system name"""
    return platform.platform()
def get_python_version():
    """python_version"""
    return platform.python_version()
def get_version():
    """system version"""
    return platform.version()
def get_architecture():
    '''system bit'''
    return platform.architecture()
def get_machine():
    """system mode"""
    return platform.machine()
def get_node():
    '''hostname'''
    return platform.node()
def get_processor():
    '''cpu mode'''
    return platform.processor()
def get_system():
    """system mode"""
    return platform.system()
def get_python_version():
    '''python version'''
    return platform.python_version()
def get_physical_cpu():
    """cpu physical"""
    physical=commands.getstatusoutput("lscpu|grep -w 'Socket(s)'|awk '{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        return "UNKNOW"
def get_cpu_cors():
    physical=commands.getstatusoutput("lscpu|grep -w  'Core(s)'|awk -F: '{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        physical=commands.getstatusoutput("cat /proc/cpuinfo|grep 'cores'|uniq|awk '{print $4}'")
        if physical[0] == 0 and physical[1]:
            return physical[1]
        else:
            return "UNKNOW"
def get_logical_cpu():
    physical=commands.getstatusoutput("lscpu|grep -w 'CPU(s)'|awk 'NR==1{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        return "UNKNOW"
def get_thread_cpu():
    physical=commands.getstatusoutput("lscpu|grep -w 'Thread(s)'|awk -F: '{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        physical=commands.getstatusoutput("lscpu|grep -w '每个核的线程数'|awk -F： '{print $2}'")
        if physical[0] == 0 and physical[1]:
            return physical[1]
        else:
            return "UNKNOW"
def get_detailed_cpu():
    physical=commands.getstatusoutput("cat /proc/cpuinfo|grep 'model name'|uniq|awk -F: '{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        return "UNKNOW"
def get_host_mode():
    physical=commands.getstatusoutput("lscpu|grep -w 'Hypervisor vendor'|awk -F: '{print $2}'")
    if physical[0] == 0 and physical[1]:
        return physical[1]
    else:
        physical=commands.getstatusoutput("lscpu|grep -w '超管理器厂商'|awk -F： '{print $2}'")
        if physical[0] == 0 and physical[1]:
            return physical[1]
        else:
            return "not a virtual machine"
def get_bios_vendor():
    bios_vendor=commands.getstatusoutput('dmidecode -s bios-vendor')
    if bios_vendor[0] == 0 and bios_vendor[1]:
        return bios_vendor[1]
    else:
        return "UNKNOW"
def get_system_product():
    system_product=commands.getstatusoutput("dmidecode |grep -A5 'System Information'|grep -e  'Manufacturer' -e 'Product'|awk -F: '{print $2}'")
    if system_product[0] == 0 and system_product[1]:
        return system_product[1].replace("\n","")
    else:
        return "UNKNOW"
def get_system_serial_number():
    system_serial_number=commands.getstatusoutput('dmidecode -s system-serial-number')
    if system_serial_number[0] == 0 and system_serial_number[1]:
        return system_serial_number[1]
    else:
        return "UNKNOW"
def get_BaseBoard_serial_number():
    BaseBoard_serial_number=commands.getstatusoutput("dmidecode |grep -A5 'Base Board Information'|grep 'Serial Number'|awk -F: '{print $2}'")
    if BaseBoard_serial_number[0] == 0 and BaseBoard_serial_number[1]:
        return BaseBoard_serial_number[1]
    else:
        return "UNKNOW"
def get_system_uuid():
    system_uuid=commands.getstatusoutput("dmidecode |grep -A8 'System Information'|grep -i 'uuid'|awk '{print $2}'")
    if system_uuid[0] == 0 and system_uuid[1]:
        return system_uuid[1]
    else:
        return "UNKNOW"
def get_system_memory():
    system_memory=commands.getstatusoutput("dmidecode|grep -P -A5 'Memory\s+Device'|grep Size|grep -v Range|grep [1-9]|awk '{sum+=$2} END {print sum,$3}'")
    if system_memory[0] == 0 and system_memory[1]:
        return system_memory[1]
    else:
        system_memory=commands.getstatusoutput("free -m|grep Mem|awk '{print $2)'")
        if system_memory[0] == 0 and system_memory[1]:
            return system_memory[1]
        else:
            return "UNKNOW"
def get_system_memory_maximum():
    system_memory_maximum=commands.getstatusoutput("dmidecode|grep -P 'Maximum\s+Capacity'|awk -F: '{print $2}'")
    if system_memory_maximum[0]== 0 and system_memory_maximum[1]:
        return system_memory_maximum[1]
    else:
        return "UNKNOW"
def get_memory_devices():
    memory_devices=commands.getstatusoutput("dmidecode|grep -P 'Number Of Devices'|awk -F: '{print $2}'")
    if memory_devices[0]==0 and memory_devices[1]:
        return memory_devices[1]
    else:
        memory_devices=commands.getstatusoutput('dmidecode|grep -P -A5 "Memory\s+Device"|grep Size|grep -v Range|wc -l')
        if memory_devices[0]==0 and system_devices[1]:
            return memory_devices[1]
        else:
            return "UNKNOW"
def get_memory_devices_size_speed():
    memory_devices_size=commands.getstatusoutput("dmidecode|grep -P -A5 'Memory\s+Device'|grep Size|grep -v Range|grep [0-9] |awk -F: '{print $2}'")
    memory_speed=commands.getstatusoutput("dmidecode|grep -A16 'Memory Device'|grep Speed|grep [0-9]|awk -F: '{print $2}'")
    if memory_devices_size[0]!=0 or not memory_devices_size[1]:
        mem_size="UNKNOW"
    else:
        mem_size=memory_devices_size[1]
    if memory_speed[0] !=0 or  not memory_speed[1]:
        if len(memory_devices_size[1])>0:
            s=len(memory_devices_size[1])
            mem_speed="UNKNOW\n"*s
    else:
        mem_speed=memory_speed[1]
    mem_size=tuple(mem_size.split("\n"))
    mem_speed=tuple(mem_speed.split("\n"))
    size_speed=zip(mem_size,mem_speed)
    n=0
    for i in size_speed:
        if n==0:
            print "单插槽内存大小与速率:"+"\033[30;34;1m%s\033[0m" % i[0].strip()+" "+"\033[30;34;1m %s\033[0m" % i[1].strip()
        else:
            print 21*" "+"\033[30;34;1m%s\033[0m" % i[0].strip()+" "+"\033[30;34;1m %s\033[0m" % i[1].strip()
        n=n+1

def get_memory_speed():
    memory_speed=commands.getstatusoutput('dmidecode|grep -A16 "Memory Device"|grep Speed|grep [0-9]')
    if memory_speed[0]==0 and memory_speed[1]:
        return memory_speed[1]
    else:
        return "UNKNOW"
def get_memory_mode():
    memory_mode=commands.getstatusoutput('dmidecode|grep -A11 "Memory Device"|grep -w "Type:"|uniq|cut -d: -f2')
    if memory_mode[0]==0 and memory_mode[1]:
        return memory_mode[1]
    else:
        return "UNKNOW"
def get_disk_size():
    disk_size=commands.getstatusoutput("fdisk -l|grep  Disk|grep dev|awk '{print $2,$3,$4,$5,$6}'")
    if disk_size[0] == 0 and disk_size[1]:
        s=disk_size[1].split("\n")
        if s[0]=="":
            del s[0];del s[0];del s[0]
            a=0
            for i in s:
                if a==0:
                    print 12*" "+"硬盘大小:"+"\033[30;34;1m %s\033[0m" % i.strip()
                else:
                    print 21*" "+"\033[30;34;1m%s\033[0m" % i.strip()
                a=a+1
        else:
            a=0
            for i in s:
                if a==0:
                    print 12*" "+"硬盘大小:"+"\033[30;34;1m%s\033[0m" % i.strip()
                else:
                    print 21*" "+"\033[30;34;1m%s\033[0m" % i.strip()
                a=a+1
    else:
        print 12*" "+"硬盘大小:"+"\033[30;34;1m%s\033[0m" % "UNKNOW"
def get_network_info():
    ip_info=commands.getstatusoutput("ifconfig")
    ip_list=[]
    hw_list=[]
    net_number=0
    if ip_info[0] == 0 and ip_info[1]:
        ip_info=ip_info[1].split("\n\n")
        for i in ip_info:
            ip_hw=[]
            ip_mask=[]
            ip_info_list=i.split("\n")
            for ip_info_child in ip_info_list:
                if "Link encap" in ip_info_child and "lo" not in ip_info_child:
                    ip_hw.append(ip_info_child.split()[0])
                    ip_hw.append(ip_info_child.split()[4])
                if "inet " in ip_info_child and "127.0.0.1" not in ip_info_child:
                    net_number+=1
                    Temporary=ip_info_child.split()
                    del Temporary[0]
                    for ip in Temporary:
                        ip_mask.append(ip.split(':')[1])
            if not ip_mask and ip_hw:
                ip_mask=["UNKNOW"]*3
            if ip_hw:
                ip_hw.append(ip_mask)
                ip_list.append(ip_hw)
    else:
        ip_list=[] 
    pci_info=commands.getstatusoutput("lspci |grep -i net|awk -F: '{print $3}'")
    if pci_info[0] == 0 and pci_info[1]:
        pci_info=pci_info[1].split("\n")
        if len(pci_info) < len(ip_list):
            pci_info.extend((len(ip_list)-len(pci_info))*["UNKNOW"])
        pci_number=len(pci_info)
    else:
        pci_number="UNKNOW"
        pci_info=["UNKNOW"]*len(ip_list)
    if ip_list:
        s=zip(ip_list,pci_info)
    print 12*" "+"网卡数量:""\033[30;34;1m %s\033[0m" % pci_number
    print 14*" "+"使用中:""\033[30;34;1m %s\033[0m" % net_number
    for i in s:
        print 16*" "+i[0][0]
        print 21*" "+"\033[30;34;1m %s\033[0m" % "HWaddr :"+"\033[30;34;1m %s\033[0m" % i[0][1]
        print 21*" "+"\033[30;34;1m %s\033[0m" % "ipv4   :"+"\033[30;34;1m %s\033[0m" % i[0][2][0]
        print 21*" "+"\033[30;34;1m %s\033[0m" % "Bcast  :"+"\033[30;34;1m %s\033[0m" %i[0][2][1]
        print 21*" "+"\033[30;34;1m %s\033[0m" % "Mask   :"+"\033[30;34;1m %s\033[0m" %i[0][2][2]
        print 21*" "+"\033[30;34;1m %s\033[0m" % "网卡型号:"+"\033[30;34;1m %s\033[0m" %i[1].strip()
#def get_network_info():
#    ip_info=commands.getstatusoutput("ifconfig |grep -A1 'Link encap:'|grep -w inet|awk '{ print $2,$3,$4}'|awk -F: '{print $2,$3,$4}'|awk '{print $1,$3,$5}'")
#    ip_list=[]
#    hw_list=[]
#    if ip_info[0] == 0 and ip_info[1]:
#        ip_info=ip_info[1].split("\n")
#        for index,value in enumerate(ip_info):
#            if "127.0.0.1" in value:
#                del ip_info[index]
#        for i in ip_info:
#            s=i.split()
#            ip_list.append(s)
#        ip_info=ip_list
#    else:
#        ip_info="UNKNOW\n\UNKNOW\nUNKNOW".split("\n")
#    HW_info=commands.getstatusoutput("ifconfig |grep 'Link\ encap'|awk '{print $1,$5}'")
#    if HW_info[0] == 0 and HW_info[1]:
#        HW_info=HW_info[1].split("\n")
#        for index,value in enumerate(HW_info):
#            if "lo" in value:
#                del HW_info[index]
#        for i in HW_info:
#            s=i.split()
#            hw_list.append(s)
#        HW_info=hw_list
#    else:
#        HW_info="UNKNOW\nUNKNOW".split("\n")
#    pci_info=commands.getstatusoutput("lspci |grep -i ether|awk -F: '{print $3}'")
#    if pci_info[0] == 0 and pci_info[1]:
#        pci_info=pci_info[1].split("\n")
#        pci_number=len(pci_info)
#    else:
#        pci_number="UNKNOW"
#        pci_info=["UNKNOW"]*len(HW_info)
#    s=zip(HW_info,ip_info,pci_info)
#    print 12*" "+"网卡数量:""\033[30;34;1m %s\033[0m" % pci_number
#    print 14*" "+"使用中:""\033[30;34;1m %s\033[0m" % len(ip_info)
#    for i in s:
#        print 16*" "+i[0][0]
#        print 21*" "+"\033[30;34;1m %s\033[0m" % "HWaddr:"+"\033[30;34;1m %s\033[0m" % i[0][1]
#        print 21*" "+"\033[30;34;1m %s\033[0m" % "ipv4:"+"\033[30;34;1m %s\033[0m" % i[1][0]
#        print 21*" "+"\033[30;34;1m %s\033[0m" % "Bcast:"+"\033[30;34;1m %s\033[0m" %i[1][1]
#        print 21*" "+"\033[30;34;1m %s\033[0m" % "Mask:"+"\033[30;34;1m %s\033[0m" %i[1][2]
#        print 21*" "+"\033[30;34;1m %s\033[0m" % "网卡型号:"+"\033[30;34;1m %s\033[0m" %i[2].strip()







#print "操作系统版本号:%s" % get_architecture()
def show_info ():
    print"          虚拟机厂商:"+ "\033[30;34;1m%s\033[0m" % (get_host_mode()).strip()
    print"          服务器型号:"+ "\033[30;34;1m%s\033[0m" % (get_system_product()).strip()
    print"          系统序列号:"+ "\033[30;34;1m%s\033[0m" % (get_system_serial_number()).strip()
    print"            主板厂家:"+ "\033[30;34;1m%s\033[0m" % (get_bios_vendor()).strip()
    print"          主板序列号:"+ "\033[30;34;1m%s\033[0m" % (get_BaseBoard_serial_number()).strip()    
    print"            系统UUID:"+ "\033[30;34;1m%s\033[0m" % (get_system_uuid()).strip()
    print"      系统名称及版本:"+ "\033[30;34;1m%s\033[0m" % (get_platform()).strip()
    print"      操作系统的位数:"+ "\033[30;34;1m%s\033[0m" % (get_architecture()[0]).strip()
    print"      操作系统主机名:"+ "\033[30;34;1m%s\033[0m" % (get_node()).strip()
    print"        操作系统类型:"+ "\033[30;34;1m%s\033[0m" % (get_system()).strip()
    print"        python版本号:"+ "\033[30;34;1m%s\033[0m" % (get_python_version()).strip()
    print"          处理器类型:"+ "\033[30;34;1m%s\033[0m" % (get_processor()).strip()
    print"         cpu详细信息:"+ "\033[30;34;1m%s\033[0m" % (get_detailed_cpu()).strip()
    print"         物理cpu个数:"+ "\033[30;34;1m%s\033[0m" % (get_physical_cpu()).strip()
    print"       每个cpu核心数:"+ "\033[30;34;1m%s\033[0m" % (get_cpu_cors()).strip()
    print"       每cpu超线程数:"+ "\033[30;34;1m%s\033[0m" % (get_thread_cpu()).strip()
    print"         逻辑cpu个数:"+ "\033[30;34;1m%s\033[0m" % (get_logical_cpu()).strip()
    print"        系统内存大小:"+ "\033[30;34;1m%s\033[0m" % (get_system_memory()).strip()
    print"        支持最大内存:"+ "\033[30;34;1m%s\033[0m" % (get_system_memory_maximum()).strip()
    print"        内存插槽数量:"+ "\033[30;34;1m%s\033[0m" % (get_memory_devices()).strip()
    print"            内存类型:"+ "\033[30;34;1m%s\033[0m" % (get_memory_mode()).strip()
    #print(" 单插槽内存大小与速率: \033[30;34;1m{}\033[0m".format((get_memory_devices_size()).strip()))
    get_memory_devices_size_speed()
    get_disk_size()
   # print("        内存速率: \033[30;34;1m{}\033[0m".format((get_memory_speed()).strip()))
    get_network_info()

    #print("")s
#    print("  操作系统类型:[]")
#    print()
if __name__ == '__main__':
    show_info()

