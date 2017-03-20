from __future__ import print_function
import sys
from collections import defaultdict

ep = '<eps>'

phrase = sys.argv[1]
output_fst = sys.argv[2]

last_id = 0

states = {0:defaultdict(lambda: len(states))}

prev_state = 0

with open(phrase, 'r') as f:
    with open(output_fst, 'w') as out:
        for line in f:
            spl = line.strip().split('\t')

            source_words = spl[0].split()
            target_words = spl[1].split()
            prob = float(spl[2])

            for word in source_words:
                cur_state = states[prev_state][word+ep]

                if cur_state not in states:
                    print('%d %d %s %s' % (prev_state, cur_state, word, ep), file=out)
                    states[cur_state] = defaultdict(lambda: len(states))

                prev_state = cur_state

            for word in target_words:
                cur_state = states[prev_state][ep+word]

                if cur_state not in states:
                    print('%d %d %s %s' % (prev_state, cur_state, ep, word), file=out)
                    states[cur_state] = defaultdict(lambda: len(states))

                prev_state = cur_state

            print('%d %d %s %s %.4f' % (prev_state, 0, ep, ep, prob), file=out)
            prev_state = 0

        print('%d %d %s %s' % (0, 0, '</s>', '</s>'), file=out)
        print('%d %d %s %s' % (0, 0, '<unk>', '<unk>'), file=out)
        print('0', file=out)
