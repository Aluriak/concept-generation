"""Run the benchmarks.

"""

import time
import random
import itertools as it
from functools import partial
from methods import METHODS_SUM as METHODS


CONTEXTS = ('small.lp', 'big.lp')

# number of objects and attributes
CONTEXT_SIZES = range(4, 100)
# density of context
CONTEXT_DENSITIES = tuple(x / 10 for x in range(1, 8))
CONTEXT_FILE_TEMPLATE = 'generated_contexts/{}_{}.lp'
RELATION_TEMPLATE = 'rel({},{}).\n'


def yield_uid() -> iter:
    """Yield uids made of characters"""
    chars = tuple(chr(_) for _ in range(ord('a'), ord('z')+1))
    yield from chars
    lenuid = 2
    while True:
        yield from map(''.join, it.permutations(chars, r=lenuid))
        lenuid += 1


def generate_context(size:int, density:float) -> str:
    """Return the file name containing the concept of given size and density"""
    assert 0. < density < 1.
    filename = CONTEXT_FILE_TEMPLATE.format(size, density)
    uids = yield_uid()
    objs = tuple(next(uids) for _ in range(size))
    atts = tuple(next(uids) for _ in range(size))
    with open(filename, 'w') as fd:
        for obj, att in it.product(objs, atts):
            if random.random() < density:
                fd.write(RELATION_TEMPLATE.format(obj, att))
    return filename


if __name__ == "__main__":
    for size, density in it.product(CONTEXT_SIZES, CONTEXT_DENSITIES):
        context = generate_context(size, density)
        print('CONTEXT:', context)
        for method in METHODS:
            # print('\t' + method.__name__ + ':', timeit(partial(method, context)))
            start = time.time()
            result = method(context)
            end = time.time() - start
            print('\t' + method.__name__ + ':', result, end)
