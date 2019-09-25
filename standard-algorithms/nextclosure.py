"""Implementation of close by one algorithm, mining for formal concepts.

The first part is the ASP implementation, using nextclosure.lp encoding.

The second part is a Python implementation.

"""


from collections import defaultdict


pretty = lambda s: '{' + ' '.join(map(str, sorted(tuple(s)))) + '}'


def get_context_as_dicts_of_set(matrix, as_char:bool=True) -> dict:
    asp_atoms = ''  # ASP encoding of the context
    context, invcontext = defaultdict(set), defaultdict(set)
    for object, values in enumerate(matrix, start=1):
        for attribute, relation in enumerate(values, start=1):
            if relation:
                if as_char:
                    attribute = chr(ord('a') - 1 + attribute)
                context[object].add(attribute)
                invcontext[attribute].add(object)
                asp_atoms += f'rel({object},{attribute}).'
        asp_atoms += '\n'
    return dict(context), dict(invcontext), asp_atoms

context, invcontext, asp_atoms = get_context_as_dicts_of_set([
    [0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 1],
    # [1, 0, 0, 0, 0, 0, 0, 0, 1],  # Everything fail with this one !
])
print('CONTEXT:', context)
print('ATOMS:\n' + asp_atoms + '\n')


print('USING ASP METHOD…')
from algorithms import next_closure_ASP
asp_concepts = set(next_closure_ASP(context, invcontext, asp_atoms))


# exit()

print('USING ITERATIVE ASP METHOD…')
from algorithms import next_closure_ASP_iterative
itasp_concepts = tuple(next_closure_ASP_iterative(context, invcontext, asp_atoms))
for ext, int in itasp_concepts:
    print('CONCEPT:', pretty(ext), pretty(int))
itasp_concepts = set(itasp_concepts)

# simple verification of equivalence on the two ASP iterative implementations.
itaspbymodel_concepts = set(next_closure_ASP_iterative(context, invcontext, asp_atoms, 'nextclosure-it-bymodel.lp'))



def gen_ordered_subsets(ordered_values:list, start:list=[]) -> [list]:
    "yield subsets in an order"
    order = {val: idx for idx, val in enumerate(ordered_values, start=1)}
    current = start

    while len(current) < len(ordered_values):
        unused_values = [v for v in ordered_values if v not in current]
        max_unused = unused_values[-1]
        current = [v for v in current if order[v] < order[max_unused]] + [max_unused]
        yield current

# ordered_values = tuple(range(1,8))
# for subset in gen_ordered_subsets(ordered_values):
    # print(subset)

print('\n\nUSING PYTHON METHOD…')
from algorithms import next_closure_python
python_concepts = set()
for ext, int in next_closure_python(context, invcontext):
    print('CONCEPT:', pretty(ext), pretty(int))
    python_concepts.add((frozenset(ext), frozenset(int)))


print('\n\nUsing Object Intersections algorithm…')
from algorithms import object_intersections_python
oint_concepts = object_intersections_python(context, invcontext)
for ext, int in oint_concepts:
    print('CONCEPT:', pretty(ext), pretty(int))


# print('\n\nUsing Object Intersections algorithm, implemented in ASP…')
from algorithms import object_intersections_ASP

# oiasp_concepts = object_intersections_ASP()
# for ext, int in oiasp_concepts:
    # print('CONCEPT:', pretty(ext), pretty(int))


print('\n\nVerifications…')
assert asp_concepts == python_concepts
print('ASP and python implementations of Next Closure found the same formal concepts !')
assert asp_concepts == itasp_concepts
print('Iterative and non-iterative ASP methods found the same formal concepts !')
assert itaspbymodel_concepts == itasp_concepts, "the two ASP iterative methods are giving different results"
print('The two iterative methods are giving the same values')
assert oint_concepts == python_concepts
print('OI method found the same formal concepts as NC !')
# assert oint_concepts == oiasp_concepts
# print('OI method found the same formal concepts as OI using ASP !')
