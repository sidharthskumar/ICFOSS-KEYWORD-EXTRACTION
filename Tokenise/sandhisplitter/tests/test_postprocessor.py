# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from sandhisplitter.postprocessor import PostProcessor
from testtools import TestCase
from sandhisplitter.util import extract
from pkg_resources import resource_filename


class TestPostProcessor(TestCase):
    def setUp(self):
        super(TestPostProcessor, self).setUp()
        self.PP = PostProcessor()
        testcases = resource_filename("sandhisplitter.tests",
                                      "resources/samples.txt")
        self.entries = open(testcases, "r", encoding='utf-8')

    def test_splits(self):
        for line in self.entries:
            (word, splits, locs) = extract(line)
            splits_generated = self.PP.split(word, locs)
            self.assertEqual(splits, splits_generated)
