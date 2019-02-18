'''Version 0.35'''

import json
import parse
import KBLoader


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = parse.get_hosts(year)
    f = open('output_file'+str(year)+'.json')
    json_data = json.load(f)
    f.close()

    json_data['hosts'] = hosts
    with open('output_file'+str(year)+'.json', 'w') as f:
        json.dump(json_data, f)

    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = parse.get_awards(year)
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    f = open('output_file' + str(year) + '.json')
    json_data = json.load(f)
    f.close()
    nominees = parse.get_nominee(year)
    if year in ['2013', '2015']:
        for award in OFFICIAL_AWARDS_1315:
            json_data['award_data'][award]['nominees'] = nominees[award]
    else:
        for award in OFFICIAL_AWARDS_1819:
            json_data['award_data'][award]['nominees'] = nominees[award]

    with open('output_file'+str(year)+'.json', 'w') as f:
        json.dump(json_data, f)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    f = open('output_file' + str(year) + '.json')
    json_data = json.load(f)
    f.close()
    winners = parse.get_winner(year)
    if year in ['2013', '2015']:
        for award in OFFICIAL_AWARDS_1315:
            json_data['award_data'][award]['winner'] = winners[award]
    else:
        for award in OFFICIAL_AWARDS_1819:
            json_data['award_data'][award]['winner'] = winners[award]

    with open('output_file'+str(year)+'.json', 'w') as f:
        json.dump(json_data, f)
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenters = parse.get_presenter(year)

    f = open('output_file' + str(year) + '.json')
    json_data = json.load(f)
    f.close()

    if year in ['2013', '2015']:
        for award in OFFICIAL_AWARDS_1315:
            json_data['award_data'][award]['presenters'] = presenters[award]
    else:
        for award in OFFICIAL_AWARDS_1819:
            json_data['award_data'][award]['presenters'] = presenters[award]

    with open('output_file'+str(year)+'.json', 'w') as f:
        json.dump(json_data, f)
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    year_list = ['2013','2015','2018', '2019']
    for year in year_list:
        try:
            parse.write_file([year])
        except:
            print("FILE NOT FOUND ERROR: Something went wrong when creating local copies. Make sure the files you need are present in the flat directory.")

    KBLoader.get_kb_lists()

    for year in year_list:
        print('creating output file for ', year)
        results = dict()
        results['hosts'] = []
        results['award_data'] = {}
        if year in ['2013', '2015']:
            for award in OFFICIAL_AWARDS_1315:
                results['award_data'][award] = {}
        else:
            for award in OFFICIAL_AWARDS_1819:
                results['award_data'][award] = {}

        with open('output_file'+str(year)+'.json', 'w') as f:
            json.dump(results, f)

    print("Pre-ceremony processing complete.")
    return

def pretty_print(year):
    f = open('output_file' + str(year) + '.json')
    json_data = json.load(f)
    f.close()

    print('hosts : ',json_data['hosts'])
    if year in ['2013', '2015']:
        for award in OFFICIAL_AWARDS_1315:
            print('-----AWARD: '+award)
            for key, val in json_data['award_data'][award].items():
                print(str(key)+':  '+str(val))

    else:
        for award in OFFICIAL_AWARDS_1819:
            print('-----AWARD: ' + award)
            for key, val in json_data['award_data'][award].items():
                print(str(key) + ':  ' + str(val))

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    print("NOTE: If the code fails and returns a module not found, please run the command: sh package.sh")
    pre_ceremony()

    # parse.write_file(['2013', '2015'])
    pretty_print('2013')

    return

if __name__ == '__main__':
    main()
