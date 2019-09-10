"""Implementation of close by one algorithm, mining for formal concepts.

The first part is the ASP implementation, using nextclosure.lp encoding.

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
    return dict(context), dict(invcontext), asp_atoms

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
models = clyngor.solve('nextclosure.lp', inline=asp_atoms).by_arity
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

print('USING ITERATIVE ASP METHOD…')

def iterative_ASP_next_closure():
    """Yield formal concepts of the context using next closure algorithm
    implemented in ASP with iterative clingo feature"""
    models = clyngor.solve('nextclosure-it.lp', inline=asp_atoms).by_arity
    for model in models:
        pass  # we just want the last one
    final_model = model
    concepts = defaultdict(lambda: [set(), set()])
    for idx, obj in model.get('ext/2', ()):
        concepts[idx][0].add(obj)
    for idx, att in model.get('int/2', ()):
        concepts[idx][1].add(att)
    for extent, intent in concepts.values():
        yield (frozenset(extent), frozenset(intent))


itasp_concepts = set(iterative_ASP_next_closure())
for ext, int in itasp_concepts:
    print('CONCEPT:', pretty(ext), pretty(int))

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
    yield derived_objects(M), M

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


print('\n\nUsing Object Intersections algorithm…')

def object_intersections():
    "Yield formal concepts of the context using OI algorithm"
    G = set(context.keys())
    M = set(invcontext.keys())
    C = [(derived_objects(M), M)]  # list of all found formal concepts
    for obj in G:
        for ext, int in C:
            inters = int & derived_attributes({obj})
            if all(inters != int for _, int in C):
                C.append((derived_objects(inters), inters))
    return {(frozenset(ext), frozenset(int)) for ext, int in C}

oint_concepts = object_intersections()
for ext, int in oint_concepts:
    print('CONCEPT:', pretty(ext), pretty(int))


print('\n\nUsing Object Intersections algorithm, implemented in ASP…')

def object_intersections_ASP():
    "Yield formal concepts of the context using OI algorithm implemented in ASP"
    G = set(context.keys())
    M = set(invcontext.keys())
    C = [(derived_objects(M), M)]  # list of all found formal concepts
    for obj in G:
        for ext, int in C:
            data = (f'\nobject({obj}).\n'
                    + ' '.join(f'concept_ext({x}).' for x in ext) + '\n'
                    + ' '.join(f'concept_int({x}).' for x in int) + '\n'
                    + ' '.join(f'concepts_int({idx},{x}).' for x in int for idx, (_, int) in enumerate(C))
                    )
            models = clyngor.solve('algo-oi.lp', inline=asp_atoms + data).by_arity
            model = next(models, None)
            if model is None: continue  # no concept yielded

            extent, intent = set(), set()
            for obj, in model.get('ext/1', ()):
                extent.add(obj)
            for att, in model.get('int/1', ()):
                intent.add(att)
            print(extent, intent)
            C.append((frozenset(extent), frozenset(intent)))
    return C


# oiasp_concepts = object_intersections_ASP()
# for ext, int in oiasp_concepts:
    # print('CONCEPT:', pretty(ext), pretty(int))

assert asp_concepts == python_concepts
print('\nBoth methods found the same formal concepts !')
assert asp_concepts == itasp_concepts
print('\nIterative and non-iterative ASP methods found the same formal concepts !')
assert oint_concepts == python_concepts
print('\nOI method found the same formal concepts as NC !')
# assert oint_concepts == oiasp_concepts
# print('\nOI method found the same formal concepts as OI using ASP !')
