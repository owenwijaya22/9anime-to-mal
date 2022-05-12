import requests
import secrets
import json
import webbrowser
import webserver


class AccessToken:

    def __init__(self):
        #declared client_id and client_secret made on https://myanimelist.net/apiconfig
        self.client_id = '963e88e06d2cc42e822fecaae6e86c22'
        self.client_secret = 'd506643fc1b782b3cb70c5d5168e78aecbe34f0d83669af953000f86ce6899fa'

    #get code verifier/challenge as a temporary password
    def get_new_code_verifier(self):
        code_verifier = secrets.token_urlsafe(100)
        return code_verifier[:128]

    #build the url for mal authentication
    def generate_url(self, client_id, code_challenge):
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={client_id}&state=YOUR_STATE&code_challenge={code_challenge}&code_challenge_method=plain'
        webbrowser.open(url)

    def get_auth_code(self):
        with open('./data/auth_code.json', 'r') as file:
            self.auth_code = json.load(file)["auth_code"]

    #get the access token to myanimelist's api
    def generate_access_token(self, code_verifier):
        url = 'https://myanimelist.net/v1/oauth2/token'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.auth_code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code'
        }
        r = requests.post(url, data=payload)
        r.raise_for_status()

        access_token = r.json()
        print('Token generated successfully!')

        with open('./data/access_token.json', 'w') as f:
            json.dump(access_token, f, indent=4)
            print('\nToken saved in "./data/access_token.json"')

    def main(self):
        HOST = 'localhost'
        PORT = 5000
        code_verifier = code_challenge = self.get_new_code_verifier()
        self.generate_url(self.client_id, code_challenge)

        webserver.start_server_thread(HOST, PORT)
        webserver.auth_code_received.wait()

        self.get_auth_code()
        self.generate_access_token(code_verifier)

access_token_bot = AccessToken()
access_token_bot.main()