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

global client
client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    

#------------------------ для графика со средними значениями полярности
#----так как теперь в БД лежат все языки, а анализируем мы только рус/енг добавляется проверка на язык!
def get_avg_polarity(mongoArray):    
    avg_pol = {}
    for i in mongoArray:
        if i['text'] == 'pop_words':
            continue
        #if i['language']=='en' or i['language']=='ru':
        if i["date"] in avg_pol:
            avg_pol[i["date"]].append(i["polarity"])
        else:
            avg_pol[i["date"]] = []
            avg_pol[i["date"]].append(i["polarity"])
    
    #Calc average polarity for each day
    for key in avg_pol.keys():
        avg_pol[key] = np.mean(avg_pol[key])
    return avg_pol

def get_languages_ratio(mongoArray):
    lang_ratio = {}

    for i in mongoArray:
        if i['text'] == 'pop_words':
            continue
        if i["language"] in lang_ratio:
            lang_ratio[i["language"]] += 1
        else:
            lang_ratio[i["language"]] = 1
    return lang_ratio
        

def get_db(hashtag, request):
    
    #client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    db = client['productiondb']
    db_request = db[hashtag].find(request)
    #str_len = str(len(list(db_request)))
    #print ("str_len не из update- " + str_len)
    #out = get_avg_polarity(db_request)
    print('conn')
    client.close()
    return db_request


def get_network_data():
    net_data = get_db('fifa2018_russia', {'text':'pop_words'}) 
    net_data_keys = list(net_data[0]['named_entities'][0].keys())
    #print(net_data_keys)
    result = {}
    nodes = []
    colors = ['rgb(208, 89, 0)','rgb(208, 143, 0)','rgb(208, 207, 0)',
    'rgb(0, 208, 43)','rgb(0, 223, 162)','rgb(20, 36, 123)',
    'rgb(98, 0, 226)','rgb(180, 19, 223)','rgb(243, 21, 200)','rgb(152, 0, 0)']
    id = 0
    for el in net_data_keys:
        nodes.append({'id':id, 'label': el, 'color': colors[id % 10]})
        id += 1
    result['nodes'] = nodes
    result['edges'] = []
    #print(result)
    return result



colors = {'background': '#7FDBFF','text': '#7FDBFF'}


f= open('./apps/fifa2018_russia.html','r')

layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='#fifa #russia'),
        ], className='center-wrap-content'),
    ],className='rs-header'),

    html.Div([
        html.Div([
        html.H1(children='Plots'),
        html.A('Twitter', href='/apps/app1', className='btn-link'),
        html.A('Second Plot', href='/apps/app2', className='btn-link'),
        ], className='center-wrap-content'),
    ], className='rs-sidebar-header'),
 
    html.Div(id='intermediate-value', style={'display': 'none'}),


    html.Div([
        html.H1(children='Polarity',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        Number of tweets - ''' + str(len(list(get_db("fifa2018_russia", {})))),
        id="num_tweets",

        style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Dropdown(id='dropdown',
            options=[
                {'label': '#fifa2018 #russia', 'value': 'fifa2018_russia'},
                {'label': '#fifa #world #cup #russia', 'value': 'fifa_world_cup_russia'}
        ],
        value='fifa2018_russia'),
        #dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-graph-bar'),
        dcc.Interval(
            id='interval-component',
            interval=1*60000
        ),


        html.H1(children='Language percent',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(id='pie-bar'),
        
        html.Div([
            visdcc.Network(id='net',
                data=get_network_data(),

                options=dict(height='600px', width='100%'))
        ]),
        html.Iframe(srcDoc=f.read(),height="900",width="1300", id='iframe'),
        html.Div([
            html.Div([
                html.H3(children='sentiment data analysis ® 2018')
            ], className='center-wrap-content'),
        ], className='rs-footer'),
    ], className='main-content')
    
])


@app.callback(Output('intermediate-value', 'children'), [Input('dropdown', 'value')],
events=[Event('interval-component', 'interval')])
def clean_data(hashtag):
    table_data = get_db(hashtag, {})

    table_data = list(table_data)

    for el in table_data:
        el.pop('_id')

    print (type(table_data))
     
    return json.dumps(table_data) # or, more generally, json.dumps(cleaned_df)

@app.callback(Output('iframe', 'srcDoc'), [Input('dropdown', 'value')])
def change_iframe(value):
    f= open(value+'.html','r')
    name = f.read()
    return name

@app.callback(Output('live-update-graph-bar', 'figure'), [Input('intermediate-value', 'children')])
             # events=[Event('interval-component', 'interval')])
def update_graph_bar(table_data):
    
    
    # client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    
    
    # db = client['productiondb']
    
    # db_request = db.fifa_russia.find()
    # print (len(list(db_request)))
    out = get_avg_polarity(json.loads(table_data))
    
    traces = list()
    #str_len = len(list(db_request))
    #print("из update"+ str_len)
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



@app.callback(Output('pie-bar', 'figure'),[Input('intermediate-value', 'children')])
            #  events=[Event('interval-pie', 'interval')])
def update_pie_bar(table_data):

    


    out = get_languages_ratio(json.loads(table_data))
    labels = list(out.keys())
    values = list(out.values())
    print(labels)
    print(values)
    trace = plotly.graph_objs.Pie(labels=labels, values=values, textinfo='none', hoverinfo='label+percent')
    
    layout = plotly.graph_objs.Layout(barmode='group')
    
    return {'data': [trace], 'layout': layout}



@app.callback(
    Output(component_id='num_tweets', component_property='children'),[Input('intermediate-value', 'children')])
    # events=[Event('interval-counter', 'interval')])
def update_output_div(table_data):
    
    print("title upd")
    string = "Number of tweets - " + str(len(list(json.loads(table_data))))
    #print (string)
    return string

@app.callback(Output('net', 'options'),[Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}
