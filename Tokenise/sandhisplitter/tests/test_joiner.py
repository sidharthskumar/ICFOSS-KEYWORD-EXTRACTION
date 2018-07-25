# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from sandhisplitter.joiner import Joiner
from testtools import TestCase
from sandhisplitter.util import extract
from pkg_resources import resource_filename


class TestJoiner(TestCase):
    def setUp(self):
        super(TestJoiner, self).setUp()
        self.J = Joiner()
        testcases = resource_filename("sandhisplitter.tests",
                                      "resources/join_cases.txt")
        self.entries = open(testcases, "r", encoding='utf-8')

    def test_splits(self):
        for line in self.entries:
            (word, splits, locs) = extract(line)
            word_joined = self.J.join_words(splits)
            self.assertEqual(word, word_joined)
