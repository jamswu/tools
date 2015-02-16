#!/usr/bin/env python
# _*_ cond:utf-8 _*_
import commands,sys,ConfigParser
import MySQLdb,re,sys

try:
    config=ConfigParser.ConfigParser()
    with open("config/config.cfg") as cfgfile:
        config.readfp(cfgfile)
        dbhost=config.get("mysql_info","host")
        dbname=config.get("mysql_info","dbname")
        username=config.get("mysql_info","username")
        password=config.get("mysql_info","password")
        port=config.getint("mysql_info","port")
        outputdir=config.get("backmysql","outputdir")
        rows=config.getint("backmysql","rows")
        threads=config.get("backmysql","threads")
        exclude_table_re=config.get("backmysql","exclude_table_re")
        long_query_guard=config.get("backmysql","long_query_guard")
        kill_long_queries=config.getboolean("backmysql","kill_long_queries")
        snapshot_interval=config.get("backmysql","snapshot_interval")
        snapshot_interval_time=config.get("backmysql","snapshot_interval_time")
        no_locks=config.get("backmysql","no_locks")
        TIME_ZONE=config.get("backmysql","TIME_ZONE")
        verbose=config.getint("backmysql","verbose")
        lock_all_tables=config.get("backmysql","lock_all_tables")
        logfile=config.get("backmysql","logfile")
        logfile_path=config.get("backmysql","logfile_path") 
except :
    print sys.exc_info()[0],":",sys.exc_info()[1]
    sys.exit()

try:
    conn=MySQLdb.connect(host=dbhost,user=username,passwd=password,db=dbname,port=port) 
    cur=conn.cursor()
    cur.execute("show tables")
    full_value=cur.fetchall()
    full_table=[]
    for i in full_value:
        full_table.append(i[0])
    print full_table
    #exclude_table=r'^users*'
    back_table=''
    exclude_table_re=set(exclude_table_re.split(","))
    #print exclude_table_re
    #print exclude_table_re
    #a=r"%s" % exclude_table_re
    #print a 
    
    for exclude in exclude_table_re:
        back_table=''
        for table in full_table:
            if not re.findall(r"%s" % exclude,table):
                #if not re.findall(r"%s" % table,back_table):
                back_table=(table+","+back_table).strip(",")
                #print back_table
                #else:
                #   pass
            else:
                pass
        full_table=back_table.split(",")
    cur.close()
    conn.close()
    print back_table
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0],e.args[1])
    sys.exit()
commands.getstatusoutput("mydumper -B %s -u %s -p %s -P %s  -h %s -o %s -T %s -r %s -D -t %s" % (dbname,username,password,port,dbhost,outputdir,back_table,rows,threads))







