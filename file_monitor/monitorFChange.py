#!/usr/bin/python env 
# _*_ coding:utf-8 _*_

import os
import pyinotify,re,time,getpass
import Logger,ConfigParser
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
        self.exclude_file=re.compile(".+\.swp$|.+\.swx$|.+\.swpx$|.+4913$|.+\.tmp$|.+\.viminfo$|.+~|.+%s" % file_path)
        
    def process_IN_CREATE(self,event):       
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message="Create file: %s" % os.path.join(event.path,event.name)
            self.info(message)

    def process_IN_DELETE(self,event): 
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "Delete file: %s" % os.path.join(event.path,event.name)
            self.info(message)
    
    def process_IN_MODIFY(self,event):
        if not self.exclude_file.match(os.path.join(event.path,event.name)):
            message = "modify file: %s" % os.path.join(event.path,event.name)
            self.info(message)
def FSMonitor():
    try:
        config=ConfigParser.ConfigParser()
        with open("config/config.cfg") as cfgfile:
            config.readfp(cfgfile)
            monitor_file=config.get("config_info","monitor_file_list").split(",")
            exclude_file=config.get("config_info","exclude_file_list").split(",")
            log_path=config.get("config_info","log_path")
            dis_console=config.get("config_info","dis_console")
            dis_level=config.get("config_info","dis_level")
    except OSError,e:
        print str(e)
        sys.exit()
    wm=pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY |pyinotify.IN_CREATE|pyinotify.IN_DELETE
    event_handler=EventHandler(log_path,dlevel=dis_level,console=dis_console)
    notifier = pyinotify.Notifier(wm,event_handler)
    if len(exclude_file) > 1: 
        excl_lst=exclude_file
    else:
        excl_lst=["/test"]
    excl = pyinotify.ExcludeFilter(excl_lst)
    wm.add_watch(monitor_file,mask,rec=True,exclude_filter=excl)
    message="now starting monitor %s" % monitor_file
    event_handler.info(message) 
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
