# Wrapper class
# Most functionalities are in model.

from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from sandhisplitter.model import Model


class Splitter:
    def __init__(self, model):
        self.M = Model(model=model)

    def splits(self, word):
        return self.M.probable_splits(word)
