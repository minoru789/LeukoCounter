from flask import Flask
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
from app import lib

import requests
import pandas as pd
import numpy as np
import json 

def read_and_treat(url):
    request_url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/cca3a6c5-b5bd-499d-ad81-1534dadad10c/url'
    headers = {'Prediction-Key': 'f53df60f8d9645b4ae1a052dc892d3ea', 'Content-Type': 'application/json'}
    payload = {'Url': url}
    r = requests.post(request_url, json=payload, headers=headers)
    data = json.loads(r.text)
    data = pd.DataFrame.from_dict(data)
    predictions = list()
    for i in range(data.shape[0]):
        predictions.append(data.predictions[i])
    predictions = pd.DataFrame(predictions)
    boundings = list()
    for j in range(len(predictions)):
        boundings.append(predictions.boundingBox[j])
    boundings = pd.DataFrame(boundings)
    result = pd.concat([boundings, predictions], axis=1)
    result = result.drop(columns = ['boundingBox'])
    result = result.merge(result.groupby(by=['left', 'top'], as_index=False)['probability'].max(), how='inner').query('probability > 0.15')
    return result.to_json()


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

