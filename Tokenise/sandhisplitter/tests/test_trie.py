from testtools import TestCase
from sandhisplitter.util import head_tail
from sandhisplitter.trie import Trie


class TestTrie(TestCase):
    def setUp(self):
        super(TestTrie, self).setUp()
        self.testTrie = Trie()

    def contains_substr(self, node, word):
        if not word:
            return '$' in node.next.keys()
        head, tail = head_tail(word)
        if head not in node.next.keys():
            return False
        return self.contains_substr(node.next[head], tail)

    def contains(self, word):
        return self.contains_substr(self.testTrie.root, word)

    def test_word(self):
        words = ["hello", "what", "hell", "h", "this"]
        for word in words:
            self.testTrie.add_word(word, False)
        for word in words:
            self.assertEqual(self.contains(word), True)

    def test_export_and_load(self):
        words = ["hello", "what", "hell", "h", "this"]
        for word in words:
            self.testTrie.add_word(word, False)
        m = self.testTrie.serialize()
        self.testTrie.load(m)
        for word in words:
            self.assertEqual(self.contains(word), True)

    def test_smoothed_psp(self):
        words = ["hello", "what", "hell", "h", "this"]
        for word in words:
            self.testTrie.add_word(word, False)
        for i in range(6):
            for word in words:
                self.assertEqual(self.testTrie.smoothed_P_sp(word, i), 0.0)
        for word in words:
            self.testTrie.add_word(word, True)
        for i in range(6):
            for word in words:
                if len(word) <= i:
                    self.assertEqual(self.testTrie.smoothed_P_sp(word, i), 0.0)
                else:
                    self.assertEqual(self.testTrie.smoothed_P_sp(word, i), 0.5)
        self.assertEqual(self.testTrie.smoothed_P_sp("hi", 0), 0.5)

        self.assertEqual(self.testTrie.smoothed_P_sp('', 0), 0.0)
