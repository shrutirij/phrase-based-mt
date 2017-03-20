from __future__ import print_function
import sys
import math
from collections import defaultdict

D = float(sys.argv[3])

bigram_count = defaultdict(lambda: 0.0)
prec_count = defaultdict(lambda: 0.0)
foll_count = defaultdict(lambda: 0.0)
unigram_count = defaultdict(lambda: 0.0)

with open(sys.argv[1], "r") as infile:
    for line in infile:
        vals = line.strip().split() + ["</s>"]
        ctxt = "<s>"
        for val in vals:
            if (ctxt, val) not in bigram_count:
                prec_count[val] += 1
                foll_count[ctxt] += 1

            bigram_count[(ctxt, val)] += 1
            unigram_count[ctxt] += 1
            ctxt = val

alpha = {}

unique_bigrams = len(bigram_count)

for w, c in unigram_count.iteritems():
    alpha[w] = D*foll_count[w]/c

# ALPHA_1 = 0.1
# ALPHA_UNK = 0.01
# ALPHA_2 = 1.0 - ALPHA_1 - ALPHA_UNK
PROB_UNK = 1e-10
UNK_WEIGHT = 1e-10/len(prec_count)

stateid = defaultdict(lambda: len(stateid))

with open(sys.argv[2], "w") as outfile:

    # Print the fallbacks
    print("%d %d <eps> <eps> %.4f" % (stateid["<s>"], stateid[""], -math.log(alpha["<s>"])), file=outfile)
    for ctxt in unigram_count:
        if ctxt != "<s>":
            print("%d %d <eps> <eps> %.4f" % (stateid[ctxt], stateid[""], -math.log(alpha[ctxt])), file=outfile)

    # Print the unigrams
    for word, val in prec_count.iteritems():
        v1 = (val/unique_bigrams)-UNK_WEIGHT
        print("%d %d %s %s %.4f" % (stateid[""], stateid[word], word, word, -math.log(v1)), file=outfile)

    print("%d %d <unk> <unk> %.4f" % (stateid[""], stateid[""], -math.log(PROB_UNK)), file=outfile)

    # Print the unigrams
    for (ctxt, word), val in bigram_count.items():
        v1 = (prec_count[word]/unique_bigrams)-UNK_WEIGHT
        v2 = (val-D)/unigram_count[ctxt]
        value = v2 + alpha[ctxt] * v1
        print("%d %d %s %s %.4f" % (stateid[ctxt], stateid[word], word, word, -math.log(value)), file=outfile)

    # Print the final state
    print(stateid["</s>"], file=outfile)
