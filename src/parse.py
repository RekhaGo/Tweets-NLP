import json
from nltk.corpus import stopwords
import csv
import re
import nltk
from collections import Counter
from math import floor, ceil

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
        tweet = line['text']
        # tweet = line['text'].lower()
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
    words.add("-")
    stopWords = create_stop_words()
    for tweet in tweets:

        #filtered = [w for w in tweet if not w in stopWords]
        filtered = [w for w in tweet if w in words]

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

def ngram_freq(tweets, word_list, alpha, beta = 10000):
    ngrams = [list(nltk.ngrams(tweet,9)) for tweet in tweets]

    word_selection=[]
    dict_names = dict()
    num_tweets_with_word=0
    for tweet_b, tweet in zip(ngrams, tweets):
        if any(word in tweet for word in word_list):
            if not 'next' in tweet:
                num_tweets_with_word +=1
                for bg in tweet_b:
                    pot_name = bg
                    # print(pot_name)
                    if pot_name in dict_names:
                        dict_names[pot_name] +=1
                    else:
                        dict_names[pot_name] = 1

    magic_constant1 = alpha*num_tweets_with_word #TODO take another look at this.
    magic_constant2 = beta*num_tweets_with_word
    for key, val in dict_names.items():
        if val > magic_constant1 and val < magic_constant2:
            # host_selection.append(str(key) + str(val))
            word_selection.append(str(key).replace('_',' '))

    print(num_tweets_with_word)
    print(word_list, word_selection)
    return dict_names

def reg_chunker(tweets):

    patterns = """
                 INNER: {<NN><NN>*?<IN><DT><NN><IN><DT><NN|NNS|JJ><NN>*?<CC>?<NN|NNS|JJ>?<NN>*?<ORSCON>*}
                 ORSCON: {<NN|JJ><NN>*<CC><NN|JJ><NN>*}
                 CHUNK: {<RBS|JJS><INNER><NN|ORSCON>?}
                 SHRTCHK: {<RBS|JJS><NN|JJ><NN>+<NN|ORSCON>}
    #            """


    parser = nltk.RegexpParser(patterns)
    trees = []
    keywords = {'best','performance', 'motion', 'television', 'series', 'music', 'artist', 'film', 'actor', 'actress', 'musical',
                'comedy', 'album', 'lead', 'director', 'original', 'language', 'foreign', 'actress', 'actor', 'singer', 'musician', 'feature',
                'award', 'awards', 'drama', 'supporting'}
    n_total = 0
    tot_tweets = len(tweets)
    for i,tweet in enumerate(tweets):
        perc = (float(i)/tot_tweets)*100
        if i%100000.0 == 0:
            print (str(perc) + '% Complete')
        if any(key in tweet for key in keywords):
            tweet = list(filter(lambda a: a != '-', tweet))
            if len(nltk.pos_tag(tweet))!=0:
                tree = parser.parse(nltk.pos_tag(tweet))
                for subtree in tree.subtrees():
                    if subtree.label() == 'CHUNK' or subtree.label() == 'SHRTCHK' or subtree.label() == 'CHUNKNP':
                        n_total += 1
                        trees.append(subtree)

    occ = Counter([' '.join([x[0] for x in tree.leaves()]).replace('HYP ','') for tree in trees])

    num = 0
    awards = []
    for key, val in occ.items():
        p_sc = 0
        for word in keywords:
            if word in key.split():
                occ[key] *= 2
        for word in key.split():
            if word not in keywords:
                if occ[key] > 0:
                    occ[key] /= 2
    n_total = sum(occ.values())
    nummer = ceil(n_total*0.002)
    print ("Num thresh: " + str(nummer) + " Total: " + str(n_total))
    for key,val in occ.items():
        if occ[key] > nummer:
            awards.append(key)

    print (len(awards))
    return awards

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
        print("Getting Cleaned Tweets.....")
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

def get_awards(year):
    return reg_chunker(get_cleaned_tweets(year))

def main():
    '''
        The loading of tweets takes a while, so writing it to cleaned.csv to read from
        after processing. REMOVE after development or if modifying preprocessing
        TODO
    '''
    # write_file([2015])
    # tweets = get_cleaned_tweets(2013)

    '''
    Getting the Hosts
    '''

    # with open('cleaned.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(cleaned_tweets)
    # #

    '''
        reading preprocessed data from file
    '''
    # cleaned_tweets = []
    # with open('cleaned.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     cleaned_tweets = list(reader)
    # write_file([2013])

    #hello award branch
    #converted host context counting to general word counting and context based selection
    #calculate_words(cleaned_tweets, ['hosts', 'host'], 0.26)
    # names_dic = calculate_words(cleaned_tweets, ['award', 'awards', 'best'], 0.09)
    # ngram_freq(cleaned_tweets, ['award', 'awards', 'best'], 0.004, 0.01)
    # reg_chunker(get_cleaned_tweets(2015))


    # res = get_hosts(2013)
    # print(res)
    # res = get_hosts(2013)
    # print(res)
    # awards = get_clean_awards()
    # print(awards)





    # tweets = get_cleaned_tweets(2013)

    # for tweet in tweets:
        # if any('best' in word for word in tweet):
            # print(tweet)



if __name__ == '__main__':
    main()
