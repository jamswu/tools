#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime,os
now=datetime.datetime.now()
datenow=now.strftime('%Y%m%d_%H')
sourcefilename='123.csv'
listuser=[]
listuser_id=[]
username=[]
with open(sourcefilename) as file4:
    for eachline in file4:
        username.append("'%s'" % eachline.split(",")[1])
user_name=",".join(username)
os.system('mysql  -uhengcaimysql  -pK2OFEWinzrBC5IrpmO5S8mqW24yE0x4D  -h  10.1.0.20 passport -e "select username,userid from users where username in( %s );">user_id.xls' % user_name)
with open('user_id.xls') as file1:
    for eachline in file1:
        listuser.append(eachline.split())

with open (sourcefilename) as file2:
    for eachline in file2:
        record= eachline.split(',')
        for i in listuser:
            if record[1] == i[0]:
                record.insert(2,i[1])
                listuser_id.append(record)
with open ('%s_user_id.csv' % datenow,'wb') as file3:
    for i in listuser_id:
        file3.write(','.join(i))
os.remove(sourcefilename)
os.remove("user_id.xls")



