import secrets
import telnetlib
import datetime
import os
from router_move.fetch_devices import fetch_devices


def backup_cisco(directory: str) -> None:
    devices = fetch_devices('cisco')

    day = str(datetime.date.today())
    path = f'{directory}/{day}/cisco'
    if not os.path.isdir(path):
        os.makedirs(path)

    os.chdir(path)

    for device in devices:
        try:
            tn = telnetlib.Telnet(device.ip)
            tn.read_until(b"ame:")
            tn.write(device.user_name.encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(device.user_password.encode("ascii") + b"\n")
            tn.write(b"terminal length 0\n")
            tn.write(b"sh run\n")
            tn.write(b"exit\n")
            output = tn.read_until(b'\nend')
            output = output.decode("ascii")
            output = output.splitlines()

            filename = f'{device.name}_backup.rsc'
            if os.path.isfile(filename):
                filename = f'{device.name}_{secrets.token_urlsafe(6)}_backup.rsc'

            fp = open(filename, "w")
            fp.write('\n'.join(output[5:]))
            fp.close()
        except Exception as e:
            continue
