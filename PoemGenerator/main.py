#import dynet
import json
from glove import Glove
import numpy as np
import csv



def read_dataset(fpath):
    print("Reading dataset...")
    with open(fpath) as json_file:
        data = json.load(json_file)
        for d in data:
            print(d["poem"])
            break

def read_glove(fpath):
    print('Loading word vectors...')
    word2vec = {}
    embeds = []
    word2idx = {}
    with open(fpath, encoding='utf-8') as f:
      for line in f:
        values = line.split()
        word = values[0]
        word2idx[word] = len(embeds)
        vec = np.asarray(values[1:], dtype='float32')
        word2vec[word] = vec
        embeds.append(vec)
        break
    return np.array(embeds),word2idx





read_dataset('unim_poem.json')
embedding,w2i = read_glove('glovo/glove.6B.50d.txt')
print(embedding)