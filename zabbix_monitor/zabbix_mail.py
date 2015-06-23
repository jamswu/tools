#!/usr/bin/python 
#coding:utf-8 
# mail.py send email
# author:  zaki
# version: 1.0.0
# desc: zabbix send mail script
# date: 2015/06/27
 
import smtplib 
from email.mime.text import MIMEText 
from sys import argv,exit
try:
    script,to_list,subject,mail_content=argv
except ValueError:
    print "Usage: %s <example@126.com> <subject> <content>" % argv[0]
    exit()
mail_server = "119.9.105.149" 
mail_user = 'replmonitor' 
mail_postfix = 's8-mail.com'
mail_server_port=25     
def send():
    me="zabbix管理员"+"<"+mail_user+"@"+mail_postfix+">"
    msg=MIMEText(mail_content,'html','utf-8')
    msg['Subject']=subject
    msg['From']=me
    msg['to'] =to_list
    server=smtplib.SMTP(mail_server,mail_server_port)
    server.ehlo()
    #server.set_debuglevel(5)
    server.sendmail(me,to_list,msg.as_string())
    server.quit()
if __name__ == "__main__":
    send()


