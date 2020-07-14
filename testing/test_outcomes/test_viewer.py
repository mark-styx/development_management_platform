import pandas as pd
import seaborn as sns
sns.set(style='darkgrid')

with open('test_results.json','r') as f: df = pd.read_json(f)

def write_plot(module):
    plot = sns.catplot(
        x='outcome',y='counts',hue='test_function',
        data=agged[['outcome','test_function','counts']][agged['test_module']==module],
        kind='bar',palette="Blues_d"
        ).set(
            title=f'{module.capitalize()} Test Case Results'
        )
    return plot

df = df.T
df['counts'] = 0
agged = df[['test_module','outcome','test_function','counts']].groupby(['test_module','test_function','outcome']).agg('count')
agged = agged.reset_index()
modules = agged['test_module'].unique()

plots = {}
for mod in modules: plots[mod] = write_plot(mod)
