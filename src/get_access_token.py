import requests
import secrets
import json

client_id = '963e88e06d2cc42e822fecaae6e86c22'
client_secret = 'd506643fc1b782b3cb70c5d5168e78aecbe34f0d83669af953000f86ce6899fa'


def get_new_code_verifier():
    code_verifier = secrets.token_urlsafe(100)
    return code_verifier[:128]


def generate_url(client_id, code_challenge):
    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={client_id}&state=YOUR_STATE&code_challenge={code_challenge}&code_challenge_method=plain'
    print(url)


def generate_code():
    authorization_code = input('Paste the authorisation code: ').strip()
    return authorization_code


def generate_access_token(client_id, client_secret, authorization_code, code_verifier):
    url = 'https://myanimelist.net/v1/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }
    r = requests.post(url, data=payload)
    print(r.url)
    r.raise_for_status()

    access_token = r.json()
    print('Token generated successfully!')

    with open('./data/access_token.json', 'w') as f:
        json.dump(access_token, f, indent=4)
        print('Token saved in "./data/access_token.json"')


if __name__ == '__main__':
    code_verifier = code_challenge = get_new_code_verifier()
    generate_url(client_id, code_challenge)
    authorization_code = generate_code()
    generate_access_token(client_id, client_secret, authorization_code, code_verifier)
