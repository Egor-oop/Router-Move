import os
import datetime

day = str(datetime.date.today())

path = f'/home/backup/{day}'


if not os.path.isdir(path):
     os.mkdir(path)

os.chdir(path)
