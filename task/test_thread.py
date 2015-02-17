#!/use/bin/env python
import thread,time,random
count=0 
def threadTest():
    global count
    for i in xrange(10000):
        count+=1
def test():
    for i in range(10):
        thread.start_new_thread(threadTest,())
    time.sleep(3)
    print count
def threadFunc(a=None,b=None,c=None,d=None):
    print time.strftime('%H:%M:%S',time.localtime()),a
    time.sleep(1)
    print time.strftime('%H:%M:%S',time.localtime()),b
    time.sleep(1)
    print time.strftime('%H:%M:%S',time.localtime()),c
    time.sleep(1)
    print time.strftime('%H:%M:%S',time.localtime()),d
    time.sleep(1)
    print time.strftime('%H:%M:%S',time.localtime()),"over"
def 
thread.start_new_thread(threadFunc,(3,4,5,6))
time.sleep(5)
