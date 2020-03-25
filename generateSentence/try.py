import itertools  
import operator  
result = itertools.accumulate([1,2,3,4,5], operator.add)  
print(list(result))


from random import randint
a= {"lo":[{"hel":4,"ha":5,"ko":1},10]}
print(randint(1,a["lo"][1]))


"""         line_number=1
        line_number+=1
    if line_number%22 == 0:
        result_regex = re.search("(([A-Za-z]*)\|)+",line)
        if result_regex is not None:
            print(line) """