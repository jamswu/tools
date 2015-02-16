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
        snapshot_interval_time=config.getint("backmysql","snapshot_interval_time")
        no_locks=config.get("backmysql","no_locks")
        verbose=config.getint("backmysql","verbose")
        lock_all_tables=config.get("backmysql","lock_all_tables")
        logfile=config.get("backmysql","logfile")
        logfile_path=config.get("backmysql","logfile_path") 
except :
    print sys.exc_info()[0],":",sys.exc_info()[1]
    sys.exit()
if kill_long_queries == "True":
    kill_long_queries="--kill-long-queries"
else:
    kill_long_queries=""
if snapshot_interval=="True":
    snapshot_interval="--snapshot-interval "+repr(snapshot_interval_time)
else:
    snapshot_interval=""
if no_locks == "True":
    no_locks="--no-locks "
else:
    no_locks=""
if lock_all_tables == "True":
    lock_all_tables="--lock-all-tables"
else:
    lock_all_tables=""
if logfile == "True":
    logfile="-L "+logfile_path
else:
    logfile=""
if verbose != 0 or 1 or 2 or 3:
    verbose="--verbose "+repr(verbose)
else:
    print "verbose must 0,1,2,3"
    sys.exit()



try:
    conn=MySQLdb.connect(host=dbhost,user=username,passwd=password,db=dbname,port=port) 
    cur=conn.cursor()
    cur.execute("show tables")
    full_value=cur.fetchall()
    full_table=[]
    for i in full_value:
        full_table.append(i[0])
    back_table=''
    exclude_table_re=set(exclude_table_re.split(","))
    
    for exclude in exclude_table_re:
        back_table=''
        for table in full_table:
            if not re.findall(r"%s" % exclude,table):
                back_table=(table+","+back_table).strip(",")
            else:
                pass
        full_table=back_table.split(",")
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0],e.args[1])
    sys.exit()
print "mydumper -B %s -u %s -p %s -P %s  -h %s -o %s -T %s -r %s -D -t %s %s %s %s %s %s %s" % (dbname,username,password,port,dbhost,outputdir,back_table,rows,threads,kill_long_queries,snapshot_interval,no_locks,lock_all_tables,verbose,logfile)