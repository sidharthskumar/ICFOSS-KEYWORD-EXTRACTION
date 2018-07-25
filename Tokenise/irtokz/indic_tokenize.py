#!/usr/bin/env python
# -*- coding=utf-8 -*-

import re
import os.path

class tokenize_ind():
    def __init__(self, lang='mal', split_sen=True):
        self.lang = lang
        self.split_sen = split_sen
        #file_path = os.path.abspath(__file__).rpartition('/')[0]

        self.mal = True

        #load nonbreaking prefixes from file
        self.NBP = dict()
        with open('/home/sid/icfoss/ICFOSS-KeyWord-Extractor/Tokenise/data/NONBREAKING_PREFIXES') as fp:
            for line in fp:
                if line.startswith('#'):
                    continue
                if '#NUMERIC_ONLY#' in line:
                    self.NBP[line.replace('#NUMERIC_ONLY#', '').split()[0]] = 2
                else:
                    self.NBP[line.strip()] = 1
    
        #precompile regexes
        self.fit()

    def fit(self):
        # remove junk characters
        self.junk = re.compile('[\x00-\x1f]')
        # seperate out on Latin-1 supplementary characters
        self.latin = re.compile(u'([\xa1-\xbf\xd7\xf7])')
        # seperate out on general unicode punctituations except "’"
        self.upunct = re.compile(u'([\u2012-\u2018\u201a-\u206f])')
        # seperate out on unicode mathematical operators
        self.umathop = re.compile(u'([\u2200-\u2211\u2213-\u22ff])')
        # seperate out on unicode fractions
        self.ufrac = re.compile(u'([\u2150-\u2160])')
        # seperate out on unicode superscripts and subscripts
        self.usupsub = re.compile(u'([\u2070-\u209f])')
        # seperate out on unicode currency symbols
        self.ucurrency = re.compile(u'([\u20a0-\u20cf])')
        # seperate out all "other" ASCII special characters
        self.specascii = re.compile(r'([!@#$%^&*\'(),_\-+={\[}\]|";:<>?`~/])')
        #self.specascii = re.compile(u"([^\u0080-\U0010ffffa-zA-Z0-9\s\.',-])")
        self.english = re.compile(r'([a-zA-Z])')
        #remove dots
        self.dots = re.compile(r'([.])')


        #split contractions right (both "'" and "’")
        self.numcs = re.compile(u"([0-9\u0966-\u096f])(['\u2019])s")
        self.aca = re.compile(u"([a-zA-Z\u0080-\u024f])(['\u2019])([a-zA-Z\u0080-\u024f])")
        self.acna = re.compile(u"([a-zA-Z\u0080-\u024f])(['\u2019])([^a-zA-Z\u0080-\u024f])")
        self.nacna = re.compile(u"([^a-zA-Z\u0080-\u024f])(['\u2019])([^a-zA-Z\u0080-\u024f])")
        self.naca = re.compile(u"([^a-zA-Z0-9\u0966-\u096f\u0080-\u024f])(['\u2019])([a-zA-Z\u0080-\u024f])")

        #restore multi-dots
        #self.restoredots = re.compile(r'(DOT)(\1*)MULTI')
        #self.restoreviram = re.compile(r'(PNVM)(\1*)MULTI')
        #self.restoredviram = re.compile(r'(DGVM)(\1*)MULTI')

        #split sentences 
        #self.splitsenir1 = re.compile(u' ([|.?\u0964\u0965]) ([\u0900-\u0d7f\u201c\u2018A-Z])')
        #self.splitsenir2 = re.compile(u' ([|.?\u0964\u0965]) ([\)\}\]\'"\u2019\u201d> ]+) ')

    def normalize(self, text):
        """
        Performs some common normalization, which includes: 
            - Byte order mark, word joiner, etc. removal
            - ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces 
        """
        text = text.replace(u'\uFEFF', '')     #BYTE_ORDER_MARK
        text = text.replace(u'\uFFFE', '')     #BYTE_ORDER_MARK_2
        text = text.replace(u'\u2060', '')     #WORD_JOINER
        text = text.replace(u'\u00AD', '')     #SOFT_HYPHEN
        text = text.replace(u'\u200B', ' ')    #ZERO_WIDTH_SPACE
        text = text.replace(u'\u00A0', ' ')    #NO_BREAK_SPACE
        text = text.replace(u'\u200D', '')     #ZERO_WIDTH_JOINER
        text = text.replace(u'\u200C', '')     #ZERO_WIDTH_NON_JOINER
        return text

    def tokenize(self, text):
        # text = text.decode('utf-8', 'ignore')
        text = self.normalize(text)
        text = '%s' %(text)
        # remove junk characters
        text = self.junk.sub('', text)
        #remove Latin-1 supplementary characters
        text = self.latin.sub('', text)
        #remove general unicode punctituations except "’"
        text = self.upunct.sub('', text)
        #remove unicode mathematical operators
        text = self.umathop.sub('', text)
        # separate out on unicode fractions
        #text = self.ufrac.sub('', text)
        #remove superscripts and subscripts
        text = self.usupsub.sub('', text)
        #remove unicode currency symbols
        text = self.ucurrency.sub('', text)
        #remove all "other" ASCII special characters
        text = self.specascii.sub('', text)


        #split contractions right (both "'" and "’")
        text = self.nacna.sub(r"\1 \2 \3", text)
        text = self.naca.sub(r"\1 \2 \3", text)
        text = self.acna.sub(r"\1 \2 \3", text)
        text = self.aca.sub(r"\1 \2\3", text)
        text = self.numcs.sub(r"\1 \2s", text)
        text = text.replace("''", " ' ' ")

        #handle non breaking prefixes
        wrds = text.split()
        text = ""
        #print(wrds)
        for w in wrds:
            if '.' in w:
                if w[0].isalpha():
                    pass
                else:
                    w = self.dots.sub(' ', w)
                    #w = self.english.sub('', w)

            else:
                #remove English characters
                w = self.english.sub('', w)
            text += "%s " % w
        #print(text)

        words = text.split()
        text = str()
        for word in words:
            if word.endswith('.'):
                word = self.dots.sub(' ', word)
            text += "%s " % word

        #seperate out "," except for Malayalam and Ascii digits
        #text = re.sub(u'([^0-9\u0d66-\u0d6f]),', r'\1 , ', text)
        #text = re.sub(u',([^0-9\u0d66-\u0d6f])', r' , \1', text)
        #separate out on Malayalam characters followed by non-Malayalam characters
        #text = re.sub(u'([\u0D00-\u0D65\u0D73-\u0D7f])([^\u0D00-\u0D65\u0D73-\u0D7f\u2212-]|[\u0964-\u0965])', r'\1 \2', text)
        #separate out Non malayalam followed by malayalam
        #text = re.sub(u'([^\u0D00-\u0D65\u0D73-\u0D7f\u2212-]|[\u0964-\u0965])([\u0D00-\u0D65\u0D73-\u0D7f])', r'\1 \2', text)
        #seperate out Malayalam fraction symbols
        text = re.sub(u'([\u0d73\u0d74\u0d75])', r' \1 ', text)
        
        #seperate out hyphens 
        #text = self.multihyphen.sub(lambda m: r'%s' %(' '.join('-'*len(m.group(1)))), text)
        #text = re.sub(u'(-?[0-9\u0d66-\u0D72]-+[0-9\u0d66-\u0D72]-?){,}',lambda m: r'%s' %(m.group().replace('-', '')), text)
        #text = text.split()
        #text = ' '.join(text)

        #restore multiple dots
        #text = self.restoredots.sub(lambda m: r'.%s' % ('.' * (len(m.group(2)) / 3)), text)

        #split sentences
        #if self.split_sen:
        #        text = self.splitsenir1.sub(r' \1\n\2', text)
        #        text = self.splitsenir2.sub(r' \1 \2\n', text)
        return text

