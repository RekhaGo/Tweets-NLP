import json
from nltk.corpus import stopwords
import csv
import re
import nltk

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
        tweet = re.sub(r'[^\w\'\#\@\s]', '', tweet)
        tweets.append(re.findall(r"[\w\#\@']+", tweet))
        # tweets.append(tweet.split(' '))
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
        # filtered = [w for w in tweet if w in words]

        filtered_sentences.append(filtered)
    print(filtered_sentences[:10])
    return filtered_sentences



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




def main():
    '''
        The loading of tweets takes a while, so writing it to cleaned.csv to read from
        after processing. REMOVE after development or if modifying preprocessing
        TODO
    '''

    tweets = load_data('../data/gg2015.json')
    cleaned_tweets = clean(tweets) #list of list of words that compose the phrase
    print(len(cleaned_tweets))
    '''
        Writing preprocessed data to file
        Comment below before turn-in
        TODO
    '''
    with open('cleaned.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_tweets)


    '''
        reading preprocessed data from file
    '''
    # cleaned_tweets = []
    # with open('cleaned.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     cleaned_tweets = list(reader)


    #hello host_branch
    #converted host context counting to general word counting and context based selection
    calculate_words(cleaned_tweets, ['hosts', 'host'], 0.26)
    # names_dic = calculate_words(cleaned_tweets, ['award', 'awards', 'best'], 0.009)


if __name__ == '__main__':
    main()
