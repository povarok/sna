
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html


from app import app

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




#------------------------ для графика со средними значениями полярности
def get_avg_polarity(mongoArray):    
    avg_pol = {}
    for i in mongoArray:
        if i["date"] in avg_pol:
            avg_pol[i["date"]].append(i["polarity"])
        else:
            avg_pol[i["date"]] = []
            avg_pol[i["date"]].append(i["polarity"])

    for key in avg_pol.keys():
        avg_pol[key] = np.mean(avg_pol[key])
    print ("db working")
    return avg_pol

client = MongoClient('mongodb://localhost:27017/')
db = client['productiondb']
db_request = db.main.find()

str_len = str(len(list(db_request)))
print ("str_len - " + str_len)
out = get_avg_polarity(db_request)



colors = {'background': '#7FDBFF','text': '#7FDBFF'}

layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Dashboard title'),
        ], className='center-wrap-content'),
    ],className='rs-header'),

    html.Div([
        html.Div([
        html.H1(children='Plots'),
        html.Form(action='/apps/app1', children=
            [
                html.Button('Polarity', className='btn btn-primary btn-lg'),
            ]),
        html.Form(action='/apps/app2', children=
            [
                html.Button('Second plot', className='btn btn-primary btn-lg'),
            ]),
        ], className='center-wrap-content'),
    ], className='rs-sidebar-header'),
 



    html.Div([
        html.H1(children='Polarity',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        Number of tweets - ''' + str_len 
    ,
    
    style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        #dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-graph-bar'),
        dcc.Interval(
            id='interval-component',
            interval=1*5000
        ),

        
        html.Div([
            html.Div([
                html.H3(children='Information here')
            ], className='center-wrap-content'),
        ], className='rs-footer'),
    ], className='main-content')

  
    
])



@app.callback(Output('live-update-graph-bar', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_bar():
    
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['productiondb']
    db_request = db.main.find()
    out = get_avg_polarity(db_request)
    
    traces = list()
    
    traces.append(plotly.graph_objs.Bar(
        x=list(out.keys()),
        y=list(out.values()),

        name='#FIFA 2018'
        ))
    layout = plotly.graph_objs.Layout(
        barmode='group',
        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Arial, sans-serif',
                size=22,
                color='black'
            ),
            exponentformat='e',
            showexponent='All',            
            showticklabels=True
        )
        
    
)
    return {'data': traces, 'layout': layout}




