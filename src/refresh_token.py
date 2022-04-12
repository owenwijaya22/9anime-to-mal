import requests
import json
from get_access_token import client_id, client_secret

with open('./data/access_token.json', 'r+') as f:
    refresh_token = json.load(f)['refresh_token']

refresh_token_url = 'https://myanimelist.net/v1/oauth2/token'

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
}

r = requests.post(refresh_token_url, payload)
fresh_access_token = r.json()
with open('./data/access_token.json', 'w') as f:
    json.dump(fresh_access_token, f, indent=4)
