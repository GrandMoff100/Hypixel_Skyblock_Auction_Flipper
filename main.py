import threading

from collections import defaultdict
from flask import Flask, render_template
from flips.ahflips import find_profitable_flips, bin_auctions
from flips.utils import get_key, keys


app = Flask(__name__)

KEY = get_key()
KEY_RESPONSES = defaultdict(list)


@app.route('/')
def index():
    return render_template(
        'index.html', 
        key=KEY.next()
    )


def flips_thread(key):
    for auction in bin_auctions(key):
        KEY_RESPONSES[key].append(auction)


@app.route('/rpc/start_flips/<string:key>')
def start_flips(key):
    KEY_RESPONSES[key] = []
    thread = threading.Thread(target=flips_thread, args=[key])
    thread.start()
    return 200


@app.route('/rpc/get_flips/<string:key>')
def get_flips(cookie, key):
    if key not in keys:
        return 'Invalid Key'
    return find_profitable_flips(KEY_RESPONSES.get(key))

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)