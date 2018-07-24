import re
import math
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statistics import median

from constants import bins_axis_names, bin_dimensions_regex, boat_speed_feature, \
                    boxplot_axis_name, coc_feature_name, feature_regex, identifier_features, \
                    fiber_optics_structure_features, fiber_optics_appendix_features, \
                    other_sensor_features, statistics_features, wind_features
from plot_bins import compute_sorted_corr, create_if_not_exist, \
                    plot_boxplot, plot_corr, plot_wind_angle_speed, \
                    preprocess_data, read_csv, sort_corr

# Bins to analyse.
bin_keys = ['bin_x{}to{}_y{}to{}'.format(x_min, x_max, y_min, y_max) for x_min, x_max, y_min, y_max in [(-95, -90, 8, 10),
                                                                                                        (-145, -140, 22, 24),
                                                                                                        (50, 55, 16, 18)]]

def create_PCA(df,
            target_feature=boat_speed_feature[1],
            var_thresh=.75,
            column_name='PC_{}',
            exclude=[x[1] for x in identifier_features + wind_features]):
    """Create Principal Component Analysis"""
    df = df.drop(exclude, axis=1)
    df.dropna(axis=1, how='all', inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(df.mean(), inplace=True)
    X, y = StandardScaler().fit_transform(df.drop(target_feature, axis=1).reset_index()), df[target_feature].reset_index()
    pca = PCA(var_thresh)
    principal_components = pca.fit_transform(X)
    return pca, pd.concat([pd.DataFrame(data=principal_components, columns=[column_name.format(i+1) for i in range(0, len(principal_components[0]))]), y], axis=1).drop(['index'], axis=1)

def create_bins(df,
                wind_features=[x[1] for x in wind_features],
                target_feature=boat_speed_feature[1],
                statistics_cols=statistics_features,
                dx=5, dy=2, min_thresh=5,
                exclude=[x[1] for x in identifier_features + wind_features],
                target_bins=bin_keys):
    """Create bins"""
    print('Creating bins with size {}˚ by {} knots...'.format(dx, dy))
    bins = {}
    for max_x in range(-180, 180, dx):
        for max_y in range(0, math.ceil(df[wind_features[1]].max()), dy):
            binned_df = df.query('{0} >= {2} and {0} < {2}+{4} and {1} >= {3} and {1} < {3}+{5}'.format(wind_features[0], wind_features[1],
                                                                                                        max_x, max_y,
                                                                                                        dx, dy))
            bin_name = 'bin_x{}to{}_y{}to{}'.format(max_x, max_x+dx, max_y, max_y+dy)
            if bin_name in target_bins:
                bin_size = len(binned_df.index)
                bin_corr, unsorted_corr = compute_sorted_corr(binned_df.drop(exclude, axis=1))
                if bin_size >= min_thresh and bin_corr is not None:
                    pca, pca_df = create_PCA(binned_df)
                    bins[bin_name] = {'bin': binned_df,
                                    'size': bin_size,
                                    'corr': bin_corr,
                                    'corr_list': pd.DataFrame(data=sort_corr(unsorted_corr, num_features=50), columns=statistics_cols),
                                    'pca': pca,
                                    'pca_df': pca_df}
                    print('Bin {} created!'.format(bin_name))
                    print('Bin size: {}.'.format(bin_size))
    print('{} bins created!'.format(len(bins)))
    return bins, dx, dy, max_x, max_y

def plot_circle_of_correlations(pc_infos,
                            ebouli,
                            pairs,
                            columns,
                            base_path, plot_fname, guide_fname,
                            feature_name=coc_feature_name):
    """Plot the circle of correlation"""
    create_if_not_exist(base_path)
    plot_path = '{}/{}.pdf'.format(base_path, plot_fname)
    guide_path = '{}/{}.csv'.format(base_path, guide_fname)
    print('Saving plot to {}.'.format(plot_path))
    print('Saving guide to {}.'.format(guide_path))
    (pc_1, pc_2) = pairs
    pc_infos[feature_name] = columns[:len(pc_infos.index)]
    pc_infos.sort_values(by=['PC_{}'.format(pc_1)], ascending=False, inplace=True)
    plt.Circle((0,0), radius=10, color='g', fill=False)
    circle1 = plt.Circle((0, 0), radius=1, color='g', fill=False)
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    for idx in range(len(pc_infos['PC_{}'.format(pc_1)])):
        x = pc_infos['PC_{}'.format(pc_1)][idx]
        y = pc_infos['PC_{}'.format(pc_2)][idx]
        plt.plot([0.0, x], [0.0, y], 'k-')
        plt.plot(x, y, 'rx')
        plt.annotate(pc_infos.index[idx], xy=(x, y), fontsize=7.5)
    plt.xlabel('{} ({}%%)'.format('PC_{}'.format(pc_1), str(ebouli[0])[:4].lstrip('0.')))
    plt.ylabel('{} ({}%%)'.format('PC_{}'.format(pc_2), str(ebouli[1])[:4].lstrip('0.')))
    plt.xlim((-1, 1))
    plt.ylim((-1, 1))
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.clf()
    pd.DataFrame(data={'Label': [label+1 for label in range(len(pc_infos.index))],
                    'Feature': [feature for feature in pc_infos[feature_name].values[:len(pc_infos.index)]]}) \
                .to_csv(guide_path, sep=';', index=False)

if __name__ == '__main__':
    print('Initializing bins analysis...')
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
    bins, dx, dy, _, max_y = create_bins(df)

    # Plot and save the bins.
    print('------------------------------------------')
    print('Creating plots...')
    reports_path = './reports/{}/analysis'.format(version)
    for bin_name, bin_items in bins.items():
        binned_df, bin_corr, bin_corr_list, bin_pca, bin_pca_df = \
                bin_items['bin'], bin_items['corr'], bin_items['corr_list'], bin_items['pca'], bin_items['pca_df']
        bin_reports_path = '{}/{}'.format(reports_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, x_start, y_start, x_finish, y_finish, dx, dy, 3, bin_reports_path, 'bin')
        plot_boxplot(binned_df, bin_reports_path, 'boxplot')
        plot_corr(bin_corr, bin_reports_path, 'corr')
        bin_corr_list.to_csv('{}/corr_list.csv'.format(bin_reports_path), sep=';', index=False)
        bin_pca_df.to_csv('{}/pca.csv'.format(bin_reports_path), sep=';', index=False)
        circle_of_corr_reports_path = '{}/{}'.format(bin_reports_path, 'circle_of_corr')
        for pc_1 in range(1, 5+1):
            for pc_2 in range(pc_1, 5+1):
                if pc_1 != pc_2:
                    ebouli = pd.Series(bin_pca.explained_variance_ratio_)
                    plot_circle_of_correlations(pd.DataFrame(np.transpose(bin_pca.components_),
                                                        columns=['PC_{}'.format(i) for i in range(len(ebouli))]),
                                        ebouli,
                                        (pc_1, pc_2),
                                        binned_df.drop([x[1] for x in identifier_features + wind_features], axis=1).columns.values,
                                        circle_of_corr_reports_path, 'coc_{}_{}'.format(pc_1, pc_2), 'guide_{}_{}'.format(pc_1, pc_2))
    print('All plots saved!')

    print('------------------------------------------')
    print('Bins analysis finished!')
