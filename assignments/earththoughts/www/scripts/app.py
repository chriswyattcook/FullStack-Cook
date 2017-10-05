from flask import Flask, url_for
from flask import request
from flask_cors import CORS
import json
from flask import jsonify
from flask import *
import random
import sys,os
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/', methods=['GET'])
def index():
    return site_map()


@app.route('/site-map', methods=['GET'])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if not url == '/site-map':
                links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    if len(links) > 0:
        return jsonify({"success": True,"routes":links})
    else:
        return jsonify({"success": False,"routes":links})


@app.route('/get_image')
def get_image():
    # print(request.args)
    # return "Hello {}!".format(request.args[''])
    image_list = []
    jsondata = json.loads(open('earthporn.json','r').read())
    for child in jsondata['data']['children']:
        image_list.append(child['data']['preview']['images'][0]['source']['url'])
    
    random.shuffle(image_list)


    return jsonify({"success":True,"url":image_list[0]})

@app.route('/get_thought')
def get_thought():
    # print(request.args)
    # return "Hello {}!".format(request.args[''])
    thought_list = []
    jsondata = json.loads(open('showerthoughts.json','r').read())
    for child in jsondata['data']['children']:
        thought_list.append(child['data']['title'])
    
    random.shuffle(thought_list)

    #print(thought_list)

    return jsonify({"success":True,"thought":thought_list[0]})

@app.route('/js/<path:filename>')
def serve_static_js(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'js'), filename)

@app.route('/css/<path:filename>')
def serve_static_css(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'css'), filename)

@app.route('/home')
def home():
    return send_file('../index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)