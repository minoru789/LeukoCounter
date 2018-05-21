import requests
import pandas as pd
import numpy as np
import json 
from flask import Flask
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
from app import lib


@app.route("/")
def main():
    return "teste gabriel"
