
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

from random import random

colors = {'background': '#7FDBFF','text': '#7FDBFF'}
#  html.Div([
#             dcc.Graph(id='wind-speed'),
#         ]),
#         dcc.Interval(id='wind-speed-update', interval=1000, n_intervals=0),



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
      Number info'''
    ,
    
    style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(id='live-update-graph-scatter', animate=True),

        dcc.Interval(
            id='interval-component',
            interval=1*1000
        ),


        html.Div([
            html.Div([
                html.H3(children='Information here')
            ], className='center-wrap-content'),
        ], className='rs-footer'),
        
    ], className='main-content')

  
    
])



@app.callback(Output('live-update-graph-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_scatter():

    traces = list()
    for t in range(2):
        traces.append(plotly.graph_objs.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[(t + 1) * random() for i in range(5)],
            name="Line " + str(t),

            line=dict(
                color=('rgb(220, 96, 167)'),
                width=4,
                dash='dashdot')

            ))
    return {'data': traces}
