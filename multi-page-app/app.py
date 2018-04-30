import dash
import os

from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
from random import random
import plotly
from textblob import TextBlob
import nltk
import pandas as pd
import re
import numpy as np
import pymongo
from pymongo import MongoClient

from flask import send_from_directory


app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True

external_css = [
    '/static/base.css',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
]
for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
