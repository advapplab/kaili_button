from flask import Flask, request, make_response
from flask_cors import cross_origin
import os.path


# APP configurations
app= Flask(__name__)



@app.route('/start', methods=['POST'])
@cross_origin()
def start():
    # {'equipment':'machine01'}

    post_data = request.json
    filename = post_data['equipment']

    f = open(filename, 'a+')  # open file in append mode
    f.write('python rules')
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