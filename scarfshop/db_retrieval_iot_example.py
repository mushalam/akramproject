from pymongo import MongoClient
import os


def read_db():
    '''Retrieve data from the database.'''
    client = MongoClient('mongodb://192.168.0.30:24916/', username=os.environ.get('username'), password=os.environ.get('password'), authSource='admin')
    db = client.iot_sensor_data
    db_keys = ['temperature', 'humidity', 'infrared', 'light']
    db_data = {key: [] for key in
    db_keys}  # Using list comprehensions - create dictionary of db_data for keys in db_keys with values of [] (empty list)

    try:
        for key in db_keys:
            collection = db[key]
            cursor = collection.find({})
            for document in cursor:
                for i in range(0, len(db_keys)):
                    if key == db_keys[i]: db_data[db_keys[i]].append(document)
        return db_data
    except Exception as e:
        print("Encountered exception: " + str(e))


def killme():
    data = read_db()
    for i in range(0, len(data['light'])):
        xdata = data['infrared'][i]['_id']
        ydata = data['infrared'][i]['value']
        print(xdata)
        print(ydata)

# read_db()
# killme()
