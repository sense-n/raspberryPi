#!/usr/env/bin python2
from __future__ import print_function
import os
import glob
import time
import datetime
import requests
import json
import pickle
import threading

SERVER_IP = '192.241.239.98'
def send_data(data_in, unit, sensor_name):
    try:
        f = open(os.getcwd() + '/unique_id', 'rb+')
        unique_id = pickle.load(f)
        [print(x) for x in unique_id]
    except (EOFError, IndexError):
        f = open(os.getcwd() + '/unique_id', 'rb+')
        data_post = {'name': sensor_name}
        
        r = requests.post('http://{0}:5000/api/uniqueId'.format(SERVER_IP), json=data_post)
        print(r.text)
        if sensor_name not in unique_id:
            unique_id[sensor_name] = r.json()['uid']
        pickle.dump(unique_id, f)
        f.close()
    

    while True:
        print("{0} {1}".format(data_in(), datetime.datetime.now().ctime()))
        temp_c = data_in()
        data_post = {'uid':str(unique_id[sensor_name]), 'data' : { 'unit': unit, 'dataparams' : data_in(), 'time' : datetime.datetime.now().timestamp()*1000} } 
        send_data = requests.post('http://{0}:5000/api/updateSensor'.format(SERVER_IP), json=data_post)
        print(send_data.text)
        print(data_post)
        time.sleep(1)

class Run (threading.Thread):
	def __init__(self, data_in, unit, name_of_sensor):
	    threading.Thread.__init__(self)
	    self.data_in = data_in
	    self.unit = unit
	    self.name_of_sensor = name_of_sensor
	    self.start()
	def run(self):
	    print("Starting sensor")
	    self.loop_function()
	    
	def loop_function(self):
	    print("Starting " + self.name_of_sensor)
	    while True:
	    	send_data(self.data_in, self.unit, self.name_of_sensor)  
