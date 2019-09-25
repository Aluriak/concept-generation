"""Comparisons of algorithms implementing the concept search.
"""

import random
import clyngor


ASP_SEARCH_CONCEPTS = """
ext(O) :- rel(O,_) ; rel(O,A): int(A).
int(A) :- rel(_,A) ; rel(O,A): ext(O).
#show ext/1.
#show int/1.
"""

# for model in clyngor.solve(inline=asp_data + ASP_SEARCH_CONCEPTS):
    # print(model)
# exit()

def models_to_time(models:clyngor.Answers):
    # print(models.statistics)
    timecode = models.statistics['Time'].split(' ')[0]
    assert timecode[-1] == 's'
    return float(timecode[:-1])

def run_nextclosure(data:str):
    models = clyngor.solve('nextclosure-it.lp', inline=data, stats=True)
    for model in models:  pass  # compute everything
    return models_to_time(models)
def run_standard(data:str):
    models = clyngor.solve(inline=ASP_SEARCH_CONCEPTS + data, stats=True)
    for model in models:  pass  # compute everything
    return models_to_time(models)
def nb_concepts(data:str):
    models = clyngor.solve(inline=ASP_SEARCH_CONCEPTS + data)
    return sum(1 for _ in models)


def table_to_asp(table, maxsize:int):
    """Return given table encoded in ASP rel/2 atoms.
    Only the `maxsize` first rows and columns are used."""
    for row in range(min(maxsize, len(table))):
        for col in range(min(maxsize, len(table[row]))):
            if table[row][col]:
                yield f'rel({row},{col}).'
        yield f'\n'

def create_table(size:int, density:float=0.5):
    "Return a boolean square table"
    table = []
    for idx in range(size):
        table.append(tuple(random.random() < density for _ in range(size)))
    return tuple(table)

TABLE_SIZE, START, STEP = 100, 2, 10
# DENSITIES = 0.05, 0.1, 0.2, 0.4
DENSITIES = 0.1, 0.2, 0.4
METHODS = {'nextclosure': run_nextclosure, 'standard': run_standard}

def benchmark(table_size=TABLE_SIZE, size_start:int=START, size_step:int=STEP, densities=DENSITIES, methods=METHODS):
    tables = {density: create_table(table_size, density) for density in densities}
    times = {'context-size': []}
    times.update({f'nb-concept-d{density}': [] for density in densities})
    times.update({f'time-per-concept-{method}-d{density}': [] for density in densities for method in methods})
    for density in tables:
        for method in methods:
            times[f'{method}-d{density}'] = []
    print(','.join(times.keys()))
    for size in range(size_start, table_size+1, size_step):
        times['context-size'].append(size)
        for density, table in tables.items():
            data = ''.join(table_to_asp(table, maxsize=size))
            nb_concept = nb_concepts(data)
            times[f'nb-concept-d{density}'].append(nb_concept)
            for method, runner in methods.items():
                runtime = runner(data)
                times[f'{method}-d{density}'].append(runtime)
                times[f'time-per-concept-{method}-d{density}'].append(nb_concept / runtime)
        print(','.join(str(times[key][-1]) for key in times.keys()))


benchmark(table_size=21, size_start=8, size_step=1, methods={
    'nextclosure': run_nextclosure,
    'standard': run_standard,
})
print()
benchmark(table_size=100, size_start=10, size_step=5, methods={
    'standard': run_standard,
})
print()
benchmark(densities=(0.1, 0.2, 0.3, 0.4), table_size=100, size_start=10, size_step=5, methods={
    'standard': run_standard,
})
