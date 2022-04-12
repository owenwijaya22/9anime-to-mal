url = 'https://api.myanimelist.net/v2/users/owenwijaya22/animelist'
headers = {'X-MAL-CLIENT-ID': '963e88e06d2cc42e822fecaae6e86c22'}
params = {}
import requests
import json

r = requests.get(url, headers=headers)
with open('./data/without_token.json', 'w') as file:
    json.dump(r.json(), file)