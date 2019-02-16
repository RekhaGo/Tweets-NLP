import requests
import unidecode

def get_kb_lists():
    query_movie ='''SELECT ?film ?filmLabel
    WHERE
    {
    ?film wdt:P31 wd:Q11424.
    ?film wdt:P577 ?date .
    FILTER("2012-01-01"^^xsd:dateTime <= ?date && ?date < "2019-01-01"^^xsd:dateTime)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }'''
    query_director = '''
    SELECT DISTINCT ?director ?directorLabel
    WHERE 
    {
      ?film wdt:P31 wd:Q11424.
      ?film wdt:P57 ?director.
      ?film wdt:P577 ?date .
      FILTER("2012-01-01"^^xsd:dateTime <= ?date && ?date < "2019-01-01"^^xsd:dateTime)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    '''
    query_cast = '''
    SELECT DISTINCT ?name 
    WHERE 
    {
      ?film wdt:P31 wd:Q11424.
      ?film wdt:P161 ?cast.
      ?cast wdt:P373 ?name.
      ?film wdt:P577 ?date .
      FILTER("2012-01-01"^^xsd:dateTime <= ?date && ?date < "2019-01-01"^^xsd:dateTime)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    '''
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    kb_movies_json = requests.get(url, params={'query': query_movie, 'format': 'json'}).json()
    kb_directors_json = requests.get(url, params={'query': query_director, 'format': 'json'}).json()
    kb_cast_json = requests.get(url, params={'query': query_cast, 'format': 'json'}).json()

    kb_movies = set()
    kb_directors = set()
    kb_actors = set()


    for item in kb_movies_json['results']['bindings']:
        kb_movies.add(unidecode.unidecode(item['filmLabel']['value'].lower()))
    for item in kb_directors_json['results']['bindings']:
        kb_directors.add(unidecode.unidecode(item['directorLabel']['value'].lower()))
    for item in kb_cast_json['results']['bindings']:
        kb_actors.add(unidecode.unidecode(item['name']['value'].lower()))


    print('Writing kb to file')
    with open('kb_movies.txt', 'w') as filehandle:
        for listitem in kb_movies:
            filehandle.write('%s\n' % listitem)
    with open('kb_directors.txt', 'w') as filehandle:
        for listitem in kb_directors:
            filehandle.write('%s\n' % listitem)
    with open('kb_actors.txt', 'w') as filehandle:
        for listitem in kb_actors:
            filehandle.write('%s\n' % listitem)

    '''
    with open('listfile.txt', 'r') as filehandle:  
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
    '''

