from numpy import save
from DB import DB
import time
import sys
import os
from utils.converter import convert
data_base = DB()
data_base.check_in.save_data(['wait'])
files = data_base.converting_data.load_data()
if files!=[]:
    save_data = files.pop()
    
else:
    data_base.check_in.save_data(['false'])
    sys.exit()
for i in files:
    convert(i, save_data)
data_base.check_in.save_data(["true"])
data_base.converting_data.save_data([])
time.sleep(5)
data_base.check_in.save_data(["wait"])
