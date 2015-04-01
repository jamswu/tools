#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
from time import sleep
from daemonize import Daemonize
pid ="test.pid"
def main():
    while True:
        sleep(5)
daemon=Daemonize(app="monitorFChange.py",pid=pid,action=main)
daemon.start()
