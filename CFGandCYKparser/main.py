from collections import defaultdict
from string import punctuation,ascii_uppercase
from random import randint
import re


def rules(path):
    """
        It takes only one argument:  folder path and returns CFG rule set and X matter-powerpuff girls-
    """
    infile = open(path,"r")

    magic = defaultdict(set) # cyk triangular matrix
    cfg_rules = defaultdict(set)
    
    for line in infile.readlines():
        line = line.strip().split("#")[0]
        if line!='' and line[:4]!="ROOT":
            """ print("->",line)
            print("\t->",re.findall(r'[a-zA-Z]+',line)) """
            line = re.findall(r'[a-zA-Z]+',line)
            magic[" ".join(line[1:])].add(line[0])
            cfg_rules[line[0]].add(" ".join(line[1:]))

    for k in cfg_rules.keys():
        cfg_rules[k] = list(cfg_rules[k])

    return magic,cfg_rules


def randsentence(cfg_rules,output_file_path):
    """
        It takes CFG rule set and name of the output file and returns generated sentences (Also they will be written to the output file) 
    """

    sentence = []

    coin = randint(0,1)
    if coin:
        print("GENERATING RULE-BASED SENTENCE WAS STARTED")
        sentence.append("S")
        flag=1
        while flag:
            flag=0
            for _ in range(len(sentence)):
                #print("Sentence ==>",sentence)
                curRule=sentence.pop(0)
                if curRule[0] in ascii_uppercase:
                    tempNew = curRule.split()
                    if tempNew[0]==curRule:
                        sentence.append(cfg_rules[curRule][randint(0,len(cfg_rules[curRule])-1)])
                    else:
                        sentence+=tempNew         
                    flag=1
                else:
                    sentence.append(curRule)
                    
    else:
        print("GENERATING RANDOM SENTENCE WAS STARTED")
        sentence_word_count = randint(5,10)
        lenKi = len(cfg_rules.keys())
        kiys = list(cfg_rules.keys())
        
        while sentence_word_count:
            randRule = kiys[randint(0,lenKi-1)]
            randWord = cfg_rules[randRule][randint(0,len(cfg_rules[randRule])-1)]
            if randWord[0] not in ascii_uppercase:
                sentence.append(randWord)
                sentence_word_count-=1

    outF = open(output_file_path,"w")
    print(" ".join(sentence),file=outF)
    outF.close()

    return " ".join(sentence)

def CYKParser(sentence,rules,triangle,output_file_path):
    """
        It takes a sentence and print whether this sentence is grammati-cally correct or not
    """
    sentence=["<s>"]+sentence.split()
    
    curX=""
    for stop in range(len(sentence)-1):
        #print("stop:",stop)
        for i in range(1,len(sentence)-stop):
            j=i+stop
            curX = "X {0} {1}".format(i,j)
            if i==j:
                #print("elementary -> "+curX+" ::: "+sentence[i])
                #print("\t",triangle[sentence[i]],"- -tpye: ",type(triangle[sentence[i]])," - - str :",str(triangle[sentence[i]]))
                if sentence[i] not in triangle.keys():
                    triangle[curX].add(sentence[i])
                else:
                    if sentence[i] in triangle.keys():
                        temp=list(triangle[sentence[i]])[0]
                        while temp in triangle.keys():
                            #print("\t\t\t----TEMP ",temp,"--- magic[temp]",triangle[temp])
                            temp = list(triangle[temp])[0]
                        triangle[curX].add(temp)
                    else:
                        triangle[curX].add(sentence[i])
            else:
                #print("cumulative -> "+curX+" ::: "," ".join(sentence[i:j+1]))
                mid = i
                while mid<j:
                    left = "X {0} {1}".format(i,mid)
                    right = "X {0} {1}".format(mid+1,j)
                    #print("\t",left,":",triangle[left],"<- :: ->",right,":",triangle[right])
                    products = [[l,r] for l in list(triangle[left]) for r in list(triangle[right])]
                    #print( "\t\t", products )
                    for product in products:
                        for merge in triangle[" ".join(product)]:
                            triangle[curX].add(merge)
                    mid+=1

    outF = open(output_file_path,"a+")
    for stop in range(len(sentence)-1):
        for i in range(1,len(sentence)-stop):
            j=i+stop
            tempX = "X {0} {1}".format(i,j)
            if len(triangle[tempX]):
                print(triangle[tempX],end="\t",file=outF)
            else:
                print("XXX",end="\t",file=outF)
        print(file=outF)
    print("Is Above Sentence Grammatically Correct :", "YES" if triangle[curX]=={"S"} else "NO",file=outF)
    outF.close()

    return 1 if triangle[curX]=={"S"} else 0

def main():
    # cfg_file_path = "./cfg.gr"
    cfg_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\CFGandCYKparser\\cfg.gr"

    # sentenceFile = "./sentence.txt"
    sentenceFile = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\CFGandCYKparser\\sentence.txt"

    magic_dict,cfg_dict=rules(cfg_file_path)
    cfg_dict=dict(cfg_dict)
    #print(magic_dict)
    #print(cfg_dict)

    generated_sentence = randsentence(cfg_dict,sentenceFile)
    print("Generated Sentence => ",generated_sentence)
    print("Is Above Sentence Grammatically Correct :", "YES" if CYKParser(generated_sentence,cfg_dict,magic_dict,sentenceFile) else "NO")
    #print("Is Above Sentence Grammatically Correct :", "YES" if CYKParser("i with this sandwich ate every mouse from that beautiful president under that mouse",cfg_dict,magic_dict,sentenceFile) else "NO")

if __name__ == "__main__":
    main()