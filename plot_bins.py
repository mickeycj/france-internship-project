import math
import os
import re
import shutil
import sys
import warnings

import chardet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from statistics import median

from constants import bins_axis_names, bin_dimensions_regex, boat_speed_feature, \
                    boxplot_axis_name, feature_regex, identifier_features, \
                    fiber_optics_structure_features, fiber_optics_appendix_features, \
                    other_sensor_features, statistics_features, wind_features

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

def preprocess_data(df,
                identifier_cols=identifier_features,
                cols_to_preprocess=fiber_optics_structure_features + fiber_optics_appendix_features,
                other_cols=other_sensor_features + wind_features + [boat_speed_feature],
                regex=feature_regex):
    """Preprocess the dataset"""
    print('Preprocessing data...')
    preprocessed_df = pd.DataFrame()
    for old_col, new_col in identifier_cols + cols_to_preprocess + other_cols:
        if (old_col, new_col) in identifier_cols + other_cols:
            preprocessed_df[new_col] = df[old_col]
        else:
            preprocessed_df[new_col] = df.filter(regex=(regex.format(old_col))).mean(axis=1)
    preprocessed_df.fillna(0, inplace=True)
    print('Preprocessing completed!')
    return preprocessed_df

def sort_corr(corr, num_features=20):
    """Sort correlation dictionary"""
    sorted_corr = sorted(corr.items(), key=lambda x: abs(x[1]), reverse=True)[:num_features]
    return sorted(sorted_corr, key=lambda x: x[1], reverse=True)

def compute_sorted_corr(df, target_feature=boat_speed_feature[1], num_features=20):
    """Compute sorted correlated features with the target feature"""
    corr = {}
    for col in df.columns:
        if col != target_feature:
            f_corr = df[target_feature].corr(df[col])
            if not math.isnan(f_corr):
                corr[col] = f_corr
    cols = [target_feature] + [x[0] for x in sort_corr(corr)]
    if len(cols) <= 1:
        return None, None
    return df[cols].corr(), corr

def create_bins(df,
                wind_features=[x[1] for x in wind_features],
                target_feature=boat_speed_feature[1],
                statistics_cols=statistics_features,
                dx=5, dy=2, min_thresh=5,
                exclude=[x[1] for x in identifier_features + wind_features]):
    """Create bins"""
    print('Creating bins with size {}˚ by {} knots...'.format(dx, dy))
    bins, corr = {}, {}
    for max_x in range(-180, 180, dx):
        for max_y in range(0, math.ceil(df[wind_features[1]].max()), dy):
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} and {1} >= {3} and {1} < {3}+{5}'.format(wind_features[0], wind_features[1],
                                                                                                        max_x, max_y,
                                                                                                        dx, dy))
            bin_size = len(binned_df.index)
            bin_corr, unsorted_corr = compute_sorted_corr(binned_df.drop(exclude, axis=1))
            if bin_size >= min_thresh and bin_corr is not None:
                bin_name = 'bin_x{}to{}_y{}to{}'.format(max_x, max_x+dx, max_y, max_y+dy)
                for col, c_corr in unsorted_corr.items():
                    if col in corr:
                        corr[col].append(c_corr)
                    else:
                        corr[col] = [c_corr]
                bins[bin_name] = {'bin': binned_df, 'size': bin_size, 'corr': bin_corr}
                print('Bin {} created!'.format(bin_name))
                print('Bin size: {}.'.format(bin_size))
    print('{} bins created!'.format(len(bins)))
    return bins, \
        dx, dy, \
        max_x, max_y, \
        pd.DataFrame(data=sort_corr({col: median(c_corr) for col, c_corr in corr.items()}),
                    columns=statistics_cols)

def create_if_not_exist(path):
    """Create a directory if not exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print('Directory {} created!'.format(path))

def plot_wind_angle_speed(df,
                        x_start, y_start,
                        x_finish, y_finish,
                        dx, dy,
                        markersize,
                        base_path, fname,
                        wind_features=[x[1] for x in wind_features],
                        axis_names=bins_axis_names,
                        main=False):
    """Plot the wind angle-speed space"""
    create_if_not_exist(base_path)
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}.'.format(path))
    _, ax = plt.subplots()
    ax.set_xlabel(axis_names[0])
    ax.set_ylabel(axis_names[1])
    ax.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=markersize)
    if main:
        ax.set_xticks(np.arange(x_start, x_finish, dx*6))
        ax.set_xticks(np.arange(x_start, x_finish, dx), minor=True)
        ax.set_yticks(np.arange(y_start, y_finish, dy))
        ax.grid(which='both', lw=.75)
    else:
        ax.set_xlim(x_start, x_finish)
        ax.set_ylim(y_start, y_finish)
        ax.grid(lw=.75)
    plt.tight_layout()
    plt.savefig(path)
    plt.clf()

def plot_boxplot(df,
                base_path, fname,
                target_feature=boat_speed_feature[1],
                axis_name=boxplot_axis_name):
    """Plot the boxplot for boat speed"""
    create_if_not_exist(base_path)
    path = '{}/{}.pdf'.format(base_path, fname)
    print('Saving plot to {}.'.format(path))
    ax = df.boxplot(column=target_feature,
                    showfliers=df[target_feature].median() == df[target_feature].mode().iloc[0],
                    return_type='axes')
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.set_ylabel(axis_name)
    plt.tight_layout()
    plt.savefig(path)
    plt.clf()

def plot_corr(corr, base_path, fname):
    """Plot the correlations with boat speed"""
    path = '{}/{}.pdf'.format(base_path, fname)
    create_if_not_exist(base_path)
    print('Saving plot to {}.'.format(path))
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, lw=.75)
    plt.xticks(rotation=30, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    plt.savefig(path)
    plt.clf()

if __name__ == '__main__':
    print('Initializing bins creation...')
    print('------------------------------------------')

    # Command line arguments.
    print('Retrieving command line arguments...')
    version = sys.argv[1]
    fnames = sys.argv[2:]

    # Ignore RunTimeWarning.
    print('Setting up warning...')
    warnings.filterwarnings('ignore')

    # Ignore PyPlot warning.
    print('Setting up PyPlot...')
    plt.rcParams.update({'figure.max_open_warning': 0})

    # Data path.
    print('Setting up data path...')
    data_path = './data/{}'.format(version)

    # Read from CSV file(s).
    print('------------------------------------------')
    df = read_csv(map(lambda fname: '{}/{}.csv'.format(data_path, fname), fnames))

    # Preprocess the dataset.
    print('------------------------------------------')
    df = preprocess_data(df)

    # Create the bins.
    print('------------------------------------------')
    bins, dx, dy, _, max_y, sorted_corr_df = create_bins(df)

    # Plot and save the bins.
    print('------------------------------------------')
    print('Creating plots...')
    reports_path = './reports/{}/initial'.format(version)
    plot_wind_angle_speed(df, -180, 0, 180+1, max_y+1, dx, dy, 0.25, reports_path, 'bins', main=True)
    sorted_corr_df.to_csv('{}/corr.csv'.format(reports_path), sep=';', index=False)
    reports_path = '{}/bins'.format(reports_path)
    for bin_name, bin_items in bins.items():
        binned_df, bin_corr = bin_items['bin'], bin_items['corr']
        bin_reports_path = '{}/{}'.format(reports_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, x_start, y_start, x_finish, y_finish, dx, dy, 3, bin_reports_path, 'bin')
        plot_boxplot(binned_df, bin_reports_path, 'boxplot')
        plot_corr(bin_corr, bin_reports_path, 'corr')
    print('All plots saved!')

    print('------------------------------------------')
    print('Bins creation finished!')
