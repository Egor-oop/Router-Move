from flask import Flask, render_template, request, redirect
import pymysql.cursors
import libapi
import ftplib
import os
from crontab import CronTab

connection = pymysql.connect(host='192.168.168.5',
                             user='admin',
                             password='parallaxtal',
                             database='RouterMove',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
@app.route('/devices', methods=['POST', 'GET'])
def index():
    with connection.cursor() as cur:
        cur.execute('''SELECT * FROM devices''')
        results = cur.fetchall()
        devices = []
        for result in results:
            devices.append(result)

        if request.method == 'POST':
            sql = ("DELETE FROM devices WHERE name = %s")
            cur.execute(sql, (request.form.get('name')))

    context = {'devices': devices}
    connection.commit()
    return render_template('devices.html', **context)

@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    if request.method == 'POST':
        with connection.cursor() as cur:
            login = cur.execute("SELECT name FROM users;")
            passwd = cur.execute("SELECT passwd FROM users;")

            if request.form.get('login') == login:
                if request.form.get('passwd') == passwd:
                    redirect('/devices')
    return render_template('authorization.html')

@app.route('/devices/newdevice', methods=['POST', 'GET'])
def new_device():
    if request.method == 'POST':
        with connection.cursor() as cur:
            sql = ("INSERT INTO devices (name, ip, user_name, users_passwd, device_type) VALUES (%s, %s, %s, %s, %s)")
            cur.execute(sql, (request.form.get('name'), request.form.get('ip'), request.form.get('user'), request.form.get('passwd'), request.form.get('device-type')))
    return render_template('newdevice.html')

@app.route('/backup', methods=['POST', 'GET'])
def backups():
    with connection.cursor() as cur:
        cur.execute('''SELECT * FROM devices''')
        results = cur.fetchall()
        devices = []
        for result in results:
            devices.append(result)

    if request.method == 'POST':
        os.system('/usr/bin/python3 /home/python/router_move/backup.py')

    return render_template('backup.html')

@app.route('/backup/settings', methods=['POST', 'GET'])
def backupsettings():
    if request.method == 'POST':
        weekdays_list = request.form.getlist('weekday')

        my_cron = CronTab(user='root')

        for job in my_cron:
            if job.comment == 'startbackup':
                my_cron.remove(job)

        job = my_cron.new(command='/usr/bin/python3 /home/python/router_move/backup.py', comment='startbackup')
        
        if request.form.get('day') != 'star':
            job.day.on(request.form.get('day'))
        if request.form.get('hours') != 'star':
            job.hour.on(request.form.get('hours'))
        if request.form.get('minute') != 'star':
            job.minute.on(request.form.get('minute'))
        '''
        job.day.on(request.form.get('day'))
        job.hour.on(request.form.get('hours'))
        job.minute.on(request.form.get('minute'))
        '''
        job.dow.on(*weekdays_list)
        
        my_cron.write()

    return render_template('backupsettings.html')

@app.route('/statistic')
def statistic():
    with connection.cursor() as cur:
        cur.execute('''SELECT * FROM statistic''')
        results = cur.fetchall()
        statistic_list = []
        for result in results:
            statistic_list.append(result)

    context = {'destatistic': statistic_list}
    connection.commit()
    return render_template('statistic.html', **context)

if __name__ == '__main__':
    app.run('192.168.168.5')
