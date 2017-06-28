from pyasp import asp


def solve(files:iter) -> iter:
    """Yield all solutions"""
    solver = asp.Gringo4Clasp(clasp_options='-n 0')
    yield from solver.run(list(files), collapseAtoms=False)



def method_1(context):
    yield from solve(['simple.lp', context])
def method_2(context):
    yield from solve(['choice.lp', context])
def method_3(context):
    yield from solve(['choice_noint.lp', context])

def method_ans_1(context):
    return tuple(method_1(context))
def method_ans_2(context):
    return tuple(method_2(context))
def method_ans_3(context):
    return tuple(method_3(context))

def method_sum_1(context):
    return sum(1 for answer in method_1(context))
def method_sum_2(context):
    return sum(1 for answer in method_2(context))
def method_sum_3(context):
    return sum(1 for answer in method_3(context))


METHODS = (method_1, method_2, method_3)
METHODS_ANS = (method_ans_1, method_ans_2, method_ans_3)
METHODS_SUM = (method_sum_1, method_sum_2, method_sum_3)
