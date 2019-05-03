import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore')
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
df = pd.read_csv('data/howpop_train.csv')
print(df.shape)
print(df.head(2).T)
df.drop(filter(lambda c: c.endswith('_lognorm'), df.columns), 
        axis = 1,       # axis = 1: столбцы 
        inplace = True) # избавляет от необходимости сохранять датасет
print(df.describe().T)
print(df.describe(include = ['object', 'bool'] # бинарные и категориальные переменные
           ).T)
# настройка внешнего вида графиков в seaborn
sns.set_style("dark")
sns.set_palette("RdBu")
rcParams['figure.figsize'] = 8, 5
print(df.published.dtype)
df['published'] = pd.to_datetime(df.published, yearfirst = True)
print(df.published.dtype)
df['year'] = [d.year for d in df.published]
df['month'] = [d.month for d in df.published]
df['dayofweek'] = [d.isoweekday() for d in df.published]
df['hour'] = [d.hour for d in df.published]
df.groupby(['year', 'month']).size().sort_values().tail(10).plot(kind='barh')
plt.show()
sns_plot = sns.countplot(x='dayofweek', hue='domain', data=df[(df['year'] == 2015) & (df['month'] == 3)])
plt.show()
sns_plot = sns.pairplot(df[['hour', 'views', 'comments', 'domain']], hue='domain', height=4)
plt.show()
df.groupby('author').agg({
    'post_id': 'count', 'votes_minus': 'mean'
     }).sort_values('post_id').tail(20).votes_minus.plot(kind='barh')
plt.show()
sns_plot = sns.countplot(x='hour', hue='dayofweek', data=df[df['dayofweek'].isin([1, 6])])
plt.show()
