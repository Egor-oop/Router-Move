#!/usr/bin/python

import telnetlib
import datetime
import os
import pymysql.cursors

connection = pymysql.connect(host='192.168.168.5',
                             user='admin',
                             password='parallaxtal',
                             database='RouterMove',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cur:
    cur.execute('''SELECT * FROM devices WHERE device_type = "eltex"''')
    results = cur.fetchall()
    devices = []
    for result in results:
        devices.append(result)


day = str(datetime.date.today())
path = f'/home/backup/{day}/eltex'
if not os.path.isdir(path):
     os.makedirs(path)

os.chdir(path)


now = datetime.datetime.now()

#host = "192.168.15.1"

#username = "oleg"
#password = "ovg7979celeron"
#filename_prefix = "eltex-backup"

for device in devices:
    tn = telnetlib.Telnet(device['ip'])
    tn.read_until(b"ame:")
    tn.write(device['user_name'].encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(device['users_passwd'].encode("ascii") + b"\n")
    tn.read_until(b'#')
    tn.write(b'terminal datadump\n')
    tn.read_until(b'#')
    tn.write(b"sh run\n")
    tn.write(b"exit\n")
    output=tn.read_until(b'#')
    output = output.decode("ascii")

    filename_pattern = '{}_backup.rsc'
    filename = filename_pattern.format(device['name'])

    fp=open(filename,"w")
    fp.write(output)
    fp.close()
