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
import flask

app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

app.css.append_css({
    'external_url': '/static/style.css',
  
})


