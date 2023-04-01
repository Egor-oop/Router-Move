import secrets
import telnetlib
import datetime
import os
from fetch_devices import fetch_devices


def backup_eltex(directory: str) -> None:
    devices = fetch_devices('eltex')
    day = str(datetime.date.today())
    path = f'{directory}/{day}/eltex'
    if not os.path.isdir(path):
        os.makedirs(path)

    for device in devices:
        try:
            tn = telnetlib.Telnet(device[2])
            tn.read_until(b"ame:")
            tn.write(device[3].encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(device[4].encode("ascii") + b"\n")
            tn.read_until(b'#')
            tn.write(b'terminal datadump\n')
            tn.read_until(b'#')
            tn.write(b"sh run\n")
            tn.write(b"exit\n")
            output = tn.read_until(b'\nsw_')
            output = output.decode("ascii")

            output = output[:-4]
            filename = f'{path}/{device[1]}_backup.rsc'
            if os.path.isfile(filename):
                filename = f'{path}/{device[1]}_{secrets.token_urlsafe(6)}_backup.rsc'

            fp = open(filename, "w")
            fp.write(output)
            fp.close()
        except Exception as e:
            continue
