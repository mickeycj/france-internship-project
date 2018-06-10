import cols
import pandas as pd
import sys, utils

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

def find_corr_of(df, target, exclude=[]):
    import math

    for col in df.drop(exclude, axis=1).columns:
        if col != target:
            corr = df[target].corr(df[col])
            if not math.isnan(corr):
                yield (col, corr)

def write_corr(df_corr, fname):
    import os

    path = './report'
    if not os.path.exists(path):
        os.makedirs(path)
    with open('{}/{}.csv'.format(path, fname), 'w') as f:
        f.write('feature, corr_with_speed\n')
        for col, corr in sorted(list(df_corr), key=lambda x: x[1], reverse=True):
            f.write('{}, {:.4f}\n'.format(col, corr))

def plot_corr(df, fname):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import seaborn as sns

    path = './report'
    if not os.path.exists(path):
        os.makedirs(path)
    _, ax = plt.subplots(figsize=(14, 10))
    corr = df.corr()
    sns.heatmap(corr,
                mask=np.zeros_like(corr, dtype=np.bool),
                cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True,
                ax=ax).get_figure().savefig('{}/{}.pdf'.format(path,fname))

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# The column names to be reduced/combined.
fname = sys.argv[2]
if fname == 'max_min':
    cols = cols.max_min()
elif fname == 'avg':
    cols = cols.avg()
else:
    print('Invalid file name!')
    exit()

# Reduce different sensors from the same location to the same columns and print the result.
transformed_df = transform(df.copy(deep=True), cols, '{}.*')
# utils.print_data(transformed_df.head(10), 7)

# Find the correlation between the speed of the boat with different sensors.
write_corr(find_corr_of(transformed_df, 'WTP_SelBoatSpd', exclude=['date TU', 'heure TU', 'latitude', 'longitude']), '{}_corr'.format(fname))

# Plot the correlation matrix.
plot_corr(transformed_df, '{}_corr'.format(fname))
