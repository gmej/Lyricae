import time
from flask import Flask

app = Flask(__name__)


@app.route('/time')
def return_current_time():
    return {'time': time.time()}