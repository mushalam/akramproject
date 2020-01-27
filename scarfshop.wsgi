#!/usr/bin/python
import sys
import os
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/scarfshop/scarfshop/")

os.environ['USERNAME'] = 'root'
os.environ['PASSWORD'] = 'Av136.356hP0x'
os.environ['DATABASE'] = 'webApp_DB'
os.environ['HOST'] = 'localhost'


from app import app as application
application.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343672'
