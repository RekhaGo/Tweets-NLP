#!/usr/bin/env python
# coding: utf-8

# In[9]:


# import statements  
import pandas as pd
import re
import json
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt

def load_analysis_data(filename):
    '''
        Load and clean winners.csv in pandas dataframe
    '''
    data_df = pd.read_csv(filename,names=['Categories', 'Winners'],header=0)
    data_df['Winners']=data_df['Winners'].str.lower().apply(lambda x:clean_tweet(x))
    return data_df

def load_tweet(filename):
    '''
        Load and clean data from json
    '''
    print('loading dataset : ',filename)
    json_data = json.loads(open(filename).read())
    tweets = []
    for line in json_data:
        tweet = line['text'].lower()
        tweets.append(clean_tweet(tweet))
    return tweets

def clean_tweet(tweet):
    '''
    Remove @,rt,links and special character
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z!?])|(http(.*))|(^rt)", " ", tweet).split())

def polarity(text):
    '''
    Calculate polarity for a given text
    '''
    result = TextBlob(text)
    return result.sentiment.polarity

def find_matching_twts(text,tweets):
    '''
    Find tweets about winners
    '''
    match=[]
    for tweet in tweets:
        if re.search(text,tweet):
            match.append(tweet)
    return match

def cal_sentiment(polarity):
    '''
    Calculate sentiment based on polarity
    '''
    strong_pos=0
    pos=0
    weak_pos=0
    neutral=0
    weak_neg=0
    neg=0
    strong_neg=0
    for i in polarity:
        if(i <= 1 and i > 0.6):
            strong_pos+=1
        elif(i <= 0.6 and i > 0.3):
            pos+=1
        elif(i <= 0.3 and i > 0):
            weak_pos+=1
        elif(i == 0):
            neutral+=1
        elif(i < 0 and i >= -0.3):
            weak_neg+=1
        elif(i < -0.3 and i >= -0.6):
            neg+=1
        elif(i < -0.6 and i >= -1):
            strong_neg+=1
    return strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg

def percentage(reaction,twt_len):
    '''
    Calculate percentage
    '''
    if twt_len!=0:
        return round(((reaction/twt_len)*100),2)
    else:
        return 0
    
def sentiment_analysis(text,tweets):
    '''
    Perform sentiment analysis for each winner
    '''
    strong_pos_list=[]
    pos_list=[]
    weak_pos_list=[]
    neutral_list=[]
    weak_neg_list=[]
    neg_list=[]
    strong_neg_list=[]
    no_of_tweets=[]
    for i, v in text.iteritems():
        txt_polarity=[]
        match_tweets=find_matching_twts(v,tweets)
        len_tweets=len(match_tweets)
        no_of_tweets.append(len_tweets)
        if len_tweets!=0:
            for twt in match_tweets:
                txt_polarity.append(polarity(twt))
            strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg=cal_sentiment(txt_polarity)
            strong_pos_list.append(percentage(strong_pos,len_tweets))
            pos_list.append(percentage(pos,len_tweets))
            weak_pos_list.append(percentage(weak_pos,len_tweets))
            neutral_list.append(percentage(neutral,len_tweets))
            weak_neg_list.append(percentage(weak_neg,len_tweets))
            neg_list.append(percentage(neg,len_tweets))
            strong_neg_list.append(percentage(strong_neg,len_tweets))
        else:
            strong_pos_list.append(0)
            pos_list.append(0)
            weak_pos_list.append(0)
            neutral_list.append(0)
            weak_neg_list.append(0)
            neg_list.append(0)
            strong_neg_list.append(0)
    return strong_pos_list,pos_list,weak_pos_list,neutral_list,weak_neg_list,neg_list,strong_neg_list,no_of_tweets

def plot_it(df_plot,No_of_col_in_csv,filename):
    '''
    plot the barh for sentiment analysis
    '''
    tmp_df=df_plot[df_plot['No of Tweets']>100]
    tmp_df=(tmp_df[tmp_df.columns[No_of_col_in_csv:-1]]).T
    headers = tmp_df.iloc[0]
    tmp_df.columns =headers
    display_df=tmp_df.drop(['Title'],axis=0)
    fig, axes = plt.subplots(nrows=len(display_df.columns), ncols=1)
    plt.rcParams.update({'axes.titlepad': 2})
    for i, c in enumerate(display_df.columns):
        display_df[c].plot(kind='barh', ax=axes[i], figsize=(10, 50))
        axes[i].set_title(c, pad=20)
        axes[i].title.set_color('red')
        axes[i].title.set_size(14)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
             
def main():
    # import the winners list
    analysis_df=load_analysis_data('winner_2013.csv')
    filename='winner_2013'
    No_of_col_in_csv=len(analysis_df.columns)
    analysis_df['Title']=analysis_df['Categories']+'\n'+analysis_df['Winners']
    # import twitter data
    tweets=load_tweet('../data/gg2013.json')
    #calculate and plot sentiment analysis
    strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg,no_of_tweets=sentiment_analysis(analysis_df['Winners'],tweets)
    response_df=pd.DataFrame(np.column_stack([strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg,no_of_tweets]), 
        columns=['Strong_Positive', 'Positive', 'Weak Positive','Neutral','Weak Negative','Negative','Strong Negative','No of Tweets'])
    final_data = pd.concat([analysis_df, response_df],axis=1)
    final_data['Title']=final_data['Title']+' \n Sentiment Analysis in % from: '+ final_data['No of Tweets'].astype(str)+' Tweets'
    filename_plot=filename+'_plot.pdf'
    print(f"The plot will be saved in the file, {filename_plot}")
    plot_it(final_data,No_of_col_in_csv,filename_plot)
    
    
if __name__ == '__main__':
    
    main()


# In[ ]:




