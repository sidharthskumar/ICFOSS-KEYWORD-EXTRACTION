from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from sandhisplitter.util import head_tail


class TrieNode:
    def __init__(self, character):
        self.character = character
        self.c_nsp = 0
        self.c_sp = 0
        self.next = {}


class Trie:
    def __init__(self):
        self.root = TrieNode('^')
        self.end = TrieNode('$')

    def update_node(self, node, word, sp):
        if not word:
            node.next['$'] = self.end
            if sp:
                node.c_sp += 1
            else:
                node.c_nsp += 1
        else:
            head, tail = head_tail(word)
            if head not in node.next.keys():
                node.next[head] = TrieNode(head)
            self.update_node(node.next[head], tail, sp)
            if sp:
                node.c_sp += 1
            else:
                node.c_nsp += 1

    def add_word(self, word, sp):
        wordList = list(word)
        self.update_node(self.root, wordList, sp)

    def P_node(self, node):
        return (node.c_sp/(1.0*(node.c_sp + node.c_nsp)))

    def serialize_node(self, node):
        """ Serialize the tree rooted at node """
        serialized = {
                "character": node.character,
                "c_sp": node.c_sp,
                "c_nsp": node.c_nsp,
                "next": {}
        }
        for child in node.next.keys():
            serialized["next"][child] = self.serialize_node(node.next[child])
        return serialized

    def serialize(self):
        """ Wrapper to make things neat """
        return self.serialize_node(self.root)

    def recursive_load(self, serialized):
        if (serialized["character"] == '$'):
            return self.end

        sub = TrieNode(serialized["character"])
        sub.c_sp = serialized["c_sp"]
        sub.c_nsp = serialized["c_nsp"]
        sub.next = {}
        for child in serialized["next"].keys():
            sub.next[child] = self.recursive_load(serialized["next"][child])
        return sub

    def load(self, serialized):
        self.root = self.recursive_load(serialized)

    def smoothed_P_sp(self, word, initial_skip):
        if not word:
            return 0.0
        tail = list(word)
        node = self.root
        smoothed, total = 0.0, 0.0
        counter = 0
        P = 0
        while (tail and node != self.end):
            head, tail = head_tail(tail)
            if head not in node.next.keys():
                break
            node = node.next[head]
            counter = counter + 1
            if counter > initial_skip:
                P = counter*self.P_node(node)
                smoothed += P
                total += counter

        if total == 0.0:
            return 0
        return smoothed/total
