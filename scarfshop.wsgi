#!/usr/bin/python
import sys
import os
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/scarfshop/scarfshop/")

os.environ['username'] = 'useradmin'
os.environ['password'] = 'Av136.356hP0x'


os.environ['MONGO_URI_USERS'] = 'mongodb://useradmin:Av136.356hP0x@192.168.0.30:24916/iot_users'
os.environ['MONGO_URI_SENSORS'] = 'mongodb://useradmin:Av136.356hP0x@192.168.0.30:24916/iot_sensor_data'


from scarfshop.app import app as application
application.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343672'
