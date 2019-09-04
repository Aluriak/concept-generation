"""Implementation of close by one algorithm, mining for formal concepts.

The first part is the ASP implementation, using closebyone.lp encoding.

The second part is a Python implementation.

"""


from collections import defaultdict
def get_context_as_dicts_of_set(matrix) -> dict:
    asp_atoms = ''  # ASP encoding of the context
    context, invcontext = defaultdict(set), defaultdict(set)
    for object, values in enumerate(matrix, start=1):
        for attribute, relation in enumerate(values, start=1):
            if relation:
                attribute = chr(ord('a') - 1 + attribute)
                context[object].add(attribute)
                invcontext[attribute].add(object)
                asp_atoms += f'rel({object},{attribute}).'
        asp_atoms += '\n'
    return context, invcontext, asp_atoms

context, invcontext, asp_atoms = get_context_as_dicts_of_set([
    [0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 1],
])
print('CONTEXT:', context)
print('ATOMS:\n' + asp_atoms + '\n')


print('USING ASP METHOD…')

import clyngor
models = clyngor.solve('closebyone.lp', inline=asp_atoms).by_arity
model = next(models)
# assert next(models, None) is None

from collections import defaultdict
concepts = defaultdict(lambda: [set(), set()])
for idx, obj in model.get('ext/2', ()):
    concepts[idx][0].add(obj)
for idx, att in model.get('int/2', ()):
    concepts[idx][1].add(att)

currents = defaultdict(set)
for idx, obj in model.get('current/2', ()):
    currents[idx].add(obj)
nexts = defaultdict(set)
for idx, obj in model.get('next/2', ()):
    nexts[idx].add(obj)
deriveds = defaultdict(set)
for idx, obj in model.get('derived/2', ()):
    deriveds[idx].add(obj)
dderiveds = defaultdict(set)
for idx, obj in model.get('double_derived/2', ()):
    dderiveds[idx].add(obj)
lasts = defaultdict(lambda: False)
for idx, in model.get('last_step_/1', ()):
    dderiveds[idx] = True

print(concepts)
asp_concepts = set()
pretty = lambda s: '{' + ' '.join(map(str, sorted(tuple(s)))) + '}'
for idx in sorted(tuple(concepts)):
    ext, int = concepts[idx]
    asp_concepts.add((frozenset(ext), frozenset(int)))
    print(f'{idx}: {pretty(ext)} × {pretty(int)}')
    print(f'     current={pretty(currents.get(idx, set()))}')
    print(f'     next={pretty(nexts.get(idx, set()))}')
    print(f'     derived={pretty(deriveds.get(idx, set()))}')
    print(f'     dderived={pretty(dderiveds.get(idx, set()))}')
    print('    ', 'LAST!' if lasts[idx] else '')


# exit()

print('\n\nUSING PYTHON METHOD…')



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


def derived_objects(attributes):
    try:
        return set.intersection(*(invcontext[attr] for attr in attributes))
    except TypeError:
        return set()
def derived_attributes(objects):
    try:
        return set.intersection(*(context[obj] for obj in objects))
    except TypeError:
        return set()

def next_closure():
    G = set(context.keys())
    M = set(invcontext.keys())
    yield derived_attributes(M), M

    curr_subset = {max(G)}
    next_object = max(G)

    idx = 1
    while curr_subset != G:
        idx += 1
        derived_subset = derived_attributes(curr_subset)
        dderived_subset = derived_objects(derived_subset)
        # print('\nLOOP:', curr_subset, '   prime=', derived_subset, '   doubleprime=',dderived_subset)
        if all(obj >= next_object for obj in dderived_subset - curr_subset):
            yield dderived_subset, derived_subset
            try:
                next_object = max(G - dderived_subset)
            except ValueError:  # no next object, all are in the extent
                break
            curr_subset = dderived_subset
        else:
            next_object = max({obj for obj in G - curr_subset if obj < max(curr_subset)})
        curr_subset.add(next_object)
        curr_subset = {obj for obj in curr_subset if next_object >= obj}
        # print('    :', 'next:', next_object)
    # print('IDX:', idx)

python_concepts = set()
for ext, int in next_closure():
    print('CONCEPT:', pretty(ext), pretty(int))
    python_concepts.add((frozenset(ext), frozenset(int)))

assert asp_concepts == python_concepts
print('\nBoth methods found the same formal concepts !')
