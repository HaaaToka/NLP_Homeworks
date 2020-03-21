from collections import defaultdict,Counter
from random import randint

class LanguageModel:

    ngrams=0
    # 1grams model
    count_of_words=defaultdict(int) # this will evolve for storing probability 
    unique_words_count = 0
    total_words_count = 20000 # for laplace smoothing

    # ngrams model
    n_mines_one_grams_dict = defaultdict(int) # this will evolve for storing probability
    unique_n_mines_one_grams = 0
    n_grams_dict = defaultdict(int) # this will evolve for storing probability
    unique_n_grams = 0

    def __init__(self,n):
        print("You create a new "+str(n)+"ngrams language modal")
        self.Ngram(n)

    def Ngram(self,n):
        self.ngrams = n

    def PunctuationSanitize(self, word_list):
        """
            Sentences are not too long. Thus, creating extra list aren't expensive
        """
        punctuation_signs = ["``","''","?","!","|",",",";",":","'s",".","--"]
        sanitized_list = []

        for elem in word_list:
            if elem in punctuation_signs:
                if elem in ["'s"] and len(sanitized_list):
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
                self.count_of_words[k]+=v

        else :
            return 23

    def Sentence2Countlist(self, sentence):

        word_list = sentence.strip().split(" ")[1:]
        word_list = self.PunctuationSanitize(word_list)

        self.CountGrams(" ".join(gram) for gram in zip(*[word_list[i:] for i in range(self.ngrams)]))
        """

            buradan yürü git
            xxx yyy zzz şeklinde olduğunda {"zzz" : [{ "xxx yyy" : 1}, 1]}

            mesela <s><s> vericem ben cümle üretirken o tek tek baka baka gidecek

        """


        self.unique_words_count = len(self.count_of_words.keys())
        self.total_words_count = sum(self.count_of_words.values())


    
    def LoadDataset2Model(self, sentences):

        for s in sentences:
            self.Sentence2Countlist(s)


        if self.ngrams == 1:
            for k,v in self.count_of_words.items():
                print( "->", k, ":", v )
        
        print(len(self.count_of_words.keys()))