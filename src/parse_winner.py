import re
import os
import json
import pickle
from nltk.corpus import stopwords

win_word_bag = ['win','winner','winners','wins','won','winning','goes to']

award_category = ['Best Motion Picture(.*)Drama',
'Best Actress(.*)Motion Picture(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Musical(.*)Comedy',
'Best Animated Feature Film',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Drama',
'Best Performance(.*)Actress(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Performance(.*)Actor(.*)(TV|Television) Series(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Drama',
'Best Director(.*)Motion Picture',
'Cecil B. DeMille Award',
'Best Supporting Actor(.*)Motion Picture',
'Best Mini[\s-]*series(.*)(TV|Television) Film',
'Best Supporting Actor(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Performance(.*)Actor(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Motion Picture(.*)Musical(.*)Comedy',
'Best Actress(.*)Motion Picture(.*)Musical(.*)Comedy',
'Best Screenplay(.*)Motion Picture',
'Best Original Score',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Musical(.*)Comedy',
'Best Supporting Actress(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best (TV|Television) Series(.*)Drama',
'Best Supporting Actress(.*)Motion Picture',
'Best Original Song',
'Best Foreign Language Film',
'Best (TV|Television) Series(.*)Musical(.*)Comedy',
'Best Actor(.*)(TV|Television) Series(.*)Musical(.*)Comedy']


def findWinner(fin, award_list, win_word_bag):
	awardDic = read_dic('twt_Award.dict')
	if awardDic is None:
		awardDic = findTweetsContainAward(fin, award_list)
		write_dic(awardDic, 'twt_Award')

	winAwardDic = read_dic('twt_Win_Award.dict')
	if winAwardDic is None:
		winAwardDic = findTweetsContainWin(awardDic, win_word_bag)
		write_dic(winAwardDic, 'twt_Win_Award')
	
	goesToWinnerDic = read_dic('twt_goes_to.dict')
	if goesToWinnerDic is None:
		goesToWinnerDic = findWinnerByWinWord(winAwardDic, 'goes to')
		write_dic(goesToWinnerDic, 'twt_goes_to.dict')

	#winnerDic = read_dic('twt_winner')
	winnerDic = None
	if winnerDic is None:
		for winWord in ['win','wins','has won','won','win for','Best']:
			winnerDic = findWinnerByWinWord(winAwardDic, winWord, curWinnerDic=winnerDic)
		write_dic(winnerDic, 'twt_winner')

	award_winner_dic = rename_awards(extractName(winnerDic))

	return award_winner_dic

def rename_awards(award_winner_dic):
	dic = {}
	for award in award_winner_dic:
		newName = re.sub('(\s|\(\.\*\)|\(|\)|\|)','_',award)
		newName = re.sub(r'\[\\s\-\]\*','',newName)
		newName = re.sub(r'_+',' ',newName).rstrip(' ')
		newName = re.sub(r'\sfor(?= made)','',newName)
		newName = re.sub(r'\sTV(?= Television)','',newName)
		dic[newName] = award_winner_dic[award]
	return dic

def findTweetsContainAward(tweets, award_list):
    dic = {}
    for words in tweets:
        line = ' '.join(words)
        for award in award_list:
            if award not in dic:
                dic[award] = []
            m = re.findall(award ,line, re.IGNORECASE)#.split('\t')[0])
            if m:
                dic[award].append(line)

    for award,values in list(dic.items()):
        if len(dic[award]) == 0:
            dic.pop(award)
            #del dic[award]
            #dic.pop(award, None)
    return dic

def findTweetsContainWin(dic, win_word_bag):
	new_dic = {}
	for award in dic:
		new_dic[award] = []
		for twts in dic[award]:
			for w in win_word_bag:
				m = re.findall(r"([^.]*?%s.*)"%w,twts,re.IGNORECASE)
				if m:
					new_dic[award].append(twts)
					break
		if len(new_dic[award]) == 0:
			for twts in dic[award]:
				new_dic[award].append(twts)
	return new_dic

def findWinnerByWinWord(dic, winWord, curWinnerDic=None):
	if curWinnerDic is None:
		new_dic = {}
	else:
		new_dic = curWinnerDic
	for award in dic:
		if award not in new_dic:
			new_dic[award] = []
		for twts in dic[award]:
			if winWord == 'goes to' or winWord == 'win for':
				m = re.search(r'%s ((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)'%winWord,twts,re.IGNORECASE)
			elif winWord == 'win':
				m = re.search(r'%s(?!\sfor) ((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)'%winWord,twts,re.IGNORECASE)
			elif winWord == 'wins' or winWord == 'has won' or winWord == 'won':
				m = re.search(r'((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*) %s(?![a-zA-Z])'%winWord,twts,re.IGNORECASE)
			elif winWord == 'Best':
				m = re.search(r'((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*) Best',twts,re.IGNORECASE)
			if m:
				new_dic[award].append(m.group(1))
	return new_dic

def extractName(winnerCandidateDic):
	award_winner_dic = {}

	for award in winnerCandidateDic:
		award_winner_dic[award] = topFrequentName(winnerCandidateDic[award])

	return award_winner_dic

def topFrequentName(namelist):
	ndic = {}
	maxFreq = 0
	mostFreqName = ''
	for name in namelist:
		if name in ndic:
			ndic[name] += 1
		else:
			ndic[name] = 1
		if ndic[name] > maxFreq:
			maxFreq = ndic[name]
			mostFreqName = name
	if mostFreqName == '':
		return 'not found'
	return mostFreqName

def read_dic(fn):
	if os.path.isfile(fn):
		with open(fn, 'rb') as f:
			awardDic = pickle.load(f)
		return awardDic
	else:
		return None

def write_dic(dic, folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	with open('%s.dict'%folder,'wb') as f:
		pickle.dump(dic,f)
	for award in dic:
		try:
			fn = open('%s/%s.txt'%(folder,re.sub('(\s|\(\.\*\)|\(|\)|\|)','_',award)),'w+', encoding="utf-8")
			for twts in dic[award]:
				fn.write('%s\n'%twts)
			fn.close()
		except Exception:
			continue


def print_dic(dic):
	for key in dic:
            print("{0} {1}".format(key, dic[key]))
            #print('%s\n%s\n'%(key,dic[key]))

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
    stopWords = create_stop_words()
    for tweet in tweets:
        filtered = [w for w in tweet if not w in stopWords]
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

def main():
    tweets = load_data('gg2013.json')
    #cleaned_tweets = clean(tweets) #list of list of words that compose the phrase
    #print(len(cleaned_tweets))
    winners = findWinner(tweets,award_category,win_word_bag)

    print_dic(winners)


if __name__ == '__main__':
    main()