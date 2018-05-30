from app import app

from dash.dependencies import Output, Event, Input, State
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
import json
import dash
import visdcc

import tweepy
from tweepy import OAuthHandler
import json
import calendar
import sys

from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from collections import deque

global client
client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    
que = deque()

#Queque def
def deq(q,v):
    print ('++++++++++')
    print (type(v))
    
    v = int(v)
    print(v)
    if len(q) == 10:
        print('зашли в иф')
        q.popleft()
        #Here append new data to array
        #q.append(random.randint(1, 4000))
        q.append( v )
    else:
        print('зашли в элс')
        print(type(v))
        q.append(v)
        print('append works')
    return q

def get_db():
    
    #client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    db = client['productiondb']
    db_request = db['streaming'].find_one()

    print('conn app2')
    print (db_request)
    print (db_request['polarity'])
    client.close()
    print ('------------------------')
    print (db_request)
    return db_request



colors = {'background': '#7FDBFF','text': '#7FDBFF'}


layout = html.Div([

    html.Div(id='intermediate-value-app2', style={'display': 'none'}),

    html.Div([
        html.Div([
            html.H1(children='Streaming'),
        ], className='center-wrap-content'),
    ],className='rs-header'),

    html.Div([
        html.Div([
        html.H1(children='Plots'),
        html.A('Twitter', href='/apps/app1', className='btn-link'),
        html.A('Streaming', href='/apps/app2', className='btn-link'),
        ], className='center-wrap-content'),
    ], className='rs-sidebar-header'),
 
    html.Div(id='intermediate-value', style={'display': 'none'}),


    html.Div([
        html.H1(children='Live tweets',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    #Here plots

    dcc.Graph(id='live-update-graph-scatter-app2', animate=True),
    
    dcc.Interval(
        id='interval-component-app2',
        interval=1*3000
    ),


    html.Div([
        html.Div([
                html.H3(children='sentiment data analysis ® 2018')
            ], className='center-wrap-content'),
        ], className='rs-footer'),
    ], className='main-content')
    
])




@app.callback(Output('intermediate-value-app2', 'children'), 
events=[Event('interval-component-app2', 'interval')])
def clean_data_app2():
    table_data = get_db()
    print ('after getdb')
    print (table_data)

    table_data.pop('_id')
    print (table_data)
    print ('pop worked')

    print (type(table_data))
     
    return json.dumps(table_data) # or, more generally, json.dumps(cleaned_df)


@app.callback(Output('live-update-graph-scatter-app2', 'figure'), [Input('intermediate-value-app2', 'children')])
            
def update_graph_scatter_app2(table_data_app2):
    v=json.loads(table_data_app2)
    print ('-----------------------------------------------------')
    print (v['polarity'])
    y_arr = deq(que,v['polarity'])
    print('que works')
    print(y_arr)
    y_arr = list(y_arr)
    print(y_arr)

    traces = list()
    for t in range(1):
        traces.append(plotly.graph_objs.Scatter(
            x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            
            y=y_arr,
            name="Line " + str(t),

            line=dict(
                color=('rgb(220, 96, 167)'),
                width=4,
                dash='dashdot')

            ))
    return {'data': traces}