from __future__ import print_function, division
import sys
import math
from collections import defaultdict

# Hyper parameters
MAX_ITER = 17
NULL = '$$null$$'

total_words = 0

# Load f (source - ENGLISH)
dicf = defaultdict(lambda: len(dicf))
corpf = []
with open(sys.argv[2], "r") as infile:
    for line in infile:
        sent = [dicf[w] for w in line.strip().split()]
        sent += [dicf[NULL]]
        corpf.append(sent)
        total_words += len(sent)

NULL_PRIOR = 0.2

# Load e (target - GERMAN)
dice = defaultdict(lambda: len(dice))
corpe = []

with open(sys.argv[1], "r") as infile:
    for line in infile:
        sent = [dice[w] for w in line.strip().split()]
        corpe.append(sent)
        # total_words += len(sent)

print(len(dice))
print(len(dicf))

# EM
pfe = defaultdict(lambda: 1/len(dicf))
iteration = 0
convergence = False
while iteration < MAX_ITER and not convergence:
    iteration += 1

    ll = 0.0

    print("EM iteration: " + str(iteration))

    cfe = defaultdict(lambda: 0.0)
    ce = defaultdict(lambda: 0.0)
    for sf, se in zip(corpf, corpe):

        for t, wf in enumerate(sf):
            total = 0.0
            for i, we in enumerate(se):
                total += pfe[(wf, we)]

            for i, we in enumerate(se):
                val = pfe[(wf, we)]/total
                cfe[(wf, we)] += val
                ce[we] += val
    for wf, we in cfe:
        pfe[(wf, we)] = cfe[(wf, we)]/ce[we]

    for sf, se in zip(corpf, corpe):
        for t, wf in enumerate(sf):
            total = 0.0
            for i, we in enumerate(se):
                total += pfe[(wf, we)]
            ll += math.log(total)
        ll += math.log(1/100.0) - len(sf)*math.log(len(se))

    print(ll/total_words)

print(len(pfe))

count_null = 0
total_w = 0.0

# Inference
with open(sys.argv[3], "w+") as outfile:
    for sf, se in zip(corpf, corpe):
        probs = []
        aligns = []
        for t, wf in enumerate(se):
            max_pos = -1
            max_prob = 0.0
            for i, we in enumerate(sf):
                if (we, wf) not in pfe:
                    print("Error")

                prob = pfe[(we, wf)]

                if sf[i] == dicf[NULL]:
                    prob *= NULL_PRIOR
                # else:
                #     prob *= (1-NULL_PRIOR)

                if prob > max_prob:
                    max_prob = prob
                    max_pos = i

            if sf[max_pos] == dicf[NULL]:
                print("Null")
                continue

            # aligns.append(str(max_pos) + '-' + str(t))
            # probs.append(max_prob)
            outfile.write('%d-%d ' % (max_pos, t))
        # min_conf = probs.index(min(probs))
        # del aligns[min_conf]
        # outfile.write(" ".join(aligns))
        outfile.write('\n')
