import socket
from .backup_mikrotik import backup_mikrotik


def run_backup(directory: str) -> None:
    try:
        backup_mikrotik(directory)
    except socket.gaierror:
        print('unknown ip')


if __name__ == '__main__':
    run_backup('/Users/egorgulido/Desktop')
