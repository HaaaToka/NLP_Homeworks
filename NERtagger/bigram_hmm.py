from collections import defaultdict


def DefaultdictInside():
    return defaultdict(int)

class HMM():

    initial_probability = defaultdict(int)
    transition_probability = defaultdict(DefaultdictInside)
    emission_probability = defaultdict(DefaultdictInside)

    total_tag_count=0
    diftag=set()

    def __init__(self):
        print("GENERATED Bigram_HMM")

    def dataset(self,filepath):
        """
            The CoNLL-2003 shared task data files contain four columns separated by a single space.
            The first item on each line is a word, the second a part-of-speech (POS) tag, the third a syntactic chunk tag and the fourth the named entity tag
            The chunk tags and the named entity tags have the format I-TYPE which means that the word is inside a phrase of type TYPE.
            Only if two phrases of the same type immediately follow each other, the first word of the second phrase will have tag B-TYPE to show that it starts a new phrase
            A word with tag O is not part of a phrase
            https://www.clips.uantwerpen.be/conll2003/ner/
        """
        print("READING FILE WAS STARTED")

        infile = open(filepath,"r")
        sentences = []

        infile.readline() # to pass -DOCSTART- -X- -X- O
        infile.readline() # to pass blank line
        
        temp_sentence = ""
        for line in infile.readlines():
            if line == "\n":
                sentences.append(temp_sentence.lower())
                temp_sentence=""
            else:
                line = line.strip().split()
                # take word and its named entity tag
                """
                    preprocessing CHECK HERE !!!!!!!
                """
                temp_sentence += line[0]+"/"+line[3]+" "

        infile.close()

        return sentences


    def HMM(self,sentences):
        """
            TASK 1: BUILD a Bigram-Hidden Markov Model
        """
        print("MODEL CREATION WAS STARTED")

        for sentence in sentences:
            tokens = sentence.split()

            try:
                prev_word, prev_tag = tokens[0].split("/")
            except:
                continue
            self.initial_probability[prev_tag]+=1
            self.emission_probability[prev_tag][prev_word]+=1
            self.diftag.add(prev_tag)
            for token in tokens[1:]:
                #print(token)
                """
                    DEL try-except block after preprocessing at below and above
                """
                try:
                    cur_word, cur_tag = token.split("/")
                except:
                    continue
                self.initial_probability[cur_tag]+=1
                self.transition_probability[prev_tag][cur_tag]+=1
                self.emission_probability[cur_tag][cur_word]+=1
                
                self.diftag.add(cur_tag)

                prev_word = cur_word
                prev_tag = cur_tag

        # P(ti+1|ti) -> Transition Probability Evaluation -> C(ti,ti+1) / C(ti+1)
        for ti_1,tis in self.transition_probability.items():
            # temp_denominator = sum(tis.values())
            for ti in tis.keys():
                self.transition_probability[ti_1][ti] /= self.initial_probability[ti]
        
        # P(wi|ti) -> Emission Probability Evaluation -> C(wi,ti) / C(ti)
        for tag, words in self.emission_probability.items():
            # temp_denominator = sum(words.values())
            for w in words.keys():
                self.emission_probability[tag][w] /= self.initial_probability[tag]

        # Initial Probabilty Evaluation
        self.total_tag_count = sum(self.initial_probability.values())
        for k in self.initial_probability.keys():
            self.initial_probability[k] /= self.total_tag_count


        print(self.diftag)


    

    def viterbi(self,test_sentences):
        """
            HELLO
        """
        print("viterbi")



    def accuracy(self,gold_sequence,predicted_sequence):
        """
            HELLO
        """
        print("accuracy")