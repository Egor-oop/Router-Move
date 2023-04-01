from flask import render_template, request, redirect
from router_move.models import Device, BackupDirectory
from router_move import app, db
import os

from crontab import CronTab


@app.route('/', methods=['POST', 'GET'])
@app.route('/devices', methods=['POST', 'GET'])
def index():
    devices = []
    devices_db = Device.query.all()
    for device in devices_db:
        devices.append(device)
    context = {'devices': devices}
    return render_template('devices.html', **context)


@app.route('/devices/newdevice', methods=['POST', 'GET'])
def new_device():
    if request.method == 'POST':
        device = Device(ip=request.form['ip'], name=request.form['name'], user_name=request.form['user'],
                        user_password=request.form['passwd'], device_type=request.form['device-type'])
        db.session.add(device)
        db.session.commit()
    return render_template('newdevice.html')


@app.route('/devices/<int:id_>', methods=['POST', 'GET'])
def retrieve_device(id_):
    device = Device.query.get(id_)
    if request.method == 'POST':
        d = Device.query.filter_by(id=id_).update(dict(
            name=request.form['name'],
            ip=request.form['ip'],
            user_name=request.form['user'],
            user_password=request.form['passwd']
        ))
        db.session.commit()
    context = {'device': device}
    return render_template('device.html', **context)


@app.route('/devices/<int:id_>/delete', methods=['DELETE', 'GET'])
def delete_device(id_):
    device = Device.query.filter_by(id=id_).delete()
    if not device:
        return redirect('/')
    db.session.commit()
    return redirect('/')


@app.route('/backup', methods=['POST', 'GET'])
def backups():
    try:
        directory = BackupDirectory.query.all()[-1]
    except IndexError:
        directory = BackupDirectory('')
    if request.method == 'POST':
        if request.form['directory'] != directory.path:
            directory = BackupDirectory(request.form['directory'])
            db.session.add(directory)
            db.session.commit()
        os.system(f'/usr/bin/python3 {os.path.dirname(__file__)}/backup.py')
    context = {'directory': directory.path}
    return render_template('backup.html', **context)


@app.route('/backup/settings', methods=['POST', 'GET'])
def backupsettings():
    if request.method == 'POST':
        weekdays_list = request.form.getlist('weekday')

        my_cron = CronTab(user=True)

        for job in my_cron:
            if job.comment == 'startbackup':
                my_cron.remove(job)

        job = my_cron.new(command=f'/usr/bin/python3 {os.path.dirname(__file__)}/backup.py {BackupDirectory.query.all()[-1]}', comment='startbackup')

        if request.form.get('day') != 'star':
            job.day.on(request.form.get('day'))
        if request.form.get('hours') != 'star':
            job.hour.on(request.form.get('hours'))
        if request.form.get('minute') != 'star':
            job.minute.on(request.form.get('minute'))
        job.dow.on(*weekdays_list)

        my_cron.write()

    return render_template('backupsettings.html')


@app.route('/statistic')
def statistic():
    # with connection.cursor() as cur:
    #     cur.execute('''SELECT * FROM statistic''')
    #     results = cur.fetchall()
    #     statistic_list = []
    #     for result in results:
    #         statistic_list.append(result)
    #
    # context = {'destatistic': statistic_list}
    # connection.commit()
    return render_template('statistic.html')


@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    # if request.method == 'POST':
    #     with connection.cursor() as cur:d
    #         login = cur.execute("SELECT name FROM users;")
    #         passwd = cur.execute("SELECT passwd FROM users;")
    #
    #         if request.form.get('login') == login:
    #             if request.form.get('passwd') == passwd:
    #                 redirect('/devices')
    return render_template('authorization.html')
