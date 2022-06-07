from __future__ import nested_scopes
from flask import Flask, request, make_response, render_template
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
NCHC_DATABASE = 'b8a71022-306e-49e2-86e3-1a0d30cafc7d'
NCHC_COLLECTION = 'datahub_HistRawData_444cbfad-250c-4243-a14f-5ea956339702'

product_status_file = 'product'

def get_altas_mgdb_connection ():

    client = MongoClient("mongodb+srv://"+ALTAS_USERNAME+":"+ALTAS_PASSWORD+"@"+ALTAS_HOST+"/")
    mgdb_database = client[ALTAS_DATABASE]
    mgdb_collection = mgdb_database[ALTAS_COLLECTION]

    return client, mgdb_collection

def get_nchc_mgdb_collection():

    # client = MongoClient(host=[NCHC_HOST + ':' + NCHC_PORT],
    #                      username=NCHC_USERNAME,
    #                      password=NCHC_PASSWORD,
    #                      authSource=NCHC_DATABASE)

    client = MongoClient("mongodb://08050cc6-73fb-4d20-b60a-484c3241a812:JE0fQbzONJAAwdCxmM9BIabK@203.145.215.67:27017/b8a71022-306e-49e2-86e3-1a0d30cafc7d")

    mgdb_database = client[NCHC_DATABASE]
    mgdb_collection = mgdb_database[NCHC_COLLECTION]
    
    return client, mgdb_collection

def get_pcs (start_time, end_time, machine):

    # combine arg
    # start_time_iso = (datetime.datetime.utcfromtimestamp(start_time)+datetime.timedelta(hours=8)).isoformat()
    # end_time_iso = (datetime.datetime.utcfromtimestamp(end_time)+datetime.timedelta(hours=8)).isoformat()
    start_time_iso = datetime.datetime.utcfromtimestamp(start_time).isoformat()
    end_time_iso = datetime.datetime.utcfromtimestamp(end_time).isoformat()

    machine = machine[0].upper() + machine[1:]
    machine = machine[0:7] + " " + machine[7:]

    # query_ts = dict()
    # query_ts['ts'] = {'$gte':datetime.datetime.utcfromtimestamp(start_time), '$lt':datetime.datetime.utcfromtimestamp(end_time)}

    # query_ID = dict()
    # query_ID['deviceId'] = machine

    # query_dict = dict()
    # query_dict['$and'] = [query_ts, query_ID]
    # print(query_dict)

    # query count of pcs in database
    client, mgdb_collection = get_nchc_mgdb_collection ()
    n_pcs = mgdb_collection.count_documents({
                '$and':
                    [
                        {'ts':{'$gte':datetime.datetime.utcfromtimestamp(start_time), '$lt':datetime.datetime.utcfromtimestamp(end_time)}},
                        {'deviceId':machine}
                    ]
            })
    client.close()

    # print(start_time_iso, end_time_iso, machine, n_pcs)

    return n_pcs


@app.route("/")
def index():
    return render_template("button.html")

@app.route('/start', methods=['POST'])
@cross_origin()
def start():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    # delete file if exist
    if os.path.exists(filename):
        os.remove(filename)
    
    if os.path.exists(product_status_file):
        os.remove(product_status_file)

    # machine name
    f = open(filename, 'a+')  # open file in append mode
    f.write(datetime.datetime.now().strftime("%s"))
    f.close()

    # product name
    f = open(product_status_file, 'a+')  # open file in append mode
    f.write(post_data['product'])
    f.close()

    response_dict = dict()
    response_dict['response'] = 200
    response_data = make_response(response_dict, 200)

    return response_data

@app.route('/stop', methods=['POST'])
@cross_origin()
def stop():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']
    product = post_data['product']

    with open(filename) as f:
        starttime = f.readlines()

    end_time = int(datetime.datetime.now().strftime("%s"))
    start_time = int(starttime[0])
    diff_second = end_time - start_time

    # print('diff = ', diff_second, ' seconds')

    # insert to database
    insert_dict = dict()
    insert_dict['machine'] = filename
    insert_dict['epoch_start'] = str(start_time)
    insert_dict['epoch_end'] = str(end_time)
    insert_dict['epoch_diff'] = str(diff_second)
    insert_dict['pcs'] = str(get_pcs(start_time, end_time, filename))
    insert_dict['product'] = product
    # print(insert_dict)

    client, mgdb_collection = get_altas_mgdb_connection ()
    mgdb_collection.insert_one(insert_dict)
    client.close()

    # remove status and response to client
    os.remove(filename)
    os.remove(product_status_file)

    response_dict = dict()
    response_dict['response'] = 200
    response_data = make_response(response_dict, 200)

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
        # file exist', means running
        response_dict['results'] = True

        # load product name
        with open(product_status_file) as f:
            product_name = f.readlines()

        print(product_name[0])
        response_dict['product'] = product_name[0]
        response_data = make_response(response_dict, 200)

    else:
        # file not exist'
        response_dict['results'] = False
        response_dict['product'] = ''
        response_data = make_response(response_dict, 200)

    return response_data

@app.route('/reset', methods=['POST'])
@cross_origin()
def reset():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    # remove status and response to client
    try:
        os.remove(filename)
        os.remove(product_status_file)
    except:
        print('do nothing')

    response_dict = dict()
    response_dict['response'] = 200
    response_data = make_response(response_dict, 200)

    return response_data

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 