import socket
from .backup_mikrotik import backup_mikrotik
from .backup_eltex import backup_eltex
from .backup_cisco import backup_cisco


def run_backup(directory: str) -> None:
    try:
        backup_mikrotik(directory)
        backup_eltex(directory)
        backup_cisco(directory)
    except socket.gaierror:
        print('unknown ip')


if __name__ == '__main__':
    run_backup('/Users/egorgulido/Desktop')
