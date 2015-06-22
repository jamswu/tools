#/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime,sys
from sys import argv
try:
    script,filename=argv
except ValueError:
    print "Usage: %s <filename>" % argv[0]
    sys.exit()
except IOError,e:
    print "sorry,%s" % repr(e)
    
now=datetime.datetime.now()
datenow=now.strftime('%Y%m%d_%H')
try:
    with open(filename) as file1:
        with open('%s.csv' % datenow,'wb') as file2:
            for eachline in file1:
                s=list(eachline.split()[3])
                b=eachline.split()
                b.extend(s)
                file2.write(','.join(b)+"\r\n")
except IOError,e:
    print "sorry,%s" % repr(e[1])


