import socket
from router_move.backup_mikrotik import backup_mikrotik
from router_move.backup_eltex import backup_eltex
from router_move.backup_cisco import backup_cisco
import sys


def run_backup(directory: str) -> None:
    paths = sys.path
    try:
        backup_mikrotik(directory)
        backup_eltex(directory)
        backup_cisco(directory)
    except socket.gaierror:
        print('unknown ip')


if __name__ == '__main__':
    run_backup('/Users/egorgulido/Desktop')
