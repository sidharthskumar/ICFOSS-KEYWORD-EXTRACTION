from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
from io import open
import argparse
import json
from sandhisplitter.util import extract, compress
from sandhisplitter.splitter import Splitter
from sandhisplitter.postprocessor import PostProcessor
from operator import add


def location_error(desired, obtained, length):
    # For more information, refer
    # https://en.wikipedia.org/wiki/Precision_and_recall

    # Get the desired lists as sets
    ds, os = map(set, [desired, obtained])
    u = set(range(1, length-1))

    # Set difference(A, B) = A - B
    # Set intersection(A, B) = A & B
    true_positives = ds & os
    true_negatives = (u - ds) & (u - os)
    false_positives = os - ds
    false_negatives = (u - os) - (u - ds)
    output = (true_positives, true_negatives,
              false_positives, false_negatives)
    return map(len, output)


def measures(location_metric):
    """
    Gets a location metric vector.
    Returns precision, recall, accuracy, true negative rate
    """
    tp, tn, fp, fn = map(float, location_metric)
    result = {}
    result["Precision"] = tp/(tp+fp)
    result["Recall"] = tp/(tp+fn)
    result["Accuracy"] = (tp+tn)/(tp+tn+fp+fn)
    result["True Negative Rate"] = tn/(tn+fp)
    return result


def main():
    # if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(description="Test a model")
    arguments = [
        ["-m", "--modelfile", "path to model file",
            str, "modelfile"],
        ["-t", "--testfile", "path to test file",
            str, "testfile"],
        ["-o", "--output", "file to store output",
            str, "output"],
    ]
    for arg in arguments:
        unix, gnu, desc, typename, dest = arg
        parser.add_argument(unix, gnu, help=desc, type=typename,
                            required=True, dest=dest)
    args = parser.parse_args()
    # Load data into the model
    modelfile = open(args.modelfile, "r", encoding="utf-8")
    model = json.load(modelfile)
    splitter = Splitter(model)
    postprocessor = PostProcessor()
    output = open(args.output, "w", encoding="utf-8")
    stats = (0, 0, 0, 0)
    linenumber = 0
    testfile = open(args.testfile, "r", encoding="utf-8")
    for line in testfile:
        linenumber += 1
        line = line.strip()
        # print(line)
        try:
            word, desired_splits, desired_locs = extract(line)
        except ValueError:
            print("Error in line %d" % linenumber)
        sps = splitter.splits(word)
        splits = postprocessor.split(word, sps)
        outstring = compress(word, splits, sps) + '\n'
        # split_metrics = split_error(desired_splits, splits)
        # Check what matches and not matches
        location_metrics = location_error(desired_locs, sps, len(word))
        stats = map(add, stats, location_metrics)
        output.write(outstring)

    # Get the aggregate measures
    results = measures(stats)
    print("Split point identification stats:")
    skeys = sorted(results.keys())
    for key in skeys:
        print('  ', key, ':', results[key])
