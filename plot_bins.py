import math
import os
import re
import sys

import chardet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Ignore PyPlot warning.
plt.rcParams.update({'figure.max_open_warning': 0})

# Command line arguments.
version = sys.argv[1]
fnames = sys.argv[2:]

# Data path.
data_path = './data/{}'.format(version)

# Possible bin angles.
bin_angles = [5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72]

# List of relevant features and axis names.
if version =='v1':
    wind_features = ['WTP_AW_angle', 'WTP_AW_speed']
    boat_speed_feature = 'WTP_SelBoatSpd'
elif version =='v2':
    wind_features = ['VarFilter_WTP_AW_angle', 'VarFilter_WTP_AW_speed']
    boat_speed_feature = 'VarFilter_WTP_SelBoatSpd'
else:
    print('This version number does not exist!')
    exit()
bins_axis_names = ['Wind Angle (˚)', 'Wind Speed (knot)']
boxplot_axis_name = 'Boat Speed (knot)'

# Regular expressions.
feature_regex = r'.*{}.*'
bin_dimensions_regex = r'[+-]?\d+'

def read_csv(fnames):
    """Read CSV file(s) to a Pandas Dataframe"""
    print('Creating dataframe...')
    def detect_and_read(fname):
        with open(fname, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
            print('File {}\'s encoding: {}'.format(fname, encoding))
            return pd.read_csv(fname, sep=';', encoding=encoding)
    df = pd.concat(map(lambda fname: detect_and_read(fname), fnames), sort=False)
    print('Dataframe created!')
    return df

def transform_columns(df, new_cols, additional_cols, regex):
    """Transform the dataset"""
    print('Transforming columns...')
    transformed_df = pd.DataFrame()
    for col in new_cols + additional_cols:
        if col not in additional_cols:
            transformed_df[col] = df.filter(regex=(regex.format(col))).mean(axis=1)
        else:
            transformed_df[col] = df[col]
    print('Columns transformed!')
    return transformed_df

def create_bins(df, dx=bin_angles[0], dy=1, min_thresh=10, tries=0):
    """Create bins"""
    if tries == 0:
        print('Creating bins...')
    else:
        print('Bin\'s size adjusted. Tries: {}'.format(tries))
    bins = {}
    max_x = -180
    while max_x < 180:
        max_y = 0
        while max_y < math.ceil(df[wind_features[1]].max()):
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} & {1} >= {3} & {1} < {3}+{5}'.format(wind_features[0], wind_features[1], max_x, max_y, dx, dy))
            if len(binned_df) >= int(math.ceil(min_thresh*0.1)):
                if len(binned_df) < min_thresh:
                    return create_bins(df, dx=bin_angles[tries+1], dy=dy+1, min_thresh=min_thresh, tries=tries+1)
                bins['bin_x{}to{}_y{}to{}'.format(max_x, max_x+dx, max_y, max_y+dy)] = binned_df
            max_y+=dy
        max_x+=dx
    if tries == 0:
        tries_str = '1 try'
    else:
        tries_str = '{} tries'.format(tries+1)
    print('Bins created after {}!'.format(tries_str))
    return bins, dx, dy, max_x, max_y

def create_if_not_exist(path):
    """Create a directory if not exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print('Directory {} created!'.format(path))

def plot_wind_angle_speed(df, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname):
    """Plot the wind angle-speed space"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    plt.xlabel(bins_axis_names[0])
    plt.ylabel(bins_axis_names[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    plt.xticks(np.arange(x_start, x_finish, dx))
    plt.yticks(np.arange(y_start, y_finish, dy))
    plt.grid(lw=.75)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_boxplot(df, base_path, fname):
    """Plot the boxplot for boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    df.boxplot(column=boat_speed_feature, showfliers=df[boat_speed_feature].median() == df[boat_speed_feature].mode().iloc[0])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel(boxplot_axis_name)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_corr(df, num_features, base_path, fname):
    """Plot the correlations with boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    corrs = {}
    for col in df.drop(wind_features, axis=1).columns:
        if col != boat_speed_feature:
            corr = df[boat_speed_feature].corr(df[col])
            if not math.isnan(corr):
                corrs[col] = corr
    sorted_corrs = sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True)[:num_features]
    sorted_corrs = sorted(sorted_corrs, key=lambda x: x[1], reverse=True)
    cols = [boat_speed_feature] + [x[0] for x in sorted_corrs]
    corr = df[cols].corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, lw=.75)
    plt.xticks(rotation=30, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

print('Initializing bins creation...')
print('------------------------------------------')
# Read from CSV file(s).
df = read_csv(map(lambda arg: '{}/{}.csv'.format(data_path, arg), fnames))

print('------------------------------------------')
# Transform the dataset to decrease the number of features.
df = transform_columns(df,
                    ['1s_FBM_P_lfwd', '1s_FBM_P_uaft', '1s_FBM_P_ufwd',
                    '1s_FBM_S_laft', '1s_FBM_S_lfwd', '1s_FBM_S_uaft', '1s_FBM_S_ufwd',
                    '1s_HUL_C_lport', '1s_HUL_C_lstbd', '1s_HUL_C_uport', '1s_HUL_C_ustbd',
                    '1s_HUL_P_lport', '1s_HUL_P_lstbd', '1s_HUL_P_uport', '1s_HUL_P_ustbd',
                    '1s_HUL_S_lport', '1s_HUL_S_lstbd', '1s_HUL_S_uport', '1s_HUL_S_ustbd',
                    '1s_Foil_B_P_01_i', '1s_Foil_B_P_01_o',
                    '1s_Foil_B_S_01_i', '1s_Foil_B_S_01_o',
                    '1s_Foil_ELE_C_01_p', '1s_Foil_ELE_C_01_s',
                    '1s_Foil_ELE_LOAD_P', '1s_Foil_ELE_LOAD_S'],
                    wind_features + [boat_speed_feature],
                    feature_regex)

# Create different-sized bins.
bin_sizes = [10, 50, 100]
for min_thresh in bin_sizes:
    print('------------------------------------------')
    # Determine the size of the bins.
    print('Creating bins with minimum size of {}.'.format(min_thresh))
    bins, dx, dy, _, max_y = create_bins(df, min_thresh=min_thresh)

    # Plot and save the bins.
    print('Creating plots...')
    reports_path = './reports/{}/min_thresh_{}'.format(version, min_thresh)
    plot_wind_angle_speed(df, -180, 0, 180+1, max_y+1, dx, dy, 0.25, reports_path, 'bins')
    reports_path = '{}/bins'.format(reports_path)
    for bin_name, binned_df in bins.items():
        bin_reports_path = '{}/{}'.format(reports_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, bin_reports_path, 'bin')
        plot_boxplot(binned_df, bin_reports_path, 'boxplot')
        plot_corr(binned_df, 20, bin_reports_path, 'corr')
    print('All plots saved!')
print('------------------------------------------')
print('Bins creation finished!')
