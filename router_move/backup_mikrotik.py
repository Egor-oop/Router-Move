from router_move import libapi
from router_move.fetch_devices import fetch_devices
import ftplib
import os
import datetime
import secrets
# from app import Device


def backup_mikrotik(directory: str) -> None:
    devices = fetch_devices('mikrotik')
    for device in devices:
        print("Connect to {}:".format(device.ip))
        filename = f'{device.name}_backup.rsc'

        # Создание сокета и объекта устройства
        try:
            s = libapi.socketOpen(device.ip)
        except Exception as e:
            continue
        dev_api = libapi.ApiRos(s)

        # Авторизация на устройстве
        try:
            if not dev_api.login(device.user_name, device.user_password):
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

    day = str(datetime.date.today())

    path = f'{directory}/{day}/mikrotik'

    if not os.path.isdir(path):
        os.makedirs(path)

    os.chdir(path)
    filename_pattern = '{}_backup.rsc'
    for device in devices:
        print("Connect to {}:".format(device.ip))
        filename = filename_pattern.format(device.name)

        try:
            with ftplib.FTP(device.ip, device.user_name, device.user_password) as con:
                if os.path.isfile(filename):
                    filename = f'{device.name}_{secrets.token_urlsafe(6)}_backup.rsc'
                with open(filename, "wb") as f:
                    con.retrbinary('RETR ' + filename_pattern.format(device.name), f.write)
                print("    File transfer: done")
        except Exception as e:
            continue

    for device in devices:
        print("Connect to {}:".format(device.ip))

        # Создание сокета и объекта устройства
        try:
            s = libapi.socketOpen(device.ip)
        except Exception as e:
            continue
        dev_api = libapi.ApiRos(s)

        # Авторизация на устройстве
        try:
            if not dev_api.login(device.user_name, device.user_password):
                break
        except Exception as e:
            continue

        # Команда для добавление bridge-интерфейса
        command = ["/file/remove", f"=numbers={device.name}_backup"]

        # Выполнение команды на устройстве
        dev_api.writeSentence(command)

        # Получение результата выполнения команды
        res = libapi.readResponse(dev_api)

        # Закрытие сокета
        libapi.socketClose(s)


if __name__ == '__main__':
    backup_mikrotik('/Users/egorgulido/Desktop')
