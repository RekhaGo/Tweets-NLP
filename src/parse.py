from nltk.corpus import stopwords
import csv
import re
import nltk
from collections import Counter
from math import floor, ceil
import os.path
import json
import time
import numpy as np

import small_helper_methods


'''
Libraries Needed:

from nltk, averaged_perceptron_tagger





'''



# LIST_OF_AWARDS = ['best screenplay - motion picture', 'best director - motion picture', 'best performance by an actress in a television series - comedy or musical', 'best foreign language film', 'best performance by an actor in a supporting role in a motion picture', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best mini-series or motion picture made for television', 'best original score - motion picture', 'best performance by an actress in a television series - drama', 'best performance by an actress in a motion picture - drama', 'cecil b. demille award', 'best performance by an actor in a motion picture - comedy or musical', 'best motion picture - drama', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a motion picture', 'best television series - drama', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best animated feature film', 'best original song - motion picture', 'best performance by an actor in a motion picture - drama', 'best television series - comedy or musical', 'best performance by an actor in a television series - drama', 'best performance by an actor in a television series - comedy or musical']



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


def write_file(lst_of_years):
    for val in lst_of_years:
        print('Writing data to file from year: ' + val)
        tweets = load_data('gg' + str(val) + '.json')
        cleaned_tweets_grammar = clean_grammar(tweets)  # list of list of words that compose the phrase
        cleaned_tweets_stopwords = clean_stopwords(tweets)  # list of list of words that compose the phrase
        '''
            Writing preprocessed data to file
            Comment below before turn-in
            TODO
        '''
        with open('cleaned_grammar_' + str(val) + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_tweets_grammar)
        with open('cleaned_stopwords_' + str(val) + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_tweets_stopwords)

def get_cleaned_tweets(year, grammar_or_stopwords):
    '''
    args for grammar_or_stopwords
    'grammar'
    'stopwords'
    '''
    try:
        with open('cleaned_'+str(grammar_or_stopwords)+'_' + str(year) + '.csv', 'r') as f:
            reader = csv.reader(f)
            cleaned_tweets = list(reader)
        return cleaned_tweets
    except:
        print("FILE NOT FOUND ERROR reading tweets from file "+'cleaned_'+str(grammar_or_stopwords)+'_' + str(year) + '.csv')

def clean_grammar(tweets):
    '''
        Filters out stop words
        - can take other logic here
    '''
    filtered_sentences = []
    words = set(nltk.corpus.words.words())
    words.add("-")
    for tweet in tweets:
        filtered = [w for w in tweet if w in words]
        filtered_sentences.append(filtered)
    return filtered_sentences

def clean_stopwords(tweets):
    '''
        Filters out stop words
        - can take other logic here
    '''
    filtered_sentences = []
    stopWords = create_stop_words()
    for tweet in tweets:
        filtered = []
        for word in tweet:
            upWord = word.lower()
            if upWord not in stopWords and not re.search('@', upWord):
                filtered.append(upWord)
        # filtered = [w.lower() for w in tweet.lower() if not w in stopWords]
        filtered_sentences.append(filtered)
    return filtered_sentences

# def get_clean_awards():
#     awards = []
#     stopwords = create_stop_words()
#     for award in LIST_OF_AWARDS:
#         filtered = [w for w in award if not w in stopwords]
#         awards.append(filtered)
#     return awards

def create_stop_words():
    '''
        Creating words to filter by
    '''
    stopWords = set(stopwords.words('english'))
    stopWords.add('rt')
    stopWords.add('@ew')
    stopWords.add('golden')
    stopWords.add('globe')
    stopWords.add('#goldenglobes')
    return stopWords

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

    # print(num_tweets_with_word)
    # print(word_list, word_selection)
    return dict_names

def reg_chunker(tweets):
    patterns = """
                 INNER: {<NN><NN>*?<IN><DT><NN><IN><DT><NN|NNS|JJ><NN>*?<CC>?<NN|NNS|JJ>?<NN>*?<ORSCON>*}
                 ORSCON: {<NN|JJ><NN>*<CC><NN|JJ><NN>*}
                 CHUNK: {<RBS|JJS><INNER><NN|ORSCON>?}
                 SHRTCHK: {<RBS|JJS><NN|JJ><NN>+<NN|ORSCON>}
               """


    parser = nltk.RegexpParser(patterns)
    trees = []
    np.random.shuffle(tweets)
    keywords = {'best','performance', 'motion', 'television', 'series', 'music', 'artist', 'film', 'actor', 'actress', 'musical',
                'comedy', 'album', 'lead', 'director', 'original', 'language', 'foreign', 'actress', 'actor', 'singer', 'musician', 'feature',
                'award', 'awards', 'drama', 'supporting'}
    n_total = 0
    # tot_tweets = len(tweets[:len(tweets)/2])

    for tweet in tweets[:int(len(tweets)/2)]:
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
    # print ("Num thresh: " + str(nummer) + " Total: " + str(n_total))
    for key,val in occ.items():
        if occ[key] > nummer:
            awards.append(key)
            # print (key)

    # print (len(awards))
    return awards



def get_awards(year):
    start = time.time()
    result = reg_chunker(get_cleaned_tweets(year, 'grammar'))
    end = time.time()
    print('awards time: {0:.2f}s for {1}'.format(end - start, year))
    return result


def tweet_contains_word(tweet, lst_of_keywords):
    if any(word in tweet for word in lst_of_keywords):
        return True
    return False

def tweet_contains_all_words(tweet, lst_of_keywords):
    if all(word in tweet for word in lst_of_keywords):
        return True
    return False

def filter_word_in_list(award, stop_words):
    for word in stop_words:
        award = re.sub(word, ' ', award)
    return award


def get_hardcoded_awards(year): #TODO compiling regex to possibly make it faster??
    stop_words = [' or ', ' in ', ' a ', ' made ', ' for ']
    clean_awards = []

    if year in ['2013', '2015']:
        LIST_OF_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    else:
        LIST_OF_AWARDS = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

    for award in LIST_OF_AWARDS:
        award = re.sub('^best .+ an\s', '', award)
        award = re.sub('best ', '', award)
        award = re.sub('television series', 'tv series', award)
        award = re.sub('television', 'tv', award)
        award = re.sub('in a ', '', award)
        award = re.sub('role ', '', award)
        award = re.sub('series, mini-series ', '', award)
        award = re.sub('mini-series or motion picture made for tv', 'mini-seriestv', award)
        award = re.sub('cecil b. demille ', 'demille ', award)
        award = re.sub('or motion picture made for tv', 'tv', award)
        award = filter_word_in_list(award, stop_words)
        clean_awards.append(award)
    return clean_awards

def list_of_awards_by_year(year):
    if year in ['2013', '2015']:
        LIST_OF_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    else:
        LIST_OF_AWARDS = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
    return LIST_OF_AWARDS


def get_HARDCODED_AWARD_DATA(year): #TODO do not use in final product.
    json_data = json.loads(open('gg'+year+'answers.json').read())
    return json_data['award_data']

def match_movie(look_phrase_str):
    movie_key_words = ['screenplay', 'film', 'pictures', 'picture', 'score', 'song', 'series', 'theme']
    for word in movie_key_words:
        if re.search(word, look_phrase_str):
            if not match_person(look_phrase_str):
                return True
    return False

def match_person(look_phrase_str):
    movie_key_words = ['director', 'actor', 'actress', 'demille']
    for word in movie_key_words:
        if re.search(word, look_phrase_str):
            return True
    return False

def remove_words_from_tweet(tweet, lst):
    filtered = []
    for word in tweet:
        if not any([re.search(val, word) for val in lst]):
            filtered.append(word)
    return filtered

def compute_bigram_hosts(year, any_filter_word, alpha):
    hosts = []
    dict_names = dict()
    cleaned_tweets = get_cleaned_tweets(year, 'stopwords')
    num_tweets_with_word = 0
    for tweet in cleaned_tweets:
        if any(re.search(any_filter_word, word) for word in tweet):
            if not 'next' in tweet:
                # print(tweet)
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
    magic_constant = alpha * num_tweets_with_word
    for key, val in dict_names.items():
        if val > magic_constant:
            # hosts.append(str(key) + str(val))
            hosts.append(str(key).replace('_', ' '))
    return hosts

def get_hosts(year):
    small_helper_methods.get_kb_actors()
    return compute_bigram_hosts(year, 'host', .28)

def update_look_phrase(look_phrase):
    if match_person(look_phrase[0]):
        if len(look_phrase) > 1:
            look_phrase[0] = look_phrase[0] + ' ' + look_phrase[1].split(' ')[0]
    else:
        if len(look_phrase) > 1:
            # print(look_phrase)
            if re.search('comedy', look_phrase[1]):
                look_phrase[0] = look_phrase[0] + ' ' + look_phrase[1].split(' ')[0]
            else:
                if not re.search('motion', look_phrase[1]):
                    look_phrase[0] = look_phrase[0] + ' ' + look_phrase[1]
    return look_phrase

def verify_answer_by_look_phrase_type(look_phrase, pot_winners, kb_movies, kb_actors):
    winners = []
    if match_movie(look_phrase[0]):
        # print('&*', pot_winners)
        for candidate in pot_winners:
            if candidate not in look_phrase[0].split(' ') and candidate not in {'motion', 'picture', 'winner', 'best',
                                                                                'wins', 'won', 'actor', 'actress',
                                                                                'comedy', 'musical', '-'}:
                lst = [movie for movie in kb_movies if re.search(candidate + ' ', movie)]
                # print('cand:', candidate, lst)
                if (len(lst) < 1):
                    lst = []
                    for movie in kb_movies:
                        if re.search(candidate, movie):
                            if len(movie.split(' ')) < 2:
                                lst.append(movie)
                if len(lst) > 0 and len(lst) < 5:
                    winners.append(lst)
                else:
                    lst = []
                    for movie in kb_movies:
                        if re.search(candidate, movie):
                            if len(movie.split(' ')) < 2:
                                lst.append(movie)
                    if len(lst) > 0 and len(lst) < 5:

                        winners.append(lst)
                    else:
                        lst = []
                        for movie in kb_movies:
                            if re.search(' ' + candidate, movie):
                                lst.append(movie)
                        if len(lst) > 0 and len(lst) < 5:
                            winners.append(lst)
                if len(winners) < 1:
                    lst.append(candidate)
                    lst = [w for w in lst if w in kb_movies]
                    if len(lst) > 0 and len(lst) < 5:
                        # print('candidate:', candidate, lst)
                        winners.append([w for w in lst if w in kb_movies])
    if match_person(look_phrase[0]):
        # print('&*', pot_winners)
        for j in range(len(pot_winners)):
            cand = pot_winners[j]
            if cand not in ['best', 'drama', 'actor', 'actress', 'cecil']:
                lst = [movie for movie in kb_actors if re.search(cand + ' ', movie)]
                # print('candidate:', cand, lst)
                if len(lst) < 1:
                    lst = [movie for movie in kb_actors if re.search(cand, movie)]
                # print(cand+'   ---list: ' ,lst)
                counter = j
                while len(lst) > 0:
                    if (counter < len(pot_winners) - 1):
                        cand += (' ' + pot_winners[counter + 1])
                        child_lst = [movie for movie in kb_actors if re.search(cand, movie)]
                        # print('candidate child:', cand, lst)
                        if (len(child_lst) > 0):
                            lst = child_lst
                        counter += 1
                    else:
                        break
                if len(lst) > 0 and len(lst) < 6:
                    winners.append(lst)
    return winners

def get_nominees_helper(all_awards, tweets, ACTUAL_AWARDS):
    kb_actors = small_helper_methods.get_kb_actors()
    kb_movies = small_helper_methods.get_kb_movies()
    # print(type(kb_actors))
    json_data = get_HARDCODED_AWARD_DATA('2013')

    selected_winners = dict()
    for idx in range(int(len(all_awards))):
        look_phrase = all_awards[idx].split(' - ')
        dict_names = dict()
        pot_winners = set()
        winners = []
        # print('-look_phrase: ', look_phrase)
        # look_phrase = update_look_phrase(look_phrase)
        # print('look_phrase: ', look_phrase)
        num_tweets_with_word = 0
        for tweet in tweets:
            if tweet_contains_all_words(tweet, look_phrase[0].split(' ')):
                if any([re.search('nomin', val) for val in tweet]):
                    tweet = remove_words_from_tweet(tweet, ['-'])
                    num_tweets_with_word += 1
                    # print('tweet: ', tweet)
                    if match_person(look_phrase[0]):
                        for i in range(len(tweet) - 1):
                            # pot_name = tweet[i]
                            pot_name = tweet[i] + ' ' + tweet[i + 1]
                            # print(pot_name)
                            if pot_name in dict_names:
                                dict_names[pot_name] += 1
                            else:
                                dict_names[pot_name] = 1
                                # num_tweets_with_word = 0
                    else:
                        for i in range(len(tweet)-1):
                            pot_name = tweet[i]
                            # pot_name = tweet[i] + ' ' + tweet[i + 1]
                            # print(pot_name)
                            if pot_name in dict_names:
                                dict_names[pot_name] += 1
                            else:
                                dict_names[pot_name] = 1
                                # num_tweets_with_word = 0
        magic_constant = .90* num_tweets_with_word
        # print('-----------look_phrase{}'.format(look_phrase))
        for key, val in dict_names.items():
            if match_person(look_phrase[0]):
                if key in kb_actors:
                    pot_winners.add(key)
            else:
                if val > magic_constant:
                    for item in kb_movies:
                        if not re.search('\d', item):
                            if re.search(key.split(' ')[0]+' ', item):
                            # if re.search(key.split(' ')[1], item):
                                # print('key matched: ', key)
                                pot_winners.add(item)
            # if match_movie(look_phrase[0]):
        winners = pot_winners
        # print('#winners: ', winners)
        # print('#Actual_nominees: ', json_data[LIST_OF_AWARDS[idx]]['nominees'])


        # print(winners)
        # if len(winners) > 0:
        #     print('potential nominees: ', pot_winners)
        #     print(winners)
        #     print('# Winners: ', winners)
        #     print('Actual_nominees: ', json_data[LIST_OF_AWARDS[idx]]['nominees'])
        # else:
        #     print("FAILED#$")
        #     print('Actual_nominees: ', json_data[LIST_OF_AWARDS[idx]]['nominees'])
        winners = [win for win in winners]
        # print(winners)
        if len(winners) > 0:
            selected_winners[ACTUAL_AWARDS[idx]] = winners
        else:
            selected_winners[ACTUAL_AWARDS[idx]] = ['a']
    return selected_winners


def updated_presenter(all_awards, tweets, calc_winners, ACTUAL_AWARDS):
    kb_actors = small_helper_methods.get_kb_actors()
    results_dict = dict()
    selected_winners = dict()
    for idx in range(int(len(all_awards))):
        dict_names = dict()
        pot_winners = set()
        winner = calc_winners[ACTUAL_AWARDS[idx]]
        look_phrase = all_awards[idx].split(' - ')
        num_tweets_with_word = 0
        winner_first_name = winner.split(' ')[0]
        for tweet in tweets:
            # if tweet_contains_all_words(tweet, look_phrase[0].split(' ')):
            if winner_first_name in tweet:
                if any([re.search('present', val) for val in tweet]):
                    num_tweets_with_word += 1
                    for i in range(len(tweet)-1):
                        pot_name = tweet[i] + ' ' + tweet[i + 1]
                        if pot_name in kb_actors:
                            if pot_name in dict_names:
                                dict_names[pot_name] += 1
                            else:
                                dict_names[pot_name] = 1

        magic_constant = 0.0 * num_tweets_with_word
        for key, val in dict_names.items():
            if val > magic_constant:
                    pot_winners.add(key)
        winners = [win for win in pot_winners]
        if len(winners) > 0:
            selected_winners[ACTUAL_AWARDS[idx]] = winners
        else:
            selected_winners[ACTUAL_AWARDS[idx]] = ['']
    return selected_winners


def get_winner_helper(all_awards, tweets, ACTUAL_AWARDS):
    #TODO take out parentheses of winners
    kb_actors = small_helper_methods.get_kb_actors()
    kb_movies = small_helper_methods.get_kb_movies()
    json_data = get_HARDCODED_AWARD_DATA('2013')
    selected_winners = dict()

    for idx in range(int(len(all_awards))):
        look_phrase = all_awards[idx].split(' - ')
        results = dict()
        dict_names = dict()
        pot_winners = []
        winners = []

        if match_person(look_phrase[0]):
            if len(look_phrase) > 1:
                look_phrase[0] = look_phrase[0] +' '+look_phrase[1].split(' ')[0]
        else:
            if len(look_phrase) > 1:
                # print(look_phrase)
                if re.search('comedy', look_phrase[1]):
                    look_phrase[0] = look_phrase[0] + ' ' + look_phrase[1].split(' ')[0]
                else:
                    if not re.search('motion', look_phrase[1]):
                        look_phrase[0] = look_phrase[0] + ' ' + look_phrase[1]
        #
        # print('--------------!---------------------------------------------------------')
        #
        #
        # print(LIST_OF_AWARDS[idx])
        # # print(len(look_phrase))
        # print(look_phrase[0])

        num_tweets_with_word = 0
        for tweet in tweets:
            if tweet_contains_all_words(tweet, look_phrase[0].split(' ')):
                if tweet_contains_word(tweet, ['wins', 'winner', 'won']):
                    num_tweets_with_word += 1
                    for i in range(len(tweet) - 1): #TODO remove this -1 and check acc again :P
                        pot_name = tweet[i]
                        # print(pot_name)
                        if pot_name in dict_names:
                            dict_names[pot_name] += 1
                        else:
                            dict_names[pot_name] = 1
        magic_constant = .28 * num_tweets_with_word
        for key, val in dict_names.items():
            if val > magic_constant:
                # winners.append(str(key) + str(val))
                pot_winners.append(str(key).replace('_', ' '))
        if match_movie(look_phrase[0]):
            # print('&*', pot_winners)
            for candidate in pot_winners:
                if candidate not in look_phrase[0].split(' ') and candidate not in {'motion', 'picture','winner','best', 'wins', 'won', 'actor','actress', 'comedy', 'musical', '-'}:

                    lst = [movie for movie in kb_movies if re.search(candidate + ' ', movie)]
                    # print('cand:', candidate, lst)
                    if (len(lst) < 1):
                        lst= []
                        for movie in kb_movies:
                            if re.search(candidate, movie):
                                if len(movie.split(' ')) < 2:
                                    lst.append(movie)
                    if len(lst) > 0 and len(lst) < 5:

                        winners.append(lst)
                    else:
                        lst = []
                        for movie in kb_movies:
                            if re.search(candidate, movie):
                                if len(movie.split(' ')) < 2:
                                    lst.append(movie)
                        if len(lst) > 0 and len(lst) < 5:

                            winners.append(lst)
                        else:
                            lst = []
                            for movie in kb_movies:
                                if re.search(' '+candidate, movie):
                                    lst.append(movie)
                            if len(lst) > 0 and len(lst) < 5:

                                winners.append(lst)
                    if len(winners) < 1:
                        lst.append(candidate)
                        lst = [w for w in lst if w in kb_movies]
                        if len(lst) > 0 and len(lst) < 5:
                            # print('candidate:', candidate, lst)
                            winners.append([w for w in lst if w in kb_movies])
        if match_person(look_phrase[0]):
            # print('&*', pot_winners)
            for j in range(len(pot_winners)):
                cand = pot_winners[j]
                if cand not in ['best', 'drama', 'actor', 'actress', 'cecil']:
                    lst = [movie for movie in kb_actors if re.search(cand+' ', movie)]
                    # print('candidate:', cand, lst)
                    if len(lst) < 1 :
                        lst = [movie for movie in kb_actors if re.search(cand, movie)]
                    # print(cand+'   ---list: ' ,lst)
                    counter = j
                    while len(lst) > 0:
                        if (counter < len(pot_winners)-1):
                            cand += (' '+pot_winners[counter+1])
                            child_lst = [movie for movie in kb_actors if re.search(cand, movie)]
                            # print('candidate child:', cand, lst)
                            if (len(child_lst) > 0):
                                lst = child_lst
                            counter+=1
                        else:
                            break
                    if len(lst) > 0 and len(lst) < 6:
                        winners.append(lst)
        # if len(winners) > 0:
        #     print('potential winners: ',pot_winners)
        #     print(winners)
        #     print('# Winners: ', winners[0][0])
        #     print('Actual_winner: ', json_data[LIST_OF_AWARDS[idx]]['winner'] )
        # else:
        #     print("FAILED#$")
        #     print('Actual_winner: ', json_data[LIST_OF_AWARDS[idx]]['winner'])
        if len(winners) > 0:
            # print(winners[0][0].split('(')[0])
            selected_winners[ACTUAL_AWARDS[idx]] = winners[0][0]
        else:
            selected_winners[ACTUAL_AWARDS[idx]] = ' '
    # print(selected_winners)
    return selected_winners

def get_winner(year):
    start = time.time()
    if os.path.isfile('calculated_winners'+year+'.json'):
        print('loading cached calculated winners')
        f = open('calculated_winners'+year+'.json', 'r')
        selected_winners = json.load(f)
        f.close()
    else:
        print('running get_winner and caching')

        tweets = get_cleaned_tweets(year, 'stopwords')
        hardcoded_awards = get_hardcoded_awards(year)
        actual_awards = list_of_awards_by_year(year)
        selected_winners = get_winner_helper(hardcoded_awards, tweets, actual_awards)
        cach_start = time.time()
        json_data = json.dumps(selected_winners)
        f = open('calculated_winners'+year+'.json', "w")
        f.write(json_data)
        f.close()
        print('get_winner caching : {0:.2f}seconds'.format( time.time() - cach_start))
    end = time.time()
    print('Total get_winner method call : {0:.2f}seconds'.format(end - start))
    return selected_winners

def get_presenter(year):
    start = time.time()
    tweets = get_cleaned_tweets(year, 'stopwords')
    hardcoded_awards = get_hardcoded_awards(year)
    actual_awards = list_of_awards_by_year(year)
    selected_winners = get_winner(year)
    # result = get_presenter_helper(hardcoded_awards, tweets, selected_winners)
    result = updated_presenter(hardcoded_awards, tweets, selected_winners, actual_awards)
    end = time.time()
    print('Presenters : {0:.2f} seconds for {1}'.format(end - start, year))
    return result
    # return longer_get_presenters(hardcoded_awards, tweets)

def get_nominee(year):
    start = time.time()
    tweets = get_cleaned_tweets(year, 'stopwords')
    hardcoded_awards = get_hardcoded_awards(year)
    actual_awards = list_of_awards_by_year(year)
    result = get_nominees_helper(hardcoded_awards, tweets, actual_awards)
    for key,val in result.items():
        print(key,val)

    end = time.time()
    print('Nominees : {0:.2f} seconds for {1}'.format(end - start, year))
    return result

def main():
    '''
        The loading of tweets takes a while, so writing it to cleaned.csv to read from
        after processing. REMOVE after development or if modifying preprocessing
        TODO
    '''
    # write_file(['2013'])
    # start = time.time()
    # tweets = get_cleaned_tweets('2013', 'stopwords')
    # print(len(tweets))
    # end = time.time()
    # print('reading tweets from file : {0:.2f} seconds for {1}'.format(end - start, '2013'))
    # for tweet in get_cleaned_tweets('2013', 'stopwords'):
    #     if 'cooper' in tweet:
    #         print(tweet)

if __name__ == '__main__':
    main()
