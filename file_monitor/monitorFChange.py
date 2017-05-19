#!/usr/bin/python env 
# _*_ coding:utf-8 _*_
# monitorFChange.py 
# author:  zaki
# version: 2.0.0
# desc: web page performance monitoring
# date: 2017/05/19

import os
import pyinotify,re,time,getpass
import Logger,ConfigParser,threading
import logging
from subprocess import Popen,PIPE
# logging.basicConfig(level = logging.WARNING,
#                     format = '[%(asctime)s] %(message)s',
#                     filename='.changefile.txt',
#                     datefmt = '%Y-%m-%d %H:%M:%S')
fmt=logging.Formatter('[%(asctime)s] %(message)s')
fmt.datefmt='%Y-%m-%d %H:%M:%S'
logger = logging.getLogger(".changefile.txt")
fh = logging.FileHandler(".changefile.txt")
fh.setFormatter(fmt)
logger.setLevel(logging.INFO)
logger.addHandler(fh)

if not os.path.isfile(".changefile.txt"):
    os.mknod(".changefile.txt")

class EventHandler(pyinotify.ProcessEvent,Logger.Logger):
    """Event handing Function"""
    
    #The current user
    #run_user=getpass.getuser()

    #初始化父类
    def __init__(self,path="/tmp/changefile.log",dlevel="yes",console="no"):        
        Logger.Logger.__init__(self,path,dlevel,console)
        if len(path.split("/")[-1]) >= 1:
            file_path=path.split("/")[-1]
        else:
            file_path=path.split("/")[-2]
        self.exclude_file=re.compile(".+\.changefile\.txt|.+\.swp$|.+\.swx$|.+\.swpx$|.+4913$|.+\.tmp$|.+\.viminfo$|.+~|.+%s" % file_path)
        
    def process_IN_CREATE(self,event):       
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message="Create file: %s" % os.path.join(event.path,event.name)
            htmlmessage="<span style='font-size:16px'><span style='background-color:blue;color:aliceblue'>Create file:</span> %s</span><br>" % os.path.join(event.path,event.name)
            self.info(message)
            logger.info(htmlmessage)
    def process_IN_DELETE(self,event): 
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Delete file: %s" % os.path.join(event.path,event.name)
            self.info(message)
            htmlmessage="<span style='font-size:16px'><span style='background-color:red;font-weight:bold;'>Delete file:</span> %s</span><br>" % os.path.join(event.path,event.name)
            logger.info(htmlmessage)
    def process_IN_MODIFY(self,event):
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Modify file: %s" % os.path.join(event.path,event.name)
            htmlmessage = "<span style='font-size:16px'><span style='color:brown;background-color:chartreuse;'>Modify file:</span> %s</span><br>" % os.path.join(event.path,event.name)
            self.info(message)
            logger.info(htmlmessage)
    def process_IN_MOVED_FROM(self,event):
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Moved from file: %s" % os.path.join(event.path,event.name)
            htmlmessage = "<span style='font-size:16px'><span style='background-color: #88be14;'>Moved from file:</span> %s</span><br>" % os.path.join(event.path,event.name)
            self.info(message)
            logger.info(htmlmessage)
    def process_IN_MOVED_TO(self,event):
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Moved to file: %s" % os.path.join(event.path,event.name)
            htmlmessage = "<span style='font-size:16px'><span style='background-color: #88be14;'>Moved to:</span> %s</span><br>"  % os.path.join(event.path,event.name)
            self.info(message)
            logger.info(htmlmessage)
    def process_IN_ATTRIB(self,event):
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Atter changed: %s" % os.path.join(event.path,event.name)
            htmlmessage = "<span style='font-size:16px'><span style='background-color: #5d59a6;'>Atter changed:</span> %s</span><br>"  % os.path.join(event.path,event.name)
            self.info(message)
            logger.info(htmlmessage)
def FSMonitor():
    try:
        config=ConfigParser.ConfigParser()
        with open("config/config.cfg") as cfgfile:
            config.readfp(cfgfile)
            monitor_file=config.get("config_info","monitor_file_list").split(",")
            exclude_file_path=config.get("config_info","exclude_file_list").split(",")
            log_path=config.get("config_info","log_path")
            if not os.path.exists("%s" % log_path):
                os.makedirs("%s" % base_dir)
            dis_console=config.get("config_info","dis_console")
            dis_level=config.get("config_info","dis_level")
            send_mail=config.get("mail","send_mail").strip()
            contact=config.get("mail","contact")
            subject=config.get("mail","mail_subject")
            delay_second=config.get("mail","delaysend")
            try:
                delay_second=int(delay_second)
            except:
                delay_second=60
    except OSError,e:
        print str(e)
        sys.exit()
    wm=pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY|pyinotify.IN_CREATE|pyinotify.IN_DELETE|pyinotify.IN_MOVED_FROM|pyinotify.IN_MOVED_TO|pyinotify.IN_ATTRIB
    event_handler=EventHandler(log_path,dlevel=dis_level,console=dis_console)
    notifier = pyinotify.Notifier(wm,event_handler)
    if len(exclude_file_path) >= 1: 
        excl_lst=exclude_file_path
    else:
        excl_lst=["/test"]
    excl = pyinotify.ExcludeFilter(excl_lst)
    wm.add_watch(monitor_file,mask,rec=True,exclude_filter=excl,auto_add=True)
    message="now starting monitor %s" % monitor_file
    event_handler.info(message)

    def sendmail():
        changefile=open(".changefile.txt","rb+") 
        contentfile=changefile.read()
        changefile.seek(0,0)
        changefile.truncate()
        changefile.close()
        if contentfile:
            with open (".sendmailfile.txt","wb") as sendfile:
                sendfile.write(contentfile)
            #os.system("python mail.py %s %s %s >>/tmp/send_mail.txt" % (contact,subject,contentfile))
            Popen("python mail.py '%s' '%s' '%s' >>/tmp/send_mail.txt" % (contact,subject,'.sendmailfile.txt'),stdout=PIPE,shell=True)
        else:
            event_handler.info("file not change!")
            pass
        timer_start()
    def timer_start():
        timer=threading.Timer(delay_second,sendmail)
        timer.start()
    if send_mail.lower() == "yes": 
        timer_start()
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break
if __name__ == "__main__":
    FSMonitor()
