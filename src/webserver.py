import logging
import threading
from flask import Flask, request


webserver = Flask(__name__)

auth_code_received = threading.Event()
auth_code = None


# Catch requests going to http://whjlocalhost/oauth
@webserver.route("/oauth")
def retrieve_auth_code():
    global auth_code
    # Read the Authorisation Code from the query string of the URL
    auth_code = request.args.get('code', None, str)
    if auth_code is None:
        return '<p><span style="font-family: consolas">code</span> field not found.</p>'
    else:
        # Tell the main thread that we received the code
        auth_code_received.set()
        return '<p><span style="font-family: consolas">Done! You can go back to your application.</p>'


def start_server(host: str, port: int):
    # Start a local web server in a new thread
    server_thread = threading.Thread(target = _start_server_thread, args = (host, port), daemon = True)
    server_thread.start()


def _start_server_thread(host: str, port: int):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL)
    webserver.run(host = host, port = port, debug = False)
