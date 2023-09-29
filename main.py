import os
import urllib.parse
import requests
import json
from dotenv import load_dotenv
from strava_data import activities, refresh_token, need_refresh, set_tokens

from flask import Flask, request, Response, jsonify, redirect
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

STRAVA_CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)

@app.route('/strava_authorize', methods=['GET'])
def strava_authorize():
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'activity:read_all'
    }
    return redirect('{}?{}'.format(
        'https://www.strava.com/oauth/authorize',
        urllib.parse.urlencode(params)
    ))

@app.route('/import_tokens', methods=['GET'])
def import_tokens():
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return jsonify(set_tokens(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, code))

@app.route('/activities',methods=['GET'])
def strava_activities():
    # If token has expired call a refresh
    if need_refresh(): 
        new_tokens = refresh_token(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, strava_tokens['refresh_token'])
        activ = activities(new_tokens['access_token'])
    else:
        activ = activities(strava_tokens['access_token'])
    return jsonify(activ)
