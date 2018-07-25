# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from sandhisplitter import Sandhisplitter
from sandhisplitter import getInstance
from sandhisplitter.model import Model
from testtools import TestCase
from sandhisplitter.util import extract
from pkg_resources import resource_filename


class TestSandhisplitter(TestCase):
    def setUp(self):
        super(TestSandhisplitter, self).setUp()
        self.model = Model(depth=3, skip=1)
        self.SS = Sandhisplitter()
        testcases = resource_filename("sandhisplitter.tests",
                                      "resources/samples.txt")
        self.entries = open(testcases, "r", encoding='utf-8')

    def test_splits(self):
        count = 0
        entries = map(lambda x: x.strip(), self.entries.readlines())
        for line in entries:
            count += 1
            (word, splits, locs) = extract(line)
            self.model.add_entry(word, splits, locs)
        m = self.model.serialize()
        self.SS.set_model(m)
        for line in entries:
            (word, splits, locs) = extract(line)
            obtained, pos = self.SS.split(word)
            self.assertEqual(locs, pos)
            self.assertEqual(splits, obtained)

    def test_details(self):
        self.assertEqual(self.SS.get_module_name(), "Sandhi-Splitter")
        self.assertEqual(self.SS.get_info(),
                         "Sandhi-splitter for malayalam")

    def test_instance(self):
        self.assertEqual(isinstance(getInstance(), Sandhisplitter), True)
