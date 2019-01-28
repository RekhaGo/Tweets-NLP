import json


json_data = json.loads(open('../data/gg2015.json').read())
for line in json_data:
    print(line['text'])