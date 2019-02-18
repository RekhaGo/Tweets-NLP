#!/usr/bin/env python
# coding: utf-8

# In[5]:


# import statements  
import pandas as pd
import re
import json
import numpy as np
import random
from IPython.display import display
from textblob import TextBlob
import matplotlib.pyplot as plt
from sentiment_analysis_winners import load_tweet,clean_tweet,polarity,find_matching_twts,cal_sentiment,percentage,sentiment_analysis

def load_analysis_data(filename):
    '''
        Load and clean presenters.csv in pandas dataframe
    '''
    data_df = pd.read_csv(filename,header=0)
    data_df=data_df.fillna('na')
    cut_off_col=10
    df_col_names=['Category']
    for i in range(1,len(data_df.columns)):
        df_col_names.append('Presenter '+str(i))
    data_df.columns=df_col_names
    if(len(data_df.columns)>cut_off_col):
        data_df = data_df.iloc[:,0:cut_off_col]
    for i in range(1,len(data_df.columns)):
        col_name=data_df.columns[i]
        data_df[col_name]=data_df[col_name].str.lower().apply(lambda x:clean_tweet(x))
    return data_df

    
def split_categories(analysis_df,tweets):
    for i in range(len(analysis_df)):
        sub_df_i=analysis_df.iloc[i,:]
        sub_df_i.reset_index(drop=True, inplace=True)
        sub_df_i=sub_df_i.to_frame(name=sub_df_i[0])
        sub_df_i.drop(sub_df_i.index[0],inplace=True)
        sub_df_i.reset_index(drop=True,inplace=True) 
        col_name=sub_df_i.columns[0]
        strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg,no_of_tweets=sentiment_analysis(sub_df_i[col_name],tweets)
        response_df=pd.DataFrame(np.column_stack([no_of_tweets,strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg]), 
        columns=['No of Tweets','Strong_Positive(%)', 'Positive(%)', 'Weak Positive(%)','Neutral(%)','Weak Negative(%)','Negative(%)','Strong Negative(%)'])
        final_data = pd.concat([sub_df_i, response_df],axis=1)
        final_data=final_data.fillna(0)
        col_name_first=sub_df_i.columns[0]
        presenter_df=final_data[final_data[col_name_first]!='na']
        pd.set_option('display.max_columns', None)  
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', -1)
        display(presenter_df)       
                      
def main():
    global No_of_col_in_csv
    global filename
    while True:
        try:
            # Get year for analysis
            year = input("Please enter the year : ")
            # import the presenters list
            analysis_filename='presenters_'+str(year)+'.csv'
            analysis_df=load_analysis_data(analysis_filename)
            # import twitter data
            json_name='gg'+str(year)+'.json'
            tweets=load_tweet(json_name)
            break
        except(FileNotFoundError, IOError):
            print("File not found. Please enter a valid year")
    #calculate and plot sentiment analysis
    if len(tweets)>1054153:
        filter_tweets=random.sample(tweets, 1000000)
        split_categories(analysis_df,filter_tweets)
    else:
        split_categories(analysis_df,tweets)
    

if __name__ == '__main__':
    
    main()

