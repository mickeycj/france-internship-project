import pandas as pd
import sys, utils

max_min_cols = ['Max_1s_FBM_P_lfwd', 'Max_1s_FBM_P_uaft', 'Max_1s_FBM_P_ufwd',
                'Max_1s_FBM_S_laft', 'Max_1s_FBM_S_lfwd', 'Max_1s_FBM_S_uaft', 'Max_1s_FBM_S_ufwd',
                'Max_1s_HUL_C_lport', 'Max_1s_HUL_C_lstbd', 'Max_1s_HUL_C_uport', 'Max_1s_HUL_C_ustbd',
                'Max_1s_HUL_P_lport', 'Max_1s_HUL_P_lstbd', 'Max_1s_HUL_P_uport', 'Max_1s_HUL_P_ustbd',
                'Max_1s_HUL_S_lport', 'Max_1s_HUL_S_lstbd', 'Max_1s_HUL_S_uport', 'Max_1s_HUL_S_ustbd',
                'Max_1s_Foil_B_P_01_i', 'Max_1s_Foil_B_P_01_o',
                'Max_1s_Foil_B_S_01_i', 'Max_1s_Foil_B_S_01_o',
                'Max_1s_Foil_ELE_C_01_p', 'Max_1s_Foil_ELE_C_01_s',
                'Max_1s_Foil_ELE_LOAD_P', 'Max_1s_Foil_ELE_LOAD_S',
                'Min_1s_FBM_P_lfwd', 'Min_1s_FBM_P_uaft', 'Min_1s_FBM_P_ufwd',
                'Min_1s_FBM_S_laft', 'Min_1s_FBM_S_lfwd', 'Min_1s_FBM_S_uaft', 'Min_1s_FBM_S_ufwd',
                'Min_1s_HUL_C_lport', 'Min_1s_HUL_C_lstbd', 'Min_1s_HUL_C_uport', 'Min_1s_HUL_C_ustbd',
                'Min_1s_HUL_P_lport', 'Min_1s_HUL_P_lstbd', 'Min_1s_HUL_P_uport', 'Min_1s_HUL_P_ustbd', 
                'Min_1s_HUL_S_lport', 'Min_1s_HUL_S_lstbd', 'Min_1s_HUL_S_uport', 'Min_1s_HUL_S_ustbd',
                'Min_1s_Foil_B_P_01_i', 'Min_1s_Foil_B_P_01_o',
                'Min_1s_Foil_B_S_01_i', 'Min_1s_Foil_B_S_01_o',
                'Min_1s_Foil_ELE_C_01_p', 'Min_1s_Foil_ELE_C_01_s',
                'Min_1s_Foil_ELE_LOAD_P', 'Min_1s_Foil_ELE_LOAD_S']

avg_cols = ['1s_FBM_P_lfwd', '1s_FBM_P_uaft', '1s_FBM_P_ufwd',
            '1s_FBM_S_laft', '1s_FBM_S_lfwd', '1s_FBM_S_uaft', '1s_FBM_S_ufwd',
            '1s_HUL_C_lport', '1s_HUL_C_lstbd', '1s_HUL_C_uport', '1s_HUL_C_ustbd',
            '1s_HUL_P_lport', '1s_HUL_P_lstbd', '1s_HUL_P_uport', '1s_HUL_P_ustbd',
            '1s_HUL_S_lport', '1s_HUL_S_lstbd', '1s_HUL_S_uport', '1s_HUL_S_ustbd',
            '1s_Foil_B_P_01_i', '1s_Foil_B_P_01_o',
            '1s_Foil_B_S_01_i', '1s_Foil_B_S_01_o',
            '1s_Foil_ELE_C_01_p', '1s_Foil_ELE_C_01_s',
            '1s_Foil_ELE_LOAD_P', '1s_Foil_ELE_LOAD_S']

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
    cols = max_min_cols
elif fname == 'avg':
    cols = max_min_cols
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
