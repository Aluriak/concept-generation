
import os
import re
import glob
from functools import partial
import pytest
import methods


SOLUTION_REG = re.compile('% ([a-z ]+)\s*×\s*([a-z ]+)\s*')


def solutions_from_file(filename:str) -> iter:
    """Yield solutions found in given file as pairs of frozenset"""
    with open(filename) as fd:
        for line in fd:
            if line.startswith('% '):
                match = SOLUTION_REG.fullmatch(line)
                if match:
                    objs, atts = match.groups()
                    objs = frozenset(objs.strip().split(' '))
                    atts = frozenset(atts.strip().split(' '))
                    yield objs, atts


def solutions_from_method(method, filename:str) -> iter:
    """Solve the given context using the given method, and extract the concepts
    in each answer (obj/1 and att/1 atoms).

    Yield the {obj}×{att} as pairs of frozenset.

    """
    for answer in method(filename):
        obj, att = set(), set()
        for atom in answer:
            if atom.predicate == 'obj':
                assert len(atom.args()) == 1
                obj.add(atom.args()[0])
            elif atom.predicate == 'att':
                assert len(atom.args()) == 1
                att.add(atom.args()[0])
        if obj and att:  # this is needed because the method 1 is (sometimes) yielding non-concept having empty obj or att
            yield frozenset(obj), frozenset(att)


def pprint_concept(concept:(frozenset, frozenset)) -> str:
    obj, att = concept
    return '{{{}}}×{{{}}}'.format(','.join(obj), ','.join(att))


def run_test_routine(method, context_file, should_fail=False):
    """Total run of the testing routine for given method and context.

    method -- method function to test
    context_file -- filename of the context used to test the method
    should_fail -- if true, expect the method to fail.

    """
    print('context_file =', context_file, '\t method =', method.__name__)
    expected = frozenset(solutions_from_file(context_file))
    found = frozenset(solutions_from_method(method, context_file))
    print('expected =', tuple(map(pprint_concept, expected)))
    print('   found =', tuple(map(pprint_concept, found)))
    if should_fail:
        assert expected != found
    else:
        assert expected == found
    print()


# Create and add in global scope the tests for pytest.
for context_file in glob.glob('test_cases/*.lp'):
    filename = os.path.basename(context_file)
    for method, name in methods.METHODS_ANS.items():
        func = partial(run_test_routine, method, context_file, should_fail=name == 'false')
        globals()['test_method_' + name + '_on_' + filename] = func
