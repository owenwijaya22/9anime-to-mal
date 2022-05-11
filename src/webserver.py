import logging
import threading
import json
from flask import Flask, request
import pathlib

webserver = Flask(__name__)

auth_code_received = threading.Event()


@webserver.route("/oauth")
def retrieve_auth_code():
    # Read the Authorisation Code from the query string of the URL
    auth_code = request.args.get('code', None, str)
    if auth_code is None:
        return '<p><span style="font-family: consolas">code</span> field not found.</p>'
    else:
        #create data directory to put all the json files/ configs
        p = pathlib.Path('./data')
        p.mkdir(exist_ok=True)
        with open('./data/auth_code.json', 'w') as file:
            json.dump({
                "auth_code": auth_code,
            }, file, indent=4)
            
        # Tell the main thread that we received the code
        auth_code_received.set()
        return '<p><span style="font-family: consolas">Done! You can go back to your application.</p>'


def start_server_thread(host: str, port: int):
    # Start a local web server in a new thread
    server_thread = threading.Thread(target=start_server,
                                     args=(host, port),
                                     daemon=True)
    server_thread.start()


def start_server(host: str, port: int):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL)
    webserver.run(host=host, port=port, debug=False)
