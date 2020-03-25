from collections import defaultdict,Counter
from random import randint

    
def DefaultdictInside():
    return [defaultdict(int),0]
class LanguageModel:

    ngrams=0
    # 1grams model
    unigram_word_dict=defaultdict(int) # this will evolve for storing probability 
    unique_words_count = 0
    total_words_count = 0 # for laplace smoothing

    # ngrams model
    """ n_mines_one_grams_dict = defaultdict(int) # this will evolve for storing probability
    unique_n_mines_one_grams = 0 """
    n_grams_dict = defaultdict(DefaultdictInside) # this will evolve for storing probability
    unique_n_grams = 0
    """
        lets say this our three word respectify"xxx yyy zzz"  {"xxx yyy" : [{ "zzz" : 1}, 1]}
        mesela <s><s> vericem ben cümle üretirken o tek tek baka baka gidecek
    """


    def __init__(self,n):
        print("You create a new "+str(n)+"ngrams language modal")
        self.Ngram(n)

    def Ngram(self,n):
        self.ngrams = n

    def PunctuationSanitize(self, word_list):
        """
            Sentences are not too long. Thus, creating extra list aren't expensive
        """
        punctuation_signs = ["``","''","?","!","|",",",";",":","'s",".","--","'re"]
        sanitized_list = []

        for elem in word_list:
            if elem in punctuation_signs:
                if elem in ["'s","'re"] and len(sanitized_list):
                    sanitized_list[-1]+=elem
            else:
                sanitized_list.append(elem.lower())

        # string->punction bak bi kelimelerde durum nasıl die
        # ngram sentence beginning/ending tags
        return (["<s>"]*(self.ngrams-1))+sanitized_list+(["</s>"]*(self.ngrams-1))

    def CountGrams(self, word_list):
        
        if self.ngrams == 1:
            temp_counts = Counter(word_list)
            for k,v in temp_counts.items():
                self.unigram_word_dict[k]+=v

        else :            
            for index in range(len(word_list)-self.ngrams):
                prev_gram = " ".join(word_list[index:self.ngrams+index-1])
                next_gram = word_list[self.ngrams+index-1]
                
                self.n_grams_dict[prev_gram][1]+=1
                self.n_grams_dict[prev_gram][0][next_gram]+=1
                

    def Sentence2Countlist(self, sentence):

        word_list = sentence.strip().split(" ")[1:]
        word_list = self.PunctuationSanitize(word_list)

        # self.CountGrams(" ".join(gram) for gram in zip(*[word_list[i:] for i in range(self.ngrams)]))
        self.CountGrams(word_list)

        self.unique_words_count = len(self.unigram_word_dict.keys())
        self.total_words_count = sum(self.unigram_word_dict.values())

        self.unique_n_grams = len(self.n_grams_dict.keys())
        for v in self.n_grams_dict.values():
            self.total_words_count += v[1]

    
    def LoadDataset2Model(self, sentences):

        for s in sentences:
            self.Sentence2Countlist(s)

        """ if self.ngrams == 1:
            for k,v in self.unigram_word_dict.items():
                print( "->", k, ":", v )
            print("Unique ->",self.unique_words_count)
        
        else: # ngrams = 2,3
            for prev,nxts in self.n_grams_dict.items():
                print("-> :",prev,"...",nxts[1])
                for nxt,cnt in nxts[0].items():
                    print("\t ",prev,",",nxt," -> :",cnt)
            print("Unique ->",self.unique_n_grams) """

        print("Total ->",self.total_words_count)
        print("DATASET WAS LOADED TO LanguageModel")

    
    def StartSentence(self):

        if self.ngrams == 1:
            return [ self.Next("give me first word") ]

        else:
            return (self.ngrams-1) * ["<s>"]

    def Generate(self, length, count):
        """
            length : the maximum number of words in a sentence
            count : how many sentences will be generated
        """ 

        print("Generating of Sentence has started".upper())
        
        for i in range(count):
            print(str(self.ngrams)+"grams sentence generation")
            print(str(i+1)+". sentence :")

            # generated_sentences = self.StartSentence()
            generated_sentences = (self.ngrams)*["<s>"]
            while len(generated_sentences)<(length+2*self.ngrams) and generated_sentences[-1]!="</s>":
                if self.ngrams == 1:
                    generated_sentences.append(["GiveMeWord"])
                else:
                    generated_sentences.append(self.Next(generated_sentences[-(self.ngrams-1):]))
                #generated_sentences.append(self.Next(" ".join(generated_sentences[-self.ngrams:])))
            
            print(" ".join(generated_sentences))

    def RandomCumulativeSummation(self,giveme_dict):
        """

            CONTINUE FROM HERE
            THE OUTLINE OF FUNCTION IS IN try.py
            THEN CONTINUE "NEXT" FUNCTION

        """ 


    def Next(self,prev_words):
        # return a random word w according to the distribution p(w|"I")
        # Used the MLE distributions for this

        prev_token = " ".join(prev_words)

        if self.ngrams == 1:
            print("unigram")

        else :
            #print("coming :",prev_words," - - tot : ", self.n_grams_dict[prev_token][1] )
            loc = randint(1,self.n_grams_dict[prev_token][1])
            #print("::LOC>> ",loc)
            for nxt,cnt in self.n_grams_dict[prev_token][0].items():
                loc -= cnt
                if loc <= 0:
                    return nxt

        return "next word"


    
    def Prob(self,sentence):
        # Returns the MLE of given sentence
        
        result = 1
        sentence=sentence.lower()
        split_sentence = sentence.split(" ")
        split_sentence = ["<s>"]*(self.ngrams-1) + split_sentence + ["</s>"]*(self.ngrams-1)

        if self.ngrams == 1:
            for word in split_sentence:
                result *= (self.unigram_word_dict[word]/self.total_words_count)
                print("{0} -> {1} / {2} = {3:.20f}".format(word,self.unigram_word_dict[word],self.total_words_count,(self.unigram_word_dict[word]/self.total_words_count)))
  
        else:
            for index in range(len(split_sentence)-self.ngrams):
                prev_gram = " ".join(split_sentence[index:self.ngrams+index-1])
                next_gram = split_sentence[self.ngrams+index-1]

                result *= ( self.n_grams_dict[prev_gram][0][next_gram] / self.n_grams_dict[prev_gram][1] )
                print(prev_gram,next_gram,"->",self.n_grams_dict[prev_gram][0][next_gram],":",self.n_grams_dict[prev_gram][1], "- - -", self.n_grams_dict[prev_gram][0][next_gram] / self.n_grams_dict[prev_gram][1])

        return result
        

    def Sprob(self,sentence):
        # Returns the MLE of given sentence with laplace smoothing
        
        result = 1
        sentence=sentence.lower()
        split_sentence = sentence.split(" ")
        split_sentence = ["<s>"]*(self.ngrams-1) + split_sentence + ["</s>"]*(self.ngrams-1)

        if self.ngrams == 1:
            for word in split_sentence:
                result *= ((self.unigram_word_dict[word] + 1) / (self.unique_words_count + self.unique_words_count))
                print("{0} -> {1} / {2} = {3:.20f}".format(word,self.unigram_word_dict[word],self.unique_words_count,(self.unigram_word_dict[word]/self.unique_words_count)))
  
        else:
            for index in range(len(split_sentence)-self.ngrams):
                prev_gram = " ".join(split_sentence[index:self.ngrams+index-1])
                next_gram = split_sentence[self.ngrams+index-1]

                print(prev_gram,next_gram,"->",self.n_grams_dict[prev_gram][0][next_gram],":",self.n_grams_dict[prev_gram][1])
                result *= ( (self.n_grams_dict[prev_gram][0][next_gram] + 1) / (self.n_grams_dict[prev_gram][1] + self.unique_n_grams) )

        return result

    def PPL(self,sentence):
        # Returns the perplexity of the given sentence
        
        result = 1
        return result

