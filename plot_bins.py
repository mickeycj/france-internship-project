import math
import os
import re
import sys

import chardet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from constants import *

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

def transform_columns(df, identifier_cols, cols_to_transform, other_cols, regex):
    """Transform the dataset"""
    print('Transforming columns...')
    transformed_df = pd.DataFrame()
    for old_col, new_col in identifier_cols + cols_to_transform + other_cols:
        if (old_col, new_col) not in identifier_cols + other_cols:
            transformed_df[new_col] = df.filter(regex=(regex.format(old_col))).mean(axis=1)
        else:
            transformed_df[new_col] = df[old_col]
    print('Columns transformed!')
    return transformed_df

def create_bins(df, wind_features, dx=bin_angles[0], dy=1, min_thresh=10, tries=0):
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
                    return create_bins(df, wind_features, dx=bin_angles[tries+1], dy=dy+1, min_thresh=min_thresh, tries=tries+1)
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

def plot_wind_angle_speed(df, wind_features, axis_names, x_start, y_start, x_finish, y_finish, dx, dy, markersize, base_path, fname):
    """Plot the wind angle-speed space"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    plt.xlabel(axis_names[0])
    plt.ylabel(axis_names[1])
    plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    plt.xticks(np.arange(x_start, x_finish, dx))
    plt.yticks(np.arange(y_start, y_finish, dy))
    plt.grid(lw=.75)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_boxplot(df, target_feature, axis_name, base_path, fname):
    """Plot the boxplot for boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    df.boxplot(column=target_feature, showfliers=df[target_feature].median() == df[target_feature].mode().iloc[0])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel(axis_name)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

def plot_corr(df, target_feature, num_features, base_path, fname):
    """Plot the correlations with boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}'.format(path))
    corrs = {}
    for col in df.columns:
        if col != target_feature:
            corr = df[target_feature].corr(df[col])
            if not math.isnan(corr):
                corrs[col] = corr
    sorted_corrs = sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True)[:num_features]
    sorted_corrs = sorted(sorted_corrs, key=lambda x: x[1], reverse=True)
    cols = [target_feature] + [x[0] for x in sorted_corrs]
    corr = df[cols].corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, lw=.75)
    plt.xticks(rotation=30, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    create_if_not_exist(base_path)
    plt.savefig(path)
    plt.clf()

print('Initializing bins creation...')

# Ignore PyPlot warning.
print('Setting up PyPlot...')
plt.rcParams.update({'figure.max_open_warning': 0})

# Command line arguments.
print('Retrieving command line arguments...')
version = sys.argv[1]
fnames = sys.argv[2:]

# Data path.
print('Setting up path to data...')
data_path = './data/{}'.format(version)

# Read from CSV file(s).
print('------------------------------------------')
df = read_csv(map(lambda arg: '{}/{}.csv'.format(data_path, arg), fnames))

# Transform the dataset to decrease the number of features.
print('------------------------------------------')
df = transform_columns(df,
                    identifier_features,
                    fiber_optics_structure_features + fiber_optics_appendix_features,
                    other_sensor_features + wind_features + [boat_speed_feature],
                    feature_regex)

# Create different-sized bins.
bin_sizes = [10, 50, 100]
for min_thresh in bin_sizes:
    print('------------------------------------------')
    # Determine the size of the bins.
    print('Creating bins with minimum size of {}.'.format(min_thresh))
    bins, dx, dy, _, max_y = create_bins(df, [x[1] for x in wind_features], min_thresh=min_thresh)

    # Plot and save the bins.
    print('Creating plots...')
    reports_path = './reports/{}/min_thresh_{}'.format(version, min_thresh)
    plot_wind_angle_speed(df, [x[1] for x in wind_features], bins_axis_names, -180, 0, 180+1, max_y+1, dx, dy, 0.25, reports_path, 'bins')
    reports_path = '{}/bins'.format(reports_path)
    for bin_name, binned_df in bins.items():
        bin_reports_path = '{}/{}'.format(reports_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, [x[1] for x in wind_features], bins_axis_names, x_start, y_start, x_finish+dx, y_finish+dy, dx, dy, 3, bin_reports_path, 'bin')
        plot_boxplot(binned_df, boat_speed_feature[1], boxplot_axis_name, bin_reports_path, 'boxplot')
        plot_corr(binned_df.drop([x[1] for x in identifier_features + wind_features], axis=1), boat_speed_feature[1], 20, bin_reports_path, 'corr')
    print('All plots saved!')
print('------------------------------------------')
print('Bins creation finished!')
