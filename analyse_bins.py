import re
import sys
import warnings

import matplotlib.pyplot as plt

from statistics import median

from constants import bins_axis_names, bin_dimensions_regex, boat_speed_feature, \
                    boxplot_axis_name, feature_regex, identifier_features, \
                    fiber_optics_structure_features, fiber_optics_appendix_features, \
                    other_sensor_features, statistics_features, wind_features
from plot_bins import compute_sorted_corr, create_bins, create_if_not_exist, \
                    plot_boxplot, plot_corr, plot_wind_angle_speed, \
                    preprocess_data, read_csv, sort_corr

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

    # Bins to analyse.
    bin_keys = ['bin_x{}to{}_y{}to{}'.format(x_min, x_max, y_min, y_max) for x_min, x_max, y_min, y_max in [(-55, -50, 16, 18),
                                                                                                            (-95, -90, 8, 10),
                                                                                                            (-145, -140, 22, 24),
                                                                                                            (50, 55, 16, 18),
                                                                                                            (140, 145, 22, 24)]]

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
    reports_path = './reports/{}/analysis'.format(version)
    for bin_name, bin_items in { key: bins[key] for key in bin_keys }.items():
        binned_df, bin_corr = bin_items['bin'], bin_items['corr']
        bin_reports_path = '{}/{}'.format(reports_path, bin_name)
        x_start, x_finish, y_start, y_finish = [int(s) for s in re.findall(bin_dimensions_regex, bin_name)]
        dx, dy = (x_finish-x_start)/4.0, (y_finish-y_start)/4.0
        plot_wind_angle_speed(binned_df, x_start, y_start, x_finish, y_finish, dx, dy, 3, bin_reports_path, 'bin')
        plot_boxplot(binned_df, bin_reports_path, 'boxplot')
        plot_corr(bin_corr, bin_reports_path, 'corr')
    print('All plots saved!')

    print('------------------------------------------')
    print('Bins analysis finished!')
