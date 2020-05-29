#import dynet
import json
from glove import Glove


gg = Glove(cooccurence=[1,2]).load_stanford("glovo/glove.6B.50d.txt")


with open('unim_poem.json') as json_file:
    data = json.load(json_file)
    for d in data:
        print(d["poem"])
        break