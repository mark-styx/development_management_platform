# general overhead
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime as dt

# path tools
from glob import glob
from pathlib import Path
from os.path import abspath
from os.path import dirname
from os.path import basename
from inspect import getsourcefile


current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))

def get_entities_loc(current_dir):
    entities = []
    main_content = list(Path(dirname(current_dir)).glob('*'))
    for item in main_content:
        if '.py' in str(item) or '.cfg' in str(item) or '.json' in str(item):
            entities.append(item)
        if os.path.isdir(item):
            sub_content = list(item.glob('*'))
            for _item in sub_content:
                if '.py' in str(_item) or '.cfg' in str(_item) or '.json' in str(item):
                    entities.append(_item)
                if os.path.isdir(_item):
                    _sub_content = list(_item.glob('*'))
                    for __item in _sub_content:
                        if '.py' in str(__item) or '.cfg' in str(__item) or '.json' in str(__item):
                            entities.append(__item)
    return entities

def import_ref_finder(fpath):
    with open(fpath,'r') as f:
            data = f.read()
    _fr = lambda data: data.find('from ')
    _im = lambda data: data.find('import ')
    _ff = lambda data: data.find('module_from_file(')
    data = data.replace('module_from_file(module_name','')
    fr,im,ff = [],[],[]
    while _fr(data) != -1:
        s = data[_fr(data):(data[_fr(data):].find('\n')) + _fr(data)]
        fr.append(s);data = data.replace(s,'')
    while _im(data) != -1:
        s = data[_im(data):(data[_im(data):].find('\n')) + _im(data)]
        im.append(s);data = data.replace(s,'')
    while _ff(data) != -1:
        s = data[_ff(data):(data[_ff(data):].find(','))+ _ff(data)]
        ff.append(s[17:]);data = data.replace(s,'')
    return fr,im,ff

def import_ref_parse(from_list,imp_list,frf_list):
    fr_refs = [x[5:x[5:].find(' ') + 6] for x in from_list]
    im_refs = [x[7:] for x in imp_list]
    repl = lambda X: X.replace(X[X.find('.'):],'')
    for idx, x in enumerate(im_refs):
        if '.' in x: im_refs[idx] = repl(x)
    for idx, x in enumerate(fr_refs):
        if '.' in x: fr_refs[idx] = repl(x)
    frf_list = [x for x in frf_list if x != 'self']
    rem_dups = lambda X: list(set([x.strip() for x in X]))
    return rem_dups(fr_refs),rem_dups(im_refs),rem_dups(frf_list)

def doc_crawler(fpath,entities):
    with open(fpath,'r') as f:
        data = f.read()
    search = lambda x: data.find(x) > -1
    refs = []
    for ent in entities:
        if search(ent): refs.append(ent)
    return refs

ent_loc = [x for x in get_entities_loc(current_dir) if 'cpython' not in str(x)]
entities = [x.replace('.py','') for x in [basename(x) for x in ent_loc]]
emap = {x:{'loc':y} for x,y in zip(entities,ent_loc)}
docs = []

for x in emap:
    emap[x]['refs'] = []
    emap[x]['cat']=''
    if '.' not in x: emap[x]['cat'] = 'module'
    if '.cfg' in x: emap[x]['cat'] = 'configuration'
    if '.json' in x: emap[x]['cat'] = 'output'
    if emap[x]['cat'] in ['configuration','output']: docs.append(x)

for x in emap:
    if emap[x]['cat'] == 'module':
        fr,im,ff = import_ref_finder(emap[x]['loc'])
        fr,im,ff = import_ref_parse(fr,im,ff)
        frimff = []
        for _ in fr: frimff.append(_)
        for _ in im: frimff.append(_)
        for _ in ff: frimff.append(_)
        frimff = [x.strip("'") for x in frimff]
        emap[x]['refs'] = [x for x in frimff if x in entities]
        for ent in set(doc_crawler(emap[x]['loc'],docs)): emap[x]['refs'].append(ent)
df = pd.DataFrame(emap)
df = df.T
df = df.reset_index()

froms = [];tos = []
for idx in range(len(df)):
    for x in df['refs'].iloc[idx]:
        froms.append(df['index'].iloc[idx])
        tos.append(x)
netdf = pd.DataFrame();netdf['from'] = froms;netdf['to']=tos

G = nx.from_pandas_edgelist(netdf, 'from', 'to')
fig = plt.figure()
nx.draw(G,with_labels=True,node_color='#0066cc',node_size=1500,edge_color='#99ff33',font_color='white')
fig.set_facecolor('#333333')
fig.set_size_inches(18.5, 10.5)
fig.savefig('entity_map.png',dpi=800,facecolor='#333333',pad_inches=0)