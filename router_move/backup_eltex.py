import secrets
import telnetlib
import datetime
import os
from router_move.fetch_devices import fetch_devices


def backup_eltex(directory: str) -> None:
    devices = fetch_devices('eltex')

    day = str(datetime.date.today())
    path = f'{directory}/{day}/eltex'
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
            tn.read_until(b'#')
            tn.write(b'terminal datadump\n')
            tn.read_until(b'#')
            tn.write(b"sh run\n")
            tn.write(b"exit\n")
            output = tn.read_until(b'\nsw_')
            output = output.decode("ascii")

            output = output[:-4]
            filename = f'{device.name}_backup.rsc'
            if os.path.isfile(filename):
                filename = f'{device.name}_{secrets.token_urlsafe(6)}_backup.rsc'

            fp = open(filename, "w")
            fp.write(output)
            fp.close()
        except Exception as e:
            continue
