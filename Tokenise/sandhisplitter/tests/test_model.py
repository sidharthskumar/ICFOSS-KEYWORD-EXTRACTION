# -*- coding: utf-8 -*-
from io import open
from sandhisplitter.model import Model
from testtools import TestCase
from sandhisplitter.util import extract
from pkg_resources import resource_filename


class TestModel(TestCase):
    def setUp(self):
        super(TestModel, self).setUp()
        self.testModel = Model(depth=3, skip=1)
        testcases = resource_filename("sandhisplitter.tests",
                                      "resources/samples.txt")
        self.entries = open(testcases, "r", encoding='utf-8')

    def test_load(self):
        count = 0
        firstline = None
        for line in self.entries:
            count += 1
            if count == 1:
                firstline = line
            (word, splits, locs) = extract(line)
            self.testModel.add_entry(word, splits, locs)
        m = self.testModel.serialize()
        self.testModel.load(m)
        self.assertEqual(self.testModel.k, 3)
        self.assertEqual(self.testModel.initial_skip, 1)
        self.assertEqual(self.testModel.k, m["k"])
        self.assertEqual(self.testModel.initial_skip, m["initial_skip"])
        # Test probale splits
        (word, splits, locs) = extract(firstline)
        locs = list(locs)
        sps = self.testModel.probable_splits(word)
        self.assertEqual(sps, locs)

    def test_error(self):
        self.assertRaises(ValueError, Model, "what")
