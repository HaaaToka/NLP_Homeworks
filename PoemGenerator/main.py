#import dynet
import json

with open('unim_poem.json') as json_file:
    data = json.load(json_file)
    for d in data:
        print(d["poem"])
        break