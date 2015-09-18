#!/usr/bin/python 
#coding:utf-8 
 
 
import smtplib 
from email.mime.text import MIMEText 
import sys 
 
mail_server = "smtp.126.com" 
mail_user = 'asdfwujian' 
mail_pass = 'wj4768593'
mail_postfix = '126.com'
mail_server_port=25 
 
def send_mail(to_list,subject,content): 
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">" 
    msg = MIMEText(content) 
    msg['Subject'] = subject 
    msg['From'] = me 
    msg['to'] = to_list 
     
    try: 
        s = smtplib.SMTP() 
        s.connect(mail_server) 
        s.login(mail_user,mail_pass) 
        s.sendmail(me,to_list,msg.as_string()) 
        s.close() 
        return True 
    except Exception,e: 
        print str(e) 
        return False 
     
#if __name__ == "__main__": 
 #   send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
def send():
    subject = 'python email test'
    me="文件监控"+"<"+mail_user+"@"+mail_postfix+">"
    fo=open("360.htm","rb")
    to_list=["jams_wu@126.com"]
    cc=["asdfwujian@163.com"]
    bcc=["asdfwujian@126.com"]
    #mail_content = '<html><h1>你好</h1></html>' # email内容
    COMESPACE=','
    mail_content = fo.read() # email内容
    print type(mail_content) 
    msg=MIMEText(mail_content,'html','utf-8')
    #msg1="hello"
    msg['Subject']=subject
    msg['From']=me
    msg['to'] =COMESPACE.join(to_list)
    msg['CC'] = COMESPACE.join(cc)
    msg['Bcc']=COMESPACE.join(bcc)
    #msg=MIMEText(mail_content,'html','utf-8')
#    print type(msg)

    server=smtplib.SMTP(mail_server,mail_server_port)
    server.ehlo()
    #server.set_debuglevel(5)
    #server.starttls()
    #server.login(mail_user)
    server.sendmail(me,to_list,msg.as_string())
    server.quit()

def send1():
    subject = 'python email test'
    me="文件监控"+"<"+mail_user+"@"+mail_postfix+">"
    to_list=["jams_wu@126.com"]
    cc=["zaki@weststarinc.co"]
    #bcc=["asdfwujian@126.com"]
    mail_content = '<html><h1>你好</h1></html>' # email内容
    COMESPACE=','
    #mail_content = fo.read() # email内容
    #print type(mail_content) 
    msg=MIMEText(mail_content,'html','utf-8')
    #msg1="hello"
    msg['Subject']=subject
    msg['From']=me
    msg['to'] =COMESPACE.join(to_list)
    msg['CC'] = COMESPACE.join(cc)
    #msg['Bcc']=COMESPACE.join(bcc)
    #msg=MIMEText(mail_content,'html','utf-8')
#    print type(msg)

    server=smtplib.SMTP(mail_server,mail_server_port)
    server.ehlo()
    #server.set_debuglevel(5)
    #server.starttls()
    server.login(mail_user,mail_pass)
    server.sendmail(me,to_list,msg.as_string())
    server.quit()

send1()


