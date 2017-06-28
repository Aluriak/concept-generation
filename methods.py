from pyasp import asp
from functools import partial


METHODS_DEF = {
    '1': 'simple',
    '2': 'choice',
    '3': 'choice_noint',
    '4': 'choice_exp',
}


def build_methods() -> iter:
    """Create methods according to METHODS_DEF,
    then yield and add it in global scope"""
    for name, filename in METHODS_DEF.items():
        filename = filename + '.lp'
        def method_func(context):
            yield from solve([filename, context])
        def method_ans_func(context):
            return tuple(method_func(context))
        def method_sum_func(context):
            return sum(1 for answer in method_func(context))
        globals()['method_' + name] = method_func
        globals()['method_ans_' + name] = method_ans_func
        globals()['method_sum_' + name] = method_sum_func
        yield method_func, method_ans_func, method_sum_func

# collect all methods
METHODS, METHODS_ANS, METHODS_SUM = zip(*build_methods())


def method_name(method:callable) -> str:
    """Return the name of given method.

    >>> methode_name(method_1)
    '1'
    >>> methode_name(method_2)
    '2'

    """
    HEAD = 'method_'
    assert method.__name__.startswith(HEAD)
    return method[:len(HEAD)]


def solve(files:iter) -> iter:
    """Yield all solutions"""
    solver = asp.Gringo4Clasp(clasp_options='-n 0')
    yield from solver.run(list(files), collapseAtoms=False)
