import os
import glob
import time
import csv
import datetime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def write_csv(write_data):
    myFile = open('readings.csv', 'a')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(write_data)
 
def record_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_data = [[time_now, temp_c, temp_f]]
        write_csv(write_data)
        return time_now, temp_c, temp_f
	
write_data = [["Timestamp","Celcius", "Farenheit"]]
write_csv(write_data)


for i in range(1000):
    print(record_temp())

	