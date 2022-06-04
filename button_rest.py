from __future__ import nested_scopes
from flask import Flask, request, make_response
from flask_cors import cross_origin

import os.path
import datetime
import urllib 

from pymongo import MongoClient

# APP configurations
app= Flask(__name__)


ALTAS_USERNAME = urllib.parse.quote_plus("kaili")
ALTAS_PASSWORD = urllib.parse.quote_plus("P@ssw0rd")
ALTAS_HOST = 'cluster0.geaah.mongodb.net'
ALTAS_DATABASE = 'pcs'
ALTAS_COLLECTION = 'test'

NCHC_USERNAME = urllib.parse.quote_plus("08050cc6-73fb-4d20-b60a-484c3241a812")
NCHC_PASSWORD = urllib.parse.quote_plus("JE0fQbzONJAAwdCxmM9BIabK")
NCHC_HOST = '203.145.215.67'
NCHC_PORT = '27017'
NCHC_DATABASE = 'JE0fQbzONJAAwdCxmM9BIabK'
NCHC_COLLECTION = 'JE0fQbzONJAAwdCxmM9BIabK'


def get_altas_mgdb_connection ():

    client = MongoClient("mongodb+srv://"+ALTAS_USERNAME+":"+ALTAS_PASSWORD+"@cluster0.geaah.mongodb.net/")
    mgdb_database = client[ALTAS_DATABASE]
    mgdb_collection = mgdb_database[ALTAS_COLLECTION]

    return client, mgdb_collection

def get_nchc_mgdb_collection():
    client = MongoClient('mongodb://mongodb:27017/')
    mgdb_database = client[NCHC_DATABASE]
    mgdb_collection = mgdb_database[NCHC_COLLECTION]

    return client, mgdb_collection


# TODO count col
def get_pcs ():
    n_pcs = 0
    return n_pcs

@app.route('/start', methods=['POST'])
@cross_origin()
def start():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    f = open(filename, 'a+')  # open file in append mode

    
    f.write(datetime.datetime.now().strftime("%s"))
    f.close()

    response_dict = dict()
    response_data = make_response("response", 200)

    return response_data


@app.route('/stop', methods=['POST'])
@cross_origin()
def stop():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    with open(filename) as f:
        starttime = f.readlines()

    end_time = int(datetime.datetime.now().strftime("%s"))
    start_time = int(starttime[0])
    diff_second = end_time - start_time

    print('diff = ', diff_second, ' seconds')

    # insert to database
    insert_dict = dict()
    insert_dict['machine'] = filename
    insert_dict['start'] = str(start_time)
    insert_dict['end'] = str(start_time)
    insert_dict['diff'] = str(diff_second)
    insert_dict['pcs'] = str(get_pcs())
    print(insert_dict)

    client, mgdb_collection = get_altas_mgdb_connection ()
    mgdb_collection.insert(insert_dict)
    client.close()

    # remove status and response to client
    os.remove(filename)

    response_dict = dict()
    response_data = make_response("response", 200)

    return response_data


@app.route('/get_status', methods=['POST'])
@cross_origin()
def get_status():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    response_dict = dict()
    file_exists = os.path.exists(filename)  
    if file_exists:
        # file exist'
        response_dict['results'] = True
        response_data = make_response(response_dict, 200)
    else:
        # file not exist'
        response_dict['results'] = False
        response_data = make_response(response_dict, 200)

    return response_data


if __name__ =='__main__':


    app.run(host='0.0.0.0', port=5001, debug=True) 