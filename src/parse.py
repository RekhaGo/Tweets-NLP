import json
from nltk.corpus import stopwords
import csv


def load_data(filename):
    '''
        Load data from json
    '''
    print('loading dataset : ',filename)
    json_data = json.loads(open(filename).read())
    tweets = []
    for line in json_data:
        tweet = line['text'].lower()
        tweets.append(tweet.split(' '))
    return tweets



def clean(tweets):
    '''
        Filters out stop words
        - can take other logic here
    '''
    print('cleaning data...')
    filtered_sentences = []
    #removing stop words from nltk corpus
    stopWords = create_stop_words()
    for tweet in tweets:
        filtered = [w for w in tweet if not w in stopWords]
        filtered_sentences.append(filtered)
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

def calculate_hosts(tweets):
    host_selection = []
    dict_names = dict()

    #Determining a good magic constant
    num_tweets_with_host = 0

    for tweet in tweets:
        if 'host' in tweet or 'hosts' in tweet:
            if not 'next' in tweet:
                num_tweets_with_host +=1
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
    magic_constant = .26*num_tweets_with_host #TODO take another look at this.
    for key, val in dict_names.items():
        if val > magic_constant:
            # host_selection.append(str(key) + str(val))
            host_selection.append(str(key).replace('_',' '))

    # print(num_tweets_with_host)
    print('Hosts: ', host_selection)






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
    # with open('cleaned.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(cleaned_tweets)


    '''
        reading preprocessed data from file
    '''
    # cleaned_tweets = []
    # with open('cleaned.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     cleaned_tweets = list(reader)




    calculate_hosts(cleaned_tweets)




if __name__ == '__main__':
    main()