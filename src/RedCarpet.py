#!/usr/bin/env python
# coding: utf-8

# In[10]:


# import statements  
import pandas as pd
import re
import json
import nltk
import itertools
import random
from itertools import chain
from IPython.display import display
from collections import Counter
from textblob import TextBlob

def load_tweet(filename):
    '''
        Load and clean data from json
    '''
    print('loading dataset : ',filename)
    json_data = json.loads(open(filename).read())
    tweets = []
    for line in json_data:
        tweet = line['text']
        tweets.append(clean_tweet(tweet))
    return tweets

def clean_tweet(tweet):
    '''
    Remove @,rt,links and special character
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z!?])|(http(.*))|(^rt)|(GoldenGlobes)|(Golden Globes)|(RT)", " ", tweet).split())

def extract_names(t):
        entity_names = []
        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_names(child))
        return entity_names

def find_entity(sample):
    '''
    Extract entity names for a given sentence
    '''
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(extract_names(tree))
    return entity_names

def polarity(tweets):
    '''
    Calculate polarity for a given text
    '''
    best_dress_twts=[]
    worst_dress_twts=[]
    neutral_dress_twts=[]
    for text in tweets:
        result = TextBlob(text).sentiment.polarity
        if result>0:
            best_dress_twts.append(text)
        elif result<0:
            worst_dress_twts.append(text)
        else:
            neutral_dress_twts.append(text)
    return best_dress_twts,worst_dress_twts,neutral_dress_twts

def clean_common_words(tweets):
    '''
    Remove commonly used words
    '''
    stop_words=['red','carpet','wow','great','golden','globe','awards','warner bros','hollywood','movies','party','everyone','phenomenal','best',
               'enjoy','style','instyle','omg','nbc','look','damn','awesome','actor','actress','gorgeous','winner','cute','performance','brilliant',
                'incredible','beauty','twitter','details','hot','party','fashion','tonight','favorite','photo','amazing','oscars','aww','stunning',
                'yay','dress','sweet','fun','model','please','anyone','everyone','someone','Fav','lol','shades','YUPP','yes','orange','fifty','grey','black',
                'OBSESSED','worst','common'
        ]
    exclusions = '|'.join(stop_words)
    clean_tweet=[]
    for t in tweets:
        clean_tweet.append(' '.join(re.sub(exclusions, " ", t,flags=re.IGNORECASE).split()))
    return clean_tweet
 
def frequent_name(tweets):
    '''
    find the most frequent entity name
    '''
    entities=[]
    for sen in tweets:
        entities.append(find_entity(sen))
    return list(chain.from_iterable(entities))

def red_carpet_tweets(tweets):
    '''
    Find tweets about red carpet
    '''
    word_list = ['dress','look','looks','great','wow','stunning','gown','model','fashion','coat','outfit','style','form','cut','cloth','clothing','creative',
                'beauty','trendy','trend','fit','image','figure','stylist','boutique','decor','stylish','wear','redcarpet','red carpet','#redcarpet','stunning','georgous','wow','great'
                ]
    filter_tweets=[]
    for tweet in tweets:
        if any(word in tweet.lower() for word in word_list):
            filter_tweets.append(tweet)
    return filter_tweets

def plot_it(best_dress_name_list,worst_dress_name_list,most_dress_name_list):
    '''
    To plot the final dataframe
    '''
    best_top_10=Counter(best_dress_name_list).most_common(10)
    worst_top_10=Counter(worst_dress_name_list).most_common(10)
    most_top_10=Counter(most_dress_name_list).most_common(10)
    best_top_10_df = pd.DataFrame(best_top_10)
    worst_top_10_df=pd.DataFrame(worst_top_10)
    most_top_10_df=pd.DataFrame(most_top_10)
    frames = [most_top_10_df,best_top_10_df, worst_top_10_df]
    result = pd.concat(frames,axis=1)
    result.columns=['Most discussed','No of Twts','Best dressed','No of Twts','Worst dressed','No of Twts']
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', -1)
    display(result)
    
    
def get_redcarpet(year):
    try:
        print("Analysis for Red Carpet starts ....")
        # import twitter data
        json_name='gg'+str(year)+'.json'
        tweets=load_tweet(json_name)
        red_carpet_twts = red_carpet_tweets(tweets)
        if len(red_carpet_twts) > 150010:
            random_red_twts = random.sample(red_carpet_twts, 150000)
            cleaned_twt = clean_common_words(random_red_twts)
        else:
            cleaned_twt = clean_common_words(red_carpet_twts)

        # split tweets based on polarity
        best_dress, worst_dress, neutral_dress = polarity(cleaned_twt)
        # get most frequent names from tweets
        best_dress_name_list = frequent_name(best_dress)
        worst_dress_name_list = frequent_name(worst_dress)
        neutral_dress_name_list = frequent_name(neutral_dress)
        most_discussed_list = list(
            itertools.chain(best_dress_name_list, worst_dress_name_list, neutral_dress_name_list))
        plot_it(best_dress_name_list, worst_dress_name_list, most_discussed_list)

    except(FileNotFoundError, IOError):
        print("File not found. Please enter a valid year")
    print("Analysis for Red Carpet ends ....")

if __name__ == '__main__':
    get_redcarpet(year)

