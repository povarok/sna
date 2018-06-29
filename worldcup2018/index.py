#
import math
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

#--------------!!!!!!!!!!!!!!!!!!!!-----------------
#Изменить название файла для анализа!!!!!!!!!!!!
filename = "mun.csv"
#Requirements for Watson

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='0762c16a-d667-4c63-95db-b0ccf162e49c',
  password='iGIqX7Aylphr',
  url='https://gateway.watsonplatform.net/natural-language-understanding/api',
  version='2018-03-16')


def keywords(text):
    json_output = natural_language_understanding.analyze(
    text=text,
    # url='https://gateway.watsonplatform.net/natural-language-understanding/api',
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
        print(df['text'][index])
        
        try:

            excess= re.search('[\S]*.[a-z]{0,6}/[\S]*',df['text'][index])
        except Exception:
            pass
        if excess != None:
            print('excess = ', excess)
            try:
                new_text=df['text'][index].replace(excess.group(),'')
            except Exception:
                pass
        else:
            new_text=df['text'][index]
        new_text=str(new_text).lower()
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
        print('Processing: ', len(result), '/', len(array))
        try:
            print ('try')
            tweet_keyword = keywords(tweet['text'])
            tweet_keyword = tweet_keyword['keywords']
            tweet["keywords"] = tweet_keyword

            print (tweet_keyword)
        except Exception:
            print('catch')
            pass
        # tweet_keyword = keywords(tweet['text'])
        # tweet["keywords"] = tweet_keyword
        result.append(tweet)
    return result
    
    
result_array=(text_analysis(csv_parser(filename)))  

client = pymongo.MongoClient("mongodb://admin:1234@cluster0-shard-00-00-ccstx.mongodb.net:27017,cluster0-shard-00-01-ccstx.mongodb.net:27017,cluster0-shard-00-02-ccstx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
#-----------------!!!!!!!!!!!!!!!!!!!!!!!!!!-------------------
#Изменить название таблицы для другого хештега!!!!!!!!!!!!!    
db = client['worldcup2018_release']
db.mundial_with_keywords.insert_many(result_array)
#-----------------!!!!!!!!!!!!!!!!!!!!!!!!!!-------------------

