__version__ = '0.0.2'

# Vocab -----------------------------------------------------------------------
from pkg_resources import resource_filename
from itertools import chain
read_vocab = lambda x: (ii.rstrip() for ii in open(resource_filename(__name__, x)))

default_vocab = set(chain(*map(read_vocab, ['vocab/yue.vocab', 'vocab/cmn.vocab'])))


# Astar -----------------------------------------------------------------------
from astar import AStar

MAX_WORD_LEN = 7

def word_len_cost(length):
    return MAX_WORD_LEN*(1/length)

class SentenceSearch(AStar):
    def __init__(self, vocab, *args, **kwargs):
        self.vocab = vocab
        self.sent = None
    
    def __call__(self, sent):
        self.sent = sent
        rev_iter = self.astar(0, len(sent))
        out = []
        try:
            start = next(rev_iter)
            for end in rev_iter:
                word = self.sent[start:end]
                is_vocab = word in self.vocab
                out.append(dict(start = start, end = end, word = word, is_vocab = is_vocab))
                start = end
        except TypeError:
            pass
        
        return out
    
    def neighbors(self, node):
        out = []
        max_neighbor = min(len(self.sent) + 1, 
                           node + MAX_WORD_LEN + 1)
        for ii in range(node + 1, max_neighbor):
            out.append(ii)
            #if ii in self.node_dict: out.append(self.node_dict[ii])
            #else:
            #    node_dict.append(ii)
        return out
    
    def distance_between(self, n1, n2):
        word = self.sent[n1:n2]

        if len(word) == 1:
            return word_len_cost(1)
        if word in self.vocab:
            return word_len_cost(len(word))

        return float('inf')
    
    def heuristic_cost_estimate(self, current, goal):
        n = goal - current
        big_chunks =  int(n / MAX_WORD_LEN)
        small_chunk = n % MAX_WORD_LEN
        cost  = word_len_cost(MAX_WORD_LEN)*(big_chunks) + \
                (small_chunk and word_len_cost(small_chunk))
        return cost


searcher = SentenceSearch(default_vocab)
