from __future__ import print_function
from collections import defaultdict
import sys
import math

MAX_PHRASE = int(sys.argv[5])

def quasi_consecutive(tp, f_align):
    tp = list(tp)
    tp.sort()

    prev = tp[0]

    i = 1
    while i < len(tp):
        if tp[i] != prev+1:
            if len(f_align[prev+1]) != 0:
                return False
        else:
            i += 1
        prev = prev+1

    return True


def phrase_extract(e, f, aligns):
    extracted = []

    global MAX_PHRASE

    e_aligns = [[] for i in range(len(e))]
    f_aligns = [[] for i in range(len(f))]

    for a in aligns:
        spl = [int(x) for x in a.split('-')]
        e_aligns[spl[0]].append(spl[1])
        f_aligns[spl[1]].append(spl[0])

    for i1 in range(len(e)):
        for i2 in range(i1, len(e)):

            if i2 - i1 > MAX_PHRASE-1:
                continue
            tp = []

            for i in range(i1, i2+1):
                for j in e_aligns[i]:
                    tp.append(j)

            if len(tp) == 0:
                continue

            tp = set(tp)

            if quasi_consecutive(tp, f_aligns):
                j1 = min(tp)
                j2 = max(tp)

                if j2 - j1 > MAX_PHRASE-1:
                    continue

                sp = []

                for j in range(j1, j2+1):
                    for i in f_aligns[j]:
                        sp.append(i)

                if len(sp) != 0 and min(sp) >= i1 and max(sp) <= i2:
                    e_phrase = e[i1:i2+1]
                    f_phrase = f[j1:j2+1]
                    # extracted.append((e_phrase, f_phrase))

                    while True:
                        j_prime = j2

                        while True:
                            f_phrase = f[j1:j_prime+1]
                            if j_prime - j1 > MAX_PHRASE-1:
                                break
                            extracted.append((e_phrase,f_phrase))
                            j_prime += 1

                            if j_prime >= len(f) or len(f_aligns[j_prime]) != 0:
                                break

                        j1 -= 1

                        if j1<0 or len(f_aligns[j1]) != 0:
                            break

    return extracted


# Load f (source)
dicf = defaultdict(lambda: len(dicf))
lookupf = {}
corpf = []
with open(sys.argv[1], "r") as infile:
    for line in infile:
        sent = [dicf[w] for w in line.strip().split()]
        corpf.append(sent)

for k,v in dicf.iteritems():
    lookupf[v] = k

# Load e (target)
dice = defaultdict(lambda: len(dice))
lookupe = {}
corpe = []
with open(sys.argv[2], "r") as infile:
    for line in infile:
        sent = [dice[w] for w in line.strip().split()]
        corpe.append(sent)

for k,v in dice.iteritems():
    lookupe[v] = k

alignments = []
with open(sys.argv[3], "r") as infile:
    for line in infile:
        alignments.append(line.strip().split())

ep_counts = defaultdict(lambda: defaultdict(lambda: 0))

for i in range(len(corpf)):
    phrases = phrase_extract(corpe[i], corpf[i], alignments[i])

    for phrase in phrases:
        ep = " ".join([lookupe[x] for x in phrase[0]])
        fp = " ".join([lookupf[x] for x in phrase[1]])

        ep_counts[ep][fp] += 1
        ep_counts[ep][0] += 1


with open(sys.argv[4], 'w') as outfile:
    for ep, fps in ep_counts.iteritems():
        count_e = float(fps[0])

        for fp, count_fe in fps.iteritems():
            if fp == 0:
                continue
            val = math.log(count_fe/count_e)
            if val != 0:
                val *= -1
            print('%s\t%s\t%.4f' % (fp, ep, val), file=outfile)
