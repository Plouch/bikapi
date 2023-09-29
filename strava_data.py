import os
import json
import requests
import time

def activities(token):
    res = requests.get('https://www.strava.com/api/v3/activities?access_token=' + token)
    return res.json()

def refresh_token(id, secret, token):
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': id,
                                'client_secret': secret,
                                'grant_type': 'refresh_token',
                                'refresh_token': token
                                }
                    )
    with open('strava_tokens.json', 'w') as savefile:
        json.dump(response.json(), savefile)
    return response.json()

def need_refresh():
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    return strava_tokens['expires_at'] < time.time()

# if json file does not exist or has been corrupted
def set_tokens(id, secret, code):
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': id,
            'client_secret': secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    strava_tokens = response.json()
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)
    with open('strava_tokens.json') as proof:
        data = json.load(proof)
    return data