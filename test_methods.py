
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


def run_test_routine(method, context_file):
        print('context_file =', context_file, '\t method =', method.__name__)
        expected = frozenset(solutions_from_file(context_file))
        found = frozenset(solutions_from_method(method, context_file))
        print('expected =', tuple(map(pprint_concept, expected)))
        print('   found =', tuple(map(pprint_concept, found)))
        assert expected == found
        print()


for context_file in glob.glob('test_cases/*.lp'):
    filename = os.path.basename(context_file)
    globals()['test_method_1_on_' + filename] = partial(run_test_routine, methods.method_ans_1, context_file)
    globals()['test_method_2_on_' + filename] = partial(run_test_routine, methods.method_ans_2, context_file)
    globals()['test_method_3_on_' + filename] = partial(run_test_routine, methods.method_ans_3, context_file)
