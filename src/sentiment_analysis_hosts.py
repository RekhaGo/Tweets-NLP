#!/usr/bin/env python
# coding: utf-8

# In[5]:


# import statements  
import pandas as pd
import re
import json
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
from sentiment_analysis_winners import load_tweet,clean_tweet,polarity,find_matching_twts,cal_sentiment,percentage,sentiment_analysis

def load_analysis_data(filename):
    '''
        Load and clean hosts.csv in pandas dataframe
    '''
    data_df = pd.read_csv(filename,names=['Hosts'],header=0)
    data_df['Hosts']=data_df['Hosts'].str.lower().apply(lambda x:clean_tweet(x))
    return data_df

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
        display_df[c].plot(kind='barh', ax=axes[i], figsize=(10,6))
        axes[i].set_title(c, pad=20)
        axes[i].title.set_color('red')
        axes[i].title.set_size(14)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
          
def main():
    global No_of_col_in_csv
    global filename
    # import the hosts list
    analysis_df=load_analysis_data('hosts_2013.csv')
    filename='hosts_2013'
    No_of_col_in_csv=len(analysis_df.columns)
    analysis_df['Title']=analysis_df['Hosts']
    # import twitter data
    tweets=load_tweet('../data/gg2013.json')
    #calculate and plot sentiment analysis
    strong_pos,pos,weak_pos,neutral,weak_neg,neg,strong_neg,no_of_tweets=sentiment_analysis(analysis_df['Hosts'],tweets)
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




