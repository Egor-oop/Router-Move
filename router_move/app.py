from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from crontab import CronTab

# connection = pymysql.connect(host='192.168.168.5',
#                              user='admin',
#                              password='parallaxtal',
#                              database='RouterMove',
#                              cursorclass=pymysql.cursors.DictCursor)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    user_name = db.Column(db.String(40), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(30), nullable=False)

    def __init__(self, ip, name, user_name, user_password, device_type):
        self.ip = ip
        self.name = name
        self.user_name = user_name
        self.user_password = user_password
        self.device_type = device_type

    def __repr__(self):
        return f'<Device {self.ip}>'


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
    # with connection.cursor() as cur:
    #     cur.execute('''SELECT * FROM devices''')
    #     results = cur.fetchall()
    #     devices = []
    #     for result in results:
    #         devices.append(result)
    #
    # if request.method == 'POST':
    #     os.system('/usr/bin/python3 /home/python/router_move/backup.py')

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


if __name__ == '__main__':
    app.run('localhost')
