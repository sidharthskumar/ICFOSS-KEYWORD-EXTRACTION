from Tokenise.irtokz.indic_tokenize import tokenize_ind
#from sandhisplitter import Sandhisplitter

inp_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Tokenise/scrapped_text.txt", "r", encoding="utf-8")
out_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tokenized_text.txt", "w", encoding="utf-8")
allwords = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/wordlist.txt", "w", encoding='utf-8')


def main():
    inp = inp_file.read()
    language = "mal"
    tok = tokenize_ind(lang="'"+language+"'", split_sen=True)
    text = tok.tokenize(inp)
    #print(text)

    #tokenizing to words
    words = text.split()
    tokens = [tk for tk in words if tk not in ["'" '.' ',']]
    print(tokens)

    #sandhi splitting
    #tks = []
    #s = Sandhisplitter()
    #for w in tokens:
    #     split = s.split(w)
    #     #print(split)
    #     if len(split) == 2:
    #         if len(split[0]) <= 4:
    #             #tks.append(split[0] + split[1])
    #             tks.append(s.join(split))
    #         else:
    #             tks.append(split[0])
    #     elif len(split) == 3:
    #         wd = s.join(split[0:1])
    #         tks.append(wd)
    #     elif len(split) == 1:
    #         tks.append(split[0])
    # print(tks)

    #print to output files
    for t in tokens:
        out_file.write("%s\n" % t)
        allwords.write("%s\n" % t)
    out_file.close()
    inp_file.close()
    allwords.close()

    number_of_words = len(tokens)
    print(number_of_words)
    return number_of_words

def tokenizer():
    wc = main()
    return wc

if __name__ == '__main__':
    main()

