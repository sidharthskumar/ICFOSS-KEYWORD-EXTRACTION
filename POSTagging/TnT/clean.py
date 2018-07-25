f_in = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/TnT/new_corpus.txt", "r", encoding='utf-8')
f_out = open("/home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/TnT/clean_corpus2.txt", 'w', encoding='utf-8')
text = f_in.read()
text = text.replace(u'\uFEFF', '')     #BYTE_ORDER_MARK
text = text.replace(u'\uFFFE', '')     #BYTE_ORDER_MARK_2
text = text.replace(u'\u2060', '')     #WORD_JOINER
text = text.replace(u'\u00AD', '')     #SOFT_HYPHEN
text = text.replace(u'\u200B', ' ')    #ZERO_WIDTH_SPACE
text = text.replace(u'\u00A0', ' ')    #NO_BREAK_SPACE
text = text.replace(u'\u200D', '')     #ZERO_WIDTH_JOINER
text = text.replace(u'\u200C', '')
dirty = text.split('\n')
clean = []
for i in dirty:
    if i not in clean:
        clean.append(i)

for j in clean:
    f_out.write("%s\n" % j)
f_in.close()
f_out.close()

