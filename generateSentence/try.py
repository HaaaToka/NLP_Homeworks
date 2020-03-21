word_list = ['<s>', 'with', 'almost', 'everything', 'else', 'to', 'make', 'them', 'happy', 'they', 'wanted', 'one', 'thing', 'they', 'had', 'no', 'children', '</s>']
jo =[ " ".join(gram) for gram in zip(*[word_list[i:] for i in range(2)])]
print(jo)

"""         line_number=1
        line_number+=1
    if line_number%22 == 0:
        result_regex = re.search("(([A-Za-z]*)\|)+",line)
        if result_regex is not None:
            print(line) """