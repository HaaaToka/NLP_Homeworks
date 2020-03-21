a=["okan","alan","ohmet","memet","onur","fatih"]
zipa = zip(*[a[i:] for i in range(2)])
for x in zipa:
    print(x)
print([" ".join(x) for x in zipa])



"""         line_number=1
        line_number+=1
    if line_number%22 == 0:
        result_regex = re.search("(([A-Za-z]*)\|)+",line)
        if result_regex is not None:
            print(line) """