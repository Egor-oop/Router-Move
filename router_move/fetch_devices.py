import sqlite3
import os


def fetch_devices(device_type: str) -> list:
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(f'{path}/database.db')
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM device WHERE device_type='{device_type}'")
    devices = res.fetchall()
    con.close()
    return devices
