from collections import defaultdict,Counter
from random import randint

    
def DefaultdictInside():
    return [defaultdict(int),0]
class LanguageModel:

    ngrams=0

    """
        lets say this our three word respectify"xxx yyy zzz"  {"xxx yyy" : [{ "zzz" : 1}, 1]}
        mesela <s><s> vericem ben cümle üretirken o tek tek baka baka gidecek
    """
    n_grams_dict = defaultdict(DefaultdictInside) # vocabulary dictionary
    unique_n_grams = 0
    total_words_count = 0 # for laplace smoothing

    all_generated_sentences = []

    def __init__(self,n):
        print("You create a new "+str(n)+"gram(s) language modal")
        self.Ngram(n)

    def Ngram(self,n):
        self.ngrams = n

    def PunctuationSanitize(self, word_list):
        """
            Sentences are not too long. Thus, creating extra list aren't expensive
        """
        punctuation_signs = ["``","`","''","'","?","!","|",",",";",":",".","--","'re","'s","n't"]
        sanitized_list = []

        for elem in word_list:
            if elem in punctuation_signs:
                if elem in ["'s","'re","n't"] and len(sanitized_list):
                    sanitized_list[-1]+=elem
            else:
                sanitized_list.append(elem.lower())

        # ngram sentence beginning/ending tags
        return (["<s>"]*(self.ngrams-1))+sanitized_list+(["</s>"]*(self.ngrams-1))

    def CountGrams(self, word_list):
        
        if self.ngrams == 1:
            for w in word_list:
                self.n_grams_dict[w][1]+=1

        else :            
            for index in range(len(word_list)-self.ngrams+1):
                prev_gram = " ".join(word_list[index:self.ngrams+index-1])
                next_gram = word_list[self.ngrams+index-1]
                
                self.n_grams_dict[prev_gram][1]+=1
                self.n_grams_dict[prev_gram][0][next_gram]+=1
                

    def Sentence2Countlist(self, sentence):

        word_list = sentence.strip().split(" ")[1:]
        word_list = self.PunctuationSanitize(word_list)

        self.CountGrams(word_list)
        self.unique_n_grams = len(self.n_grams_dict.keys())
    
    def LoadDataset2Model(self, sentences):

        for s in sentences:
            self.Sentence2Countlist(s)

        for v in self.n_grams_dict.values():
            self.total_words_count += v[1]

        print("\tUnique Word Count ->",self.unique_n_grams)
        print("\tTotal Word Count ->",self.total_words_count)
        print("DATASET WAS LOADED TO LanguageModel")

    
    def StartSentence(self):

        if self.ngrams == 1:
            return [ "GiveMeFirstWord" ]

        else:
            return (self.ngrams-1) * ["<s>"]


    def PrintSentence(self,generated_words):

        while generated_words[-1]=="</s>":
            generated_words.pop()

        if self.ngrams == 1:
            self.all_generated_sentences.append(" ".join(generated_words[1:]))
            print(self.all_generated_sentences[-1])

        else:
            self.all_generated_sentences.append(" ".join(generated_words[self.ngrams-1:]))
            print(self.all_generated_sentences[-1])

        self.PPL(self.all_generated_sentences[-1]) # beginning tokens(<s>) are not included
        # self.PPL(" ".join(generated_words)) # beginning tokens(<s>) are included

    def Generate(self, length, count):
        """
            length : the maximum number of words in a sentence
            count : how many sentences will be generated
        """ 

        print("GENERATING OF "+str(self.ngrams)+"GRAM(S) SENTENCE HAS STARTED")
        
        for i in range(count):
            print(str(i+1)+". Sentence :", end=" ")
            generated_sentence = self.StartSentence()
            while len(generated_sentence)<(length+self.ngrams-1) and generated_sentence[-1]!="</s>":
                if self.ngrams == 1:
                    generated_sentence.append(self.Next(["GiveMeWord"]))
                else:
                    generated_sentence.append(self.Next(generated_sentence[-(self.ngrams-1):]))
            
            self.PrintSentence(generated_sentence)

        return self.all_generated_sentences

    def Next(self,prev_words):
        # return a random word w according to the distribution p(w|"I")
        # Used the MLE distributions for this

        prev_token = " ".join(prev_words)

        if self.ngrams == 1:
            # Random Cumulative Summation
            loc = randint(1,self.total_words_count)
            for nxt,dctCnt in self.n_grams_dict.items():
                loc -= dctCnt[1]
                if loc <= 0:
                    return nxt

        else :
            # print("coming :",prev_words," - - tot : ", self.n_grams_dict[prev_token][1] )
            loc = randint(1,self.n_grams_dict[prev_token][1])
            for nxt,cnt in self.n_grams_dict[prev_token][0].items():
                loc -= cnt
                if loc <= 0:
                    return nxt

    
    def Prob(self,sentence):
        # Returns the MLE of given sentence
        
        result = 1
        sentence=sentence.lower()
        split_sentence = sentence.split(" ")
        split_sentence = ["<s>"]*(self.ngrams-1) + split_sentence + ["</s>"]*(self.ngrams-1)

        if self.ngrams == 1:
            for word in split_sentence:
                # print("{0} -> {1} / {2} = {3:.20f}".format(word,self.n_grams_dict[word][1],self.total_words_count,(self.n_grams_dict[word][1]/self.total_words_count)))
                result *= (self.n_grams_dict[word][1]/self.total_words_count)
  
        else:
            for index in range(len(split_sentence)-self.ngrams):
                prev_gram = " ".join(split_sentence[index:self.ngrams+index-1])
                next_gram = split_sentence[self.ngrams+index-1]

                # print(prev_gram,next_gram,"->",self.n_grams_dict[prev_gram][0][next_gram],":",self.n_grams_dict[prev_gram][1], "- - -", self.n_grams_dict[prev_gram][0][next_gram] / self.n_grams_dict[prev_gram][1])
                
                if self.n_grams_dict[prev_gram][0][next_gram] == 0:
                    # There are some sentences that are not stop with ending token. They are interrupted because of wanted length of sentence
                    # This is caused to zero division error at calculating perplexity
                    # I am not sure about which one should I use (Prob or Sprob)
                    # If there wouldn't be any length rule, this condition wouldn't be exist
                    result *= ( (self.n_grams_dict[prev_gram][0][next_gram]+1) / self.n_grams_dict[prev_gram][1] )
                else:
                    result *= ( self.n_grams_dict[prev_gram][0][next_gram] / self.n_grams_dict[prev_gram][1] )

        print("Probabilty of sentence :{0:.20f}".format(result))
        return result
        

    def Sprob(self,sentence):
        # Returns the MLE of given sentence with laplace smoothing
        
        result = 1
        sentence=sentence.lower()
        split_sentence = sentence.split(" ")
        split_sentence = ["<s>"]*(self.ngrams-1) + split_sentence + ["</s>"]*(self.ngrams-1)

        if self.ngrams == 1:
            for word in split_sentence:
                # print("{0} -> {1} / {2} = {3:.20f}".format(word,self.n_grams_dict[word][1],self.unique_n_grams,(self.n_grams_dict[word][1]/self.unique_n_grams)))
                result *= ((self.n_grams_dict[word][1] + 1) / (self.unique_n_grams + self.unique_n_grams))
  
        else:
            for index in range(len(split_sentence)-self.ngrams):
                prev_gram = " ".join(split_sentence[index:self.ngrams+index-1])
                next_gram = split_sentence[self.ngrams+index-1]

                # print(prev_gram,next_gram,"->",self.n_grams_dict[prev_gram][0][next_gram],":",self.n_grams_dict[prev_gram][1])
                result *= ( (self.n_grams_dict[prev_gram][0][next_gram] + 1) / (self.n_grams_dict[prev_gram][1] + self.unique_n_grams) )

        print("S-Probabilty of sentence :{0:.20f}".format(result))
        return result

    def PPL(self,sentence):
        # Returns the perplexity of the given sentence
        # second formula from assignment pdf 
        
        result = 1/self.Prob(sentence)
        result = result**(1/len(sentence.split(" ")))

        print("Perplexity of sentence :{0:.20f}".format(result))
        return result


