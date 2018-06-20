#вывод обработанного массива
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import pandas as pd
import re
import numpy as np
import pymongo
from pymongo import MongoClient
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, KeywordsOptions


filename = "C:/Users/Vasily/Anaconda3/GitHub/sna/worldcup2018/fifa_world_cup_russia.csv"
#Requirements for Watson

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='a6a6b0d5-370e-42b1-8391-97f12a99fb19',
  password='tK7MknYJsSGI',
  version='2018-03-16')


def keywords(text):
    json_output = natural_language_understanding.analyze(
    text=text,
    features=Features(
    keywords=KeywordsOptions(
      sentiment=True,
      emotion=True,
      limit=2)))
    return json_output


    

def csv_parser(filename):
    df = pd.read_csv(filename,sep=';')
    array = []

    for index in df.index:
        
        Dict={}
        excess= re.search('[\S]*.[a-z]{0,6}/[\S]*',df['text'][index])
        if excess != None:
            new_text=df['text'][index].replace(excess.group(),'')
        else:
            new_text=df['text'][index]
        new_text=new_text.lower()
        Dict['text']= new_text
        Dict['date']=df['date'][index].split(' ')[0]
        Dict['language']=df['language'][index]
        array.append(Dict)
        
   
    return(array)

#csv_parser(filename)



def named_entities(text):


    parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(text.split()), binary=True)  # POS tagging before chunking!

    named_entities = []

    for t in parse_tree.subtrees():
        if t.label() == 'NE':    #тут мы добавляем фильтр, какие штуки из предложения нам нужны
            #named_entities.append(t)
            named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
    return named_entities
    


# метод обработки массива твитов
def text_analysis (array):
    result = []
    tb = Blobber(analyzer=NaiveBayesAnalyzer())
    for tweet in array:
        
        tweet["polarity"] = tb(tweet["text"]).sentiment.p_pos - tb(tweet["text"]).sentiment.p_neg #добавляем поле полярность твита в именованый массив
        #print ('twit["polarity"]' + str(twit["polarity"]))
        tweet["noun_phrases"] = TextBlob(tweet["text"]).noun_phrases  # непонятно что это.  .. , но тоже добавляем
        tweet["named_entities"] = named_entities(tweet["text"])

        try:
            print ('tweet[text]' + tweet['text'])
            tweet_keyword = keywords(tweet['text'])
            tweet_keyword = tweet_keyword['keywords']
            tweet["keywords"] = tweet_keyword
        except:
            pass
        result.append(tweet)
    return result
    
    
result_array=(text_analysis(csv_parser(filename)))  


client = pymongo.MongoClient("mongodb://povarok:EDCFVgb1@cluster0-shard-00-00-watg3.mongodb.net:27017,cluster0-shard-00-01-watg3.mongodb.net:27017,cluster0-shard-00-02-watg3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    
db = client['worldcup2018_test']
db.fifa2018_russia.insert_many(result_array)

