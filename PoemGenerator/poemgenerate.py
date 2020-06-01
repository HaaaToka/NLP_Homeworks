import dynet as dy
import json
from glove import Glove
import numpy as np
import csv
from collections import defaultdict
from operator import itemgetter
import random


def DefaultdictInside():
    return [defaultdict(int),0]

vectorDim = 50 # 50 100 200 300
ngram = 2 # 3->trigram   2->bigram  1->unigram


##################################  READ DATASET  ###################################

# bos # begin of sentence
# eos # end of sentence
# eol # end of line
# bol # begin of line
def read_dataset(fpath):
    """
    replace(".:?"," ")
    , ; ! " | -> these are not in dataset
    ' - 're 's n't 've 'll -> didn't touched by me
    """
    print("Reading dataset...")
    poems=[]
    n_grams_dict=defaultdict(DefaultdictInside)
    with open(fpath) as json_file:
        data = json.load(json_file)
        for d in data:
            if d["id"]==100:
                break
            poem = d["poem"]
            #poem = poem.lower() -- dataset already lowercased
            poem = poem.replace("\n"," eol ")
            poem = poem.replace("."," ")
            poem = poem.replace(":"," ")
            poem = poem.replace("?"," ")
            poem = "bos "+poem+" eos"
            poem = poem.split()
            poems.append([])
            for i in range(len(poem)-ngram+1):
                poems[-1].append(poem[i:i+ngram])
                
                prev_gram = poems[-1][-1][:ngram-1]
                next_gram = poems[-1][-1][-1]    
                n_grams_dict[" ".join(prev_gram)][1]+=1
                n_grams_dict[" ".join(prev_gram)][0][next_gram]+=1
            n_grams_dict["eos"][1]+=1
            
    print("Just Finished Reading dataset...")
    return poems,n_grams_dict

poems,count_dict= read_dataset('unim_poem.json')
print("Poem Count:",len(poems))
#print(poems[0])
keys = list(count_dict.keys())
unique_gram = len(keys)
print("Unique Gram:",unique_gram)
tot=0
for k,v in count_dict.items():
    tot += v[1]
print("Total Word:",tot)


##################################  READ GLOVE ###################################


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
            
    mean = np.array(embeds).mean(axis=0,dtype='float32')
    word2vec["mmeann"]=mean # if the word doesn't occur in vocab, it will take mean value
    embeds.append(mean)
    
    print("Finished Loading word vectors...")
    return np.array(embeds),word2idx,word2vec

embedding,w2i, w2v= read_glove('glovo/glove.6B.'+str(vectorDim)+'d.txt')
print(embedding.shape)
print(embedding.size)


##################################  TRAIN  ###################################


def sumvec(w2v,words):
    """
        If our model was 3,4,5gram, 
        this function would add the value of the w2vs for input vector
    """
    _temp = np.zeros(50)
    for w in words:
        try:
            _temp+=w2v[w]
        except:
            _temp+=w2v["mmeann"]
    return _temp


h = 150 # HiddenUnit
m = vectorDim

EPOCH = 10

_model = dy.Model()
H = _model.add_parameters((h, m))
d = _model.add_parameters(h)
U = _model.add_parameters((unique_gram, h))
b = _model.add_parameters(unique_gram)
_trainer = dy.SimpleSGDTrainer(_model)


i=0
for epoch in range(1, EPOCH + 1):
    epoch_loss = 0.0
    for p in poems:
        for gram in p:
            x=sumvec(w2v,gram[:ngram-1])
            try:
                y=keys.index(gram[-1])
            except:
                y=random.randint(0,len(keys)-1)
            dy.renew_cg()
            x = dy.inputVector(x)
            input_layer = dy.tanh(H * x + d)
            hidden_layer = U * input_layer + b
            output_layer = dy.softmax(hidden_layer)
            loss = dy.pickneglogsoftmax(output_layer, y)
            epoch_loss += loss.scalar_value()
            loss.forward()
            loss.backward()
            _trainer.update()
    print("Epoch %d. loss = %f" % (epoch, epoch_loss/len(poems)))



##################################  GENERATE POEM  ###################################


# I leave you alone with my meaningless, absurd poems

close=20
satir = 4
genarated_poem=["bos"]
generated_poems=[[]]

for i in range(satir):
    #while 1:
    while len(genarated_poem)<10:
        x=sumvec(w2v,genarated_poem[-1])
        dy.renew_cg()
        x = dy.inputVector(x)
        input_layer = dy.tanh(H * x + d)
        hidden_layer = U * input_layer + b
        output_layer = list(dy.softmax(hidden_layer).value())
        oen = list(enumerate(output_layer))
        oen=sorted(oen,key=itemgetter(1),reverse=True)
        rnd = random.randint(0,close-1)
        genarated_poem.append(keys[oen[rnd][0]])
        #print(genarated_poem)
        if genarated_poem[-1]=="eol":
            break
    generated_poems[-1]+=genarated_poem
    generated_poem=["eol"]

generated_poems[-1]= " ".join(generated_poems[-1]).replace("bos ","").replace("eol ","\n").replace("eol","").replace("bol ", "")
print(generated_poems)



##################################  PERPLEXITY  ###################################

def Sprob(poem,n_grams_dict,unique_word,ngram):
    # Returns the MLE of given sentence with laplace smoothing
        
    result = 1
    split_poem = poem.split()+["eol"]


    for index in range(len(split_poem)-ngram):
        prev_gram = " ".join(split_poem[index:ngram+index-1])
        next_gram = split_poem[ngram+index-1]

        result *= ( (n_grams_dict[prev_gram][0][next_gram] + 1) / (n_grams_dict[prev_gram][1] + unique_word) )

    #print("\t-> S-Probabilty of sentence :{0:.30f}".format(result))
    return result



def perplexity(poems,n_grams_dict,unique_word,ngram):
    # Returns the perplexity of the given sentence
    # second formula from assignment pdf 

    result=1
    for p in poems:
        for pl in p.split("\n"):
            result*=Sprob(pl,n_grams_dict,unique_word,ngram)
        
    result=1/result
    result = result**(1/(len(p.split(" "))+satir))

    print("-> Perplexity of sentence :{0:.20f}".format(result))

perplexity(generated_poems,count_dict,unique_gram,ngram)
        
# deneme 