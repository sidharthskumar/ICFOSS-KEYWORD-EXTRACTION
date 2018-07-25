import subprocess
file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Extraction/output.txt", 'r')
r = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/uploadr/templates/read.txt", 'w')

def main(dictr):
    f = file.read()
    line = f.split('\n')
    feat = [l.split() for l in line]
    end = len(feat)-1
    feat.__delitem__(end)
    #print(feat)
    #print(len(feat))
    labels = [l[5] for l in feat[:-1]]
    #labels = [l[5] for l in feat[:-1]]
    #print(labels)
    #print(len(labels))
    #print(dictr)
    print(len(dictr))
    keywords = []

    malwords = []
    for val in dictr.values():
        malwords.append(val[0])

    #print(malwords)
    i = 0
    for lab in labels:
        if lab == "B_K":
            value = malwords[i]
            keywords.append(value)
            i+=1
        else:
            i+=1
            continue

    file.close()
    print(keywords) #final keyword output
    print(len(keywords))#no of keywords
    for i in keywords:
        r.write(i+"\n")
    subprocess.call(['./goto.sh'])
def extraction(d):
    main(d)

#if __name__ == '__main__':
#    main()
