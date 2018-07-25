# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from sandhisplitter.util import vowelT
from sandhisplitter.util import split_word_at_locations


class PostProcessor:
    def transform(self, first, second):
        """
        Applies morphophonemic changes, rule based for now
        Transforms Wx, yZ -> Wx' + y'Z.
        """

        # ya additions
        if(first[-1] == u'യ' and second[0] in vowelT.keys()):
            first = first[:-1]
            second = vowelT[second[0]] + second[1:]

        # ma - am
        elif(first[-1] == u'മ' and second[0] in vowelT.keys()):
            first = first[:-1] + u'ം'
            second = vowelT[second[0]] + second[1:]

        # kkV = kk~ + char(V)
        elif(second[0] in vowelT):
            first = first + u'്'
            second = vowelT[second[0]] + second[1:]

        # Doubling
        if(len(second) >= 3):
            x, y, z = second[:3]
            double = False
            if(x == z and y == u'്'):
                if(first[-1] == 'യ'):
                    first = first[:-1]
                elif(first[-1] == 'മ'):
                    first = first[:-1] + u'ം'
                else:
                    double = True

                if double:
                    second = second[2:]
                else:
                    second = 'അ'+second
        return (first, second)

    def split(self, word, locations):
        """
        Applies transform to wordsat each
        location provided in locations
        """
        splits = split_word_at_locations(word, locations)
        word_count = len(splits)
        for i in range(word_count-1):
            first, second = splits[i:i+2]
            first, second = self.transform(first, second)
            splits[i] = first
            splits[i+1] = second
        return splits
