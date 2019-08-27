

import timeit
import altair as alt
import pandas as pd

def activate():
    if alt.renderers.active != 'notebook':
        alt.renderers.enable('notebook')


def mk_insert_and_lookup(hs, count):
    def insert_and_lookup(k):
        if hasattr(hs, 'add'):
            hs.add(k)
            hs.contains(k)
        else:
            hs.insert(k)
            hs.lookup(k)   
    
    def result():
        for i in range(count):
            insert_and_lookup(i)
    
    return result


from math import log

def hash_experiment(thing, low, high):
    activate()
    results = []
    for f in range(6, 18):
        il = mk_insert_and_lookup(thing, 1 << f)
        trials = int(50000.0 / (1 << (f - 2)))
        tm = timeit.timeit(mk_insert_and_lookup(thing, 1 << f), number=trials)
        results.append((1 << f, (float(tm) / (1 << f) / trials) * 1000000))
    
    df = pd.DataFrame(results)
    df.columns = ["elements", "avgtime"]
    
    return alt.Chart(df).mark_line().encode(alt.X("elements", scale=alt.Scale(type="log", base=2)), y="avgtime").interactive()