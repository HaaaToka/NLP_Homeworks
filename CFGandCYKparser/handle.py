from collections import defaultdict
from string import punctuation,ascii_uppercase,ascii_lowercase
from random import randint


def go_deep(current, magic):
    while current in magic.keys():
        current = list(magic[current])[0]
    return current

def rules(path):
    """
        It takes only one argument:  folder path and returns CFG rule set and X matter-powerpuff girls-
    """
    infile = open(path,"r")

    magic = defaultdict(set) # cyk triangular matrix
    cfg_rules = defaultdict(set)
    irregulars = []
    
    for line in infile.readlines():
        line = line.strip().split("#")[0].split()

        if len(line):
            if line[-1] in punctuation:
                irregulars.append(line)
            else:
                ismix=0            
                for elem in line[1:]:
                    if elem not in punctuation and elem[0] in ascii_lowercase:
                        ismix+=1
                        break
                for elem in line[1:]:
                    if elem not in punctuation and elem[0] in ascii_uppercase:
                        ismix-=1
                        break

                if ismix == 0:
                    # it is irregular such as "is it true that S"
                    irregulars.append(line) 
                else:
                    magic[" ".join(line[1:])].add(line[0])
                    cfg_rules[line[0]].add(" ".join(line[1:]))

    irrc=0
    nonName = "IRREGULAR"
    for i in range(len(irregulars)):
        print(irregulars[i])
        for j in range(1,len(irregulars[i])):
            if irregulars[i][j] in punctuation or irregulars[i][j][0] in ascii_lowercase:
                print("\t->",irregulars[i][j])
                if irregulars[i][j] in magic.keys():
                    irregulars[i][j]=go_deep(list(magic[irregulars[i][j]])[0],magic)
                else:
                    while nonName+str(irrc) in cfg_rules.keys():
                        irrc+=1
                    cfg_rules[nonName+str(irrc)].add(irregulars[i][j])
                    magic[irregulars[i][j]].add(nonName+str(irrc))
                    irregulars[i][j] = nonName+str(irrc)

        while len(irregulars[i])>=3:
            print("  ->"," ".join(irregulars[i]),"\\newline")
            if " ".join(irregulars[i][1:3]) in magic.keys(): #stupid check
                irregulars[i][1]=list(magic[" ".join(irregulars[i][1:3])])[0]
            else:
                while nonName+str(irrc) in cfg_rules.keys():
                    irrc+=1
                cfg_rules[nonName+str(irrc)].add(" ".join(irregulars[i][1:3]))
                magic[" ".join(irregulars[i][1:3])].add(nonName+str(irrc))
                irregulars[i][1]=nonName+str(irrc)
            irregulars[i].pop(2)
        print("  ->"," ".join(irregulars[i]),"\\newline")

        magic[" ".join(irregulars[i][1:])].add(irregulars[i][0])
        cfg_rules[irregulars[i][0]].add(" ".join(irregulars[i][1:]))

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
        sentence.append("ROOT")
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
            if cfg_rules[randRule][0][0] not in ascii_uppercase:
                sentence.append(cfg_rules[randRule][randint(0,len(cfg_rules[randRule])-1)])
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
                # print("\t",triangle[sentence[i]],"- -tpye: ",type(triangle[sentence[i]])," - - str :",str(triangle[sentence[i]]))
                if sentence[i] not in triangle.keys():
                    triangle[curX].add(sentence[i])
                else:
                    triangle[curX].add(go_deep(list(triangle[sentence[i]])[0],triangle))
                #print("\t",triangle[curX])
            else:
                # print("cumulative -> "+curX+" ::: "," ".join(sentence[i:j+1]))
                mid = i
                while mid<j:
                    left = "X {0} {1}".format(i,mid)
                    right = "X {0} {1}".format(mid+1,j)
                    # print("\t",left,":",triangle[left],"<- :: ->",right,":",triangle[right])
                    products = [[l,r] for l in list(triangle[left]) for r in list(triangle[right])]
                    # print( "\t\t", products )
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

    isgrammaticly=0
    if triangle[curX]:
        isgrammaticly = triangle[list(triangle[curX])[0]]
        print("Is Above Sentence Grammatically Correct :", "YES" if triangle[list(triangle[curX])[0]] else "NO",file=outF)
    else:
        print("Is Above Sentence Grammatically Correct : NO",file=outF)
    outF.close()

    return isgrammaticly

def main():
    # cfg_file_path = "./cfg.gr"
    cfg_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\CFGandCYKparser\\cfg.gr"

    # sentenceFile = "./sentence.txt"
    sentenceFile = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\CFGandCYKparser\\sentence.txt"

    magic_dict,cfg_dict=rules(cfg_file_path)
    cfg_dict=dict(cfg_dict)

    generated_sentence = randsentence(cfg_dict,sentenceFile)
    print("Generated Sentence => ",generated_sentence)
    print("Is Above Sentence Grammatically Correct :", "YES" if CYKParser(generated_sentence,cfg_dict,magic_dict,sentenceFile) else "NO")

    print(">>>>>", "YES" if CYKParser("i want you .",cfg_dict,magic_dict,sentenceFile) else "NO")

if __name__ == "__main__":
    main()