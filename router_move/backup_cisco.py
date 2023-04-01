import secrets
import telnetlib
import datetime
import os
from fetch_devices import fetch_devices


def backup_cisco(directory: str) -> None:
    devices = fetch_devices('cisco')
    day = str(datetime.date.today())
    path = f'{directory}/{day}/cisco'
    if not os.path.isdir(path):
        os.makedirs(path)

    for device in devices:
        try:
            tn = telnetlib.Telnet(device[2])
            tn.read_until(b"ame:")
            tn.write(device[3].encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(device[4].encode("ascii") + b"\n")
            tn.write(b"terminal length 0\n")
            tn.write(b"sh run\n")
            tn.write(b"exit\n")
            output = tn.read_until(b'\nend')
            output = output.decode("ascii")
            output = output.splitlines()

            filename = f'{path}/{device[1]}_backup.rsc'
            if os.path.isfile(filename):
                filename = f'{path}/{device[1]}_{secrets.token_urlsafe(6)}_backup.rsc'

            fp = open(filename, "w")
            fp.write('\n'.join(output[5:]))
            fp.close()
        except Exception as e:
            continue
