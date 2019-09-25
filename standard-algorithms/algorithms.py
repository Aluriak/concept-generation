"""File containing implementations of standard FCA algorithms,
in both python and ASP.

"""

import clyngor
from collections import defaultdict

def derived_objects(invcontext, attributes):
    try:
        return set.intersection(*(invcontext[attr] for attr in attributes))
    except TypeError:
        return set.union(*invcontext.values())
def derived_attributes(context, objects):
    try:
        return set.intersection(*(context[obj] for obj in objects))
    except TypeError:
        return set.union(*context.values())

def next_closure_python(context, invcontext):
    G = set(context.keys())
    M = set(invcontext.keys())
    yield derived_objects(invcontext, M), M

    curr_subset = {max(G)}
    next_object = max(G)

    idx = 1
    while curr_subset != G:
        idx += 1
        derived_subset = derived_attributes(context, curr_subset)
        dderived_subset = derived_objects(invcontext, derived_subset)
        # print('\nLOOP:', curr_subset, '   prime=', derived_subset, '   doubleprime=',dderived_subset, '   next=', next_object)
        if all(obj >= next_object for obj in dderived_subset - curr_subset):
            yield dderived_subset, derived_subset
            try:
                next_object = max(G - dderived_subset)
            except ValueError:  # no next object, all are in the extent
                # print('BREAKING!', G, dderived_subset)
                break
            curr_subset = dderived_subset
        else:
            next_object = max({obj for obj in G - curr_subset if obj < max(curr_subset)})
        curr_subset.add(next_object)
        curr_subset = {obj for obj in curr_subset if next_object >= obj}
    # print('END WHILE!', G, dderived_subset)
    yield G, derived_attributes(context, G)


def next_closure_ASP(context, invcontext, asp_data:str, asp_code:str='nextclosure.lp', debug=False):
    """Non iterative implementation of Next Closure in ASP"""
    models = clyngor.solve(asp_code, inline=asp_data).by_arity
    model = next(models)
    # assert next(models, None) is None

    concepts = defaultdict(lambda: [set(), set()])
    for idx, obj in model.get('ext/2', ()):
        concepts[idx][0].add(obj)
    for idx, att in model.get('int/2', ()):
        concepts[idx][1].add(att)

    if debug:
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

    asp_concepts = set()
    for idx in sorted(tuple(concepts)):
        ext, int = concepts[idx]
        asp_concepts.add((frozenset(ext), frozenset(int)))
        if debug:
            print(f'{idx}: {pretty(ext)} × {pretty(int)}')
            print(f'     current={pretty(currents.get(idx, set()))}')
            print(f'     next={pretty(nexts.get(idx, set()))}')
            print(f'     derived={pretty(deriveds.get(idx, set()))}')
            print(f'     dderived={pretty(dderiveds.get(idx, set()))}')
            print('    ', 'LAST!' if lasts[idx] else '')
    return asp_concepts


def next_closure_ASP_iterative(context, invcontext, asp_data:str, asp_code:str='nextclosure-it.lp'):
    """Yield formal concepts of the context using next closure algorithm
    implemented in ASP with iterative clingo feature"""
    models = clyngor.solve(asp_code, inline=asp_data).by_arity
    concepts = defaultdict(lambda: [set(), set()])
    for model in models:
        for idx, obj in model.get('ext/2', ()):
            concepts[idx][0].add(obj)
        for idx, att in model.get('int/2', ()):
            concepts[idx][1].add(att)
    for extent, intent in concepts.values():
        yield (frozenset(extent), frozenset(intent))

def object_intersections_python(context, invcontext):
    "Yield formal concepts of the context using OI algorithm"
    G = set(context.keys())
    M = set(invcontext.keys())
    C = [(derived_objects(invcontext, M), M)]  # list of all found formal concepts
    for obj in G:
        for ext, int in C:
            inters = int & derived_attributes(context, {obj})
            if all(inters != int for _, int in C):
                C.append((derived_objects(invcontext, inters), inters))
    return {(frozenset(ext), frozenset(int)) for ext, int in C}


def object_intersections_ASP(context, invcontext, asp_data:str):
    "Yield formal concepts of the context using OI algorithm implemented in ASP"
    G = set(context.keys())
    M = set(invcontext.keys())
    C = [(derived_objects(invcontext, M), M)]  # list of all found formal concepts
    for obj in G:
        for ext, int in C:
            data = (f'\nobject({obj}).\n'
                    + ' '.join(f'concept_ext({x}).' for x in ext) + '\n'
                    + ' '.join(f'concept_int({x}).' for x in int) + '\n'
                    + ' '.join(f'concepts_int({idx},{x}).' for x in int for idx, (_, int) in enumerate(C))
                    )
            models = clyngor.solve('algo-oi.lp', inline=asp_data + data).by_arity
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
