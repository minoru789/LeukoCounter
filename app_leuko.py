import requests
import pandas as pd
import numpy as np
import json 
from flask import Flask
import os

app = Flask(__name__)

from app import routes
from app import lib


@app.route("/")
def main():
    return "teste gabriel"
