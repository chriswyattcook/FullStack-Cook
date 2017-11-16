from flask import Flask, url_for
import requests
from flask import request
from flask_cors import CORS
import json
from flask import jsonify
import random
import os 
from pymongo import MongoClient
import time


IMAGEDIR = './memes_blank'

# Create a link to our mongo database
client = MongoClient()

# name of our specific db
db = 'memes_db'

app = Flask(__name__)
CORS(app)

def has_no_empty_params(rule):
    """
    Used in the "site_map" function
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/', methods=['GET'])
def index():
    return site_map()


@app.route('/meme_generator/v1.0/site_map', methods=['GET'])
def site_map():
    links = {}
    methods = ["DELETE", "GET", "PATCH", "POST", "PUT"]
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters

        for m in methods:
            if m in rule.methods and has_no_empty_params(rule):
                if not m in links:
                    links[m] = []
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links[m].append((url, rule.endpoint))

    # links is now a list of url, endpoint tuples
    if len(links) > 0:
        return jsonify({"success": True, "routes": links})
    else:
        return jsonify({"success": False, "routes": links})


@app.route('/meme_generator/v1.0/grab_image', methods=['GET'])
def grab_image():
    """
    Gets an image from the web and saves it to the local file system.
    """
    
    url = request.args['url']
    fname = request.args['fname'].replace(' ','_').strip()

    if fname == '':
        fname = str(time.time())

    # Turn URL into a list with the '.' (dot) as the delimiter
    parts = url.split('.')
    # Now the image extension (jpg,png,etc.) will be on the end of the list
    ext = parts[-1]

    # New way!!
    # Append path to filename for saving
    full_fname = os.path.join(IMAGEDIR,fname+'.'+ext)
    # Go grab the image via the requests library
    f = open(full_fname,'wb')
    f.write(requests.get(url).content)
    f.close()

    # Old way!!
    # with open(fname+'.'+ext, 'wb') as handle:
    #         response = requests.get(url, stream=True)

    #         if not response.ok:
    #             print(response)

    #         for block in response.iter_content(1024):
    #             if not block:
    #                 break

    #             handle.write(block)

    # Check to see if file was actually saved and return 
    # appropriate message
    if os.path.isfile(full_fname):
        return jsonify({"success":True,"img_path":full_fname})
    else:
        return jsonify({"success":False,"error":"Error saving file."})


@app.route('/meme_generator/v1.0/generate_image', methods=['GET'])
def generate_image():
    print(request.args)
    
    return {}

@app.route('/meme_generator/v1.0/find_image', methods=['GET'])
def find_image():

    mid = request.args['id']
    user = request.args['user']

    collection = user + '_memes'

    filter = {}

    filter['mid'] = mid

    images = client[db][collection].find(filter, {"_id": 0})

    results_list = []
    for image in images:
        results_list.append(image)

    return jsonify(results_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
