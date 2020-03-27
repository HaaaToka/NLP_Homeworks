import itertools  
import operator  
result = itertools.accumulate([1,2,3,4,5], operator.add)  
print(list(result))


from random import randint
a= {"lo":1,"hel":2,"ha":3,"ko":4}
a["kel"]=5
a["gel"]=6
a["mel"]=7
a["del"]=8
a["zel"]=9
a["fel"]=0
for k,v in a.items():
    print(k,":",v)


"""         line_number=1
        line_number+=1
    if line_number%22 == 0:
        result_regex = re.search("(([A-Za-z]*)\|)+",line)
        if result_regex is not None:
            print(line) """