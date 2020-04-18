from bigram_hmm import HMM
import csv


def dataset(filepath):
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
    mids = [[]]

    infile.readline() # to pass -DOCSTART- -X- -X- O
    infile.readline() # to pass blank line
    
    temp_sentence = [["<s>","<s>"]]
    for line in infile.readlines():
        if line == "\n":
            temp_sentence.append(["</s>","</s>"])
            sentences.append(temp_sentence)
            temp_sentence=[["<s>","<s>"]]
            mids.append([])
        elif line=="-DOCSTART- -X- -X- O\n":
            infile.readline()
            pass
        else:
            line = line.lower().strip().split()
            # take word and its named entity tag
            temp_sentence.append( [line[0],line[3]] )
            mids[-1].append( [line[1],line[2]] )

    infile.close()

    return mids,sentences


def accuracy(gold_sequence,predicted_sequence):
    print("CALCULATING ACCURACY WAS STARTED")
    correct = 0
    total = 0
    for i in range(len(gold_sequence)):
        #print(gold_sequence[i][1:],len(gold_sequence[i]),"\n",predicted_sequence[i],len(predicted_sequence[i]))
        for t_i in range(1,len(gold_sequence[i])-2):
            total+=1
            if gold_sequence[i][t_i][1] == predicted_sequence[i][t_i]:
                correct +=1
    print(correct,total,correct/total)
    return(correct/total) 


def main():

    train_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\NERtagger\\train.txt"
    test_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\NERtagger\\test.txt"
    output_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\NERtagger\\output.csv"
    outFile = open(output_file_path,"w",newline="")
    writer = csv.writer(outFile,delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Id","Category"])
    bigram_hmm = HMM()

    train_middles, train_sentences = dataset(train_file_path)
    test_middles, test_sentences = dataset(test_file_path)

    bigram_hmm.HMM(train_sentences)
    
    suggested_tags = []
    wordnumber=1
    print("VITERBI WAS STARTED")
    for t_s in test_sentences:
        suggested_tags.append( bigram_hmm.viterbi(t_s) )
        for tag in suggested_tags[-1]:
            writer.writerow([wordnumber,tag.upper()])
            wordnumber+=1
    
    outFile.close()

    accuracy(test_sentences,suggested_tags)


    


if __name__ == "__main__":
    main()   