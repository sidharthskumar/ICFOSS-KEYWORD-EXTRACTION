# -*- coding: utf-8 -*-
import re
import csv


#print(tokens)
tag = ['NNN', 'NNNP', 'NNST', 'VVMVNF', 'VVAUX', 'VVMVF', "VVN"]  # nnn-1 nnnp-2 nnnst-3 verb-4
keywords = dict()
final_result = dict()


def main(wc):
    in_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/tagged_split.txt", 'r', encoding='utf-8')
    f_out = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/features.txt", 'w', encoding='utf-8')
    wl = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/wordlist.txt", 'r', encoding='utf-8')
    wordlist = wl.read()
    wl.close()
    allwords = wordlist.split('\n')
    text = in_file.read()
    in_file.close()
    words = text.split('\n')
    print(words)
    tokens = [tk.split() for tk in words if len(tk.split()) == 2]
    print(tokens)
    id = 1
    # filtering nouns and verbs
    for t in tokens:
        if t[1] in tag:
            #print(t[0], t[1])
            keywords.setdefault(id, []).append(t[0])
            if t[1] == "NNN":
                keywords.setdefault(id, []).append("NNN")
            elif t[1] == "NNNP":
                keywords.setdefault(id, []).append("NNNP")
            elif t[1] == "NNST":
                keywords.setdefault(id, []).append("NNST")
            elif t[1] == "VVMVNF":
                keywords.setdefault(id, []).append("VVMVNF")
            elif t[1] == "VVAUX":
                keywords.setdefault(id, []).append("VVAUX")
            elif t[1] == "VVMVF":
                keywords.setdefault(id, []).append("VVMVF")
            elif t[1] == "VVN":
                keywords.setdefault(id, []).append("VVN")
            else:
                break
            id += 1
    #print(keywords)

    # counting frequency
    for i in keywords.keys():
        count = 0
        values = keywords[i]
        check = values[0]
        re.compile(check, re.UNICODE)
        for j in keywords.values():
            if check == j[0]:
                count += 1
        keywords.setdefault(i, []).append(count)
    #print(keywords)

    #max frequency
    freqs = []
    for k in keywords.values():
        freqs.append(k[2])
    maxfreq = max(freqs)
    print(maxfreq)

    #deleting duplicates
    result = {}
    for key, value in keywords.items():
        if value not in result.values():
            result[key] = value
    #print(result)


    # assigning TF
    wordcount = float(wc)
    for key, value in result.items():
        tf = value[2] / maxfreq
        result[key] = [value[0], value[1], tf]
    # print(result)

    # checking presence in heading and url
    hurl = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/head_url.txt", 'r', encoding='utf-8')
    headurl = hurl.read()
    #cleaning headurl
    headurl = headurl.replace(u'\u200D', '')  # ZERO_WIDTH_JOINER
    headurl = headurl.replace(u'\u200C', '')  # ZERO_WIDTH_NON_JOINER
    headurl = headurl.replace(u'\u200B', ' ')  # ZERO_WIDTH_SPACE
    headurl = headurl.replace(u'\u00A0', ' ')  # NO_BREAK_SPACE

    headurl_words = headurl.split()
    #print(headurl_words)
    for key, value in result.items():
        if value[0] in headurl_words:
            result.setdefault(key, []).append(1)
        else:
            result.setdefault(key, []).append(0)
    #print(result)


    #assigning depth
    for key, values in result.items():
        pos = -1
        for i,check in enumerate(allwords):
            if values[0] == check:
                pos = i
                break
            else:
                continue
        depth = float(pos / wordcount)
        result.setdefault(key, []).append(depth)
    print(result)

    #assigning LEN
    lengs = [len(x) for x in allwords]
    max_len = max(lengs)

    for key, val in result.items():
        LEN = float(len(val[0])/max_len)
        result.setdefault(key, []).append(LEN)
    print(result)


    #writing to features text file
    for value in result.values():
        wd = str(value[0])
        pos = str(value[1])
        tf = str(value[2])
        hu = str(value[3])
        dp = str(value[4])
        ln = str(value[5])
        line = pos + "\t" + tf + "\t" + hu + "\t" + dp + "\t" + ln
        #line = wd + " " + pos + " " + tf + " " + hu + " " + dp + " " + ln
        f_out.write(line+"\n")
    hurl.close()
    f_out.close()
    return result


def featureExtractor(x):
    ret = main(x)
    return ret


#if __name__ == '__main__':
#    main(84)



#with open('features.csv', 'a') as csvfile:
    #fieldnames = ['POS', 'TF', 'Head/URL', 'Depth']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer = csv.writer(csvfile)
    #writer.writeheader()
#    for value in result.values():
        #malword = value[0].encode('utf-8')
#        writer.writerow({'POS': value[1], 'TF': value[2], 'Head/URL': value[3], 'Depth': value[4]})
