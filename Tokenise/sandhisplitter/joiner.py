# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from sandhisplitter.util import invVT


class Joiner:
    # ha, this needs to be substituted, can't capture these
    # all based on rules.
    # Another time, even space separated joins are gramatically
    # valid.

    def join(self, first, second):
        if(first[len(first) - 1] == '്'):
            if(second[0] in invVT.keys()):
                first = first[0:len(first) - 1]
                second = invVT[second[0]] + second[1:]

        elif(first[len(first) - 1] == 'ം'):
            if second[0] in invVT.keys():
                first = first[0:len(first) - 1] + 'മ'
                second = invVT[second[0]] + second[1:]

        elif(second[0] in invVT.keys()):
            first = first + 'യ'
            second = invVT[second[0]] + second[1:]

        # elif(second[0] in doubling):
            # if(first[len(first)-1] )
            # second = second[0]+'്'+second

        return first + second

    def join_words(self, words):
        concat = None
        for word in words:
            if concat is None:
                concat = word
            else:
                concat = self.join(concat, word)
        return concat
