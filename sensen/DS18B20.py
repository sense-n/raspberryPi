#!/usr/env/bin python2
from __future__ import print_function
import os
import glob
import time
import datetime
import requests
import json
import pickle
import sensen.sensor

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
SERVER_IP = '172.20.10.4'
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000
        return temp_c

def main():
    sensen.sensor.send_data(read_temp, "C", "DS18B20")

if __name__ == '__main__':
    main()
