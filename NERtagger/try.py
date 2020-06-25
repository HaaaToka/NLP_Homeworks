for i in range(5,1,-1):
    print(i)






"""


import random

a= "b-org,o,b-misc,b-per,i-per,b-loc,i-org,i-misc,i-loc"
a= a.split(",")
print(a)

ifile = open("test.txt","r")
ofile = open("submit.txt","w")

print(ifile.readline(),end="",file=ofile)
for line in ifile.readlines():
    if line=="\n":
        print(file=ofile)
        continue
    line = line.lower().strip().split()
    if random.randint(5,10) == 7:
        line[-1] = a[random.randint(0,7)]
    print(" ".join(line),file=ofile)

"""