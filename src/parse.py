import json
from nltk.corpus import stopwords
import csv
import re
import nltk


LIST_OF_AWARDS = ['best screenplay - motion picture', 'best director - motion picture', 'best performance by an actress in a television series - comedy or musical', 'best foreign language film', 'best performance by an actor in a supporting role in a motion picture', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best mini-series or motion picture made for television', 'best original score - motion picture', 'best performance by an actress in a television series - drama', 'best performance by an actress in a motion picture - drama', 'cecil b. demille award', 'best performance by an actor in a motion picture - comedy or musical', 'best motion picture - drama', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a motion picture', 'best television series - drama', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best animated feature film', 'best original song - motion picture', 'best performance by an actor in a motion picture - drama', 'best television series - comedy or musical', 'best performance by an actor in a television series - drama', 'best performance by an actor in a television series - comedy or musical']

def load_data(filename):
    '''
        Load data from json
        Added in regex preprocessing for cleaning and tokenizing
    '''
    print('loading dataset : ',filename)
    json_data = json.loads(open(filename).read())
    tweets = []
    for line in json_data:
        tweet = line['text'].lower()
        tweet = re.sub(r'[^\w\'\#\@\s\-]', '', tweet)
        tweets.append(re.findall(r"[\w\#\@\-']+", tweet))
    return tweets

def clean(tweets):
    '''
        Filters out stop words
        - can take other logic here
    '''
    print('cleaning data...')
    filtered_sentences = []
    #removing stop words from nltk corpus
    words = set(nltk.corpus.words.words())
    stopWords = create_stop_words()
    for tweet in tweets:
        filtered = [w for w in tweet if not w in stopWords]
        filtered_sentences.append(filtered)
    print(filtered_sentences[:10])
    return filtered_sentences

def get_clean_awards():
    awards = []
    stopwords = create_stop_words()
    for award in LIST_OF_AWARDS:
        filtered = [w for w in award if not w in stopwords]
        awards.append(filtered)
    return awards

def create_stop_words():
    '''
        Creating words to filter by
    '''
    stopWords = set(stopwords.words('english'))
    stopWords.add('rt')
    stopWords.add('@ew')
    return stopWords



def print_tweets(tweets, num_tweets):
    '''
        Print helper for tweets, pass in tweets and number to display
        print_tweets(cleaned_tweets, 3)
    '''

    for i in range(num_tweets):
        print(tweets[i])

'''function to find most common (fraction = alpha) word-pair associations with respect to a particular word word_list
    Arguments:
        tweets: list of tweets, word_list: list of words, alpha: fraction of count to be selected
        returns: nothing
'''
def calculate_words(tweets, word_list, alpha):
    word_selection = []
    dict_names = dict()

    #Determining a good magic constant
    num_tweets_with_word = 0

    for tweet in tweets:
        if any(word in tweet for word in word_list):
            if not 'next' in tweet:
                num_tweets_with_word +=1
                for i in range(len(tweet)-1):
                    pot_name = tweet[i]+'_'+tweet[i+1]
                    # print(pot_name)
                    if pot_name in dict_names:
                        dict_names[pot_name] +=1
                    else:
                        dict_names[pot_name] = 1
    '''
        Magic constant below is calculated as a percentage of total tweets, since 2015 is
        much larger than 2013...
    '''
    magic_constant = alpha*num_tweets_with_word #TODO take another look at this.
    for key, val in dict_names.items():
        if val > magic_constant:
            # host_selection.append(str(key) + str(val))
            word_selection.append(str(key).replace('_',' '))

    #CAUTION: with alpha to regulate size of word selection
    print(num_tweets_with_word)
    print(word_list, word_selection)
    return dict_names

def write_file(lst_of_years):
    for val in lst_of_years:
        tweets = load_data('../data/gg'+str(val)+'.json')
        cleaned_tweets = clean(tweets) #list of list of words that compose the phrase
        print(len(cleaned_tweets))
        '''
            Writing preprocessed data to file
            Comment below before turn-in
            TODO
        '''
        with open('cleaned'+str(val)+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_tweets)
def get_cleaned_tweets(year):
    cleaned_tweets = []
    with open('cleaned'+str(year)+'.csv', 'r') as f:
        reader = csv.reader(f)
        cleaned_tweets = list(reader)
    return cleaned_tweets




def get_hosts(year):
    cleaned_tweets = get_cleaned_tweets(year)
    word_list = ['hosts', 'host', 'hosting']
    hosts = []
    dict_names = dict()

    # Determining a good magic constant
    num_tweets_with_word = 0

    for tweet in cleaned_tweets:
        if any(word in tweet for word in word_list):
            if not 'next' in tweet:
                num_tweets_with_word += 1
                for i in range(len(tweet) - 1):
                    pot_name = tweet[i] + '_' + tweet[i + 1]
                    # print(pot_name)
                    if pot_name in dict_names:
                        dict_names[pot_name] += 1
                    else:
                        dict_names[pot_name] = 1
    '''
        Magic constant below is calculated as a percentage of total tweets, since 2015 is
        much larger than 2013...
    '''
    magic_constant = .28 * num_tweets_with_word
    for key, val in dict_names.items():
        if val > magic_constant:
            # hosts.append(str(key) + str(val))
            hosts.append(str(key).replace('_', ' '))
    return hosts

def main():
    '''
        The loading of tweets takes a while, so writing it to cleaned.csv to read from
        after processing. REMOVE after development or if modifying preprocessing
        TODO
    '''
    # write_file([2013]);
    # tweets = get_cleaned_tweets(2013)

    '''
    Getting the Hosts
    '''
    # res = get_hosts(2013)
    # print(res)
    awards = get_clean_awards()
    print(awards)





    tweets = get_cleaned_tweets(2013)

    # for tweet in tweets:
        # if any('best' in word for word in tweet):
            # print(tweet)


if __name__ == '__main__':
    main()
