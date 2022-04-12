from get_access_token import client_id, client_secret
import json
import requests
with open('./data/access_token.json', 'r+') as f:
    access_token = json.load(f)['access_token']

url = 'https://api.myanimelist.net/v2/users/@me/animelist?fields=list_status'
response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        }).json()
with open('./data/@me.json', 'w') as f:
    json.dump(response, f, indent=4)