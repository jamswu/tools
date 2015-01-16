#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import logging,os
class Logger:
    def __init__(self,path,dlevel="yes",console = "NO",clevel = logging.DEBUG,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        if dlevel.lower().strip() == "yes":
            fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s','%Y-%m-%d %H:%M:%S')
        else:
            fmt = logging.Formatter('%(asctime)s %(message)s','%Y-%m-%d %H:%M:%S')

        #SET console log
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        #set file log
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        if console.lower().strip() == "yes":
            self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)
    def info(self,message):
        self.logger.info(message)
    def war(self,message):
        self.logger.warn(message)
    def error(self,message):
        self.logger.error(message)
    def cri(self,message):
        self.logger.critical(message)
if __name__ == "__main__":
    log_info = Logger("log_1.txt",console="yes")
    log_info.debug("一个debug信息")
    log_info.info('一个info信息')
    log_info.war("一个warning信息")
    log_info.error("一个error信息")
    log_info.cri("一个致命critical信息")