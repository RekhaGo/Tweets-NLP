import json
from nltk.corpus import stopwords
import csv
import re
import nltk
from scipy._lib.decorator import getfullargspec

from src import small_helper_methods as smh
from src import KBLoader


LIST_OF_AWARDS = ['best screenplay - motion picture', 'best director - motion picture', 'best performance by an actress in a television series - comedy or musical', 'best foreign language film', 'best performance by an actor in a supporting role in a motion picture', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best mini-series or motion picture made for television', 'best original score - motion picture', 'best performance by an actress in a television series - drama', 'best performance by an actress in a motion picture - drama', 'cecil b. demille award', 'best performance by an actor in a motion picture - comedy or musical', 'best motion picture - drama', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a motion picture', 'best television series - drama', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best animated feature film', 'best original song - motion picture', 'best performance by an actor in a motion picture - drama', 'best television series - comedy or musical', 'best performance by an actor in a television series - drama', 'best performance by an actor in a television series - comedy or musical']

def get_kb_movies():
    with open('kb_movies.txt', 'r') as filehandle:
        movies = []
        for line in filehandle:
            movies.append(line[:-1])
    return movies

def get_kb_actors():
    with open('kb_actors.txt', 'r') as filehandle:
        movies = []
        for line in filehandle:
            movies.append(line[:-1])
    return movies

def get_kb_directors():
    with open('kb_directors.txt', 'r') as filehandle:
        movies = []
        for line in filehandle:
            movies.append(line[:-1])
    return movies







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
    stopWords.add('golden')
    stopWords.add('globe')
    stopWords.add('#goldenglobes')

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

def get_nominees(year):
    pass



def subrat_get_presenters():
    pass

def tweet_contains_word(tweet, lst_of_keywords):
    if any(word in tweet for word in lst_of_keywords):
        return True
    return False
def tweet_contains_all_words(tweet, lst_of_keywords):
    # print('list of key words: ', lst_of_keywords)


    if all(word in tweet for word in lst_of_keywords):
        return True
    return False

def filter_word_in_list(award, stop_words):
    # lst_of_words= award.split(" ")
    # filtered = [word for word in lst_of_words if (word not in stop_words) and word != '-']
    for word in stop_words:
        award = re.sub(word, ' ', award)

    return award


def get_hardcoded_awards(): #TODO compiling regex to possibly make it faster??
    stop_words = [' or ', ' in ', ' a ', ' made ', ' for ']
    clean_awards = []
    for award in LIST_OF_AWARDS:
        # print(award)
        award = re.sub('^best .+ an\s', '', award)
        award = re.sub('best ', '', award)
        award = re.sub('television series', 'tv series', award)
        award = re.sub('television', 'tv', award)
        award = re.sub('in a ', '', award)
        award = re.sub('role ', '', award)
        award = re.sub('series, mini-series ', '', award)
        award = re.sub('mini-series or motion picture made for tv', 'mini-seriestv', award)
        award = re.sub('cecil b. demille ', 'demille ', award)
        # print('award: : ', award)
        award = re.sub('or motion picture made for tv', 'tv', award)

        # award = re.sub('comedy or musical', 'comedymusical', award)
        award = filter_word_in_list(award, stop_words)
        # print(award)

        clean_awards.append(award)
    return clean_awards



def get_HARDCODED_AWARD_DATA(year): #TODO do not use in final product.
    json_data = json.loads(open('gg'+year+'answers.json').read())
    return json_data['award_data']

def match_movie(look_phrase_str):
    # print('@movie matched', look_phrase_str)
    movie_key_words = ['screenplay', 'film', 'pictures', 'picture', 'score', 'song', 'series', 'theme']
    for word in movie_key_words:
        if re.search(word, look_phrase_str):
            if not match_person(look_phrase_str):
                return True
    return False
def match_person(look_phrase_str):
    # print('@person matched: ', look_phrase_str)
    movie_key_words = ['director', 'actor', 'actress', 'demille']
    for word in movie_key_words:
        if re.search(word, look_phrase_str):
            return True
    return False

def subrat_get_winner(all_awards, tweets):


    kb_actors = get_kb_actors()
    kb_directors = get_kb_directors()
    kb_movies = get_kb_movies()
    json_data = get_HARDCODED_AWARD_DATA('2015')
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
                    for i in range(len(tweet) - 1):
                        pot_name = tweet[i]
                        # print(pot_name)
                        if pot_name in dict_names:
                            dict_names[pot_name] += 1
                        else:
                            dict_names[pot_name] = 1
                            # num_tweets_with_word = 0
        magic_constant = .28 * num_tweets_with_word
        for key, val in dict_names.items():
            if val > magic_constant:
                # winners.append(str(key) + str(val))
                pot_winners.append(str(key).replace('_', ' '))
        if match_movie(look_phrase[0]):
            # print('&*', pot_winners)
            for candidate in pot_winners:
                if candidate not in look_phrase[0].split(' ') and candidate not in ['motion', 'picture','winner','best', 'wins', 'won', 'actor','actress', 'comedy', 'musical', '-']:

                    lst = [movie for movie in kb_movies if re.search(candidate + ' ', movie)]
                    # print('candidate:', candidate, lst)
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
                        if len(lst) > 0 and len(lst) < 5:
                            winners.append(lst)
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
            selected_winners[LIST_OF_AWARDS[idx]] = winners[0][0]
    # print(selected_winners)
    return selected_winners

def get_winner(year):
    tweets = get_cleaned_tweets(year)
    hardcoded_awards = get_hardcoded_awards()
    return subrat_get_winner(hardcoded_awards, tweets)

def main():
    '''
        The loading of tweets takes a while, so writing it to cleaned.csv to read from
        after processing. REMOVE after development or if modifying preprocessing
        TODO
    '''
    # write_file([2013]);
    # tweets = get_cleaned_tweets(2015)

    '''
    Getting the Hosts
    # '''
    # hardcoded_awards = get_hardcoded_awards()
    # subrat_get_winner(hardcoded_awards, tweets)

    # actors_kb = get_kb_actors()
    # for actor in actors_kb:
    #     if re.search('costner', actor):
    #         print(actor)
    #

    # for tweet in tweets:
    #     if 'fargo' in tweet and 'wins' in tweet:
    #         print(tweet)

    # get_winner('2015')





    # print(get_kb_directors())
    # for val in get_kb_movies():
    #     if re.match('transp', val):
    #         print(val)


if __name__ == '__main__':
    main()
