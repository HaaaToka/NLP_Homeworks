from collections import defaultdict
from string import ascii_lowercase, digits

def returner():
    return 1

def DefaultdictInside():
    return defaultdict(int)

class HMM():

    # { tag_name : howmanytimesoccuredindataset }
    initial_probability = defaultdict(int)
    # { prev_tag : { next_tag : next_tag_count } }
    transition_probability = defaultdict(DefaultdictInside)
    # { word : { belong_tag : word-tag_count } }
    emission_probability = defaultdict(DefaultdictInside)

    total_tag_count=0
    unique_word_count=0
    diftag=[]

    def __init__(self):
        print("GENERATED Bigram_HMM")

    def HMM(self,sentences):
        """
            TASK 1: BUILD a Bigram-Hidden Markov Model
        """
        print("MODEL CREATION WAS STARTED")

        for tokens in sentences:
            prev_word, prev_tag = tokens[0][0], tokens[0][1]
            self.initial_probability[prev_tag]+=1
            self.emission_probability[prev_word][prev_tag]+=1
            self.diftag.append(prev_tag)
            
            for token in tokens[1:]:
                cur_word, cur_tag = token
                self.initial_probability[cur_tag]+=1
                self.transition_probability[prev_tag][cur_tag]+=1
                self.emission_probability[cur_word][cur_tag]+=1
                
                self.diftag.append(cur_tag)

                prev_word = cur_word
                prev_tag = cur_tag

        # P(ti+1|ti) -> Transition Probability Evaluation -> C(ti,ti+1) / C(ti)
        for ti,tis in self.transition_probability.items():
            for ti_1 in tis.keys():
                self.transition_probability[ti][ti_1] /= self.initial_probability[ti]
        
        # P(wi|ti) -> Emission Probability Evaluation -> C(wi,ti) / C(ti)
        self.unique_word_count = len(self.emission_probability)
        for word,tags in self.emission_probability.items():
            for t in tags.keys():
                self.emission_probability[word][t] /= self.initial_probability[t]

        # Initial Probabilty Evaluation
        self.total_tag_count = sum(self.initial_probability.values())-self.initial_probability["<s>"]-self.initial_probability["</s>"]
        for k in self.initial_probability.keys():
            self.initial_probability[k] /= self.total_tag_count

        self.diftag = list(set(self.diftag))


    def viterbi(self,test_sentence):
        """
            to achive the most likely sequence
            calculate the argmax_{t1...tm}p(t1...tm | w1...wm)
            returns tagged test sentence

            vit_matrix represent below matrix
                    <s>                 </s>
                    w0  w1  w2  w3  ... wn
            <s>     1
            b-org   0
            b-misc  0
            b-per   0
            b-loc   0
            i-org   0
            i-misc  0
            i-per   0
            i-loc   0
            o       0
            </s>    0

        """

        ############################### The fisrt step of Viterbi Algorithm ##############################################

        length_sentence = len(test_sentence)

        # initiate the viterbi matrix to store probability of the most likely sequence
        vit_matrix =[[0 for __ in range(length_sentence)] for _ in range(len(self.diftag))]
        vit_matrix[self.diftag.index("<s>")][0]=1

        # some words are not in train dataset. therefore I equalize it to 1/(total_word_count+unique_word)
        # total tag and total word count is same because each word has tag
        laplacer = 1/(self.total_tag_count+self.unique_word_count)
        # I explained below code works in report via Figure xx
        for column_ind in range(1,length_sentence-1):
            word, real_tag = test_sentence[column_ind]
            for to_ind,to_tag in enumerate(self.diftag):
                for from_ind,from_tag in enumerate(self.diftag):
                    p_wi_ti=self.emission_probability[word][to_tag]
                    if p_wi_ti == 0:
                        # if this word hasn't seen in train dataset I give it a tiny chance
                        p_wi_ti=laplacer
                    p_ti1_ti=self.transition_probability[from_tag][to_tag]
                    vit_matrix[to_ind][column_ind] = max(vit_matrix[to_ind][column_ind],
                                                         vit_matrix[from_ind][column_ind-1]*p_wi_ti*p_ti1_ti)

                    
        ############################### The Second step of Viterbi Algorithm ##############################################
        # Backtrace part

        suggested_tags=[]
        for column_ind in range(1,length_sentence-1):
            # print(test_sentence[column_ind]," => ")
            maksi_prob=0
            suggested_tags.append("hulololo") # hulololo is my Spotify list which I was listening while I was coding the assignment 
            for line_ind in range(len(self.diftag)-1,-1,-1):
                if vit_matrix[line_ind][column_ind] >= maksi_prob:
                    # print("\t CHANGE => old:",maksi_prob,"new :",vit_matrix[line_ind][column_ind]," TAG:",self.diftag[line_ind])
                    maksi_prob = vit_matrix[line_ind][column_ind]
                    suggested_tags[-1] = self.diftag[line_ind]
        # print(suggested_tags)
        return suggested_tags
