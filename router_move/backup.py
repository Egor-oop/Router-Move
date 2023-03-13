import os

try:
    os.system('/usr/bin/python3 /home/python/router_move/backup_mikrotik.py')
except soket.gaierror:
    print('unknown ip')
else:
    print('unknown ip')
os.system('/usr/bin/python3 /home/python/router_move/backup_eltex.py')
os.system('/usr/bin/python3 /home/python/router_move/backup_cisco.py')
