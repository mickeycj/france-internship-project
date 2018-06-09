def read_csv(fname):
    import pandas as pd

    return pd.read_csv(fname, sep=';')

def transform(df, new_cols, regex):
    for col in new_cols:
        filtered = df.filter(regex=(regex.format(col)))
        df[col] = filtered.mean(axis=1)
        df.drop(filtered.columns, axis=1, inplace=True)
    return df

def print_data(df, steps):
    i = 0
    while i<len(df.keys()):
        print('{}\n'.format(df.iloc[:, i:i+steps]))
        i+=steps

def find_corr_of(df, target):
    import math

    for col in df.drop(['date TU', 'heure TU', 'latitude', 'longitude'], axis=1).columns:
        if col != target:
            corr = df[target].corr(df[col])
            if not math.isnan(corr):
                yield (col, corr)

def print_corr(df_corr):
    for col, corr in sorted(list(df_corr), key=lambda x: x[1], reverse=True):
        print('{}: {:.4f}'.format(col, corr))

def plot_corr(df):
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns

    _, ax = plt.subplots(figsize=(14, 10))
    corr = df.corr()
    sns.heatmap(corr,
                mask=np.zeros_like(corr, dtype=np.bool),
                cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True,
                ax=ax)
    plt.show()
