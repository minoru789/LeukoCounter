from app import app
from flask import request
from app.lib import read_and_treat
import requests
import pandas as pd
import numpy as np
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    json_loads = request.get_json(silent=True)
    url = json_loads.get('url', '')
    print(url)
    if url:
        result = read_and_treat(url)
        return result
    return 'Invalid request'
