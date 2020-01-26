import threading
from pymongo import MongoClient
import os


def read_db():
    '''Retrieve data from the database.'''
    client = MongoClient('mongodb://192.168.0.30:24916/', username=os.environ.get('username'), password=os.environ.get('password'), authSource='admin')
    db = client.iot_sensor_data

    db_keys = ['temperature', 'humidity', 'infrared', 'light']
    db_data = {key: [] for key in db_keys}  # Using list comprehensions - create dictionary of db_data for keys in db_keys with values of [] (empty list)

    for key in db_keys:
        collection = db[key]
        cursor = collection.find({})
        print("cursor is:" + str(cursor))
        for document in cursor:
            print(document)
            for i in range(0, len(db_keys)):
                if key == db_keys[i]: db_data[db_keys[i]].append(document)
    print(db_data)


def insert_db(identifier, value1, value2, timestamp):
    '''Push data to the database.'''

    client = MongoClient('mongodb://192.168.0.30:24916/', username=os.environ.get('username'), password=os.environ.get('password'), authSource='admin')
    db = client.iot_sensor_data
    timestamp = timestamp.strftime("%m/%d/%Y;%H:%M:%S") #source: https://www.programiz.com/python-programming/datetime/strftime
    db_keys = ['infrared', 'temperature', 'humidity', 'light']

    if identifier == 'IR':
        collection = db[db_keys[0]] #https://stackoverflow.com/a/51567245; as my client already points to correct db endpoint, i need to select collection
        dict = {
            '_id': timestamp,
            'value': value1
        }
        collection.insert_one(dict)

    elif identifier == 'TH':
        collection = db[db_keys[1]]
        dict = {
            '_id': timestamp,
            'value': value1
        }
        collection.insert_one(dict)

        collection = db[db_keys[2]]
        dict = {
            '_id': timestamp,
            'value': value2
        }
        collection.insert_one(dict)

    elif identifier == 'LX':
        collection = db[db_keys[3]]
        dict = {
            '_id': timestamp,
            'value': value1
        }
        collection.insert_one(dict)

    client.close()
    print("Data in DB.")

    # 'data_id': 'data_id'
    # 'username': 'username'
    # 'address': 'address',


# TESTING SECTION
#read_db()
#import datetime
#now = datetime.datetime.now()
#insert_db('IR', 1, None, now)


# if __name__ == "__main__":
#     thread1 = threading.Thread(target=insert_db)
