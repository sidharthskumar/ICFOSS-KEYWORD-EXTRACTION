from irtokz.indic_tokenize import tokenize_ind
import re


# test_file = open("test.txt", "w", encoding="utf-8")

def splitTagged():
    in_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tagged_text.txt", "r", encoding="utf-8")
    lines = in_file.readlines()
    del lines[0:12]
    del lines[-3:]
    in_file.close()
    in_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tagged_text2.txt", "w", encoding="utf-8")
    in_file.writelines(lines)
    in_file.close()
    in_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tagged_text2.txt", "r", encoding="utf-8")
    inp = in_file.read()
    in_file.close()

    # reformatting tagged tokens
    text = inp
    # remove dot from abbrevations
    #text = re.sub(u'([\u0D00-\u0D65\u0D73-\u0D7f])-?([\u002e])', r'\1', text)
    text = text.replace('\t', "")
    text = text.replace('_', "")
    text = re.sub(u'([\u0D00-\u0D65\u0D73-\u0D7f])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(u'([1234567890])([a-zA-Z])', r'\1 \2', text)

    out_file = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features/tagged_split.txt", "w", encoding="utf-8")
    #print(text)
    out_file.write("%s" % text)
    out_file.close()


#if __name__ == '__main__':
#    splitTagged()
