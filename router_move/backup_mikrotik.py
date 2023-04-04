import libapi
from fetch_devices import fetch_devices
import ftplib
import os
import datetime
import secrets


def backup_mikrotik(directory: str) -> None:
    devices = fetch_devices('mikrotik')

    day = str(datetime.date.today())

    path = f'{directory}/{day}/mikrotik'

    if not os.path.isdir(path):
        os.makedirs(path)

    for device in devices:
        print("Connect to {}:".format(device[2]))
        filename = f'{device[1]}_backup.rsc'

        # Создание сокета и объекта устройства
        try:
            s = libapi.socketOpen(device[2])
        except Exception as e:
            continue
        dev_api = libapi.ApiRos(s)

        # Авторизация на устройстве
        try:
            if not dev_api.login(device[3], device[4]):
                break
        except Exception as e:
            continue

        command = ['/export', f'=file={filename}', '=show-sensitive', '=terse']

        # Выполнение команды на устройстве
        dev_api.writeSentence(command)

        # Получение результата выполнения команды
        res = libapi.readResponse(dev_api)

        # Закрытие сокета
        libapi.socketClose(s)

    filename_pattern = '{}_backup.rsc'
    for device in devices:
        print("Connect to {}:".format(device[2]))
        filename = filename_pattern.format(device[1])

        try:
            with ftplib.FTP(device[2], device[3], device[4]) as con:
                if os.path.isfile(f'{path}/{filename}'):
                    filename = f'{device[1]}_{secrets.token_urlsafe(6)}_backup.rsc'
                with open(f'{path}/{filename}', "wb") as f:
                    con.retrbinary('RETR ' + filename_pattern.format(device[1]), f.write)
                print("    File transfer: done")
        except Exception as e:
            continue

    for device in devices:
        print("Connect to {}:".format(device[2],))

        # Создание сокета и объекта устройства
        try:
            s = libapi.socketOpen(device[2],)
        except Exception as e:
            continue
        dev_api = libapi.ApiRos(s)

        # Авторизация на устройстве
        try:
            if not dev_api.login(device[3], device[4]):
                break
        except Exception as e:
            continue

        # Команда для добавление bridge-интерфейса
        command = ["/file/remove", f"=numbers={device[1]}_backup"]

        # Выполнение команды на устройстве
        dev_api.writeSentence(command)

        # Получение результата выполнения команды
        res = libapi.readResponse(dev_api)

        # Закрытие сокета
        libapi.socketClose(s)


if __name__ == '__main__':
    backup_mikrotik('/Users/egorgulido/Desktop')
