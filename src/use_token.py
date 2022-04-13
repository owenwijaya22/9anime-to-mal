from get_access_token import client_id, client_secret
import json
import requests
with open('./data/access_token.json', 'r+') as f:
    access_token = json.load(f)['access_token']

url = 'https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=100'
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(url, headers=headers).json()
with open('./data/data.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, indent=4)