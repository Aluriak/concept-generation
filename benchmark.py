"""Run the benchmarks.

"""

import csv
import time
import random
import itertools as it
import timeit
from functools import partial
from methods import METHODS_SUM as METHODS


# Make timeit return both time and function return value
timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""


CONTEXTS = ('small.lp', 'big.lp')

# number of objects and attributes
CONTEXT_SIZES = range(10, 50)
# density of context
CONTEXT_DENSITIES = tuple(x / 10 for x in range(4, 5))
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
    outfile = open('output.csv', 'w')
    STATIC_FIELDS = ['context size', 'context density', '#concept']
    METHOD_FIELDS = [name + ' time' for name in METHODS.values()]
    output = csv.DictWriter(outfile, fieldnames=STATIC_FIELDS + METHOD_FIELDS)
    output.writeheader()
    for size, density in it.product(CONTEXT_SIZES, CONTEXT_DENSITIES):
        static_data = {'context size': size, 'context density': density, '#concept': 0}
        context = generate_context(size, density)
        results = {}  # method: runtime
        print('CONTEXT:', context)
        for method, name in METHODS.items():
            runtime, nb_concept = timeit.timeit(partial(method, context), number=3)
            method(context)
            print('\t' + method.__name__ + ':', nb_concept, runtime)
            results[name + ' time'] = runtime
        output.writerow({**static_data, **results})
    outfile.close()
