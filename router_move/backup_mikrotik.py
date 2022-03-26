import libapi
import ftplib
import pymysql.cursors
import os
import datetime

connection = pymysql.connect(host='192.168.168.5',
                             user='admin',
                             password='parallaxtal',
                             database='RouterMove',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cur:
    cur.execute('''SELECT * FROM devices WHERE device_type = "mikrotik"''')
    results = cur.fetchall()
    devices = []
    for result in results:
        devices.append(result)


for device in devices:
    print("Connect to {}:".format(device['ip']))

    #Создание сокета и объекта устройства
    try:
    	s = libapi.socketOpen(device['ip'])
    except Exception as e:
        continue
    dev_api = libapi.ApiRos(s)

    #Авторизация на устройстве
    try:
        if not dev_api.login(device['user_name'], device['users_passwd']):
            break
    except Exception as e:
        continue

    command = ["/export", f"=file={device['name']}_backup"]

    #Выполнение команды на устройстве
    dev_api.writeSentence(command)

    #Получение результата выполнения команды
    res = libapi.readResponse(dev_api)

    #Закрытие сокета
    libapi.socketClose(s)

day = str(datetime.date.today())

path = f'/home/backup/{day}/mikrotik'

if not os.path.isdir(path):
     os.makedirs(path)

os.chdir(path)

filename_pattern = '{}_backup.rsc'

for device in devices:
    print("Connect to {}:".format(device['ip']))

    filename = filename_pattern.format(device['name'])
    try:
    	with ftplib.FTP(device['ip'], device['user_name'], device['users_passwd']) as con:
            with open(filename, "wb") as f:
                con.retrbinary('RETR ' + filename, f.write)
            print("    File transfer: done")
    except Exception as e:
        continue

for device in devices:
    print("Connect to {}:".format(device['ip']))

    #Создание сокета и объекта устройства
    try:
    	s = libapi.socketOpen(device['ip'])
    except Exception as e:
        continue
    dev_api = libapi.ApiRos(s)

    #Авторизация на устройстве
    try:
        if not dev_api.login(device['user_name'], device['users_passwd']):
            break
    except Exception as e:
        continue

    #Команда для добавление bridge-интерфейса
    command = ["/file/remove", f"=numbers={device['name']}_backup"]

    #Выполнение команды на устройстве
    dev_api.writeSentence(command)

    #Получение результата выполнения команды
    res = libapi.readResponse(dev_api)

    #Закрытие сокета
    libapi.socketClose(s)
