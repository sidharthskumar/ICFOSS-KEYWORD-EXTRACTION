# -*- coding: utf-8 -*-
from io import open
from testtools import TestCase
from pkg_resources import resource_filename
from sandhisplitter.util import extract, compress, head_tail


class TestUtils(TestCase):
    def setUp(self):
        super(TestUtils, self).setUp()
        testcases = resource_filename("sandhisplitter.tests",
                                      "resources/samples.txt")
        self.entries = open(testcases, "r", encoding='utf-8')

    def test_extract_compress(self):
        entries = map(lambda x: x.strip(), self.entries.readlines())
        for inline in entries:
            s, sps, l = extract(inline)
            outline = compress(s, sps, l)
            self.assertEqual(inline, outline)

    def test_head_tail(self):
        self.assertRaises(IndexError, head_tail, [])
        self.assertEqual(head_tail([1]), (1, []))
        self.assertEqual(head_tail([1, 2]), (1, [2]))
