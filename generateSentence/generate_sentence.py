
import re
from string import punctuation
from language_model import LanguageModel

def dataset(folderPath):
    """
        Actually this function is useless because we use extra memory space to store all sentences but I have to write this function
        It would be more efficient if I count the words sentence by sentence instead of reading and storing the whole file 
        because we use only count of words to generate sentence
    """
    dataFile = open(folderPath+"\\assignment1-dataset.txt","r") # for windows
    # dataFile = open(folderPath+"/assignment1-dataset.txt","r") # for linux
    sentences = []

    line_number = 0
    for line in dataFile.readlines():
        line_number+=1
        if line_number%22 == 0:
            """
                there is a blank line in each twenty-two lines 
                Each twente-first line contains XXXXX and aaaa|bbbb|cccc.
                I delete "aaaa|bbbb|cccc" part.
                I replace the XXXXX part with the answer that is at the end of the line.
            """
            sentences[-1] = sentences[-1].split("\t\t")[0]
            answer = sentences[-1].split("\t")[1]
            sentences[-1] = sentences[-1].split("\t")[0]
            sentences[-1] = sentences[-1].replace("XXXXX",answer)
            # print("-->>",answer, ":", sentences[-1])
        else:
            sentences.append(line)

        """ if line_number == 50000:
            break """
    
    print("DATASET FILE HAS READ")
    return sentences

def main():

    # path = input ("Where is the dataset(assignment1-dataset.txt)? Give me folder path : ")
    path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\generateSentence"
    """ NN_grams = input('''Which grams model you want? 
                        \nUnigram -> 1, Bigram -> 2, Trigram ->3 and so on. 
                        \nGive me your wanted ''') """
    NN_grams = 2

    sentences = dataset(path)

    ngram_language_model = LanguageModel(NN_grams)
    ngram_language_model.LoadDataset2Model(sentences)
    generated_sentences = ngram_language_model.Generate(20,10)

    print(ngram_language_model.Prob(generated_sentences[-1]))
    print(ngram_language_model.PPL(generated_sentences[-1]))



if __name__ == "__main__":
    main()   