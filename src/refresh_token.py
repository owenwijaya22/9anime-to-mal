import requests
import json
from get_access_token import client_id, client_secret

def get_refresh_token():
    with open('./data/access_token.json', 'r+') as f:
        refresh_token = json.load(f)['refresh_token']

def get_fresh_access_token(refresh_token):
    refresh_token_url = 'https://myanimelist.net/v1/oauth2/token'

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    r = requests.post(refresh_token_url, payload)
    fresh_access_token = r.json()
    return fresh_access_token

def save_fresh_access_token(fresh_access_token, file_path):
    with open(file_path, 'w') as f:
        json.dump(fresh_access_token, f, indent=4)

def main():
    file_path = './data/access_token.json'
    refresh_token = get_refresh_token(file_path)
    fresh_access_token = get_fresh_access_token(refresh_token)
    save_fresh_access_token(fresh_access_token, file_path)
    
if __name__ == '__main__':
    main()